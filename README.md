# Django Project

## Overview

This Django project is designed to demonstrate a web application with role-based access control and real-time WebSocket notifications. The project uses Django REST Framework (DRF) for building APIs and PostgreSQL for database management. JWT authentication is implemented for secure login functionality.

## Features

- **Role-Based Access Control:** Different user roles with distinct permissions.
- **Real-Time Notifications:** WebSocket support for real-time updates.
- **JWT Authentication:** Secure user authentication with JSON Web Tokens.
- **PostgreSQL Database:** Robust and scalable database management.

## Getting Started

### Prerequisites

- Python 3.8 or higher
- Django 5.1 or higher
- Django REST Framework
- PostgreSQL
- pip

### Installation

STEP 1:
python -m venv env

<!-- Window CMD -->
cd env\scripts
activate

<!-- Ubuntu -->
source env\scripts\activate


STEP 2:
pip install -r requirements.txt

STEP 3:
python manage.py makemigrations

STEP 4:
python manage.py migrate

STEP 5:
python manage.py createsuperuser

username = Admin
password = Admin@123