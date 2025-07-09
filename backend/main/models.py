from django.db import models


class Tag(models.Model):
    name = models.CharField(max_length=64, unique=True, null=False)


class Profile(models.Model):
    username = models.CharField(max_length=150, unique=True, null=False)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    height = models.IntegerField(min=1, max=300)
    birthday = models.DateField(null=False)
    description = models.TextField(max_length=1024)
    last_access = models.DateTimeField()
    tags = models.ManyToManyField(Tag)


class User(models.Model):
    email = models.EmailField(max_length=254, unique=True, null=False)
    password = models.CharField(max_length=128, null=False)
    profile = models.ForeignKey(Profile)


class Ai(models.Model):
    personality = models.TextField()
    schedule = models.TextField()
    last_execution = models.DateTimeField()
    next_execution = models.DateTimeField()
    profile = models.ForeignKey(Profile)


class Match(models.Model):
    profile_a = models.ForeignKey(Profile)
    profile_b = models.ForeignKey(Profile)
    do_match_a_b = models.BooleanField()
    do_match_b_a = models.BooleanField()


class Message(models.Model):
    message = models.TextField()
    published = models.DateTimeField()
    deleted = models.BooleanField()
    replied_message = models.ForeignKey("self")
    profile = models.ForeignKey(Profile)
    match = models.ForeignKey(Match, null=False)
