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
    response = client.get('/users/')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'users': [{'id': 1, 'email': 'alice@example.com', 'username': 'alice'}]
    }


def test_read_user_id(client):
    response = client.get('/user/1')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'id': 1,
        'email': 'alice@example.com',
        'username': 'alice',
    }


def test_read_user_id_should_return_not_found_(client):
    response = client.get('/user/999')
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'User NOT FOUND'}


def test_update_user(client):
    response = client.put(
        '/users/1',
        json={
            'username': 'Bob',
            'email': 'bob@example.com',
            'password': 'secret',
        },
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'username': 'Bob',
        'email': 'bob@example.com',
        'id': 1,
    }


def test_update_user_should_return_not_found_(client):
    response = client.put(
        '/users/999',
        json={
            'username': 'bob',
            'email': 'bob@example.com',
            'password': 'mynewpassword',
        },
    )
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'User NOT FOUND'}


def test_user_delete(client):
    response = client.delete('/users/1')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'username': 'Bob',
        'email': 'bob@example.com',
        'id': 1,
    }


def test_delete_user_should_return_not_found(client):
    response = client.delete('/users/666')
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'User NOT FOUND'}
