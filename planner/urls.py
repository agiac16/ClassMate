from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

app_name = 'planner'

urlpatterns = [
    path('weekly/', views.weeklyPlanner, name='weekly'),
    path('monthly/', views.monthlyPlanner, name='monthly'),
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)