from django.db import models
from django.utils import timezone
from djmoney.models.fields import MoneyField


class Streamer(models.Model):
    username = models.CharField(max_length=255, unique=True)
    email = models.EmailField(unique=True)
    balance = models.DecimalField(max_digits=18, decimal_places=2)
    balance_currency = models.CharField(max_length=3, default="USD")
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def balance_amount(self):
        from djmoney.money import Money
        return Money(self.balance, self.balance_currency)

    @balance_amount.setter
    def balance_amount(self, value):
        self.balance = value.amount
        self.balance_currency = value.currency

class Payment(models.Model):
    amount = MoneyField(max_digits=18, decimal_places=2, default_currency="USD")
    source = models.CharField(max_length=255)
    description = models.TextField()
    streamer_id = models.IntegerField()
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)


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
    # payment_id = models.IntegerField()
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)


class Session(models.Model):
    streamer_id = models.IntegerField()
    game_id = models.IntegerField()
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
