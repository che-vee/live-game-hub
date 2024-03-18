"""
URL configuration for app project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from game_hub.views import main, streamer

urlpatterns = [

    path('', main.home, name='home'),
    path("admin/", admin.site.urls),

    path('streamers/', streamer.GetAllStreamersView.as_view(), name='get_streamers'),
    path('streamers/<int:pk>/', streamer.GetStreamerByIDView.as_view(), name='get_streamer_by_id'),
    path('streamers/<int:pk>/edit/', streamer.UpdateStreamerView.as_view(), name='streamer_edit'),
    path('streamers/new/', streamer.CreateStreamerView.as_view(), name='streamer_new'),
    path('streamers/<int:pk>/delete/', streamer.DeleteStreamerView.as_view(), name='delete_streamer_by_id'),
]
