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

class CaseDetail(models.Model):
    model = models.CharField(max_length=100)
    api = models.CharField(max_length=100)
    charger = models.CharField(max_length=100)
    caseName = models.CharField(max_length=200)
    result = models.IntegerField()
    useTime =models.CharField(max_length=100)
    comment =models.CharField(max_length=1000)
    all = models.CharField(max_length=128000)
    only = models.IntegerField()
    class Meta:
        db_table = 'CaseDetail'

class listAPIMointor(models.Model):
    rt = models.CharField(max_length=100)
    all = models.IntegerField()
    fail = models.IntegerField()
    only = models.IntegerField()
    class Meta:
        db_table = 'listAPIMointor'