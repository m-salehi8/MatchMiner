from django.db import models
import uuid

class Source(models.Model):
    STATUS_CHOICES = (
        ("active", "Active"),
        ("running", "Running"),
        ("complete", "Complete"),
        ("failed", "Failed"),
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    uuid = models.UUIDField(default=uuid.uuid4(), unique=True, editable=False)
    name = models.CharField(max_length=100, unique=True)
    base_url = models.URLField()
    extra = models.JSONField(null=True, blank=True)
    status = models.CharField(max_length=128, choices=STATUS_CHOICES, default="active")
    def __str__(self):
        return self.name



class LeagueLinks(models.Model):
    name = models.CharField(max_length=120)
    start_year = models.PositiveIntegerField()
    end_year = models.PositiveIntegerField()
    source = models.ForeignKey(Source, on_delete=models.SET_NULL, null=True, blank=True, related_name="leagues" )
    url = models.URLField(null=True, blank=True)
    def __str__(self):
        return self.name



class LeagueSeasonLinks(models.Model):
    league = models.ForeignKey(LeagueLinks, related_name="season", on_delete=models.CASCADE)
    year = models.PositiveIntegerField()
    match_count = models.PositiveIntegerField()
    url = models.URLField()

    def __str__(self):
        return self.league.name + "   " + str(self.year)



class MatchLinks(models.Model):
    STATUS_CHOICES = (
        ("done", "Done"),
        ("running", "Running"),
        ("field", "Field"),
        ("in_queue", "In Queue")
    )

    url = models.URLField()
    match_id = models.CharField(max_length=200)
    title = models.CharField(max_length=500)
    status = models.CharField(choices=STATUS_CHOICES, max_length=200)
    match_obj = models.ForeignKey("match.MatchData", on_delete=models.SET_NULL, related_name="match_link", null=True, blank=True)
    extra = models.JSONField(null=True, blank=True)
    is_done = models.BooleanField(default=False)
    session = models.ForeignKey(LeagueSeasonLinks, on_delete=models.CASCADE, related_name="matches")


    def __str__(self):
        return self.title + "   " + self.match_id

