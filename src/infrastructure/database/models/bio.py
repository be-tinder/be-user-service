import sqlalchemy as sa
import sqlalchemy.orm as orm

from src.domain import enums
from src.infrastructure.database import alchemy_config


class UserBio(alchemy_config.Base):
    __tablename__ = 'db_user_bios'

    id: orm.Mapped[int] = orm.mapped_column(sa.Integer, primary_key=True)
    bio: orm.Mapped[str] = orm.mapped_column(sa.String(500), nullable=True)
    height: orm.Mapped[int] = orm.mapped_column(sa.Integer, nullable=True)
    goals_relation: orm.Mapped[str] = orm.mapped_column(sa.Enum(enums.TinderPreference), nullable=True)
    languages: orm.Mapped[list] = orm.mapped_column(sa.ARRAY(sa.String), nullable=True)
    zodiac_sign: orm.Mapped[str] = orm.mapped_column(sa.Enum(enums.ZodiacSign, native_enum=False), nullable=True)
    education: orm.Mapped[str] = orm.mapped_column(sa.Enum(enums.Education, native_enum=False), nullable=True)
    children_preference: orm.Mapped[str] = orm.mapped_column(sa.Enum(enums.ChildrenPreference), nullable=True)

    user_id: orm.Mapped[int] = orm.mapped_column(sa.ForeignKey('db_users.id'), unique=True)

    user = orm.relationship('User', backref='user_bio')
