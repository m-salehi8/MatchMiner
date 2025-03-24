from django.db import models
from source.models import MatchLinks, Source
import uuid

class MatchCrawl(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    source = models.ForeignKey(Source, on_delete=models.SET_NULL, null=True, blank=True, related_name="crawls" )
    match = models.ForeignKey(MatchLinks, on_delete=models.CASCADE, related_name="crawls")
    extra = models.JSONField(null=True, blank=True)

    has_index = models.BooleanField(default=False)
    has_line = models.BooleanField(default=False)
    has_stik = models.BooleanField(default=False)
    has_club = models.BooleanField(default=False)
    has_time = models.BooleanField(default=False)


class CleanData(models.Model):
    match = models.ForeignKey(MatchCrawl, on_delete=models.CASCADE, related_name="clean_data")
    match_pk = models.CharField(max_length=110, null=True, blank=True)
    title = models.CharField(max_length=1000, null=True, blank=True)
    year = models.PositiveSmallIntegerField(null=True, blank=True)
    league_name = models.CharField(max_length=500, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    statistics = models.JSONField(null=True, blank=True)
    league = models.JSONField(null=True, blank=True)
    related_data = models.JSONField(null=True, blank=True)
    stadium = models.JSONField(null=True, blank=True)
    referee = models.JSONField(null=True, blank=True)
    result = models.JSONField(null=True, blank=True)
    home_team = models.JSONField(null=True, blank=True)
    away_team = models.JSONField(null=True, blank=True)
    club = models.JSONField(null=True, blank=True)
    cards = models.JSONField(null=True, blank=True)
    goals = models.JSONField(null=True, blank=True)
    substitutions = models.JSONField(null=True, blank=True)
    match_date = models.JSONField(null=True, blank=True)



class IndexTab(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    match = models.ForeignKey(MatchCrawl, on_delete=models.CASCADE, related_name="indexes")
    extra = models.JSONField(null=True, blank=True)
    crawl_data = models.JSONField(null=True, blank=True)
    is_valid = models.BooleanField(default=False)


class LineUpsTab(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    match = models.ForeignKey(MatchCrawl, on_delete=models.CASCADE, related_name="lineups")
    extra = models.JSONField(null=True, blank=True)
    crawl_data = models.JSONField(null=True, blank=True)
    is_valid = models.BooleanField(default=False)


class StatisticsTab(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    match = models.ForeignKey(MatchCrawl, on_delete=models.CASCADE, related_name="statistics")
    extra = models.JSONField(null=True, blank=True)
    crawl_data = models.JSONField(null=True, blank=True)
    is_valid = models.BooleanField(default=False)



class ClubTab(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    match = models.ForeignKey(MatchCrawl, on_delete=models.CASCADE, related_name="clubs")
    extra = models.JSONField(null=True, blank=True)
    crawl_data = models.JSONField(null=True, blank=True)
    is_valid = models.BooleanField(default=False)


class TimeLineTab(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    match = models.ForeignKey(MatchCrawl, on_delete=models.CASCADE, related_name="timelines")
    extra = models.JSONField(null=True, blank=True)
    crawl_data = models.JSONField(null=True, blank=True)
    is_valid = models.BooleanField(default=False)





