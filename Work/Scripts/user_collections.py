from users import *


class UserCollection:

    def __init__(self):
        self.__objects = {}
        self.__count = 0

    @property
    def count(self) -> int:
        return self.__count

    def append_user(self, user: User):
        user.id = self.__count
        self.__objects.update({self.__count: user})
        self.__count += 1

    def get_user_by_id(self, user_id: str) -> User:
        return self.__objects.get(user_id)

    def get_user_by_mail(self, user_mail: str) -> CommonUser | Admin:
        for i in self.__objects:
            if self.__objects[i].mail == user_mail:
                return self.__objects[i]

    def change_user(self, user_id, user):
        user.id = user_id
        self.__objects[user_id] = user

    def del_user(self, user_id: str):
        del self.__objects[user_id]
        self.__count -= 1

    def get_user_by_rights(self, rights: int) -> CommonUser | Admin:
        for i in self.__objects:
            if self.__objects[i].access.rightsToItems == rights:
                return self.__objects[i]