from flask import Flask, render_template, flash
from server import app, clubs, competitions, updateClubs, updateCompetitions
from unittest.mock import patch
from conftest import load_clubs, load_competitions


# Test d'intégration pour la route '/purchasePlaces'
@patch('server.updateClubs')  # Remplace la fonction updateClubs par une fonction fictive
@patch('server.updateCompetitions')  # Remplace la fonction updateCompetitions par une fonction fictive
def test_purchase_places_integration(mock_update_clubs, mock_update_competitions, load_clubs, load_competitions):
    app.config['TESTING'] = True
    app.secret_key = 'something_special'

    # Utilisez les données de test chargées à partir du fichier JSON de base
    clubs[:] = load_clubs  # Remplace les données de clubs par les données de test
    competitions[:] = load_competitions  # Remplace les données de compétitions par les données de test

    # Données de test
    competition_name = 'Spring Festival'
    club_name = 'Simply Lift'
    places_required = 2

    # Obtient les valeurs initiales des points du club et du nombre de places de la compétition
    initial_club = next((c for c in clubs if c['name'] == club_name), None)
    initial_competition = next((c for c in competitions if c['name'] == competition_name), None)
    initial_club_points = int(initial_club['points']) if initial_club else 0
    initial_competition_places = int(initial_competition['numberOfPlaces']) if initial_competition else 0

    with app.test_client() as client:
        # Effectue une réservation en soumettant le formulaire
        response = client.post('/purchasePlaces', data={
            'competition': competition_name,
            'club': club_name,
            'places': str(places_required)
        })

        # Vérifie que la redirection s'est produite avec succès
        assert response.status_code == 200

        # Vérifie que les points du club ont été mis à jour correctement
        updated_club = next((c for c in clubs if c['name'] == club_name), None)
        assert updated_club is not None
        assert int(updated_club['points']) == initial_club_points - places_required

        # Vérifie que les compétitions ont également été mises à jour
        updated_competition = next((c for c in competitions if c['name'] == competition_name), None)
        assert updated_competition is not None
        assert int(updated_competition['numberOfPlaces']) == initial_competition_places - places_required


