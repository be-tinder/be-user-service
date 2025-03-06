import sqlalchemy as sa
import sqlalchemy.orm as orm

from src.infrastructure.database import alchemy_config


class Interest(alchemy_config.Base):
    __tablename__ = "db_interests"

    id: orm.Mapped[int] = orm.mapped_column(sa.Integer, primary_key=True, index=True)
    name: orm.Mapped[str] = orm.mapped_column(sa.String, unique=True, index=True)
