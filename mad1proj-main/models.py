# Models
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
# Import db from extensions.py
from app import app
db = SQLAlchemy(app)

# Customer Model
class Customer(db.Model):
    __tablename__ = 'customer'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    passhash = db.Column(db.String(256), nullable=False)
    full_name = db.Column(db.String(120), nullable=False)
    address = db.Column(db.String(255), nullable=False)
    city = db.Column(db.String(100), nullable=False)
    pincode = db.Column(db.String(10), nullable=False)
    phone_number = db.Column(db.String(15), nullable=False)
    is_admin = db.Column(db.Boolean, nullable=False, default=False)

    def set_password(self, password): # used in register
        self.passhash = generate_password_hash(password) 
    def check_password(self, password): # used in login
        return check_password_hash(self.passhash, password)

    service_requests = db.relationship('ServiceRequest', backref='customer', lazy=True)

def create_admin_if_not_exists():
    admin = Customer.query.filter_by(email="admin@gmail.com").first()
    if not admin:
        admin = Customer(
            email="admin@gmail.com",
            full_name="admin",
            address="Admin Address",
            city="Admin City",
            pincode="000000",
            phone_number="0000000000",
            is_admin=True
        )
        admin.set_password("admin")
        db.session.add(admin)
        db.session.commit()
        print("Admin user created successfully")
def reset_professional_table():
    with app.app_context():
        # Drop only the professional table
        Professional.__table__.drop(db.engine)
        # Recreate only the professional table
        Professional.__table__.create(db.engine)
        print("Professional table reset successfully")  

# Update your database initialization
# Professional Model
class Professional(db.Model):
    __tablename__ = 'professional'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    passhash = db.Column(db.String(256), nullable=False)
    full_name = db.Column(db.String(120), nullable=False)
    city = db.Column(db.String(100), nullable=False)
    pincode = db.Column(db.String(10), nullable=False)
    phone_number = db.Column(db.String(15), nullable=False)
    service_package_id = db.Column(db.Integer, db.ForeignKey('service_package.id'), nullable=False)
    experience = db.Column(db.Integer, nullable=False)
    document = db.Column(db.String(255), nullable=False)
    status = db.Column(db.String(50), nullable=False, default="pending")

    service_requests = db.relationship('ServiceRequest', backref='professional', lazy=True)
    rejected_requests = db.relationship('RejectedServiceRequest', backref='professional', lazy=True)

# ServiceCategory Model
class ServiceCategory(db.Model):
    __tablename__ = 'service_category'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)

    service_packages = db.relationship('ServicePackage', backref='service_category', lazy=True, cascade="all, delete-orphan")

# ServicePackage Model
class ServicePackage(db.Model):
    __tablename__ = 'service_package'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    price = db.Column(db.Float, nullable=False)
    service_category_id = db.Column(db.Integer, db.ForeignKey('service_category.id'), nullable=False)
    time = db.Column(db.Integer, nullable=False)  # Time in hours
    description = db.Column(db.Text, nullable=False)

    service_requests = db.relationship('ServiceRequest', backref='service_package', lazy=True)

# ServiceRequest Model
class ServiceRequest(db.Model):
    __tablename__ = 'service_request'
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=False)
    professional_id = db.Column(db.Integer, db.ForeignKey('professional.id'), nullable=True)  # Null until assigned
    service_package_id = db.Column(db.Integer, db.ForeignKey('service_package.id'), nullable=False)
    status = db.Column(db.String(50), nullable=False, default="requested")  # requested, assigned, completed
    date_of_request = db.Column(db.DateTime, nullable=False)
    date_of_completion = db.Column(db.DateTime, nullable=True)
    rating = db.Column(db.Float, nullable=True)
    remarks = db.Column(db.Text, nullable=True)

# CustomerLogs Model
class CustomerLogs(db.Model):
    __tablename__ = 'customer_logs'
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=False)  # Foreign key to Customer table
    action = db.Column(db.String(50), nullable=False)  # Action performed: create, update, delete
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    details = db.Column(db.Text, nullable=True)  # Additional details about the change

    # Relationship to the Customer model
    customer = db.relationship('Customer', backref=db.backref('logs', lazy=True))
    
    
# RejectedServiceRequest Model
class RejectedServiceRequest(db.Model):
    __tablename__ = 'rejected_service_request'
    id = db.Column(db.Integer, primary_key=True)
    service_request_id = db.Column(db.Integer, db.ForeignKey('service_request.id'), nullable=False)
    professional_id = db.Column(db.Integer, db.ForeignKey('professional.id'), nullable=False)

with app.app_context():
    db.create_all()
    create_admin_if_not_exists()