import datetime
import json
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