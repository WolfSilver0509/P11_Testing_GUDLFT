import pytest
from flask import Flask, render_template, request, flash, url_for
from server import app, loadClubs, loadCompetitions

# Fixtures

@pytest.fixture
def client():
    app.config['TESTING'] = True
    client = app.test_client()
    yield client



def test_purchase_places_before_date_limit(client):
    response = client.post('//book/<competition>/<club>', data={'competition': 'Fall Classic', 'club': 'Simply Lift', 'places': '5'})
    assert response.status_code == 200
    assert "Ce concours a déjà eu lieu. / This competition has already taken place." in response.data.decode('utf-8')





