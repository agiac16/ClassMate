from django.urls import path
from . import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path("", views.homepage, name='homepage'),
    path("signup/", views.signup_view, name='signup'),
    path('login/', views.login_view, name='login')
]

