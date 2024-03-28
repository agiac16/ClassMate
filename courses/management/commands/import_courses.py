import logging
from django.core.management.base import BaseCommand
from courses.models import Course
from schedule.models import Rule
import pandas as pd
import os
from django.conf import settings
from datetime import datetime
import re
from itertools import groupby

# Configure logger
logger = logging.getLogger(__name__)


def get_or_create_rule(day_chars):
    day_map = {'M': 'MO', 'T': 'TU', 'W': 'WE', 'R': 'TH', 'F': 'FR'}
    rule_strings = [day_map.get(day_char, '') for day_char in day_chars]
    rule_strings = [r for r in rule_strings if r]

    if rule_strings:
        rule_name = f"Every {', '.join(rule_strings)}"
        rule, created = Rule.objects.get_or_create(
            name=rule_name,
            defaults={'description': f"Occurs every {', '.join(rule_strings)}",
                      'frequency': 'WEEKLY',
                      'params': f"byweekday={','.join(rule_strings)}"}
        )
        return rule
    return None

class Command(BaseCommand):
    help = 'Import courses from a CSV file within the project.'

    def handle(self, *args, **kwargs):
        file_name = 'Section_Tally.csv'
        file_path = os.path.join(settings.BASE_DIR, 'data', file_name)

        if not os.path.exists(file_path):
            logger.error(f'File {file_path} does not exist')
            return

        df = pd.read_csv(file_path)

        for index, row in df.iterrows():
            logger.info(f"Processing row {index + 1}: {row['Title']}")

            if 'Online' in row['Session']:
                logger.info(" - Online course, skipping detailed scheduling.")
                continue

            class_details = str(row.get('Day  Beg   End   Bldg Room  (Type)', ''))
            pattern = r'(\w+)\s+(\d+)\s+(\d+)\s+(\w+)\s+(\w+)\s*\((\w+)\)'
            matches = re.findall(pattern, class_details)

            print(f"Class Details: {class_details}")
            print(f"Matches: {matches}")

            course, _ = Course.objects.update_or_create(
                crn=row['CRN'],
                defaults={
                    'course_name': row['Title'],
                    'course_code': row['Crse'],
                    'department': row['Subj'],
                    'credit_hours': int(row['Hrs']),
                    'professor': row['Prof'],
                }
            )

            # Clear existing rules for the course
            course.rule = None
            course.rule_2 = None
            course.start_time = None
            course.end_time = None
            course.start_time_2 = None
            course.end_time_2 = None

            class_matches = [match for match in matches if match[-1].lower() == 'class']

            if len(class_matches) > 0:
                day_chars, start_str, end_str, building, room, class_type = class_matches[0]
                print(f"Day: {day_chars}, Start: {start_str}, End: {end_str}, Type: {class_type}")
                course.start_time = datetime.strptime(start_str, '%H%M').time()
                course.end_time = datetime.strptime(end_str, '%H%M').time()
                course.rule = get_or_create_rule(day_chars)

                if len(class_matches) > 1:
                    day_chars_2, start_str_2, end_str_2, building_2, room_2, class_type_2 = class_matches[1]
                    print(f"Day 2: {day_chars_2}, Start 2: {start_str_2}, End 2: {end_str_2}, Type 2: {class_type_2}")
                    course.start_time_2 = datetime.strptime(start_str_2, '%H%M').time()
                    course.end_time_2 = datetime.strptime(end_str_2, '%H%M').time()
                    course.rule_2 = get_or_create_rule(day_chars_2)

            course.save()
            print(" - Course '%s' updated with rules and times." % row['Title'])

        print('Successfully imported courses with rules and times.')
