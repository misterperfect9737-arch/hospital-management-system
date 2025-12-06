# Hospital Management System - Project Report

## Student Information
- **Name:** [Your Name]
- **Roll Number:** [Your Roll Number]
- **Course:** Modern Application Development

## Project Overview
This is a Hospital Management System built with Flask that manages patients, doctors, and appointments with role-based access control.

## AI/LLM Usage Declaration
**Percentage of AI/LLM used in this project:** [Specify percentage, e.g., 30%]

**How AI was used:**
- Code structure and boilerplate generation
- Debugging assistance
- Documentation writing
- Learning Flask concepts

**What I implemented myself:**
- Database schema design
- Business logic for appointments
- User interface design
- Feature integration
- Testing and bug fixes

## Technologies Used
- **Backend:** Flask 3.0 (Python web framework)
- **Database:** SQLite with SQLAlchemy ORM
- **Authentication:** Flask-Login with Werkzeug password hashing
- **Frontend:** HTML5, CSS3, JavaScript, Bootstrap 5
- **Icons:** Font Awesome 6

## Features Implemented

### Admin Features
- Dashboard with statistics (doctors, patients, appointments)
- Add, edit, and deactivate doctors
- Manage patient records
- View and manage all appointments
- Search functionality for doctors and patients

### Doctor Features
- Personal dashboard with appointment statistics
- View upcoming and past appointments
- Set availability schedule
- Complete appointments with diagnosis and prescriptions
- View patient medical history
- Cancel appointments

### Patient Features
- Browse doctors by department (6 departments)
- Search doctors by name or specialization
- Book appointments with available doctors
- View upcoming appointments
- Cancel booked appointments
- Access complete medical history
- Update personal profile

## Database Schema

### Tables (7 total):
1. **User** - Authentication and basic user info
2. **Department** - Medical departments/specializations
3. **Doctor** - Doctor-specific information
4. **Patient** - Patient-specific information
5. **Appointment** - Appointment bookings
6. **Treatment** - Medical records and prescriptions
7. **DoctorAvailability** - Doctor availability schedule

### Relationships:
- User → Doctor (one-to-one)
- User → Patient (one-to-one)
- Department → Doctor (one-to-many)
- Doctor → Appointment (one-to-many)
- Patient → Appointment (one-to-many)
- Appointment → Treatment (one-to-one)
- Doctor → DoctorAvailability (one-to-many)

## Key Functionalities

### Authentication & Authorization
- Secure password hashing using Werkzeug
- Session-based authentication with Flask-Login
- Role-based access control (Admin, Doctor, Patient)
- Protected routes with @login_required decorator

### Appointment Management
- Conflict prevention (checks for existing appointments)
- Date and time validation
- Status tracking (Booked, Completed, Cancelled)
- Doctor availability checking

### Search & Filter
- Search doctors by name or specialization
- Filter appointments by status
- Search patients by name, email, or phone

### Data Validation
- Frontend validation with HTML5
- Backend validation in routes
- Email format validation
- Phone number validation
- Date validation (no past dates for appointments)

## Security Features
- Password hashing (not stored in plain text)
- Session management
- CSRF protection
- Input sanitization
- Role-based access control

## Challenges Faced
1. **Appointment Conflict Prevention:** Implemented database queries to check for existing appointments at the same time
2. **Role-Based Access:** Created middleware to ensure users can only access their authorized routes
3. **Database Relationships:** Properly set up foreign keys and cascading deletes
4. **Date/Time Handling:** Managed timezone-aware datetime objects

## Future Enhancements
- Email notifications for appointments
- Payment integration for consultation fees
- Video consultation feature
- Prescription PDF generation
- SMS reminders
- Advanced analytics dashboard

## Installation & Setup

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Installation Steps
```bash
# Install dependencies
pip install -r requirements.txt

# Run application
python app.py

# Access at http://localhost:5000
```

### Default Credentials
- **Admin:** admin / admin123
- **Doctor:** dr.smith / doctor123

## Project Structure
```
hospital-management-system/
├── app.py                 # Main application
├── models.py              # Database models
├── routes.py              # Application routes
├── requirements.txt       # Dependencies
├── static/
│   ├── css/
│   │   └── style.css     # Custom styles
│   └── js/
│       └── main.js       # JavaScript
└── templates/
    ├── base.html         # Base template
    ├── index.html        # Homepage
    ├── login.html        # Login page
    ├── register.html     # Registration
    ├── admin/            # Admin templates
    ├── doctor/           # Doctor templates
    └── patient/          # Patient templates
```

## Testing
- Tested all user roles (Admin, Doctor, Patient)
- Verified appointment booking and completion
- Tested search and filter functionality
- Validated form inputs
- Checked database integrity
- Tested on multiple browsers

## Conclusion
This Hospital Management System successfully implements all required features with a clean, user-friendly interface. The application demonstrates proper use of Flask framework, database design, authentication, and role-based access control.

## GitHub Repository
[Add your GitHub repository link here]

## Declaration
I declare that this project was completed by me with the assistance of AI tools as mentioned above. All core logic and implementation decisions were made by me.

**Date:** [Current Date]
**Signature:** [Your Name]
