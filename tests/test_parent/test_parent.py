from http import HTTPStatus

from tests.utils.random_content import random_string


def test_post_parent(client):
    json_data = {
        'email': f"{random_string()}@gmail.com",
        'password': random_string(),
        'nickname': random_string(),
    }

    # check parameters (must use email, password, nickname)
    resp = client.post('/parent')
    assert resp.status_code == HTTPStatus.BAD_REQUEST
    message = resp.json['message']
    assert 'email' in message
    assert 'password' in message
    assert 'nickname' in message

    # check response
    resp = client.post('/parent', json=json_data)
    assert resp.status_code == HTTPStatus.CREATED
    assert 'id' in resp.json
    assert json_data['email'] == resp.json.get('email')
    assert json_data['nickname'] == resp.json.get('nickname')
    assert [] == resp.json.get('children')


def test_get_parent(client, parent):
    # check auth
    resp = client.get('/parent')
    assert resp.status_code == HTTPStatus.UNAUTHORIZED

    # check response
    resp = client.get('/parent', auth=(parent.email, parent.password))
    assert resp.status_code == HTTPStatus.OK
    assert parent.id == resp.json.get('id')
    assert parent.email == resp.json.get('email')
    assert parent.nickname == resp.json.get('nickname')
    assert [] == resp.json.get('children')


def test_patch_parent(client, parent):
    # check auth
    resp = client.patch('/parent')
    assert resp.status_code == HTTPStatus.UNAUTHORIZED

    to_change = {
        'email': f"{random_string()}@gmail.com",
        'password': random_string(),
        'nickname': random_string(),
    }

    # check response
    resp = client.patch('/parent', auth=(parent.email, parent.password), json=to_change)
    assert resp.status_code == HTTPStatus.OK

    # update parent data
    for key, val in to_change.items():
        setattr(parent, key, val)

    # check response
    assert parent.id == resp.json.get('id')
    assert parent.email == resp.json.get('email')
    assert parent.nickname == resp.json.get('nickname')
    assert [] == resp.json.get('children')
