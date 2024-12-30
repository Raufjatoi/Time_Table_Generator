# Generated by Django 5.1.4 on 2024-12-29 14:49

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Subject',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('lectures_per_week', models.PositiveIntegerField()),
                ('duration_per_lecture', models.PositiveIntegerField()),
                ('is_major', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Timeslot',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('day', models.CharField(choices=[('Monday', 'Monday'), ('Tuesday', 'Tuesday'), ('Wednesday', 'Wednesday'), ('Thursday', 'Thursday'), ('Friday', 'Friday')], max_length=10)),
                ('start_time', models.TimeField()),
                ('end_time', models.TimeField()),
            ],
        ),
        migrations.CreateModel(
            name='Teacher',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('working_hours', models.CharField(max_length=100)),
                ('subjects', models.ManyToManyField(related_name='assigned_teachers', to='table.subject')),
            ],
        ),
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('year', models.CharField(max_length=100)),
                ('total_lectures_per_week', models.PositiveIntegerField()),
                ('start_time', models.TimeField()),
                ('end_time', models.TimeField()),
                ('major_subjects', models.ManyToManyField(limit_choices_to={'is_major': True}, related_name='major_in_departments', to='table.subject')),
                ('minor_subjects', models.ManyToManyField(limit_choices_to={'is_major': False}, related_name='minor_in_departments', to='table.subject')),
                ('teachers', models.ManyToManyField(to='table.teacher')),
            ],
        ),
        migrations.CreateModel(
            name='TimeTable',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('year_group', models.CharField(choices=[('1st Year', '1st Year'), ('2nd Year', '2nd Year'), ('3rd Year', '3rd Year'), ('4th Year', '4th Year'), ('Final Year', 'Final Year')], max_length=20)),
                ('department', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='table.department')),
                ('subject', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='table.subject')),
                ('timeslot', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='table.timeslot')),
            ],
            options={
                'unique_together': {('department', 'subject', 'timeslot', 'year_group')},
            },
        ),
    ]
