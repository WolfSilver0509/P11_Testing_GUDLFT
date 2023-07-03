import pytest
from .conftest import client, load_clubs, load_competitions
import html
from flask import Flask, render_template, flash
from P11_Testing_GUDLFT.server import app, clubs, competitions, book
import json
import datetime

def load_json_file(file_path):
    with open(file_path) as f:
        data = json.load(f)
    return data


def test_user_path_valide(client):
    """ Teste le chemin d'accès valide pour l'utilisateur """
    def test_loadClubs():
        # Données de test
        clubs_data = {
            'clubs': [
                {'name': 'Club A', 'points': 100},
                {'name': 'Club B', 'points': 150},
                {'name': 'Club C', 'points': 200}
            ]
        }

        # Mock du fichier JSON pour le test
        mock_file = mock_open(read_data=json.dumps(clubs_data))

        with patch('builtins.open', mock_file):
            # Appeler la fonction loadClubs
            from P11_Testing_GUDLFT.server import loadClubs
            result = loadClubs()

            # Vérifier que le fichier JSON a été ouvert avec le bon nom de fichier
            mock_file.assert_called_once_with('clubs.json')

            # Vérifier que la fonction a renvoyé les données de clubs correctement
            assert result == clubs_data['clubs']

    def test_loadCompetitions():
        # Données de test
        competitions_data = {
            'competitions': [
                {'name': 'Competition A', 'numberOfPlaces': 50},
                {'name': 'Competition B', 'numberOfPlaces': 100},
                {'name': 'Competition C', 'numberOfPlaces': 200}
            ]
        }

        # Mock du fichier JSON pour le test
        mock_file = mock_open(read_data=json.dumps(competitions_data))

        with patch('builtins.open', mock_file):
            # Appeler la fonction loadCompetitions
            from P11_Testing_GUDLFT.server import loadCompetitions
            result = loadCompetitions()

            # Vérifier que le fichier JSON a été ouvert avec le bon nom de fichier
            mock_file.assert_called_once_with('competitions.json')

            # Vérifier que la fonction a renvoyé les données de compétitions correctement
            assert result == competitions_data['competitions']

    def test_index():
        # Créer un client de test Flask
        with app.test_client() as client:
            # Appeler la route '/'
            response = client.get('/')

            # Vérifier que la réponse a un code de statut 200 (OK)
            assert response.status_code == 200

            # Vérifier que le contenu HTML rendu contient le texte 'index.html'
            assert b'Welcome to the GUDLFT Registration Portal!' in response.data

    def show_summary_with_existing_email(client):
        # Simule une requête POST à '/showSummary' avec un email existant
        response = client.post('/showSummary', data={'email': 'kate@shelifts.co.uk'})

        # Assert retourne le code 200 (OK)
        assert response.status_code == 200

        assert 'Welcome' in response.get_data(as_text=True)
        assert 'kate@shelifts.co.uk' in response.get_data(as_text=True)

    def purchase_places_with_enough_points_available(client):
        clubs = load_json_file("clubs.json")["clubs"]
        competitions = load_json_file("competitions.json")["competitions"]

        # Simuler une requête POST avec suffisamment de points disponibles
        response = client.post('/purchasePlaces',
                               data={'competition': 'Fall Classic', 'club': 'She Lifts', 'places': '3'})

        # Vérifier la réponse
        assert response.status_code == 200
        assert "Place réservé avec succcés / Great-booking complete!" in response.data.decode('utf-8')

    def purchase_valid_places(client):
        # Créez des données de test pour la compétition et le club pour tester la réservation de places
        clubs = load_json_file("clubs.json")["clubs"]
        competitions = load_json_file("competitions.json")["competitions"]

        # Simulez une requête POST avec un nombre de places dans la limite maximale
        response = client.post('/purchasePlaces',
                               data={'competition': 'Fall Classic', 'club': 'She Lifts', 'places': '5'})
        # print(f"response: {response.data.decode('utf-8')}")
        # Vérifiez la réponse et le message flash correspondant
        assert response.status_code == 200
        assert "Place réservé avec succcés / Great-booking complete!" in response.data.decode('utf-8')

    def book_valide_date(load_competitions, load_clubs):
        # Utilisez les données de test chargées à partir des fichiers JSON
        clubs.extend(load_clubs)
        competitions.extend(load_competitions)

        with app.test_client() as client:
            # Créer une nouvelle compétition avec une date future
            future_competition = {
                'name': 'Future Competition',
                'date': (datetime.date.today() + datetime.timedelta(days=7)).strftime("%Y-%m-%d %H:%M:%S"),
                'numberOfPlaces': 10
            }
            competitions.append(future_competition)

            # Exécuter la fonction book avec la compétition future
            response = client.get('/book/Future Competition/She Lifts')
            # Vérifier que la réponse contient les informations attendues
            assert response.status_code == 200

    def logout(client):
        # Appeler la route '/logout'
        response = client.get('/logout', follow_redirects=True)

        # Vérifier que la redirection se fait vers la route 'index'
        assert response.status_code == 200
        assert request.path == '/logout'

        # Vérifier que la fonction 'index' est appelée
        assert b'Welcome to the GUDLFT Registration Portal!' in response.data

