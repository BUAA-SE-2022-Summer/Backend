# Generated by Django 4.0.6 on 2022-08-10 11:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='File',
            fields=[
                ('fileID', models.AutoField(editable=False, primary_key=True, serialize=False)),
                ('file_name', models.CharField(max_length=100)),
                ('file_type', models.CharField(default='doc', max_length=100)),
                ('fatherID', models.IntegerField(default=0)),
                ('content', models.TextField(max_length=65535, null=True)),
                ('isDelete', models.BooleanField(default=False)),
                ('is_star', models.BooleanField(default=False)),
                ('create_time', models.DateTimeField(auto_now_add=True)),
                ('last_modify_time', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'file',
            },
        ),
        migrations.CreateModel(
            name='Xml',
            fields=[
                ('xmlID', models.AutoField(editable=False, primary_key=True, serialize=False)),
                ('xml_name', models.CharField(max_length=100)),
                ('content', models.TextField(max_length=65535, null=True)),
                ('create_time', models.DateTimeField(auto_now_add=True)),
                ('last_modify_time', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='user.user')),
            ],
        ),
    ]
