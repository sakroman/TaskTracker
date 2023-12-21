from django import template

register = template.Library()


@register.filter
def filter_due_date(tasks, due_date):
    return tasks.filter(due_date=due_date)
