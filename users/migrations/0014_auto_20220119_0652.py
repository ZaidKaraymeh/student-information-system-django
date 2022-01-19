# Generated by Django 3.2.9 on 2022-01-19 03:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0013_rename_assignmentsubmissionfiles_assignmentsubmissionfile'),
    ]

    operations = [
        migrations.AddField(
            model_name='assignmentsubmission',
            name='submitted',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='grade',
            name='letter_grade',
            field=models.CharField(choices=[('A', 'A'), ('A-', 'A-'), ('B', 'B'), ('B-', 'B-'), ('C', 'C'), ('C-', 'C-'), ('D', 'D'), ('D-', 'D-'), ('F', 'F')], default='A', max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='grade',
            name='point_grade',
            field=models.IntegerField(default=0),
        ),
    ]
