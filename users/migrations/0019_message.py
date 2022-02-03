# Generated by Django 3.2.9 on 2022-02-02 10:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0018_remove_assignmentsubmission_grade'),
    ]

    operations = [
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=250)),
                ('content', models.TextField(max_length=9000)),
                ('date_sent', models.DateTimeField(auto_now_add=True)),
                ('recievers', models.ManyToManyField(to='users.CustomUser')),
                ('sender', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sender', to='users.customuser')),
            ],
        ),
    ]
