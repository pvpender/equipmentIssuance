

class Equipment:

    def __init__(self, new_id: int, title: str, count: int, reserve_count: int, x: int, y: int):
        self.__id = new_id
        self.__title = title
        #self.__description = description
        self.__count = count
        self.__reserve_count = reserve_count
        self.__x = x
        self.__y = y

    @property
    def id(self) -> int:
        return self.__id

    @id.setter
    def id(self, new_id: int):
        self.__id = new_id

    @property
    def title(self) -> str:
        return self.__title

    @title.setter
    def title(self, title: str):
        self.__title = title

    """@property
    def description(self) -> str:
        return self.__description

    @description.setter
    def description(self, new_description: str):
        self.__description = new_description"""

    @property
    def count(self) -> int:
        return self.__count

    @count.setter
    def count(self, new_count: int):
        self.__count = new_count

    @property
    def reserve_count(self) -> int:
        return self.reserve_count

    @reserve_count.setter
    def reserve_count(self, new_res_count: int):
        self.__reserve_count = new_res_count

    @property
    def x(self) -> int:
        return self.__x

    @x.setter
    def x(self, new_x: int):
        self.__x = new_x

    @property
    def y(self) -> int:
        return self.__y

    @y.setter
    def y(self, new_y: int):
        self.__y = new_y
