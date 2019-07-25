from django import template


register = template.Library()


@register.filter(name='completed_tasks_count')
def completed_tasks_count(course):
    tasks_completed = len([t for t in course.task_set.filter(status=2)])
    return tasks_completed


@register.filter(name='completed_tasks_percent')
def completed_tasks_percent(course):
    completed_count = len([t for t in course.task_set.filter(status=2)])
    tasks_from_course = course.task_set.count()
    percent = 100 // (tasks_from_course / completed_count) if completed_count != 0 else 0
    return int(percent)


@register.filter(name='tasks_pending')
def tasks_pending(course):
    tasks = course.task_set.filter(price_status=1)
    return tasks.count()


@register.filter(name='task_status')
def task_status(num):
    result = {
        0: 'In search',
        1: 'In progress',
        2: 'Completed'
    }
    return result[num]