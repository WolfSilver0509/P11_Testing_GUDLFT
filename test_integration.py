import pytest
from server import app
from conftest import client
import html


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
    assert response.status_code == 200
    assert "Place réservé avec succcés / Great-booking complete!" in response.data.decode('utf-8')


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

from flask import Flask, request, render_template, flash
import json


def load_json_file(file_path):
    with open(file_path) as f:
        data = json.load(f)
    return data


def test_purchase_places_exceed_max_limit(client):
    # charger des données de test pour la compétition et le club pour tester la réservation de places
    clubs = load_json_file("clubs.json")["clubs"]
    competitions = load_json_file("competitions.json")["competitions"]

    # Simulez une requête POST avec un nombre de places supérieur à la limite maximale
    response = client.post('/purchasePlaces', data={ 'club': 'Simply Lift','competition': 'Fall Classic', 'places': '13'})

    # Vérifiez la réponse et le message flash correspondant
    assert response.status_code == 200
    assert "Un maximum de 12 places peuvent être réservées par un club / Maximum 12 places can be booked by a club." in response.data.decode('utf-8')


def test_purchase_valid_places(client):
    # Créez des données de test pour la compétition et le club pour tester la réservation de places
    clubs = load_json_file("clubs.json")["clubs"]
    competitions = load_json_file("competitions.json")["competitions"]

    # Simulez une requête POST avec un nombre de places dans la limite maximale
    response = client.post('/purchasePlaces', data={'competition': 'Fall Classic', 'club': 'Simply Lift', 'places': '10'})
    # print(f"response: {response.data.decode('utf-8')}")
    # Vérifiez la réponse et le message flash correspondant
    assert response.status_code == 200
    assert "Place réservé avec succcés / Great-booking complete!" in response.data.decode('utf-8')



from flask import Flask, render_template, flash
import pytest
from server import app, clubs, competitions, book

# Fixture pour les données de test
@pytest.fixture
def load_clubs():
    with open('clubs.json') as c:
        listOfClubs = json.load(c)['clubs']
        return listOfClubs

@pytest.fixture
def load_competitions():
    with open('competitions.json') as comps:
        listOfCompetitions = json.load(comps)['competitions']
        return listOfCompetitions

# Test d'intégration pour la route '/book/<competition>/<club>'
def test_book_route(load_clubs, load_competitions):
    app.config['TESTING'] = True
    app.secret_key = 'something_special'

    # Utilisez les données de test chargées à partir des fichiers JSON
    clubs.extend(load_clubs)
    competitions.extend(load_competitions)

    with app.test_client() as client:
        # Exécute la fonction book avec une compétition passée
        response = client.get('/book/Spring Festival/Simply Lift')

        # Vérifie que la redirection s'est produite
        assert response.status_code == 200
        assert "Ce concours a déjà eu lieu. / This competition has already taken place." in response.data.decode('utf-8')


    with app.test_client() as client:
        # Créer une nouvelle compétition avec une date future
        future_competition = {
            'name': 'Future Competition',
            'date': (datetime.date.today() + datetime.timedelta(days=7)).strftime("%Y-%m-%d %H:%M:%S"),
            'numberOfPlaces': 10
        }
        competitions.append(future_competition)

        # Exécuter la fonction book avec la compétition future
        response = client.get('/book/Future Competition/Simply Lift')
        # Vérifier que la réponse contient les informations attendues
        assert response.status_code == 200
import datetime