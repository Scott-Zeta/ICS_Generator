# Generated by Django 5.0.4 on 2024-04-09 05:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('generator_core', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='downloadrecord',
            old_name='acess_time',
            new_name='access_time',
        ),
        migrations.RenameField(
            model_name='uploadrecord',
            old_name='acess_time',
            new_name='access_time',
        ),
    ]
