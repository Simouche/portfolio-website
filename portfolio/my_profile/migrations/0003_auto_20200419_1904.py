# Generated by Django 3.0.2 on 2020-04-19 18:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('my_profile', '0002_emailmessage'),
    ]

    operations = [
        migrations.AddField(
            model_name='workexperience',
            name='company_link',
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='workexperience',
            name='project_link',
            field=models.URLField(blank=True, null=True),
        ),
    ]
