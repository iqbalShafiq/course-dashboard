from huey.contrib.djhuey import task
from apps.courses.methods import map_schedules
from apps.courses.models import Course

@task()
def assign_schedules(course_id):
    """
    Task to assign a single schedule to a random teacher.
    """
    course = Course.objects.get(id=course_id)
    course.task_running = True
    course.save()

    try:
        print("Assigning schedules...")
        map_schedules(course_id)
    finally:
        # Mark task as completed
        course.task_running = False
        course.save()
