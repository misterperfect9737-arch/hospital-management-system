# HOSPITAL MANAGEMENT SYSTEM - PROJECT REPORT

---

## STUDENT DETAILS

**Name:** KANDUKURU VENKATA SRI KOUSHIK  
**Roll Number:** 24f2006882 
**Course:** IITM Degree in Data Science and Applications  
**Project Title:** Hospital Management System  
**Submission Date:** 16-nov-2025

---

## PROJECT DETAILS

### Problem Statement

Hospitals need efficient systems to manage patients, doctors, appointments, and treatments. Currently, many hospitals use manual registers or disconnected software, which makes it difficult to manage records, avoid scheduling conflicts, and track patient history.

### Solution Approach

I developed a comprehensive Hospital Management System (HMS) web application that allows Admins, Doctors, and Patients to interact with the system based on their roles. The system provides:

- **Role-based access control** for three user types
- **Centralized database** for all hospital data
- **Automated appointment scheduling** with conflict prevention
- **Digital medical records** with complete treatment history
- **Intuitive user interface** for easy navigation

### Technical Architecture

**Backend:**
- Flask 3.0 framework for application logic
- SQLAlchemy ORM for database operations
- Flask-Login for authentication and session management
- Werkzeug for password hashing

**Frontend:**
- Jinja2 templating engine
- HTML5 and CSS3
- Bootstrap 5.3 for responsive design
- JavaScript for interactive features
- Font Awesome icons

**Database:**
- SQLite database created programmatically
- 7 interconnected tables with proper relationships
- Automatic initialization with admin and sample data

---

## AI/LLM DECLARATION

**AI/LLM Usage:** Yes

**Extent of Use:**
- Used AI assistance (Kiro IDE) for code generation and debugging
- AI helped with:
  - Database schema design
  - Route implementation
  - Template creation
  - CSS styling and animations
  - Bug fixing and optimization
- All code was reviewed, tested, and customized for this project
- Understanding of Flask, SQLAlchemy, and web development concepts was enhanced through AI-assisted learning

---

## FRAMEWORKS AND LIBRARIES USED

### Backend Frameworks
- **Flask 3.0.0** - Web application framework
- **Flask-SQLAlchemy 3.1.1** - ORM for database operations
- **Flask-Login 0.6.3** - User session management
- **Werkzeug 3.0.1** - Password hashing and security

### Frontend Frameworks
- **Bootstrap 5.3.0** - Responsive UI framework
- **Font Awesome 6.4.0** - Icon library
- **Jinja2** - Template engine (included with Flask)

### Database
- **SQLite** - Lightweight relational database

### Additional Technologies
- **HTML5** - Markup language
- **CSS3** - Styling with custom animations
- **JavaScript** - Client-side interactivity

---

## DATABASE ER DIAGRAM

```
┌─────────────┐
│    User     │
├─────────────┤
│ id (PK)     │
│ username    │
│ email       │
│ password    │
│ role        │
│ full_name   │
│ phone       │
│ is_active   │
└──────┬──────┘
       │
       ├──────────────────┬──────────────────┐
       │                  │                  │
┌──────▼──────┐    ┌──────▼──────┐   ┌──────▼──────┐
│   Doctor    │    │   Patient   │   │    Admin    │
├─────────────┤    ├─────────────┤   └─────────────┘
│ id (PK)     │    │ id (PK)     │
│ user_id(FK) │    │ user_id(FK) │
│ dept_id(FK) │    │ dob         │
│ special.    │    │ gender      │
│ qualif.     │    │ blood_group │
│ experience  │    │ address     │
│ fee         │    │ emergency   │
└──────┬──────┘    └──────┬──────┘
       │                  │
       │    ┌─────────────▼──────────────┐
       │    │      Appointment           │
       │    ├────────────────────────────┤
       └────► id (PK)                    │
            │ patient_id (FK)            │
            │ doctor_id (FK)             │
            │ appointment_date           │
            │ appointment_time           │
            │ status                     │
            │ reason                     │
            └──────┬─────────────────────┘
                   │
            ┌──────▼──────┐
            │  Treatment  │
            ├─────────────┤
            │ id (PK)     │
            │ appt_id(FK) │
            │ diagnosis   │
            │ prescription│
            │ notes       │
            └─────────────┘

┌──────────────┐         ┌────────────────────┐
│ Department   │◄────────│ DoctorAvailability │
├──────────────┤         ├────────────────────┤
│ id (PK)      │         │ id (PK)            │
│ name         │         │ doctor_id (FK)     │
│ description  │         │ date               │
└──────────────┘         │ start_time         │
                         │ end_time           │
                         │ is_available       │
                         └────────────────────┘
```

### Table Relationships:
- User → Doctor (One-to-One)
- User → Patient (One-to-One)
- Department → Doctor (One-to-Many)
- Doctor → Appointment (One-to-Many)
- Patient → Appointment (One-to-Many)
- Appointment → Treatment (One-to-One)
- Doctor → DoctorAvailability (One-to-Many)

---

## API RESOURCE ENDPOINTS

### Appointment APIs

**GET /api/appointments**
- Description: Retrieve appointments with filters
- Parameters: status, doctor_id, patient_id
- Response: JSON array of appointments

**GET /api/appointments/<id>**
- Description: Get specific appointment details
- Response: JSON object with appointment and treatment data

**POST /api/appointments**
- Description: Create new appointment
- Body: patient_id, doctor_id, date, time, reason
- Response: Success message with appointment ID

**PUT /api/appointments/<id>**
- Description: Update appointment status or details
- Body: status, date, time
- Response: Success message

