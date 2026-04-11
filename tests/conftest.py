from contextlib import contextmanager
from datetime import datetime

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, event
from sqlalchemy.orm import Session
from sqlalchemy.pool import StaticPool

from fastapi_zero.app import app
from fastapi_zero.database import get_session
from fastapi_zero.models import User, table_registry


# A injeção de dependência permite que sobrescrevamos a dependência
# na hora dos testes, na fixture client nos sobrescrevemos a get_session
# pela fixture session - onde criamos uma sessão em memória
@pytest.fixture
def client(session):
    def get_session_override():
        return session

    with TestClient(app) as client:
        app.dependency_overrides[get_session] = get_session_override
        yield client

    app.dependency_overrides.clear()


@pytest.fixture
def session():
    # engine - cria ums conexão com o banco
    # sqlite - cria um banco em memória
    engine = create_engine(
        'sqlite:///:memory:',
        # Não precisa verificar se é a mesma thread
        # Uma thread é uma “tarefa independênte”
        connect_args={'check_same_thread': False},
        poolclass=StaticPool,
    )

    # abaixo criamos a(as) tabela(s) no banco
    table_registry.metadata.create_all(engine)

    with Session(engine) as session:
        yield session

    # Limpamos o banco
    table_registry.metadata.drop_all(engine)


@contextmanager
# o * obriga a instância a nomear o parâmetro todos os parâmetros.
def __mock_db_time(*, model, time=datetime(2026, 4, 2)):
    def fake_time_hook(mapper, connection, target):
        # hasattr
        # serve para verificar se um objeto possui determinado atributo.
        if hasattr(target, 'created_at'):
            target.created_at = time
        if hasattr(target, 'updated_at'):
            target.updated_at = time

    event.listen(model, 'before_insert', fake_time_hook)
    yield time
    event.remove(model, 'before_insert', fake_time_hook)


@pytest.fixture
def mock_db_time():
    return __mock_db_time


@pytest.fixture
def user(session):
    user = User(
        username='Arthur', email='arthur@hotmail.com', password='secret'
    )
    session.add(user)
    session.commit()
    session.refresh(user)

    return user
