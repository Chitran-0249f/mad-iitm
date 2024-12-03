from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy



app = Flask(__name__) # create a flask app, named app

import config
import models
from Folder1.auth import auth_blueprint
from Folder1.admin_dashboard import admin_blueprint
from Folder2.customer_view import customer_view
from Folder2.Folder3.professional_view import professional_view
from Folder2.Folder3.service_requests import service_requests
from Folder2.services import customer_services

@app.route('/')
def home():
    return redirect(url_for('auth.login'))

app.register_blueprint(auth_blueprint, url_prefix='/auth')
app.register_blueprint(admin_blueprint, url_prefix='/admin')
app.register_blueprint(customer_view, url_prefix='/customer')
app.register_blueprint(professional_view, url_prefix='/professional')
app.register_blueprint(service_requests, url_prefix='/service_requests')
app.register_blueprint(customer_services)
app.config['UPLOAD_FOLDER'] = 'static/uploads'
if __name__ == "__main__":
    app.run(debug=True)
