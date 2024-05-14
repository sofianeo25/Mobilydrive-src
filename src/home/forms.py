# forms.py
from django import forms
from .models import Devis


class ItineraireForm(forms.Form):
    depart = forms.CharField(label='Départ', max_length=100)
    arrivee = forms.CharField(label='Arrivée', max_length=100)


# formulaire dans Contact

class ContactForm(forms.Form):
    first_name = forms.CharField(label='Prénom', max_length=100, required=True,
                                 widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Prénom'}))
    last_name = forms.CharField(label='Nom', max_length=100, required=True,
                                widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nom'}))
    phone = forms.CharField(label='Numéro de téléphone', max_length=15, required=True, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Numéro de téléphone'}))
    email = forms.EmailField(label='E-mail', required=True, widget=forms.EmailInput(
        attrs={'class': 'form-control', 'placeholder': 'Entrez votre e-mail'}))


# formulaire dans home

class ContactUsForm(forms.Form):
    first_name = forms.CharField(label='Prénom', max_length=100,
                                 widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Votre prénom'}))
    last_name = forms.CharField(label='Nom', max_length=100,
                                widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Votre nom'}))
    phone = forms.CharField(label='Numéro de téléphone', max_length=15, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Votre numéro de téléphone'}))
    message = forms.CharField(label='Votre message', widget=forms.Textarea(
        attrs={'class': 'form-control', 'placeholder': 'Tapez votre message ici', 'rows': 4}))
    request_type = forms.ChoiceField(choices=[
            ('Transfert de véhicule', 'Transfert de véhicule'),
            ('Conciergerie', 'Conciergerie'),
            ('Service VTC', 'Service VTC'),
            ('Location de voiture', 'Location de voiture'),
            ('Autre', 'Autre')
        ])