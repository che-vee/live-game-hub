from mongoengine import (
    Document,
    StringField,
    EmailField,
    FloatField,
    DateTimeField,
    ReferenceField,
    EmbeddedDocumentField,
    EmbeddedDocument,
    BooleanField,
)
from django.utils import timezone


class Viewer(Document):
    username = StringField(required=True)
    email = EmailField(required=True)
    user_agent = StringField()
    cookies = StringField()
    streamer_id = StringField()
    session_id = StringField()
    created_at = DateTimeField(required=True, default=timezone.now)
    updated_at = DateTimeField(default=timezone.now)

class ViewerSnapshot(EmbeddedDocument):
    username = StringField(required=True)
    email = EmailField(required=True)
    user_agent = StringField()
    cookies = StringField()
    streamer_id = StringField()
    session_id = StringField()
    created_at = DateTimeField(required=True, default=timezone.now)
    updated_at = DateTimeField(default=timezone.now)


class PaymentDetails(EmbeddedDocument):
    transaction_id = StringField()
    confirmed = BooleanField(default=False)
    method = StringField()
    confirmation_date = DateTimeField()


class ViewerPurchase(Document):
    viewer_id = ReferenceField(Viewer)
    viewer_snapshot = EmbeddedDocumentField(ViewerSnapshot)
    amount = FloatField(required=True)
    currency = StringField(max_length=3, required=True)
    purchase_date = DateTimeField(required=True)
    payment_details = EmbeddedDocumentField(PaymentDetails)
    game_id = StringField()
    created_at = DateTimeField(required=True, default=timezone.now)
    updated_at = DateTimeField(default=timezone.now)
