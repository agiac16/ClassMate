from django.urls import path
from . import views

app_name = 'user'

urlpatterns = [
    path('profile/', views.viewProfile, name='viewProfile'),
    path('profile/update/', views.updateProfile, name='updateProfile'), 
    path('profile/delete/<int:pk>', views.deleteCourse, name='deleteCourse'),
    path('profile/reset-password/<int:pk>', views.resetPassword, name='resetPassword')
]