# Employee Management System (Django Web Application)

## Overview

This project is a web-based employee management system built using the Django framework. It combines object-oriented design principles with web development, specifically implementing the Strategy Pattern to handle flexible salary calculations.

The application allows users to create, manage, and view employees through a web interface as well as via Django’s built-in admin panel.

---

## Features

* Create and manage employee records
* Dynamic salary calculation using the Strategy Pattern:

  * Fixed salary model
  * Hourly wage model (hourly rate × hours worked)
* Persistent data storage using SQLite
* Web-based user interface
* Integrated Django admin panel for efficient data management

---

## Technologies

* Python 3.13.0
* Django
* SQLite (default database)
* HTML (Django Templates)

---

## Project Structure

```
DjangoProject/
│
├── manage.py
├── DjangoProject/
│   ├── settings.py
│   ├── urls.py
│
└── staff/
    ├── models.py
    ├── views.py
    ├── urls.py
    ├── templates/
    │   └── staff/
    │       ├── liste.html
    │       └── form.html
    |       └── confirm_delete.html
    └── management/
    |    └── commands
    |      └── populate_staff.py
           
```

---

## Installation & Setup

### 1. Activate virtual environment

```
.venv\Scripts\activate
```

### 2. Install dependencies

```
pip install django
```

### 3. Apply migrations

```
python manage.py makemigrations
python manage.py migrate
```

### 4. Create admin user

```
python manage.py createsuperuser
```

### 5. Run development server

```
using lauch.json in the order that contains manage.py with the argument runserver 
```

---

## Access

* Application:
  http://127.0.0.1:8000/

* Admin Interface:
  http://127.0.0.1:8000/admin/

---

## Architecture

The application is based on the Strategy Pattern to encapsulate different salary calculation logics:

* **FixedSalaryModel**: constant salary
* **WorkerModel**: salary based on hourly rate and working hours

This logic is integrated into Django models and/or service classes, allowing dynamic salary computation.

---

## Django App: `staff`

The core functionality is implemented inside the `staff` app.

### Responsibilities of the `staff` app:

* Defines the **database models** (`models.py`) for employees
* Implements **views** (`views.py`) for rendering web pages
* Manages **URL routing** (`urls.py`)
* Manages **Forms** ('forms.py') for data input
* Provides **templates** for frontend rendering

The app follows Django’s modular design approach, keeping business logic, database structure, and presentation cleanly separated.

---

## Possible Extensions

* REST API integration with Django REST Framework
* Authentication and user roles
* Frontend improvements using Bootstrap or React
* Advanced filtering and search functionality
* Exceptions-Validations of employee input data

---

## Notes

* The project is configured for development (`DEBUG = True`)
* Production deployment requires additional security and configuration adjustments

---

## Author

This project was developed as part of a software engineering exercise, combining object-oriented programming concepts (Strategy Pattern) with modern web development using Django.
