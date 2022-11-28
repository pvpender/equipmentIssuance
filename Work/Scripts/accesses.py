class Access():
    def __init__(self, can_get_without_req: bool, can_send_req: bool, rightsToItems: int):
        super().__init__()
        self.__can_get_without_req = can_get_without_req
        self.__can_send_req = can_send_req
        self.__rightsToItems=rightsToItems

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
    @property
    def rightsToItems(self) -> int:
        return self.__rightsToItems

    @rightsToItems.setter
    def rightsToItems(self, newRightsToItems: int):
        self.__rightsToItems = newRightsToItems

class AdminAccess(Access):
    def __init__(self,  can_insert: bool, can_delete: bool, can_change: bool, can_get_request: bool, can_get_without_req:list,rightsToItems: int ,power: int):
        self.__can_insert = can_insert
        self.__can_delete = can_delete
        self.__can_change = can_change
        self.__can_get_request = can_get_request
        self.__can_get_without_req=can_get_without_req
        self.__power=power ##Права относительно пользователей в виде числа. К примеру: 21, где 20 - властен добавлять, менять и удалять пользователей, 1 - властен добавлять админов
        self.__rightsToItems=rightsToItems


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