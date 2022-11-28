from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import Boolean
from sqlalchemy import Text
from sqlalchemy.orm import declarative_base, Session, relationship
from users import *
from equipment import *

Base = declarative_base()


class Accesses(Base):
    __tablename__ = "user_accesses"
    id = Column(Integer, primary_key=True)
    can_get_without_req = Column(Boolean)
    can_send_request = Column(Boolean)
    users = relationship("Users")


class AdminAccesses(Base):
    __tablename__ = "admin_accesses"
    id = Column(Integer, primary_key=True)
    can_get_without_req = Column(Boolean)
    can_send_request = Column(Boolean)
    can_insert = Column(Boolean)
    can_delete = Column(Boolean)
    can_change = Column(Boolean)
    can_get_request = Column(Boolean)
    power = Column(Integer)
    admins = relationship("Admins")

    def __repr__(self):
        return f"AdminAccess(id={self.id!r}, can_insert={self.can_insert!r}, can_delete={self.can_delete!r}," \
               f"can_change={self.can_change!r}, can_get_request={self.can_get_request!r})"


class Users(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    pass_number = Column(Integer)
    mail = Column(Text)
    access_id = Column(Integer, ForeignKey("user_accesses.id"))


class Admins(Base):
    __tablename__ = "admins"
    id = Column(Integer, primary_key=True)
    pass_number = Column(Integer)
    mail = Column(Text)
    password = Column(Text)
    access_id = Column(Integer, ForeignKey("admin_accesses.id"))

    def __repr__(self):
        return f"Admin(id={self.id!r}, mail={self.mail!r})"


class Equipments(Base):
    __tablename__ = "equipments"
    id = Column(Integer, primary_key=True)
    title = Column(Text)
    description = Column(Text)
    count = Column(Integer)
    reserve_count = Column(Integer)


class DataBase:

    def __init__(self, session: Session):
        self.__session = session

    def add_user(self, user: CommonUser):
        exist = self.__session.query(Users.id).filter(Users.mail == user.mail).first()
        if exist:
            raise Exception("This user already exists!")
        access = user.access
        access_id = self.__session.query(Accesses.id).filter(
            Accesses.can_send_request == access.can_send_req,
            Accesses.can_get_without_req == access.can_get_without_req
        ).first()
        if not access_id:
            db_access = Accesses(
                can_get_without_req=access.can_get_without_req,
                can_send_request=access.can_send_req
            )
            self.__session.add(db_access)
            self.__session.commit()
            access_id = self.__session.query(Accesses.id).filter(
                Accesses.can_send_request == access.can_send_req,
                Accesses.can_get_without_req == access.can_get_without_req
            ).one()
        db_user = Users(
            pass_number=user.id,
            mail=user.mail,
            access_id=access_id[0]
        )
        self.__session.add(db_user)
        self.__session.commit()

    def update_user(self, user: CommonUser):
        access = user.access
        access_id = self.__session.query(Accesses.id).filter(
            Accesses.can_send_request == access.can_send_req,
            Accesses.can_get_without_req == access.can_get_without_req
        ).first()
        if not access_id:
            db_access = Accesses(
                can_get_without_req=access.can_get_without_req,
                can_send_request=access.can_send_req
            )
            self.__session.add(db_access)
            self.__session.commit()
            access_id = self.__session.query(Accesses.id).filter(
                Accesses.can_send_request == access.can_send_req,
                Accesses.can_get_without_req == access.can_get_without_req
            ).one()
        self.__session.query(Users).filter(Users.mail == user.mail).update(
            {"pass_number": user.id, "mail": user.mail, "access_id": access_id[0]}
        )
        self.__session.commit()

    def delete_user(self, user: CommonUser):
        self.__session.query(Users).filter(Users.mail == user.mail).delete()
        self.__session.commit()

    def add_admin(self, admin: Admin):
        exist = self.__session.query(Admins.id).filter(Admins.mail == admin.mail).first()
        if exist:
            raise Exception("This admin already exists!")
        access = admin.access
        access_id = self.__session.query(AdminAccesses.id).filter(
            AdminAccesses.can_send_request == access.can_send_req,
            AdminAccesses.can_get_without_req == access.can_get_without_req,
            AdminAccesses.can_change == access.can_change,
            AdminAccesses.can_insert == access.can_insert,
            AdminAccesses.can_delete == access.can_delete,
            AdminAccesses.can_get_request == access.can_get_request,
            AdminAccesses.power == access.power
        ).first()
        if not access_id:
            db_access = AdminAccesses(
                can_get_without_req=access.can_get_without_req,
                can_send_request=access.can_send_req,
                can_insert=access.can_insert,
                can_delete=access.can_delete,
                can_change=access.can_change,
                can_get_request=access.can_get_request,
                power=access.power
            )
            self.__session.add(db_access)
            self.__session.commit()
            access_id = self.__session.query(AdminAccesses.id).filter(
                AdminAccesses.can_send_request == access.can_send_req,
                AdminAccesses.can_get_without_req == access.can_get_without_req,
                AdminAccesses.can_change == access.can_change,
                AdminAccesses.can_insert == access.can_insert,
                AdminAccesses.can_delete == access.can_delete,
                AdminAccesses.can_get_request == access.can_get_request,
                AdminAccesses.power == access.power
            ).one()
        db_admin = Admins(
            pass_number=admin.id,
            mail=admin.mail,
            password=admin.password,
            access_id=access_id[0]
        )
        self.__session.add(db_admin)
        self.__session.commit()

    def update_admin(self, admin: Admin):
        access = admin.access
        access_id = self.__session.query(AdminAccesses.id).filter(
            AdminAccesses.can_send_request == access.can_send_req,
            AdminAccesses.can_get_without_req == access.can_get_without_req,
            AdminAccesses.can_change == access.can_change,
            AdminAccesses.can_insert == access.can_insert,
            AdminAccesses.can_delete == access.can_delete,
            AdminAccesses.can_get_request == access.can_get_request,
            AdminAccesses.power == access.power
        ).first()
        if not access_id:
            db_access = AdminAccesses(
                can_get_without_req=access.can_get_without_req,
                can_send_request=access.can_send_req,
                can_insert=access.can_insert,
                can_delete=access.can_delete,
                can_change=access.can_change,
                can_get_request=access.can_get_request,
                power=access.power
            )
            self.__session.add(db_access)
            self.__session.commit()
            access_id = self.__session.query(AdminAccesses.id).filter(
                AdminAccesses.can_send_request == access.can_send_req,
                AdminAccesses.can_get_without_req == access.can_get_without_req,
                AdminAccesses.can_change == access.can_change,
                AdminAccesses.can_insert == access.can_insert,
                AdminAccesses.can_delete == access.can_delete,
                AdminAccesses.can_get_request == access.can_get_request,
                AdminAccesses.power == access.power
            ).one()
        self.__session.query(Admins).filter(Admins.mail == admin.mail).update(
            {"pass_number": admin.id, "mail": admin.mail, "password": admin.password, "access_id": access_id[0]}
        )
        self.__session.commit()

    def delete_admin(self, admin: Admin):
        self.__session.query(Admins).filter(Admins.mail == admin.mail).delete()
        self.__session.commit()

    def add_equipment(self, equipment: Equipment):
        exist = self.__session.query(Equipments.id).filter(Equipments.title == equipment.title).first()
        if exist:
            raise Exception("This equipment already exists!")
        db_equipment = Equipments(
            title=equipment.title,
            description=equipment.description,
            count=equipment.count,
            reserve_count=equipment.reserve_count
        )
        self.__session.add(db_equipment)
        self.__session.commit()

    def update_equipment(self, equipment: Equipment):
        self.__session.query(Equipments).filter(Equipments.title == equipment.title).update(
            {"title": equipment.title, "description": equipment.description,
             "count": equipment.count, "reserve_count": equipment.reserve_count}
        )

    def delete_equipment(self, equipment: Equipment):
        self.__session.query(Equipments).filter(Equipments.title == equipment.title).delete()
        self.__session.commit()