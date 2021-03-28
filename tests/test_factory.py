from webapp import create_app
'''
    This code is for testing the factory.
'''

def test_config():
    assert not create_app().testing
    assert create_app({'TESTING': True}).testing


def test_hello(client):
    # The hello route was added as an example when writing the factory, and it returns "Hello, World!"
    # The test checks that the response data matches.
    response = client.get('/hello')
    assert response.data == b'Hello, World!'