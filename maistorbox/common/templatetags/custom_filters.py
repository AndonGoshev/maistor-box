from django import template

register = template.Library()

@register.filter
def range_filter(value):
    return range(value)


@register.filter
def approved_feedback(feedbacks):
    return feedbacks.filter(approved=True)