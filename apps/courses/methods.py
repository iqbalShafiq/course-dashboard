import random
import time as t
from datetime import datetime, time, timedelta
from apps.schedules.models import Schedule, DayOfWeek
from apps.courses.models import Course
from django.db.models import Q
from apps.teachers.models import Teacher

def map_schedules(course_id):
    print("Mapping schedules...")
    """
    Randomly assigns a single schedule to a random teacher.
    Ensures no time or room conflicts.
    """
    teacher = random.choice(Teacher.objects.filter(is_active=True))
    courses = Course.objects.filter(is_active=True)
    rooms = ["Room A", "Room B", "Room C", "Room D"]
    days = list(DayOfWeek.values)

    course = courses.get(id=course_id)
    day_of_week = random.choice(days)
    start_hour = random.randint(8, 16)  # Random start time between 8 AM and 4 PM
    start_time = time(hour=start_hour, minute=0)
    end_time = (datetime.combine(datetime.today(), start_time) + timedelta(hours=1)).time()
    room = random.choice(rooms)

    t.sleep(2)

    # Check for conflicts
    conflict_exists = Schedule.objects.filter(
        Q(teacher=teacher) | Q(room=room),
        day_of_week=day_of_week,
        start_time__lt=end_time,
        end_time__gt=start_time,
    ).exists()

    t.sleep(2)

    if not conflict_exists:
        Schedule.objects.create(
            teacher=teacher,
            course=course,
            day_of_week=day_of_week,
            start_time=start_time,
            end_time=end_time,
            room=room,
            is_active=True,
        )