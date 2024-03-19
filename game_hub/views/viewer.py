from django.shortcuts import render
from django.db import transaction
from .models import Streamer, Game, GameType, GamePurchase, Session
from djmoney.money import Money

def viewer_join_session(request, viewer_id, session_id):
    with transaction.atomic():
        # Placeholder for the logic for a viewer to join a session
        session = Session.objects.get(pk=session_id)
        # Logic for viewer joining the session goes here
    return render(request, 'join_session.html', {'session': session})

def viewer_play_game(request, viewer_id, game_id):
    with transaction.atomic():
        # Placeholder for the logic for a viewer to play a game
        game = Game.objects.get(pk=game_id)
        # Logic for viewer playing the game goes here
    return render(request, 'play_game.html', {'game': game})