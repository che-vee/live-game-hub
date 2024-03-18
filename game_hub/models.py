from django.db import models

class Streamer(models.Model):
    username = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    balance = models.DecimalField(max_digits=10, decimal_places=2)

class Game(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()

class GameType(models.Model):
    genre = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    game_id = models.IntegerField()

class GamePurchase(models.Model):
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    user_id = models.IntegerField()
    game_type_id = models.IntegerField()

class Session(models.Model):
    user_id = models.IntegerField()
    game_id = models.IntegerField()
