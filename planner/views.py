from django.shortcuts import render, get_object_or_404
from .models import Planner, TimeSlot
from assignments.models import Assignment
from courses.models import Course, AdditionalActivity
from users.models import Student
from django.utils import timezone
from datetime import datetime, time, timedelta
from django.db.models import Sum
from datetime import date

class PlannerAlgorithm:
    def __init__(self, student, start_date, end_date):
        self.student = student
        self.start_date = start_date
        self.end_date = end_date
        self.planner = Planner.objects.create(student=student, start_date=start_date, end_date=end_date)
        self.courses = Course.objects.filter(enrolled_students=student)
        self.activities = AdditionalActivity.objects.filter(student=student, start_time__date__gte=start_date, start_time__date__lte=end_date)
        self.assignments = Assignment.objects.filter(student=student, due_date__gte=start_date, due_date__lte=end_date)
        self.dates_with_slots = {}

    def generate_planner(self):
        self.populate_course_and_activity_slots()
        self.allocate_assignment_slots()
        return self.planner

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

    def allocate_assignment_slots(self):
        min_gap_duration = timedelta(hours=1)  # Minimum gap duration for free time
        max_consecutive_slots = 2  # Maximum number of consecutive slots for the same assignment

        for assignment in sorted(self.assignments, key=lambda x: (x.due_date, -x.priority)):
            remaining_time = assignment.estimated_completion_time
            consecutive_slots = 0
            prev_assignment = None

            for date, timeslots in sorted(self.dates_with_slots.items(), key=lambda x: x[0]):
                if date > assignment.due_date or remaining_time <= timedelta():
                    break

                free_slots = self.calculate_free_time_slots(date, timeslots)
                for start_time, end_time in free_slots:
                    slot_duration = min(
                        datetime.combine(date, end_time) - datetime.combine(date, start_time),
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
                        end_time = (datetime.combine(date, start_time) + slot_duration).time()
                        remaining_time -= slot_duration

                        self.create_timeslot(date, start_time, end_time, assignment=assignment)

                        if remaining_time <= timedelta():
                            break

                # Check for large gaps of unused space
                if free_slots:
                    start_time, end_time = free_slots[-1]
                    gap_duration = datetime.combine(date, end_time) - datetime.combine(date, start_time)
                    if gap_duration >= min_gap_duration:
                        # Allocate free time slot
                        self.create_timeslot(date, start_time, end_time)

            if remaining_time > timedelta():
                print(f"Could not fully allocate time for {assignment.title}. Remaining time: {remaining_time}")

    def should_occur_on_day(self, course, date):
        day_code = date.strftime('%a')[0].upper()
        return day_code in (course.days or '') or day_code in (course.days_2 or '')

    def calculate_free_time_slots(self, date, timeslots):
        work_start = datetime.combine(date, time(8, 0))
        work_end = datetime.combine(date, time(20, 0))
        free_slots = []
        previous_end = work_start

        for slot in timeslots.order_by('start_time'):
            if datetime.combine(date, slot.start_time) > previous_end:
                free_slots.append((previous_end.time(), slot.start_time))
            previous_end = max(previous_end, datetime.combine(date, slot.end_time))

        if previous_end < work_end:
            free_slots.append((previous_end.time(), work_end.time()))

        return free_slots

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
    start_date = timezone.datetime(year, month, 1).date()
    end_date = (start_date + timedelta(days=44)).replace(day=1) - timedelta(days=1)

    planner_algorithm = PlannerAlgorithm(student, start_date, end_date)
    planner = planner_algorithm.generate_planner()

    return render(request, 'planner/monthly_planner.html', {'planner': planner, 'dates_with_slots': planner_algorithm.dates_with_slots})