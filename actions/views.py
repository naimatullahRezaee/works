from django.shortcuts import render
from accounts.decorators import allowed_groups
from django.contrib.auth.decorators import login_required
from .models import Action
from django.contrib.contenttypes.models import ContentType


@login_required(login_url="login")
def all_actions(request):
    actions = Action.objects.all()
    
@login_required(login_url="login")
@allowed_groups(groups=["managers", "instructors", "admins"])
def action_detail(request, pk):
    action  = Action.objects.get(id=pk)
    context = {
        "action" : action, 
    }
    return render(request, "actions/detail.html", context)