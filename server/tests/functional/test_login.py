import pytest
from flask import g, session
import time
#from flaskr.db import get_db



def test_login(client, auth):
    response = client.post('/api/v1/users/login', json={'username': 'heist', 'password': '111'})
    assert response.status_code == 200
    json_data = response.get_json()
    print(json_data)
    print(response.headers)
 
    #assert response.headers['Location'] == 'http://localhost/'


@pytest.mark.parametrize(('username', 'password', 'message'), (
    ('heist', 'test', b'Incorrect password.'),
    ('test', '111', b'Incorrect username.'),
))
def test_login_validate_input(auth, username, password, message):
    response = auth.login(username, password)
    assert response.status_code == 401
    #print(response.data)
    #assert message in response.data

@pytest.mark.slow
@pytest.mark.parametrize( ('username','password', 'privilege'), (
                          ('heist', '111' , '0'),
                          ('combo', 'combo12378981', '1'),

))
def test_get_users_privilege(auth, username, password,privilege):
    resp = auth.login(username, password)
    assert resp.status_code == 200
    print(resp.get_json())