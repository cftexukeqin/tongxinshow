# Generated by Django 2.0.5 on 2020-05-19 13:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('front', '0002_auto_20200507_2110'),
    ]

    operations = [
        migrations.CreateModel(
            name='Data',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=300)),
                ('year', models.CharField(default='2020', max_length=4)),
                ('jidu', models.CharField(default='', max_length=10)),
                ('nums', models.FloatField(default=0)),
                ('add_time', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.DeleteModel(
            name='Document',
        ),
    ]
