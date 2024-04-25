from django.shortcuts import render, get_object_or_404
from .models import Planner, TimeSlot
from assignments.models import Assignment
from courses.models import Course, AdditionalActivity
from users.models import Student
from django.utils import timezone
from datetime import datetime, time, timedelta
from django.db.models import Sum
from datetime import date
from django.http import JsonResponse

class PlannerAlgorithm:
    def __init__(self, student, start_date, end_date, planner=None):
        self.student = student
        self.start_date = start_date
        self.end_date = end_date
        self.planner = planner or Planner.objects.get_or_create(student=student, start_date=start_date, end_date=end_date)[0]
        self.courses = Course.objects.filter(enrolled_students=student)
        self.activities = AdditionalActivity.objects.filter(student=student, start_time__date__gte=start_date.date(), start_time__date__lte=end_date.date())
        self.assignments = Assignment.objects.filter(student=student, due_date__gte=start_date.date(), due_date__lte=end_date.date())
        self.dates_with_slots = {}

    def generate_planner(self, planner):
        self.planner = planner

        # Update assignment completion times based on completed time slots
        self.update_assignment_completion_times()

        # Get canceled time slots before clearing the planner
        canceled_slots = TimeSlot.objects.filter(planner=self.planner, canceled=True)

        # Clear existing time slots associated with the planner
        TimeSlot.objects.filter(planner=self.planner).delete()

        self.populate_course_and_activity_slots()
        self.allocate_assignment_slots(canceled_slots)
        return self.planner

    def update_assignment_completion_times(self):
        for assignment in self.assignments:
            completed_slots = TimeSlot.objects.filter(planner=self.planner, assignment=assignment, completed=True)
            completed_duration = sum((slot.end_time - slot.start_time for slot in completed_slots), timedelta())
            assignment.estimated_completion_time -= completed_duration
            assignment.save()

    def populate_course_and_activity_slots(self):
        for date in (self.start_date + timedelta(days=n) for n in range((self.end_date - self.start_date).days + 1)):
            for course in self.courses:
                if self.should_occur_on_day(course, date):
                    self.create_timeslot(date, course.start_time, course.end_time, course=course)
                    if course.start_time_2 and course.end_time_2:
                        self.create_timeslot(date, course.start_time_2, course.end_time_2, course=course)

            for activity in self.activities.filter(start_time__date=date):
                self.create_timeslot(date, activity.start_time, activity.end_time, activity=activity)

            self.dates_with_slots[date] = TimeSlot.objects.filter(planner=self.planner, date=date)

    def allocate_assignment_slots(self, canceled_slots):
        min_gap_duration = timedelta(hours=1)  # Minimum gap duration for free time
        max_consecutive_slots = 2  # Maximum number of consecutive slots for the same assignment

        for assignment in sorted(self.assignments, key=lambda x: (x.due_date, -x.priority)):
            remaining_time = assignment.estimated_completion_time
            consecutive_slots = 0
            prev_assignment = None

            for date, timeslots in sorted(self.dates_with_slots.items(), key=lambda x: x[0]):
                if date.date() > assignment.due_date or remaining_time <= timedelta():                    break

                free_slots = self.calculate_free_time_slots(date, timeslots, canceled_slots)
                for start_time, end_time in free_slots:
                    slot_duration = min(
                        end_time - start_time,
                        assignment.max_slot_duration,
                        remaining_time
                    )
                    if slot_duration <= timedelta():
                        continue

                    if prev_assignment == assignment:
                        consecutive_slots += 1
                    else:
                        consecutive_slots = 1
                        prev_assignment = assignment

                    if consecutive_slots > max_consecutive_slots:
                        # Allocate free time slot
                        self.create_timeslot(date, start_time, end_time)
                        consecutive_slots = 0
                        prev_assignment = None
                    else:
                        end_time = start_time + slot_duration
                        remaining_time -= slot_duration

                        self.create_timeslot(date, start_time, end_time, assignment=assignment)

                        if remaining_time <= timedelta():
                            break

                # Check for large gaps of unused space
                if free_slots:
                    start_time, end_time = free_slots[-1]
                    gap_duration = end_time - start_time
                    if gap_duration >= min_gap_duration:
                        # Allocate free time slot
                        self.create_timeslot(date, start_time, end_time)

            if remaining_time > timedelta():
                print(f"Could not fully allocate time for {assignment.title}. Remaining time: {remaining_time}")

    def calculate_free_time_slots(self, date, timeslots, canceled_slots):
        work_start = datetime.combine(date, time(8, 0))
        work_end = datetime.combine(date, time(20, 0))
        free_slots = []
        previous_end = work_start

        # Add canceled time slots to the list of slots
        canceled_slots_on_date = canceled_slots.filter(date=date)
        timeslots = list(timeslots) + list(canceled_slots_on_date)

        for slot in sorted(timeslots, key=lambda x: x.start_time):
            if datetime.combine(date, slot.start_time) > previous_end:
                free_slots.append((previous_end.time(), slot.start_time))
            previous_end = max(previous_end, datetime.combine(date, slot.end_time))

        if previous_end < work_end:
            free_slots.append((previous_end.time(), work_end.time()))

        return free_slots

    def should_occur_on_day(self, course, date):
        day_code = date.strftime('%a')[0].upper()
        return day_code in (course.days or '') or day_code in (course.days_2 or '')

    def create_timeslot(self, date, start_time, end_time, course=None, activity=None, assignment=None):
        TimeSlot.objects.create(
            planner=self.planner,
            date=date,
            start_time=start_time,
            end_time=end_time,
            course=course,
            activity=activity,
            assignment=assignment
        )

