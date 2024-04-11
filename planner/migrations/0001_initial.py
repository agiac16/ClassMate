# Generated by Django 4.2.6 on 2024-04-04 18:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("courses", "0002_remove_course_description_course_end_time_and_more"),
        ("users", "0002_alter_student_enrollment_year_and_more"),
        ("assignments", "0002_assignment_owner"),
    ]

    operations = [
        migrations.CreateModel(
            name="DailyPlanner",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("date", models.DateField()),
                (
                    "student",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="users.student"
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="TimeSlot",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("start_time", models.TimeField()),
                ("end_time", models.TimeField()),
                (
                    "activity",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="courses.additionalactivity",
                    ),
                ),
                (
                    "assignment",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="assignments.assignment",
                    ),
                ),
                (
                    "planner",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="planner.dailyplanner",
                    ),
                ),
            ],
        ),
    ]