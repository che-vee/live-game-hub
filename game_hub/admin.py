from django.contrib import admin
from .models import Streamer, Payment, Game, GameType, GamePurchase, Session

admin.site.register(Streamer)
admin.site.register(Payment)
admin.site.register(Game)
admin.site.register(GameType)
admin.site.register(GamePurchase)
admin.site.register(Session)
