from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from game_hub.models import Streamer

# transactions here?
class GetAllStreamersView(ListView):
    model = Streamer
    template_name = 'streamers/get_streamers.html'

class GetStreamerByIDView(DetailView):
    model = Streamer
    template_name = 'streamers/get_streamer_by_id.html'

class UpdateStreamerView(UpdateView):
    model = Streamer
    fields = ['username', 'email', 'balance']
    template_name = 'streamers/streamer_form.html'

class CreateStreamerView(CreateView):
    model = Streamer
    fields = ['username', 'email', 'balance']
    template_name = 'streamers/streamer_form.html' # same as update?

class DeleteStreamerView(DeleteView):
    model = Streamer
    template_name = 'streamers/delete_streamer_by_id.html'
    success_url = '/streamers/'
