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
