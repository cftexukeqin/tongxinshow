# Generated by Django 2.0.5 on 2020-05-18 22:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_userprofile_image'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userprofile',
            old_name='name',
            new_name='nick_name',
        ),
    ]
