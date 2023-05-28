
class Request:
    """User request class"""
    def __init__(self, sender_id: int, equipment_id: int, count: int, purpose: str):
        super().__init__()
        self.__equipment_id = equipment_id
        self.__count = count
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
        """

        Returns:
            Is request solved
        """
        return self.__solved

    @property
    def approved(self) -> bool:
        """
        Returns:
            Is request approved
        """
        return self.__approved

    @property
    def rejected(self) -> bool:
        """

        Returns:
            Is request rejected
        """
        return self.__rejected

    @property
    def equipment_id(self) -> int:
        """

        Returns:
            Equipment id for this request
        """
        return self.__equipment_id

    @property
    def purpose(self) -> str:
        """

        Returns:
            Purpose
        """
        return self.__purpose

    @property
    def sender_id(self) -> int:
        """

        Returns:
            Sender id from database
        """
        return self.__sender_id

    @property
    def count(self) -> int:
        """

        Returns:
            Count
        """
        return self.__count

    @property
    def approved_id(self) -> int:
        """

        Returns:
            From which admin was approved
        """
        return self.__approved_id

    @property
    def notified(self) -> bool:
        """

        Returns:
            Is notified
        """
        return self.__notified

    @property
    def taken(self) -> bool:
        """

        Returns:
            Is taken
        """
        return self.__taken

    def approve(self, admin_id: str):
        """
        Approve request

        Args:
            admin_id (int):
                Who has approved
        Returns:

        """
        self.__solved = True
        self.__approved = True
        self.__approved_id = admin_id

    def reject(self, admin_id: str):
        """
        Reject request

        Args:
            admin_id (int):
                Who has rejected
        Returns:

        """
        self.__solved = True
        self.__rejected = True
        self.__approved_id = admin_id


