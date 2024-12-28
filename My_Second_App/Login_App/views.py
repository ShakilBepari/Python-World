from django.shortcuts import render
from .forms import UserForm, UserInfoForm
from django.contrib.auth import login, logout, authenticate
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import UserInfo


# Create your views here.

def index(req):
    diction = {'title': 'Home Page'}
    if req.user.is_authenticated:
        current_user = req.user
        user_id = current_user.id
        user_basic_info = User.objects.get(pk=user_id)
        user_more_info = UserInfo.objects.get(user_id = user_id)
        diction = {'title': 'Home Page', 'user_basic_info': user_basic_info, 'user_more_info': user_more_info}

    return render(req, 'Login_App/index.html', context=diction)


@login_required
def user_logout(req):
    logout(req)
    return HttpResponseRedirect(reverse('Login_App:login'))


def login_page(req):
    return render(req, 'Login_App/login.html', context={'title': 'Login Page'})


def user_login(req):
    if req.method == 'POST':
        username = req.POST.get('username')
        password = req.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(req, user)
                return HttpResponseRedirect(reverse('Login_App:index'))
            else:
                return HttpResponse('Sorry user is not active?')
        else:
            return HttpResponse('Sorry Username or Password incorrect?')
    else:
        return HttpResponseRedirect(reverse('Login_App:login'))


def register(req):
    registered = False

    if req.method == 'POST':
        user_form = UserForm(data=req.POST)
        user_info_form = UserInfoForm(data=req.POST)
        if user_form.is_valid() and user_info_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()

            user_info = user_info_form.save(commit=False)
            user_info.user = user

            print(req.FILES)

            if 'profile_pic' in req.FILES:
                user_info.profile_pic = req.FILES['profile_pic']

            user_info.save()
            registered = True

    else:
        user_form = UserForm
        user_info_form = UserInfoForm

    diction = {'title': 'User Form', 'user_form': user_form, 'user_info_form': user_info_form, 'registered': registered}
    return render(req, 'Login_App/register.html', context=diction)
