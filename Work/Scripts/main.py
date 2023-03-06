from PyQt6.QtWidgets import QApplication, QWidget
from interface2 import LogWindow
from users import *
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from user_collections import *
from database import *
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from database import *
import sqlalchemy
import cryptography
import pymysql

import datetime
engine = create_engine("")
Base.metadata.create_all(engine)
sqlalchemy.pool_recycle = 10
sqlalchemy.pool_timeout = 20
#session = Session(engine)
db = DataBase(engine)
m = db.get_all_users()
#print(m[0][1].power)
f = db.get_all_actions()
for i in f:
    print(i.user_id, i.action, i.what, i.what_id, i.action_time)
zero_admin = Admin(1, "superuser", "superpassword", AdminAccess(12, True, True, True, True, True))
user_list = UserCollection(db)
user_list.append_user(zero_admin)

mas = user_list.get_user_list()
print(user_list.count)


app = QApplication([])


window = LogWindow(user_list, db)

app.exec()
