# Generated by Django 3.0.8 on 2020-07-19 11:54

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Contract',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('payed', models.BooleanField(default=False)),
                ('amount', models.IntegerField(null=True)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='KillerManager',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_of_work_time', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Victim',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time_of_death', models.DateTimeField(null=True)),
                ('username', models.CharField(max_length=250)),
                ('age', models.IntegerField()),
                ('difficulty', models.IntegerField()),
                ('priority', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Link',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('post_victim', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='post_victim', to='api.Victim')),
                ('pre_victim', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pre_victim', to='api.Victim')),
            ],
        ),
        migrations.CreateModel(
            name='ContractToVictim',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('contract', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.Contract')),
                ('victim', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.Victim')),
            ],
        ),
    ]
