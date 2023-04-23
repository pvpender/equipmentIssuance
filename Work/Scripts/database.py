import datetime
from enum import Enum
from typing import List
from PyQt6.QtWidgets import QMessageBox
from sqlalchemy import ForeignKey
from sqlalchemy import BigInteger
from sqlalchemy import Text, DateTime, Engine, create_engine
from sqlalchemy.orm import DeclarativeBase, Session, relationship, Mapped, mapped_column
from users import *
from equipment import *
from sqlalchemy.exc import OperationalError, IntegrityError
import request as req
import time
import threading


def show_message(title: str, info: str):
    msg_box = QMessageBox()
    msg_box.setText(info)
    msg_box.setWindowTitle(title)
    msg_box.exec()


def fix_died_connection(a: Session):
    try:
        a.close()
    except OperationalError:
        a.rollback()
        a.close()
    return


class Base(DeclarativeBase):
    pass


class Groups(Base):
    __tablename__ = "groups"
    id: Mapped[int] = mapped_column(primary_key=True)
    group_name: Mapped[str] = mapped_column(Text)


class UserGroups(Base):
    __tablename__ = "user_groups"
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete='CASCADE'))
    group_id: Mapped[int] = mapped_column(ForeignKey("groups.id", ondelete='CASCADE'))
    group: Mapped["Groups"] = relationship()
    user: Mapped["Users"] = relationship()


"""class AdminGroups(Base):
    __tablename__ = "admin_groups"
    id: Mapped[int] = mapped_column(primary_key=True)
    admin_id: Mapped[int] = mapped_column(ForeignKey("admins.id", ondelete='CASCADE'))
    group_id: Mapped[int] = mapped_column(ForeignKey("groups.id", ondelete='CASCADE'))
    group: Mapped["Groups"] = relationship()
    admin: Mapped["Admins"] = relationship()"""


class EquipmentGroups(Base):
    __tablename__ = "equipment_groups"
    id: Mapped[int] = mapped_column(primary_key=True)
    equipment_id: Mapped[int] = mapped_column(ForeignKey("equipments.id", ondelete='CASCADE'))
    group_id: Mapped[int] = mapped_column(ForeignKey("groups.id", ondelete='CASCADE'))
    group: Mapped["Groups"] = relationship()
    equipment: Mapped["Equipments"] = relationship()


class AdminAccesses(Base):
    __tablename__ = "admin_accesses"
    id: Mapped[int] = mapped_column(primary_key=True)
    can_add_users: Mapped[bool]
    can_change_users: Mapped[bool]
    can_add_inventory: Mapped[bool]
    can_change_inventory: Mapped[bool]
    can_get_request: Mapped[bool]
    admins: Mapped[List["Admins"]] = relationship()


class Users(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    pass_number: Mapped[int] = mapped_column(BigInteger)
    mail: Mapped[str] = mapped_column(Text)
    user_groups: Mapped[List["UserGroups"]] = relationship(back_populates="user", cascade="save-update, delete")


"""class Admins(Base):
    __tablename__ = "admins"
    id: Mapped[int] = mapped_column(primary_key=True)
    pass_number: Mapped[int] = mapped_column(BigInteger)
    mail: Mapped[str] = mapped_column(Text)
    access_id: Mapped[int] = mapped_column(ForeignKey("admin_accesses.id"))
    access: Mapped["AdminAccesses"] = relationship(back_populates="admins")
    admin_groups: Mapped[List["AdminGroups"]] = relationship(back_populates="admin")"""


class Admins(Base):
    __tablename__ = "admins"
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), primary_key=True,
                                         autoincrement=False)
    access_id: Mapped[int] = mapped_column(ForeignKey("admin_accesses.id"))
    access: Mapped["AdminAccesses"] = relationship(back_populates="admins")
    user: Mapped["Users"] = relationship()


class Logins(Base):
    __tablename__ = "logins"
    id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete='CASCADE'), primary_key=True, autoincrement=False)
    login: Mapped[str] = mapped_column(Text)
    password: Mapped[str] = mapped_column(Text)


"""class AdminLogins(Base):
    __tablename__ = "admin_logins"
    id: Mapped[int] = mapped_column(ForeignKey("admins.id", ondelete='CASCADE'), primary_key=True, autoincrement=False)
    login: Mapped[str] = mapped_column(Text)
    password: Mapped[str] = mapped_column(Text)"""


