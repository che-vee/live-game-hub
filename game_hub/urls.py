from django.urls import path

from .views import main, streamer

urlpatterns = [
    path("", main.home, name="index"),

    path('streamers/', streamer.GetAllStreamersView.as_view(), name='get_streamers'),
    path('streamers/<int:pk>/', streamer.GetStreamerByIDView.as_view(), name='streamer_detail'),
    path('streamers/<int:pk>/edit/', streamer.UpdateStreamerView.as_view(), name='streamer_update'),
    path('streamers/new/', streamer.CreateStreamerView.as_view(), name='streamer_create'),
    path('streamers/<int:pk>/delete/', streamer.DeleteStreamerView.as_view(), name='streamer_delete'),
]