import sqlalchemy as sa
import sqlalchemy.orm as orm

from src.infrastructure.database import alchemy_config


class UserInterested(alchemy_config.Base):
    __tablename__ = 'db_user_interested'

    id: orm.Mapped[int] = orm.mapped_column(sa.INTEGER, primary_key=True)
    user_id: orm.Mapped[int] = orm.mapped_column(sa.ForeignKey('db_users.id', ondelete="CASCADE", onupdate="CASCADE"))
    interest_id: orm.Mapped[int] = orm.mapped_column(sa.ForeignKey('db_interests.id'))

    user = orm.relationship('User', back_populates='interests', uselist=False)

    __table_args__ = (
        sa.Index('ix_user_interested', 'user_id', 'interest_id', unique=True),
    )
