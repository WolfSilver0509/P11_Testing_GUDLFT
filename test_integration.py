import pytest
from server import app
import html

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_show_summary_with_existing_email(client):
    # Simule une requête POST à '/showSummary' avec un email existant
    response = client.post('/showSummary', data={'email': 'kate@shelifts.co.uk'})

    # Assert retourne le code 200 (OK)
    assert response.status_code == 200

    
    assert 'Welcome' in response.get_data(as_text=True)
    assert 'kate@shelifts.co.uk' in response.get_data(as_text=True)

def test_show_summary_with_non_existing_email(client):
    # Simule une requête POST à '/showSummary' avec un email non existant
    response = client.post('/showSummary', data={'email': 'nonexisting@example.com'})

    # Assert retourne le code 200 (OK)
    assert response.status_code == 200

    error_message = "L'email nonexisting@example.com n'est pas enregistré sur le site."
    decoded_response = html.unescape(response.get_data(as_text=True))
    assert error_message in decoded_response

import json
from flask import Flask
from flask.testing import FlaskClient
from pytest import fixture



@fixture
def client() -> FlaskClient:
    with app.test_client() as client:
        yield client


def load_json_file(file_path):
    with open(file_path) as f:
        data = json.load(f)
    return data


def test_purchase_places_with_enough_points_available(client):
    clubs = load_json_file("clubs.json")["clubs"]
    competitions = load_json_file("competitions.json")["competitions"]

    # Simuler une requête POST avec suffisamment de points disponibles
    response = client.post('/purchasePlaces',
                           data={'competition': 'Fall Classic', 'club': 'Simply Lift', 'places': '3'})

    # Vérifier la réponse
    print(response)
    assert response.status_code == 200
    assert "Super votre réservation est bien prise en compte / Great-booking complete!" in response.data.decode('utf-8')


def test_purchase_places_with_not_enough_points_available(client):
    clubs = load_json_file("clubs.json")["clubs"]
    competitions = load_json_file("competitions.json")["competitions"]

    # Simuler une requête POST avec un nombre de points supérieur à ceux disponibles
    response = client.post('/purchasePlaces',
                           data={'competition': 'Fall Classic', 'club': 'Iron Temple', 'places': '5'})
    # Vérifier la réponse
    assert response.status_code == 200
    assert "Pas assez de points disponibles pour ce club. / Not enough points available for this club." in response.data.decode(
        'utf-8')
