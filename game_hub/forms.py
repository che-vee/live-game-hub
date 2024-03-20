from django import forms

class PurchaseGameForm(forms.Form):
    streamer_id = forms.IntegerField(label='Streamer ID')
    gametype_id = forms.IntegerField(label='Game Type ID')

class UpdateBalanceForm(forms.Form):
    streamer_id = forms.IntegerField(widget=forms.HiddenInput())
    new_balance = forms.DecimalField(max_digits=18, decimal_places=2, label='New Balance')
