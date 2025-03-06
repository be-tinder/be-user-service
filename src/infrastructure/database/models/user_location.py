import sqlalchemy as sa
import sqlalchemy.orm as orm

from src.infrastructure.database.alchemy_config import Base


class UserLocation(Base):
    __tablename__ = "user_location"

    id: orm.Mapped[int] = orm.mapped_column(sa.Integer, primary_key=True)
    latitude: orm.Mapped[float] = orm.mapped_column(sa.Float)
    longitude: orm.Mapped[float] = orm.mapped_column(sa.Float)
    user_id: orm.Mapped[int] = orm.mapped_column(sa.Integer)

    user = orm.relationship("User", back_populates="user_location", uselist=False)
