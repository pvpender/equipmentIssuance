from abc import ABC, abstractmethod
from accesses import *
#   Возможно стоит попробовать @mail.setter @property


class User(ABC):

    def __init__(self, user_id: int, mail: str):
        self.__id = user_id
        self.__mail = mail

    @property
    def id(self) -> int:
        return self.__id

    @property
    def mail(self) -> str:
        return self.__mail

    @id.setter
    def id(self, new_id: int):
        self.__id = new_id

    @mail.setter
    def mail(self, new_mail: str):
        self.__mail = new_mail

    @abstractmethod
    def del_user(self):
        pass


class Admin(User):

    def __init__(self, user_id, mail, password: str, access: AdminAccess):
        super().__init__(user_id, mail)
        self.__password = password
        self.__access = access

    @property
    def password(self) -> str:
        return self.__password

    @password.setter
    def password(self, new_password: str):
        self.__password = new_password

    @property
    def access(self) -> AdminAccess:
        return self.__access

    @access.setter
    def access(self, new_access: AdminAccess):
        self.__access = new_access

    def del_user(self):
        del self.__password
        del self.__access


class CommonUser(User):

    def __init__(self, user_id: int, mail: str, access: Access):
        super().__init__(user_id, mail)
        self.__access = access

    @property
    def access(self) -> Access:
        return self.__access

    @access.setter
    def access(self, new_access: Access):
        self.__access = new_access

    def del_user(self):
        del self.__access
