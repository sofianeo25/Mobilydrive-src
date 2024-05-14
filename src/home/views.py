import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import requests
from django.conf import settings
from django.core.mail import send_mail
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template.defaultfilters import floatformat

from .forms import ItineraireForm, ContactUsForm, ContactForm
from .utils import get_route


def home(request):
    return render(request, 'home.html', {})


def calculer_consommation_carburant(distance_km):
    # Formule arbitraire pour calculer la consommation de carburant en litres
    consommation_litres = distance_km * 0.07
    return consommation_litres


def calculer_prix(distance_km):
    # Formule arbitraire pour calculer le prix en euros
    if distance_km >= 600:
        prix = distance_km * 0.8
    elif 500 <= distance_km < 600:
        prix = distance_km * 0.9
    elif 350 <= distance_km < 500:
        prix = distance_km * 1.1
    else:
        prix = distance_km * 1.2
    return prix


def map_view(request):
    if request.method == 'POST':
        form = ItineraireForm(request.POST)
        if form.is_valid():
            depart = form.cleaned_data['depart']
            arrivee = form.cleaned_data['arrivee']

            # Utilisez l'API OpenRouteService pour obtenir les données d'itinéraire
            api_key = "5b3ce3597851110001cf624863339ce406db475da2a32b7797543249"
            departure = [2.3522,
                         48.8566]  # Vous pouvez remplacer ces coordonnées par celles récupérées via le formulaire si
            # besoin
            destination = [5.3698, 43.2965]  # Idem pour la destination
            route_data = get_route(departure, destination, api_key)

            return render(request, 'map.html', {'form': form, 'routeData': route_data})

    else:
        form = ItineraireForm()

    return render(request, 'map.html', {'form': form})


def calcul_itineraire(request):
    cout = None  # Initialisation de la variable coût
    if request.method == 'POST':
        form = ItineraireForm(request.POST)
        if form.is_valid():
            depart = form.cleaned_data['depart']
            arrivee = form.cleaned_data['arrivee']
            request.session['depart'] = depart  # Stockage de 'depart' dans la session
            request.session['arrivee'] = arrivee  # Stockage de 'arrivee' dans la session

            url = f'http://www.mapquestapi.com/directions/v2/route?key={settings.MAPQUEST_API_KEY}&from={depart}&to={arrivee}'
            response = requests.get(url).json()

            distance_miles = response['route']['distance']
            distance_km = round(distance_miles * 1.60934, 2)  # Convertir les miles en kilomètres
            cout = calculer_prix(distance_km)

            # Calculer la consommation de carburant et le prix avec les coordonnées géographiques
            point_depart = (
                response['route']['locations'][0]['latLng']['lat'], response['route']['locations'][0]['latLng']['lng'])
            point_arrivee = (
                response['route']['locations'][1]['latLng']['lat'], response['route']['locations'][1]['latLng']['lng'])
            consommation_litres = calculer_consommation_carburant(distance_km)
            prix = calculer_prix(distance_km)
            request.session['prix'] = prix
            return render(request, 'itineraire.html',
                          {'form': form, 'distance': distance_km, 'cout': cout, 'consommation': consommation_litres,
                           'prix': prix})

    else:
        form = ItineraireForm()
    return render(request, 'itineraire.html', {'form': form})


def contact(request):
    if request.method == 'POST':
        # Récupération des données du formulaire
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        phone = request.POST.get('phone')
        message = request.POST.get('message')

        # Construction du message e-mail
        email_content = f"""
        Prénom: {first_name}
        Nom: {last_name}
        Numéro de téléphone: {phone}
        Message: {message}
        """

        # Paramètres de connexion au serveur SMTP
        smtp_server = 'smtp.example.com'  # Remplacez-le par votre serveur SMTP
        smtp_port = 587  # Port SMTP (habituellement 587 pour TLS)
        smtp_username = 'your_smtp_username'
        smtp_password = 'your_smtp_password'

        # Connexion au serveur SMTP
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(smtp_username, smtp_password)

        # Construction du message e-mail
        msg = MIMEMultipart()
        msg['From'] = 'your_email@example.com'
        msg['To'] = 'contact@sftech.fr'
        msg['Subject'] = 'Nouveau message de formulaire de contact'
        msg.attach(MIMEText(email_content, 'plain'))

        # Envoi de l'e-mail
        server.send_message(msg)

        # Fermeture de la connexion SMTP
        server.quit()

        # Redirection ou affichage d'un message de succès
        return HttpResponse('Votre message a été envoyé avec succès!')
    else:
        # Si la requête n'est pas de type POST, retourner à la page de contact
        return render(request, 'contact.html')


def contact_view(request):
    # Récupération des données de départ et d'arrivée depuis la session
    depart = request.session.get('depart')
    arrivee = request.session.get('arrivee')
    prix = request.session.get('prix')
    prix = round(prix, 2)

    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        phone = request.POST.get('phone')
        email = request.POST.get('email')

        if first_name and last_name and phone and email:
            name = f"{first_name} {last_name}"
            subject = f"Le prospect {name} est intéressé pour un trajet"
            recipient_email = 'sofiane.ouardi25200@gmail.com'
            body = (
                f"Voici ses coordonnées :\n"
                f"Nom: {last_name}\n"
                f"Prénom: {first_name}\n"
                f"Téléphone: {phone}\n"
                f"Email: {email}\n"
                f"Départ: {depart}\n"
                f"Arrivée: {arrivee}\n"
                f"Pour un devis à un prix de : {prix} €\n"
            )

            send_mail(subject, body, settings.EMAIL_HOST_USER, [recipient_email], fail_silently=False)
            return redirect('success_url')
        else:
            return HttpResponse("Merci de remplir tous les champs du formulaire.", status=400)

    return render(request, 'itineraire.html', {})


def success_view(request):
    # Le template 'success.html' contiendra le message de confirmation
    return render(request, 'success.html')


def contact_us_view(request):
    if request.method == 'POST':
        form = ContactUsForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            phone = form.cleaned_data['phone']
            message = form.cleaned_data['message']
            request_type = form.cleaned_data['request_type']

            # Assurez-vous que tous les champs requis sont remplis
            if first_name and last_name and phone and message and request_type:
                name = f"{first_name} {last_name}"
                subject = f"Demande de {name} - {request_type}"
                recipient_email = 'sofiane.ouardi25200@gmail.com'  # L'adresse email du destinataire (à configurer)
                body = (
                    f"Voici sa demande :\n"
                    f"Nom: {last_name}\n"
                    f"Prénom: {first_name}\n"
                    f"Téléphone: {phone}\n"
                    f"Demande: {request_type}\n"
                    f"Message: {message}\n"
                )

                send_mail(
                    subject,
                    body,
                    settings.EMAIL_HOST_USER,
                    [recipient_email],  # Utilisez une liste pour ajouter d'autres destinataires si nécessaire
                    fail_silently=False,
                )
                return redirect('success_url')  # Redirigez vers une URL de succès après l'envoi
            else:
                return HttpResponse("Merci de remplir tous les champs du formulaire.", status=400)
    else:
        form = ContactUsForm()

    return render(request, 'home.html', {'form': form})