from flask import Blueprint, render_template, session, redirect, url_for, request, flash
from models import db, ServiceCategory, Professional, Customer, ServicePackage, ServiceRequest
from datetime import datetime

customer_view = Blueprint('customer_view', __name__)

@customer_view.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    
    categories = ServiceCategory.query.all()
    service_requests = ServiceRequest.query.filter_by(customer_id=session['user_id']).all()
    
    return render_template('dashboard/customer_dashboard.html', 
                         categories=categories,
                         service_requests=service_requests)



@customer_view.route('/summary')
def summary():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    
    requests = ServiceRequest.query.filter_by(customer_id=session['user_id'])
    total_requests = requests.count()
    ongoing_requests = requests.filter_by(status='requested').count()
    completed_requests = requests.filter_by(status='completed').count()
    cancelled_requests = requests.filter_by(status='cancelled').count()
    
    return render_template('customer/customer_summary.html',
                         total=total_requests,
                         ongoing=ongoing_requests,
                         completed=completed_requests,
                         cancelled=cancelled_requests)


@customer_view.route('/category/<int:category_id>')
def view_category_services(category_id):
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    
    category = ServiceCategory.query.get_or_404(category_id)
    return render_template('category_services.html', category=category)



@customer_view.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        service_package = request.form.get('service_package')
        customer_id = session.get('user_id')
        customer = Customer.query.get(customer_id)
        

        # Debugging: Check customer and city
        if customer:
            print(f"Customer Details: {customer}")
            print(f"Customer's City: {customer.city}")
        else:
            print("No customer found for the given ID.")
            flash("Customer not found.", "danger")
            return render_template('search.html')

        # Query for service requests filtered by service package name and city
        try:
            service_request = (
                ServiceRequest.query
                .join(Professional)  # Join with the Professional table
                .join(ServicePackage, Professional.service_package_id == ServicePackage.id)  # Join with ServicePackage
                .filter(ServicePackage.name == service_package)  # Filter by service package name
                .filter(Customer.city == customer.city)  # Filter by customer's city
                .first()
            )

            # Debugging: Print the resulting service request
            if service_request:
                print(f"Service Request Found: {service_request}")
            else:
                print("No matching service request found.")
        except Exception as e:
            print(f"Error while querying service request: {e}")
            flash("An error occurred while processing the request.", "danger")
            return render_template('search.html')

        # Flash a warning if no service request was found
        if not service_request:
            flash('Service request not found or you do not have access to it.', 'warning')

        return render_template('search.html',
                             service_request=service_request)
    
    return render_template('search.html')



