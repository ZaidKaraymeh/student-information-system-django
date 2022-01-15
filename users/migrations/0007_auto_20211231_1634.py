# Generated by Django 3.2.9 on 2021-12-31 13:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_assignment_date_posted'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='assignment',
            name='file',
        ),
        migrations.CreateModel(
            name='AssignmentFile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(null=True, upload_to='documents/%Y/%m/%d')),
                ('assignment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='assignment', to='users.assignment')),
            ],
        ),
    ]