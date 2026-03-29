from http import HTTPStatus


def test_root_deve_retornar_ola_mundo(client):
    # Arrange
    # Act
    response = client.get('/')
    # Assert
    assert response.json() == {'message': 'Olá mundo!'}
    assert response.status_code == HTTPStatus.OK


def test_creat_user(client):
    response = client.post(
        '/users/',
        json={
            'username': 'alice',
            'email': 'alice@example.com',
            'password': 'secret',
        },
    )
    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        'id': 1,
        'email': 'alice@example.com',
        'username': 'alice',
    }


def test_read_users(client):
    resource = client.get('/users/')
    assert resource.status_code == HTTPStatus.OK
    assert resource.json() == {
        'users': [{'id': 1, 'email': 'alice@example.com', 'username': 'alice'}]
    }


def test_updateuser(client):
    resource = client.put(
        '/users/1',
        json={
            'username': 'Bob',
            'email': 'bob@example.com',
            'password': 'secret',
        },
    )
    assert resource.status_code == HTTPStatus.OK
    assert resource.json() == {
        'username': 'Bob',
        'email': 'bob@example.com',
        'id': 1,
    }


def test_user_delete(client):
    resource = client.delete('/users/1')
    assert resource.status_code == HTTPStatus.OK
    assert resource.json() == {
        'username': 'Bob',
        'email': 'bob@example.com',
        'id': 1,
    }
