# import pytest
from flask import Flask, request, render_template, flash
import json
from conftest import app, client , mock_competitions, mock_clubs
# from server import app

# @pytest.fixture
# def client():
#     app.config['TESTING'] = True
#     client = app.test_client()
#     yield client
#

def test_purchase_places_exceed_max_limit(client , mock_competitions, mock_clubs):
    # charger des données de test pour la compétition et le club
    competitions = mock_competitions
    clubs = mock_clubs

    # Simulez une requête POST avec un nombre de places supérieur à la limite maximale
    response = client.post('/purchasePlaces', data={ 'club': 'Simply_Lift','competition': 'More_than_12_places_avalaible', 'places': '13'})

    # Vérifiez la réponse et le message flash correspondant
    assert response.status_code == 200
    assert "Un maximum de 12 places peuvent être réservées par un club / Maximum 12 places can be booked by a club." in response.data.decode('utf-8')


def test_purchase_valid_places(client, mock_competitions, mock_clubs):
    # Créez des données de test pour la compétition et le club
    competition = mock_competitions
    club = mock_clubs
    # Simulez une requête POST avec un nombre de places dans la limite maximale
    response = client.post('/purchasePlaces', data={'competition': 'More_than_12_places_avalaible', 'club': 'Simply_Lift', 'places': '6'})
    # Vérifiez la réponse et le message flash correspondant
    assert response.status_code == 200
    assert "Place réservé avec succcés / Great-booking complete!" in response.data.decode('utf-8')


