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

class User(models.Model):
    email = models.CharField(max_length=200, unique=True, null=False)
    password = models.CharField(max_length=20, null=False)
    profile_id = models.IntegerField()

class Ai(models.Model):
    personality = models.TextField()
    schedule = models.TextField()
    last_execution = models.DateTimeField()
    next_execution = models.DateTimeField()
    profile_id = models.IntegerField()
class Match(models.Model):
    #FK tendría que añadir algo :/ dudillas.
    profile_id_a = models.IntegerField()
    profile_id_b = models.IntegerField()
    do_match_a_b = models.BooleanField()
    do_match_b_a = models.BooleanField()

class Message(models.Model):
    message = models.TextField()
    #Tengo dudas en ambas tanto la de arriba por no limitarlo en char aunque es
    #un mensaje al final y podria ser char. Y luego, la de abajo por lo del tipo
    #que hemos puesto int pero no se yo. 
    type = models.IntegerField()
    published = models.DateTimeField()
    deleted = models.BooleanField()
    replied_message_id = models.IntegerField()
    profile_id = models.IntegerField()
    #debo de añadir aquí también que no sea null o a ser FK ya está todo eso donde corresponde?
    match_id = models.IntegerField()

