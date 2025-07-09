from django.db import models


class Tag(models.Model):
    name = models.CharField(max_length=64, unique=True, null=False)


class Profile(models.Model):
    username = models.CharField(max_length=150, unique=True, null=False)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    height = models.IntegerField()
    birthday = models.DateField(null=False)
    description = models.TextField(max_length=1024)
    last_access = models.DateTimeField()
    tags = models.ManyToManyField(Tag)


class User(models.Model):
    email = models.EmailField(max_length=254, unique=True, null=False)
    password = models.CharField(max_length=128, null=False)
    profile = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True)


class Ai(models.Model):
    personality = models.TextField()
    schedule = models.TextField()
    last_execution = models.DateTimeField()
    next_execution = models.DateTimeField()
    profile = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True)


class Match(models.Model):
    profile_a = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
        null=False,
        related_name="matches_as_profile_a",
    )
    profile_b = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
        null=False,
        related_name="matches_as_profile_b",
    )
    do_match_a_b = models.BooleanField()
    do_match_b_a = models.BooleanField()


class Message(models.Model):
    msg = models.TextField()
    published = models.DateTimeField()
    deleted = models.BooleanField()
    replied_message = models.ForeignKey("self", on_delete=models.SET_NULL, null=True)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, null=False)
    match = models.ForeignKey(Match, on_delete=models.CASCADE, null=False)
