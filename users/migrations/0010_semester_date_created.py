# Generated by Django 3.2.9 on 2022-03-25 06:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0009_semester_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='semester',
            name='date_created',
            field=models.DateField(auto_now_add=True, null=True),
        ),
    ]
