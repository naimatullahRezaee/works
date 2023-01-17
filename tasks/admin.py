from django.contrib import admin
from .models import Assignment, Respond, AssignmentScore, Event


admin.site.register(Assignment)
admin.site.register(Respond)
admin.site.register(AssignmentScore)
admin.site.register(Event)
