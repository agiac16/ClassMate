# Generated by Django 5.0.1 on 2024-04-05 15:58

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('assignments', '0005_alter_assignment_additional_username'),
        ('users', '0002_alter_student_enrollment_year_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='AssignmentRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('P', 'Pending'), ('A', 'Accepted'), ('D', 'Declined')], default='P', max_length=1)),
                ('assignment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='assignments.assignment')),
                ('requestee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='received_requests', to='users.student')),
                ('requester', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sent_requests', to='users.student')),
            ],
        ),
    ]
