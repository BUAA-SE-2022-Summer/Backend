# Generated by Django 4.0.3 on 2022-07-27 07:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='username',
            field=models.CharField(default='', max_length=64, verbose_name='用户名'),
        ),
    ]
