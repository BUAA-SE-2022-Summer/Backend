# Generated by Django 4.0.6 on 2022-08-01 10:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0006_user_img'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='img',
            field=models.CharField(default='', max_length=256, verbose_name='头像'),
        ),
    ]
