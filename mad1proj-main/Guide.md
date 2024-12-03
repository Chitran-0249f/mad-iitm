```
Project Root Folder
├── Code
│   ├── Folder 1
│   │   ├── auth.py               # Authentication-related functions and routes (e.g., login, registration)
│   │   └── admin_dashboard.py     # Admin dashboard logic, including user management and service handling
│   ├── Folder 2
│   │   ├── Folder 3
│   │   │   ├── service_requests.py  # Logic for creating, updating, and managing service requests
│   │   │   └── professional_view.py # Views and actions for service professionals (e.g., accept/reject requests)
│   │   ├── customer_dashboard.py    # Customer dashboard logic, including search and request creation
│   │   └── services.py              # Logic for service CRUD operations (e.g., create, update, delete services)
│   ├── app.py                     # Main application file with Flask app configuration and route setup
│   ├── config.py                  # Configuration file for Flask settings, database URIs, etc.
│   ├── models.py                  # Database models (User, Service, ServiceRequest, etc.) and relationships
│   ├── utils.py                   # Utility functions (e.g., validations, helper functions for views)
│   ├── requirements.txt           # List of project dependencies (Flask, SQLite, Jinja2, etc.)
│   ├── README.md                  # Overview of the project, setup instructions, and features
│   └── templates                  # Folder for HTML templates
│       ├── base.html              # Base layout template for consistent styling across pages
│       ├── admin_dashboard.html   # Admin dashboard view
│       ├── customer_dashboard.html # Customer dashboard view
│       ├── professional_dashboard.html # Service professional dashboard view
│       └── login.html             # Login form for all users
│   └── static                     # Folder for CSS, JavaScript, and image files
│       ├── css
│       │   └── style.css          # Custom CSS for styling the application
│       └── js
│           └── scripts.js         # Custom JavaScript for client-side interactivity and validation
└── Project Report.pdf             # Project report document with details on implementation, ER diagram, and API endpoints
```

original
Project Root Folder
├── Code
│ ├── Folder 1
│ │ ├── file3.py
│ │ └── file4.py
│ ├── Folder 2
│ │ ├── Folder 3
│ │ │ ├── file7.py
│ │ │ └── file8.py
│ │ ├── file5.py
│ │ └── file6.py
│ ├── file1.py
│ └── file2.py
└── Project Report.pdf how would thsi look at the end


### ER Diagram
Database schema:
1. Customer
    - id
    - Email
    - passhash
    - Full Name
    - Address
    - City
    - pincode
    - phone number
2. Professional
    - id
    - Email
    - passhash
    - Full Name
    - City
    - pincode
    - phone number
    - Service Type
    - Experience
    - Document
    - Status (pending, approved, rejected)
3. ServiceCategory
    - id
    - Name (cleaning, plumbing, etc.)
4. ServicePackage
    - id
    - Name
    - Price
    - Service Category (id)
    - Time (in hours)
    - Description
    - db.relationship('ServiceCategory', backref='service_packages', lazy=True, cascade="all, delete-orphan")
4. ServiceRequest
    - id
    - Customer (id)
    - Professional (id)
    - Service Package (id)
    - Status (Requested, assigned, completed)
    - Date of Request
    - Date of Completion
    - Rating
    - remarks
5. RejectedServiceRequest
    - id
    - Service Request (id)
    - Professional (id)
    - So that a professional doesn't see a request that he has rejected

find the project statement at : https://docs.google.com/document/u/1/d/1waf_CKBLk25fkwF-R4KS7wLq4KTIPhUcAtj6if5N-zo/pub