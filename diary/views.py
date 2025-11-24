from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from .models import Entry
from django import forms

class EntryForm(forms.ModelForm):
    class Meta:
        model = Entry
        fields = ['country', 'dish', 'description', 'photo']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }

@login_required
def home(request):
    entries = Entry.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'home.html', {'entries': entries})

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
    return render(request, 'form.html', {'form': form})

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})