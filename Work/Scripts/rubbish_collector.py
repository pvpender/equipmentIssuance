from database import DataBase, fix_died_connection
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
import time
import threading


def clear_connection(db: DataBase):
    if (time.time() - db.last_db_access_time) > 200:
        t = threading.Thread(target=fix_died_connection, args=(db.session,))
        t.start()
        db.session = Session(create_engine(f"mysql+pymysql://admin:testPass@194.67.206.233:3306/test_base"))
        db.last_db_access_time = time.time()

