from tests.utils.random_content import random_string, random_mac
from http import HTTPStatus


def test_post_child(client, parent):
    json_data = {
        'mac_address': random_mac(),
        'nickname': random_string(),
        'parent_token': random_string(),
    }

    # invalid token
    resp = client.post('/child', json=json_data)
    assert resp.status_code == HTTPStatus.UNAUTHORIZED

    # get token
    resp = client.get('/parent/child_registration_token', auth=(parent.email, parent.password))
    assert resp.status_code == HTTPStatus.OK
    json_data['parent_token'] = resp.json

    # valid token & invalid params
    resp = client.post('/child', json={'parent_token': json_data['parent_token']})
    assert resp.status_code == HTTPStatus.BAD_REQUEST

    # valid request
    resp = client.post('/child', json=json_data)
    assert resp.status_code == HTTPStatus.CREATED
    assert 'token' in resp.json


def test_get_child(client, parent, child):
    # invalid auth
    resp = client.get('/child')
    assert resp.status_code == HTTPStatus.UNAUTHORIZED

    # invalid parameters
    resp = client.get('/child', auth=(parent.email, parent.password))
    assert resp.status_code == HTTPStatus.BAD_REQUEST
    message = resp.json['message']
    assert 'id' in message

    # valid request
    params = {'id': child.id}
    resp = client.get('/child', auth=(parent.email, parent.password), query_string=params)
    assert resp.status_code == HTTPStatus.OK

    assert resp.json['id'] == child.id
    assert resp.json['parent_id'] == parent.id
    assert resp.json['mac_address'] == child.mac_address
    assert resp.json['nickname'] == child.nickname
    assert not resp.json['blocked']  # False
    assert isinstance(resp.json['usage_limits'], dict)
    assert 'Look at' in resp.json['block_websites']
    assert 'Look at' in resp.json['activity']
    assert 'Look at' in resp.json['web_history']
    assert 'Look at' in resp.json['waiting_commands']


def test_patch_child(client, parent, child):
    # test invalid auth
    resp = client.patch('/child')
    assert resp.status_code == HTTPStatus.UNAUTHORIZED

    # test invalid parameters
    resp = client.patch('/child', auth=(parent.email, parent.password))
    assert resp.status_code == HTTPStatus.BAD_REQUEST
    message = resp.json['message']
    assert 'id' in message

    # test valid request
    json_data = {
        'nickname': random_string(),
        'blocked': True,
    }

    params = {'id': child.id}
    resp = client.patch('/child', auth=(parent.email, parent.password), query_string=params, json=json_data)
    child.nickname = json_data['nickname']

    assert resp.status_code == HTTPStatus.OK
    assert resp.json['id'] == child.id
    assert resp.json['parent_id'] == parent.id
    assert resp.json['mac_address'] == child.mac_address
    assert resp.json['nickname'] == child.nickname
    assert resp.json['blocked']  # True
    # todo: add usage limits test
