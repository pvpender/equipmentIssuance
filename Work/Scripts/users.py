from abc import ABC, abstractmethod
from typing import Union

from accesses import *


class User(ABC):

    def __init__(self, pass_number: int, mail: str, base_id=None):
        self.__pass_number = pass_number
        self.__mail = mail
        self.__base_id = base_id

    @property
    def pass_number(self) -> int:
        return self.__pass_number

    @property
    def mail(self) -> str:
        return self.__mail

    @pass_number.setter
    def pass_number(self, new_pass_number: int):
        self.__pass_number = new_pass_number

    @mail.setter
    def mail(self, new_mail: str):
        self.__mail = new_mail

    @property
    def base_id(self) -> Union[None, int]:
        return self.__base_id

    @base_id.setter
    def base_id(self, base_id):
        if self.__base_id is None:
            self.__base_id = base_id
        else:
            raise Exception("Can set only empty id")

    @abstractmethod
    def del_user(self):
        pass


class Admin(User):

    def __init__(self, pass_nuber, mail, access: AdminAccess, base_id=None):
        super().__init__(pass_nuber, mail, base_id)
        self.__access = access

    @property
    def access(self) -> AdminAccess:
        return self.__access

    @access.setter
    def access(self, new_access: AdminAccess):
        self.__access = new_access

    def del_user(self):
        del self.__access


class CommonUser(User):
    def __init__(self, pass_number: int, mail: str, access: Access, base_id=None):
        super().__init__(pass_number, mail, base_id)
        self.__access = access

    @property
    def access(self) -> Access:
        return self.__access

    @access.setter
    def access(self, new_access: Access):
        self.__access = new_access

    def del_user(self):
        del self.__access
