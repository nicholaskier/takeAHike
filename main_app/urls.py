from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('hikes/', views.hikes_index, name='index')
]