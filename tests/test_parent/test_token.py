from http import HTTPStatus


def test_get_token(client, parent):
    resp = client.get('/parent/child_registration_token')
    assert resp.status_code == HTTPStatus.UNAUTHORIZED

    # check response
    resp = client.get('/parent/child_registration_token', auth=(parent.email, parent.password))
    assert resp.status_code == HTTPStatus.OK
    assert resp.json != ''  # check for token existence
