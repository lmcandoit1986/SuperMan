# Generated by Django 2.2.2 on 2020-04-07 03:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Server', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='uicasedetail',
            name='Jenkinsid',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='uicasedetail',
            name='platform',
            field=models.CharField(default=1, max_length=100),
            preserve_default=False,
        ),
    ]
