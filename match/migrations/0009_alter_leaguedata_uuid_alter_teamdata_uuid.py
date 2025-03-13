# Generated by Django 5.1.7 on 2025-03-13 00:30

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('match', '0008_alter_leaguedata_uuid_alter_teamdata_uuid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='leaguedata',
            name='uuid',
            field=models.UUIDField(default=uuid.UUID('bac09765-cc07-4ccc-8a10-5a315319c66b'), editable=False, unique=True),
        ),
        migrations.AlterField(
            model_name='teamdata',
            name='uuid',
            field=models.UUIDField(default=uuid.UUID('b7e12f20-8651-40a8-bfcc-c520f25ded2a'), editable=False, unique=True),
        ),
    ]
