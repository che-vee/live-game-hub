from django.shortcuts import render
from django.db import transaction
from .models import Streamer, Game, GameType, GamePurchase, Session
from djmoney.money import Money

def host_game(request, streamer_id, game_id):
    with transaction.atomic():
        # Assuming the same logic as create session for demo purpose
        session = Session.objects.create(streamer_id=streamer_id, game_id=game_id)
    return render(request, 'host_game.html', {'session': session})