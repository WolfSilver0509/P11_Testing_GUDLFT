import datetime
import json
import pytest
from flask import Flask
from unittest.mock import patch
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

# Test unitaire pour la réservation sur une compétition passée
@patch('server.datetime')
def test_book_past_competition(mock_datetime, load_clubs, load_competitions):
    mock_datetime.date.today.return_value = datetime.date(2023, 1, 1)

    # Utilisez les données de test chargées à partir des fichiers JSON
    clubs.extend(load_clubs)
    competitions.extend(load_competitions)

    # Exécute la fonction book avec une compétition passée
    response = book('Fall Classic', 'She Lifts')

    # Vérifie que la redirection s'est produite
    assert response.status_code == 200
    assert 'Ce concours a déjà eu lieu.' not in response.data.decode('utf-8')
    assert 'This competition has already taken place.' not in response.data.decode('utf-8')


# Test unitaire pour la réservation sur une compétition future
#Utilisation du décorateur patch pour remplacer la fonction datetime.date.today par une fonction de mock ,
# et fixer sa valeur à une date spécifique afin de simuler différentes conditions temporelles.
@patch('server.datetime')
def atest_book_future_competition(mock_datetime, load_clubs, load_competitions):
    mock_datetime.date.today.return_value = datetime.date(2023, 1, 1)

    # Utilisez les données de test chargées à partir des fichiers JSON
    clubs.extend(load_clubs)
    competitions.extend(load_competitions)

    # Crée une nouvelle compétition avec une date future
    future_competition = {
        'name': 'Future Competition',
        'date': (datetime.date.today() + datetime.timedelta(days=7)).strftime("%Y-%m-%d %H:%M:%S"),
        'numberOfPlaces': 10
    }
    competitions.append(future_competition)

    # Exécute la fonction book avec la compétition future
    response = book('Future Competition', 'She Lifts')

    # Vérifie que la réponse contient les informations attendues
    assert response.status_code == 200


