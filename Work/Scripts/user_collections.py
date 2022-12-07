from users import *
from database import DataBase


class UserCollection:

    def __init__(self, db: DataBase):
        self.__db = db
        self.__objects = {}
        self.__count = 0
        mas = self.__db.get_all_users()
        for i in mas:
            self.__objects.update({i[0].pass_number: CommonUser(i[0].pass_number, i[0].mail, Access(i[1].power))})
            self.__count += 1
        mas = self.__db.get_all_admins()
        for i in mas:
            self.__objects.update({i[0].pass_number: Admin(i[0].pass_number, i[0].mail, i[0].password,
                                                           AdminAccess(i[1].power,
                                                                       i[1].can_add_users,
                                                                       i[1].can_change_users,
                                                                       i[1].can_add_inventory,
                                                                       i[1].can_change_inventory,
                                                                       i[1].can_get_request))})
            self.__count += 1

    @property
    def count(self) -> int:
        return self.__count

    def append_user(self, user: CommonUser | Admin):
        try:
            if type(user) == type(CommonUser):
                self.__db.add_user(user)
            else:
                self.__db.add_admin(user)
            self.__objects.update({user.id: user})
            self.__count += 1
        except ValueError:
            return -1

    def get_user_by_id(self, user_id: int) -> CommonUser | Admin:
        return self.__objects.get(user_id)

    def check_user_by_id(self, user_id: int) -> bool:
        if self.__objects.get(user_id):
            return True
        else:
            return False

    def get_user_by_mail(self, user_mail: str) -> CommonUser | Admin:
        for i in self.__objects.values():
            if i.mail == user_mail:
                return i
    def check_user_by_mail(self, user_mail: str) -> bool:
        for i in self.__objects.values():
            if i.mail == user_mail:
                return True
        return False
    def change_user(self, user_id: int, mail: str, user: CommonUser | Admin):
        if type(user) == type(CommonUser):
            self.__db.update_user(user_id, mail, user)
        else:
            self.__db.update_admin(user_id, mail, user)
        del self.__objects[user_id]
        self.__objects.update({user.id: user})

    def del_user(self, user_id: str):
        if type(self.__objects[user_id]) == type(CommonUser):
            self.__db.delete_user(self.__objects[user_id])
        else:
            self.__db.delete_admin(self.__objects[user_id])
        del self.__objects[user_id]
        self.__count -= 1

    def get_user_list(self):
        return list(self.__objects.values())

    def get_user_by_rights(self, rights: int) -> CommonUser | Admin:
        for i in self.__objects:
            if self.__objects[i].access.power == rights:
                return self.__objects[i]
