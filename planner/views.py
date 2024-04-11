from django.shortcuts import render, get_object_or_404
from .models import DailyPlanner, TimeSlot
from assignments.models import Assignment
from courses.models import Course, AdditionalActivity
from users.models import Student
from django.utils import timezone
from datetime import timedelta
from django.db.models import F, Sum

def generate_daily_planner(request, year, month):
    student = get_object_or_404(Student, account=request.user)
    today = timezone.now().date()
    start_date = timezone.datetime(year, month, today.day).date()
    end_date = start_date + timedelta(days=30)

    # Get the student's enrolled courses
    courses = Course.objects.filter(enrolled_students=student)

    # Get additional activities for the month
    activities = AdditionalActivity.objects.filter(student=student, start_time__date__gte=start_date, start_time__date__lte=end_date)

    # Get assignments due within the month
    assignments = Assignment.objects.filter(student=student, due_date__gte=start_date, due_date__lte=end_date)

    # Generate daily planners for each day of the month
    for date in (start_date + timedelta(days=n) for n in range((end_date - start_date).days + 1)):
        planner, created = DailyPlanner.objects.get_or_create(student=student, date=date)

        # Clear existing time slots for the day
        TimeSlot.objects.filter(planner=planner).delete()

        # Create time slots for courses
        for course in courses:
            if should_occur_on_day(course, date):
                TimeSlot.objects.create(
                    planner=planner,
                    start_time=course.start_time,
                    end_time=course.end_time,
                    course=course
                )
                if course.start_time_2 and course.end_time_2:
                    TimeSlot.objects.create(
                        planner=planner,
                        start_time=course.start_time_2,
                        end_time=course.end_time_2,
                        course=course
                    )

        # Create time slots for additional activities
        for activity in activities.filter(start_time__date=date):
            TimeSlot.objects.create(
                planner=planner,
                start_time=activity.start_time,
                end_time=activity.end_time,
                activity=activity
            )

        # Create time slots for assignments
        assignments_due = assignments.filter(due_date__gte=date).order_by('due_date', 'priority')
        available_slots = list(TimeSlot.objects.filter(planner=planner, assignment__isnull=True).order_by('start_time'))

        for assignment in assignments_due:
            remaining_time = assignment.estimated_completion_time
            allocated_slots = []

            while remaining_time > timedelta() and available_slots:
                slot = available_slots.pop(0)
                slot_duration = min(slot.end_time - slot.start_time, remaining_time)
                TimeSlot.objects.create(
                    planner=planner,
                    start_time=slot.start_time,
                    end_time=slot.start_time + slot_duration,
                    assignment=assignment
                )
                remaining_time -= slot_duration
                allocated_slots.append(slot)

            # Spread out the allocated slots evenly
            if len(allocated_slots) > 1:
                total_duration = sum((slot.end_time - slot.start_time) for slot in allocated_slots)
                avg_duration = total_duration / len(allocated_slots)
                start_time = allocated_slots[0].start_time
                for slot in allocated_slots:
                    slot.start_time = start_time
                    slot.end_time = start_time + avg_duration
                    slot.save()
                    start_time += avg_duration

    # Render the monthly planner template with the generated daily planners
    daily_planners = DailyPlanner.objects.filter(student=student, date__gte=start_date, date__lte=end_date).order_by('date')
    return render(request, 'planner/monthly_planner.html', {'daily_planners': daily_planners, 'year': year, 'month': month})

def should_occur_on_day(course, date):
    day_code = date.strftime('%a')[0].upper()
    if course.days and day_code in course.days:
        return True
    if course.days_2 and day_code in course.days_2:
        return True
    return False
