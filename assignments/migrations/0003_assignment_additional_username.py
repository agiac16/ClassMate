# Generated by Django 5.0.1 on 2024-04-04 18:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('assignments', '0002_assignment_owner'),
    ]

    operations = [
        migrations.AddField(
            model_name='assignment',
            name='additional_username',
            field=models.CharField(max_length=255, null=True),
        ),
    ]