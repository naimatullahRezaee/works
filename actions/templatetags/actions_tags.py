from django import template
from ..models import Action

register = template.Library()

@register.simple_tag
def limited_notifications():
    actions_count =  Action.objects.filter().count()
    if actions_count > 10:
        return "9+"
    else:
        return actions_count

@register.inclusion_tag("actions/navbar_display_actions.html")
def latest_actions(count=10):
    actions = Action.objects.all()[:count]
    return {"actions" : actions}
