from django.shortcuts import render

from users.models import CustomUser
# Create your views here.

def home(request):
    if not request.user.is_authenticated:
        return render(request, "sis/home.html")
    user = CustomUser.objects.get(id=request.user.id)
    context = {"user":user}
    if (user.user_type == "STA"):
        x = "sis/staff_templates/staff_home.html"
    elif user.user_type == "ADM":
        x = "sis/admin_templates/admin_home.html"
    else:
        x = "sis/home.html"


    return render(request, x, context)