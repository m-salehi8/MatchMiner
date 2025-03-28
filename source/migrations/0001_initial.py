# Generated by Django 5.1.7 on 2025-03-12 19:57

import django.db.models.deletion
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('match', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='LeagueLinks',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=120)),
                ('start_year', models.PositiveIntegerField()),
                ('end_year', models.PositiveIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Source',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('uuid', models.UUIDField(default=uuid.UUID('5c6d4562-051e-4521-86d4-af4cf86a114f'), editable=False, unique=True)),
                ('name', models.CharField(max_length=100, unique=True)),
                ('base_url', models.URLField()),
                ('extra', models.JSONField(blank=True, null=True)),
                ('status', models.CharField(choices=[('active', 'Active'), ('running', 'Running'), ('complete', 'Complete'), ('failed', 'Failed')], default='active', max_length=128)),
            ],
        ),
        migrations.CreateModel(
            name='LeagueSeasonLinks',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('year', models.PositiveIntegerField()),
                ('match_count', models.PositiveIntegerField()),
                ('url', models.URLField()),
                ('league', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='season', to='source.leaguelinks')),
            ],
        ),
        migrations.CreateModel(
            name='MatchLinks',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.URLField()),
                ('match_id', models.CharField(max_length=200)),
                ('title', models.CharField(max_length=500)),
                ('status', models.CharField(choices=[('done', 'Done'), ('running', 'Running'), ('field', 'Field'), ('in_queue', 'In Queue')], max_length=200)),
                ('extra', models.JSONField()),
                ('is_done', models.BooleanField(default=False)),
                ('match_obj', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='match_link', to='match.matchdata')),
                ('session', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='matches', to='source.leagueseasonlinks')),
            ],
        ),
    ]
