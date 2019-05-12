from django.contrib import messages
from django.shortcuts import render, redirect

from appusers.models import User


class DashBoardMixin:
    model = None
    template = None
    profile = None

    def get(self, request):
        if request.user.is_anonymous:
            return redirect('/')

        self.profile = User.objects.get(id=request.user.id)

        model_name = self.model.__class__.__name__.lower()
        return render(request, self.template, context={
            model_name: self.model,
            'profile': self.profile
        })


class EditProfileMixin:
    model = None
    form = None
    template = None

    def get(self, request, pk):
        m = self.model.objects.get(id=pk)
        f = self.form(instance=m)
        model_name = self.model.__name__.lower()
        return render(request, self.template, context={
            'form': f,
            model_name: m
        })

    def post(self, request, pk):
        m = self.model.objects.get(id=pk)
        f = self.form(request.POST, request.FILES, instance=m)

        model_name = self.model.__name__.lower()
        if f.is_valid():
            if 'photo' in request.FILES:
                f.photo = request.FILES['photo']
            f.save()
            messages.success(request, 'Врайтер успешно изменён (перевести)')
            return redirect(F'/admin/{model_name}s/')
        else:
            return render(request, self.template, context={
                'form': f,
                model_name: m
            })
