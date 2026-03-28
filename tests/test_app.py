from http import HTTPStatus

from fastapi.testclient import TestClient

from fastapi_zero.app import app


def test_root_deve_retornar_ola_mundo():
    """
    Esse teste tem 3 etapas (AAA)
    A - Arrange - arranjo
    A - Act     - Execura a coisa (o SUT)
    A - Assert  - Garante que A é A
    """
    # Arrange
    client = TestClient(app)
    # Act
    response = client.get('/')
    # Assert
    assert response.json() == {'message': 'Olá mundo!'}
    assert response.status_code == HTTPStatus.OK


def test_exercicio_aula_02():

    client = TestClient(app)

    response = client.get('/exercicio-html')

    assert '<h1> Olá Mundo </h1>' in response.text
    assert response.status_code == HTTPStatus.OK
