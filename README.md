# Hospital Management System

A modern, feature-rich Hospital Management System built with Flask, featuring role-based access control for Admins, Doctors, and Patients.

## Features

### Admin Features
- Dashboard with statistics (total doctors, patients, appointments)
- Add, edit, and deactivate doctor profiles
- Manage patient records
- View and manage all appointments
- Search functionality for doctors and patients

### Doctor Features
- Personal dashboard with appointment statistics
- View upcoming and past appointments
- Set availability for the next 7 days
- Complete appointments with diagnosis and prescriptions
- View patient medical history
- Cancel appointments

### Patient Features
- Browse doctors by department and specialization
- Search doctors by name or specialization
- Book appointments with available doctors
- View upcoming appointments
- Cancel booked appointments
- Access complete medical history with diagnoses and prescriptions
- Update personal profile

### Technical Features
- RESTful API endpoints for appointments and doctors
- Responsive design with Bootstrap 5
- Smooth animations and transitions
- Form validation (frontend and backend)
- Secure password hashing
- SQLite database with programmatic creation
- Role-based access control
- Conflict prevention for appointment booking

## Installation

1. Install Python 3.8 or higher

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
python app.py
```

4. Access the application at `http://localhost:5000`

## Default Credentials

**Admin Account:**
- Username: `admin`
- Password: `admin123`

## Database

The database is created automatically on first run. No manual setup required.

### Database Schema

- **User**: Stores user credentials and basic info
- **Department**: Medical departments/specializations
- **Doctor**: Doctor-specific information
- **Patient**: Patient-specific information
- **Appointment**: Appointment bookings
- **Treatment**: Medical records and prescriptions
- **DoctorAvailability**: Doctor availability schedule

## API Endpoints

### Appointments
- `GET /api/appointments` - List appointments (with filters)
- `GET /api/appointments/<id>` - Get appointment details
- `POST /api/appointments` - Create appointment
- `PUT /api/appointments/<id>` - Update appointment
- `DELETE /api/appointments/<id>` - Cancel appointment

### Doctors
- `GET /api/doctors` - List doctors (with filters)

## Project Structure

```
hospital-management-system/
├── app.py                 # Main application file
├── models.py              # Database models
├── routes.py              # Application routes
├── requirements.txt       # Python dependencies
├── static/
│   ├── css/
│   │   └── style.css     # Custom styles
│   └── js/
│       └── main.js       # JavaScript functionality
└── templates/
    ├── base.html         # Base template
    ├── index.html        # Landing page
    ├── login.html        # Login page
    ├── register.html     # Registration page
    ├── admin/            # Admin templates
    ├── doctor/           # Doctor templates
    └── patient/          # Patient templates
```

## Technologies Used

- **Backend**: Flask 3.0
- **Database**: SQLite with SQLAlchemy ORM
- **Authentication**: Flask-Login
- **Frontend**: HTML5, CSS3, JavaScript
- **UI Framework**: Bootstrap 5
- **Icons**: Font Awesome 6

## Security Features

- Password hashing with Werkzeug
- Session-based authentication
- Role-based access control
- CSRF protection
- Input validation

## Browser Support

- Chrome (latest)
- Firefox (latest)
- Safari (latest)
- Edge (latest)

## License

This project is created for educational purposes.
