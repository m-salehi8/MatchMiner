# Generated by Django 5.1.7 on 2025-03-14 20:03

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('match', '0015_alter_leaguedata_uuid_alter_teamdata_uuid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='leaguedata',
            name='uuid',
            field=models.UUIDField(default=uuid.UUID('7853db39-1d27-4861-8e1e-952bedd7e149'), editable=False, unique=True),
        ),
        migrations.AlterField(
            model_name='teamdata',
            name='uuid',
            field=models.UUIDField(default=uuid.UUID('3e8c3f18-e7eb-4805-bf0d-9a7d0cef6309'), editable=False, unique=True),
        ),
    ]
