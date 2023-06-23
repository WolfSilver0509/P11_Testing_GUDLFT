import json
import pytest

from server import app

import json

@pytest.fixture
def client():
    app.config['TESTING'] = True
    client = app.test_client()
    yield client

def test_purchase_places_with_enough_points_available(client):
    # Charger les données des fichiers JSON
    clubs_data = json.loads("clubs.json")
    competitions_data = json.loads("competitions.json")

    # Simuler une requête POST avec suffisamment de points disponibles
    response = client.post('/purchasePlaces', data={'competition': 'Fall Classic', 'club': 'Simply Lift', 'places': '3'})

    # Vérifier la réponse
    assert response.status_code == 200
    assert "Great-booking complete!" in response.data.decode('utf-8')

    # Vérifier que les points et le nombre de places ont été mis à jour
    clubs = clubs_data['clubs']
    competitions = competitions_data['competitions']

    club = next((c for c in clubs if c['name'] == 'Simply Lift'), None)
    competition = next((c for c in competitions if c['name'] == 'Fall Classic'), None)

    assert club is not None
    assert competition is not None

    assert int(club['points']) == 10  # Points restants après achat de 3 places
    assert int(competition['numberOfPlaces']) == 10  # Places restantes après achat de 3 places

def test_purchase_places_with_not_enough_points_available(client):
    # Charger les données des fichiers JSON
    clubs_data = json.loads("clubs.json")
    competitions_data = json.loads("competitions.json")

    # Simuler une requête POST avec un nombre de points supérieur à ceux disponibles
    response = client.post('/purchasePlaces', data={'competition': 'Fall Classic', 'club': 'Iron Temple', 'places': '5'})

    # Vérifier la réponse
    assert response.status_code == 200
    assert "Not enough points available for this club." in response.data.decode('utf-8')

    # Vérifier que les points et le nombre de places n'ont pas été modifiés
    clubs = clubs_data['clubs']
    competitions = competitions_data['competitions']

    club = next((c for c in clubs if c['name'] == 'Iron Temple'), None)
    competition = next((c for c in competitions if c['name'] == 'Fall Classic'), None)

    assert club is not None
    assert competition is not None

    assert int(club['points']) == 4  # Points restants inchangés
    assert int(competition['numberOfPlaces']) == 13  # Places restantes inchangées
