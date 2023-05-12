from typing import Type


class Access:

    """Base Access class"""

    def __init__(self, groups: list):
        """

        Args:
            groups (list): list of user groups
        """
        self.__groups = groups

    @property
    def groups(self) -> list:
        """

        Returns:
            List of user groups
        """
        return self.__groups

    @groups.setter
    def groups(self, new_groups: list):
        """

        Args:
            new_groups (list): Set new user groups list

        """
        self.__groups = new_groups


class AdminAccess(Access):

    """
    Admin access class
    """

    def __init__(self, groups: list, can_add_users: bool, can_change_users: bool, can_add_inventory: bool,
                 can_change_inventory: bool, can_get_request: bool):
        """

        Args:
            groups (list): List of user groups
            can_add_users (bool): Possibility to adding users
            can_change_users (bool): Possibility to updating users
            can_add_inventory (bool): Possibility to adding inventory
            can_change_inventory: Possibility to changing inventory
            can_get_request: Possibility to getting requests
        """
        super().__init__(groups)
        self.__can_add_users = can_add_users
        self.__can_change_users = can_change_users
        self.__can_add_inventory = can_add_inventory
        self.__can_change_inventory = can_change_inventory
        self.__can_get_request = can_get_request

    @property
    def can_add_users(self) -> bool:
        """

        Returns:
            Possibility of adding users
        """
        return self.__can_add_users

    @can_add_users.setter
    def can_add_users(self, new_opportunity: bool):
        """

        Args:
            new_opportunity (bool):

        Returns:

        """
        self.__can_add_users = new_opportunity

    @property
    def can_change_users(self) -> bool:
        """

        Returns:
            Possibility to change users
        """
        return self.__can_change_users

    @can_change_users.setter
    def can_change_users(self, new_opportunity: bool):
        """

        Args:
            new_opportunity:

        Returns:

        """
        self.__can_change_users = new_opportunity

    @property
    def can_add_inventory(self) -> bool:
        """

        Returns:
            Possibility to adding inventory
        """
        return self.__can_add_inventory

    @can_add_inventory.setter
    def can_add_inventory(self, new_opportunity: bool):
        """

        Args:
            new_opportunity:

        Returns:

        """
        self.__can_add_inventory = new_opportunity

    @property
    def can_change_inventory(self) -> bool:
        """

        Returns:
            Possibility to change inventory
        """
        return self.__can_change_inventory

    @can_change_inventory.setter
    def can_change_inventory(self, new_opportunity: bool):
        """

        Args:
            new_opportunity:

        Returns:

        """
        self.__can_change_inventory = new_opportunity

    @property
    def can_get_request(self) -> bool:
        """

        Returns:
            Possibility to getting requests
        """
        return self.__can_get_request

    @can_get_request.setter
    def can_get_request(self, new_opportunity: bool):
        """

        Args:
            new_opportunity:

        Returns:

        """
        self.__can_get_request = new_opportunity