def generate_monthly_planner(request, year, month):
    student = get_object_or_404(Student, account=request.user)
    planner = Planner.objects.filter(student=student).first()

    if planner:
        start_date = planner.start_date
        end_date = planner.end_date
    else:
        current_datetime = timezone.now()
        start_date = current_datetime.replace(minute=current_datetime.minute // 15 * 15, second=0, microsecond=0)
        end_date = (start_date + timedelta(days=30)).replace(hour=23, minute=59, second=59, microsecond=999999)
        planner = Planner.objects.create(student=student, start_date=start_date, end_date=end_date)

    dates_with_slots = {}
    for date in (start_date + timedelta(days=n) for n in range((end_date - start_date).days + 1)):
        dates_with_slots[date] = TimeSlot.objects.filter(planner=planner, date=date)

    return render(request, 'planner/monthly_planner.html', {'planner': planner, 'dates_with_slots': dates_with_slots})

def generate_planner(request):
    student = get_object_or_404(Student, account=request.user)
    planner = get_object_or_404(Planner, student=student)

    current_datetime = timezone.now()
    start_date = current_datetime.replace(minute=current_datetime.minute // 15 * 15, second=0, microsecond=0)
    end_date = (start_date + timedelta(days=30)).replace(hour=23, minute=59, second=59, microsecond=999999)

    planner.start_date = start_date
    planner.end_date = end_date
    planner.save()

    planner_algorithm = PlannerAlgorithm(student, start_date, end_date, planner=planner)
    planner = planner_algorithm.generate_planner(planner)

    return JsonResponse({'success': True})

def complete_assignment(request, assignment_id, timeslot_id):
    assignment = get_object_or_404(Assignment, id=assignment_id)
    timeslot = get_object_or_404(TimeSlot, id=timeslot_id)

    # Mark the time slot as completed
    timeslot.completed = True
    timeslot.save()

    return JsonResponse({'success': True})

def cancel_timeslot(request, timeslot_id):
    timeslot = get_object_or_404(TimeSlot, id=timeslot_id)

    # Mark the time slot as canceled
    timeslot.canceled = True
    timeslot.save()

    return JsonResponse({'success': True})