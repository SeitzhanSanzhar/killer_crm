# Generated by Django 3.0.8 on 2020-07-18 14:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_link_victim'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='victim',
            name='status',
        ),
        migrations.AddField(
            model_name='victim',
            name='priority',
            field=models.IntegerField(null=True),
        ),
    ]
