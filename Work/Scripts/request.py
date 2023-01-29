
class Request:
    def __init__(self, sender_tg_id: int, sender_mail: str, what: str, count: int, purpose: str):
        super().__init__()
        self.__what = what
        self.__count = count
        self.__sender_id = sender_tg_id
        self.__sender_mail = sender_mail
        self.__solved = False
        self.__approved = False
        self.__rejected = False
        self.__approved_id = 0
        self.__purpose = purpose

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
    def what(self) -> str:
        return self.__what

    @property
    def purpose(self) -> str:
        return self.__purpose

    @property
    def sender_tg_id(self) -> int:
        return self.__sender_id

    @property
    def sender_mail(self) -> str:
        return self.__sender_mail

    @property
    def count(self) -> int:
        return self.__count

    @property
    def approved_id(self) -> int:
        return self.__approved_id

    def approve(self, admin_id: str):
        self.__solved = True
        self.__approved = True
        self.__approved_id = admin_id

    def reject(self, admin_id: str):
        self.__solved = True
        self.__rejected = True
        self.__approved_id = admin_id


