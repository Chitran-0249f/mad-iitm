# professional_view/service_request.py
from flask import Blueprint, redirect, url_for, session, flash
from models import ServiceRequest, RejectedServiceRequest, Professional, db
from datetime import datetime

service_requests = Blueprint('service_requests', __name__)

@service_requests.before_request
def check_professional_login():
    if 'professional_id' not in session:
        return redirect(url_for('auth.login'))

@service_requests.route('/accept/<int:request_id>')
def accept_request(request_id):
    professional_id = session.get('professional_id')
    professional = Professional.query.get(professional_id)
    
    if professional.status != 'approved':
        flash('Your account must be approved to accept requests.', 'danger')
        return redirect(url_for('professional_view.dashboard'))
    
    service_request = ServiceRequest.query.get_or_404(request_id)
    
    # Check if request matches professional's service package
    if service_request.service_package_id != professional.service_package_id:
        flash('This service request does not match your service package.', 'danger')
        return redirect(url_for('professional_view.dashboard'))
    
    if service_request.professional_id is not None:
        flash('This request has already been assigned.', 'warning')
        return redirect(url_for('professional_view.dashboard'))
    
    # Check if professional has previously rejected this request
    previously_rejected = RejectedServiceRequest.query.filter_by(
        service_request_id=request_id,
        professional_id=professional_id
    ).first()
    
    if previously_rejected:
        flash('You cannot accept a request you previously rejected.', 'danger')
        return redirect(url_for('professional_view.dashboard'))
    
    service_request.professional_id = professional_id
    service_request.status = 'assigned'
    db.session.commit()
    
    flash('Request accepted successfully!', 'success')
    return redirect(url_for('professional_view.dashboard'))

@service_requests.route('/reject/<int:request_id>')
def reject_request(request_id):
    professional_id = session.get('professional_id')
    service_request = ServiceRequest.query.get_or_404(request_id)
    
    # Check if request is already assigned
    if service_request.professional_id is not None:
        flash('Cannot reject an already assigned request.', 'danger')
        return redirect(url_for('professional_view.dashboard'))
    
    # Check if already rejected by this professional
    existing_rejection = RejectedServiceRequest.query.filter_by(
        service_request_id=request_id,
        professional_id=professional_id
    ).first()
    
    if existing_rejection:
        flash('You have already rejected this request.', 'warning')
        return redirect(url_for('professional_view.dashboard'))
    
    # Create rejected request record
    rejected_request = RejectedServiceRequest(
        service_request_id=request_id,
        professional_id=professional_id
    )
    db.session.add(rejected_request)
    db.session.commit()
    
    flash('Request rejected successfully.', 'info')
    return redirect(url_for('professional_view.dashboard'))

@service_requests.route('/complete/<int:request_id>')
def complete_request(request_id):
    professional_id = session.get('professional_id')
    service_request = ServiceRequest.query.get_or_404(request_id)
    
    if service_request.professional_id != professional_id:
        flash('You can only complete requests assigned to you.', 'danger')
        return redirect(url_for('professional.dashboard'))
    
    if service_request.status != 'assigned':
        flash('Only assigned requests can be marked as completed.', 'warning')
        return redirect(url_for('professional_view.dashboard'))
    
    service_request.status = 'completed'
    service_request.date_of_completion = datetime.now()
    db.session.commit()
    
    flash('Request marked as completed successfully!', 'success')
    return redirect(url_for('professional.dashboard'))