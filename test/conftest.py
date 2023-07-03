import pytest
from P11_Testing_GUDLFT.server import app
# from P11_testting_GUDLFT.test import clubs, competitions
import json

# Fixture pour les données de test
@pytest.fixture
def load_clubs():
    with open('test/clubs.json') as c:
        listOfClubs = json.load(c)['clubs']
        return listOfClubs

@pytest.fixture
def load_competitions():
    with open('test/competitions.json') as comps:
        listOfCompetitions = json.load(comps)['competitions']
        return listOfCompetitions