from django.contrib import admin
from .models import Entry

@admin.register(Entry)
class EntryAdmin(admin.ModelAdmin):
    list_display = ('dish', 'user', 'country', 'rating', 'created_at')
    list_filter = ('country', 'rating', 'created_at')
    search_fields = ('dish', 'description')