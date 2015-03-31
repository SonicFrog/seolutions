from django.db import models
from django.contrib.auth.models import User


class Keyword(models.Model):
    keyword = models.CharField(max_length=200)
    keyword.short_description = "Keyword"

    def __str__(self):
        return self.keyword


class Site(models.Model):
    name = models.CharField(max_length=200)
    url = models.CharField(max_length=1000)
    admins = models.ManyToManyField(User)
    keywords = models.ManyToManyField(Keyword)

    def __str__(self):
        return self.name


class Responsibility(models.Model):
    site = models.ForeignKey(Site)
    site.short_description = "Website"

    person = models.ForeignKey(User)
    person.short_description = "Administrator"

    notify = models.BooleanField(default=True)
    notify.boolean = True
    notify.short_description = "Notify person of reports?"

    def __str__(self):
        return self.person


class KeywordRelation(models.Model):
    site = models.ForeignKey(Site)
    keyword = models.ForeignKey(Keyword)
    active = models.BooleanField(default=True)

    active.boolean = True
    active.short_description = "Scrap for this keyword/site combination"

    def __str__(self):
        return self.keyword


class Report(models.Model):
    date = models.DateTimeField(auto_now=True)
    site = models.ForeignKey(Site)
    keyword = models.ForeignKey(Keyword)
    page = models.IntegerField(default=-1)
    rank = models.IntegerField(default=-1)

    def __str__(self):
        return "Ranking of " + self.site + " on " + self.date


class Campaign(object):
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    site = models.ForeignKey(Site)
    keywords = models.ManyToManyField(Keyword)

    def __str__(self):
        return "Campaign for " + self.site + " for " ", ".join(self.keywords)
