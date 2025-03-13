from django.db import models
from source.models import Source
import uuid


class LeagueData(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    uuid = models.UUIDField(default=uuid.uuid4(), unique=True, editable=False)
    source = models.ForeignKey(Source, on_delete=models.SET_NULL, null=True, blank=True, related_name="league" )

    name = models.CharField(max_length=150)
    country = models.CharField(max_length=100, blank=True, null=True)
    logo = models.URLField(blank=True, null=True)
    year = models.PositiveIntegerField()
    extra = models.JSONField(null=True, blank=True)

    def __str__(self):
        return self.name


class TeamData(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    uuid = models.UUIDField(default=uuid.uuid4(), unique=True, editable=False)
    source = models.ForeignKey(Source, on_delete=models.SET_NULL, null=True, blank=True, related_name="teams" )

    url = models.CharField(max_length=256)
    name = models.CharField(max_length=150)
    logo = models.URLField(blank=True, null=True)
    manager = models.JSONField()
    player = models.JSONField()
    composition = models.CharField(max_length=50)
    extra = models.JSONField()

    def __str__(self):
        return self.name


class StadiumData(models.Model):
    name = models.CharField(max_length=512)
    url = models.CharField(max_length=256)
    attendance = models.CharField(max_length=128)



class RefereeData(models.Model):
    name = models.CharField(max_length=512)
    url = models.CharField(max_length=512)
    assistant = models.JSONField()



class MatchData(models.Model):
    league = models.ForeignKey(LeagueData, on_delete=models.SET_NULL, blank=True, null=True)
    home_team = models.ForeignKey(TeamData, on_delete=models.CASCADE, related_name='home_matches')
    away_team = models.ForeignKey(TeamData, on_delete=models.CASCADE, related_name='away_matches')
    stadium = models.ForeignKey(StadiumData, on_delete=models.SET_NULL, blank=True, null=True)
    referee = models.ForeignKey(RefereeData, on_delete=models.SET_NULL, blank=True, null=True)

    match_date = models.DateTimeField(blank=True, null=True)

    home_score = models.IntegerField(blank=True, null=True)
    away_score = models.IntegerField(blank=True, null=True)
    match_id = models.CharField(max_length=200, null=True, blank=True)

    sku = models.CharField(max_length=100, unique=True, blank=True, null=True)
    full_time_result = models.CharField(max_length=10, blank=True, null=True)
    extra_time_result = models.CharField(max_length=10, blank=True, null=True)
    url = models.CharField(max_length=256)

    goals = models.JSONField()
    cards = models.JSONField()
    substitutions = models.JSONField()



    extra = models.JSONField(blank=True, null=True)

    def __str__(self):
        return f"{self.home_team} vs {self.away_team} on {self.date_time}"
