# Generated by Django 4.0.6 on 2022-08-01 03:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0003_user_email_user_identity_user_phone_user_real_name_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='identity',
        ),
    ]
