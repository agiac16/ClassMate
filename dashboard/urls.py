from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path("", views.dashboard, name='dashboard'),
    path('course/<int:course_id>/', views.course_dashboard, name='course_dashboard'),
    path('add-course/', views.add_course, name='add_course'),
    path('add-assignment/', views.add_assignment, name='add_assignment'),
    path('edit-assignment/<int:assignment_id>/', views.edit_assignment, name='edit_assignment'),
    path('delete-assignment/<int:assignment_id>/', views.delete_assignment, name='delete_assignment'),
    path('bulk-import/', views.bulk_import, name='bulk_import'), 
   path('add-sample-course/', views.add_sample_course, name='add_sample_course'),  # Add this line for the sample course

]
