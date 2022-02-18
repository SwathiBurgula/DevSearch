from email import message
import re
from django.shortcuts import redirect, render
from .models import Message, Profile
from myproject.models import Project
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from .forms import CustomUserCreationForm
from .forms import ProfileForm, SkillForm, MessageForm
from .utils import searchProfiles, paginateProfiles
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.views import View

# Create your views here.


def profiles(request):
    profiles,search_query = searchProfiles(request)

    profiles,custom_range = paginateProfiles(request,profiles, 3)

#    profiles = Profile.objects.all()
    context = {'profiles': profiles,'search_query':search_query,
               'custom_range':custom_range,
    }

    return render(request, 'users/profiles-all.html', context)


def profile(request, pk):
    profile = Profile.objects.get(id=pk)
    top_skills = profile.skill_set.exclude(description__iexact="")
    other_skills = profile.skill_set.filter(description="")
    print(other_skills)

    projects = Project.objects.filter(owner_id=pk)
    print(projects)
    context = {'profile': profile,
               'topskills': top_skills,
               'otherskills': other_skills,
               'projects': projects,
               }
    return render(request, 'users/single-profile.html', context)


def loginUser(request):
    page = 'login'
    
    if request.method == 'POST':
        username = request.POST['username'].lower()
        password = request.POST['password']

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'User does not exist')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            

            return redirect(request.GET['next'] if 'next' in request.GET else 'users:account')
        else:
            messages.error(request, "Username or Password doesn't match")
           
    context = {'page': page}
    return render(request, 'users/login_register.html', context)


def logoutUser(request):
    logout(request)
    messages.info(request, 'User successfully logged out!')
    return redirect('users:login')


def registerUser(request):
    page = 'register'
    form = CustomUserCreationForm()
    context = {'page': page,
               'form': form
               }

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)

        if form.is_valid():
            user=form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            messages.success(request, 'User created successfully')
            login(request, user)
            return redirect('users:profiles-all')
        else:
            messages.error(
                request, 'Some error occurred during registration')
            print(form.errors)
    

    context={'page':page, 'form':form, }      
    return render(request, 'users/login_register.html', context)


def userAccount(request):
    profile = request.user.profile
    context={
        'profile':profile,
    }
    return render(request,'users/account.html',context)



def editAccount(request):
    profile = request.user.profile
    form = ProfileForm(instance=profile)

    if request.method == 'POST':
        form = ProfileForm(request.POST,request.FILES,instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request,'Profile updated Successfully')
            return redirect('users:account')
        else:
            messages.error(request,'Enter valid data in fields')   

    context={'form':form}
    return render(request,'users/profile-form.html',context)





def createSkill(request):
    profile = request.user.profile
    form = SkillForm()

    if request.method == 'POST':
        form = SkillForm(request.POST)
        if form.is_valid():
            skill = form.save(commit=False)
            skill.owner = profile
            skill.save()
            messages.success(request,'Skill created Successflly')
            return redirect('users:account')
        else:
            messages.error(request,'Some error occurred')


    context = {'form':form}
    return render(request,'users/skill-form.html',context)




def updateSkill(request,id):
    profile = request.user.profile
    skill = profile.skill_set.get(id=id)
    form = SkillForm(instance = skill)

    if request.method == 'POST':
        form = SkillForm(request.POST,instance=skill)
        if form.is_valid():
            form.save()
                       
            messages.success(request,'Skill updated Successflly')
            return redirect('users:account')
        else:
            messages.error(request,'Some error occurred')


    context = {'form':form}
    return render(request,'users/skill-form.html',context)





def deleteSkill(request,id):
    profile = request.user.profile
    skill = profile.skill_set.get(id=id)

    if request.method == 'POST':
        skill.delete()
        messages.success(request,'skill deleted successfully')
        return redirect('users:account')

    context = {'object':skill}
    return render(request,'projects/delete-form.html',context)


@login_required(login_url='users:login')
def inbox(request):
    recipient = request.user.profile
    recieved_msgs = recipient.messages.all()
    unreadCount = recieved_msgs.filter(is_read=False).count()

    context = {'recieved_msgs': recieved_msgs, 'unreadCount': unreadCount}
    return render(request, 'users/inbox.html', context)

@login_required(login_url='users:login')

def viewMessage(request,pk):
    recipient = Profile.objects.get(id=pk)
    if message.is_read == False:
        message.is_read == True
        message.save()

    context = {'message':message}
    return render(request, 'users/message.html', context)

def createMessage(request,pk):
    recipient = Profile.objects.get(id=pk)
    form = MessageForm()

    if request.method == 'POST':
        form = MessageForm(request.POST)
        try:
            sender = request.user.profile
        except:
            sender = None
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = sender
            message.recipient = recipient

            if sender:
                message.name = sender.name
                message.email = sender.email

            message.save()
            return redirect('users:profiles-all')

    context={'form':form,'recipient':recipient}
    return render(request,'users/message-form.html',context)