import os
import django
import threading
import time
from django.db import transaction
from moneyed import Money
from django.db.models import F

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "app.settings")
django.setup()

from game_hub.models import Streamer, GameType, Payment, GamePurchase


def make_purchase(streamer_id, game_type_id, balance_currency="USD"):
    with transaction.atomic():
        try:
            streamer = Streamer.objects.select_for_update().get(id=streamer_id)
            game_type = GameType.objects.get(id=game_type_id)
            print(
                f"Thread {threading.current_thread().name}: Streamer {streamer.id} balance before purchase is {streamer.balance}"
            )

            if Money(streamer.balance, balance_currency) >= game_type.price:
                Payment.objects.create(
                    amount=game_type.price,
                    source="test",
                    description="test",
                    streamer_id=streamer_id,
                )

                time.sleep(5)

                GamePurchase.objects.create(
                    amount=game_type.price,
                    streamer_id=streamer_id,
                    gametype_id=game_type_id,
                )

                streamer.balance = F("balance") - game_type.price.amount
                streamer.save()
                print(
                    f"Thread {threading.current_thread().name}: Purchase successful, new balance is {streamer.balance}"
                )
            else:
                print(
                    f"Thread {threading.current_thread().name}: Insufficient funds for purchase"
                )
        except Exception as e:
            print(f"Purchase failed: {e}")


def run_concurrency_test():
    streamer = Streamer.objects.create(
        username="test_script_17", email="script_17@test.com", balance=100
    )
    game_type = GameType.objects.create(
        genre="Script Test Game", price=Money(100, "USD")
    )

    threads = [
        threading.Thread(target=make_purchase, args=(streamer.id, game_type.id))
        for _ in range(2)
    ]
    [thread.start() for thread in threads]
    print("All purchase threads started")
    [thread.join() for thread in threads]
    print("All purchase threads completed")

    payments = Payment.objects.filter(streamer_id=streamer.id)
    for payment in payments:
        print(
            f"Payment logged: Streamer {payment.streamer_id}, Amount {payment.amount}, Timestamp {payment.created_at}"
        )

    streamer.refresh_from_db()
    print(f"Final streamer balance: {streamer.balance}")


if __name__ == "__main__":
    run_concurrency_test()
