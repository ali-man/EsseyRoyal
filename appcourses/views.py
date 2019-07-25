# import datetime
#
# from django.utils.timezone import make_aware
# from django.contrib import messages
# from django.db.models import Q
# from django.shortcuts import render, redirect
#
# from appcourses.forms import TaskForm
# from appcourses.models import CourseFile, Course, Task, TaskFile
# from appusers.models import User
#
#
# def customer_index(request):
#
#     if request.method == 'GET':
#         # TODO: Выводить только те курсы, у которых статус 2
#         courses = Course.objects.all()
#
#         return render(request, 'dashboard/customer/course/index.html', locals())
#
#     if request.method == 'POST':
#         user = User.objects.get(email=request.user)
#         if request.POST['title'] != '':
#             title = request.POST['title']
#             files = request.FILES.getlist('files')
#             course = Course()
#             course.customer = user
#             course.title = title
#             course.save()
#             if len(files) != 0:
#                 for f in files:
#                     file = CourseFile()
#                     file.course = course
#                     file.file = f
#                     file.save()
#
#         return render(request, 'dashboard/customer/course/index.html', locals())
#
#
# def manager_courses(request):
#     user = User.objects.get(email=request.user)
#     tasks = Task.objects.all()
#     courses = Course.objects.filter(Q(manager=None) | Q(manager=user))
#     in_review = tasks.filter(price_status=2, status=0)
#     in_process = tasks.filter(price_status=2, status=1)
#     completed = tasks.filter(price_status=2, status=2)
#     context = {
#         'courses': courses,
#         'in_review': in_review,
#         'in_process': in_process,
#         'completed': completed,
#     }
#
#     return render(request, 'dashboard/manager/courses/index.html', context=context)
#
#
# def to_datetime(_datetime):
#     # 2019-06-30T12:12
#     dt = _datetime.split('T')  # ['2019-06-30', '12:12']
#     d = [int(d) for d in dt[0].split('-')]  # [2019, 06, 30]
#     t = [int(t) for t in dt[1].split(':')]  # [12, 12]
#     format_date = datetime.datetime(d[0], d[1], d[2], t[0], t[1])
#     aware_datetime = make_aware(format_date)
#     return aware_datetime
#
#
# # TODO: Закрыть доступ всем кроме менеджеров
# def manager_course_detail(request, course_id):
#     course = Course.objects.get(id=course_id)
#     form = TaskForm()
#     # writers = User.objects.filter(groups__name='Writer')
#
#     if request.method == 'POST':
#         if 'send_customer' in request.POST:
#             task = Task.objects.get(id=int(request.POST['send_customer']))
#             task.price_status = 1
#             task.save()
#             # TODO: Отправить уведомление заказчику о новых тасках
#         else:
#             form = TaskForm(request.POST)
#             attached_files = request.FILES.getlist('attached-files')
#             dt = to_datetime(request.POST['due_date'])
#             if form.is_valid():
#                 cd = form.cleaned_data
#                 task = Task()
#                 task.course = course
#                 task.title = cd['title']
#                 task.due_date = dt
#                 task.question = cd['question']
#                 task.pages = cd['pages']
#                 task.description = cd['description']
#                 task.price_for_customer = cd['price_for_customer']
#                 if cd['to_writer']:
#                     task.to_writer = cd['to_writer']
#                     # writer = User.objects.get(email=cd['writer'])
#                     # task.writer = writer
#                     task.price_for_writer = cd['price_for_writer']
#                 task.save()
#                 if len(attached_files) != 0:
#                     for f in attached_files:
#                         file = TaskFile()
#                         file.task = task
#                         file.file = f
#                         file.save()
#                 messages.success(request, 'Added new task')
#                 return redirect('/dashboard/m/courses/{}/'.format(course_id))
#             else:
#                 messages.error(request, 'The fields are incorrectly filled')
#
#     return render(request, 'dashboard/manager/courses/detail.html', locals())
#
#
# # TODO: Закрыть доступ всем кроме заказчика
# def customer_course_detail(request, course_id):
#     course = Course.objects.get(id=course_id)
#
#     if request.method == 'POST':
#         r = request.POST
#         he_take = r.get('he_rake', None)
#         agree = r.get('agree', None)
#
#         if he_take is not None:
#             task = Task.objects.get(id=int(he_take))
#             task.delete()
#             # TODO: Написать уведомление на почту менеджеру об отказе от таска
#
#         if agree is not None:
#             task = Task.objects.get(id=int(agree))
#             task.price_status = 2
#             task.save()
#             # TODO: Написать уведомление на почту менеджеру о согласие на таск, а так же, уведомление врайтерам о новом таске
#
#     return render(request, 'dashboard/customer/course/detail.html', locals())