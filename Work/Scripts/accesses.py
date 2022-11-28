from abc import ABC


class Access:
    def __init__(self, new_id: int, can_get_without_req: bool, can_send_req: bool):
        self.__id = new_id
        self.__can_get_without_req = can_get_without_req
        self.__can_send_req = can_send_req

    @property
    def id(self) -> int:
        return self.__id

    @id.setter
    def id(self, new_id: int):
        self.__id = new_id

    @property
    def can_get_without_req(self) -> bool:
        return self.__can_get_without_req

    @can_get_without_req.setter
    def can_get_without_req(self, new_list_eq: bool):
        self.__can_get_without_req = new_list_eq

    @property
    def can_send_req(self) -> bool:
        return self.__can_send_req

    @can_send_req.setter
    def can_send_req(self, new_opportunity: bool):
        self.__can_send_req = new_opportunity
# Переименовать can_get_without_request


class AdminAccess(Access):
    def __init__(self, new_id: int, can_insert: bool, can_delete: bool, can_change: bool, can_get_request: bool,
                 can_get_without_req:bool, power: int):
        super().__init__(new_id, can_get_without_req, can_get_request)
        self.__can_insert = can_insert
        self.__can_delete = can_delete
        self.__can_change = can_change
        self.__can_get_request = can_get_request
        self.__can_get_without_req=can_get_without_req
        self.__power=power ##Права относительно пользователей в виде числа. К примеру: 21, где 20 - властен добавлять, менять и удалять пользователей, 1 - властен добавлять админов

    @property
    def can_insert(self) -> bool:
        return self.__can_insert

    @can_insert.setter
    def can_insert(self, new_opportunity: bool):
        self.__can_insert = new_opportunity

    @property
    def can_delete(self) -> bool:
        return self.__can_delete

    @can_delete.setter
    def can_delete(self, new_opportunity: bool):
        self.__can_delete = new_opportunity

    @property
    def can_change(self) -> bool:
        return self.__can_change

    @can_change.setter
    def can_change(self, new_opportunity: bool):
        self.__can_change = new_opportunity

    @property
    def can_get_request(self) -> bool:
        return self.__can_get_request

    @can_get_request.setter
    def can_get_request(self, new_opportunity: bool):
        self.__can_get_request = new_opportunity

    @property
    def power(self)->int:
        return self.__power
    @power.setter
    def power(self, newPower: int):
        self.__power=newPower