# Generated by Django 5.1.7 on 2025-03-12 22:33

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('source', '0005_alter_matchlinks_extra_alter_source_uuid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='source',
            name='uuid',
            field=models.UUIDField(default=uuid.UUID('c60a35a3-c9ab-46a0-9c10-b8623f552a42'), editable=False, unique=True),
        ),
    ]
