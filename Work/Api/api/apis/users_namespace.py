from flask_restx import Namespace, Resource, fields
from flask import request
from models import Logins
import logging

users_namespace = Namespace("users", description="Get information about user")

user = users_namespace.model('UserLogin', {
    'login': fields.String(required=True, description='User login'),
    'password': fields.String(required=True, description='User password')
})


@users_namespace.route("/existing", methods=['POST'])
class UsersExistingApi(Resource):
    @users_namespace.doc("admin_check")
    @users_namespace.expect(user)
    def post(self):
        """Check if user exists"""
        login = request.json.get("login")
        password = request.json.get('password')
        if not login or not password:
            return {"success": False, "message": "Invalid login or password."}, 400
        is_admin = Logins.check_user(login, password)
        if is_admin:
            logging.info(f"User with login '{login}' exists.")
            return {"success": True, "message": "User exists."}
        else:
            logging.warning(f"User with login '{login}' does not exist.")
            return {"success": False, "message": "User does not exist."}, 404
