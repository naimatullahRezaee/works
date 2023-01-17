from django.http import HttpResponse
from django.shortcuts import redirect


from courses.models import Course

def allowed_groups(groups = []):
    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs):
            group = None

            if request.user.groups.exists():
                group = request.user.groups.all()[0].name
            if group in groups or request.user.is_staff:
                return view_func(request, *args, **kwargs)
            else:
                return HttpResponse("You are not authorize to view this page ")
        
        return wrapper_func
    return decorator

def is_admin(groups=[]):
    for group in groups:
        for per in group.permissions.all():
            pass


# def owner_mixin(func):
#     def check_and_call(request, *args, **kwargs):
#         pk = kwargs["pk"]
#         course = Course.objects.get(pk=pk)
#         if not (course.owner.id == request.user.id):
#             return HttpResponse("You are not the owner of this course ")
#         return func(request, *args, **kwargs)
#     return check_and_call