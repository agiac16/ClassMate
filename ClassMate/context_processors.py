from django.shortcuts import get_object_or_404
from courses.models import Course
from dashboard.views import course_dashboard
from users.models import Student  

def user_courses(request):
    if request.user.is_authenticated:
        student = get_object_or_404(Student, account=request.user)
        user_courses = Course.objects.filter(enrolled_students=student)

        return {'user_courses': user_courses}
    else:
        return {}
    
def all_courses(request):
    courses = Course.objects.all()
    return {'courses': courses}
    
# gets all users courses and adds it to context, can be used in any view now