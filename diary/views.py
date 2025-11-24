from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Q, Count
from .models import Entry
from django import forms

# Форма
class EntryForm(forms.ModelForm):
    class Meta:
        model = Entry
        fields = ['country', 'dish', 'description', 'photo', 'rating', 'is_favorite']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4, 'class': 'form-control'}),
            'rating': forms.RadioSelect(attrs={'class': 'form-check-input'}),
            'is_favorite': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
        labels = {
            'rating': 'Оценка',
            'is_favorite': 'В избранное ❤️',
        }

@login_required
def home(request):
    entries = Entry.objects.filter(user=request.user)

    # Поиск
    query = request.GET.get('q')
    if query:
        entries = entries.filter(Q(dish__icontains=query) | Q(description__icontains=query))

    # Фильтр по стране
    country = request.GET.get('country')

    # Фильтр по избранному
    favorite = request.GET.get('favorite')

    if favorite:
        entries = entries.filter(is_favorite=True)
    if country:
        entries = entries.filter(country=country)

    entries = entries.order_by('-created_at')

    # Статистика и страны
    countries = Entry.objects.filter(user=request.user).values('country').annotate(count=Count('id')).order_by('country')
    total_countries = countries.count()
    total_entries = Entry.objects.filter(user=request.user).count()

    return render(request, 'home.html', {
        'entries': entries,
        'countries': countries,
        'current_country': country,
        'query': query or '',
        'favorite': favorite,
        'total_countries': total_countries,
        'total_entries': total_entries,
    })

@login_required
def add_entry(request):
    if request.method == 'POST':
        form = EntryForm(request.POST, request.FILES)
        if form.is_valid():
            entry = form.save(commit=False)
            entry.user = request.user
            entry.save()
            return redirect('home')
    else:
        form = EntryForm()
    return render(request, 'form.html', {'form': form, 'title': 'Новая запись'})

@login_required
def toggle_favorite(request, pk):
    entry = get_object_or_404(Entry, pk=pk, user=request.user)
    entry.is_favorite = not entry.is_favorite
    entry.save()
    return redirect('home')