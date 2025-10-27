from models import Product, db
from services.service_errors import ServiceError

class ProductService():

    @staticmethod
    def get_all():
        return Product.query.all()
    
    @staticmethod
    def get_by_id(id):
        item = Product.query.get(id)
        if not item:
            raise ServiceError("not found")
        return item
    
    @staticmethod
    def create(data):
        # need checks if key is present in model (data validation check)
        item = Product(**data)
        
        db.session.add(item)
        db.session.commit()
        return item

    @staticmethod
    def delete(id):
        item = Product.query.get(id)
        if not item:
            raise ServiceError("not found")
        
        db.session.delete(item)
        db.session.commit()
        return item
    
    @staticmethod
    def update(data):
        """{'id' : 1, 'name': 'abc'..}"""
        item = Product.query.get(data["id"])
        if not item:
            raise ServiceError("not found")
        
        # need checks if key is present in model
        print(item.name)
        print(data)
        for key in data:
            setattr(item, key, data[key])

        db.session.commit()
        return item

        
