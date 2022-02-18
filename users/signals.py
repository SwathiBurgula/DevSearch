from django.db.models.signals import post_save,post_delete
from .models import Profile
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf import settings


# @receiver(post_save, sender=User)
def createProfile(sender,instance,created,**kwargs):
    if created:
        user = instance
        profile = Profile.objects.create(
            user = user,
            name = user.first_name,
            username = user.username,
            email = user.email,
            # profile_image = '/profiles/user-default.png'
        )
        print('Same Record created in Profile ')

        subject = "Welcome to Developer's web Application"
        message = "We glad you are here"

        send_mail(
            subject,
            message,
            settings.EMAIL_HOST_USER,
            [profile.email],
            fail_silently=False,
        )


def deleteUser(sender,instance,**kwargs):
    try:          
            user = instance.user
            user.delete()
            print('User also deleted')
    except:
        print('User already deleted')



def updateUser(sender,instance,created,**kwargs):
    if created == False:
        profile = instance
        user = profile.user
        user.first_name = profile.name
        user.username = profile.username
        user.email = profile.email
        user.save()
        print('User updated')



post_save.connect(createProfile,sender=User)
post_delete.connect(deleteUser,sender=Profile)
post_save.connect(updateUser,sender=Profile)