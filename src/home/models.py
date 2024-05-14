# models.py
from django.db import models


class Devis(models.Model):
    nom = models.CharField(max_length=100)
    telephone = models.CharField(max_length=20)
    email = models.EmailField()
    point_depart = models.CharField(max_length=255)
    point_arrivee = models.CharField(max_length=255)
    distance = models.FloatField()
    consommation_carburant = models.FloatField()
    prix = models.FloatField()
