from django.contrib.auth.decorators import login_required
from django.http.response import HttpResponseForbidden
from django.shortcuts import redirect, render

from users.models import CustomUser
# Create your views here.


"""
Schools home menu, for everyone to see
"""
def home(request):
    return render(request, 'sis/home.html')
"""
if not request.user.is_authenticated:
    return render(request, "sis/home.html")
user = CustomUser.objects.get(id=request.user.id)
context = {"user":user}
if (user.user_type == "STA"):
    template = "sis/staff_templates/staff_home.html"
elif user.user_type == "ADM":
    template = "sis/admin_templates/admin_home_new.html"
else:
    template = "sis/home.html"

return render(request, template, context)
"""


"""
School SIS view, for students, staff, and admin only
"""
@login_required
def home_sis(request):
    user = CustomUser.objects.get(id=request.user.id)
    if (user.user_type == "STA"):
        template = "sis/staff_templates/staff_home.html"
    elif user.user_type == "ADM":
        template = "sis/admin_templates/admin_home_new.html"
    elif user.user_type == "STU":
        template = "sis/student_templates/student_home.html"
    else:
        return HttpResponseForbidden("Only School Members Allowed")
    context ={"user":user}
    return render(request, template, context)
    