class Equipments(Base):
    __tablename__ = "equipments"
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(Text)
    description: Mapped[str] = mapped_column(Text)
    count: Mapped[int]
    reserve_count: Mapped[int]
    x: Mapped[int]
    y: Mapped[int]
    equipment_groups: Mapped[List["EquipmentGroups"]] = relationship(back_populates="equipment")


class TelegramLogins(Base):
    __tablename__ = "telegram_logins"
    id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete='CASCADE'), primary_key=True, autoincrement=False)
    tg_id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=False)
    user: Mapped[List["Users"]] = relationship()


"""class TelegramAdminLogins(Base):
    __tablename__ = "telegram_admin_logins"
    id: Mapped[int] = mapped_column(ForeignKey("admins.id", ondelete='CASCADE'), primary_key=True, autoincrement=False)
    tg_id: Mapped[int] = mapped_column(BigInteger)
    admin: Mapped[List["Admins"]] = relationship()"""


class LastRequest(Base):
    __tablename__ = "last_message"
    tg_id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=False)
    title: Mapped[str] = mapped_column(Text)


class LastLogin(Base):
    __tablename__ = "last_login"
    tg_id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=False)
    login: Mapped[str] = mapped_column(Text)


class UserRequests(Base):
    __tablename__ = "user_requests"
    id: Mapped[int] = mapped_column(primary_key=True)
    equipment_id: Mapped[int] = mapped_column(ForeignKey("equipments.id", ondelete='CASCADE'))
    count: Mapped[int] = mapped_column(default=1)
    purpose: Mapped[str] = mapped_column(Text)
    sender_tg_id: Mapped[int] = mapped_column(BigInteger)
    sender_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete='CASCADE'))
    solved: Mapped[bool] = mapped_column(default=False)
    approved: Mapped[bool] = mapped_column(nullable=True)
    approved_id: Mapped[int] = mapped_column(nullable=True)
    notified: Mapped[bool] = mapped_column(default=False)
    taken: Mapped[bool] = mapped_column(default=False)


"""class AdminRequests(Base):
    __tablename__ = "admin_requests"
    id: Mapped[int] = mapped_column(primary_key=True)
    equipment_id: Mapped[int]
    count: Mapped[int] = mapped_column(default=1)
    purpose: Mapped[str] = mapped_column(Text)
    sender_tg_id: Mapped[int] = mapped_column(BigInteger)
    sender_id: Mapped[int]
    taken: Mapped[bool] = mapped_column(default=False)"""

"""class Actions(Base):    # trash
    __tablename__ = "actions"
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int]
    action: Mapped[str] = mapped_column(Text)
    what: Mapped[str] = mapped_column(Text)
    users_row_id: Mapped[int] = mapped_column(ForeignKey("users_backup.id"))
    admins_row_id: Mapped[int] = mapped_column(ForeignKey("admins_backup.id"))
    equipments_row_id: Mapped[int] = mapped_column(ForeignKey("equipments_backup.id"))
    action_time: Mapped[datetime.datetime] = mapped_column(DateTime)"""


class UsersBackUp(Base):
    __tablename__ = "users_backup"
    id: Mapped[int] = mapped_column(primary_key=True)
    user: Mapped[int]
    action: Mapped[str] = mapped_column(Text)
    action_time: Mapped[datetime.datetime] = mapped_column(DateTime)
    id_in_table: Mapped[int]
    pass_number: Mapped[int] = mapped_column(BigInteger)
    mail: Mapped[str] = mapped_column(Text)


"""class AdminsBackUp(Base):
    __tablename__ = "admins_backup"
    id: Mapped[int] = mapped_column(primary_key=True)
    user: Mapped[int]
    action: Mapped[str] = mapped_column(Text)
    action_time: Mapped[datetime.datetime] = mapped_column(DateTime)
    id_in_table: Mapped[int]
    pass_number: Mapped[int] = mapped_column(BigInteger)
    mail: Mapped[str] = mapped_column(Text)
    access_id: Mapped[int]"""


