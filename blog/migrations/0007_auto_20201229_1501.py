# Generated by Django 3.1.1 on 2020-12-29 15:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0006_blogcomment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blogcomment',
            name='content',
            field=models.TextField(blank=True),
        ),
    ]