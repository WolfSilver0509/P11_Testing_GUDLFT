import json
import pytest

from server import app

import json

@pytest.fixture
def client():
    app.config['TESTING'] = True
    client = app.test_client()
    yield client

def test_purchase_places_with_enough_points_available(client):
    # Charger les données des fichiers JSON
    with open("clubs.json") as clubs_file:
        clubs_data = json.load(clubs_file)

    with open("competitions.json") as competitions_file:
        competitions_data = json.load(competitions_file)

    # Simuler une requête POST avec suffisamment de points disponibles
    response = client.post('/purchasePlaces', data={'competition': 'Fall Classic', 'club': 'Simply Lift', 'places': '3'})

    # Vérifier la réponse
    assert response.status_code == 200
    assert "Great-booking complete!" in response.data.decode('utf-8')


def test_purchase_places_with_not_enough_points_available(client):
    # Charger les données des fichiers JSON
    with open("clubs.json") as clubs_file:
        clubs_data = json.load(clubs_file)

    with open("competitions.json") as competitions_file:
        competitions_data = json.load(competitions_file)

    # Simuler une requête POST avec un nombre de points supérieur à ceux disponibles
    response = client.post('/purchasePlaces', data={'competition': 'Fall Classic', 'club': 'Iron Temple', 'places': '5'})

    # Vérifier la réponse
    assert response.status_code == 200
    assert "Not enough points available for this club." in response.data.decode('utf-8')