class AdminBackUp(Base):
    __tablename__ = "admins_backup"
    id: Mapped[int] = mapped_column(primary_key=True)
    user: Mapped[int]
    action: Mapped[str] = mapped_column(Text)
    action_time: Mapped[datetime.datetime] = mapped_column(DateTime)
    id_in_table: Mapped[int]
    access_id: Mapped[int]


class EquipmentBackUp(Base):
    __tablename__ = "equipments_backup"
    id: Mapped[int] = mapped_column(primary_key=True)
    user: Mapped[int]
    action: Mapped[str] = mapped_column(Text)
    action_time: Mapped[datetime.datetime] = mapped_column(DateTime)
    id_in_table: Mapped[int]
    title: Mapped[str] = mapped_column(Text)
    description: Mapped[str] = mapped_column(Text)
    count: Mapped[int]
    reserve_count: Mapped[int]
    x: Mapped[int]
    y: Mapped[int]


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


def restart_if_except(function):
    """
    Decorator for reconnecting
    :param function:
    :return:
    """

    def check(*args, **kwargs):
        self = args[0]
        if (time.time() - self.last_db_access_time) > 200:
            t = threading.Thread(target=fix_died_connection, args=(self.session,))
            t.start()
            self.session = Session(create_engine(f"mysql+pymysql://admin:testPass@194.67.206.233:3306/test_base"))
        self.last_db_access_time = time.time()
        try:
            self.session.commit()
            return function(*args, **kwargs)
        except OperationalError as oe:
            print(oe)
            self.session.rollback()
            return function(*args, **kwargs)

    return check


def for_all_methods(decorator):
    """
    Decorate all class methods
    :param decorator:
    :return:
    """

    def decorate(cls):
        print(cls.__dict__)
        for attr in cls.__dict__:
            if callable(getattr(cls, attr)) and attr != '__init__':
                setattr(cls, attr, decorator(getattr(cls, attr)))
        return cls

    return decorate


