from PyQt6.QtWidgets import QApplication, QWidget
from interface2 import LogWindow
from users import *
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from equipment_collections import EquipmentCollection
from user_collections import *
from database import *
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from database import *
import sqlalchemy
import cryptography
import pymysql

import datetime


#engine = create_engine("mysql+pymysql://freedb_testadminuser:#q4UD$mVTfVrscM@sql.freedb.tech/freedb_Testbase")
#engine = create_engine("mysql+pymysql://developer:deVpass@194.67.206.233:3306/dev_base")
engine = create_engine("mysql+pymysql://admin:testPass@194.67.206.233:3306/test_base")
Base.metadata.create_all(engine)
sqlalchemy.pool_recycle = 10
sqlalchemy.pool_timeout = 20
#session = Session(engine)
db = DataBase(engine)

#db.del_group(2)
#db.add_group("biv")
#db.add_user(CommonUser(123, "test", [1]))
#db.delete_user(db.get_user_by_id(123))
#db.add_equipment(Equipment("test", "test", 2, 0, []))
#print(m[0][1].power)
#f = db.get_all_actions()
#for i in f:
#    print(i.user_id, i.action, i.what, i.what_id, i.action_time)
zero_admin = Admin(1, "superuser", AdminAccess([1], True, True, True, True, True))
user_list = UserCollection(db)
user_list.append_user(zero_admin)
print(user_list.get_user_list())

mas = user_list.get_user_list()
#print(user_list.count)
#print(db.get_action_by_passes_as_df([1]))
#print(db.get_inv_from_act_as_df(["test", "тестик"]))

equipment_list = EquipmentCollection(db)

print(user_list.get_user_by_id(1))

"""
Веди переменную последнего обращения к базе в декораторе делай проверку, если что-то не так - rollback сессии

Роллбэк не сработает, зато можно создавать новую сессию (эта всё равно уже нерабочая) тогда избежим большую задержку


"""


app = QApplication([])


window = LogWindow(user_list, equipment_list, db)


app.exec()
