from typing import Type


class Access:
    def __init__(self, groups: list):
        self.__groups = groups

    @property
    def groups(self) -> list:
        return self.__groups

    @groups.setter
    def groups(self, new_groups: list):
        self.__groups = new_groups


class AdminAccess(Access):
    def __init__(self, groups: list, can_add_users: bool, can_change_users: bool, can_add_inventory: bool,
                 can_change_inventory: bool, can_get_request: bool):
        super().__init__(groups)
        self.__can_add_users = can_add_users
        self.__can_change_users = can_change_users
        self.__can_add_inventory = can_add_inventory
        self.__can_change_inventory = can_change_inventory
        self.__can_get_request = can_get_request

    @property
    def can_add_users(self) -> bool:
        return self.__can_add_users

    @can_add_users.setter
    def can_add_users(self, new_opportunity: bool):
        self.__can_add_users = new_opportunity

    @property
    def can_change_users(self) -> bool:
        return self.__can_change_users

    @can_change_users.setter
    def can_change_users(self, new_opportunity: bool):
        self.__can_change_users = new_opportunity

    @property
    def can_add_inventory(self) -> bool:
        return self.__can_add_inventory

    @can_add_inventory.setter
    def can_add_inventory(self, new_opportunity: bool):
        self.__can_add_inventory = new_opportunity

    @property
    def can_change_inventory(self) -> bool:
        return self.__can_change_inventory

    @can_change_inventory.setter
    def can_change_inventory(self, new_opportunity: bool):
        self.__can_change_inventory = new_opportunity

    @property
    def can_get_request(self) -> bool:
        return self.__can_get_request

    @can_get_request.setter
    def can_get_request(self, new_opportunity: bool):
        self.__can_get_request = new_opportunity
