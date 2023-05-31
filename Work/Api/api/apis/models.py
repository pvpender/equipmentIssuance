from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Users(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    pass_number = db.Column(db.BigInteger)
    mail = db.Column(db.Text)

    @classmethod
    def get_user_by_pass(cls, pass_number: int):
        return cls.query.filter_by(pass_number=pass_number).first()


class Admins(db.Model):
    __tablename__ = "admins"
    user_id = db.Column(db.ForeignKey("users.id", ondelete='CASCADE'), primary_key=True)
    access_id = db.Column(db.ForeignKey("admin_accesses.id"))

    @classmethod
    def get_admin_by_pass(cls, pass_number: int):
        user = Users.get_user_by_pass(pass_number)
        if user:
            return cls.query.filter_by(user_id=user.id).first()
        return None


class Logins(db.Model):
    __tablename__ = "logins"
    id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete='CASCADE'), primary_key=True, autoincrement=False)
    login = db.Column(db.Text, nullable=False)
    password = db.Column(db.Text, nullable=False)
    user = db.relationship("Users")

    @classmethod
    def check_user(cls, login: str, password: str):
        if cls.query.filter_by(login=login, password=password).first():
            return True
        return False

    @classmethod
    def check_admin(cls, login: str, password: str):
        user = cls.query.filter_by(login=login, password=password).first()
        if user and Admins.get_admin_by_pass(user.user.pass_number):
            return True
        return False


class Equipments(db.Model):
    __tablename__ = "equipments"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Text)
    description = db.Column(db.Text)
    count = db.Column(db.Integer)
    reserve_count = db.Column(db.Integer)
    x = db.Column(db.Integer)
    y = db.Column(db.Integer)

    @classmethod
    def get_equipment_by_id(cls, eq_id: int):
        return cls.query.filter_by(id=eq_id).first()


class UserRequests(db.Model):
    __tablename__ = "user_requests"
    id = db.Column(db.Integer, primary_key=True)
    equipment_id = db.Column(db.Integer, nullable=False)
    count = db.Column(db.Integer)
    purpose = db.Column(db.Text)
    sender_id = db.Column(db.Integer, nullable=False)
    solved = db.Column(db.Boolean, default=False)
    approved = db.Column(db.Boolean)
    approved_id = db.Column(db.Integer())
    notified = db.Column(db.Boolean, default=False)
    taken = db.Column(db.Boolean, default=False)

    @classmethod
    def check_requests(cls, user_id: int, req_filter: str):
        if req_filter.lower() == "untaken":
            return cls.query.filter_by(sender_id=user_id, taken=False).all()
        elif req_filter.lower() == "taken":
            return cls.query.filter_by(sender_id=user_id, taken=True).all()
        return cls.query.filter_by(sender_id=user_id).all()

    @classmethod
    def update_request(cls, req_id: int, taken: bool):
        cls.query.filter_by(id=req_id).update({"taken": taken}, synchronize_session=False)
        db.session.commit()


class CurrentRequests(db.Model):
    __tablename__ = "current_request"
    user_id = db.Column(db.ForeignKey("users.id", ondelete='CASCADE'), primary_key=True)
    request_id = db.Column(db.ForeignKey('user_requests.id', ondelete='CASCADE'), nullable=True)

    @classmethod
    def add_current_request(cls, user_id):
        new_request = cls(user_id=user_id)
        db.session.add(new_request)
        db.session.commit()

