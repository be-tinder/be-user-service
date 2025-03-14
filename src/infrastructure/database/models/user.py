from datetime import datetime

import sqlalchemy as sa
import sqlalchemy.orm as orm

from src.domain import enums
from src.infrastructure.database import alchemy_config
from src.infrastructure.database import mixins


class User(alchemy_config.Base, mixins.TimeStampMixin):
    __tablename__ = 'db_users'

    id: orm.Mapped[int] = orm.mapped_column(sa.Integer, primary_key=True)
    name: orm.Mapped[str] = orm.mapped_column(sa.String, nullable=True)
    phone_number: orm.Mapped[str] = orm.mapped_column(sa.String, unique=True, index=True)
    gender: orm.Mapped[str] = orm.mapped_column(
        sa.Enum(
            enums.Gender,
            native_enum=False
        ),
        default=enums.Gender.NOT_SPECIFIED,
        index=True
    )
    sexual_orientation: orm.Mapped[str] = orm.mapped_column(sa.String, nullable=True, index=True)
    birth_date: orm.Mapped[datetime.date] = orm.mapped_column(sa.Date, nullable=True)

    interests = orm.relationship("UserInterested", back_populates="user", uselist=True)
    photos = orm.relationship("UserImage", back_populates="user")
    user_location = orm.relationship("UserLocation", back_populates="user", uselist=False)
