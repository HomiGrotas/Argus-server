from tests.utils.random_content import random_string, random_mac
from http import HTTPStatus


def test_post_child(client, parent):
    resp = client.get('/parent/child_registration_token', auth=(parent.email, parent.password))
    assert resp.status_code == HTTPStatus.OK
    token = resp.json

    json_data = {
        'mac_address': random_mac(),
        'nickname': random_string(),
        'parent_token': token,
    }
    resp = client.post('/child', json=json_data)
    assert resp.status_code == HTTPStatus.CREATED
    assert 'token' in resp.json


def test_get_child(client, child):
    pass


def test_patch_child():
    pass
