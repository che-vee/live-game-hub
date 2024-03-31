from mongoengine import (
    Document,
    IntField,
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


class GameType(EmbeddedDocument):
    genre = StringField(max_length=255, required=True)
    price = FloatField(required=True)
    created_at = DateTimeField(default=timezone.now)
    updated_at = DateTimeField(default=timezone.now)

class Game(EmbeddedDocument):
    name = StringField(max_length=255, required=True)
    description = StringField()
    gametype = EmbeddedDocumentField(GameType, required=True)
    created_at = DateTimeField(default=timezone.now)
    updated_at = DateTimeField(default=timezone.now)

class Session(Document):
    streamer_id = IntField(required=True)
    game = EmbeddedDocumentField(Game, required=True)
    duration = IntField() 
    score = IntField()
    status = StringField(max_length=20)
    game_mode = StringField(max_length=20)
    platform = StringField(max_length=20)
    session_events = StringField()
    session_metadata = StringField()
    start_time = DateTimeField(default=timezone.now)
    end_time = DateTimeField(default=timezone.now)

    def __str__(self):
        return (f"Session(streamer_id={self.streamer_id}, game={self.game}, duration={self.duration}, "
                f"score={self.score}, status={self.status}, game_mode={self.game_mode}, platform={self.platform}, "
                f"session_events={self.session_events}, session_metadata={self.session_metadata}, "
                f"start_time={self.start_time}, end_time={self.end_time})")
