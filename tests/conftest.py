from contextlib import contextmanager
from datetime import datetime

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, event
from sqlalchemy.orm import Session

from fastapi_zero.app import app
from fastapi_zero.models import table_registry


@pytest.fixture
def client():
    # Arrange
    return TestClient(app)


@pytest.fixture
def session():
    # engine - cria ums conexão com o banco
    # sqlite - cria um banco em memória
    engine = create_engine('sqlite:///:memory:')

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
