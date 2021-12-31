# Generated by Django 3.2.9 on 2021-12-28 07:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_rename_descrption_quiz_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='quiz',
            name='course',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='users.course'),
        ),
        migrations.AddField(
            model_name='quiz',
            name='instructor',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='users.customuser'),
        ),
        migrations.AddField(
            model_name='quiz',
            name='quiz_type',
            field=models.CharField(max_length=50, null=True),
        ),
    ]
