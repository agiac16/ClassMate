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
    start_date = timezone.datetime(year, month, 1).date()
    end_date = (start_date + timedelta(days=31)).replace(day=1) - timedelta(days=1)

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
            if course.days and date.strftime('%a') in course.days:
                TimeSlot.objects.create(
                    planner=planner,
                    start_time=course.start_time,
                    end_time=course.end_time,
                    course=course
                )
            if course.days_2 and date.strftime('%a') in course.days_2:
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

        # Calculate the total estimated completion time for all assignments due on the same day
        total_estimated_time = assignments.filter(due_date=date).aggregate(total_time=Sum('estimated_completion_time'))['total_time']

        # Calculate the available time slots for the day
        available_slots = []
        current_time = timezone.datetime.combine(date, timezone.datetime.min.time())
        end_of_day = timezone.datetime.combine(date, timezone.datetime.max.time())

        max_slot_length = timedelta(hours=1)  # Define the maximum slot length
        max_timeslots = 3  # Define the maximum number of time slots per assignment

        while current_time < end_of_day:
            # Check if the current time slot overlaps with any existing time slots
            overlapping_slots = TimeSlot.objects.filter(
                planner=planner,
                start_time__lte=current_time + max_slot_length,
                end_time__gt=current_time
            )

            if not overlapping_slots.exists():
                available_slots.append(current_time)

            current_time += max_slot_length

        # Sort assignments by priority and due date
        assignments = assignments.filter(due_date=date).order_by('-priority', 'due_date')

        for assignment in assignments:
            remaining_time = assignment.estimated_completion_time
            timeslots_used = 0

            while remaining_time > timedelta() and (max_timeslots == 0 or timeslots_used < max_timeslots):
                if not available_slots:
                    break

                slot_length = min(remaining_time, max_slot_length)
                start_time = available_slots.pop()
                end_time = start_time + slot_length

                TimeSlot.objects.create(
                    planner=planner,
                    start_time=start_time,
                    end_time=end_time,
                    assignment=assignment
                )

                remaining_time -= slot_length
                timeslots_used += 1

            # Update the assignment's estimated completion time
            assignment.estimated_completion_time = remaining_time
            assignment.save()

        # Distribute the remaining available slots evenly for flexible time
        if available_slots:
            flexible_slot_duration = (end_of_day - current_time) / len(available_slots)

            for slot_start in available_slots:
                TimeSlot.objects.create(
                    planner=planner,
                    start_time=slot_start,
                    end_time=slot_start + flexible_slot_duration
                )

    # Render the monthly planner template with the generated daily planners
    daily_planners = DailyPlanner.objects.filter(student=student, date__gte=start_date, date__lte=end_date).order_by('date')
    return render(request, 'planner/monthly_planner.html', {'daily_planners': daily_planners, 'year': year, 'month': month})
