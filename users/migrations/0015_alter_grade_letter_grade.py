# Generated by Django 3.2.9 on 2022-01-22 09:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0014_auto_20220119_0652'),
    ]

    operations = [
        migrations.AlterField(
            model_name='grade',
            name='letter_grade',
            field=models.CharField(choices=[('A', 'A'), ('A-', 'A-'), ('B', 'B'), ('B-', 'B-'), ('C', 'C'), ('C-', 'C-'), ('D', 'D'), ('D-', 'D-'), ('F', 'F')], default='F', max_length=50, null=True),
        ),
    ]
