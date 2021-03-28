import os
import tempfile

import pytest
from webapp import create_app
from webapp.db import get_db, init_db

with open(os.path.join(os.path.dirname(__file__), 'data.sql'), 'rb') as f:
    _data_sql = f.read().decode('utf8')

@pytest.fixture
def app():
    # tempfile.mkstemp() creates and opens a temporary file, returning the file object and the path to it.
    db_fd, db_path = tempfile.mkstemp()
    
    # TESTING tells Flask that the app is in test mode.
    # Flask changes some internal behavior so it’s easier to test,
    # other extensions can also use the flag to make testing them easier
    app = create_app({
        'TESTING': True,
        'DATABASE': db_path,
    })

    with app.app_context():
        init_db()
        get_db().executescript(_data_sql)

    yield app

    os.close(db_fd)
    os.unlink(db_path)


@pytest.fixture
def client(app):
    # The client fixture calls app.test_client() with the application object created by the app fixture. 
    # Tests will use the client to make requests to the application without running the server.
    return app.test_client()


@pytest.fixture
def runner(app):
    # The runner fixture is similar to client. 
    # app.test_cli_runner() creates a runner that can call the Click commands registered with the application.
    return app.test_cli_runner()


# a class with methods to make a POST request to the login view with the client.
class AuthActions(object):
    def __init__(self, client):
        self._client = client

    # test login
    def login(self, username='test', password='test'):
                    # email='abc@gmail.com', phone='123-145-147',\
                    # first_name='Hello', middle_name='T.', last_name='Wang',\
                    # address='555 Westwood Plaza level, Los Angeles, CA 90095', occupation='Professor')

        return self._client.post(
            '/auth/login',
            data={'username': username, 'password': password} 
        )
        #, 'email': email, 'phone': phone, 'first_name': first_name, 'middle_name': middle_name, 'last_name': last_name, 'address': address, 'occupation': occupation}

    # test logout
    def logout(self):
        return self._client.get('/auth/logout')

# With the auth fixture, call auth.login() in a test to log in as the test user, 
# which was inserted as part of the test data in the app fixture.
@pytest.fixture
def auth(client):
    return AuthActions(client)