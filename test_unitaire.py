from server import app
from flask import request
import pytest
import html


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
