from flask import jsonify, request
from flask_restful import Resource, marshal, fields, marshal_with, reqparse
from services import UserService
from .resource_utils import validate_date
from .marshal_fields import user_field   
from flask_security import current_user
from flask_security.decorators import roles_required


parser = reqparse.RequestParser()
parser.add_argument("name", type=str, required=True)
parser.add_argument("email", type=str, required=True)

marshal_fields = user_field
service = UserService

"""/api/product/:id"""
class UserResource(Resource):
    # @marshal_with(marshal_fields) either decorator or return function
    # -> only admin
    def get(self, id):
        if (current_user.has_role("manager") or current_user.has_role("customer") ) and current_user.id != id:
            return {'message': "not authorized"}, 401
        item = service.get_by_id(id)
        return marshal(item, marshal_fields), 200

    # -> admin / (customer / manager) own data
    def put(self, id):
        if (current_user.has_role("manager") or current_user.has_role("customer") ) and current_user.id != id:
            return {'message': "not authorized"}, 401
        item = service.get_by_id(id)
        if not item:
            return {"message" : "not found "}, 404
        args = parser.parse_args()
        args["id"] = id
        item = service.update(args)
        return marshal(item, marshal_fields)
    
    def patch(self, id):
        item = service.get_by_id(id)
        if (current_user.has_role("manager") or current_user.has_role("customer") ) and current_user.id != id:
            return {'message': "not authorized"}, 401
        if not item:
            return {"message" : "not found "}, 404
        data = request.get_json()
        data["id"] = id
        item = service.update(data)       
        return marshal(item, marshal_fields), 200
    
    def delete(self, id):
        if (current_user.has_role("manager") or current_user.has_role("customer") ) and current_user.id != id:
            return {'message': "not authorized"}, 401
        item = service.get_by_id(id)
        if not item:
            return {"message" : "not found "}, 404
        message = service.delete(id)
        return message, 200
    
    
    
"""/api/product -> get, post""" 
class UserListResource(Resource):
    # admin only
    @roles_required("admin")
    def get(self):
        items = service.get_all()
        return marshal(items, marshal_fields)

    # /user/:id/approve (only admin)
def approve_user(id):
    user = UserService.update({"active": True, "id": id})
    return marshal(user, user_field)