@for_all_methods(restart_if_except)
class DataBase:
    """Class for working with database"""

    def __init__(self, engine: Engine):
        self.__engine = engine
        self.__session = Session(engine)
        self.__last_db_access_time = time.time()

    @property
    def last_db_access_time(self) -> float:
        return self.__last_db_access_time

    @last_db_access_time.setter
    def last_db_access_time(self, new_time: float):
        self.__last_db_access_time = new_time

    @property
    def session(self) -> Session:
        """
        Get current session
        :return: session
        """
        return self.__session

    @session.setter
    def session(self, new_session: Session):
        self.__session = new_session

    def add_group(self, group_name: str):
        """
        Add new group to base
        :param group_name: str
        :return: None
        """
        self.__session.add(Groups(group_name=group_name))
        self.__session.commit()

    def rename_group(self, group_id: int, new_name: str):
        self.__session.query(Groups).filter(Groups.id == group_id).update(
            {"group_name": new_name}
        )
        self.__session.commit()

    def del_group(self, group_id: int):
        self.__session.query(Groups).filter(Groups.id == group_id).delete()
        self.__session.commit()

    def get_all_groups(self) -> list:
        return self.__session.query(Groups).all()

    def get_group_by_id(self, group_id: int):
        return self.__session.query(Groups).filter(Groups.id == group_id).first()

    def get_group_by_name(self, group_name: str):
        return self.__session.query(Groups).filter(Groups.group_name == group_name).first()

    def add_user_group(self, user_id: int, group_id: int):
        self.__session.add(UserGroups(user_id=user_id, group_id=group_id))
        self.__session.commit()

    def del_user_group(self, user_id, groups: list):
        self.__session.query(UserGroups).filter(UserGroups.group_id.in_(groups), UserGroups.user_id == user_id).delete()

    def add_equipment_group(self, equipment_id: int, group_id: int):
        self.__session.add(EquipmentGroups(equipment_id=equipment_id, group_id=group_id))
        self.__session.commit()

    def del_equipment_group(self, equipment_id: int, groups: list):
        self.__session.query(EquipmentGroups).filter(
            EquipmentGroups.group_id.in_(groups),
            EquipmentGroups.equipment_id == equipment_id
        ).delete()
        self.__session.commit()

    def change_user(self, login: str, password: str):
        self.__session.close_all()
        self.__engine.dispose()
        # self.__engine = create_engine(f"mysql+pymysql://developer:deVpass@194.67.206.233:3306/dev_base")
        self.__engine = create_engine(f"mysql+pymysql://admin:testPass@194.67.206.233:3306/test_base")
        # self.__session.close()
        self.__session = Session(self.__engine)

    def add_user(self, user: CommonUser):
        exist = self.__session.query(Users.id).filter(
            Users.mail == user.mail,
            Users.pass_number == user.pass_number
        ).first()
        if exist:
            raise ValueError("This user already exists!")
        db_user = Users(
            pass_number=user.pass_number,
            mail=user.mail,
        )
        self.__session.add(db_user)
        self.__session.commit()
        user_id = self.get_user_by_mail(user.mail).id
        for i in user.access.groups:
            try:
                self.add_user_group(user_id, i)
            except IntegrityError:
                pass
        self.__session.commit()

    def update_user(self, old_id: int, old_mail: str, user: CommonUser):
        self.__session.query(UserGroups).filter(
            UserGroups.user_id == user.base_id,
            UserGroups.group_id.notin_(user.access.groups)
        ).delete()
        exists = list(map(list, zip(*self.__session.query(UserGroups.group_id).filter(
            UserGroups.user_id == user.base_id).all())))
        if exists:
            exists = exists[0]
        try:
            for i in user.access.groups:
                if i not in exists:
                    self.__session.add(UserGroups(user_id=user.base_id, group_id=i))
            self.__session.query(Users).filter(Users.mail == old_mail, Users.pass_number == old_id).update(
                {"pass_number": user.pass_number, "mail": user.mail}, synchronize_session=False
            )
            self.__session.commit()
        except IntegrityError:
            show_message("Ошибка синхронизации", "Обновите пользователей и оборудование!")
            self.__session.rollback()

    def delete_user(self, user: CommonUser):
        try:
            self.__session.query(Users).filter_by(mail=user.mail, pass_number=user.pass_number).delete()
        except OperationalError:
            self.__session.rollback()
            self.__session.query(Users).filter_by(mail=user.mail, pass_number=user.pass_number).delete()
        self.__session.commit()

    def get_user_by_id(self, pass_number: int):
        return self.__session.query(Users).filter(Users.pass_number == pass_number).first()

    def get_user_by_mail(self, mail: str) -> Union[Users, None]:
        return self.__session.query(Users).filter(Users.mail == mail).first()

    def get_all_users(self) -> List[Type[Users]]:
        return self.__session.query(Users).all()

    def add_user_login(self, user_id, login: str, password: str):
        self.__session.add(Logins(id=user_id, login=login, password=password))

    def get_user_login(self, login: str) -> Union[Logins, None]:
        return self.__session.query(Logins).filter(Logins.login == login).first()

    def add_admin(self, admin: Admin):
        exist = self.__session.query(Users.id).filter(Users.mail == admin.mail,
                                                      Users.pass_number == admin.pass_number).first()
        if exist:
            raise ValueError("This admin already exists!")
        access = admin.access
        access_id = self.__session.query(AdminAccesses.id).filter(
            AdminAccesses.can_add_users == access.can_add_users,
            AdminAccesses.can_change_users == access.can_change_users,
            AdminAccesses.can_add_inventory == access.can_add_inventory,
            AdminAccesses.can_change_inventory == access.can_change_inventory,
            AdminAccesses.can_get_request == access.can_get_request,
        ).first()
        if not access_id:
            db_access = AdminAccesses(
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
            ).one()
        self.add_user(CommonUser(admin.pass_number, admin.mail, Access(admin.access.groups)))
        user_id = self.__session.query(Users.id).filter(Users.mail == admin.mail,
                                                        Users.pass_number == admin.pass_number).one()
        db_admin = Admins(
            user_id=user_id[0],
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
        ).first()
        if not access_id:
            db_access = AdminAccesses(
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
                AdminAccesses.can_change_users == access.can_change_users,
                AdminAccesses.can_add_inventory == access.can_add_inventory,
                AdminAccesses.can_get_request == access.can_get_request,
            ).one()
        self.__session.query(UserGroups).filter(
            UserGroups.user_id == admin.base_id,
            UserGroups.group_id.notin_(admin.access.groups)
        ).delete()
        exists = list(map(
            list,
            zip(*self.__session.query(UserGroups.group_id).filter(UserGroups.user_id == admin.base_id).all())
        ))
        if exists:
            exists = exists[0]
        try:
            for i in admin.access.groups:
                    if i not in exists:
                        self.__session.add(UserGroups(user_id=admin.base_id, group_id=i))
            else:
                self.__session.query(Users).filter(Users.mail == old_mail, Users.pass_number == old_id).update(
                    {"pass_number": admin.pass_number, "mail": admin.mail},
                    synchronize_session=False
                )
                self.__session.query(Admins).filter(Admins.user_id == admin.base_id).update(
                    {"access_id": access_id[0]}
                )
                self.__session.commit()
        except IntegrityError:
            show_message("Ошибка синхронизации", "Обновите группы и пользователей")
            self.__session.rollback()

    def delete_admin(self, admin: Admin):
        self.__session.query(Users).filter(Users.id == admin.base_id).delete()
        self.__session.commit()

    def get_admin_by_id(self, pass_number: int):
        return self.__session.query(Admins).join(Users).filter(Users.pass_number == pass_number).first()

    def get_admin_by_mail(self, mail: str) -> Union[Admins, None]:
        return self.__session.query(Admins).join(Users).filter(Users.mail == mail).first()

    def get_all_admins(self):
        return self.__session.query(Admins).all()

    def add_equipment(self, equipment: Equipment):
        exist = self.__session.query(Equipments.id).filter(Equipments.title == equipment.title).first()
        if exist:
            raise ValueError("This equipment already exists!")
        db_equipment = Equipments(
            title=equipment.title,
            description=equipment.description,
            count=equipment.count,
            reserve_count=equipment.reserve_count,
            x=equipment.x,
            y=equipment.y
        )
        self.__session.add(db_equipment)
        self.__session.commit()
        equipment_id = self.get_equipment_by_title(equipment.title).id
        for i in equipment.groups:
            try:
                self.add_equipment_group(equipment_id=equipment_id, group_id=i)
            except IntegrityError:
                pass

    def update_equipment(self, equipment: Union[Equipment, Equipments]):
        if not (equipment.x and equipment.y):
            exist = self.__session.query(Equipments).filter(
                Equipments.x == equipment.x, Equipments.y == equipment.y
            ).first()
            if exist:
                raise ValueError("This cell is occupied!")
        if isinstance(equipment, Equipment):
            self.__session.query(EquipmentGroups).filter(
                EquipmentGroups.equipment_id == equipment.id,
                EquipmentGroups.group_id.notin_(equipment.groups)
            ).delete()
            exist_groups = list(map(list, zip(*self.__session.query(EquipmentGroups.group_id).filter(
                EquipmentGroups.equipment_id == equipment.id
            ).all())))
            if exist_groups:
                exist_groups = exist_groups[0]
            for i in equipment.groups:
                if i not in exist_groups:
                    self.__session.add(EquipmentGroups(equipment_id=equipment.id, group_id=i))
        try:
            self.__session.query(Equipments).filter(Equipments.id == equipment.id).update(
                {"title": equipment.title, "description": equipment.description,
                 "count": equipment.count, "reserve_count": equipment.reserve_count,
                 "x": equipment.x, "y": equipment.y}, synchronize_session=False
            )
            self.__session.commit()
        except IntegrityError:
            show_message("Ошибка синхронизации", "Обновите группы и оборудование")
            self.__session.rollback()

    def delete_equipment(self, equipment: Equipment):
        self.__session.query(Equipments).filter(Equipments.title == equipment.title).delete()
        self.__session.commit()

    def get_equipment_by_id(self, eq_id: int):
        return self.__session.query(Equipments).filter(Equipments.id == eq_id).first()

    def get_equipment_by_title(self, title: str) -> Union[Equipments, None]:
        return self.__session.query(Equipments).filter(Equipments.title == title).first()

    def get_equipments_by_group(self, group_id: int) -> list:
        return self.__session.query(EquipmentGroups).filter(EquipmentGroups.group_id == group_id).all()

    def get_all_equipment(self):
        return self.__session.query(Equipments).all()

    def get_equipment_by_coordinates(self, x: int, y: int):
        if x != -1 and y != -1:
            return self.__session.query(Equipments).filter(Equipments.x == x, Equipments.y == y).first()
        else:
            return None

    def get_tg_user(self, tg_id) -> Union[TelegramLogins, None]:
        return self.__session.query(TelegramLogins).filter(TelegramLogins.tg_id == tg_id).first()

    def add_tg_user(self, tg_id: int, user_id: int):
        if self.get_tg_user(tg_id):
            self.__session.query(TelegramLogins).filter(TelegramLogins.tg_id == tg_id).update(
                {"id": user_id}
            )
        else:
            self.__session.add(TelegramLogins(id=user_id, tg_id=tg_id))
        self.__session.commit()

    def add_user_request(self, request: req.Request):
        db_request = UserRequests(
            sender_tg_id=request.sender_tg_id,
            sender_id=request.sender_id,
            equipment_id=request.equipment_id,
            count=request.count,
            purpose=request.purpose,
            solved=False
        )
        eq = self.get_equipment_by_id(request.equipment_id)
        eq.reserve_count += 1
        if isinstance(eq, Union[Equipments, Equipments]):
            self.update_equipment(eq)
        self.__session.add(db_request)
        self.__session.commit()

    def add_admin_request(self, request: req.Request):
        db_request = UserRequests(
            sender_tg_id=request.sender_tg_id,
            sender_id=request.sender_id,
            equipment_id=request.equipment_id,
            count=request.count,
            purpose=request.purpose,
            solved=True,
            approved=True,
            notified=True
        )
        eq = self.get_equipment_by_id(request.equipment_id)
        eq.reserve_count += 1
        if isinstance(eq, Union[Equipments, Equipments]):
            self.update_equipment(eq)
        self.__session.add(db_request)
        self.__session.commit()

    def get_all_users_requests(self):
        return self.__session.query(UserRequests).all()

    def get_solved_users_requests(self) -> List[Type[UserRequests]]:
        return self.__session.query(UserRequests).filter(UserRequests.solved.is_(True)).all()

    def get_solved_unannounced_users_request(self) -> List[Type[UserRequests]]:
        return self.__session.query(UserRequests).filter(
            UserRequests.solved.is_(True),
            UserRequests.notified.is_(False)
        ).all()

    def get_unsolved_users_requests(self) -> Union[List[Type[UserRequests]]]:
        return self.__session.query(UserRequests).filter(UserRequests.solved.is_(False)).all()

    def get_first_unsolved_users_request(self) -> Union[Type[UserRequests], None]:
        return self.__session.query(UserRequests).filter((UserRequests.solved is False) or
                                                         (UserRequests.solved.is_(None))).first()

    def add_last_request(self, tg_id: int, title: str):
        self.__session.query(LastRequest).filter(LastRequest.tg_id == tg_id).delete()
        last_request = LastRequest(
            tg_id=tg_id,
            title=title,
        )
        self.__session.add(last_request)
        self.__session.commit()

    def get_last_request(self, tg_id) -> Union[UserRequests, None]:
        return self.__session.query(LastRequest).filter(LastRequest.tg_id == tg_id).first()

    def add_last_login(self, tg_id: int, login: str):
        self.__session.query(LastLogin).filter(LastLogin.tg_id == tg_id).delete()
        self.__session.add(LastLogin(
            tg_id=tg_id,
            login=login
        ))
        self.__session.commit()

    def get_last_login(self, tg_id) -> Type[LastLogin]:
        return self.__session.query(LastLogin).filter(LastLogin.tg_id == tg_id).first()

    def get_user_request(self, request_id: int) -> Union[UserRequests, None]:
        return self.__session.query(UserRequests).filter(UserRequests.id == request_id).first()

    def update_user_request(self, request: Union[Type[UserRequests]]):
        self.__session.query(UserRequests).filter(UserRequests.id == request.id).update(
            {
                "solved": request.solved,
                "approved": request.approved,
                "approved_id": request.approved_id,
                "notified": request.notified,
                "taken": request.taken
            }, synchronize_session=False)
        self.__session.commit()

    def del_user_request(self, req_id: int):
        self.__session.query(UserRequests).filter(UserRequests.id == req_id).delete()
        self.__session.commit()
