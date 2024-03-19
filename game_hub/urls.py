from django.urls import path
from .views import * 

urlpatterns = [
    path("", home, name="index"),

    path('streamers/', GetAllStreamersView.as_view(), name='streamers'),
    path('purchases/', GetAllPurchasesView.as_view(), name='purchases'),
    path('update_balance/', update_balance_view, name='update_balance'),
    path('handle_purchase/', handle_purchase_view, name='handle_purchase'),
]