import uuid
import random
from datetime import datetime, timedelta, timezone
from faker import Faker
from faker_food import FoodProvider
from flask_security.utils import hash_password
from app import app  # Ensure your Flask app is imported
from models import db, User, Role, UserRoles, Manager, Customer, Section, Product, Sale, SaleItem

fake = Faker()
fake.add_provider(FoodProvider)


def seed_data():
    with app.app_context():
        print("🧹 Clearing old data...")
        db.drop_all()
        db.create_all()

        # -----------------------------
        # Create Roles
        # -----------------------------
        print("👥 Creating roles...")
        roles = {
            "admin": Role(name="admin", description="Administrator with full access"),
            "manager": Role(name="manager", description="Manager responsible for operations"),
            "customer": Role(name="customer", description="Regular customer user"),
        }
        db.session.add_all(roles.values())
        db.session.commit()

        # -----------------------------
        # Create Admin User
        # -----------------------------
        print("🧑‍💻 Creating admin user...")
        admin_user = User(
            name="Admin User",
            email="admin@example.com",
            password=hash_password("pass"),
            fs_uniquifier=str(uuid.uuid4()),
            active=True,
        )
        db.session.add(admin_user)
        db.session.commit()

        db.session.add(UserRoles(user_id=admin_user.id, role_id=roles["admin"].id))
        db.session.commit()

        # -----------------------------
        # Create Managers
        # -----------------------------
        print("👔 Creating manager users...")
        managers = []
        for _ in range(10):
            user = User(
                name=fake.name(),
                email=fake.unique.email(),
                password=hash_password("pass"),
                fs_uniquifier=str(uuid.uuid4()),
                active=True,
            )
            db.session.add(user)
            db.session.flush()

            db.session.add(UserRoles(user_id=user.id, role_id=roles["manager"].id))

            mgr = Manager(
                salary=random.randint(40000, 100000),
                address=fake.address(),
                department=random.choice(["Sales", "Logistics", "HR", "Procurement"]),
                user_id=user.id,
            )
            db.session.add(mgr)
            managers.append(user)

        db.session.commit()

        # -----------------------------
        # Create Customers
        # -----------------------------
        print("🧑‍🤝‍🧑 Creating customer users...")
        customers = []
        for _ in range(50):
            user = User(
                name=fake.name(),
                email=fake.unique.email(),
                password=hash_password("pass"),
                fs_uniquifier=str(uuid.uuid4()),
                active=True,
            )
            db.session.add(user)
            db.session.flush()

            db.session.add(UserRoles(user_id=user.id, role_id=roles["customer"].id))

            cust = Customer(
                loyalty_points=random.randint(0, 1000),
                user_id=user.id,
            )
            db.session.add(cust)
            customers.append(user)

        db.session.commit()

        # -----------------------------
        # Create Sections
        # -----------------------------
        print("📦 Creating product sections...")
        section_names = ["Fruits", "Beverages", "Bakery", "Snacks", "Dairy", "Vegetables"]
        sections = []
        for name in section_names:
            s = Section(name=name)
            db.session.add(s)
            sections.append(s)
        db.session.commit()

        # -----------------------------
        # Create Products
        # -----------------------------
        print("🍎 Creating products...")
        products = []
        for s in sections:
            for _ in range(10):
                product = Product(
                    name=fake.unique.ingredient(),
                    price=round(random.uniform(10, 500), 2),
                    stock=random.randint(10, 200),
                    expiry=datetime.now(timezone.utc) + timedelta(days=random.randint(30, 365)),
                    mfd=datetime.now(timezone.utc) - timedelta(days=random.randint(1, 90)),
                    unit_of_sale=random.choice(["kg", "litre", "unit"]),
                    section_id=s.id,
                )
                db.session.add(product)
                products.append(product)
        db.session.commit()

        # -----------------------------
        # Create Sales Data
        # -----------------------------
        print("💰 Creating sales data over time...")
        sales = []
        now = datetime.now(timezone.utc)
        for _ in range(300):  # 300 random sales
            sale_date = now - timedelta(days=random.randint(0, 180))
            sale_customer = random.choice(customers)
            total_amount = 0

            sale = Sale(
                total_amount=0,  # temporary
                customer_id=sale_customer.id,
                created_at=sale_date,
                updated_at=sale_date,
            )
            db.session.add(sale)
            db.session.flush()

            for _ in range(random.randint(1, 5)):  # 1–5 items per sale
                product = random.choice(products)
                quantity = random.randint(1, 5)
                price = float(product.price)
                total_amount += price * quantity

                sale_item = SaleItem(
                    quantity=quantity,
                    price_at_sale=price,
                    product_id=product.id,
                    sale_id=sale.id,
                    created_at=sale_date,
                    updated_at=sale_date,
                )
                db.session.add(sale_item)

            sale.total_amount = total_amount
            db.session.add(sale)
            sales.append(sale)

        db.session.commit()
        print("✅ Database seeded successfully!")


if __name__ == "__main__":
    seed_data()
