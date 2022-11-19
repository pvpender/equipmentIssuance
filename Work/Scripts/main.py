from PyQt6.QtWidgets import QApplication, QWidget
from interface import LogWindow
from users import *
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from user_collections import *
from database import *
import pymysql

#engine = create_engine("mysql+pymysql://sql7544993:9razbAvzG4@sql7.freemysqlhosting.net/sql7544993")
#Base.metadata.create_all(engine)
#session = Session(engine)
#super = Admins(
#    mail="superuser",
#    access_id=0,
#    access=AdminAccesses(
#        can_insert=1,
#        can_delete=1,
#        can_change=1,
#        can_get_request=1
#    )
#)
#session.add(super)
#session.commit()
zero_admin = Admin(0, "superuser", "superpassword", AdminAccess(True, True, True, True, True))

user_list = UserCollection()
user_list.append_user(zero_admin)

app = QApplication([])

window = LogWindow(user_list)

app.exec()
