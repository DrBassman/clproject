# Generated by Django 2.1.3 on 2018-11-26 02:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cl', '0005_auto_20181119_1056'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='configdefaults',
            options={'verbose_name_plural': 'Defaults (only 1 record)'},
        ),
        migrations.AddField(
            model_name='contactlens',
            name='power_ranges',
            field=models.TextField(blank=True),
        ),
    ]