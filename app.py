from flask import Flask
from flask_login import LoginManager
from werkzeug.security import generate_password_hash
from models import db, User, Department, Doctor, DoctorAvailability
from routes import register_routes

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here-change-in-production'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///hospital.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

register_routes(app)

def init_db():
    with app.app_context():
        db.create_all()
        
        # Create admin if not exists
        admin = User.query.filter_by(username='admin').first()
        if not admin:
            admin = User(
                username='admin',
                email='admin@hospital.com',
                password=generate_password_hash('admin123'),
                role='admin',
                full_name='System Administrator',
                phone='1234567890'
            )
            db.session.add(admin)
            db.session.commit()
            print("Admin created successfully!")
        
        # Create default departments if not exist
        if Department.query.count() == 0:
            departments = [
                Department(name='Cardiology', description='Heart and cardiovascular system'),
                Department(name='Neurology', description='Brain and nervous system'),
                Department(name='Orthopedics', description='Bones, joints, and muscles'),
                Department(name='Pediatrics', description='Children healthcare'),
                Department(name='Dermatology', description='Skin, hair, and nails'),
                Department(name='General Medicine', description='General health consultation')
            ]
            db.session.add_all(departments)
            db.session.commit()
            print("Departments created successfully!")
        
        # Create sample doctors if not exist
        if Doctor.query.count() == 0:
            from datetime import date, time, timedelta
            
            # Get departments
            cardiology = Department.query.filter_by(name='Cardiology').first()
            neurology = Department.query.filter_by(name='Neurology').first()
            orthopedics = Department.query.filter_by(name='Orthopedics').first()
            pediatrics = Department.query.filter_by(name='Pediatrics').first()
            dermatology = Department.query.filter_by(name='Dermatology').first()
            general = Department.query.filter_by(name='General Medicine').first()
            
            sample_doctors = [
                {
                    'username': 'dr.smith',
                    'email': 'smith@hospital.com',
                    'password': 'doctor123',
                    'full_name': 'Dr. John Smith',
                    'phone': '9876543210',
                    'department_id': cardiology.id,
                    'specialization': 'Cardiologist',
                    'qualification': 'MD, DM Cardiology',
                    'experience_years': 15,
                    'consultation_fee': 500.00,
                    'bio': 'Experienced cardiologist specializing in heart diseases and cardiac care.'
                },
                {
                    'username': 'dr.johnson',
                    'email': 'johnson@hospital.com',
                    'password': 'doctor123',
                    'full_name': 'Dr. Sarah Johnson',
                    'phone': '9876543211',
                    'department_id': neurology.id,
                    'specialization': 'Neurologist',
                    'qualification': 'MD, DM Neurology',
                    'experience_years': 12,
                    'consultation_fee': 600.00,
                    'bio': 'Expert in treating neurological disorders and brain-related conditions.'
                },
                {
                    'username': 'dr.williams',
                    'email': 'williams@hospital.com',
                    'password': 'doctor123',
                    'full_name': 'Dr. Michael Williams',
                    'phone': '9876543212',
                    'department_id': orthopedics.id,
                    'specialization': 'Orthopedic Surgeon',
                    'qualification': 'MS Orthopedics',
                    'experience_years': 10,
                    'consultation_fee': 450.00,
                    'bio': 'Specialized in bone, joint, and muscle treatments and surgeries.'
                },
                {
                    'username': 'dr.brown',
                    'email': 'brown@hospital.com',
                    'password': 'doctor123',
                    'full_name': 'Dr. Emily Brown',
                    'phone': '9876543213',
                    'department_id': pediatrics.id,
                    'specialization': 'Pediatrician',
                    'qualification': 'MD Pediatrics',
                    'experience_years': 8,
                    'consultation_fee': 400.00,
                    'bio': 'Caring for children\'s health from infancy through adolescence.'
                },
                {
                    'username': 'dr.davis',
                    'email': 'davis@hospital.com',
                    'password': 'doctor123',
                    'full_name': 'Dr. Robert Davis',
                    'phone': '9876543214',
                    'department_id': dermatology.id,
                    'specialization': 'Dermatologist',
                    'qualification': 'MD Dermatology',
                    'experience_years': 7,
                    'consultation_fee': 350.00,
                    'bio': 'Expert in skin, hair, and nail treatments and cosmetic procedures.'
                },
                {
                    'username': 'dr.wilson',
                    'email': 'wilson@hospital.com',
                    'password': 'doctor123',
                    'full_name': 'Dr. Lisa Wilson',
                    'phone': '9876543215',
                    'department_id': general.id,
                    'specialization': 'General Physician',
                    'qualification': 'MBBS, MD',
                    'experience_years': 5,
                    'consultation_fee': 300.00,
                    'bio': 'General health consultation and primary care services.'
                }
            ]
            
            for doc_data in sample_doctors:
                user = User(
                    username=doc_data['username'],
                    email=doc_data['email'],
                    password=generate_password_hash(doc_data['password']),
                    role='doctor',
                    full_name=doc_data['full_name'],
                    phone=doc_data['phone']
                )
                db.session.add(user)
                db.session.flush()
                
                doctor = Doctor(
                    user_id=user.id,
                    department_id=doc_data['department_id'],
                    specialization=doc_data['specialization'],
                    qualification=doc_data['qualification'],
                    experience_years=doc_data['experience_years'],
                    consultation_fee=doc_data['consultation_fee'],
                    bio=doc_data['bio']
                )
                db.session.add(doctor)
                db.session.flush()  # Flush to get doctor.id
                
                # Add availability for next 7 days
                today = date.today()
                for i in range(7):
                    avail_date = today + timedelta(days=i)
                    availability = DoctorAvailability(
                        doctor_id=doctor.id,
                        date=avail_date,
                        start_time=time(9, 0),
                        end_time=time(17, 0),
                        is_available=True
                    )
                    db.session.add(availability)
            
            db.session.commit()
            print("Sample doctors created successfully with availability!")

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
