from database import DataBase, fix_died_connection
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
import time
import threading
from conf import BASE_URL


def clear_connection(db: DataBase):
    if (time.time() - db.last_db_access_time) > 200:
        t = threading.Thread(target=fix_died_connection, args=(db.session,))
        t.start()
        db.session = Session(create_engine(BASE_URL))
        db.last_db_access_time = time.time()

