# Generated by Django 3.2.9 on 2022-01-13 12:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0009_auto_20220113_1350'),
    ]

    operations = [
        migrations.RenameField(
            model_name='attendance',
            old_name='attendace_reports',
            new_name='attendance_reports',
        ),
    ]
