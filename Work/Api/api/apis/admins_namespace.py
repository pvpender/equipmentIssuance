import logging
from flask import Blueprint, request
from flask_restx import Namespace, Resource, fields
from models import Logins

admins_namespace = Namespace("admins", description="Get information about admins")

admin = admins_namespace.model('AdminLogin', {
    'login': fields.String(required=True, description='Admin login'),
    'password': fields.String(required=True, description='Admin password')
})


@admins_namespace.route("/existing", methods=['POST'])
class AdminsExistingApi(Resource):
    @admins_namespace.doc("admin_check")
    @admins_namespace.expect(admin)
    def post(self):
        """Check if admin exists"""
        login = request.json.get("login")
        password = request.json.get('password')
        if not login or not password:
            return {"success": False, "message": "Invalid login or password."}, 400
        is_admin = Logins.check_admin(login, password)
        if is_admin:
            logging.info(f"Admin with login '{login}' exists.")
            return {"success": True, "message": "Admin exists."}
        else:
            logging.warning(f"Admin with login '{login}' does not exist.")
            return {"success": False, "message": "Admin does not exist."}, 404
