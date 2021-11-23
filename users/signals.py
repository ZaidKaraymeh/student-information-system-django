from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Profile, CustomUser

# When a user is saved do the function
# revierver is create profile
# if a user is created make a profile object to the user
@receiver(post_save, sender=CustomUser)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

# instance is the user
@receiver(post_save, sender=CustomUser)
def save_profile(sender, instance, **kwargs):
    instance.profile.save() 



            


# @receiver(post_save,sender=CustomUser)
# def save_user(sender,instance,**kwargs):
#     if instance.user_type=="ADM":
#         instance.admin.save()
#     if instance.user_type=="STA":
#         instance.staff.save()
#     if instance.user_type=="STU":
#         instance.student.save()



# @receiver(post_save,sender=Staff)
# def save_user_saff(sender,instance,**kwargs):
#     instance.user.is_staff = True
#     instance.save()

# @receiver(post_save,sender=Admin)
# def save_user_admin(sender,instance,**kwargs):
#     instance.user.is_superuser = True
#     instance.save()



