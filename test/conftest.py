import pytest
from unittest.mock import patch
from P11_Testing_GUDLFT.server import app, clubs, competitions
import json

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client


@pytest.fixture
def mock_competitions(mocker):
    """
    LEs données :
    competition[0] pour tester les erreurs sur les points insuffisants pour acheter une place
    competition[1] pour tester les erreurs sur la réservation de plus de 12 places par club sur la même compétition
    competition[2] pour tester les erreur sur la date d'une compétition passée
    """

    competitions = [
        {'name': 'More_than_12_places_avalaible', "date": "2024-03-27 10:00:00",'numberOfPlaces': '13'},
        {"name": "HollyDays", "date": "2025-03-27 10:00:00", "numberOfPlaces": "25"},
        {"name": "Date_Over", "date": "2003-03-15 10:00:00", "numberOfPlaces": "10"}
    ]
    mocker.patch('P11_Testing_GUDLFT.server.competitions', competitions)
    return competitions


@pytest.fixture
def mock_clubs(mocker):
    """
    club[1] pour tester les erreurs sur les points insuffisants pour acheter une place
    club[2] pour tester les erreurs sur la réservation de plus de 12 places par club sur la même compétition
    club[3] pour tester un utilisateurs qui est une copie du json original
    """
    clubs = [
        {'name': 'Club_1', 'email': 'club1@example.com', "points": "1"},
        {'name': 'Club_2', 'email': 'club2@example.com', "points": "6"},
        {"name": "Simply_Lift", "email": "john@simplylift.co", "points": "13"}
    ]
    mocker.patch('P11_Testing_GUDLFT.server.clubs', clubs)
    return clubs



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