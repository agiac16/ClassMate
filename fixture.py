import os
import django
import random
from faker import Faker
from datetime import date, timedelta

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ClassMate.settings')
django.setup()

from django.contrib.auth.models import User
from users.models import Student
from friends.models import Friend
from courses.models import Course
from forum.models import ForumThread
from forum.models import ForumPost
from courses.models import ClassSchedule
from assignments.models import Assignment
from courses.models import AdditionalActivity
from courses.models import AcademicRecord

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

# Assign each course to a random student
for course in course_objects:
    student = random.choice(students)
    course.enrolled_students.add(student)

    
# # Create and save friends
# for student_obj in students:
#     friend_student = random.choice(students)
#     if student_obj != friend_student:
#         Friend.objects.create(
#             user1=student_obj.account,
#             user2=friend_student.account,
#             status=random.choice(['requested', 'accepted', 'declined'])
#         )


from django.utils import timezone

# Create and save forum posts and threads with timezone-aware datetime objects
for student in students:
    for course in course_objects:
        post = ForumPost.objects.create(
            title=fake.sentence(),
            content=fake.text(),
            posted_by=student,
            course=course
        )

        for _ in range(random.randint(1, 5)):
            ForumThread.objects.create(
                parent_post=post,
                content=fake.text(),
                posted_by=random.choice(students),
                timestamp=timezone.make_aware(fake.date_time())
            )



# Create and save class schedules
schedules = [ClassSchedule.objects.create(
    student=student_obj,
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
            student=student_obj,
            course=course,
            title=fake.sentence(),
            description=fake.text(),
            due_date=date.today() + timedelta(days=random.randint(1,7)),
            priority=random.randint(1, 5),
            estimated_completion_time=timedelta(hours=random.randint(1, 5))
        )

# Create and save additional activities
from django.utils import timezone

# Create and save additional activities with timezone-aware datetime objects
for student in students:
    for _ in range(random.randint(1, 3)):
        AdditionalActivity.objects.create(
            student=student,
            title=fake.sentence(),
            description=fake.text(),
            start_time=timezone.make_aware(fake.date_time()),
            end_time=timezone.make_aware(fake.date_time()),
            location=fake.address()
        )



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

# # Friends of a specific student
# student = students[0]
# friends = Friend.objects.filter(user1=student.account, status='accepted')
# print(f"\nFriends of {student.full_name}: {[User.objects.get(id=friend.user2_id).username for friend in friends]}")

# Class schedules for Spring semester
spring_schedules = ClassSchedule.objects.filter(semester="Spring")
print(f"\nClass schedules for Spring semester: {[schedule.course.course_name for schedule in spring_schedules]}")

# Assignments with high priority (4 or 5)
high_priority_assignments = Assignment.objects.filter(priority__gte=4)
print(f"\nHigh priority assignments: {[assignment.title for assignment in high_priority_assignments]}")

# Academic records with grade 'A'
a_records = AcademicRecord.objects.filter(grade='A')
print(f"\nAcademic records with grade 'A': {[record.class_schedule.course.course_name for record in a_records]}")


# Forum posts for a specific course
course_name = "Introduction to Computer Science"
course_posts = ForumPost.objects.filter(course__course_name=course_name)
print(f"\nForum posts for {course_name}: {[post.title for post in course_posts]}")

# Replies (threads) for a specific forum post
post_title = course_posts.first().title if course_posts.exists() else "No posts available"
post_threads = ForumThread.objects.filter(parent_post__title=post_title)
print(f"\nReplies for forum post '{post_title}': {[thread.content for thread in post_threads]}")

# Additional activities for a specific student
student_name = students[0].full_name
student_activities = AdditionalActivity.objects.filter(student__full_name=student_name)
print(f"\nAdditional activities for {student_name}: {[activity.title for activity in student_activities]}")


# Forum posts posted by students in a specific major
major = "Computer Science"
posts_by_major = ForumPost.objects.filter(posted_by__major=major)
print(f"\nForum posts posted by students in {major}: {[post.title for post in posts_by_major]}")

