# Generated by Django 3.2.9 on 2021-12-01 19:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='announcement',
            old_name='owner',
            new_name='author',
        ),
    ]