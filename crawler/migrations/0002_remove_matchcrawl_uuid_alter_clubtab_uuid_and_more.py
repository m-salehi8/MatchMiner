# Generated by Django 5.1.7 on 2025-03-12 22:44

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crawler', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='matchcrawl',
            name='uuid',
        ),
        migrations.AlterField(
            model_name='clubtab',
            name='uuid',
            field=models.UUIDField(default=uuid.UUID('d60a614e-4431-4a8b-bef5-ce29bac9e4ac'), editable=False, unique=True),
        ),
        migrations.AlterField(
            model_name='indextab',
            name='uuid',
            field=models.UUIDField(default=uuid.UUID('ae6e7454-8f70-4490-a330-d75525f7a5ae'), editable=False, unique=True),
        ),
        migrations.AlterField(
            model_name='lineupstab',
            name='uuid',
            field=models.UUIDField(default=uuid.UUID('ab7dcaec-c88d-4113-b2c9-5aec71ea00f8'), editable=False, unique=True),
        ),
        migrations.AlterField(
            model_name='statisticstab',
            name='uuid',
            field=models.UUIDField(default=uuid.UUID('3616b173-f66b-4909-b151-953226aac254'), editable=False, unique=True),
        ),
        migrations.AlterField(
            model_name='timelinetab',
            name='uuid',
            field=models.UUIDField(default=uuid.UUID('86a7a46d-e5da-4ebd-956b-49809914c6c5'), editable=False, unique=True),
        ),
    ]
