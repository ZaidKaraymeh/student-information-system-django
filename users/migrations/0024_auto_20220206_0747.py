# Generated by Django 3.2.9 on 2022-02-06 04:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0023_auto_20220206_0744'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='replies',
            field=models.ManyToManyField(to='users.Reply'),
        ),
        migrations.AlterField(
            model_name='message',
            name='files',
            field=models.ManyToManyField(to='users.MailFiles'),
        ),
    ]
