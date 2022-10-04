from abc import ABC, abstractmethod

#   Возможно стоит попробовать @mail.setter @property


class User(ABC):

    def __init__(self, user_id, mail):
        self.__id = user_id
        self.__mail = mail

    def get_id(self):
        return self.__id

    def get_mail(self):
        return self.__mail

    def set_id(self, new_id):
        self.__id = new_id

    def set_mail(self, new_mail):
        self.__mail = new_mail

    @abstractmethod
    def del_user(self):
        pass


class Admin(User):
    pass

