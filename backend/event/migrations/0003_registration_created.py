# Generated by Django 3.2.9 on 2021-12-02 16:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('event', '0002_auto_20211202_1241'),
    ]

    operations = [
        migrations.AddField(
            model_name='registration',
            name='created',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
