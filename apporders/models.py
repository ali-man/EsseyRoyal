import re
import docx
import xlrd
import io
import json
import datetime
import os
import threading

from django.conf import settings
from pdfminer.converter import TextConverter
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.pdfpage import PDFPage

from ckeditor.fields import RichTextField
from django.db import models

from EsseyRoyal.local_settings import LOCAL
from appmail.views import customer_send_mail, writer_send_mail, manager_send_mail
from apporders.validators import validate_file_extension
from appusers.models import User


# TODO: Написать дату принятия заказа Writer-ом


class FilterWord(models.Model):
    word = models.CharField(verbose_name='Word', max_length=30, unique=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        words = [F'{i.word}' for i in FilterWord.objects.all()]
        path = settings.STATICFILES_DIRS[0] if LOCAL else settings.STATIC_ROOT
        with open(path + '/words.json', 'w') as write_file:
            json.dump(words, write_file)

    def __str__(self):
        return self.word


class PriceDeadline(models.Model):
    days = models.IntegerField(verbose_name='Days', default=0)
    hours = models.IntegerField(verbose_name='Hours', default=0)
    price = models.DecimalField(verbose_name='Price', default=0, max_digits=10, decimal_places=2)

    class Meta:
        verbose_name = 'Price of deadline'
        verbose_name_plural = 'Prices of deadline'
        ordering = ['hours']

    def save(self, *args, **kwargs):
        if self.hours == 0:
            self.hours = self.days * 24
        super().save(*args, **kwargs)

    def __str__(self):
        return 'Days: %s / hours: %s / price: $ %s' % (self.days, self.hours, self.price)


class TypeOrder(models.Model):
    title = models.CharField(verbose_name='Type of order', max_length=50)
    price_client = models.DecimalField(verbose_name='Price for client (+ Price Deadline)', max_digits=10,
                                       decimal_places=2)
    price_writer = models.DecimalField(verbose_name='Price for writer', max_digits=10, decimal_places=2)

    def __str__(self):
        return self.title


class FormatOrder(models.Model):
    title = models.CharField(verbose_name='Format of order', max_length=50, unique=True)

    class Meta:
        verbose_name = 'Format of order'
        verbose_name_plural = 'Format of orders'

    def __str__(self):
        return self.title


class Order(models.Model):
    IN_REVIEW = 0
    IN_PROGRESS = 1
    COMPLETED = 2
    MODERATION = 3

    STATUS = (
        (IN_REVIEW, 'In review'),
        (IN_PROGRESS, 'In progress'),
        (COMPLETED, 'Completed'),
        (MODERATION, 'Moderation'),
    )
    customer = models.ForeignKey(User, verbose_name='Customer', related_name='order_customer', on_delete=models.CASCADE)
    title = models.CharField(verbose_name='Title of order', max_length=100)
    type_order = models.ForeignKey(TypeOrder, verbose_name='Type of order', on_delete=models.CASCADE, null=True)
    format_order = models.ForeignKey(FormatOrder, verbose_name='Format of order', on_delete=models.CASCADE)
    number_page = models.IntegerField(verbose_name='Number of page', default=1)
    deadline = models.DateTimeField(verbose_name='Deadline', auto_now=False)
    description = RichTextField(verbose_name='Description', blank=True)
    status = models.IntegerField(verbose_name='Status order', choices=STATUS, default=MODERATION)
    created_datetime = models.DateTimeField(verbose_name='Created datetime', auto_now_add=True)
    per_page = models.DecimalField(verbose_name='Price per page', max_digits=10, decimal_places=2, default=0)
    total_cost = models.DecimalField(verbose_name='Total cost', max_digits=10, decimal_places=2, default=0)
    writer = models.ForeignKey(User, verbose_name='Writer', related_name='order_writer', on_delete=models.CASCADE,
                               null=True, blank=True)
    completed_datetime = models.DateTimeField(verbose_name='Completed datetime', auto_now=True)

    class Meta:
        verbose_name = 'Order'
        verbose_name_plural = 'Orders'
        ordering = ['-id']

    def total_cost_writer(self):
        result = self.type_order.price_writer * self.number_page
        return result

    def save(self, *args, **kwargs):
        if self.created_datetime:
            deadline = (self.deadline - self.created_datetime).total_seconds()
        else:
            deadline = (self.deadline - datetime.datetime.now()).total_seconds()
        hours = int(divmod(deadline, 3600)[0])
        deadlines_price = PriceDeadline.objects.filter(hours__lte=hours)
        last_index = len(deadlines_price) - 1  # Последний индекс из queryset
        price = deadlines_price[last_index].price + self.type_order.price_client  # Цена type of order
        self.per_page = price
        self.total_cost = price * self.number_page

        super().save(*args, **kwargs)

        manager_link_order = F'dashboard/m/order/{self.id}/'
        writer_link_order = F'dashboard/w/order/{self.id}/'
        customer_link_order = F'order/progress/{self.id}/'
        if self.status == 0:
            manager_send_mail('New order', self.customer, self.title, manager_link_order)
            writer_send_mail('New order', self.title, writer_link_order)
        elif self.status == 1:
            customer_send_mail('Take task', self.title, self.customer.email, customer_link_order)
            manager_send_mail('Take order', self.writer, self.title, manager_link_order)
        elif self.status == 2:
            writer_send_mail('Completed order', self.title, '')
            manager_send_mail('Completed order', self.writer, self.title, manager_link_order)

    def __str__(self):
        return self.title


class FilesOrder(models.Model):
    order = models.ForeignKey(Order, verbose_name='ID Order', on_delete=models.CASCADE)
    file = models.FileField(verbose_name='Attached files', upload_to='customer/order/files/%Y/%m/%d/',
                            validators=[validate_file_extension],
                            null=True, blank=True)

    def filename(self):
        return os.path.basename(self.file.name)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        threading.Thread(target=checking_files(self.file, self.order.id)).start()

    def __str__(self):
        return '%s' % self.id


class FeedbackOrder(models.Model):
    order = models.OneToOneField(Order, verbose_name='Order', on_delete=models.CASCADE)
    text = models.TextField(verbose_name='Message', blank=True)
    rating = models.IntegerField(verbose_name='Rating', null=True, blank=True)

    class Meta:
        verbose_name = 'Feedback order'
        verbose_name_plural = "Feedback's order"

    def __str__(self):
        return '%s' % self.text


class AdditionallyOrder(models.Model):
    order = models.OneToOneField(Order, verbose_name='Order', on_delete=models.CASCADE)
    created_datetime = models.DateTimeField(verbose_name='Created datetime', auto_now_add=True)
    updated_datetime = models.DateTimeField(verbose_name='Updated datetime', auto_now=True)

    class Meta:
        verbose_name = 'Additionally order'
        verbose_name_plural = 'Additionally orders'

    def __str__(self):
        return '%s' % self.order


class FilesAdditionallyOrder(models.Model):
    additionally_order = models.ForeignKey(AdditionallyOrder, verbose_name='Additionally order',
                                           on_delete=models.CASCADE)
    file = models.FileField(verbose_name='File', upload_to='writer/order/files/%Y/%m/%d/')
    created_datetime = models.DateTimeField(verbose_name='Created datetime', auto_now_add=True)

    class Meta:
        verbose_name = 'File additionally order'
        verbose_name_plural = 'Files additionally order'

    def filename(self):
        return os.path.basename(self.file.name)

    def __str__(self):
        return '%s' % self.file.url


class Chat(models.Model):
    order = models.ForeignKey(Order, verbose_name='Order', on_delete=models.CASCADE)
    user = models.ForeignKey(User, verbose_name='User', on_delete=models.CASCADE)
    message = models.TextField(verbose_name='Message')
    status = models.BooleanField(verbose_name='Send', default=False)
    created_datetime = models.DateTimeField(verbose_name='Created datetime', auto_now_add=True)

    class Meta:
        verbose_name = 'Chat'
        verbose_name_plural = 'Chats'

    def __str__(self):
        return self.message


class SearchWord:

    def search_word(self, line_sting):
        with open(settings.STATIC_ROOT + '/words.json', 'r') as read_file:
            WORDS = json.load(read_file)
        texts = []
        for word in WORDS:
            t = re.search(word, line_sting.lower())
            if t is not None:
                texts.append(t.group())
        return texts


class Processing:
    FORMATS = ['docx', 'xls', 'xlsx', 'excel', 'pdf']
    sw = SearchWord()

    def moderation_order(self, words, order_id):
        order = Order.objects.get(id=order_id)

        # TODO: Фильтр слов по полю Description

        if len(words) > 0:
            manager_send_mail('title mail', order.customer, F'{order.title} {words}', F'dashboard/m/order/{order.id}/')
        else:
            order.status = 0
            order.save()

    def extract_text_by_page(self, pdf_path):
        with open(pdf_path, 'rb') as fh:
            for page in PDFPage.get_pages(fh,
                                          caching=True,
                                          check_extractable=True):
                resource_manager = PDFResourceManager()
                fake_file_handle = io.StringIO()
                converter = TextConverter(resource_manager, fake_file_handle)
                page_interpreter = PDFPageInterpreter(resource_manager, converter)
                page_interpreter.process_page(page)

                text = fake_file_handle.getvalue()
                yield text

                converter.close()
                fake_file_handle.close()

    def processing_pdf(self, _file, obj_id):
        """ Работа с pdf файлами
            Читает все страницы
        """
        filter_words = []
        for page in self.extract_text_by_page(_file.path):
            try:
                filter_words += list(self.sw.search_word(page))
            except TypeError:
                continue

        self.moderation_order(filter_words, obj_id)

    def processing_docx(self, _file, obj_id):
        """ Работа с docx файлами
            Читает все страницы по строчкам, пустые строки пропускает
        """
        doc = docx.Document(_file.path)
        filter_words = []
        for line in doc.paragraphs:
            if len(line.text) != 0:
                filter_words += list(self.sw.search_word(line.text))

        self.moderation_order(filter_words, obj_id)

    def processing_excel(self, f, obj_id):
        """
        Работа с 'xls', 'xlsx', 'excel' файлами
        Читает все страницы по строчкам, пустые строчки пропускает
        :param f: полученный файл из модели '' из метода save()
        :return:
        """
        rb = xlrd.open_workbook(f.path)
        filter_words = []
        for i in range(rb.nsheets):
            sheet = rb.sheet_by_index(i)
            for rownum in range(sheet.nrows):
                row = sheet.row_values(rownum)
                for c_el in row:
                    if len(str(c_el)) > 0:
                        filter_words += list(self.sw.search_word(str(c_el)))

        self.moderation_order(filter_words, obj_id)


def checking_files(f, obj_id):
    pc = Processing()
    file_format = f.name.split('.')[-1]

    if file_format == 'docx':
        pc.processing_docx(f, obj_id)

    elif file_format == 'xls' or file_format == 'xlsx' or file_format == 'excel':
        pc.processing_excel(f, obj_id)

    elif file_format == 'pdf':
        pc.processing_pdf(f, obj_id)

    else:
        pass