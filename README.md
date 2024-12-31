# Operations Tracking System (OTS) for Hexa Steel®

A comprehensive system for tracking operations, including material management, production logging, and quality control. Built with Django and designed for future integration with ERP systems like Odoo or Dolibarr.

## Features

- Material Management
- Production Process Tracking
- Project Management
- Production Logging
- Quality Control
- Material Usage Tracking

## Tech Stack

- Python 3.12
- Django 5.1.4
- Django REST Framework
- MySQL Database

## Installation

1. Clone the repository
2. Create a virtual environment:
   ```bash
   python -m venv venv
   ```
3. Activate the virtual environment:
   - Windows: `venv\Scripts\activate`
   - Linux/Mac: `source venv/bin/activate`

4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

5. Create a `.env` file with the following variables:
   ```env
   DEBUG=True
   SECRET_KEY=your-secret-key
   DB_NAME=ots_django
   DB_USER=your-db-user
   DB_PASSWORD=your-db-password
   DB_HOST=localhost
   DB_PORT=3306
   ```

6. Create the database:
   ```sql
   CREATE DATABASE ots_django CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
   ```

7. Apply migrations:
   ```bash
   python manage.py migrate
   ```

8. Create a superuser:
   ```bash
   python manage.py createsuperuser
   ```

## Running the Application

1. Start the development server:
   ```bash
   python manage.py runserver
   ```

2. Access the admin interface at `http://localhost:8000/admin`

## Project Structure

- `core/` - Main application directory
  - `models.py` - Database models
  - `admin.py` - Admin interface configuration
  - `views.py` - View logic
  - `urls.py` - URL routing

## Models

1. Material
   - Name, code, description, unit
   - Quantity and minimum stock tracking

2. ProductionProcess
   - Name, code, description
   - Standard time for the process

3. Project
   - Name, code, description
   - Status tracking
   - Start and end dates

4. ProductionLog
   - Links to Project and Process
   - Operator tracking
   - Start and end times
   - Quantity produced

5. QualityCheck
   - Links to ProductionLog
   - Inspector tracking
   - Measurements and specifications
   - Pass/Fail results

6. MaterialUsage
   - Links to ProductionLog and Material
   - Quantity used tracking

## Future Integration

The system is designed to be compatible with ERP systems like Odoo and Dolibarr through:
- Consistent data models
- REST API endpoints
- Standard authentication mechanisms
