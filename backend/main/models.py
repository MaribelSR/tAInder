from django.db import models

class Tag(models.Model):
    name = models.CharField(max_length=64, unique=True, null=False)

class Profile(models.Model):
    username = models.CharField(max_length=64, unique=True, null=False)
    first_name = models.CharField(max_length=128)
    last_name = models.CharField(max_length=128)
    height = models.IntegerField(min=1, max=300)
    birthday = models.DateField(null=False)
    description = models.TextField(max_length=1024)
    last_access = models.DateTimeField()
    tags = models.ManyToManyField(Tag)

class Ai(models.Model):
    personality = models.TextField()
    schedule = models.TextField()
    last_execution = models.DateTimeField()
    next_execution = models.DateTimeField()

