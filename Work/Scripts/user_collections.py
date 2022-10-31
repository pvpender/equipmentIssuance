from users import *


class UserCollection:

    def __init__(self):
        self.__objects = []
        self.__count = 0

    @property
    def count(self) -> int:
        return self.__count

    def append_user(self, user: User):
        self.__objects.append(user)
        self.__count += 1

    def find_user(self, user_id: int):
        for i in self.__objects:
            if i.id == user_id:
                return i

    def change_user(self, user_id, user):
        for i in range(self.__count):
            if self.__objects[i].id == user_id:
                self.__objects[i] = user
                break

    def del_user(self, user_id: int):
        del self.__objects[user_id]
        self.__count -= 1


