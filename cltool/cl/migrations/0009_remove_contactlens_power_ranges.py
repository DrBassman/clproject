# Generated by Django 2.1.3 on 2018-11-26 03:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cl', '0008_contactlens_power_ranges'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='contactlens',
            name='power_ranges',
        ),
    ]
