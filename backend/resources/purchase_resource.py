from decimal import Decimal
from flask_restful import Resource, marshal_with, fields
from flask import request
from flask_security import auth_required, current_user
from models import Product, Sale, SaleItem
from extensions import db
from http import HTTPStatus
from datetime import datetime

# Define marshal fields for nested responses
sale_item_fields = {
    'id': fields.Integer,
    'product_id': fields.Integer,
    'quantity': fields.Integer,
    'price_at_sale': fields.Float,
    'product': fields.Nested({
        'id': fields.Integer,
        'name': fields.String,
        'image': fields.String,
    })
}

sale_fields = {
    'id': fields.Integer,
    'customer_id': fields.Integer,
    'total_amount': fields.Float,
    'status': fields.String,
    'created_at': fields.DateTime(dt_format='iso8601'),
    'sale_items': fields.List(fields.Nested(sale_item_fields))
}

class PurchaseResource(Resource):
    @auth_required("token")
    def post(self):
        """Process purchase from cart items"""
        try:
            # Get cart items from request
            items = request.get_json()['items']
            if not items or not isinstance(items, list):
                return {"message": "Invalid cart data"}, HTTPStatus.BAD_REQUEST

            # Create new sale
            sale = Sale(customer_id=current_user.id)
            db.session.add(sale)
            db.session.flush()  # Get the sale.id

            total_amount = 0

            # Process each item
            for item in items:
                product_id = item.get('product_id')
                quantity = int(item.get('quantity', 0))  # Ensure quantity is int

                # Validate product exists
                product = Product.query.get(product_id)
                if not product:
                    db.session.rollback()
                    return {"message": f"Product {product_id} not found"}, HTTPStatus.NOT_FOUND

                # Check stock availability
                if product.stock < quantity:
                    db.session.rollback()
                    return {
                        "message": f"Insufficient stock for {product.name}. Available: {product.stock}"
                    }, HTTPStatus.BAD_REQUEST

                # Convert price to float for calculations
                unit_price = float(product.price)

                # Create sale item
                sale_item = SaleItem(
                    product_id=product_id,
                    sale_id=sale.id,
                    quantity=quantity,
                    price_at_sale=unit_price
                )
                db.session.add(sale_item)

                # Update product stock (both are integers)
                product.stock = product.stock - quantity

                # Calculate total
                total_amount += unit_price * quantity

            # Update sale total
            sale.total_amount = total_amount
            
            db.session.commit()

            return {
                "message": "Purchase successful",
                "sale_id": sale.id,
                "total": total_amount
            }, HTTPStatus.CREATED

        except Exception as e:
            db.session.rollback()
            return {"message": f"Purchase failed: {str(e)}"}, HTTPStatus.INTERNAL_SERVER_ERROR

class OrderListResource(Resource):
    @auth_required("token")
    @marshal_with(sale_fields)
    def get(self):
        """Get all orders for current user"""
        orders = Sale.query.filter_by(customer_id=current_user.id)\
                          .order_by(Sale.created_at.desc())\
                          .all()
        return orders

class OrderDetailResource(Resource):
    @auth_required("token")
    @marshal_with(sale_fields)
    def get(self, order_id):
        """Get specific order details"""
        order = Sale.query.filter_by(
            id=order_id, 
            customer_id=current_user.id
        ).first()
        
        if not order:
            return {"message": "Order not found"}, HTTPStatus.NOT_FOUND
            
        return order
