import datetime
import json
from flask import Flask , render_template
from unittest.mock import patch
from server import book
from conftest import app, client, mock_competitions, mock_clubs

# # Fixture pour les données de test
# @pytest.fixture
# def load_clubs():
#     with open('clubs.json') as c:
#         listOfClubs = json.load(c)['clubs']
#         return listOfClubs
#
# @pytest.fixture
# def load_competitions():
#     with open('competitions.json') as comps:
#         listOfCompetitions = json.load(comps)['competitions']
#         return listOfCompetitions

# Test unitaire pour la réservation sur une compétition passée

def test_book_past_competition(mock_competitions, mock_clubs):
    with app.test_request_context():

        competitions = mock_competitions
        clubs = mock_clubs

        # Exécute la fonction book avec une compétition passée
        with app.test_client() as client:
            response = client.get('/book/Date_Over/Simply_Lift')

            # Vérifie que la redirection s'est produite
            assert response.status_code == 200
            assert "Ce concours a déjà eu lieu." in response.data.decode('utf-8')
            assert "This competition has already taken place." in response.data.decode('utf-8')


def test_book_future_competition(mock_clubs, mock_competitions):
    with app.test_request_context():

        competitions = mock_competitions
        clubs = mock_clubs

        # Exécute la fonction book avec une compétition passée
        with app.test_client() as client:
            response = client.get('/book/HollyDays/Simply_Lift')

            # Vérifie que la redirection s'est produite
            assert response.status_code == 200
            assert "Great-booking complete!"



