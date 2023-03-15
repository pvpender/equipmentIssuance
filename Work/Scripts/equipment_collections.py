from typing import Any

from sqlalchemy.orm import InstrumentedAttribute

from Work.Scripts.equipment import Equipment
from equipment import Equipment
from database import DataBase


class EquipmentCollection:
    def __init__(self, db: DataBase):
        self.__db = db
        self.__objects = {}
        self.__count = 0
        mas = db.get_all_equipment()
        for i in mas:
            groups = [j.id for j in i.equipment_groups]
            self.__objects.update({i.id: Equipment(i.title,
                                                   i.description,
                                                   i.count,
                                                   i.reserve_count,
                                                   groups,
                                                   i.x,
                                                   i.y,
                                                   i.id)})
            self.__count += 1

    @property
    def count(self) -> int:
        return self.__count

    def get_equipment_by_id(self, equipment_id: int) -> Equipment:
        return self.__objects[equipment_id]

    def get_equipment_by_title(self, title: str) -> Equipment:
        for i in self.__objects.values():
            if i.title == title:
                return i

    def get_equipment_list(self) -> list:
        return list(self.__objects.values())

    def add_equipment(self, equipment: Equipment):
        self.__db.add_equipment(equipment)
        equipment.id = self.__db.get_equipment_by_title(equipment.title)
        self.__objects.update({equipment.title: equipment})
        self.__count += 1

    def change_equipment(self, equipment: Equipment):
        self.__db.update_equipment(equipment)
        self.__objects[equipment.id] = equipment

    def del_equipment(self, equipment_id: int):
        self.__db.delete_equipment(self.__objects[equipment_id])
        del self.__objects[equipment_id]

    def add_groups(self, equipment_id: int, groups: list):
        for i in groups:
            if i not in self.__objects[equipment_id].groups:
                self.__db.add_equipment_group(equipment_id, i)
                self.__objects[equipment_id].groups.append(i)

    def del_groups(self, equipment_id: int, groups: list):
        self.__db.del_equipment_group(equipment_id, groups)
        for i in groups:
            try:
                self.__objects[equipment_id].groups.remove(i)
            except ValueError:
                pass

    def get_equipment_by_group(self, group_id: int) -> list:
        mas = [i for i in self.__objects.values() if group_id in i.groups]
        return mas


