# Generated by Django 3.1.1 on 2020-12-22 12:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_auto_20200820_1654'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='liked',
        ),
        migrations.DeleteModel(
            name='Like',
        ),
    ]
