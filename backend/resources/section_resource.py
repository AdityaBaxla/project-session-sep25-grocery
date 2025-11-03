from flask import jsonify, request
from flask_restful import Resource, marshal, fields, marshal_with, reqparse
from services import SectionService, RequestService
from .resource_utils import validate_date
from .marshal_fields import section_field   
from flask_security import current_user



parser = reqparse.RequestParser()
parser.add_argument("name", type=str, required=True)


marshal_fields = section_field
service = SectionService


"""/api/product/:id"""
class SectionResource(Resource):
    # @marshal_with(marshal_fields) either decorator or return function
    def get(self, id):
        item = service.get_by_id(id)
        return marshal(item, marshal_fields), 200

    def put(self, id):
        item = service.get_by_id(id)
        if not item:
            return {"message" : "not found "}, 404
        args = parser.parse_args()
        args["id"] = id

        if (current_user.has_role("manager")):
            RequestService.create({"data": args, "status": "created", "type": "put section", "user_id": current_user.id})
            return {"message": "request for service is created, wait for admin to approve"}, 200

        item = service.update(args)
        return marshal(item, marshal_fields)
    
    def patch(self, id):
        item = service.get_by_id(id)
        if not item:
            return {"message" : "not found "}, 404
        data = request.get_json()
        data["id"] = id

        if (current_user.has_role("manager")):
            RequestService.create({"data": data, "status": "created", "type": "patch section", "user_id": current_user.id})
            return {"message": "request for service is created, wait for admin to approve"}, 200
        
        item = service.update(data)       
        return marshal(item, marshal_fields), 200
    
    def delete(self, id):
        item = service.get_by_id(id)
        if not item:
            return {"message" : "not found "}, 404
        
        if (current_user.has_role("manager")):
            RequestService.create({"data": {"id": id}, "status": "created", "type": "delete section", "user_id": current_user.id})
            return {"message": "request for service is created, wait for admin to approve"}, 200
        
        message = service.delete(id)
        return message, 200
    
    
    
"""/api/product -> get, post""" 
class SectionListResource(Resource):
    def get(self):
        items = service.get_all()
        return marshal(items, marshal_fields)
    
    def post(self):
        args = parser.parse_args()

        if (current_user.has_role("manager")):
            RequestService.create({"data": args, "status": "created", "type": "post section", "user_id": current_user.id})
            return {"message": "request for service is created, wait for admin to approve"}, 200
        
        item = service.create(args)
        return marshal(item, marshal_fields)
        