import sqlalchemy as sa
import sqlalchemy.orm as orm

from src.infrastructure.database import alchemy_config


class UserImage(alchemy_config.Base):
    __tablename__ = "db_user_images"

    id: orm.Mapped[int] = orm.mapped_column(sa.Integer, primary_key=True, index=True)
    image_path: orm.Mapped[str] = orm.mapped_column(sa.String)
    user_id: orm.Mapped[int] = orm.mapped_column(sa.ForeignKey("db_users.id", ondelete="CASCADE"))

    user = orm.relationship("User", back_populates="photos", uselist=False)
