from django.shortcuts import render
from django.db import transaction
from .models import Streamer, Game, GameType, GamePurchase, Session
from djmoney.money import Money

def create_session(request, streamer_id, game_id):
    with transaction.atomic():
        session = Session.objects.create(streamer_id=streamer_id, game_id=game_id)
    return render(request, 'create_session.html', {'session': session})

def session_produce_event(request, session_id):
    with transaction.atomic():
        # Placeholder for the logic to produce an event
        session = Session.objects.get(pk=session_id)
        # Event creation logic goes here
    return render(request, 'session_event.html', {'session': session})
