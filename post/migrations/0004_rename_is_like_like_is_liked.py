# Generated by Django 4.2.1 on 2023-05-11 13:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0003_like'),
    ]

    operations = [
        migrations.RenameField(
            model_name='like',
            old_name='is_like',
            new_name='is_liked',
        ),
    ]