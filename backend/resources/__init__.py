from flask_restful import Api
from flask import Blueprint

from resources.auth_resource import auth_bp
from .products_resource import ProductListResource, ProductResource
from .section_resource import SectionListResource, SectionResource
from .user_resource import UserListResource, UserResource, approve_user

api_bp = Blueprint("api", __name__, url_prefix="/api")

api = Api(api_bp)

api.add_resource(ProductListResource, "/products")
api.add_resource(ProductResource, "/products/<int:id>")

api.add_resource(SectionListResource, "/sections")
api.add_resource(SectionResource, "/sections/<int:id>")

api.add_resource(UserListResource, "/users")
api.add_resource(UserResource, "/users/<int:id>")

api_bp.add_url_rule("/user/<int:id>/approve", view_func=approve_user, methods=["PATCH"]) # add role_required admin

