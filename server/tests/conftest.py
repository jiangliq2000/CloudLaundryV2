# -*- coding: utf-8 -*-
#  Created by liqiang.jiang on 2018/10/12.
#refere file
# https://github.com/pallets/flask/blob/1.0.2/examples/tutorial/tests/conftest.py

import os
import tempfile

import pytest
from app import create_app

"""
#from flaskr.db import get_db, init_db

# read in SQL for populating test data
with open(os.path.join(os.path.dirname(__file__), 'data.sql'), 'rb') as f:
    _data_sql = f.read().decode('utf8')
"""

@pytest.fixture(scope="session")
def app():
    """Create and configure a new app instance for each test."""
    # create a temporary file to isolate the database for each test
    #db_fd, db_path = tempfile.mkstemp()
    # create the app with common test config
    app = create_app("testing")

    # create the database and load test data
    with app.app_context():
        #init_db()
        #get_db().executescript(_data_sql)
        print("init database")

    yield app

    # close and remove the temporary database
    #os.close(db_fd)
    #os.unlink(db_path)


@pytest.fixture(scope="session")
def client(app):
    """A test client for the app."""
    return app.test_client()


@pytest.fixture(scope="session")
def runner(app):
    """A test runner for the app's Click commands."""
    return app.test_cli_runner()


class AuthActions(object):
    def __init__(self, client):
        self._client = client

    def login(self, username='heist', password='111'):
        # must use json as payload name
        return self._client.post('/api/v1/users/login', json={'username': username, 'password': password}
        )

    def logout(self):
        return self._client.get('/auth/logout')


@pytest.fixture(scope="session")
def auth(client):
    return AuthActions(client)

@pytest.fixture(scope="session")
def token(auth):
    print("token: execute login to get access_token")
    resp = auth.login()
    json_data = resp.get_json()
    return json_data['access_token']