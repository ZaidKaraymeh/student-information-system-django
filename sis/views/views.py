from audioop import reverse
from email import message
import json
from django.contrib.auth.decorators import login_required
from django.dispatch import receiver
from django.http.response import HttpResponseForbidden
from django.shortcuts import redirect, render
from users.models import CustomUser, Assignment, Post, Message
from ..forms import MessageForm, MessageRecieversForm
from itertools import chain
from operator import attrgetter
from django.forms import modelformset_factory
from django.contrib import messages
import json 
from django.core import serializers

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
    context ={"user":user}
    if (user.user_type == "STA"):
        template = "sis/staff_templates/staff_home.html"
    elif user.user_type == "ADM":
        template = "sis/admin_templates/admin_home_new.html"
    elif user.user_type == "STU":
        template = "sis/student_templates/student_home.html"

        courses = user.course_set.all()
        posts = []
        for course in courses:
            assignment_temp = Assignment.objects.filter(course__id = course.id)
            post_temp = Post.objects.filter(course__id = course.id)
            posts = [*posts, *assignment_temp, *post_temp]
        posts_sorted = sorted(
            posts,
            key=attrgetter('date_posted'),
            reverse=True
            )
        # print(courses, user.username)
        context = {
            "user": user,
            "courses": courses,
            "posts": posts_sorted,
        }

    else:
        return HttpResponseForbidden("Only School Members Allowed")
    return render(request, template, context)
    
def inbox(request):
    user = CustomUser.objects.get(id=request.user.id)

    
    if request.method == "POST":
        
        message_form = MessageForm(request.POST or None)
        print("POST")
        if message_form.is_valid():
            print("is valid")
            message = message_form.save(commit=False)
            message.sender = user
            message.reciever = CustomUser.objects.get(
                id=message_form.cleaned_data["users"]
            )
            message.save()
            messages.success(request, "Message Sent Successfully!")
            return redirect("inbox")


    else:
        message_form = MessageForm()

    sent_messages = Message.objects.filter(sender_id=user.id).order_by("-date_sent")
    recieved_messages = Message.objects.filter(reciever_id=user.id).order_by("-date_sent")

    context = {
            "user": user,
            "message_form":message_form,
            "sent_msgs": sent_messages,
            "recieved_msgs": recieved_messages,
        }
    return render(request, "sis/admin_templates/inbox.html", context)


def account(request):
    user = CustomUser.objects.get(id=request.user.id)


    context = {
        "user": user,
    }

    return render(request, "sis/admin_templates/account.html", context)

