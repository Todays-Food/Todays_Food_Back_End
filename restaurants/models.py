from django.db import models
from django.conf import settings


class Naver(models.Model):
    title = models.CharField(max_length=100)
    link = models.URLField()
    category = models.CharField(max_length=100)
    address = models.CharField(max_length=150)
    roadAddress = models.CharField(max_length=200)
    mapx = models.IntegerField()
    mapy = models.IntegerField()  


class Weather_api(models.Model):
    location = models.TextField()
    weather_summary = models.TextField()
    now_temp = models.TextField()
    dust = models.TextField()
    little_dust = models.TextField()    
