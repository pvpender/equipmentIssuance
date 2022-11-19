from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import Boolean
from sqlalchemy import Text
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class AdminAccesses(Base):
    __tablename__ = "admin_accesses"
    id = Column(Integer, primary_key=True)
    can_insert = Column(Boolean)
    can_delete = Column(Boolean)
    can_change = Column(Boolean)
    can_get_request = Column(Boolean)
    admins = relationship("Admins")

    def __repr__(self):
        return f"AdminAccess(id={self.id!r}, can_insert={self.can_insert!r}, can_delete={self.can_delete!r}," \
               f"can_change={self.can_change!r}, can_get_request={self.can_get_request!r})"


class Admins(Base):
    __tablename__ = "admins"
    id = Column(Integer, primary_key=True)
    mail = Column(Text)
    access_id = Column(Integer, ForeignKey("admin_accesses.id"))

    def __repr__(self):
        return f"Admin(id={self.id!r}, mail={self.mail!r})"