def test_user_path_invalide_email(client):

    def show_summary_with_non_existing_email(client):
        # Simule une requête POST à '/showSummary' avec un email non existant
        response = client.post('/showSummary', data={'email': 'nonexisting@example.com'})

        # Assert retourne le code 200 (OK)
        assert response.status_code == 200

        error_message = "L'email nonexisting@example.com n'est pas enregistré sur le site."
        decoded_response = html.unescape(response.get_data(as_text=True))
        assert error_message in decoded_response


def test_user_path_invalide_place(client):

    def show_summary_with_existing_email(client):
        # Simule une requête POST à '/showSummary' avec un email existant
        response = client.post('/showSummary', data={'email': 'admin@irontemple.com'})

        # Assert retourne le code 200 (OK)
        assert response.status_code == 200

        assert 'Welcome' in response.get_data(as_text=True)
        assert 'admin@irontemple.com' in response.get_data(as_text=True)

    def purchase_places_with_not_enough_points_available(client):
        clubs = load_json_file("clubs.json")["clubs"]
        competitions = load_json_file("competitions.json")["competitions"]

        # Simuler une requête POST avec un nombre de points supérieur à ceux disponibles
        response = client.post('/purchasePlaces',
                               data={'competition': 'Fall Classic', 'club': 'Iron Temple', 'places': '5'})
        # Vérifier la réponse
        assert response.status_code == 200
        assert "Pas assez de points disponibles pour ce club. / Not enough points available for this club." in response.data.decode(
            'utf-8')

    def logout(client):
        # Appeler la route '/logout'
        response = client.get('/logout', follow_redirects=True)

        # Vérifier que la redirection se fait vers la route 'index'
        assert response.status_code == 200
        assert request.path == '/logout'

        # Vérifier que la fonction 'index' est appelée
        assert b'Welcome to the GUDLFT Registration Portal!' in response.data


def test_user_path_invalide_place_exed_12(client):

    def show_summary_with_existing_email(client):
        # Simule une requête POST à '/showSummary' avec un email existant
        response = client.post('/showSummary', data={'email': 'john@simplylift.co'})

        # Assert retourne le code 200 (OK)
        assert response.status_code == 200

        assert 'Welcome' in response.get_data(as_text=True)
        assert 'john@simplylift.co' in response.get_data(as_text=True)

    def purchase_places_exceed_max_limit(client):
        # charger des données de test pour la compétition et le club pour tester la réservation de places
        clubs = load_json_file("clubs.json")["clubs"]
        competitions = load_json_file("competitions.json")["competitions"]

        # Simulez une requête POST avec un nombre de places supérieur à la limite maximale
        response = client.post('/purchasePlaces',
                               data={'club': 'Simply Lift', 'competition': 'Fall Classic', 'places': '13'})

        # Vérifiez la réponse et le message flash correspondant
        assert response.status_code == 200
        assert "Un maximum de 12 places peuvent être réservées par un club / Maximum 12 places can be booked by a club." in response.data.decode(
            'utf-8')

    def logout(client):
        # Appeler la route '/logout'
        response = client.get('/logout', follow_redirects=True)

        # Vérifier que la redirection se fait vers la route 'index'
        assert response.status_code == 200
        assert request.path == '/logout'

        # Vérifier que la fonction 'index' est appelée
        assert b'Welcome to the GUDLFT Registration Portal!' in response.data

def user_path_invalide_date_past(client):

    def show_summary_with_existing_email(client):
        # Simule une requête POST à '/showSummary' avec un email existant
        response = client.post('/showSummary', data={'email': 'john@simplylift.co'})

        # Assert retourne le code 200 (OK)
        assert response.status_code == 200

        assert 'Welcome' in response.get_data(as_text=True)
        assert 'john@simplylift.co' in response.get_data(as_text=True)

    # Test d'intégration pour la route '/book/<competition>/<club>'
    def book_date_past(load_clubs, load_competitions):
        # Utilisez les données de test chargées à partir des fichiers JSON
        clubs.extend(load_clubs)
        competitions.extend(load_competitions)

        with app.test_client() as client:
            # Exécute la fonction book avec une compétition passée
            response = client.get('/book/Spring Festival/Simply Lift')

            # Vérifie que la redirection s'est produite
            assert response.status_code == 200
            assert "Ce concours a déjà eu lieu. / This competition has already taken place." in response.data.decode(
                'utf-8')

    def logout(client):
        # Appeler la route '/logout'
        response = client.get('/logout', follow_redirects=True)

        # Vérifier que la redirection se fait vers la route 'index'
        assert response.status_code == 200
        assert request.path == '/logout'

        # Vérifier que la fonction 'index' est appelée
        assert b'Welcome to the GUDLFT Registration Portal!' in response.data


