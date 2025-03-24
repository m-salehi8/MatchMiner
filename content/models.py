from django.db import models

# Create your models here.
from django.db import models
from source.models import Source, LeagueSeasonLinks, LeagueLinks
import uuid


class Team(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    url = models.CharField(max_length=256)
    name = models.CharField(max_length=150)
    logo = models.URLField(blank=True, null=True)
    extra = models.JSONField()

    def __str__(self):
        return self.name



class Stadium(models.Model):
    name = models.CharField(max_length=512)
    url = models.CharField(max_length=256)
    attendance = models.CharField(max_length=128)

    def __str__(self):
        return self.name


class Referee(models.Model):
    name = models.CharField(max_length=512)
    url = models.CharField(max_length=512)
    assistant = models.JSONField()

    def __str__(self):
        return self.name


class Player(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    name = models.CharField(max_length=512)
    url = models.CharField(max_length=512)
    image = models.CharField(blank=True, null=True, max_length=512)
    country = models.CharField(max_length=512)

    def __str__(self):
        return self.name


class Manager(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    name = models.CharField(max_length=512)
    url = models.CharField(max_length=512)
    image = models.CharField(blank=True, null=True, max_length=512)
    country = models.CharField(max_length=512)

    def __str__(self):
        return self.name


class Match(models.Model):
    league = models.ForeignKey(LeagueLinks, on_delete=models.SET_NULL, blank=True, null=True)
    session = models.ForeignKey(LeagueSeasonLinks, on_delete=models.SET_NULL, blank=True, null=True)
    stadium = models.ForeignKey(Stadium, on_delete=models.SET_NULL, blank=True, null=True)
    referee = models.ForeignKey(Referee, on_delete=models.SET_NULL, blank=True, null=True)

    match_date = models.CharField(blank=True, null=True, max_length=20)
    match_time = models.CharField(blank=True, null=True, max_length=20)
    match_day = models.CharField(blank=True, null=True, max_length=20)

    home_score = models.IntegerField(blank=True, null=True)
    away_score = models.IntegerField(blank=True, null=True)
    match_id = models.CharField(max_length=200, null=True, blank=True)
    url = models.CharField(max_length=256)
    extra = models.JSONField(blank=True, null=True)


    statistics = models.JSONField(blank=True, null=True)
    club = models.JSONField(blank=True, null=True)
    home_goals = models.JSONField(blank=True, null=True)
    away_goals = models.JSONField(blank=True, null=True)
    home_cards = models.JSONField(blank=True, null=True)
    away_cards = models.JSONField(blank=True, null=True)
    home_substitutions = models.JSONField(blank=True, null=True)
    away_substitutions = models.JSONField(blank=True, null=True)



    def __str__(self):
#        return f"{self.home_team} vs {self.away_team}"
        return f"{self.match_id}"



class MatchTeam(models.Model):
    STATUS_CHOICES = (
        ("home", "Home"),
        ("away", "Away"),
        ("other", "Other"),
    )
    match = models.ForeignKey(Match, on_delete=models.CASCADE, related_name="teams")
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name="teams")
    state = models.CharField(max_length=50, choices=STATUS_CHOICES)
    winner = models.BooleanField(default=False)
    position = models.IntegerField(blank=True, null=True)
    goals = models.JSONField()
    Manager = models.ForeignKey(Manager, on_delete=models.CASCADE, related_name="teams")


class MatchTeamPlayer(models.Model):
    POST_CHOICES = (
        ("goalkeeper", "Goalkeeper"),
        ("centre", "Centre"),
        ("defensive", "Defensive"),
        ("attacking", "Attacking")
    )
    match_team = models.ForeignKey(MatchTeam, on_delete=models.CASCADE, related_name="players")
    player = models.ForeignKey(Player, on_delete=models.CASCADE, related_name="players")
    post = models.CharField(max_length=50, choices=POST_CHOICES)
    main_player = models.BooleanField(default=False)
    number = models.CharField(blank=True, null=True, max_length=50)
    market_value = models.CharField(blank=True, null=True, max_length=50,)
    is_captain = models.BooleanField(default=False)
    goal = models.BooleanField(default=False)
    card = models.BooleanField(default=False)
    substitutes = models.BooleanField(default=False)
