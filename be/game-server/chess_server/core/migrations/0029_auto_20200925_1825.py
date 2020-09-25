# Generated by Django 3.0.8 on 2020-09-25 18:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0028_auto_20200925_0139'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='is_active',
        ),
        migrations.RemoveField(
            model_name='user',
            name='is_staff',
        ),
        migrations.AddField(
            model_name='user',
            name='is_guest',
            field=models.BooleanField(default=False),
        ),
    ]