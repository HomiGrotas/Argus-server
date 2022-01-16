import pytest
from http import HTTPStatus

from app import create_app, db
from .utils.random_content import random_string, random_mac

app = create_app()
db.drop_all(app=app)
db.create_all(app=app)


class Parent:
    def __init__(self, id: int, email: str, nickname: str, children: [], password: str):
        self.id = id
        self.email = email
        self.nickname = nickname
        self.children = children
        self.password = password


class Child:
    def __init__(self, mac_address: str, nickname: str, token: str):
        self.mac_address = mac_address
        self.nickname = nickname
        self.token = token


@pytest.fixture
def client():
    """A test client for the app."""
    return app.test_client()


@pytest.fixture
def parent(client):
    json_data = {
        'email': f"{random_string()}@test.com",
        'password': random_string(),
        'nickname': random_string(),
    }
    resp = client.post('/parent', json=json_data)
    assert resp.status_code == HTTPStatus.CREATED
    json_resp = resp.json
    json_resp['password'] = json_data['password']
    new_parent = Parent(**json_resp)
    return new_parent


@pytest.fixture
def child(client, parent):
    # get token
    resp = client.get('/parent/child_registration_token', auth=(parent.email, parent.password))
    assert resp.status_code == HTTPStatus.OK
    token = resp.json

    # create child
    json_data = {
        'mac_address': random_mac(),
        'nickname': random_string(),
        'parent_token': token,
    }
    resp = client.post('/child', json=json_data)
    assert resp.status_code == HTTPStatus.CREATED
    token = resp.json['token']

    return Child(
        mac_address=json_data['mac_address'],
        nickname=json_data['nickname'],
        token=token,
    )
