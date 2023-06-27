import pytest
from flask import Flask, request, render_template, flash
import json
from server import app

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client



def test_purchase_places_exceed_max_limit(client):
    # Créez des données de test pour la compétition et le club
    competitions = [
        {'name': 'Fall Classic', 'numberOfPlaces': '10'}
    ]
    clubs = [
        {'name': 'Simply Lift'}
    ]

    # Simulez une requête POST avec un nombre de places supérieur à la limite maximale
    response = client.post('/purchasePlaces', data={ 'club': 'Simply Lift','competition': 'Fall Classic', 'places': '13'})

    # Vérifiez la réponse et le message flash correspondant
    assert response.status_code == 200
    assert "Un maximum de 12 places peuvent être réservées par un club / Maximum 12 places can be booked by a club." in response.data.decode('utf-8')


def test_purchase_valid_places(client):
    # Créez des données de test pour la compétition et le club
    competitions = [
        {'name': 'Fall Classic', 'numberOfPlaces': '13'}
    ]
    clubs = [
        {'name': 'Simply Lift'}
    ]
    # Simulez une requête POST avec un nombre de places dans la limite maximale
    response = client.post('/purchasePlaces', data={'competition': 'Fall Classic', 'club': 'Simply Lift', 'places': '5'})

    # Vérifiez la réponse et le message flash correspondant
    assert response.status_code == 200
    assert "Place réservé avec succcés / Great-booking complete!" in response.data.decode('utf-8')


