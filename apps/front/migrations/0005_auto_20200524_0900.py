# Generated by Django 2.1.7 on 2020-05-24 09:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('front', '0004_auto_20200519_1443'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='data',
            options={'ordering': ['add_time']},
        ),
    ]
