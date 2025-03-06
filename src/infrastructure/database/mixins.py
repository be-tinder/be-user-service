from datetime import datetime

import sqlalchemy as sa
import sqlalchemy.orm as orm


class TimeStampMixin:
    """Base class for time-stamp mixins."""
    create_date: orm.Mapped[datetime] = orm.mapped_column(sa.TIMESTAMP, default=datetime.utcnow)
    update_date: orm.Mapped[datetime] = orm.mapped_column(sa.TIMESTAMP, default=datetime.utcnow)
