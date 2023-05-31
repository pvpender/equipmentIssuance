from PyQt6.QtWidgets import QApplication
from interface2 import LogWindow
from equipment_collections import EquipmentCollection
from user_collections import *
from database import *
from rubbish_collector import clear_connection
from apscheduler.schedulers.background import BackgroundScheduler
import sqlalchemy


engine = create_engine(BASE_URL)
Base.metadata.create_all(engine)
sqlalchemy.pool_recycle = 10
sqlalchemy.pool_timeout = 20

db = DataBase(engine)

zero_admin = Admin(1, "superuser", AdminAccess([], True, True, True, True, True))
user_list = UserCollection(db)
user_list.append_user(zero_admin)

mas = user_list.get_user_list()


equipment_list = EquipmentCollection(db)


scheduler = BackgroundScheduler()
scheduler.add_job(clear_connection, 'interval', seconds=200, args=(db,))
scheduler.start()


app = QApplication([])


window = LogWindow(user_list, equipment_list, db)


app.exec()
