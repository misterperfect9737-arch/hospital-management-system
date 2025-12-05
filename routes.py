from flask import render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta, date, time
from models import db, User, Doctor, Patient, Appointment, Treatment, Department, DoctorAvailability
from sqlalchemy import or_, and_, func

def register_routes(app):
    
    @app.route('/')
    def index():
        return render_template('index.html')
    
    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if current_user.is_authenticated:
            return redirect(url_for('dashboard'))
        
        if request.method == 'POST':
            username = request.form.get('username')
            password = request.form.get('password')
            
            user = User.query.filter_by(username=username).first()
            
            if user and check_password_hash(user.password, password):
                if not user.is_active:
                    flash('Your account has been deactivated. Please contact admin.', 'danger')
                    return redirect(url_for('login'))
                login_user(user)
                flash('Login successful!', 'success')
                return redirect(url_for('dashboard'))
            else:
                flash('Invalid username or password', 'danger')
        
        return render_template('login.html')
    
    @app.route('/register', methods=['GET', 'POST'])
    def register():
        if current_user.is_authenticated:
            return redirect(url_for('dashboard'))
        
        if request.method == 'POST':
            username = request.form.get('username')
            email = request.form.get('email')
            password = request.form.get('password')
            full_name = request.form.get('full_name')
            phone = request.form.get('phone')
            dob = request.form.get('dob')
            gender = request.form.get('gender')
            blood_group = request.form.get('blood_group')
            address = request.form.get('address')
            emergency_contact = request.form.get('emergency_contact')
            
            if User.query.filter_by(username=username).first():
                flash('Username already exists', 'danger')
                return redirect(url_for('register'))
            
            if User.query.filter_by(email=email).first():
                flash('Email already registered', 'danger')
                return redirect(url_for('register'))
            
            user = User(
                username=username,
                email=email,
                password=generate_password_hash(password),
                role='patient',
                full_name=full_name,
                phone=phone
            )
            db.session.add(user)
            db.session.flush()
            
            patient = Patient(
                user_id=user.id,
                date_of_birth=datetime.strptime(dob, '%Y-%m-%d').date() if dob else None,
                gender=gender,
                blood_group=blood_group,
                address=address,
                emergency_contact=emergency_contact
            )
            db.session.add(patient)
            db.session.commit()
            
            flash('Registration successful! Please login.', 'success')
            return redirect(url_for('login'))
        
        return render_template('register.html')
    
    @app.route('/logout')
    @login_required
    def logout():
        logout_user()
        flash('Logged out successfully', 'success')
        return redirect(url_for('index'))
    
    @app.route('/dashboard')
    @login_required
    def dashboard():
        if current_user.role == 'admin':
            return redirect(url_for('admin_dashboard'))
        elif current_user.role == 'doctor':
            return redirect(url_for('doctor_dashboard'))
        elif current_user.role == 'patient':
            return redirect(url_for('patient_dashboard'))
    
    # Admin Routes
    @app.route('/admin/dashboard')
    @login_required
    def admin_dashboard():
        if current_user.role != 'admin':
            flash('Unauthorized access', 'danger')
            return redirect(url_for('dashboard'))
        
        total_doctors = Doctor.query.join(User).filter(User.is_active == True).count()
        total_patients = Patient.query.join(User).filter(User.is_active == True).count()
        total_appointments = Appointment.query.count()
        today_appointments = Appointment.query.filter(
            Appointment.appointment_date == date.today()
        ).count()
        
        recent_appointments = Appointment.query.order_by(
            Appointment.created_at.desc()
        ).limit(10).all()
        
        return render_template('admin/dashboard.html',
                             total_doctors=total_doctors,
                             total_patients=total_patients,
                             total_appointments=total_appointments,
                             today_appointments=today_appointments,
                             recent_appointments=recent_appointments)

    
    @app.route('/admin/doctors')
    @login_required
    def admin_doctors():
        if current_user.role != 'admin':
            flash('Unauthorized access', 'danger')
            return redirect(url_for('dashboard'))
        
        search = request.args.get('search', '')
        if search:
            doctors = Doctor.query.join(User).filter(
                or_(
                    User.full_name.ilike(f'%{search}%'),
                    Doctor.specialization.ilike(f'%{search}%')
                )
            ).all()
        else:
            doctors = Doctor.query.all()
        
        return render_template('admin/doctors.html', doctors=doctors, search=search)
    
    @app.route('/admin/doctor/add', methods=['GET', 'POST'])
    @login_required
    def admin_add_doctor():
        if current_user.role != 'admin':
            flash('Unauthorized access', 'danger')
            return redirect(url_for('dashboard'))
        
        if request.method == 'POST':
            username = request.form.get('username')
            email = request.form.get('email')
            password = request.form.get('password')
            full_name = request.form.get('full_name')
            phone = request.form.get('phone')
            department_id = request.form.get('department_id')
            specialization = request.form.get('specialization')
            qualification = request.form.get('qualification')
            experience_years = request.form.get('experience_years')
            consultation_fee = request.form.get('consultation_fee')
            bio = request.form.get('bio')
            
            if User.query.filter_by(username=username).first():
                flash('Username already exists', 'danger')
                return redirect(url_for('admin_add_doctor'))
            
            user = User(
                username=username,
                email=email,
                password=generate_password_hash(password),
                role='doctor',
                full_name=full_name,
                phone=phone
            )
            db.session.add(user)
            db.session.flush()
            
            doctor = Doctor(
                user_id=user.id,
                department_id=department_id,
                specialization=specialization,
                qualification=qualification,
                experience_years=experience_years,
                consultation_fee=consultation_fee,
                bio=bio
            )
            db.session.add(doctor)
            db.session.commit()
            
            flash('Doctor added successfully!', 'success')
            return redirect(url_for('admin_doctors'))
        
        departments = Department.query.all()
        return render_template('admin/add_doctor.html', departments=departments)
    
    @app.route('/admin/doctor/edit/<int:id>', methods=['GET', 'POST'])
    @login_required
    def admin_edit_doctor(id):
        if current_user.role != 'admin':
            flash('Unauthorized access', 'danger')
            return redirect(url_for('dashboard'))
        
        doctor = Doctor.query.get_or_404(id)
        
        if request.method == 'POST':
            doctor.user.full_name = request.form.get('full_name')
            doctor.user.email = request.form.get('email')
            doctor.user.phone = request.form.get('phone')
            doctor.department_id = request.form.get('department_id')
            doctor.specialization = request.form.get('specialization')
            doctor.qualification = request.form.get('qualification')
            doctor.experience_years = request.form.get('experience_years')
            doctor.consultation_fee = request.form.get('consultation_fee')
            doctor.bio = request.form.get('bio')
            
            db.session.commit()
            flash('Doctor updated successfully!', 'success')
            return redirect(url_for('admin_doctors'))
        
        departments = Department.query.all()
        return render_template('admin/edit_doctor.html', doctor=doctor, departments=departments)
    
    @app.route('/admin/doctor/delete/<int:id>')
    @login_required
    def admin_delete_doctor(id):
        if current_user.role != 'admin':
            flash('Unauthorized access', 'danger')
            return redirect(url_for('dashboard'))
        
        doctor = Doctor.query.get_or_404(id)
        doctor.user.is_active = False
        db.session.commit()
        
        flash('Doctor deactivated successfully!', 'success')
        return redirect(url_for('admin_doctors'))
    
    @app.route('/admin/patients')
    @login_required
    def admin_patients():
        if current_user.role != 'admin':
            flash('Unauthorized access', 'danger')
            return redirect(url_for('dashboard'))
        
        search = request.args.get('search', '')
        if search:
            patients = Patient.query.join(User).filter(
                or_(
                    User.full_name.ilike(f'%{search}%'),
                    User.email.ilike(f'%{search}%'),
                    User.phone.ilike(f'%{search}%')
                )
            ).all()
        else:
            patients = Patient.query.all()
        
        return render_template('admin/patients.html', patients=patients, search=search)
    
    @app.route('/admin/patient/edit/<int:id>', methods=['GET', 'POST'])
    @login_required
    def admin_edit_patient(id):
        if current_user.role != 'admin':
            flash('Unauthorized access', 'danger')
            return redirect(url_for('dashboard'))
        
        patient = Patient.query.get_or_404(id)
        
        if request.method == 'POST':
            patient.user.full_name = request.form.get('full_name')
            patient.user.email = request.form.get('email')
            patient.user.phone = request.form.get('phone')
            patient.gender = request.form.get('gender')
            patient.blood_group = request.form.get('blood_group')
            patient.address = request.form.get('address')
            patient.emergency_contact = request.form.get('emergency_contact')
            
            dob = request.form.get('date_of_birth')
            if dob:
                patient.date_of_birth = datetime.strptime(dob, '%Y-%m-%d').date()
            
            db.session.commit()
            flash('Patient updated successfully!', 'success')
            return redirect(url_for('admin_patients'))
        
        return render_template('admin/edit_patient.html', patient=patient)
    
    @app.route('/admin/patient/delete/<int:id>')
    @login_required
    def admin_delete_patient(id):
        if current_user.role != 'admin':
            flash('Unauthorized access', 'danger')
            return redirect(url_for('dashboard'))
        
        patient = Patient.query.get_or_404(id)
        patient.user.is_active = False
        db.session.commit()
        
        flash('Patient deactivated successfully!', 'success')
        return redirect(url_for('admin_patients'))
    
    @app.route('/admin/appointments')
    @login_required
    def admin_appointments():
        if current_user.role != 'admin':
            flash('Unauthorized access', 'danger')
            return redirect(url_for('dashboard'))
        
        status_filter = request.args.get('status', '')
        if status_filter:
            appointments = Appointment.query.filter_by(status=status_filter).order_by(
                Appointment.appointment_date.desc(),
                Appointment.appointment_time.desc()
            ).all()
        else:
            appointments = Appointment.query.order_by(
                Appointment.appointment_date.desc(),
                Appointment.appointment_time.desc()
            ).all()
        
        return render_template('admin/appointments.html', appointments=appointments, status_filter=status_filter)
    
    # Doctor Routes
    @app.route('/doctor/dashboard')
    @login_required
    def doctor_dashboard():
        if current_user.role != 'doctor':
            flash('Unauthorized access', 'danger')
            return redirect(url_for('dashboard'))
        
        doctor = Doctor.query.filter_by(user_id=current_user.id).first()
        
        today = date.today()
        week_end = today + timedelta(days=7)
        
        upcoming_appointments = Appointment.query.filter(
            Appointment.doctor_id == doctor.id,
            Appointment.appointment_date >= today,
            Appointment.appointment_date <= week_end,
            Appointment.status == 'Booked'
        ).order_by(Appointment.appointment_date, Appointment.appointment_time).all()
        
        today_appointments = Appointment.query.filter(
            Appointment.doctor_id == doctor.id,
            Appointment.appointment_date == today
        ).count()
        
        total_patients = db.session.query(func.count(func.distinct(Appointment.patient_id))).filter(
            Appointment.doctor_id == doctor.id
        ).scalar()
        
        completed_appointments = Appointment.query.filter(
            Appointment.doctor_id == doctor.id,
            Appointment.status == 'Completed'
        ).count()
        
        return render_template('doctor/dashboard.html',
                             doctor=doctor,
                             upcoming_appointments=upcoming_appointments,
                             today_appointments=today_appointments,
                             total_patients=total_patients,
                             completed_appointments=completed_appointments)

    
    @app.route('/doctor/appointments')
    @login_required
    def doctor_appointments():
        if current_user.role != 'doctor':
            flash('Unauthorized access', 'danger')
            return redirect(url_for('dashboard'))
        
        doctor = Doctor.query.filter_by(user_id=current_user.id).first()
        status_filter = request.args.get('status', '')
        
        if status_filter:
            appointments = Appointment.query.filter_by(
                doctor_id=doctor.id,
                status=status_filter
            ).order_by(Appointment.appointment_date.desc()).all()
        else:
            appointments = Appointment.query.filter_by(
                doctor_id=doctor.id
            ).order_by(Appointment.appointment_date.desc()).all()
        
        return render_template('doctor/appointments.html', appointments=appointments, status_filter=status_filter)
    
    @app.route('/doctor/appointment/<int:id>/complete', methods=['GET', 'POST'])
    @login_required
    def doctor_complete_appointment(id):
        if current_user.role != 'doctor':
            flash('Unauthorized access', 'danger')
            return redirect(url_for('dashboard'))
        
        appointment = Appointment.query.get_or_404(id)
        doctor = Doctor.query.filter_by(user_id=current_user.id).first()
        
        if appointment.doctor_id != doctor.id:
            flash('Unauthorized access', 'danger')
            return redirect(url_for('doctor_appointments'))
        
        if request.method == 'POST':
            diagnosis = request.form.get('diagnosis')
            prescription = request.form.get('prescription')
            notes = request.form.get('notes')
            
            appointment.status = 'Completed'
            
            treatment = Treatment(
                appointment_id=appointment.id,
                diagnosis=diagnosis,
                prescription=prescription,
                notes=notes
            )
            db.session.add(treatment)
            db.session.commit()
            
            flash('Appointment completed successfully!', 'success')
            return redirect(url_for('doctor_appointments'))
        
        return render_template('doctor/complete_appointment.html', appointment=appointment)
    
    @app.route('/doctor/appointment/<int:id>/cancel')
    @login_required
    def doctor_cancel_appointment(id):
        if current_user.role != 'doctor':
            flash('Unauthorized access', 'danger')
            return redirect(url_for('dashboard'))
        
        appointment = Appointment.query.get_or_404(id)
        doctor = Doctor.query.filter_by(user_id=current_user.id).first()
        
        if appointment.doctor_id != doctor.id:
            flash('Unauthorized access', 'danger')
            return redirect(url_for('doctor_appointments'))
        
        appointment.status = 'Cancelled'
        db.session.commit()
        
        flash('Appointment cancelled successfully!', 'success')
        return redirect(url_for('doctor_appointments'))
    
    @app.route('/doctor/patient/<int:id>/history')
    @login_required
    def doctor_patient_history(id):
        if current_user.role != 'doctor':
            flash('Unauthorized access', 'danger')
            return redirect(url_for('dashboard'))
        
        patient = Patient.query.get_or_404(id)
        doctor = Doctor.query.filter_by(user_id=current_user.id).first()
        
        appointments = Appointment.query.filter(
            Appointment.patient_id == patient.id,
            Appointment.status == 'Completed'
        ).order_by(Appointment.appointment_date.desc()).all()
        
        return render_template('doctor/patient_history.html', patient=patient, appointments=appointments)
    
    @app.route('/doctor/availability', methods=['GET', 'POST'])
    @login_required
    def doctor_availability():
        if current_user.role != 'doctor':
            flash('Unauthorized access', 'danger')
            return redirect(url_for('dashboard'))
        
        doctor = Doctor.query.filter_by(user_id=current_user.id).first()
        
        if request.method == 'POST':
            date_str = request.form.get('date')
            start_time_str = request.form.get('start_time')
            end_time_str = request.form.get('end_time')
            
            availability_date = datetime.strptime(date_str, '%Y-%m-%d').date()
            start_time = datetime.strptime(start_time_str, '%H:%M').time()
            end_time = datetime.strptime(end_time_str, '%H:%M').time()
            
            existing = DoctorAvailability.query.filter_by(
                doctor_id=doctor.id,
                date=availability_date
            ).first()
            
            if existing:
                existing.start_time = start_time
                existing.end_time = end_time
                existing.is_available = True
            else:
                availability = DoctorAvailability(
                    doctor_id=doctor.id,
                    date=availability_date,
                    start_time=start_time,
                    end_time=end_time,
                    is_available=True
                )
                db.session.add(availability)
            
            db.session.commit()
            flash('Availability updated successfully!', 'success')
            return redirect(url_for('doctor_availability'))
        
        today = date.today()
        week_end = today + timedelta(days=7)
        
        availabilities = DoctorAvailability.query.filter(
            DoctorAvailability.doctor_id == doctor.id,
            DoctorAvailability.date >= today,
            DoctorAvailability.date <= week_end
        ).order_by(DoctorAvailability.date).all()
        
        return render_template('doctor/availability.html', availabilities=availabilities)
    
    # Patient Routes
    @app.route('/patient/dashboard')
    @login_required
    def patient_dashboard():
        if current_user.role != 'patient':
            flash('Unauthorized access', 'danger')
            return redirect(url_for('dashboard'))
        
        patient = Patient.query.filter_by(user_id=current_user.id).first()
        
        if not patient:
            flash('Patient profile not found. Please contact admin.', 'danger')
            return redirect(url_for('logout'))
        
        departments = Department.query.all()
        
        upcoming_appointments = Appointment.query.filter(
            Appointment.patient_id == patient.id,
            Appointment.appointment_date >= date.today(),
            Appointment.status == 'Booked'
        ).order_by(Appointment.appointment_date, Appointment.appointment_time).all()
        
        return render_template('patient/dashboard.html',
                             patient=patient,
                             departments=departments,
                             upcoming_appointments=upcoming_appointments)
    
    @app.route('/patient/doctors')
    @login_required
    def patient_doctors():
        if current_user.role != 'patient':
            flash('Unauthorized access', 'danger')
            return redirect(url_for('dashboard'))
        
        search = request.args.get('search', '')
        department_id = request.args.get('department', '')
        
        query = Doctor.query.join(User).filter(User.is_active == True)
        
        if search:
            query = query.filter(
                or_(
                    User.full_name.ilike(f'%{search}%'),
                    Doctor.specialization.ilike(f'%{search}%')
                )
            )
        
        if department_id:
            query = query.filter(Doctor.department_id == department_id)
        
        doctors = query.all()
        departments = Department.query.all()
        
        return render_template('patient/doctors.html',
                             doctors=doctors,
                             departments=departments,
                             search=search,
                             selected_department=department_id)
    
    @app.route('/patient/book/<int:doctor_id>', methods=['GET', 'POST'])
    @login_required
    def patient_book_appointment(doctor_id):
        if current_user.role != 'patient':
            flash('Unauthorized access', 'danger')
            return redirect(url_for('dashboard'))
        
        doctor = Doctor.query.get_or_404(doctor_id)
        patient = Patient.query.filter_by(user_id=current_user.id).first()
        
        if not patient:
            flash('Patient profile not found. Please contact admin.', 'danger')
            return redirect(url_for('logout'))
        
        if request.method == 'POST':
            appointment_date_str = request.form.get('appointment_date')
            appointment_time_str = request.form.get('appointment_time')
            reason = request.form.get('reason')
            
            appointment_date = datetime.strptime(appointment_date_str, '%Y-%m-%d').date()
            appointment_time = datetime.strptime(appointment_time_str, '%H:%M').time()
            
            # Check for conflicts
            existing = Appointment.query.filter(
                Appointment.doctor_id == doctor.id,
                Appointment.appointment_date == appointment_date,
                Appointment.appointment_time == appointment_time,
                Appointment.status == 'Booked'
            ).first()
            
            if existing:
                flash('This time slot is already booked. Please choose another time.', 'danger')
                return redirect(url_for('patient_book_appointment', doctor_id=doctor_id))
            
            appointment = Appointment(
                patient_id=patient.id,
                doctor_id=doctor.id,
                appointment_date=appointment_date,
                appointment_time=appointment_time,
                reason=reason,
                status='Booked'
            )
            db.session.add(appointment)
            db.session.commit()
            
            flash('Appointment booked successfully!', 'success')
            return redirect(url_for('patient_appointments'))
        
        today = date.today()
        week_end = today + timedelta(days=7)
        
        availabilities = DoctorAvailability.query.filter(
            DoctorAvailability.doctor_id == doctor.id,
            DoctorAvailability.date >= today,
            DoctorAvailability.date <= week_end,
            DoctorAvailability.is_available == True
        ).order_by(DoctorAvailability.date).all()
        
        return render_template('patient/book_appointment.html', doctor=doctor, availabilities=availabilities)

    
    @app.route('/patient/appointments')
    @login_required
    def patient_appointments():
        if current_user.role != 'patient':
            flash('Unauthorized access', 'danger')
            return redirect(url_for('dashboard'))
        
        patient = Patient.query.filter_by(user_id=current_user.id).first()
        
        # Only show Booked and Completed appointments (exclude Cancelled)
        appointments = Appointment.query.filter(
            Appointment.patient_id == patient.id,
            Appointment.status.in_(['Booked', 'Completed'])
        ).order_by(Appointment.appointment_date.desc(), Appointment.appointment_time.desc()).all()
        
        return render_template('patient/appointments.html', appointments=appointments)
    
    @app.route('/patient/appointment/<int:id>/cancel')
    @login_required
    def patient_cancel_appointment(id):
        if current_user.role != 'patient':
            flash('Unauthorized access', 'danger')
            return redirect(url_for('dashboard'))
        
        appointment = Appointment.query.get_or_404(id)
        patient = Patient.query.filter_by(user_id=current_user.id).first()
        
        if appointment.patient_id != patient.id:
            flash('Unauthorized access', 'danger')
            return redirect(url_for('patient_appointments'))
        
        if appointment.status != 'Booked':
            flash('Only booked appointments can be cancelled', 'danger')
            return redirect(url_for('patient_appointments'))
        
        appointment.status = 'Cancelled'
        db.session.commit()
        
        flash('Appointment cancelled successfully!', 'success')
        return redirect(url_for('patient_appointments'))
    
    @app.route('/patient/history')
    @login_required
    def patient_history():
        if current_user.role != 'patient':
            flash('Unauthorized access', 'danger')
            return redirect(url_for('dashboard'))
        
        patient = Patient.query.filter_by(user_id=current_user.id).first()
        
        appointments = Appointment.query.filter(
            Appointment.patient_id == patient.id,
            Appointment.status == 'Completed'
        ).order_by(Appointment.appointment_date.desc()).all()
        
        return render_template('patient/history.html', appointments=appointments)
    
    @app.route('/patient/profile', methods=['GET', 'POST'])
    @login_required
    def patient_profile():
        if current_user.role != 'patient':
            flash('Unauthorized access', 'danger')
            return redirect(url_for('dashboard'))
        
        patient = Patient.query.filter_by(user_id=current_user.id).first()
        
        if request.method == 'POST':
            current_user.full_name = request.form.get('full_name')
            current_user.email = request.form.get('email')
            current_user.phone = request.form.get('phone')
            patient.gender = request.form.get('gender')
            patient.blood_group = request.form.get('blood_group')
            patient.address = request.form.get('address')
            patient.emergency_contact = request.form.get('emergency_contact')
            
            dob = request.form.get('date_of_birth')
            if dob:
                patient.date_of_birth = datetime.strptime(dob, '%Y-%m-%d').date()
            
            db.session.commit()
            flash('Profile updated successfully!', 'success')
            return redirect(url_for('patient_profile'))
        
        return render_template('patient/profile.html', patient=patient)
    
    # API Routes
    @app.route('/api/appointments', methods=['GET'])
    @login_required
    def api_get_appointments():
        status = request.args.get('status')
        doctor_id = request.args.get('doctor_id')
        patient_id = request.args.get('patient_id')
        
        query = Appointment.query
        
        if status:
            query = query.filter_by(status=status)
        if doctor_id:
            query = query.filter_by(doctor_id=doctor_id)
        if patient_id:
            query = query.filter_by(patient_id=patient_id)
        
        appointments = query.all()
        
        result = []
        for apt in appointments:
            result.append({
                'id': apt.id,
                'patient_name': apt.patient.user.full_name,
                'doctor_name': apt.doctor.user.full_name,
                'date': apt.appointment_date.strftime('%Y-%m-%d'),
                'time': apt.appointment_time.strftime('%H:%M'),
                'status': apt.status,
                'reason': apt.reason
            })
        
        return jsonify(result)
    
    @app.route('/api/appointments/<int:id>', methods=['GET'])
    @login_required
    def api_get_appointment(id):
        appointment = Appointment.query.get_or_404(id)
        
        result = {
            'id': appointment.id,
            'patient_name': appointment.patient.user.full_name,
            'doctor_name': appointment.doctor.user.full_name,
            'date': appointment.appointment_date.strftime('%Y-%m-%d'),
            'time': appointment.appointment_time.strftime('%H:%M'),
            'status': appointment.status,
            'reason': appointment.reason
        }
        
        if appointment.treatment:
            result['treatment'] = {
                'diagnosis': appointment.treatment.diagnosis,
                'prescription': appointment.treatment.prescription,
                'notes': appointment.treatment.notes
            }
        
        return jsonify(result)
    
    @app.route('/api/appointments', methods=['POST'])
    @login_required
    def api_create_appointment():
        data = request.get_json()
        
        appointment = Appointment(
            patient_id=data['patient_id'],
            doctor_id=data['doctor_id'],
            appointment_date=datetime.strptime(data['date'], '%Y-%m-%d').date(),
            appointment_time=datetime.strptime(data['time'], '%H:%M').time(),
            reason=data.get('reason', ''),
            status='Booked'
        )
        
        db.session.add(appointment)
        db.session.commit()
        
        return jsonify({'message': 'Appointment created', 'id': appointment.id}), 201
    
    @app.route('/api/appointments/<int:id>', methods=['PUT'])
    @login_required
    def api_update_appointment(id):
        appointment = Appointment.query.get_or_404(id)
        data = request.get_json()
        
        if 'status' in data:
            appointment.status = data['status']
        if 'date' in data:
            appointment.appointment_date = datetime.strptime(data['date'], '%Y-%m-%d').date()
        if 'time' in data:
            appointment.appointment_time = datetime.strptime(data['time'], '%H:%M').time()
        
        db.session.commit()
        
        return jsonify({'message': 'Appointment updated'})
    
    @app.route('/api/appointments/<int:id>', methods=['DELETE'])
    @login_required
    def api_delete_appointment(id):
        appointment = Appointment.query.get_or_404(id)
        appointment.status = 'Cancelled'
        db.session.commit()
        
        return jsonify({'message': 'Appointment cancelled'})
    
    @app.route('/api/doctors', methods=['GET'])
    def api_get_doctors():
        specialization = request.args.get('specialization')
        
        query = Doctor.query.join(User).filter(User.is_active == True)
        
        if specialization:
            query = query.filter(Doctor.specialization.ilike(f'%{specialization}%'))
        
        doctors = query.all()
        
        result = []
        for doc in doctors:
            result.append({
                'id': doc.id,
                'name': doc.user.full_name,
                'specialization': doc.specialization,
                'department': doc.department.name,
                'experience_years': doc.experience_years,
                'consultation_fee': doc.consultation_fee
            })
        
        return jsonify(result)
