from django.urls import path
from . import views

app_name = 'user'

urlpatterns = [
    path('profile/', views.viewProfile, name='viewProfile'),
    path('profile/update/', views.updateProfile, name='updateProfile'),    
]