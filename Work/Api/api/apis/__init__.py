from flask import Blueprint
from flask_restx import Api
from admins_namespace import admins_namespace
from users_namespace import users_namespace
from request_namespace import request_namespace

blueprint = Blueprint("api", __name__)
api = Api(blueprint, version='0.1', title="equipmentIssuance User API")
api.add_namespace(admins_namespace)
api.add_namespace(users_namespace)
api.add_namespace(request_namespace)