**DELETE /api/appointments/<id>**
- Description: Cancel appointment
- Response: Success message

### Doctor APIs

**GET /api/doctors**
- Description: List all active doctors
- Parameters: specialization (optional)
- Response: JSON array of doctors with details

---

## KEY FEATURES IMPLEMENTED

### Admin Features
✓ Pre-created admin account (programmatic)
✓ Dashboard with statistics (doctors, patients, appointments)
✓ Add/Edit/Delete doctor profiles
✓ View and manage all appointments
✓ Search doctors by name/specialization
✓ Search patients by name/email/phone
✓ Edit patient information
✓ Deactivate doctors and patients

### Doctor Features
✓ Login and personalized dashboard
✓ View upcoming appointments for day/week
✓ List of assigned patients
✓ Mark appointments as Completed/Cancelled
✓ Enter diagnosis, prescriptions, and notes
✓ View patient medical history
✓ Set availability for next 7 days

### Patient Features
✓ Self-registration and login
✓ Dashboard with all departments
✓ Search doctors by specialization
✓ View doctor profiles and availability
✓ Book appointments with date/time selection
✓ Cancel appointments
✓ View appointment history
✓ Access medical records with diagnosis
✓ Edit profile information

### Core Functionalities
✓ Prevent double bookings (conflict detection)
✓ Dynamic status updates (Booked → Completed → Cancelled)
✓ Comprehensive search functionality
✓ Complete medical record storage
✓ Treatment history tracking
✓ Password hashing for security
✓ Role-based access control
✓ Form validation (frontend & backend)

### Additional Features
✓ Modern, responsive UI with animations
✓ Attractive landing page
✓ Floating "Book Appointment" button
✓ RESTful API endpoints
✓ Demo credentials display
✓ Mobile-friendly design
✓ Clean, professional interface

---

## PROJECT STRUCTURE

```
hospital-management-system/
├── app.py                      # Main application file
├── models.py                   # Database models
├── routes.py                   # Application routes
├── requirements.txt            # Python dependencies
├── static/
│   ├── css/
│   │   ├── style.css          # Main styles
│   │   └── homepage.css       # Homepage styles
│   └── js/
│       └── main.js            # JavaScript functions
├── templates/
│   ├── base.html              # Base template
│   ├── index.html             # Landing page
│   ├── login.html             # Login page
│   ├── register.html          # Registration page
│   ├── admin/
│   │   ├── dashboard.html
│   │   ├── doctors.html
│   │   ├── add_doctor.html
│   │   ├── edit_doctor.html
│   │   ├── patients.html
│   │   ├── edit_patient.html
│   │   └── appointments.html
│   ├── doctor/
│   │   ├── dashboard.html
│   │   ├── appointments.html
│   │   ├── complete_appointment.html
│   │   ├── availability.html
│   │   └── patient_history.html
│   └── patient/
│       ├── dashboard.html
│       ├── doctors.html
│       ├── book_appointment.html
│       ├── appointments.html
│       ├── history.html
│       └── profile.html
└── instance/
    └── hospital.db            # SQLite database (auto-created)
```

---

## TESTING AND VALIDATION

### Test Accounts

**Admin:**
- Username: admin
- Password: admin123

**Doctors (all use password: doctor123):**
- dr.smith (Cardiologist)
- dr.johnson (Neurologist)
- dr.williams (Orthopedic Surgeon)
- dr.brown (Pediatrician)
- dr.davis (Dermatologist)
- dr.wilson (General Physician)

**Patient:**
- Register new account for testing

### Testing Performed
✓ User registration and login
✓ Role-based access control
✓ Appointment booking workflow
✓ Conflict prevention
✓ Medical record creation
✓ Search functionality
✓ Form validation
✓ Responsive design on multiple devices
✓ API endpoints
✓ Database integrity

---

## CHALLENGES AND SOLUTIONS

### Challenge 1: Database Design
**Problem:** Designing relationships between multiple entities
**Solution:** Created normalized schema with proper foreign keys and relationships

### Challenge 2: Role-Based Access
**Problem:** Ensuring users only access their authorized features
**Solution:** Implemented Flask-Login with role checks on every route

### Challenge 3: Appointment Conflicts
**Problem:** Preventing double bookings
**Solution:** Added database query to check existing appointments before booking

### Challenge 4: Responsive Design
**Problem:** Making UI work on all devices
**Solution:** Used Bootstrap grid system and custom media queries

---

## FUTURE ENHANCEMENTS

- Email notifications for appointments
- SMS reminders
- Payment integration
- Video consultation feature
- Advanced analytics dashboard
- Multi-language support
- Mobile application
- Integration with medical devices

---

## CONCLUSION

The Hospital Management System successfully addresses the problem of inefficient hospital record management. The system provides a comprehensive solution with role-based access, automated scheduling, and digital record keeping. All core requirements have been implemented and tested successfully.

The project demonstrates proficiency in:
- Full-stack web development
- Database design and management
- User authentication and authorization
- RESTful API development
- Responsive UI/UX design

---

## VIDEO PRESENTATION LINK

**Video URL:** https://drive.google.com/file/d/1Pvu10kzleQQ-4V8DKNBK1T--Vzn1D91C/view?usp=sharing

**Note:** Upload your video to Google Drive, set sharing to "Anyone with link", and paste the link above.

---

## DECLARATION

I hereby declare that this project is my original work and has been completed with AI assistance as mentioned in the AI/LLM Declaration section. All external resources and libraries used have been properly acknowledged.

**Student Signature:** kvs koushik 
**Date:** 16-nov-2025

---

**END OF REPORT**
