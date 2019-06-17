from django.db import models

# Create your models here.

class resultAll(models.Model):

    platform =models.CharField(max_length=20)
    detail = models.CharField(max_length=12800)
    sumery = models.CharField(max_length=1280)
    Jenkinsid = models.IntegerField()

    class Meta:
        db_table = 'resultAll'

class performanceData(models.Model):
    platform = models.CharField(max_length=20)
    startTime = models.CharField(max_length=1280)
    pageTime = models.CharField(max_length=12800)
    fps = models.CharField(max_length=128000)
    cpu = models.CharField(max_length=128000)
    mem = models.CharField(max_length=128000)
    runt = models.CharField(max_length=1280)
    Jenkinsid = models.IntegerField()
    model = models.CharField(max_length=60)
    Appname=models.CharField(max_length=40)
    CodeVersion = models.CharField(max_length=40)
    class Meta:
        db_table = 'performanceData'