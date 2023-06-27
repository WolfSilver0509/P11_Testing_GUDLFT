import pytest
from flask import Flask, request, render_template, flash
import json

@pytest.fixture
def client():
    app = Flask(__name__)
    app.config['TESTING'] = True
    client = app.test_client()
    yield client


def load_json_file(file_path):
    with open(file_path) as f:
        data = json.load(f)
    return data


def test_purchase_places_exceed_max_limit(client):
    # Créez des données de test pour la compétition et le club
    clubs = load_json_file("clubs.json")["clubs"]
    competitions = load_json_file("competitions.json")["competitions"]

    print(clubs)
    print(competitions)

    # Simulez une requête POST avec un nombre de places supérieur à la limite maximale
    response = client.post('/purchasePlaces', data={ 'club': 'Simply Lift','competition': 'Fall Classic', 'places': '13'})

    print(response)
    # Vérifiez la réponse et le message flash correspondant
    assert response.status_code == 200
    assert "Un maximum de 12 places peuvent être réservées par un club / Maximum 12 places can be booked by a club." in response.data.decode('utf-8')








def atest_purchase_places_within_max_limit(client):
    # Créez des données de test pour la compétition et le club
    competitions = [
        {'name': 'Fall Classic', 'numberOfPlaces': '10'}
    ]
    clubs = [
        {'name': 'Simply Lift'}
    ]

    # Simulez une requête POST avec un nombre de places dans la limite maximale
    response = client.post('/purchasePlaces', data={'competition': 'Fall Classic', 'club': 'Simply Lift', 'places': '10'})

    # Vérifiez la réponse et le message flash correspondant
    assert response.status_code == 200
    assert "Great-booking complete!" in response.data.decode('utf-8')

def atest_purchase_places_below_max_limit(client):
    # Créez des données de test pour la compétition et le club
    competitions = [
        {'name': 'Fall Classic', 'numberOfPlaces': '10'}
    ]
    clubs = [
        {'name': 'Simply Lift'}
    ]

    # Simulez une requête POST avec un nombre de places en dessous de la limite maximale
    response = client.post('/purchasePlaces', data={'competition': 'Fall Classic', 'club': 'Simply Lift', 'places': '5'})

    # Vérifiez la réponse et le message flash correspondant
    assert response.status_code == 200
    assert "Great-booking complete!" in response.data.decode('utf-8')
