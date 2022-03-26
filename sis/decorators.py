
from django.http import HttpResponse
from django.shortcuts import redirect
from users.models import CustomUser

def is_admin(function):
    def new_function(request, *args, **kwargs):
        user = CustomUser.objects.get(id=request.user.id)
        if user.user_type != "ADM":
            return HttpResponse("Access Denied")
        else:
            return function(request, *args, **kwargs)
    return new_function
def is_staff(function):
    def new_function(request, *args, **kwargs):
        user = CustomUser.objects.get(id=request.user.id)
        if user.user_type != "STA" and user.user_type != "ADM":
            return HttpResponse("Access Denied")
        else:
            return function(request, *args, **kwargs)
    return new_function
