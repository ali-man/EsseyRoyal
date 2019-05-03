# Generated by Django 2.2.1 on 2019-05-03 00:55

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=50, verbose_name='First name')),
                ('second_name', models.CharField(max_length=50, verbose_name='Second name')),
                ('academic_institution', models.CharField(blank=True, max_length=100, verbose_name='Academic Institution')),
                ('phone', models.CharField(max_length=50, verbose_name='Phone number')),
                ('email', models.EmailField(max_length=100, verbose_name='Email')),
            ],
            options={
                'verbose_name': 'Client',
                'verbose_name_plural': 'Clients',
            },
        ),
        migrations.CreateModel(
            name='Manager',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=100, verbose_name='Имя')),
                ('second_name', models.CharField(max_length=100, verbose_name='Фамилия')),
                ('phone_number', models.CharField(max_length=30, verbose_name='Телефон номер')),
                ('corporate_email', models.EmailField(blank=True, max_length=254, verbose_name='Корпоративный email адрес')),
                ('personal_email', models.EmailField(max_length=254, verbose_name='Персональный email адрес')),
                ('photo', models.ImageField(blank=True, upload_to='dashboards/photo/managers/', verbose_name='Фото')),
            ],
            options={
                'verbose_name': 'Manager',
                'verbose_name_plural': 'Managers',
            },
        ),
        migrations.CreateModel(
            name='Writer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=50, verbose_name='First name')),
                ('second_name', models.CharField(max_length=50, verbose_name='Second name')),
                ('degree', models.CharField(max_length=100, verbose_name='Degree')),
                ('academic_institution', models.CharField(blank=True, max_length=100, verbose_name='Academic Institution')),
                ('phone_number', models.CharField(max_length=30, verbose_name='Телефон номер')),
                ('corporate_email', models.EmailField(blank=True, max_length=254, verbose_name='Корпоративный email адрес')),
                ('personal_email', models.EmailField(max_length=254, verbose_name='Персональный email адрес')),
                ('photo', models.ImageField(blank=True, upload_to='dashboards/photo/writers/', verbose_name='Фото')),
            ],
            options={
                'verbose_name': 'Writer',
                'verbose_name_plural': 'Writers',
            },
        ),
    ]
