from django.db import models
from django.utils import timezone
from djmoney.models.fields import MoneyField


class Streamer(models.Model):
    username = models.CharField(max_length=255, unique=True)
    email = models.EmailField(unique=True)
    balance = MoneyField(max_digits=18, decimal_places=2, default_currency="USD")

    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)


class Payment(models.Model):
    amount = MoneyField(max_digits=18, decimal_places=2, default_currency="USD")
    source = models.CharField(max_length=255)
    description = models.TextField()
    streamer_id = models.IntegerField()

    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    # Amount
    # Payee
    # Payer
    # Datetime
    # Method
    # Description
    # Status
    # Transaction ID
    # Bill details

class Game(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    gametype_id = models.IntegerField()

    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)


class GameType(models.Model):
    genre = models.CharField(max_length=255)
    price = MoneyField(max_digits=18, decimal_places=2, default_currency="USD")

    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)


class GamePurchase(models.Model):
    amount = MoneyField(max_digits=18, decimal_places=2, default_currency="USD")
    streamer_id = models.IntegerField()
    gametype_id = models.IntegerField()
    payment_id = models.IntegerField()


    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)


class Session(models.Model):
    streamer_id = models.IntegerField()
    game_id = models.IntegerField()

    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
