from fastapi.testclient import TestClient
from main import app, ALLOWED_ORIGIN, EMAIL

client = TestClient(app)


def test_stats_dynamic():
    response = client.get('/stats?values=-3,0,6,9')
    assert response.status_code == 200
    assert response.json() == {
        'email': EMAIL,
        'count': 4,
        'sum': 12,
        'min': -3,
        'max': 9,
        'mean': 3.0,
    }
    assert response.headers.get('x-request-id')
    assert float(response.headers['x-process-time']) >= 0


def test_allowed_preflight():
    response = client.options(
        '/stats',
        headers={'Origin': ALLOWED_ORIGIN, 'Access-Control-Request-Method': 'GET'},
    )
    assert response.status_code == 200
    assert response.headers.get('access-control-allow-origin') == ALLOWED_ORIGIN
    assert response.headers.get('x-request-id')
    assert float(response.headers['x-process-time']) >= 0


def test_rejected_preflight():
    response = client.options(
        '/stats',
        headers={'Origin': 'https://evil.example', 'Access-Control-Request-Method': 'GET'},
    )
    assert response.status_code == 400
    assert 'access-control-allow-origin' not in response.headers
    assert response.headers.get('x-request-id')
    assert float(response.headers['x-process-time']) >= 0


def test_bad_values():
    response = client.get('/stats?values=1,nope,3')
    assert response.status_code == 400
    assert response.headers.get('x-request-id')
    assert float(response.headers['x-process-time']) >= 0
