
class Equipment:

    """Equipment class"""
    def __init__(self, title: str, description: str, count: int,
                 reserve_count: int, groups: list, x: int = -1, y: int = -1, eq_id=None):
        """

        Args:
            title (str): Equipment title
            description (str): Equipment description
            count (int): Count of equipment
            reserve_count (int): Count of reserved equipment
            groups (list): List of equipment groups
            x (int): Position
            y (int): Position
            eq_id (int): Id from database
        """
        self.__title = title
        self.__description = description
        self.__id = eq_id
        self.__count = count
        self.__reserve_count = reserve_count
        self.__groups = groups
        self.__x = x
        self.__y = y

    @property
    def id(self) -> int:
        """

        Returns:
            Id
        """
        return self.__id

    @id.setter
    def id(self, new_id: int):
        """
        Setter for id. Use it ONLY for updating empty id
        Args:
            new_id (int):

        Returns:
            None
        """
        if self.__id is None:
            self.__id = new_id
        else:
            raise Exception("Can set only empty id")

    @property
    def title(self) -> str:
        """

        Returns:
            Equipment title
        """
        return self.__title

    @title.setter
    def title(self, title: str):
        self.__title = title

    @property
    def description(self) -> str:
        """

        Returns:
            Equipment description
        """
        return self.__description

    @description.setter
    def description(self, new_description: str):
        self.__description = new_description

    @property
    def count(self) -> int:
        """Total count of equipment"""
        return self.__count

    @count.setter
    def count(self, new_count: int):
        self.__count = new_count

    @property
    def reserve_count(self) -> int:
        """

        Returns:
            Count of reserved equipment
        """
        return self.__reserve_count

    @reserve_count.setter
    def reserve_count(self, new_res_count: int):
        self.__reserve_count = new_res_count

    @property
    def groups(self) -> list:
        """

        Returns:
            List of equipment groups
        """
        return self.__groups

    @groups.setter
    def groups(self, new_groups: list):
        self.__groups = new_groups

    @property
    def x(self) -> int:
        """

        Returns:
            X axis
        """
        return self.__x

    @x.setter
    def x(self, new_x: int):
        self.__x = new_x

    @property
    def y(self) -> int:
        """

        Returns:
            Y axis
        """
        return self.__y

    @y.setter
    def y(self, new_y: int):
        self.__y = new_y
