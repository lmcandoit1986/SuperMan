# Generated by Django 2.2.2 on 2020-04-10 02:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Server', '0005_failreason'),
    ]

    operations = [
        migrations.AddField(
            model_name='uicasedetail',
            name='reason',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]
