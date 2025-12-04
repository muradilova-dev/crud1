from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('add/', views.add_entry, name='add_entry'),
    path('toggle-favorite/<int:pk>/', views.toggle_favorite, name='toggle_favorite'),
    path('entry/<int:pk>/pdf/', views.export_pdf, name='export_pdf'),
    path('edit/<int:pk>/', views.edit_entry, name='edit_entry'),
]


