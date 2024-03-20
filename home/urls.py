from django.urls import path
from . import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path("", views.homepage, name='homepage'),
    path("signup/", views.signup, name='signup'),
    path('login/', views.login, name='login')
]

