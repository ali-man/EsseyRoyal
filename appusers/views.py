from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import Group
from django.shortcuts import redirect

from appusers.models import User


def register(request):
    if request.method == 'POST':
        r = request.POST
        email = r.get('email', None)
        password1 = r.get('password1', None)
        password2 = r.get('password2', None)

        if (password1 == password2 is not None) and email is not None:
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                create_user = User.objects.create_user(email=email, password=password2)
                create_user.save()
                group = Group.objects.get(name='Customer')
                create_user.groups.add(group)
                create_user.save()
                user = authenticate(email=email, password=password2)
            login(request, user)
            messages.success(request, 'You have successfully registered')
        else:
            messages.error(request, 'Not all fields are filled.')

        return redirect('/')


def logout_user(request):
    logout(request)
    messages.success(request, 'You successfully logged out')
    return redirect('/')


def change_profile(request):
    if request.method == 'POST':
        r = request.POST
        user = User.objects.get(email=request.user)
        user.first_name = r['first_name']
        user.last_name = r['last_name']
        user.academic_institution = r['academic_institution']
        user.degree = r['degree']
        user.phone = r['phone']
        user.corporate_email = r['corporate_email']
        if 'avatar' in request.FILES:
            user.avatar = request.FILES['avatar']
        user.save()
        messages.success(request, 'Profile successfully changed')
        return redirect('/dashboard/')
    else:
        messages.error(request, 'Invalid request method')
        return redirect('/dashboard/')


def login_user(request):
    email = request.POST['username']
    password = request.POST['password']
    user = authenticate(email=email, password=password)
    if user is not None:
        login(request, user)
        messages.success(request, 'You are successfully logged in.')
        return redirect('/dashboard/')
    else:
        messages.error(request, 'wrong login or password')
        return redirect('/')