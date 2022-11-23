from equipment import *


class EquipmentList:
    def __init__(self):
        self.__objects = {}
        self.__count = 0

    @property
    def count(self) -> int:
        return self.__count

    def append(self, equipment: Equipment):
        equipment.id = self.__count
        self.__objects.update({self.__count: equipment})
        self.__count += 1

    def change_equipment(self, equipment_id: int, equipment: Equipment):
        equipment.id = equipment_id
        self.__objects[equipment_id] = equipment

    def get_equipment(self, equipment_id: int) -> Equipment:
        return self.__objects[equipment_id]

    def del_equipment(self, equipment_id):
        del self.__objects[equipment_id]
        self.__count -= 1
        mas_new_keys = [i for i in range(self.__count+1)]
        self.__objects = dict(zip(mas_new_keys, list(self.__objects.values())))
