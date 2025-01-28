import pytest
from app.main import app

@pytest.fixture
def client():
    app.testing = True
    with app.test_client() as client:
        yield client

def test_get_players(client):
    response = client.get('/api/v1/players')
    assert response.status_code == 200
    assert 'names' in response.get_json()

def test_get_player_stats(client):
    response = client.get('/api/v1/player-stats/Jackson%20Jobe')
    assert response.status_code == 200
    assert 'stats' in response.get_json()

def test_compare_players(client):
    response = client.get('/api/v1/compare-players/Jackson%20Jobe')
    assert response.status_code == 200
    assert 'result' in response.get_json()
