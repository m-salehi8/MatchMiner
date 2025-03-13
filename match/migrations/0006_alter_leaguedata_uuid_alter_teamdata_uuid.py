# Generated by Django 5.1.7 on 2025-03-12 20:52

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('match', '0005_alter_leaguedata_uuid_alter_teamdata_uuid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='leaguedata',
            name='uuid',
            field=models.UUIDField(default=uuid.UUID('c48c0435-3265-424a-a111-eb69c9796f24'), editable=False, unique=True),
        ),
        migrations.AlterField(
            model_name='teamdata',
            name='uuid',
            field=models.UUIDField(default=uuid.UUID('52d57797-f09d-4b0b-8031-cae66e8dfa72'), editable=False, unique=True),
        ),
    ]
