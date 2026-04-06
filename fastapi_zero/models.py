from datetime import datetime

from sqlalchemy import func  # pega a hora do banco de dados
from sqlalchemy.orm import Mapped, mapped_column, registry

table_registry = registry()


@table_registry.mapped_as_dataclass()
class User:
    __tablename__ = 'users'

    # init=False
    # indica que não vamos passar a informação primary_key como argumento
    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    username: Mapped[str] = mapped_column(unique=True)
    email: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str]
    created_at: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now()
    )
    update_at: Mapped[datetime] = mapped_column(
        init=False, onupdate=func.now
    )
