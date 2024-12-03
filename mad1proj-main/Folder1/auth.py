from flask import Blueprint, request, redirect, url_for, session, render_template, flash, current_app as app
from werkzeug.security import check_password_hash, generate_password_hash
from models import db, Customer, Professional, ServicePackage
from werkzeug.utils import secure_filename
import os


auth_blueprint = Blueprint('auth', __name__)

@auth_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        # Check admin credentials
        admin = Customer.query.filter_by(email=email, is_admin=True).first()
        if admin and admin.check_password(password):
            session['user_id'] = admin.id
            session['role'] = 'admin'
            flash('Logged in successfully', 'success')
            return redirect(url_for('admin.dashboard'))

        # Check customer credentials
        customer = Customer.query.filter_by(email=email, is_admin=False).first()
        if customer and customer.check_password(password):
            session['user_id'] = customer.id
            session['role'] = 'customer'
            flash('Logged in successfully', 'success')
            return redirect(url_for('customer_view.dashboard'))

        # Check professional credentials
        professional = Professional.query.filter_by(email=email).first()
        if professional and check_password_hash(professional.passhash, password):
            session['professional_id'] = professional.id
            session['user_id']=professional.id
            session['role'] = 'professional'
            flash('Logged in successfully', 'success')
            return redirect(url_for('professional_view.dashboard'))

        # If no match, raise an error
        error = "Invalid email or password."
        flash(error, 'danger')
        return render_template('login.html')
    return render_template('login.html')


@auth_blueprint.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        full_name = request.form.get('full_name')
        phone_number = request.form.get('phone_number')
        address = request.form.get('address')
        city = request.form.get('city')
        pincode = request.form.get('pincode')
        if Customer.query.filter_by(email=email).first():
            flash('Email already exists', 'danger')
            return redirect(url_for('auth.register'))
        if Customer.query.filter_by(phone_number=phone_number).first():
            flash('Phone number already associated with another account', 'danger')
            return redirect(url_for('auth.register'))
        customer = Customer(email=email, passhash= generate_password_hash(password), full_name=full_name, phone_number=phone_number, address=address, city=city, pincode=pincode, is_admin=False)
        db.session.add(customer)
        db.session.commit()
        return redirect(url_for('auth.login'))
    return render_template('register.html')
        
        
@auth_blueprint.route('/register/professional', methods=['GET', 'POST'])
def register_professional():
    services = ServicePackage.query.all()
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        full_name = request.form.get('full_name')
        phone_number = request.form.get('phone_number')
        city = request.form.get('city')
        pincode = request.form.get('pincode')
        service_package_id = request.form.get('service_package_id')
        experience = request.form.get('experience')
        if Professional.query.filter_by(email=email).first():
            flash('Email already exists', 'danger')
            return redirect(url_for('auth.register_professional'))
        if Professional.query.filter_by(phone_number=phone_number).first():
            flash('Phone number already associated with another account', 'danger')
            return redirect(url_for('auth.register_professional'))

        file_path = None
        
        if 'document' in request.files:
            file = request.files['document']
            if file.filename != '' and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(file_path)
            else:
                flash('Please upload a valid file (pdf, jpg, jpeg, or png)', 'danger')
                return redirect(request.url)
        else:
            flash('Document upload is required', 'danger')
            return redirect(request.url)

        professional = Professional(
            email=email,
            passhash=generate_password_hash(password),
            full_name=full_name,
            phone_number=phone_number,
            city=city,
            pincode=pincode,
            service_package_id=service_package_id,
            experience=experience,
            document=file_path
        )   
        db.session.add(professional)
        db.session.commit()
        flash('Registration successful', 'success')
        return redirect(url_for('auth.login'))
    return render_template('register_professional.html', services=services)

def allowed_file(filename):
    ALLOWED_EXTENSIONS = {'pdf', 'jpg', 'jpeg', 'png'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@auth_blueprint.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('auth.login'))