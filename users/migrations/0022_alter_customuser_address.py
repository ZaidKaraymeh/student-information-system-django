# Generated by Django 3.2.9 on 2021-12-21 08:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0021_auto_20211128_1748'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='address',
            field=models.CharField(max_length=500, null=True),
        ),
    ]
