from PyQt6.QtWidgets import QApplication, QWidget
from interface import LogWindow
from users import *
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from user_collections import *
from database import *
import pymysql
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from database import *
import pymysql

engine = create_engine("mysql+pymysql://freedb_testadminuser:#q4UD$mVTfVrscM@sql.freedb.tech/freedb_Testbase")
Base.metadata.create_all(engine)
session = Session(engine)
db = DataBase(session)

zero_admin = Admin(0, "superuser", "superpassword", AdminAccess(12, True, True, True, True, True))
user_list = UserCollection()
user_list.append_user(zero_admin)

app = QApplication([])

window = LogWindow(user_list)

app.exec()
