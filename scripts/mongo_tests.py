from game_hub.mongo_models import Viewer, ViewerPurchase, ViewerSnapshot, PaymentDetails
import datetime
import time
import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "app.settings")
django.setup()


def get_or_create_viewer(username, email):
    viewer = Viewer.objects(username=username).first()
    if not viewer:
        viewer = Viewer(
            username=username,
            email=email,
            user_agent="Mozilla/5.0",
            cookies="session_id=abc123; csrftoken=def456",
            streamer_id="streamer123",
            session_id="session123",
            created_at=datetime.datetime.now(),
            updated_at=datetime.datetime.now(),
        )
        viewer.save()
    return viewer


def insert_purchases(num_purchases, viewer_username):
    viewer = get_or_create_viewer(viewer_username, f"{viewer_username}@example.com")
    viewer_snapshot = ViewerSnapshot(
        username=viewer.username,
        email=viewer.email,
        user_agent=viewer.user_agent,
        cookies=viewer.cookies,
        streamer_id=viewer.streamer_id,
        session_id=viewer.session_id,
        created_at=viewer.created_at,
        updated_at=viewer.updated_at,
    )

    payment_details = PaymentDetails(
        transaction_id="txn_123456789",
        confirmed=True,
        method="Credit Card",
        confirmation_date=datetime.datetime.now(),
    )

    purchases = [
        ViewerPurchase(
            viewer_id=viewer,
            viewer_snapshot=viewer_snapshot,
            amount=29.99,
            currency="USD",
            purchase_date=datetime.datetime.now(),
            payment_details=payment_details,
            game_id="game123",
            created_at=datetime.datetime.now(),
            updated_at=datetime.datetime.now(),
        )
        for _ in range(num_purchases)
    ]

    start_time = time.time()
    ViewerPurchase.objects.insert(purchases, load_bulk=False)
    end_time = time.time()

    print(
        f'Inserted {num_purchases} purchases for "{viewer_username}" in {end_time - start_time} seconds at rate of {num_purchases/(end_time - start_time)} purchases per second.'
    )


def update_purchases(viewer_username, new_amount):
    start_time = time.time()

    viewer = Viewer.objects(username=viewer_username).first()

    if viewer:
        update_count = ViewerPurchase.objects(viewer_id=viewer).update(
            set__amount=new_amount, set__updated_at=datetime.datetime.now()
        )
        end_time = time.time()
        print(
            f'Updated purchases for "{viewer_username}" in {end_time - start_time} seconds at rate of {update_count/(end_time - start_time)} updates per second.'
        )
    else:
        end_time = time.time()
        print(f'No viewer found with username "{viewer_username}".')


num_purchases = 10000
username = "test_user_5"

insert_purchases(num_purchases, username)
update_purchases(username, new_amount=49.99)
