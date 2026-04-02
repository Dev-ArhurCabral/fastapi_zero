from dataclasses import asdict

from sqlalchemy import select

from fastapi_zero.models import User


def test_create_user(session, mock_db_time):
    with mock_db_time(model=User) as time:
        new_user = User(
            username='Teste', email='teste@test.com', password='secreta'
        )
        # Com a session podemos fazer várias operações
        # depois fazer uma unica operação com o banco.
        # É um lugar transitivo entre o que ta acontecendo
        # no código e o que irá acontecer no banco
        session.add(new_user)
        session.commit()
        user = session.scalar(select(User).where(User.username == 'Teste'))
    assert asdict(user) == {
        'id': 1,
        'username': 'Teste',
        'email': 'teste@test.com',
        'password': 'secreta',
        'created_at': time,
    }
