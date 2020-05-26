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

class UICaseDetail(models.Model):
    model = models.CharField(max_length=100)
    case = models.CharField(max_length=100)
    caseName = models.CharField(max_length=200)
    result = models.IntegerField()
    useTime =models.CharField(max_length=100)
    comment =models.CharField(max_length=1000)
    all = models.CharField(max_length=128000)
    pic = models.CharField(max_length=1000)
    listid = models.IntegerField()
    Jenkinsid = models.IntegerField()
    platform = models.CharField(max_length=100)
    reason = models.IntegerField()
    class Meta:
        db_table = 'UICaseDetail'

class listAPIMointor(models.Model):
    rt = models.CharField(max_length=100)
    all = models.IntegerField()
    fail = models.IntegerField()
    only = models.IntegerField()
    class Meta:
        db_table = 'listAPIMointor'

class uiAutoRunListN(models.Model):
    platform = models.CharField(max_length=100)
    allNum = models.IntegerField()
    failNum = models.IntegerField()
    rt = models.CharField(max_length=100)
    Jenkinsid = models.IntegerField()
    link = models.CharField(max_length=200)
    appName = models.CharField(max_length=100)
    model = models.CharField(max_length=200)
    device = models.CharField(max_length=100)
    ut = models.CharField(max_length=100)
    appVersion = models.CharField(max_length=100)
    class Meta:
        db_table = 'uiAutoRunListN'

class mockData(models.Model):
    api = models.CharField(max_length=100)
    keyword = models.CharField(max_length=100)
    data = models.CharField(max_length=2000)
    status = models.IntegerField()
    class Meta:
        db_table = 'mockData'

class failReason(models.Model):
    reason = models.CharField(max_length=100)
    class Meta:
        db_table = 'failReason'

class Imgdb(models.Model):
    img_url = models.ImageField(upload_to='img')
    class Meta:
        db_table = 'Imgdb'

class APIrunlist(models.Model):
    Jenkinsid = models.IntegerField()
    allNum = models.IntegerField()
    failNum = models.IntegerField()
    rt = models.CharField(max_length=100)
    ut = models.CharField(max_length=100)
    type = models.IntegerField()
    kind = models.CharField(max_length=200)
    class Meta:
        db_table = 'APIrunlist'

class apiCases(models.Model):
    model = models.CharField(max_length=100)
    api = models.CharField(max_length=100)
    case = models.CharField(max_length=100)
    title = models.CharField(max_length=200)
    result = models.IntegerField()
    useTime = models.CharField(max_length=100)
    comment = models.CharField(max_length=1000)
    Jenkinsid = models.IntegerField()
    class Meta:
        db_table = 'apiCases'