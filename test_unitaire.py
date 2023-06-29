import html
from flask import Flask, request, render_template, flash
import json
from conftest import app, client , mock_competitions, mock_clubs

def test_show_summary_with_existing_email(monkeypatch):
    # Définir les données simulées pour la requête
    email = 'kate@shelifts.co.uk'
    data = {'email': email}

    # Simuler la requête
    with app.test_client() as client:
        response = client.post('/showSummary', data=data)

    # Vérifier la réponse
    assert response.status_code == 200
    assert b'Welcome' in response.data
    assert b'kate@shelifts.co.uk' in response.data

def test_show_summary_with_non_existing_email(monkeypatch):
    # Définir les données simulées pour la requête
    email = 'nonexisting@example.com'
    data = {'email': email}

    # Simuler la requête
    with app.test_client() as client:
        response = client.post('/showSummary', data=data)

    # Vérifier la réponse
    assert response.status_code == 200
    error_message = f"L'email {email} n'est pas enregistré sur le site."
    decoded_response = html.unescape(response.get_data(as_text=True))
    assert error_message in decoded_response

def test_purchase_places_with_enough_points_available(client, mock_competitions, mock_clubs):
    # Charger les données des fichiers JSON
    competitions = mock_competitions
    clubs = mock_clubs

    # Simuler une requête POST avec suffisamment de points disponibles
    response = client.post('/purchasePlaces', data={'competition': 'HollyDays', 'club': 'Simply_Lift', 'places': '3'})
    # Vérifier la réponse
    assert response.status_code == 200
    assert "Place réservé avec succcés / Great-booking complete!" in response.data.decode('utf-8')


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


def test_purchase_places_exceed_max_limit(client , mock_competitions, mock_clubs):
    # charger des données de test pour la compétition et le club pour tester la réservation de places
    competitions = mock_competitions
    clubs = mock_clubs

    # Simulez une requête POST avec un nombre de places supérieur à la limite maximale
    response = client.post('/purchasePlaces', data={ 'club': 'Simply_Lift','competition': 'More_than_12_places_avalaible', 'places': '13'})

    # Vérifiez la réponse et le message flash correspondant
    assert response.status_code == 200
    assert "Un maximum de 12 places peuvent être réservées par un club / Maximum 12 places can be booked by a club." in response.data.decode('utf-8')


def test_purchase_valid_places(client, mock_competitions, mock_clubs):
    # Créez des données de test pour la compétition et le club pour tester la réservation de places
    competition = mock_competitions
    club = mock_clubs
    # Simulez une requête POST avec un nombre de places dans la limite maximale
    response = client.post('/purchasePlaces', data={'competition': 'More_than_12_places_avalaible', 'club': 'Simply_Lift', 'places': '6'})
    # Vérifiez la réponse et le message flash correspondant
    assert response.status_code == 200
    assert "Place réservé avec succcés / Great-booking complete!" in response.data.decode('utf-8')



from unittest.mock import patch
from server import book
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

# from server import app, clubs, competitions, updateClubs, updateCompetitions
# from conftest import load_clubs, load_competitions
#
# # Test d'intégration pour la route '/purchasePlaces'
# @patch('server.updateClubs')  # Remplace la fonction updateClubs par une fonction fictive
# @patch('server.updateCompetitions')  # Remplace la fonction updateCompetitions par une fonction fictive
# def test_purchase_places_integration(mock_update_clubs, mock_update_competitions, load_clubs, load_competitions):
#     app.config['TESTING'] = True
#     app.secret_key = 'something_special'
#
#     # Utilisez les données de test chargées à partir du fichier JSON de base
#     clubs[:] = load_clubs  # Remplace les données de clubs par les données de test
#     competitions[:] = load_competitions  # Remplace les données de compétitions par les données de test
#
#     # Données de test
#     competition_name = 'Spring Festival'
#     club_name = 'Simply Lift'
#     places_required = 2
#
#     # Obtient les valeurs initiales des points du club et du nombre de places de la compétition
#     initial_club = next((c for c in clubs if c['name'] == club_name), None)
#     initial_competition = next((c for c in competitions if c['name'] == competition_name), None)
#     initial_club_points = int(initial_club['points']) if initial_club else 0
#     initial_competition_places = int(initial_competition['numberOfPlaces']) if initial_competition else 0
#
#     with app.test_client() as client:
#         # Effectue une réservation en soumettant le formulaire
#         response = client.post('/purchasePlaces', data={
#             'competition': competition_name,
#             'club': club_name,
#             'places': str(places_required)
#         })
#
#         # Vérifie que la redirection s'est produite avec succès
#         assert response.status_code == 200
#
#         # Vérifie que les points du club ont été mis à jour correctement
#         updated_club = next((c for c in clubs if c['name'] == club_name), None)
#         assert updated_club is not None
#         assert int(updated_club['points']) == initial_club_points - places_required
#
#         # Vérifie que les compétitions ont également été mises à jour
#         updated_competition = next((c for c in competitions if c['name'] == competition_name), None)
#         assert updated_competition is not None
#         assert int(updated_competition['numberOfPlaces']) == initial_competition_places - places_required
#
#
