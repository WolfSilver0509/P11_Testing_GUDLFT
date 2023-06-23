import json
from flask import Flask
from flask.testing import FlaskClient
from pytest import fixture

from server import app


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
    response = client.post('/purchasePlaces', data={'competitions': 'Fall Classic', 'club': 'Simply Lift', 'places': '3'})

    # Vérifier la réponse
    assert response.status_code == 200
    assert "Super votre réservation est bien prise en compte / Great-booking complete!" in response.data.decode('utf-8')

    # Vérifier que les points du club et le nombre de places de la compétition ont été mis à jour
    updated_club = next(c for c in clubs if c['name'] == 'Simply Lift')
    updated_competition = next(c for c in competitions if c['name'] == 'Fall Classic')

    assert updated_club['points'] == '10'
    assert updated_competition['numberOfPlaces'] == '10'


def test_purchase_places_with_not_enough_points_available(client):
    clubs = load_json_file("clubs.json")["clubs"]
    competitions = load_json_file("competitions.json")["competitions"]

    # Simuler une requête POST avec un nombre de points supérieur à ceux disponibles
    response = client.post('/purchasePlaces', data={'competitions': 'Fall Classic', 'club': 'Iron Temple', 'places': '5'})

    # Vérifier la réponse
    assert response.status_code == 200
    assert "Pas assez de points disponibles pour ce club. / Not enough points available for this club." in response.data.decode('utf-8')

    # Vérifier que les points du club et le nombre de places de la compétition n'ont pas été modifiés
    unchanged_club = next(c for c in clubs if c['name'] == 'Iron Temple')
    unchanged_competition = next(c for c in competitions if c['name'] == 'Fall Classic')

    assert unchanged_club['points'] == '4'
    assert unchanged_competition['numberOfPlaces'] == '13'
