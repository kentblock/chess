# Generated by Django 3.0.8 on 2020-09-23 22:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0024_auto_20200921_1741'),
    ]

    operations = [
        migrations.AddField(
            model_name='move',
            name='notation',
            field=models.CharField(default='Bxe5', max_length=10),
            preserve_default=False,
        ),
    ]