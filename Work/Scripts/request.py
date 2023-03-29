
class Request:
    def __init__(self, sender_tg_id: int, sender_id: int, equipment_id: int, count: int, purpose: str):
        super().__init__()
        self.__equipment_id = equipment_id
        self.__count = count
        self.__sender_tg_id = sender_tg_id
        self.__sender_id = sender_id
        self.__solved = False
        self.__approved = False
        self.__rejected = False
        self.__approved_id = 0
        self.__purpose = purpose
        self.__notified = False
        self.__taken = False

    @property
    def solved(self) -> bool:
        return self.__solved

    @property
    def approved(self) -> bool:
        return self.__approved

    @property
    def rejected(self) -> bool:
        return self.__rejected

    @property
    def equipment_id(self) -> int:
        return self.__equipment_id

    @property
    def purpose(self) -> str:
        return self.__purpose

    @property
    def sender_tg_id(self) -> int:
        return self.__sender_tg_id

    @property
    def sender_id(self) -> int:
        return self.__sender_id

    @property
    def count(self) -> int:
        return self.__count

    @property
    def approved_id(self) -> int:
        return self.__approved_id

    @property
    def notified(self) -> bool:
        return self.__notified

    @property
    def taken(self) -> bool:
        return self.__taken

    def approve(self, admin_id: str):
        self.__solved = True
        self.__approved = True
        self.__approved_id = admin_id

    def reject(self, admin_id: str):
        self.__solved = True
        self.__rejected = True
        self.__approved_id = admin_id


