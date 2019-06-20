import json

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import Group
from django.core import serializers
from django.http import JsonResponse, HttpResponse
from django.shortcuts import redirect, render
from django.views.generic.base import View

from appdashboard.views import access_to_manager_and_admin
from appusers.models import User, MessageChatUser, ChatUser, FileChatUser


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


class ChatViews(View):

    @staticmethod
    def get(request, pk):

        if request.user.is_anonymous:
            print('ASD')
            messages.error(request, 'Access is limited')
            return redirect('/')

        chat = ChatUser.objects.get(id=pk)
        messages_from_chat = MessageChatUser.objects.filter(chat=chat).order_by('-id')
        files_from_chat = FileChatUser.objects.filter(chat=chat).order_by('-id')

        if request.is_ajax():
            print(request.GET)
            r_mfc = request.GET.get('messagesFromChat', None)
            r_ffc = request.GET.get('filesFromChat', None)

            # Вывод сообщений из чата
            if r_mfc is not None:
                messages_chat = MessageChatUser.objects.filter(chat=chat)
                obj_messages = []
                for message in messages_chat:
                    created_datetime = '{}:{} {}.{}.{}'.format(
                        message.created_time.hour, message.created_time.minute,
                        message.created_date.day, message.created_date.month, message.created_date.year
                    )
                    updated_datetime = '{}:{} {}.{}.{}'.format(
                        message.updated_time.hour, message.updated_time.minute,
                        message.updated_date.day, message.updated_date.month, message.updated_date.year
                    )
                    _dict = {
                        'avatar': message.owner.avatar.url if message.owner.avatar else '/static/img/noimage.png',
                        'owner': message.owner.get_full_name() if message.owner.get_full_name else message.owner.email,
                        'message': message.message,
                        'created_datetime': created_datetime,
                        'updated_datetime': updated_datetime,
                    }
                    obj_messages.append(_dict)

                data = json.dumps(obj_messages)
                return HttpResponse(data, content_type="application/json")

            # Вывод файлов из чата
            if r_ffc is not None:
                files_chat = FileChatUser.objects.filter(chat=chat)
                obj_files = []
                for file in files_chat:
                    created_datetime = '{}:{} {}.{}.{}'.format(
                        file.created_time.hour, file.created_time.minute,
                        file.created_date.day, file.created_date.month, file.created_date.year
                    )
                    _dict = {
                        'avatar': file.owner.avatar.url if file.owner.avatar else '/static/img/noimage.png',
                        'owner': file.owner.get_full_name() if file.owner.get_full_name else file.owner.email,
                        'name': file.filename(),
                        'link': F'{file.file}',
                        'created_datetime': created_datetime,
                    }
                    obj_files.append(_dict)

                data = json.dumps(obj_files)
                return HttpResponse(data, content_type="application/json")

        user = User.objects.get(email=request.user)
        if access_to_manager_and_admin(request.user) or chat.user == user:
            context = {
                'chat': chat,
                'messages_from_chat': messages_from_chat,
                'files_from_chat': files_from_chat
            }
            return render(request, 'accounts/chat/main.html', context=context)
        else:
            return redirect(F'/chat/{request.user.chatuser.id}/')

    @staticmethod
    def post(request, pk):
        if request.is_ajax():
            message = request.POST['message']
            files = request.FILES.getlist('files[]')
            chat = ChatUser.objects.get(id=pk)
            user = User.objects.get(email=request.user)

            if len(files) != 0:
                for f in files:
                    print(f)
                    file = FileChatUser()
                    file.chat = chat
                    file.owner = user
                    file.file = f
                    file.save()

            if message != '':
                message_chat = MessageChatUser()
                message_chat.owner = user
                message_chat.chat = chat
                message_chat.message = message
                message_chat.save()

                return JsonResponse({'ok': 'asd'})

            return JsonResponse({'error': 'Not message'})



        else:
            messages.error(request, 'This is not ajax request')