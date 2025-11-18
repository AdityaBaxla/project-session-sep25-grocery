from flask import jsonify, request
from flask_restful import Resource, marshal, fields, marshal_with, reqparse
from services import ProductService
from .resource_utils import validate_date
from .marshal_fields import product_fields
from extensions import cache



parser = reqparse.RequestParser()
parser.add_argument("name", type=str, required=True)
parser.add_argument("price", type=float, required=True)
parser.add_argument("stock", )
parser.add_argument("mfd", type=validate_date  )
parser.add_argument("expiry", type=validate_date)
parser.add_argument("unit_of_sale")  
parser.add_argument("section_id")

marshal_fields = product_fields
service = ProductService


"""/api/product/:id"""
class ProductResource(Resource):
    # @marshal_with(marshal_fields) either decorator or return function

    @cache.memoize()
    def get(self, id):
        item = service.get_by_id(id)
        return marshal(item, marshal_fields), 200

    def put(self, id):
        item = service.get_by_id(id)
        if not item:
            return {"message" : "not found "}, 404
        args = parser.parse_args()
        args["id"] = id
        item = service.update(args)
        cache.delete_memoized(ProductResource.get, ProductResource, id)
        return marshal(item, marshal_fields)
    
    def patch(self, id):
        item = service.get_by_id(id)
        if not item:
            return {"message" : "not found "}, 404
        data = request.get_json()
        data["id"] = id
        item = service.update(data)       
        return marshal(item, marshal_fields), 200
    
    def delete(self, id):
        item = service.get_by_id(id)
        if not item:
            return {"message" : "not found "}, 404
        message = service.delete(id)
        return message, 200
    
    
    
"""/api/product -> get, post""" 
class ProductListResource(Resource):

    @cache.cached(key_prefix="product_get")
    def get(self):
        items = service.get_all()
        return marshal(items, marshal_fields)
    
    def post(self):
        args = parser.parse_args()
        item = service.create(args)
        cache.delete("product_get")
        return marshal(item, marshal_fields)
        