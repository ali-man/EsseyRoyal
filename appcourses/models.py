import os

from django.db import models

from appusers.models import User

from pytils.translit import slugify


# TODO: Написать дату принятия заказа Writer-ом/Manager-ом


class Course(models.Model):
    customer = models.ForeignKey(User, verbose_name='Customer', related_name='course_customer',
                                 on_delete=models.CASCADE)
    title = models.CharField(verbose_name='Title', max_length=100)
    manager = models.ForeignKey(User, verbose_name='Manager', related_name='course_manager', on_delete=models.CASCADE,
                                blank=True, null=True)
    price = models.DecimalField(verbose_name='Price from tasks', max_digits=10, decimal_places=2, default=0)
    created_datetime = models.DateTimeField(verbose_name='Created datetime', auto_now_add=True)

    class Meta:
        verbose_name = 'Course'
        verbose_name_plural = 'Courses'
        ordering = ['-id']

    def save(self, *args, **kwargs):
        if self.manager is None:
            # TODO: Отправить уведомление на почту всем менеджерам
            pass
        tasks = Task.objects.filter(course__id=self.id)
        if len(tasks) != 0:
            self.price = sum([i.price_for_customer for i in tasks])
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class CourseFile(models.Model):
    course = models.ForeignKey(Course, verbose_name='Course', on_delete=models.CASCADE)
    file = models.FileField(verbose_name='File', upload_to='customer/course/files/%Y/%m/%d/', null=True, blank=True)
    created_datetime = models.DateTimeField(verbose_name='Created datetime', auto_now_add=True)

    class Meta:
        verbose_name = 'Course File'
        verbose_name_plural = 'Course Files'

    def filename(self):
        return os.path.basename(self.file.name)

    def __str__(self):
        return '%s' % self.id


class Task(models.Model):
    PRICE_SETTING = 1
    PRICE_ACCESS = 2

    PRICE_STATUS = (
        (PRICE_SETTING, 'Price setting'),
        (PRICE_ACCESS, 'Price access'),
    )

    IN_REVIEW = 0
    IN_PROCESS = 1
    COMPLETED = 2

    STATUS = (
        (IN_REVIEW, 'In review'),
        (IN_PROCESS, 'In process'),
        (COMPLETED, 'Completed'),
    )

    course = models.ForeignKey(Course, verbose_name='Course', on_delete=models.CASCADE)
    title = models.CharField(verbose_name='Title', max_length=50)
    slug = models.SlugField(verbose_name='URL', max_length=50, blank=True)
    question = models.TextField(verbose_name='Question', blank=True)
    pages = models.IntegerField(verbose_name='Pages', default=1)
    description = models.TextField(verbose_name='Description', blank=True)
    due_date = models.DateTimeField(verbose_name='Due date', blank=True)
    price_for_writer = models.DecimalField(verbose_name='Price for writer', max_digits=10, decimal_places=2, null=True,
                                           blank=True)
    price_for_customer = models.DecimalField(verbose_name='Price for customer', max_digits=10, decimal_places=2)
    to_writer = models.BooleanField(verbose_name='To writer', default=False)
    writer = models.ForeignKey(User, verbose_name='Writer', related_name='task_writer',
                               on_delete=models.CASCADE, blank=True, null=True)
    price_status = models.IntegerField(verbose_name='Price status', choices=PRICE_STATUS, default=0)
    status = models.IntegerField(verbose_name='Status', choices=STATUS, default=0)
    created_datetime = models.DateTimeField(verbose_name='Created datetime', auto_now_add=True)

    class Meta:
        verbose_name = 'Task'
        verbose_name_plural = 'Tasks'
        ordering = ['-id']

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)
        Course.objects.get(id=self.course.id).save()

    def __str__(self):
        return self.title


class TaskFile(models.Model):
    task = models.ForeignKey(Task, verbose_name='Task', on_delete=models.CASCADE)
    file = models.FileField(verbose_name='File', upload_to='manager/course/replies/%Y/%m/%d/', null=True, blank=True)
    created_datetime = models.DateTimeField(verbose_name='Created datetime', auto_now_add=True)

    class Meta:
        verbose_name = 'Task File'
        verbose_name_plural = 'Task Files'

    def filename(self):
        return os.path.basename(self.file.name)

    def __str__(self):
        return '%s' % self.id


class TaskFileCompleted(models.Model):
    task = models.ForeignKey(Task, verbose_name='Task', on_delete=models.CASCADE)
    file = models.FileField(verbose_name='File', upload_to='courses/completed/%Y/%m/%d/', null=True, blank=True)
    created_datetime = models.DateTimeField(verbose_name='Created datetime', auto_now_add=True)

    class Meta:
        verbose_name = 'Task File Completed'
        verbose_name_plural = 'Task Files Completed'

    def filename(self):
        return os.path.basename(self.file.name)

    def __str__(self):
        return '%s' % self.id
