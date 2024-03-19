from django.shortcuts import render
from django.db import transaction
from .models import Streamer, Game, GameType, GamePurchase, Session
from djmoney.money import Money

def purchase_game(request, streamer_id, gametype_id):
    with transaction.atomic():
        streamer = Streamer.objects.select_for_update().get(pk=streamer_id)
        game_type = GameType.objects.get(pk=gametype_id)
        streamer.balance -= game_type.price
        streamer.save()
        GamePurchase.objects.create(amount=game_type.price, streamer_id=streamer_id, gametype_id=gametype_id)
        # You'd typically have a payment processing step here
    return render(request, 'purchase_game.html', {})










