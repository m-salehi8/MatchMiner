# Generated by Django 5.1.7 on 2025-03-13 01:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crawler', '0004_remove_indextab_uuid'),
    ]

    operations = [
        migrations.AddField(
            model_name='matchcrawl',
            name='has_club',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='matchcrawl',
            name='has_index',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='matchcrawl',
            name='has_line',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='matchcrawl',
            name='has_stik',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='matchcrawl',
            name='has_time',
            field=models.BooleanField(default=False),
        ),
    ]
