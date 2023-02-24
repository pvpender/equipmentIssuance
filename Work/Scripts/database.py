import datetime
from enum import Enum
from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import Integer, BigInteger
from sqlalchemy import Boolean
from sqlalchemy import Text, DateTime
from sqlalchemy.orm import declarative_base, Session, relationship
from users import *
from equipment import *
from sqlalchemy.exc import OperationalError
import request as req

Base = declarative_base()


class Accesses(Base):
    __tablename__ = "user_accesses"
    id = Column(Integer, primary_key=True)
    power = Column(Integer)
    users = relationship("Users")


class AdminAccesses(Base):
    __tablename__ = "admin_accesses"
    id = Column(Integer, primary_key=True)
    power = Column(Integer)
    can_add_users = Column(Boolean)
    can_change_users = Column(Boolean)
    can_add_inventory = Column(Boolean)
    can_change_inventory = Column(Boolean)
    can_get_request = Column(Boolean)
    admins = relationship("Admins")

    def __repr__(self):
        return f"AdminAccess(id={self.id!r}, can_insert={self.can_insert!r}, can_delete={self.can_delete!r}," \
               f"can_change={self.can_change!r}, can_get_request={self.can_get_request!r})"


class Users(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    pass_number = Column(BigInteger)
    mail = Column(Text)
    access_id = Column(Integer, ForeignKey("user_accesses.id"))


class Admins(Base):
    __tablename__ = "admins"
    id = Column(Integer, primary_key=True)
    pass_number = Column(BigInteger)
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
    access = Column(Integer)
    x = Column(Integer)
    y = Column(Integer)


class TelegramLogins(Base):
    __tablename__ = "telegram_logins"
    id = Column(Integer, primary_key=True)
    user_id = Column(BigInteger)
    mail = Column(Text)
    power = Column(Integer)


class LastRequest(Base):
    __tablename__ = "last_message"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    title = Column(Text)


class UserRequests(Base):
    __tablename__ = "user_requests"
    id = Column(Integer, primary_key=True)
    title = Column(Text)
    count = Column(Integer)
    purpose = Column(Text)
    sender_tg_id = Column(Integer)
    sender_mail = Column(Text)
    solved = Column(Boolean)
    approved = Column(Boolean)
    approved_id = Column(Integer)


class ActionTypes(Enum):
    INSERT = "insert"
    UPDATE = "update"
    DELETE = "delete"
    APPROVE = "approve"
    REJECT = "reject"


class WhatTypes(Enum):
    USER = "user"
    EQUIPMENT = "equipment"
    REQUEST = "request"


class Actions(Base):
    __tablename__ = "actions"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    action = Column(Text)
    what = Column(Text)
    what_id = Column(Text)
    action_time = Column(DateTime)


def restart_if_except(function):
    def check(*args, **kwargs):
        self = args[0]
        try:
            return function(*args, **kwargs)
        except OperationalError:
            self.session.rollback()
            return function(*args, **kwargs)

    return check


def for_all_methods(decorator):
    def decorate(cls):
        print(cls.__dict__)
        for attr in cls.__dict__:
            if callable(getattr(cls, attr)):
                setattr(cls, attr, decorator(getattr(cls, attr)))
        return cls

    return decorate


@for_all_methods(restart_if_except)
class DataBase:

    def __init__(self, session: Session):
        self.__session = session

    @property
    def session(self):
        return self.__session

    """@staticmethod
    def __restart_if_except(function):
        def check(*args, **kwargs):
            self = args[0]
            try:
                return function(*args, **kwargs)
            except OperationalError:
                self.__session.rollback()
                return function(*args, **kwargs)

        return check
        """

    def add_user(self, user: CommonUser):
        exist = self.__session.query(Users.id).filter(Users.mail == user.mail, Users.pass_number == user.id).first()
        if exist:
            raise ValueError("This user already exists!")
        access = user.access
        access_id = self.__session.query(Accesses.id).filter(
            Accesses.power == access.power,
        ).first()
        if not access_id:
            db_access = Accesses(
                power=access.power
            )
            self.__session.add(db_access)
            self.__session.commit()
            access_id = self.__session.query(Accesses.id).filter(
                Accesses.power == access.power
            ).one()
        db_user = Users(
            pass_number=user.id,
            mail=user.mail,
            access_id=access_id[0]
        )
        self.__session.add(db_user)
        self.__session.commit()

    def update_user(self, old_id: int, old_mail: str, user: CommonUser):
        access = user.access
        access_id = self.__session.query(Accesses.id).filter(
            Accesses.power == access.power
        ).first()
        if not access_id:
            db_access = Accesses(
                power=access.power
            )
            self.__session.add(db_access)
            self.__session.commit()
            access_id = self.__session.query(Accesses.id).filter(
                Accesses.power == access.power
            ).one()
        self.__session.query(Users).filter(Users.mail == old_mail, Users.pass_number == old_id).update(
            {"pass_number": user.id, "mail": user.mail, "access_id": access_id[0]}, synchronize_session=False
        )
        self.__session.commit()

    def delete_user(self, user: CommonUser):
        try:
            self.__session.query(Users).filter_by(mail=user.mail, pass_number=user.id).delete()
        except OperationalError:
            self.__session.rollback()
            self.__session.query(Users).filter_by(mail=user.mail, pass_number=user.id).delete()
        self.__session.commit()

    def get_user_by_id(self, pass_number: int):
        self.__session.commit()
        return self.__session.query(Users, Accesses).join(Accesses).filter(Users.pass_number == pass_number).first()

    def get_user_by_mail(self, mail: str):
        self.__session.commit()
        return self.__session.query(Users, Accesses).join(Accesses).filter(Users.mail == mail).first()

    def get_all_users(self):
        self.__session.commit()
        return self.__session.query(Users, Accesses).join(Accesses).all()

    def add_admin(self, admin: Admin):
        exist = self.__session.query(Admins.id).filter(Admins.mail == admin.mail,
                                                       Admins.pass_number == admin.id).first()
        if exist:
            raise ValueError("This admin already exists!")
        access = admin.access
        access_id = self.__session.query(AdminAccesses.id).filter(
            AdminAccesses.power == access.power,
            AdminAccesses.can_add_users == access.can_add_users,
            AdminAccesses.can_change_users == access.can_change_users,
            AdminAccesses.can_add_inventory == access.can_add_inventory,
            AdminAccesses.can_change_inventory == access.can_change_inventory,
            AdminAccesses.can_get_request == access.can_get_request,
        ).first()
        if not access_id:
            db_access = AdminAccesses(
                power=access.power,
                can_add_users=access.can_add_users,
                can_change_users=access.can_change_users,
                can_add_inventory=access.can_add_inventory,
                can_change_inventory=access.can_change_inventory,
                can_get_request=access.can_get_request,
            )
            self.__session.add(db_access)
            self.__session.commit()
            access_id = self.__session.query(AdminAccesses.id).filter(
                AdminAccesses.can_add_users == access.can_add_users,
                AdminAccesses.can_change_users == access.can_change_users,
                AdminAccesses.can_change_inventory == access.can_change_inventory,
                AdminAccesses.can_add_inventory == access.can_add_inventory,
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

    def update_admin(self, old_id: int, old_mail: str, admin: Admin):
        access = admin.access
        access_id = self.__session.query(AdminAccesses.id).filter(
            AdminAccesses.can_add_users == access.can_add_users,
            AdminAccesses.can_change_users == access.can_change_users,
            AdminAccesses.can_change_inventory == access.can_change_inventory,
            AdminAccesses.can_add_inventory == access.can_add_inventory,
            AdminAccesses.can_get_request == access.can_get_request,
            AdminAccesses.power == access.power
        ).first()
        if not access_id:
            db_access = AdminAccesses(
                can_add_users=access.can_add_users,
                can_change_users=access.can_change_users,
                can_add_inventory=access.can_add_inventory,
                can_change_inventory=access.can_change_inventory,
                can_get_request=access.can_get_request,
                power=access.power
            )
            self.__session.add(db_access)
            self.__session.commit()
            access_id = self.__session.query(AdminAccesses.id).filter(
                AdminAccesses.can_add_users == access.can_add_users,
                AdminAccesses.can_change_users == access.can_change_users,
                AdminAccesses.can_change_users == access.can_change_users,
                AdminAccesses.can_add_inventory == access.can_add_inventory,
                AdminAccesses.can_get_request == access.can_get_request,
                AdminAccesses.power == access.power
            ).one()
        self.__session.query(Admins).filter(Admins.mail == old_mail, Admins.pass_number == old_id).update(
            {"pass_number": admin.id, "mail": admin.mail, "password": admin.password, "access_id": access_id[0]},
            synchronize_session=False
        )
        self.__session.commit()

    def delete_admin(self, admin: Admin):
        self.__session.query(Admins).filter(Admins.mail == admin.mail, Admins.pass_number == admin.id).delete()
        self.__session.commit()

    def get_admin_by_id(self, pass_number: int):
        self.__session.commit()
        return self.__session.query(Admins, AdminAccesses).join(AdminAccesses).filter(
            Admins.pass_number == pass_number).first()

    def get_admin_by_mail(self, mail: str):
        self.__session.commit()
        return self.__session.query(Admins, AdminAccesses).join(AdminAccesses).filter(Admins.mail == mail).first()

    def get_all_admins(self):
        self.__session.commit()
        return self.__session.query(Admins, AdminAccesses).join(AdminAccesses).all()

    def add_equipment(self, equipment: Equipment):
        exist = self.__session.query(Equipments.id).filter(Equipments.title == equipment.title).first()
        if exist:
            raise ValueError("This equipment already exists!")
        db_equipment = Equipments(
            title=equipment.title,
            description=equipment.description,
            count=equipment.count,
            reserve_count=equipment.reserve_count,
            access=equipment.access,
            x=equipment.x,
            y=equipment.y
        )
        self.__session.add(db_equipment)
        self.__session.commit()
        equipment.id = self.get_equipment_by_title(equipment.title).id

    def update_equipment(self, old_id: int, equipment: Equipment):
        if not (equipment.x and equipment.y):
            exist = self.__session.query(Equipments).filter(
                Equipments.x == equipment.x, Equipments.y == equipment.y
            ).first()
            if exist:
                raise ValueError("This cell is occupied!")
        self.__session.query(Equipments).filter(Equipments.id == old_id).update(
            {"title": equipment.title, "description": equipment.description,
             "count": equipment.count, "reserve_count": equipment.reserve_count,
             "access": equipment.access, "x": equipment.x, "y": equipment.y}, synchronize_session=False
        )

    def delete_equipment(self, equipment: Equipment):
        self.__session.query(Equipments).filter(Equipments.title == equipment.title).delete()
        self.__session.commit()

    def get_equipment_by_title(self, title: str):
        self.__session.commit()
        return self.__session.query(Equipments).filter(Equipments.title == title).first()

    def get_all_equipment(self):
        self.__session.commit()
        return self.__session.query(Equipments).all()

    def get_equipment_by_coordinates(self, x: int, y: int):
        self.__session.commit()
        if x != -1 and y != -1:
            return self.__session.query(Equipments).filter(Equipments.x == x, Equipments.y == y).first()
        else:
            return None

    def get_equipment_by_id(self, eq_id: int):
        self.__session.commit()
        return self.__session.query(Equipments).filter(Equipments.id == eq_id).first()

    def get_tg_user(self, user_id):
        self.__session.commit()
        return self.__session.query(TelegramLogins).filter(TelegramLogins.user_id == user_id).first()

    def add_tg_user(self, user_id, mail, power):
        db_user = TelegramLogins(
            user_id=user_id,
            mail=mail,
            power=power
        )
        if not self.get_tg_user(user_id):
            self.__session.add(db_user)
        else:
            self.__session.query(TelegramLogins).filter(TelegramLogins.user_id == user_id).update(
                {"mail": mail, "power": power}, synchronize_session=False
            )
        self.__session.commit()

    def add_request(self, request: req.Request):
        db_request = UserRequests(
            sender_tg_id=request.sender_tg_id,
            sender_mail=request.sender_mail,
            title=request.what,
            count=request.count,
            purpose=request.purpose,
            solved=False
        )
        eq = self.get_equipment_by_title(request.what)
        eq.reserve_count += 1
        self.update_equipment(eq.id, eq)
        self.__session.add(db_request)
        self.__session.commit()

    def get_all_requests(self):
        self.__session.commit()
        return self.__session.query(UserRequests).all()

    def get_solved_requests(self):
        self.__session.commit()
        return self.__session.query(UserRequests).filter(UserRequests.solved is True).all()

    def get_unsolved_requests(self):
        self.__session.commit()
        return self.__session.query(UserRequests).filter((UserRequests.solved is False) or
                                                         (UserRequests.solved.is_(None))).all()

    def get_first_unsolved_request(self):
        self.__session.commit()
        return self.__session.query(UserRequests).filter((UserRequests.solved is False) or
                                                         (UserRequests.solved.is_(None))).first()

    def add_last_request(self, user_id: int, title: str, description: str):
        self.__session.query(LastRequest).filter(LastRequest.user_id == user_id).delete()
        last_request = LastRequest(
            user_id=user_id,
            title=title,
        )
        self.__session.add(last_request)
        self.__session.commit()

    def get_last_request(self, user_id):
        self.__session.commit()
        return self.__session.query(LastRequest).filter(LastRequest.user_id == user_id).first()

    def update_request(self, request: UserRequests):
        self.__session.query(UserRequests).filter(UserRequests.sender_tg_id == request.sender_tg_id,
                                                  UserRequests.title == request.title,
                                                  UserRequests.solved is False).update(
            {
                "solved": True,
                "approved": request.approved,
                "approved_id": request.approved_id
            }, synchronize_session=False)

    def add_action(self, user_mail_or_id: str | int, action: ActionTypes, what: WhatTypes, what_id: str | int):
        if isinstance(user_mail_or_id, str):
            user = self.get_user_by_mail(user_mail_or_id)
            user = self.get_admin_by_mail(user_mail_or_id) if not user else user
            user_mail_or_id = user[0].id
        new_action = Actions(
            user_id=user_mail_or_id,
            action=action,
            what=what,
            what_id=what_id,
            action_time=datetime.datetime.now()
        )
        self.__session.add(new_action)
        self.__session.commit()

    def get_all_actions(self):
        return self.__session.query(Actions).all()

