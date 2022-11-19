from PyQt6.QtWidgets import QApplication, QWidget
from interface import LogWindow
from users import *
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from user_collections import *
from database import *
import pymysql

engine = create_engine("mysql+pymysql://freedb_testadminuser:#q4UD$mVTfVrscM@sql.freedb.tech/freedb_Testbase")
Base.metadata.create_all(engine)
session = Session(engine)
"""access = AdminAccesses(
    can_insert=1,
    can_delete=1,
    can_change=1,
    can_get_request=1
)
session.add(access)
session.commit()"""
"""ids = session.query(AdminAccesses.id).filter(AdminAccesses.can_insert == 1, AdminAccesses.can_delete == 1,
                                         AdminAccesses.can_change == 1, AdminAccesses.can_get_request == 1)
super = Admins(
    mail="superuser",
    access_id=ids,
)
session.add(super)"""
session.commit()
zero_admin = Admin(0, "superuser", "superpassword", AdminAccess(True, True, True, True, True))

rez = session.query(Admins, AdminAccesses).join(AdminAccesses).all()
print(rez[0][0].mail)
user_list = UserCollection()
user_list.append_user(zero_admin)

app = QApplication([])

window = LogWindow(user_list)

app.exec()
