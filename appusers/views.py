from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.views.generic.base import View

from appprofile.models import Client
from appusers.models import User


class SignUpViews(View):
    @staticmethod
    def get(request):
        if request.user.is_authenticated:
            messages.info(request, 'Вы авторизованы (Перевести)')
            redirect('/')
        return render(request, 'appusers/sign-up.html', locals())

    @staticmethod
    def post(request):
        r = request.POST
        first_name = r.get('firstname', None)
        last_name = r.get('lastname', None)
        email = r.get('email', None)
        password1 = r.get('password1', None)
        password2 = r.get('password2', None)

        if (password1 == password2 is not None) and email is not None:
            create_user = User.objects.create_user(email=email, password=password2)
            create_user.first_name = first_name if first_name is not None else ''
            create_user.last_name = last_name if last_name is not None else ''
            create_user.is_client = True
            create_user.save()
            client = Client()
            client.user = create_user
            client.save()
            user = authenticate(email=email, password=password2)
            login(request, user)
            messages.success(request, 'Вы успешно зарегистрированы (перевести)')
        else:
            messages.error(request, 'Не все поля заполнены (перевести)')

        return redirect('/')


class SignInViews(View):
    @staticmethod
    def get(request):
        if request.user.is_authenticated:
            messages.info(request, 'Вы авторизованы (Перевести)')
            return redirect('/')
        return render(request, 'appusers/sign-in.html')

    @staticmethod
    def post(request):
        r = request.POST
        email = r.get('email', None)
        password = r.get('password', None)
        if email and password is not None:
            user = authenticate(email=email, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    messages.success(request, 'Вы успешно авторизовались (перевести)')
                else:
                    messages.error(request, 'Ваш аккаунт заблокирован (перевести)')
            else:
                messages.error(request, 'Неверный email или пароль (перевести)')
        else:
            messages.error(request, 'Заполните все формы (перевести)')

        return redirect('/')


def logout_user(request):
    logout(request)
    messages.success(request, 'Вы успешно разлогинились (перевести)')
    return redirect('/')