from users import *
from database import DataBase


class UserCollection:

    def __init__(self, db: DataBase):
        self.__db = db
        self.__objects = {}
        self.__count = 0
        mas = self.__db.get_all_admins()
        for i in mas:
            groups = [j.group_id for j in i.user.user_groups]
            self.__objects.update({i.user.pass_number: Admin(i.user.pass_number, i.user.mail,
                                                             AdminAccess(groups,
                                                                         i.access.can_add_users,
                                                                         i.access.can_change_users,
                                                                         i.access.can_add_inventory,
                                                                         i.access.can_change_inventory,
                                                                         i.access.can_get_request), i.user_id)})
            self.__count += 1
        mas = self.__db.get_all_users()
        for i in mas:
            if not self.__objects.get(i.pass_number):
                groups = [j.group_id for j in i.user_groups]
                self.__objects.update({i.pass_number: CommonUser(i.pass_number, i.mail, Access(groups), i.id)})
                self.__count += 1

    @property
    def count(self) -> int:
        return self.__count

    def append_user(self, user: CommonUser | Admin):
        try:
            if isinstance(user, CommonUser):
                self.__db.add_user(user)
                base_id = self.__db.get_user_by_mail(user.mail).id
            else:
                self.__db.add_admin(user)
                base_id = self.__db.get_admin_by_mail(user.mail).user.id
            user.base_id = base_id
            self.__objects.update({user.pass_number: user})
            self.__count += 1
        except ValueError:
            return -1

    def get_user_by_id(self, user_id: int) -> CommonUser | Admin | None:
        for i in self.__objects.values():
            if i.base_id == user_id:
                return i
        return None

    def get_user_by_pass(self, pass_number: int) -> CommonUser | Admin | None:
        return self.__objects.get(pass_number)

    def check_user_by_pass(self, pass_number: int) -> bool:
        for i in self.__objects.values():
            if i.pass_number == pass_number:
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

    def change_user(self, pass_number: int, mail: str, user: CommonUser | Admin):
        if isinstance(user, CommonUser):
            self.__db.update_user(pass_number, mail, user)
        else:
            self.__db.update_admin(pass_number, mail, user)
        del self.__objects[pass_number]
        self.__objects.update({user.pass_number: user})

    def del_user(self, pass_number: int):
        print(self.__objects)
        if isinstance(self.__objects[pass_number], CommonUser):
            self.__db.delete_user(self.__objects[pass_number])
        else:
            self.__db.delete_admin(self.__objects[pass_number])
        del self.__objects[pass_number]
        self.__count -= 1

    def get_user_list(self):
        return list(self.__objects.values())

    def add_groups(self, pass_number, groups: list):
        for i in groups:
            if i not in self.__objects[pass_number].access.groups:
                self.__objects[pass_number].access.groups.append(i)
                self.__db.add_user_group(self.__objects[pass_number].base_id, i)

    def del_groups(self, pass_number, groups: list):
        if isinstance(self.__objects[pass_number], CommonUser):
            self.__db.del_user_group(self.__objects[pass_number].base_id, groups)
        else:
            self.__db.del_admin_group(self.__objects[pass_number].base_id, groups)
        for i in groups:
            try:
                self.__objects[pass_number].access.groups.remove(i)
            except ValueError:
                pass

    def get_user_by_group(self, group_id: int) -> list:
        mas = [i for i in self.__objects.values() if group_id in i.access.groups]
        return mas

    """def get_user_by_rights(self, rights: int) -> CommonUser | Admin:
        for i in self.__objects:
            if self.__objects[i].access.power == rights:
                return self.__objects[i]"""
