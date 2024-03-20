from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from .models import *
from .forms import *
from .transactions import *

def home(request):
    return render(request, 'home.html')


class GetAllStreamersView(ListView):
    model = Streamer
    template_name = 'streamers.html'
    context_object_name = 'streamers'
    queryset = Streamer.objects.order_by('id')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['purchase_form'] = PurchaseGameForm() 
        return context

class GetAllPurchasesView(ListView):
    model = GamePurchase
    template_name = 'purchases.html'
    context_object_name = 'purchases'


def handle_purchase_view(request):
    if request.method == 'POST':
        form = PurchaseGameForm(request.POST)
        if form.is_valid():
            try:
                streamer_id = form.cleaned_data.get('streamer_id')
                gametype_id = form.cleaned_data.get('gametype_id')

                streamer_purchase_game(request, streamer_id, gametype_id)
                messages.success(request, "Game purchased successfully!")
            except ValueError as e:
                messages.error(request, str(e))
            except Exception as e:
                messages.error(request, str(e))
        else:
            for field in form:
                for error in field.errors:
                    messages.error(request, "{}: {}".format(field.label, error))
            for error in form.non_field_errors():
                messages.error(request, error)
    return redirect('streamers')


def update_balance_view(request):
    if request.method == 'POST':
        form = UpdateBalanceForm(request.POST)
        if form.is_valid():
            try:
                streamer_id = form.cleaned_data['streamer_id']
                new_balance = form.cleaned_data['new_balance']
                update_streamer_balance(streamer_id, new_balance)
                messages.success(request, 'Balance updated successfully.')
            except Streamer.DoesNotExist:
                messages.error(request, 'Streamer not found.')
            except Exception as e:
                messages.error(request, str(e))

            return redirect('streamers')
        else:
            messages.error(request, 'Invalid form submission.')

    return redirect('streamers')
