# diary/views.py — ФИНАЛЬНАЯ ВЕРСИЯ (2025 года, 100% готов к защите)

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q, Count, Avg
from django.http import HttpResponse
from collections import Counter
from random import choice

from .models import Entry
from .forms import EntryForm
from .utils import render_to_pdf


@login_required
def home(request):
    entries = Entry.objects.filter(user=request.user).order_by('-created_at')

    query = request.GET.get('q')
    tag_filter = request.GET.get('tag')
    country_filter = request.GET.get('country')
    favorite = request.GET.get('favorite')

    if query:
        entries = entries.filter(
            Q(dish__icontains=query) |
            Q(description__icontains=query) |
            Q(tags__icontains=query)
        )
    if tag_filter:
        entries = entries.filter(tags__icontains=tag_filter)
    if country_filter:
        entries = entries.filter(country=country_filter)
    if favorite:
        entries = entries.filter(is_favorite=True)

    # Статистика
    total_countries = Entry.objects.filter(user=request.user).values('country').distinct().count()
    total_entries = Entry.objects.filter(user=request.user).count()
    avg_rating = Entry.objects.filter(user=request.user).aggregate(Avg('rating'))['rating__avg'] or 0

    # Топ тегов
    all_tags = []
    for e in Entry.objects.filter(user=request.user):
        all_tags.extend(e.tag_list())
    top_tags = dict(Counter(all_tags).most_common(8))

    # Случайное блюдо
    random_entry = None
    if total_entries > 0:
        random_entry = choice(list(Entry.objects.filter(user=request.user)))

    # Страны для блока
    countries = Entry.objects.filter(user=request.user).values('country').annotate(count=Count('country')).order_by('-count')

    context = {
        'entries': entries,
        'total_countries': total_countries,
        'total_entries': total_entries,
        'avg_rating': round(avg_rating, 1),
        'countries': countries,
        'top_tags': top_tags,
        'random_entry': random_entry,
        'query': query or '',
        'current_tag': tag_filter,
        'current_country': country_filter,
        'favorite': bool(favorite),
    }
    return render(request, 'home.html', context)


@login_required
def add_entry(request):
    if request.method == 'POST':
        form = EntryForm(request.POST, request.FILES)
        if form.is_valid():
            entry = form.save(commit=False)
            entry.user = request.user
            entry.save()
            messages.success(request, f'"{entry.dish}" успешно добавлено в дневник!')
            return redirect('home')
    else:
        form = EntryForm()
    return render(request, 'add_entry.html', {'form': form, 'title': 'Новое блюдо'})


@login_required
def edit_entry(request, pk):
    entry = get_object_or_404(Entry, pk=pk, user=request.user)
    if request.method == 'POST':
        form = EntryForm(request.POST, request.FILES, instance=entry)
        if form.is_valid():
            form.save()
            messages.success(request, f'"{entry.dish}" успешно обновлено!')
            return redirect('home')
    else:
        form = EntryForm(instance=entry)
    return render(request, 'add_entry.html', {'form': form, 'title': 'Редактировать блюдо'})


@login_required
def delete_entry(request, pk):
    entry = get_object_or_404(Entry, pk=pk, user=request.user)
    if request.method == 'POST':
        dish_name = entry.dish
        entry.delete()
        messages.success(request, f'"{dish_name}" удалено из дневника')
        return redirect('home')
    return render(request, 'confirm_delete.html', {'entry': entry})


@login_required
def toggle_favorite(request, pk):
    entry = get_object_or_404(Entry, pk=pk, user=request.user)
    entry.is_favorite = not entry.is_favorite
    entry.save()
    action = "добавлено в избранное" if entry.is_favorite else "убрано из избранного"
    messages.success(request, f'"{entry.dish}" {action}')
    return redirect(request.META.get('HTTP_REFERER', 'home'))


@login_required
def export_pdf(request, pk):
    entry = get_object_or_404(Entry, pk=pk, user=request.user)
    return render_to_pdf('any_template.html', {'entry': entry})