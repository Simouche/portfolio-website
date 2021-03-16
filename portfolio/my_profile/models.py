import os

from django.db import models

from my_profile.backend import generate_user_code
from portfolio.settings import MEDIA_ROOT, MEDIA_URL


class MyProfile(models.Model):
    fullname = models.CharField(max_length=100)
    birth_date = models.DateField()
    email = models.EmailField()
    phone = models.CharField(max_length=15)  # todo remember to add validator
    profile_description = models.TextField()
    skills_description = models.TextField()
    about_intro = models.TextField()

    def __str__(self):
        return self.fullname


class Links(models.Model):
    social_media = models.CharField(max_length=20, null=False, blank=False)
    link = models.CharField(max_length=255, null=False, blank=False, unique=True)
    owner = models.ForeignKey(MyProfile, on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.social_media


class Stack(models.Model):
    name = models.CharField(max_length=30)
    what_can_do_with = models.CharField(max_length=255)
    owner = models.ForeignKey(MyProfile, on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.name


class WorkExperience(models.Model):
    job_title = models.CharField(max_length=50)
    start = models.DateField()
    end = models.DateField(null=True, blank=True)
    company_name = models.CharField(max_length=100)
    description = models.TextField()
    owner = models.ForeignKey(MyProfile, on_delete=models.DO_NOTHING)
    company_link = models.URLField(null=True, blank=True)
    project_link = models.URLField(null=True, blank=True)

    def __str__(self):
        return self.job_title + " at " + self.company_name


class Education(models.Model):
    diploma_title = models.CharField(max_length=100)
    start = models.DateField()
    end = models.DateField()
    school_name = models.CharField(max_length=100)
    description = models.TextField()
    owner = models.ForeignKey(MyProfile, on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.diploma_title


class Application(models.Model):
    name = models.CharField(max_length=50)
    type = models.CharField(max_length=20)
    description = models.TextField()
    carousel = models.CharField(max_length=255, null=True, blank=True)
    owner = models.ForeignKey(MyProfile, on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.name

    @property
    def images(self):
        names = os.listdir(self.carousel)
        urls = []
        for name in names:
            urls.append(MEDIA_URL + self.name + "/" + name)
        return urls

    def save(self, *args, **kwargs):
        super(Application, self).save(*args, **kwargs)
        if not self.carousel:
            path = os.path.join(MEDIA_ROOT, self.name)
            os.mkdir(path)
            self.carousel = path
            super(Application, self).save(*args, **kwargs)


class Service(models.Model):
    service_name = models.CharField(max_length=100)
    service_description = models.CharField(max_length=512)
    owner = models.ForeignKey(MyProfile, on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.service_name


class Visitors(models.Model):
    code = models.CharField(max_length=128, default=generate_user_code)
    count = models.IntegerField(default=0)

    def __str__(self):
        return "{} visited: {}".format(self.code, self.count)


class IpAddress(models.Model):
    visitor = models.ForeignKey(Visitors, on_delete=models.DO_NOTHING)
    address = models.CharField(max_length=255)
    date = models.DateField(auto_now_add=True, editable=False)
    time = models.TimeField(auto_now_add=True, editable=False)

    def __str__(self):
        return "visitor: {} address: {} on: {} at: {}".format(self.visitor.code, self.address, self.date, self.time)


class EmailMessage(models.Model):
    name = models.CharField(max_length=255, blank=False)
    email = models.EmailField(blank=False)
    subject = models.CharField(max_length=150, blank=False)
    message = models.TextField()

    def __str__(self):
        return "Name: {} Email: {} Subject: {}".format(self.name, self.email, self.subject)
