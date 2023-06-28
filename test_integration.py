from flask import Flask, request, render_template, flash
import json
from server import app
from conftest import client


def load_json_file(file_path):
    with open(file_path) as f:
        data = json.load(f)
    return data


def test_purchase_places_exceed_max_limit(client):
    # charger des données de test pour la compétition et le club
    clubs = load_json_file("clubs.json")["clubs"]
    competitions = load_json_file("competitions.json")["competitions"]

    # Simulez une requête POST avec un nombre de places supérieur à la limite maximale
    response = client.post('/purchasePlaces', data={ 'club': 'Simply Lift','competition': 'Fall Classic', 'places': '13'})

    # Vérifiez la réponse et le message flash correspondant
    assert response.status_code == 200
    assert "Un maximum de 12 places peuvent être réservées par un club / Maximum 12 places can be booked by a club." in response.data.decode('utf-8')


def test_purchase_valid_places(client):
    # Créez des données de test pour la compétition et le club
    # Créez des données de test pour la compétition et le club
    clubs = load_json_file("clubs.json")["clubs"]
    competitions = load_json_file("competitions.json")["competitions"]

    # Simulez une requête POST avec un nombre de places dans la limite maximale
    response = client.post('/purchasePlaces', data={'competition': 'Fall Classic', 'club': 'Simply Lift', 'places': '10'})
    # Vérifiez la réponse et le message flash correspondant
    assert response.status_code == 200
    assert "Place réservé avec succcés / Great-booking complete!" in response.data.decode('utf-8')


