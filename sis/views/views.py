from audioop import reverse
from email import message
import json
from django.contrib.auth.decorators import login_required
from django.dispatch import receiver
from django.http.response import HttpResponseForbidden
from django.shortcuts import redirect, render
from users.models import CustomUser, Assignment, Post, Message, Reply, MailFiles, Fee, FeeReport
from ..forms import MessageForm, MessageRecieversForm, MessageReplyForm
from itertools import chain
from operator import attrgetter
from django.forms import modelformset_factory
from django.contrib import messages
import json 
from django.core import serializers
from django.db.models import Q
from notifications.signals import notify

# Create your views here.


"""
Schools home menu, for everyone to see
"""
def home(request):
    try:
        user = CustomUser.objects.get(id=request.user.id)
    except:
        return redirect("login")
    context = {
        'user':user,
    }
    return render(request, 'sis/home.html', context)
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
        template = "sis/admin_templates/admin_home_new.html"
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
    user.notifications.mark_all_as_read()

    if request.method == "POST":
        message_form = MessageForm(request.POST or None, request.FILES)
        reply_form = MessageReplyForm(request.POST or None, request.FILES)
        if message_form.is_valid():
            message = message_form.save(commit=False)
            message.sender = user
            message.reciever = CustomUser.objects.get(
                id=message_form.cleaned_data["users"]
            )
            message.save()

            for file in request.FILES.getlist('file'):
                obj = MailFiles.objects.create(
                    file=file,
                )
                obj.save()
                message.files.add(obj)
                message.save()
            sender = message.sender
            receiver = message.reciever
            notify.send(sender, recipient=receiver, verb='Message')
            messages.success(request, "Message Sent Successfully!")
            return redirect("inbox")
        if reply_form.is_valid():
            reply = reply_form.save(commit=False)
            msg = Message.objects.get(id=request.POST.get('msg_id'))
            if msg.is_replied == True:
                prev_reply = Reply.objects.get(id=request.POST.get('reply_id'))
                if prev_reply.sender.id == user.id:
                    reply.sender = prev_reply.sender
                    reply.reciever = prev_reply.reciever
                    sender = prev_reply.sender
                    receiver = prev_reply.reciever
                    notify.send(sender, recipient=receiver, verb='Message')
                else:
                    reply.sender = prev_reply.reciever
                    reply.reciever = prev_reply.sender
                    sender = prev_reply.sender
                    receiver = prev_reply.reciever
                    notify.send(sender, recipient=receiver, verb='Message')
            else:
                if msg.sender.id == user.id:
                    reply.sender = msg.sender
                    reply.reciever = msg.reciever
                    sender = msg.sender
                    receiver = msg.reciever
                    notify.send(sender, recipient=receiver, verb='Message')
                else:
                    reply.sender = msg.reciever
                    reply.reciever = msg.sender
                    sender = msg.sender
                    receiver = msg.reciever
                    notify.send(sender, recipient=receiver, verb='Message')
            reply.save()

            for file in request.FILES.getlist('file'):
                obj = MailFiles.objects.create(
                    file=file,
                )
                obj.save()
                reply.files.add(obj)
                reply.save()
            msg.replies.add(reply)
            msg.save()
            
            messages.success(request, "Reply Sent Successfully!")
            return redirect("inbox")


    else:
        message_form = MessageForm()
        reply_form = MessageReplyForm()

    sent_messages = Message.objects.filter(sender_id=user.id).order_by("-date_sent")
    recieved_messages = Message.objects.filter(
        Q(reciever_id=user.id, is_replied=False) 
        | 
        Q(is_replied=True, reciever_id=user.id)
        |
        Q(is_replied=True, sender_id=user.id)
    ).order_by("-date_reply")
    # recieved_messages = Message.objects.filter(Q(reciever_id=user.id, is_replied=True) | Q(reciever_id=user.id)).order_by("-date_reply")

    context = {
            "user": user,
            "message_form":message_form,
            "reply_form": reply_form,
            "sent_msgs": sent_messages,
            "recieved_msgs": recieved_messages,
        }
    return render(request, "sis/admin_templates/inbox.html", context)


def account(request):
    user = CustomUser.objects.get(id=request.user.id)
    student = CustomUser.objects.get(id=request.user.id)
    fee = Fee.objects.last()
    report, created = FeeReport.objects.get_or_create(
    student = student,
    defaults={
        'note': "---",
        "amount_paid": 0,
        "paid_full":False,
        },
    )
    
    if created:
        fee.student_fees.add(report)

    context = {
        "user":user,
        "student":student,
        "report":report,
        "fee":fee,

    }

    return render(request, "sis/admin_templates/account.html", context)

