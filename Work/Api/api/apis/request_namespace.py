from flask_restx import Namespace, Resource, fields
from flask import request
from models import UserRequests, Equipments, Users, Admins, CurrentRequests
import logging

request_namespace = Namespace("requests", description="Get information about user request")

request_model = request_namespace.model('Request', {
    'id': fields.Integer(required=True, description='Request id'),
    'taken': fields.Boolean(required=True, description='Is it taken')
})

current_request_model = request_namespace.model("CurrentRequest",
                                                {"pass_number": fields.Integer(required=True, description="Pass number")})


@request_namespace.route("/<int:pass_number>", methods=['GET'])
@request_namespace.doc(params={"pass_number": "Pass number in decimal number system"})
class RequestExistingApi(Resource):
    @request_namespace.doc("requests_check", params={"filter": "Request filter. Set taken/untaken for getting special "
                                                               "requests"})
    def get(self, pass_number):
        """Check if requests exists"""
        requests_type = request.args.get('filter', 'not_executed')
        usr = Users.get_user_by_pass(pass_number)
        if not usr:
            return {"success": False}, 404
        requests = UserRequests.check_requests(usr.id, requests_type)
        if requests:
            logging.info(f"Find approved requests for '{pass_number}'.")
            response = []
            for i in requests:
                eq = Equipments.get_equipment_by_id(i.equipment_id)
                response.append({
                    "id": i.id,
                    "count": i.count,
                    "equipment": {
                        "id": eq.id,
                        "title": eq.title,
                        "description": eq.description,
                        "x": eq.x,
                        "y": eq.y
                    }
                })
            return {
                "success": True,
                "sender_id": requests[0].sender_id,
                "requests": response
            }, 200
        else:
            logging.warning(f"Doesn't find approved requests for '{pass_number}'.")
            return {"success": False}, 404


@request_namespace.route("/current", methods=["GET", "PUT", "DELETE"])
class CurrentRequestApi(Resource):
    @request_namespace.doc("Check current request")
    def get(self):
        """Check if exist current request"""

    @request_namespace.doc("Add current request")
    @request_namespace.expect(current_request_model)
    def put(self):
        pass_number = request.json.get("pass_number")
        user = Users.get_user_by_pass(pass_number)
        CurrentRequests.add_current_request(user.id)




@request_namespace.route("/update", methods=["PUT"])
class RequestUpdatingApi(Resource):
    @request_namespace.expect(request_model)
    def put(self):
        """Update request"""
        r_id = request.json.get("id")
        taken = request.json.get("taken")
        UserRequests.update_request(r_id, taken)
