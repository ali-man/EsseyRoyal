import os
from django.core.exceptions import ValidationError


def validate_file_extension(value):
    ext = os.path.splitext(value.name)[1]
    valid_extensions = ['.pdf', '.doc', '.docx', '.jpg', '.png', '.xlsx', '.xls', '.excel']
    if not ext.lower() in valid_extensions:
        raise ValidationError('Неподдерживаемое расширение файла.')


def validate_file_views(value):
    ext = os.path.splitext(value.name)[1]
    valid_extensions = ['.pdf', '.doc', '.docx', '.jpg', '.png', '.xlsx', '.xls', '.excel']
    if not ext.lower() in valid_extensions:
        return 'error'
    else:
        return 'ok'
