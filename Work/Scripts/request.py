from accesses import*
class Request():
    def __init__(self, senderId:str, what:str, howMany:int, purpose:str):
        super().__init__()
        self.__what=what
        self.__howMany=howMany
        self.__senderid=senderId
        self.__isSolved=False
        self.__isApproved=False
        self.__isRejected=False
        self.__whoApprovedId=""
        self.__purpose=purpose

    @property
    def isSolved(self)-> bool:
        return self.isSolved
    @property
    def isApproved(self)-> bool:
        return self.__isApproved
    @property
    def isRejected(self)->bool:
        return self.__isRejected
    @property
    def what(self)-> str:
        return self.__what
    @property
    def purpose(self) -> str:
        return self.__purpose
    @property
    def senderId(self) -> str:
        return self.__senderid
    @property
    def howMany(self)-> int:
        return self.__howMany
    def Approved(self, adminsId: str):
        self.__isSolved = True
        self.__isApproved=True
        self.__whoApproved=adminsId
    def Rejected(self, adminsId: str):
        self.__isSolved = True
        self.__isRejected=True
        self.__whoApproved=adminsId