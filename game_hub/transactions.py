from django.shortcuts import render
from django.db import transaction
from .models import *
from djmoney.money import Money

@transaction.atomic
def streamer_purchase_game(request, streamer_id, gametype_id, source='spend of money from balance', description='generated desc'):
    streamer = Streamer.objects.select_for_update().get(pk=streamer_id)
    game_type = GameType.objects.get(pk=gametype_id)
    game_price = game_type.price

    if streamer.balance_amount < game_type.price:
        raise ValueError("Insufficient balance")

    payment = Payment.objects.create(
        amount=game_price,
        source=source,
        description=description,
        streamer_id=streamer_id
    )
    
    GamePurchase.objects.create(
        amount=game_price, 
        streamer_id=streamer_id, 
        gametype_id=gametype_id,
        # payment_id=payment.id
    )

    streamer.balance_amount -= game_price
    streamer.save()

@transaction.atomic
def update_streamer_balance(streamer_id, new_balance):
    streamer = Streamer.objects.select_for_update().get(pk=streamer_id)
    currency = streamer.balance_currency if streamer.balance else 'USD'
    streamer.balance_amount = Money(new_balance, currency)
    streamer.save()


#  -----TODO------
@transaction.atomic
def streamer_host_game(request, streamer_id, game_id):
    session = Session.objects.create(streamer_id=streamer_id, game_id=game_id)

@transaction.atomic
def streamer_create_session(request, streamer_id, game_id):
    session = Session.objects.create(streamer_id=streamer_id, game_id=game_id)

@transaction.atomic
def session_produce_event(request, session_id):
    session = Session.objects.get(pk=session_id)

@transaction.atomic
def viewer_join_session(request, viewer_id, session_id):
    session = Session.objects.get(pk=session_id)

@transaction.atomic
def viewer_play_game(request, viewer_id, game_id):
    game = Game.objects.get(pk=game_id)
