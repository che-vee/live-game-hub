from django.test import TestCase, TransactionTestCase
from .models import Streamer, GameType, Payment, GamePurchase
from django.db import transaction
import threading

class PurchaseGameTest(TransactionTestCase):
    def setUp(self):
        self.streamer = Streamer.objects.create(username='test_streamer', email='test@email.com', balance=1000)
        self.game_type = GameType.objects.create(name='Test Game', price=100)

    def test_concurrent_purchases(self):
        payment_details = {'source': 'test', 'description': 'test purchase'}

        def make_purchase():
            try:
                streamer_purchase_game(None, self.streamer.id, self.game_type.id, payment_details)
            except Exception as e:
                pass

        threads = [threading.Thread(target=make_purchase) for _ in range(10)]
        [t.start() for t in threads]
        [t.join() for t in threads]

        self.streamer.refresh_from_db()
        total_payments = Payment.objects.filter(streamer_id=self.streamer.id).count()
        total_purchases = GamePurchase.objects.filter(streamer_id=self.streamer.id).count()

        self.assertEqual(self.streamer.balance, 1000 - self.game_type.price * total_payments)
        self.assertEqual(total_payments, total_purchases)

