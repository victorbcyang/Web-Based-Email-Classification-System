import pytest
from flask import g, session
from webapp.db import get_db
'''
    This code is for testing register.
'''

# test register
def test_register(client, app):
    # client.get() makes a GET request and returns the Response object returned by Flask.
    # simple request is made and checked for a 200 OK status_code.
    # If rendering failed, Flask would return a 500 Internal Server Error code.
    assert client.get('/auth/register').status_code == 200

    # client.post() makes a POST request, converting the data dict into form data.
    response = client.post(
        '/auth/register', \
            data={'username': 'a', 'password': 'a', \
                'email': 'hello@jjj.com', 'phone': '752-896-147', \
                    'first_name': 'Happy', 'middle_name': 'H.', 'last_name': 'Chen', \
                        'address': '888 S Hope', 'occupation': 'Student'}
    )
    # headers will have a Location header with the login URL when the register view redirects to the login view.
    assert 'http://localhost/auth/login' == response.headers['Location']

    with app.app_context():
        assert get_db().execute(
            "SELECT * FROM user WHERE username = 'a'",
        ).fetchone() is not None


# test different invalid input and error messages
# pytest.mark.parametrize tells Pytest to run the same test function with different arguments.
@pytest.mark.parametrize(('username', 'password', 'email', 'phone', 'first_name', 'middle_name', 'last_name', 'address', 'occupation', 'message'),(
    ('', '', '', '', '', '', '', '', '', b'Username is required.'),
    ('a', '', '', '', '', '', '', '', '', b'Password is required.'),
    ('a', 'a', '', '', '', '', '', '', '', b'Email is required.'),
    ('a', 'a', 'hello@jjj.com', '', '', '', '', '', '', b'Phone is required.'),
    ('a', 'a', 'hello@jjj.com', '752-896-147', '', '', '', '', '', b'First Name is required.'),
    ('a', 'a', 'hello@jjj.com', '752-896-147', 'Happy', '', '', '', '', b'Middle Name is required.'),
    ('a', 'a', 'hello@jjj.com', '752-896-147', 'Happy', 'H.', '', '', '', b'Last Name is required.'),
    ('a', 'a', 'hello@jjj.com', '752-896-147', 'Happy', 'H.', 'Chen', '', '', b'Address is required.'),
    ('a', 'a', 'hello@jjj.com', '752-896-147', 'Happy', 'H.', 'Chen', '888 S Hope', '', b'Occupation is required.'),
    ('test', 'test', 'cdf@yahoo.com', '456-789-963', 'Name', 'M.', 'Last', '10980 Wellworth Ave, Los Angeles, CA 90024', 'CEO', b'already registered'),
))
def test_register_validate_input(client, username, password, email, phone, first_name, middle_name, last_name, address, occupation, message):
    response = client.post(
        '/auth/register',
        data={'username': username, 'password': password, \
                'email': email, 'phone': phone, \
                    'first_name': first_name, 'middle_name': middle_name, 'last_name': last_name, \
                        'address': address, 'occupation': occupation}
    )
    assert message in response.data



# test login after registered
def test_login(client, auth):
    # client.get() makes a GET request and returns the Response object returned by Flask.
    # simple request is made and checked for a 200 OK status_code.
    # If rendering failed, Flask would return a 500 Internal Server Error code.
    assert client.get('/auth/login').status_code == 200
    response = auth.login()
    assert response.headers['Location'] == 'http://localhost/'

    # client in a with block allows accessing context variables such as session after the response is returned.
    with client:
        client.get('/')
        assert session['user_id'] == 1
        assert g.user['username'] == 'test'


# test different invalid input and error messages
# pytest.mark.parametrize tells Pytest to run the same test function with different arguments.
@pytest.mark.parametrize(('username', 'password', 'message'), (
    ('a', 'test', b'Incorrect username.'),
    ('test', 'a', b'Incorrect password.'),
))
def test_login_validate_input(auth, username, password, message):
    response = auth.login(username, password)
    assert message in response.data


# test logout
def test_logout(client, auth):
    auth.login()
    
    # client in a with block allows accessing context variables such as session after the response is returned.
    with client:
        auth.logout()
        # session should not contain user_id after logging out.
        assert 'user_id' not in session