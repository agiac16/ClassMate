import os
import django
import random
from faker import Faker
from datetime import timedelta

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ClassMate.settings')
django.setup()

from django.contrib.auth.models import User
from myapp.models.student import Student
from myapp.models.friends import Friend
from myapp.models.courses import Course
from myapp.models.forum_threads import ForumThread
from myapp.models.forum_posts import ForumPost
from myapp.models.class_schedules import ClassSchedule
from myapp.models.assignments import Assignment
from myapp.models.additional_activities import AdditionalActivity
from myapp.models.academic_records import AcademicRecord

fake = Faker()

# Create more meaningful fake data for courses
course_data = [
    {"name": "Introduction to Computer Science", "code": 101, "department": "CS", "credits": 4},
    {"name": "Calculus I", "code": 201, "department": "MATH", "credits": 4},
    {"name": "Physics for Engineers", "code": 102, "department": "PHYS", "credits": 3},
    {"name": "Digital Logic Design", "code": 204, "department": "EE", "credits": 3},
    {"name": "Mechanics of Materials", "code": 303, "department": "ME", "credits": 3},
]

# Create and save courses
course_objects = [Course.objects.create(
    course_name=course["name"],
    course_code=course["code"],
    crn=random.randint(10000, 99999),
    department=course["department"],
    credit_hours=course["credits"],
    description=fake.text()
) for course in course_data]

# Create and save students with associated user accounts
students = [Student.objects.create(
    account=User.objects.create_user(username=fake.user_name(), email=fake.email(), password="password"),
    full_name=fake.name(),
    major=random.choice(['Computer Science', 'Electrical Engineering', 'Mechanical Engineering', 'Physics', 'Mathematics']),
    enrollment_year=random.randint(2018, 2022),
    expected_graduation_year=random.randint(2023, 2027)
) for _ in range(20)]

# Create and save friends
for student_obj in students:
    friend_student = random.choice(students)
    if student_obj != friend_student:
        Friend.objects.create(
            user1=student_obj.account,
            user2=friend_student.account,
            status=random.choice(['requested', 'accepted', 'declined'])
        )

# Create and save forum posts and threads


# Create and save class schedules
schedules = [ClassSchedule.objects.create(
    user=student_obj.account,
    course=random.choice(course_objects),
    semester=random.choice(['Fall', 'Spring', 'Summer']),
    year=random.randint(2021, 2024),
    days_of_week=random.choice(['MWF', 'TTh', 'MW', 'TThF']),
    start_time=fake.time(),
    end_time=fake.time()
) for student_obj in students for _ in range(3)]

# Create and save assignments
for student_obj in students:
    for course in course_objects:
        Assignment.objects.create(
            user=student_obj.account,
            course=course,
            title=fake.sentence(),
            description=fake.text(),
            due_date=fake.date(),
            priority=random.randint(1, 5),
            estimated_completion_time=timedelta(hours=random.randint(1, 5))
        )

# Create and save additional activities


# Create and save academic records
for schedule in schedules:
    AcademicRecord.objects.create(
        class_schedule=schedule,
        grade=random.choice(['A', 'B', 'C', 'D', 'F'])
    )
# Example queries
print("Example Queries:")

# Students majoring in Electrical Engineering
ee_students = Student.objects.filter(major="Electrical Engineering")
print(f"\nStudents majoring in Electrical Engineering: {[student_obj.full_name for student_obj in ee_students]}")

# Friends of a specific student
student = students[0]
friends = Friend.objects.filter(user1=student.account, status='accepted')
print(f"\nFriends of {student.full_name}: {[User.objects.get(id=friend.user2_id).username for friend in friends]}")

# Class schedules for Spring semester
spring_schedules = ClassSchedule.objects.filter(semester="Spring")
print(f"\nClass schedules for Spring semester: {[schedule.course.course_name for schedule in spring_schedules]}")

# Assignments with high priority (4 or 5)
high_priority_assignments = Assignment.objects.filter(priority__gte=4)
print(f"\nHigh priority assignments: {[assignment.title for assignment in high_priority_assignments]}")

# Academic records with grade 'A'
a_records = AcademicRecord.objects.filter(grade='A')
print(f"\nAcademic records with grade 'A': {[record.class_schedule.course.course_name for record in a_records]}")
