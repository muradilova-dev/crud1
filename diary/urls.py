from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('add/', views.add_entry, name='add_entry'),
    path('toggle-favorite/<int:pk>/', views.toggle_favorite, name='toggle_favorite'),
]