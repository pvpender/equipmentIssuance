from PyQt6.QtWidgets import QApplication, QWidget
from interface import LogWindow
from users import *
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from user_collections import *
from database import *
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from database import *
import sqlalchemy
import pymysql


#engine = create_engine("mysql+pymysql://freedb_testadminuser:#q4UD$mVTfVrscM@sql.freedb.tech/freedb_Testbase")
engine = create_engine("mysql+pymysql://admin:testpassword!@194.67.206.233:3306/test_base")
Base.metadata.create_all(engine)
sqlalchemy.pool_recycle = 10
sqlalchemy.pool_timeout = 20
session = Session(engine)
db = DataBase(session)
m = db.get_all_users()
#print(m[0][1].power)
zero_admin = Admin(1, "superuser", "superpassword", AdminAccess(12, True, True, True, True, True))
user_list = UserCollection(db)
user_list.append_user(zero_admin)

mas = user_list.get_user_list()
print(user_list.count)


app = QApplication([])


window = LogWindow(user_list, db)

app.exec()
