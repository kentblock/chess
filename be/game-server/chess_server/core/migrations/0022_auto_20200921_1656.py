# Generated by Django 3.0.8 on 2020-09-21 16:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0021_auto_20200917_2311'),
    ]

    operations = [
        migrations.RenameField(
            model_name='game',
            old_name='started',
            new_name='_started',
        ),
    ]