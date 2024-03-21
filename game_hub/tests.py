from django.test import TransactionTestCase
from .models import Streamer, GameType, Payment, GamePurchase
from djmoney.money import Money
from .transactions import streamer_purchase_game
from django.db import transaction

import threading


class PurchaseGameTest(TransactionTestCase):
    def setUp(self):
        self.streamer = Streamer.objects.create(
            username="test_streamer", email="test@email.com", balance=1000
        )
        self.game_type = GameType.objects.create(
            genre="Test Game", price=Money(100, "USD")
        )

    def test_concurrent_purchases(self):
        payment_details = {"source": "test", "description": "test purchase"}

        def make_purchase():
            try:
                print(f"Attempting to purchase for streamer {self.streamer.id}")
                streamer_purchase_game(
                    None, self.streamer.id, self.game_type.id, **payment_details
                )
                print("Purchase successful")
            except Exception as e:
                print(f"Purchase failed: {e}")

        threads = [threading.Thread(target=make_purchase) for _ in range(10)]
        [t.start() for t in threads]
        print("All purchase threads started")
        [t.join() for t in threads]
        print("All purchase threads completed")

        self.streamer.refresh_from_db()
        total_payments = Payment.objects.filter(streamer_id=self.streamer.id).count()
        total_purchases = GamePurchase.objects.filter(
            streamer_id=self.streamer.id
        ).count()

        print(f"Total payments: {total_payments}")
        print(f"Total purchases: {total_purchases}")

        expected_balance = Money(1000, "USD") - (self.game_type.price * total_payments)
        print(
            f"Expected balance: {expected_balance}, Actual balance: {Money(self.streamer.balance, self.streamer.balance_currency)}"
        )

        self.assertEqual(
            Money(self.streamer.balance, self.streamer.balance_currency),
            expected_balance,
        )
        self.assertEqual(total_payments, total_purchases)


class IsolationTest(TransactionTestCase):
    def setUp(self):
        self.streamer = Streamer.objects.create(
            username="test_streamer", email="test@email.com", balance=100
        )
        self.game_type = GameType.objects.create(
            genre="Test Game", price=Money(100, "USD")
        )
        print(
            f"Created streamer with ID {self.streamer.id} and initial balance {self.streamer.balance}"
        )
        print(
            f"Created game type with ID {self.game_type.id} and price {self.game_type.price}"
        )

    def test_concurrent_purchases_isolation(self):
        payment_details = {"source": "test", "description": "test purchase"}

        def make_purchase():
            try:
                print(f"Attempting to purchase for streamer {self.streamer.id}")
                streamer_purchase_game(
                    None, self.streamer.id, self.game_type.id, **payment_details
                )
                print("Purchase successful")
            except Exception as e:
                print(f"Purchase failed: {e}")

        threads = [threading.Thread(target=make_purchase) for _ in range(2)]

        [thread.start() for thread in threads]
        print("All purchase threads started")
        [thread.join() for thread in threads]
        print("All purchase threads completed")

        self.streamer.refresh_from_db()
        purchases_count = GamePurchase.objects.filter(
            streamer_id=self.streamer.id
        ).count()
        payments_count = Payment.objects.filter(streamer_id=self.streamer.id).count()

        print(f"Total purchases made: {purchases_count}")
        print(f"Total payments made: {payments_count}")
        print(f"Final streamer balance: {self.streamer.balance}")


class ReadCommittedTest(TransactionTestCase):
    def setUp(self):
        self.streamer = Streamer.objects.create(
            username="test_streamer", email="test@email.com", balance=100
        )
        self.game_type = GameType.objects.create(
            genre="Test Game", price=Money(100, "USD")
        )
        print(
            f"Created streamer with ID {self.streamer.id} and initial balance {self.streamer.balance}"
        )
        print(
            f"Created game type with ID {self.game_type.id} and price {self.game_type.price}"
        )

    def test_read_committed_concurrency(self):
        def make_purchase():
            with transaction.atomic():
                try:
                    streamer = Streamer.objects.get(id=self.streamer.id)
                    print(
                        f"Thread {threading.current_thread().name}: Streamer balance before purchase is {streamer.balance}"
                    )

                    if (
                        Money(streamer.balance, self.streamer.balance_currency)
                        >= self.game_type.price
                    ):
                        import time

                        time.sleep(0.5)
                        streamer.balance = (
                            Money(streamer.balance, self.streamer.balance_currency)
                            - self.game_type.price
                        )
                        streamer.balance = streamer.balance.amount
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

        threads = [threading.Thread(target=make_purchase) for _ in range(2)]

        [thread.start() for thread in threads]
        print("All purchase threads started")
        [thread.join() for thread in threads]
        print("All purchase threads completed")

        self.streamer.refresh_from_db()
        print(f"Final streamer balance: {self.streamer.balance}")
