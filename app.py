from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os
from sqlalchemy import text, and_, or_, func
from models import db, Corporation, Clinic, Employee, Physician, Nurse, Surgeon, Shift, Patient, Medical_Data, Allergy, Illness, Surgery_Type, Surgery_Skill, Surgery, Consultation, Medicine, Prescription, Clinic_Bed, Diagnosis, Patient_Allergy, AttendsTo, AdmittedTo, ReactsWith, Surgery_Type_Skill, Nurse_Skill, Nurse_Surgery_Type, Surgery_Schedule, WorksShift
from datetime import datetime, date

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://postgres:Admin@localhost:5432/postgres'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize SQLAlchemy with app
db.init_app(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/test-db')
def test_db():
    try:
        db.session.execute(text('SELECT 1'))
        return jsonify({'status': 'success', 'message': 'Database connection successful'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})

@app.route('/api/corporations', methods=['GET'])
def get_corporations():
    corporations = Corporation.query.all()
    return jsonify([
        {
            'Name': c.name,
            'PercentOwn': float(c.percentown),
            'HeadquartersStreet': c.headquartersstreet,
            'HeadquartersCity': c.headquarterscity,
            'HeadquartersState': c.headquartersstate,
            'HeadquartersZip': c.headquarterszip
        } for c in corporations
    ])

@app.route('/api/corporations/<string:name>', methods=['GET'])
def get_corporation(name):
    c = Corporation.query.get_or_404(name)
    return jsonify({
        'Name': c.name,
        'PercentOwn': float(c.percentown),
        'HeadquartersStreet': c.headquartersstreet,
        'HeadquartersCity': c.headquarterscity,
        'HeadquartersState': c.headquartersstate,
        'HeadquartersStreet': c.headquartersstreet,
        'HeadquartersCity': c.headquarterscity,
        'HeadquartersState': c.headquartersstate,
        'HeadquartersZip': c.headquarterszip
    })

@app.route('/api/corporations', methods=['POST'])
def create_corporation():
    data = request.get_json()
    corporation = Corporation(
        Name=data['Name'],
        percentown=data['PercentOwn'],
        HeadquartersStreet=data['HeadquartersStreet'],
        HeadquartersCity=data['HeadquartersCity'],
        HeadquartersState=data['HeadquartersState'],
        HeadquartersZip=data['HeadquartersZip']
    )
    db.session.add(corporation)
    db.session.commit()
    return jsonify({'Name': corporation.Name}), 201

@app.route('/api/corporations/<string:name>', methods=['PUT'])
def update_corporation(name):
    corporation = Corporation.query.get_or_404(name)
    data = request.get_json()
    
    corporation.percentown = data.get('percentown', corporation.percentown)
    corporation.headquartersstreet = data.get('HeadquartersStreet', corporation.headquartersstreet)
    corporation.headquarterscity = data.get('HeadquartersCity', corporation.headquarterscity)
    corporation.headquartersstate = data.get('HeadquartersState', corporation.headquartersstate)
    corporation.headquarterszip = data.get('HeadquartersZip', corporation.headquarterszip)
    
    db.session.commit()
    return jsonify({'Name': corporation.Name})

@app.route('/api/corporations/<string:name>', methods=['DELETE'])
def delete_corporation(name):
    c = Corporation.query.get_or_404(name)
    db.session.delete(c)
    db.session.commit()
    return jsonify({'message': 'Corporation deleted'})

# --- Clinic CRUD ---
@app.route('/api/clinics', methods=['GET'])
def get_clinics():
    clinics = Clinic.query.all()
    return jsonify([
        {
            'Name': c.name,
            'Street': c.street,
            'City': c.city,
            'State': c.state,
            'Zip': c.zip,
            'OwnerID': c.ownerid
        } for c in clinics
    ])

@app.route('/api/clinics/<string:name>', methods=['GET'])
def get_clinic(name):
    c = Clinic.query.get_or_404(name)
    return jsonify({
        'Name': c.name,
        'Street': c.street,
        'City': c.city,
        'State': c.state,
        'Zip': c.zip,
        'OwnerID': c.ownerid
    })

@app.route('/api/clinics', methods=['POST'])
def create_clinic():
    data = request.get_json()
    clinic = Clinic(
        Name=data['Name'],
        Street=data['Street'],
        City=data['City'],
        State=data['State'],
        Zip=data['Zip'],
        OwnerID=data.get('OwnerID')
    )
    db.session.add(clinic)
    db.session.commit()
    return jsonify({'Name': clinic.name}), 201

@app.route('/api/clinics/<string:name>', methods=['PUT'])
def update_clinic(name):
    clinic = Clinic.query.get_or_404(name)
    data = request.get_json()
    clinic.street = data.get('Street', clinic.street)
    clinic.city = data.get('City', clinic.city)
    clinic.state = data.get('State', clinic.state)
    clinic.zip = data.get('Zip', clinic.zip)
    clinic.ownerid = data.get('OwnerID', clinic.ownerid)
    db.session.commit()
    return jsonify({'Name': clinic.name})

@app.route('/api/clinics/<string:name>', methods=['DELETE'])
def delete_clinic(name):
    c = Clinic.query.get_or_404(name)
    db.session.delete(c)
    db.session.commit()
    return jsonify({'message': 'Clinic deleted'})

# --- Employee CRUD ---
@app.route('/api/employees', methods=['GET'])
def get_employees():
    employees = Employee.query.all()
    return jsonify([
        {
            'empid': e.empid,
            'first_name': e.first_name,
            'last_name': e.last_name,
            'ssn': e.ssn,
            'salary': float(e.salary) if e.salary is not None else None,
            'gender': e.gender,
            'employeetype': e.employeetype,
            'phone': e.phone,
            'street': e.street,
            'city': e.city,
            'state': e.state,
            'zip': e.zip
        } for e in employees
    ])

@app.route('/api/employees/<int:empid>', methods=['GET'])
def get_employee(empid):
    e = Employee.query.get_or_404(empid)
    return jsonify({
        'empid': e.empid,
        'first_name': e.first_name,
        'last_name': e.last_name,
        'ssn': e.ssn,
        'salary': float(e.salary) if e.salary is not None else None,
        'gender': e.gender,
        'employeetype': e.employeetype,
        'phone': e.phone,
        'street': e.street,
        'city': e.city,
        'state': e.state,
        'zip': e.zip
    })

@app.route('/api/employees', methods=['POST'])
def create_employee():
    data = request.get_json()
    # Check for duplicate SSN
    if Employee.query.filter_by(ssn=data['SSN']).first():
        return jsonify({'error': 'SSN already exists for an employee'}), 400
    # Find the current max empid
    max_empid = db.session.query(func.max(Employee.empid)).scalar()
    new_empid = (max_empid or 0) + 1
    employee = Employee(
        empid=new_empid,  # Set the new empid here
        first_name=data['First_Name'],
        last_name=data['Last_Name'],
        ssn=data['SSN'],
        salary=data.get('Salary'),
        gender=data.get('Gender'),
        employeetype=data['EmployeeType'],
        phone=data['Phone'],
        street=data['Street'],
        city=data['City'],
        state=data['State'],
        zip=data['Zip']
    )
    db.session.add(employee)
    db.session.commit()
    return jsonify({'EmpID': employee.empid}), 201

@app.route('/api/employees/<int:empid>', methods=['PUT'])
def update_employee(empid):
    employee = Employee.query.get_or_404(empid)
    data = request.get_json()
    employee.first_name = data.get('First_Name', employee.first_name)
    employee.last_name = data.get('Last_Name', employee.last_name)
    employee.ssn = data.get('SSN', employee.ssn)
    employee.salary = data.get('Salary', employee.salary)
    employee.gender = data.get('Gender', employee.gender)
    employee.employeetype = data.get('EmployeeType', employee.employeetype)
    employee.phone = data.get('Phone', employee.phone)
    employee.street = data.get('Street', employee.street)
    employee.city = data.get('City', employee.city)
    employee.state = data.get('State', employee.state)
    employee.zip = data.get('Zip', employee.zip)
    db.session.commit()
    return jsonify({'EmpID': employee.empid})

@app.route('/api/employees/<int:empid>', methods=['DELETE'])
def delete_employee(empid):
    e = Employee.query.get_or_404(empid)
    # Explicitly delete related child records first
    if e.nurse:
        db.session.delete(e.nurse)
    if e.physician:
        db.session.delete(e.physician)
    if e.surgeon:
        db.session.delete(e.surgeon)
    db.session.delete(e)
    db.session.commit()
    return jsonify({'message': 'Employee deleted'})

# --- Physician CRUD ---
@app.route('/api/physicians', methods=['GET'])
def get_physicians():
    physicians = Physician.query.all()
    return jsonify([
        {
            'physicianid': p.physicianid,
            'specialty': p.specialty,
            'type': p.type,
            'empid': p.physicianid,
            'first_name': p.employee.first_name if p.employee else '',
            'last_name': p.employee.last_name if p.employee else ''
        } for p in physicians
    ])

@app.route('/api/physicians/<int:physicianid>', methods=['GET'])
def get_physician(physicianid):
    p = Physician.query.get_or_404(physicianid)
    return jsonify({
        'physicianid': p.physicianid,
        'specialty': p.specialty,
        'type': p.type,
        'empid': p.physicianid
    })

@app.route('/api/physicians', methods=['POST'])
def create_physician():
    data = request.get_json()
    p = Physician(
        physicianid=data['PhysicianID'],
        specialty=data['Specialty'],
        type=data['Type']
    )
    db.session.add(p)
    db.session.commit()
    return jsonify({'PhysicianID': p.physicianid}), 201

@app.route('/api/physicians/<int:physicianid>', methods=['PUT'])
def update_physician(physicianid):
    p = Physician.query.get_or_404(physicianid)
    data = request.get_json()
    p.specialty = data.get('Specialty', p.specialty)
    p.type = data.get('Type', p.type)
    db.session.commit()
    return jsonify({'PhysicianID': p.physicianid})

@app.route('/api/physicians/<int:physicianid>', methods=['DELETE'])
def delete_physician(physicianid):
    p = Physician.query.get_or_404(physicianid)
    db.session.delete(p)
    db.session.commit()
    return jsonify({'message': 'Physician deleted'})

# --- Nurse CRUD ---
@app.route('/api/nurses', methods=['GET'])
def get_nurses():
    nurses = Nurse.query.all()
    return jsonify([
        {
            'nurseid': n.nurseid,
            'grade': n.grade,
            'years': n.years,
            'first_name': n.employee.first_name if n.employee else '',
            'last_name': n.employee.last_name if n.employee else ''
        } for n in nurses
    ])

@app.route('/api/nurses/<int:nurseid>', methods=['GET'])
def get_nurse(nurseid):
    n = Nurse.query.get_or_404(nurseid)
    return jsonify({'nurseid': n.nurseid, 'grade': n.grade, 'years': n.years})

@app.route('/api/nurses', methods=['POST'])
def create_nurse():
    data = request.get_json()
    n = Nurse(
        nurseid=data['NurseID'],
        grade=data['Grade'],
        years=data['Years']
    )
    db.session.add(n)
    db.session.commit()
    return jsonify({'NurseID': n.nurseid}), 201

@app.route('/api/nurses/<int:nurseid>', methods=['PUT'])
def update_nurse(nurseid):
    n = Nurse.query.get_or_404(nurseid)
    data = request.get_json()
    n.grade = data.get('Grade', n.grade)
    n.years = data.get('Years', n.years)
    db.session.commit()
    return jsonify({'NurseID': n.nurseid})

@app.route('/api/nurses/<int:nurseid>', methods=['DELETE'])
def delete_nurse(nurseid):
    n = Nurse.query.get_or_404(nurseid)
    db.session.delete(n)
    db.session.commit()
    return jsonify({'message': 'Nurse deleted'})

# --- Surgeon CRUD ---
@app.route('/api/surgeons', methods=['GET'])
def get_surgeons():
    surgeons = Surgeon.query.all()
    return jsonify([
        {
            'surgeonid': s.surgeonid,
            'specialty': s.specialty,
            'contracttype': s.contracttype,
            'contractduration': s.contractduration,
            'contractamount': float(s.contractamount) if s.contractamount is not None else None
        } for s in surgeons
    ])

@app.route('/api/surgeons/<int:surgeonid>', methods=['GET'])
def get_surgeon(surgeonid):
    s = Surgeon.query.get_or_404(surgeonid)
    return jsonify({
        'surgeonid': s.surgeonid,
        'specialty': s.specialty,
        'contracttype': s.contracttype,
        'contractduration': s.contractduration,
        'contractamount': float(s.contractamount) if s.contractamount is not None else None
    })

@app.route('/api/surgeons', methods=['POST'])
def create_surgeon():
    data = request.get_json()
    s = Surgeon(
        surgeonid=data['SurgeonID'],
        specialty=data['Specialty'],
        contracttype=data['ContractType'],
        contractduration=data['ContractDuration'],
        contractamount=data.get('ContractAmount')
    )
    db.session.add(s)
    db.session.commit()
    return jsonify({'SurgeonID': s.surgeonid}), 201

@app.route('/api/surgeons/<int:surgeonid>', methods=['PUT'])
def update_surgeon(surgeonid):
    s = Surgeon.query.get_or_404(surgeonid)
    data = request.get_json()
    s.specialty = data.get('Specialty', s.specialty)
    s.contracttype = data.get('ContractType', s.contracttype)
    s.contractduration = data.get('ContractDuration', s.contractduration)
    s.contractamount = data.get('ContractAmount', s.contractamount)
    db.session.commit()
    return jsonify({'SurgeonID': s.surgeonid})

@app.route('/api/surgeons/<int:surgeonid>', methods=['DELETE'])
def delete_surgeon(surgeonid):
    s = Surgeon.query.get_or_404(surgeonid)
    db.session.delete(s)
    db.session.commit()
    return jsonify({'message': 'Surgeon deleted'})

# --- Shift CRUD ---
@app.route('/api/shifts', methods=['GET'])
def get_shifts():
    shifts = Shift.query.all()
    return jsonify([
        {
            'empid': s.empid,
            'first_name': s.employee.first_name if s.employee else '',
            'last_name': s.employee.last_name if s.employee else '',
            'day': s.day,
            'begin_time': s.begintime.strftime('%H:%M:%S') if s.begintime else None,
            'end_time': s.endtime.strftime('%H:%M:%S') if s.endtime else None
        } for s in shifts
    ])

@app.route('/api/shifts/<int:empid>/<string:day>', methods=['GET'])
def get_shift(empid, day):
    s = Shift.query.get_or_404((empid, day))
    return jsonify({
        'empid': s.empid,
        'day': s.day,
        'begin_time': s.begintime.strftime('%H:%M:%S') if s.begintime else None,
        'end_time': s.endtime.strftime('%H:%M:%S') if s.endtime else None
    })

@app.route('/api/shifts', methods=['POST'])
def create_shift():
    data = request.get_json()
    from datetime import datetime
    # Validate time order
    try:
        begin = datetime.strptime(data['BeginTime'], '%H:%M')
        end = datetime.strptime(data['EndTime'], '%H:%M')
        if end <= begin:
            return jsonify({'error': 'End time must be after begin time'}), 400
    except Exception as e:
        return jsonify({'error': 'Invalid time format'}), 400
    s = Shift(
        empid=data['EmpID'],
        day=data['Day'],
        begintime=data['BeginTime'],
        endtime=data['EndTime']
    )
    db.session.add(s)
    db.session.commit()
    return jsonify({'EmpID': s.empid, 'Day': s.day}), 201

@app.route('/api/shifts/<int:empid>/<string:day>', methods=['PUT'])
def update_shift(empid, day):
    s = Shift.query.get_or_404((empid, day))
    data = request.get_json()
    s.begintime = data.get('BeginTime', s.begintime)
    s.endtime = data.get('EndTime', s.endtime)
    db.session.commit()
    return jsonify({'EmpID': s.empid, 'Day': s.day})

@app.route('/api/shifts/<int:empid>/<string:day>', methods=['DELETE'])
def delete_shift(empid, day):
    s = Shift.query.get_or_404((empid, day))
    db.session.delete(s)
    db.session.commit()
    return jsonify({'message': 'Shift deleted'})

# --- Patient CRUD ---
@app.route('/api/patients', methods=['GET'])
def get_patients():
    patients = Patient.query.all()
    return jsonify([
        {
            'pid': p.pid,
            'primaryphysician': p.primaryphysician,
            'd_o_b': p.d_o_b.isoformat() if p.d_o_b else None,
            'ssn': p.ssn,
            'first_name': p.pfirstname,
            'last_name': p.plastname,
            'pfir': p.pfirstname,
            'plast': p.plastname,
            'gender': p.gender,
            'blood_type': p.bloodtype,
            'street': p.pstreet,
            'city': p.pcity,
            'state': p.pstate,
            'zip': p.pzip
        } for p in patients
    ])

@app.route('/api/patients/<int:pid>', methods=['GET'])
def get_patient(pid):
    p = Patient.query.get_or_404(pid)
    return jsonify({
        'pid': p.pid,
        'primaryphysician': p.primaryphysician,
        'd_o_b': p.d_o_b.isoformat() if p.d_o_b else None,
        'ssn': p.ssn,
        'first_name': p.pfirstname,
        'last_name': p.plastname,
        'gender': p.gender,
        'blood_type': p.bloodtype,
        'street': p.pstreet,
        'city': p.pcity,
        'state': p.pstate,
        'zip': p.pzip
    })

@app.route('/api/patients', methods=['POST'])
def create_patient():
    data = request.get_json()
    # Check for duplicate SSN
    if Patient.query.filter_by(ssn=data['SSN']).first():
        return jsonify({'error': 'SSN already exists for a patient'}), 400
    # Find the current max pid
    max_pid = db.session.query(func.max(Patient.pid)).scalar()
    new_pid = (max_pid or 0) + 1
    patient = Patient(
        pid=new_pid,  # Set the new pid here
        primaryphysician=data['PrimaryPhysician'],
        d_o_b=data['D_O_B'],
        ssn=data['SSN'],
        pfirstname=data['PFirstName'],
        plastname=data['PLastName'],
        gender=data['Gender'],
        bloodtype=data['BloodType'],
        pstreet=data['PStreet'],
        pcity=data['PCity'],
        pstate=data['PState'],
        pzip=data['PZip']
    )
    db.session.add(patient)
    db.session.commit()
    return jsonify({'PID': patient.pid}), 201

@app.route('/api/patients/<int:pid>', methods=['PUT'])
def update_patient(pid):
    p = Patient.query.get_or_404(pid)
    data = request.get_json()
    p.primaryphysician = data.get('PrimaryPhysician', p.primaryphysician)
    p.d_o_b = data.get('D_O_B', p.d_o_b)
    p.ssn = data.get('SSN', p.ssn)
    p.pfirstname = data.get('PFirstName', p.pfirstname)
    p.plastname = data.get('PLastName', p.plastname)
    p.gender = data.get('Gender', p.gender)
    p.bloodtype = data.get('BloodType', p.bloodtype)
    p.pstreet = data.get('PStreet', p.pstreet)
    p.pcity = data.get('PCity', p.pcity)
    p.pstate = data.get('PState', p.pstate)
    p.pzip = data.get('PZip', p.pzip)
    db.session.commit()
    return jsonify({'PID': p.pid})

@app.route('/api/patients/<int:pid>', methods=['DELETE'])
def delete_patient(pid):
    p = Patient.query.get_or_404(pid)
    db.session.delete(p)
    db.session.commit()
    return jsonify({'message': 'Patient deleted'})

# --- Medical Data CRUD ---
@app.route('/api/medicaldata', methods=['GET'])
def get_medicaldata():
    records = Medical_Data.query.all()
    result = []
    for m in records:
        patient = Patient.query.get(m.pid)
        allergies = [{'name': a.allergy.description} for a in patient.allergies] if patient else []
        illnesses = [{'name': d.illness.description} for d in patient.diagnoses] if patient else []
        result.append({
            'patient_ssn': patient.ssn if patient else '',
            'patient_name': f"{patient.pfirstname} {patient.plastname}" if patient else '',
            'blood_type': patient.bloodtype if patient else '',
            'allergies': allergies,
            'illnesses': illnesses,
            'pid': m.pid,
            'blood_sugar': float(m.bloodsugar) if m.bloodsugar is not None else None,
            'cholesterol': float(m.cholesterol) if m.cholesterol is not None else None,
            'triglycerides': float(m.triglycerides) if m.triglycerides is not None else None,
            'hdl': float(m.hdl) if m.hdl is not None else None,
            'ldl': float(m.ldl) if m.ldl is not None else None,
            'last_update': m.lastupdate.isoformat() if m.lastupdate else None,
            'heart_risk': m.heart_risk
        })
    return jsonify(result)

@app.route('/api/medicaldata/<int:pid>', methods=['GET'])
def get_medicaldata_by_pid(pid):
    m = Medical_Data.query.get_or_404(pid)
    return jsonify({
        'pid': m.pid,
        'blood_sugar': float(m.bloodsugar) if m.bloodsugar is not None else None,
        'cholesterol': float(m.cholesterol) if m.cholesterol is not None else None,
        'triglycerides': float(m.triglycerides) if m.triglycerides is not None else None,
        'hdl': float(m.hdl) if m.hdl is not None else None,
        'ldl': float(m.ldl) if m.ldl is not None else None,
        'last_update': m.lastupdate.isoformat() if m.lastupdate else None,
        'heart_risk': m.heart_risk
    })

@app.route('/api/medicaldata/<string:ssn>', methods=['GET'])
def get_medicaldata_by_ssn(ssn):
    # Find the patient by SSN
    patient = Patient.query.filter_by(ssn=ssn).first()
    if not patient:
        return jsonify({'error': 'Patient not found'}), 404
    # Find the medical data by PID
    m = Medical_Data.query.filter_by(pid=patient.pid).first()
    if not m:
        return jsonify({'error': 'Medical data not found'}), 404
    # Get allergies and illnesses
    allergies = [{'name': a.allergy.description} for a in patient.allergies] if patient else []
    illnesses = [{'name': d.illness.description} for d in patient.diagnoses] if patient else []
    return jsonify({
        'pid': m.pid,
        'blood_sugar': float(m.bloodsugar) if m.bloodsugar is not None else None,
        'cholesterol': float(m.cholesterol) if m.cholesterol is not None else None,
        'triglycerides': float(m.triglycerides) if m.triglycerides is not None else None,
        'hdl': float(m.hdl) if m.hdl is not None else None,
        'ldl': float(m.ldl) if m.ldl is not None else None,
        'last_update': m.lastupdate.isoformat() if m.lastupdate else None,
        'heart_risk': m.heart_risk,
        'blood_type': patient.bloodtype,
        'allergies': allergies,
        'illnesses': illnesses
    })

@app.route('/api/medicaldata', methods=['POST'])
def create_medicaldata():
    data = request.get_json()
    m = Medical_Data(
        pid=data['PID'],
        bloodsugar=data.get('BloodSugar'),
        cholesterol=data.get('Cholesterol'),
        triglycerides=data.get('Triglycerides'),
        hdl=data.get('HDL'),
        ldl=data.get('LDL'),
        lastupdate=date.today()  # Set automatically
        # Do not set heart_risk, let DB calculate
    )
    db.session.add(m)
    db.session.commit()
    return jsonify({'PID': m.pid}), 201

@app.route('/api/medicaldata/<int:pid>', methods=['PUT'])
def update_medicaldata(pid):
    m = Medical_Data.query.get_or_404(pid)
    data = request.get_json()
    m.bloodsugar = data.get('BloodSugar', m.bloodsugar)
    m.cholesterol = data.get('Cholesterol', m.cholesterol)
    m.triglycerides = data.get('Triglycerides', m.triglycerides)
    m.hdl = data.get('HDL', m.hdl)
    m.ldl = data.get('LDL', m.ldl)
    m.lastupdate = data.get('LastUpdate', m.lastupdate)
    m.heart_risk = data.get('Heart_Risk', m.heart_risk)
    db.session.commit()
    return jsonify({'PID': m.pid})

@app.route('/api/medicaldata/<int:pid>', methods=['DELETE'])
def delete_medicaldata(pid):
    m = Medical_Data.query.get_or_404(pid)
    db.session.delete(m)
    db.session.commit()
    return jsonify({'message': 'MedicalData deleted'})

# --- Clinic Bed CRUD ---
@app.route('/api/clinicbeds', methods=['GET'])
def get_clinicbeds():
    beds = Clinic_Bed.query.all()
    return jsonify([
        {
            'BedID': b.bedid,
            'Clinic': b.clinic,
            'RoomNum': b.roomnum,
            'BedLetter': b.bedletter,
            'Unit': b.unit,
            'Wing': b.wing
        } for b in beds
    ])

@app.route('/api/clinicbeds/<int:bedid>', methods=['GET'])
def get_clinicbed(bedid):
    b = Clinic_Bed.query.get_or_404(bedid)
    return jsonify({
        'BedID': b.bedid,
        'Clinic': b.clinic,
        'RoomNum': b.roomnum,
        'BedLetter': b.bedletter,
        'Unit': b.unit,
        'Wing': b.wing
    })

@app.route('/api/clinicbeds', methods=['POST'])
def create_clinicbed():
    data = request.get_json()
    b = Clinic_Bed(
        clinic=data['Clinic'],
        roomnum=data['RoomNum'],
        bedletter=data['BedLetter'],
        unit=data['Unit'],
        wing=data['Wing']
    )
    db.session.add(b)
    db.session.commit()
    return jsonify({'BedID': b.bedid}), 201

@app.route('/api/clinicbeds/<int:bedid>', methods=['PUT'])
def update_clinicbed(bedid):
    b = Clinic_Bed.query.get_or_404(bedid)
    data = request.get_json()
    b.clinic = data.get('Clinic', b.clinic)
    b.roomnum = data.get('RoomNum', b.roomnum)
    b.bedletter = data.get('BedLetter', b.bedletter)
    b.unit = data.get('Unit', b.unit)
    b.wing = data.get('Wing', b.wing)
    db.session.commit()
    return jsonify({'BedID': b.bedid})

@app.route('/api/clinicbeds/<int:bedid>', methods=['DELETE'])
def delete_clinicbed(bedid):
    b = Clinic_Bed.query.get_or_404(bedid)
    db.session.delete(b)
    db.session.commit()
    return jsonify({'message': 'ClinicBed deleted'})

# --- AdmittedTo CRUD ---
@app.route('/api/admittedto', methods=['GET'])
def get_admittedto():
    admitted = AdmittedTo.query.all()
    return jsonify([
        {
            'PID': a.pid,
            'BedID': a.bedid,
            'Date_IN': a.date_in.isoformat() if a.date_in else None,
            'Date_OUT': a.date_out.isoformat() if a.date_out else None
        } for a in admitted
    ])

@app.route('/api/admittedto', methods=['POST'])
def create_admittedto():
    data = request.get_json()
    admitted = AdmittedTo(
        pid=data['PID'],
        bedid=data['BedID'],
        date_in=data['Date_IN'],
        date_out=data.get('Date_OUT')
    )
    db.session.add(admitted)
    db.session.commit()
    return jsonify({'PID': admitted.pid, 'BedID': admitted.bedid}), 201

@app.route('/api/admittedto/<int:pid>/<int:bedid>', methods=['PUT'])
def update_admittedto(pid, bedid):
    admitted = AdmittedTo.query.get_or_404((pid, bedid))
    data = request.get_json()
    admitted.date_in = data.get('Date_IN', admitted.date_in)
    admitted.date_out = data.get('Date_OUT', admitted.date_out)
    db.session.commit()
    return jsonify({'PID': admitted.pid, 'BedID': admitted.bedid})

@app.route('/api/admittedto/<int:pid>/<int:bedid>', methods=['DELETE'])
def delete_admittedto(pid, bedid):
    admitted = AdmittedTo.query.get_or_404((pid, bedid))
    db.session.delete(admitted)
    db.session.commit()
    return jsonify({'message': 'Admission record deleted'})

# --- AttendsTo CRUD ---
@app.route('/api/attendsto', methods=['GET'])
def get_attendsto():
    attends = AttendsTo.query.all()
    return jsonify([
        {
            'NurseID': a.nurseid,
            'PID': a.pid,
            'StartDate': a.startdate.isoformat() if a.startdate else None,
            'EndDate': a.enddate.isoformat() if a.enddate else None
        } for a in attends
    ])

@app.route('/api/attendsto', methods=['POST'])
def create_attendsto():
    data = request.get_json()
    attends = AttendsTo(
        nurseid=data['NurseID'],
        pid=data['PID'],
        startdate=data['StartDate'],
        enddate=data.get('EndDate')
    )
    db.session.add(attends)
    db.session.commit()
    return jsonify({'NurseID': attends.nurseid, 'PID': attends.pid}), 201

@app.route('/api/attendsto/<int:nurseid>/<int:pid>', methods=['PUT'])
def update_attendsto(nurseid, pid):
    attends = AttendsTo.query.get_or_404((nurseid, pid))
    data = request.get_json()
    attends.startdate = data.get('StartDate', attends.startdate)
    attends.enddate = data.get('EndDate', attends.enddate)
    db.session.commit()
    return jsonify({'NurseID': attends.nurseid, 'PID': attends.pid})

@app.route('/api/attendsto/<int:nurseid>/<int:pid>', methods=['DELETE'])
def delete_attendsto(nurseid, pid):
    attends = AttendsTo.query.get_or_404((nurseid, pid))
    db.session.delete(attends)
    db.session.commit()
    return jsonify({'message': 'AttendsTo record deleted'})

# --- Illness CRUD ---
@app.route('/api/illnesses', methods=['GET'])
def get_illnesses():
    illnesses = Illness.query.all()
    return jsonify([
        {'IllnessCode': i.illnesscode, 'Description': i.description} for i in illnesses
    ])

@app.route('/api/illnesses/<int:illnesscode>', methods=['GET'])
def get_illness(illnesscode):
    i = Illness.query.get_or_404(illnesscode)
    return jsonify({'IllnessCode': i.illnesscode, 'Description': i.description})

@app.route('/api/illnesses', methods=['POST'])
def create_illness():
    data = request.get_json()
    i = Illness(illnesscode=data['IllnessCode'], description=data['Description'])
    db.session.add(i)
    db.session.commit()
    return jsonify({'IllnessCode': i.illnesscode}), 201

@app.route('/api/illnesses/<int:illnesscode>', methods=['PUT'])
def update_illness(illnesscode):
    i = Illness.query.get_or_404(illnesscode)
    data = request.get_json()
    i.description = data.get('Description', i.description)
    db.session.commit()
    return jsonify({'IllnessCode': i.illnesscode})

@app.route('/api/illnesses/<int:illnesscode>', methods=['DELETE'])
def delete_illness(illnesscode):
    i = Illness.query.get_or_404(illnesscode)
    db.session.delete(i)
    db.session.commit()
    return jsonify({'message': 'Illness deleted'})

# --- Allergy CRUD ---
@app.route('/api/allergies', methods=['GET'])
def get_allergies():
    allergies = Allergy.query.all()
    return jsonify([
        {'allergycode': a.allergycode, 'description': a.description} for a in allergies
    ])

@app.route('/api/allergies/<int:allergycode>', methods=['GET'])
def get_allergy(allergycode):
    a = Allergy.query.get_or_404(allergycode)
    return jsonify({'allergycode': a.allergycode, 'description': a.description})

@app.route('/api/allergies', methods=['POST'])
def create_allergy():
    data = request.get_json()
    a = Allergy(allergycode=data['AllergyCode'], description=data['Description'])
    db.session.add(a)
    db.session.commit()
    return jsonify({'allergycode': a.allergycode}), 201

@app.route('/api/allergies/<int:allergycode>', methods=['PUT'])
def update_allergy(allergycode):
    a = Allergy.query.get_or_404(allergycode)
    data = request.get_json()
    a.description = data.get('Description', a.description)
    db.session.commit()
    return jsonify({'allergycode': a.allergycode})

@app.route('/api/allergies/<int:allergycode>', methods=['DELETE'])
def delete_allergy(allergycode):
    a = Allergy.query.get_or_404(allergycode)
    db.session.delete(a)
    db.session.commit()
    return jsonify({'message': 'Allergy deleted'})

# --- Patient_Allergy CRUD ---
@app.route('/api/patientallergies', methods=['GET'])
def get_patientallergies():
    records = Patient_Allergy.query.all()
    return jsonify([
        {'PID': r.pid, 'AllergyCode': r.allergycode} for r in records
    ])

@app.route('/api/patientallergies', methods=['POST'])
def create_patientallergy():
    data = request.get_json()
    r = Patient_Allergy(pid=data['PID'], allergycode=data['AllergyCode'])
    db.session.add(r)
    db.session.commit()
    return jsonify({'PID': r.pid, 'AllergyCode': r.allergycode}), 201

@app.route('/api/patientallergies/<int:pid>/<int:allergycode>', methods=['DELETE'])
def delete_patientallergy(pid, allergycode):
    r = Patient_Allergy.query.get_or_404((pid, allergycode))
    db.session.delete(r)
    db.session.commit()
    return jsonify({'message': 'Patient_Allergy deleted'})

# --- Diagnosis CRUD ---
@app.route('/api/diagnoses', methods=['GET'])
def get_diagnoses():
    records = Diagnosis.query.all()
    return jsonify([
        {
            'PID': d.pid,
            'PhysicianID': d.physicianid,
            'IllnessCode': d.illnesscode,
            'Date': d.date.isoformat() if d.date else None,
            'Notes': d.notes,
            'Comment': d.comment
        } for d in records
    ])

@app.route('/api/diagnoses', methods=['POST'])
def create_diagnosis():
    data = request.get_json()
    d = Diagnosis(
        pid=data['PID'],
        physicianid=data['PhysicianID'],
        illnesscode=data['IllnessCode'],
        date=data['Date'],
        notes=data.get('Notes'),
        comment=data.get('Comment')
    )
    db.session.add(d)
    db.session.commit()
    return jsonify({'PID': d.pid, 'PhysicianID': d.physicianid, 'IllnessCode': d.illnesscode}), 201

@app.route('/api/diagnoses/<int:pid>/<int:physicianid>/<int:illnesscode>', methods=['DELETE'])
def delete_diagnosis(pid, physicianid, illnesscode):
    d = Diagnosis.query.get_or_404((pid, physicianid, illnesscode))
    db.session.delete(d)
    db.session.commit()
    return jsonify({'message': 'Diagnosis deleted'})

# --- Consultation CRUD ---
@app.route('/api/consultations', methods=['GET'])
def get_consultations():
    records = Consultation.query.all()
    return jsonify([
        {
            'pid': c.pid,
            'physicianid': c.physicianid,
            'date': c.date.isoformat() if c.date else None,
            'reason': c.type,
            'notes': getattr(c, 'notes', None),
            'type': c.type
        } for c in records
    ])

@app.route('/api/consultations', methods=['POST'])
def create_consultation():
    data = request.get_json()
    c = Consultation(
        pid=data['pid'],
        physicianid=data['physicianid'],
        date=data['date'],
        type=data.get('reason', ''),
        notes=data.get('notes', None)
    )
    db.session.add(c)
    db.session.commit()
    return jsonify({'pid': c.pid, 'physicianid': c.physicianid, 'date': c.date}), 201

@app.route('/api/consultations/<int:pid>/<int:physicianid>/<date>', methods=['PUT'])
def update_consultation(pid, physicianid, date):
    c = Consultation.query.get_or_404((pid, physicianid, date))
    data = request.get_json()
    c.type = data.get('reason', c.type)
    c.notes = data.get('notes', c.notes)
    db.session.commit()
    return jsonify({'pid': c.pid, 'physicianid': c.physicianid, 'date': c.date})

@app.route('/api/consultations/<int:pid>/<int:physicianid>/<date>', methods=['DELETE'])
def delete_consultation(pid, physicianid, date):
    c = Consultation.query.get_or_404((pid, physicianid, date))
    db.session.delete(c)
    db.session.commit()
    return jsonify({'message': 'Consultation deleted'})

# --- Medicine CRUD ---
@app.route('/api/medicines', methods=['GET'])
def get_medicines():
    medicines = Medicine.query.all()
    return jsonify([
        {
            'code': m.code,
            'madeby': m.madeby,
            'name': m.name,
            'usage': m.usage,
            'description': m.usage,  # For compatibility with old UI
            'unitcost': float(m.unitcost) if m.unitcost is not None else None,
            'quantity': m.quantity,
            'qtyordered': m.qtyordered
        } for m in medicines
    ])

@app.route('/api/medicines/<int:code>', methods=['GET'])
def get_medicine(code):
    m = Medicine.query.get_or_404(code)
    return jsonify({
        'code': m.code,
        'madeby': m.madeby,
        'name': m.name,
        'usage': m.usage,
        'description': m.usage,  # For compatibility with old UI
        'unitcost': float(m.unitcost) if m.unitcost is not None else None,
        'quantity': m.quantity,
        'qtyordered': m.qtyordered
    })

@app.route('/api/medicines', methods=['POST'])
def create_medicine():
    data = request.get_json()
    m = Medicine(
        code=data['code'],
        madeby=data.get('MadeBy'),
        name=data['Name'],
        usage=data.get('Usage'),
        unitcost=data['UnitCost'],
        quantity=data['Quantity'],
        qtyordered=data['QtyOrdered']
    )
    db.session.add(m)
    db.session.commit()
    return jsonify({'code': m.code}), 201

@app.route('/api/medicines/<int:code>', methods=['PUT'])
def update_medicine(code):
    m = Medicine.query.get_or_404(code)
    data = request.get_json()
    m.madeby = data.get('MadeBy', m.madeby)
    m.name = data.get('Name', m.name)
    m.usage = data.get('Usage', m.usage)
    m.unitcost = data.get('UnitCost', m.unitcost)
    m.quantity = data.get('Quantity', m.quantity)
    m.qtyordered = data.get('QtyOrdered', m.qtyordered)
    db.session.commit()
    return jsonify({'code': m.code})

@app.route('/api/medicines/<int:code>', methods=['DELETE'])
def delete_medicine(code):
    m = Medicine.query.get_or_404(code)
    db.session.delete(m)
    db.session.commit()
    return jsonify({'message': 'Medicine deleted'})

# --- ReactsWith CRUD ---
@app.route('/api/reactswith', methods=['GET'])
def get_reactswith():
    records = ReactsWith.query.all()
    return jsonify([
        {'Medicine1': r.medicine1, 'Medicine2': r.medicine2, 'Severity': r.severity} for r in records
    ])

@app.route('/api/reactswith', methods=['POST'])
def create_reactswith():
    data = request.get_json()
    r = ReactsWith(medicine1=data['Medicine1'], medicine2=data['Medicine2'], severity=data['Severity'])
    db.session.add(r)
    db.session.commit()
    return jsonify({'Medicine1': r.medicine1, 'Medicine2': r.medicine2}), 201

@app.route('/api/reactswith/<int:medicine1>/<int:medicine2>', methods=['DELETE'])
def delete_reactswith(medicine1, medicine2):
    r = ReactsWith.query.get_or_404((medicine1, medicine2))
    db.session.delete(r)
    db.session.commit()
    return jsonify({'message': 'ReactsWith deleted'})

# --- Prescription CRUD ---
@app.route('/api/prescriptions', methods=['GET'])
def get_prescriptions():
    prescriptions = Prescription.query.all()
    return jsonify([
        {
            'prescriptionid': p.prescriptionid,
            'pid': p.pid,
            'medicinecode': p.medicinecode,
            'prescriber': p.prescriber,
            'dateprescrbed': p.dateprescrbed.isoformat() if p.dateprescrbed else None,
            'dosage': p.dosage,
            'duration': p.duration,
            'frequency': p.frequency,
            'quantity': p.quantity
        } for p in prescriptions
    ])

@app.route('/api/prescriptions', methods=['POST'])
def create_prescription():
    data = request.get_json()
    # Find the current max prescriptionid
    max_prescriptionid = db.session.query(func.max(Prescription.prescriptionid)).scalar()
    new_prescriptionid = (max_prescriptionid or 0) + 1
    p = Prescription(
        prescriptionid=new_prescriptionid,  # Auto-generate prescriptionid
        pid=data['pid'],
        medicinecode=data['medicinecode'],
        prescriber=data['prescriber'],
        dateprescrbed=data['dateprescrbed'],
        dosage=data.get('dosage'),
        duration=data.get('duration'),
        frequency=data.get('frequency'),
        quantity=data.get('quantity')
    )
    db.session.add(p)
    db.session.commit()
    return jsonify({'prescriptionid': p.prescriptionid}), 201

@app.route('/api/prescriptions/<int:prescriptionid>', methods=['PUT'])
def update_prescription(prescriptionid):
    p = Prescription.query.get_or_404(prescriptionid)
    data = request.get_json()
    p.pid = data.get('pid', p.pid)
    p.medicinecode = data.get('medicinecode', p.medicinecode)
    p.prescriber = data.get('prescriber', p.prescriber)
    p.dateprescrbed = data.get('dateprescrbed', p.dateprescrbed)
    p.dosage = data.get('dosage', p.dosage)
    p.duration = data.get('duration', p.duration)
    p.frequency = data.get('frequency', p.frequency)
    p.quantity = data.get('quantity', p.quantity)
    db.session.commit()
    return jsonify({'prescriptionid': p.prescriptionid})

@app.route('/api/prescriptions/<int:prescriptionid>', methods=['DELETE'])
def delete_prescription(prescriptionid):
    p = Prescription.query.get_or_404(prescriptionid)
    db.session.delete(p)
    db.session.commit()
    return jsonify({'message': 'Prescription deleted'})

# --- Surgery_Type CRUD ---
@app.route('/api/surgerytypes', methods=['GET'])
def get_surgerytypes():
    types = Surgery_Type.query.all()
    return jsonify([
        {
            'SurgeryCode': t.surgerycode,
            'Name': t.name,
            'Type': t.type,
            'AnatomicLocation': t.anatomiclocation,
            'SpecialNeeds': t.specialneeds
        } for t in types
    ])

@app.route('/api/surgerytypes/<int:surgerycode>', methods=['GET'])
def get_surgerytype(surgerycode):
    t = Surgery_Type.query.get_or_404(surgerycode)
    return jsonify({
        'SurgeryCode': t.surgerycode,
        'Name': t.name,
        'Type': t.type,
        'AnatomicLocation': t.anatomiclocation,
        'SpecialNeeds': t.specialneeds
    })

@app.route('/api/surgerytypes', methods=['POST'])
def create_surgerytype():
    data = request.get_json()
    t = Surgery_Type(
        surgerycode=data['SurgeryCode'],
        name=data['Name'],
        type=data['Type'],
        anatomiclocation=data['AnatomicLocation'],
        specialneeds=data.get('SpecialNeeds')
    )
    db.session.add(t)
    db.session.commit()
    return jsonify({'SurgeryCode': t.surgerycode}), 201

@app.route('/api/surgerytypes/<int:surgerycode>', methods=['PUT'])
def update_surgerytype(surgerycode):
    t = Surgery_Type.query.get_or_404(surgerycode)
    data = request.get_json()
    t.name = data.get('Name', t.name)
    t.type = data.get('Type', t.type)
    t.anatomiclocation = data.get('AnatomicLocation', t.anatomiclocation)
    t.specialneeds = data.get('SpecialNeeds', t.specialneeds)
    db.session.commit()
    return jsonify({'SurgeryCode': t.surgerycode})

@app.route('/api/surgerytypes/<int:surgerycode>', methods=['DELETE'])
def delete_surgerytype(surgerycode):
    t = Surgery_Type.query.get_or_404(surgerycode)
    db.session.delete(t)
    db.session.commit()
    return jsonify({'message': 'Surgery_Type deleted'})

# --- Surgery_Skill CRUD ---
@app.route('/api/surgeryskills', methods=['GET'])
def get_surgeryskills():
    skills = Surgery_Skill.query.all()
    return jsonify([
        {'SkillCode': s.skillcode, 'Description': s.description} for s in skills
    ])

@app.route('/api/surgeryskills/<int:skillcode>', methods=['GET'])
def get_surgeryskill(skillcode):
    s = Surgery_Skill.query.get_or_404(skillcode)
    return jsonify({'SkillCode': s.skillcode, 'Description': s.description})

@app.route('/api/surgeryskills', methods=['POST'])
def create_surgeryskill():
    data = request.get_json()
    try:
        s = Surgery_Skill(skillcode=data['SkillCode'], description=data['Description'])
        db.session.add(s)
        db.session.commit()
        return jsonify({'SkillCode': s.skillcode}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400

@app.route('/api/surgeryskills/<int:skillcode>', methods=['PUT'])
def update_surgeryskill(skillcode):
    s = Surgery_Skill.query.get_or_404(skillcode)
    data = request.get_json()
    s.description = data.get('Description', s.description)
    db.session.commit()
    return jsonify({'SkillCode': s.skillcode})

@app.route('/api/surgeryskills/<int:skillcode>', methods=['DELETE'])
def delete_surgeryskill(skillcode):
    s = Surgery_Skill.query.get_or_404(skillcode)
    db.session.delete(s)
    db.session.commit()
    return jsonify({'message': 'Surgery_Skill deleted'})

# --- Surgery_Type_Skill CRUD ---
@app.route('/api/surgerytypeskills', methods=['GET'])
def get_surgerytypeskills():
    records = Surgery_Type_Skill.query.all()
    return jsonify([
        {'SurgeryCode': r.surgerycode, 'SkillCode': r.skillcode} for r in records
    ])

@app.route('/api/surgerytypeskills', methods=['POST'])
def create_surgerytypeskill():
    data = request.get_json()
    r = Surgery_Type_Skill(surgerycode=data['SurgeryCode'], skillcode=data['SkillCode'])
    db.session.add(r)
    db.session.commit()
    return jsonify({'SurgeryCode': r.surgerycode, 'SkillCode': r.skillcode}), 201

@app.route('/api/surgerytypeskills/<int:surgerycode>/<int:skillcode>', methods=['DELETE'])
def delete_surgerytypeskill(surgerycode, skillcode):
    r = Surgery_Type_Skill.query.get_or_404((surgerycode, skillcode))
    db.session.delete(r)
    db.session.commit()
    return jsonify({'message': 'Surgery_Type_Skill deleted'})

# --- Nurse_Skill CRUD ---
@app.route('/api/nurseskills', methods=['GET'])
def get_nurseskills():
    records = Nurse_Skill.query.all()
    return jsonify([
        {'NurseID': r.nurseid, 'SkillCode': r.skillcode} for r in records
    ])

@app.route('/api/nurseskills', methods=['POST'])
def create_nurseskill():
    data = request.get_json()
    try:
        r = Nurse_Skill(nurseid=data['NurseID'], skillcode=data['SkillCode'])
        db.session.add(r)
        db.session.commit()
        return jsonify({'NurseID': r.nurseid, 'SkillCode': r.skillcode}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400

@app.route('/api/nurseskills/<int:nurseid>/<int:skillcode>', methods=['DELETE'])
def delete_nurseskill(nurseid, skillcode):
    r = Nurse_Skill.query.get_or_404((nurseid, skillcode))
    db.session.delete(r)
    db.session.commit()
    return jsonify({'message': 'Nurse_Skill deleted'})

# --- Nurse_Surgery_Type CRUD ---
@app.route('/api/nursesurgerytypes', methods=['GET'])
def get_nursesurgerytypes():
    records = Nurse_Surgery_Type.query.all()
    return jsonify([
        {'NurseID': r.nurseid, 'SurgeryCode': r.surgerycode} for r in records
    ])

@app.route('/api/nursesurgerytypes', methods=['POST'])
def create_nursesurgerytype():
    data = request.get_json()
    r = Nurse_Surgery_Type(nurseid=data['NurseID'], surgerycode=data['SurgeryCode'])
    db.session.add(r)
    db.session.commit()
    return jsonify({'NurseID': r.nurseid, 'SurgeryCode': r.surgerycode}), 201

@app.route('/api/nursesurgerytypes/<int:nurseid>/<int:surgerycode>', methods=['DELETE'])
def delete_nursesurgerytype(nurseid, surgerycode):
    r = Nurse_Surgery_Type.query.get_or_404((nurseid, surgerycode))
    db.session.delete(r)
    db.session.commit()
    return jsonify({'message': 'Nurse_Surgery_Type deleted'})

# --- Surgery_Schedule CRUD ---
@app.route('/api/surgeryschedules', methods=['GET'])
def get_surgeryschedules():
    records = Surgery_Schedule.query.all()
    return jsonify([
        {'NurseID': r.nurseid, 'SurgeryShift': r.surgeryshift, 'Date': r.date.isoformat() if r.date else None} for r in records
    ])

@app.route('/api/surgeryschedules', methods=['POST'])
def create_surgeryschedule():
    data = request.get_json()
    r = Surgery_Schedule(nurseid=data['NurseID'], surgeryshift=data['SurgeryShift'], date=data['Date'])
    db.session.add(r)
    db.session.commit()
    return jsonify({'NurseID': r.nurseid, 'SurgeryShift': r.surgeryshift, 'Date': r.date}), 201

@app.route('/api/surgeryschedules/<int:nurseid>/<surgeryshift>/<date>', methods=['DELETE'])
def delete_surgeryschedule(nurseid, surgeryshift, date):
    r = Surgery_Schedule.query.get_or_404((nurseid, surgeryshift, date))
    db.session.delete(r)
    db.session.commit()
    return jsonify({'message': 'Surgery_Schedule deleted'})

# --- Surgery CRUD ---
@app.route('/api/surgeries', methods=['GET'])
def get_surgeries():
    records = Surgery.query.all()
    return jsonify([
        {
            'PID': s.pid,
            'SurgeonID': s.surgeonid,
            'SurgeryCode': s.surgerycode,
            'Date': s.date.isoformat() if s.date else None,
            'Theater': s.theater,
            'SurgeryShift': s.surgeryshift
        } for s in records
    ])

@app.route('/api/surgeries', methods=['POST'])
def create_surgery():
    data = request.get_json()
    nurses = data.get('Nurses', [])
    if not nurses or len(nurses) < 2:
        return jsonify({'error': 'At least two nurses must be assigned to the surgery.'}), 400
    s = Surgery(
        pid=data['PID'],
        surgeonid=data['SurgeonID'],
        surgerycode=data['SurgeryCode'],
        date=data['Date'],
        theater=data['Theater'],
        surgeryshift=data.get('SurgeryShift')
    )
    db.session.add(s)
    db.session.flush()  # Get PKs for Surgery_Schedule
    # Assign nurses to the surgery
    for nurse_id in nurses:
        # Prevent duplicate assignment
        exists = Surgery_Schedule.query.filter_by(nurseid=nurse_id, date=data['Date'], surgeryshift=data.get('SurgeryShift')).first()
        if exists:
            continue
        sched = Surgery_Schedule(nurseid=nurse_id, surgeryshift=data.get('SurgeryShift'), date=data['Date'])
        db.session.add(sched)
    db.session.commit()
    return jsonify({'PID': s.pid, 'SurgeonID': s.surgeonid, 'SurgeryCode': s.surgerycode, 'Date': s.date}), 201

@app.route('/api/surgeries/<int:pid>/<int:surgeonid>/<int:surgerycode>/<date>', methods=['DELETE'])
def delete_surgery(pid, surgeonid, surgerycode, date):
    s = Surgery.query.get_or_404((pid, surgeonid, surgerycode, date))
    db.session.delete(s)
    db.session.commit()
    return jsonify({'message': 'Surgery deleted'})

@app.route('/admin')
def admin_panel():
    return render_template('admin.html')

@app.route('/application')
def application_panel():
    return render_template('application.html')

@app.route('/application/surgeries')
def application_surgeries():
    return render_template('surgeries.html')

@app.route('/application/consultations')
def application_consultations():
    return render_template('consultations.html')

@app.route('/application/medicines')
def application_medicines():
    return render_template('medicines.html')

@app.route('/application/prescriptions')
def application_prescriptions():
    return render_template('prescriptions.html')

@app.route('/application/staff')
def application_staff():
    return render_template('staff.html')

@app.route('/application/patients')
def application_patients():
    return render_template('patients.html')

@app.route('/application/medical-records')
def application_medical_records():
    return render_template('medical-records.html')

@app.route('/application/shifts')
def application_shifts():
    return render_template('shifts.html')

@app.route('/application/in-patient-management')
def application_in_patient_management():
    return render_template('in-patient-management.html')

@app.route('/api/eligible_nurses', methods=['POST'])
def get_eligible_nurses():
    data = request.get_json()
    surgerycode = data['surgerycode']
    date_str = data['date']
    surgeryshift = data['surgeryshift'].strip() if data['surgeryshift'] else ''
    print(f"[DEBUG] Received: surgerycode={surgerycode}, date_str={date_str}, surgeryshift={surgeryshift}")
    try:
        date_obj = datetime.strptime(date_str, '%Y-%m-%d').date()
        print(f"[DEBUG] Parsed date_obj: {date_obj}")
    except Exception as e:
        print(f"[ERROR] Date parsing failed: {e}")
        return jsonify({'error': 'Invalid date format'}), 400

    # Nurses assigned to this surgery type
    assigned_nurses = db.session.query(Nurse_Surgery_Type.nurseid).filter_by(surgerycode=surgerycode).subquery()

    # Nurses already scheduled for a surgery at this date/shift
    busy_nurses = db.session.query(Surgery_Schedule.nurseid).filter_by(date=date_obj, surgeryshift=surgeryshift).subquery()

    # Eligible nurses: assigned to this surgery type and not busy
    eligible_nurses = db.session.query(Nurse).filter(
        Nurse.nurseid.in_(assigned_nurses.select()),
        ~Nurse.nurseid.in_(busy_nurses.select())
    ).all()

    result = [
        {'NurseID': n.nurseid, 'FirstName': n.employee.first_name, 'LastName': n.employee.last_name}
        for n in eligible_nurses
    ]
    return jsonify(result)

# --- Patient by SSN ---
@app.route('/api/patients/ssn/<string:ssn>', methods=['GET'])
def get_patient_by_ssn(ssn):
    p = Patient.query.filter_by(ssn=ssn).first_or_404()
    return jsonify({
        'pid': p.pid,
        'primaryphysician': p.primaryphysician,
        'd_o_b': p.d_o_b.isoformat() if p.d_o_b else None,
        'ssn': p.ssn,
        'first_name': p.pfirstname,
        'last_name': p.plastname,
        'gender': p.gender,
        'blood_type': p.bloodtype,
        'street': p.pstreet,
        'city': p.pcity,
        'state': p.pstate,
        'zip': p.pzip
    })

# --- Patient Allergies by PID ---
@app.route('/api/patients/<int:pid>/allergies', methods=['GET'])
def get_patient_allergies(pid):
    patient = Patient.query.get_or_404(pid)
    allergies = [
        {
            'allergycode': pa.allergycode,
            'description': pa.allergy.description
        }
        for pa in patient.allergies
    ]
    return jsonify(allergies)

# --- Patient Allergies by SSN ---
@app.route('/api/patients/ssn/<string:ssn>/allergies', methods=['GET'])
def get_patient_allergies_by_ssn(ssn):
    patient = Patient.query.filter_by(ssn=ssn).first_or_404()
    allergies = [
        {
            'allergycode': pa.allergycode,
            'description': pa.allergy.description
        }
        for pa in patient.allergies
    ]
    return jsonify(allergies)

# --- Add Allergy to Patient (by PID) ---
@app.route('/api/patients/<int:pid>/allergies', methods=['POST'])
def add_patient_allergy(pid):
    data = request.get_json()
    allergy_code = data['AllergyCode']
    # Check if already exists
    if Patient_Allergy.query.get((pid, allergy_code)):
        return jsonify({'error': 'Allergy already exists for this patient'}), 400
    pa = Patient_Allergy(pid=pid, allergycode=allergy_code)
    db.session.add(pa)
    db.session.commit()
    return jsonify({'PID': pid, 'AllergyCode': allergy_code}), 201

# --- Delete Allergy from Patient (by PID) ---
@app.route('/api/patients/<int:pid>/allergies/<int:allergycode>', methods=['DELETE'])
def delete_patient_allergy(pid, allergycode):
    pa = Patient_Allergy.query.get_or_404((pid, allergycode))
    db.session.delete(pa)
    db.session.commit()
    return jsonify({'message': 'Allergy removed from patient'})

@app.route('/api/worksshift', methods=['GET'])
def get_worksshift():
    assignments = WorksShift.query.all()
    result = []
    for a in assignments:
        emp = Employee.query.filter_by(ssn=a.employee_ssn).first()
        result.append({
            'empid': a.empid,
            'day': a.day,
            'employee_ssn': a.employee_ssn,
            'employee_name': f"{emp.first_name} {emp.last_name}" if emp else ''
        })
    return jsonify(result)

@app.route('/api/worksshift', methods=['POST'])
def assign_worksshift():
    data = request.get_json()
    empid = int(data['empid']) if 'empid' in data else int(data['employee_ssn'].split('-')[0])
    day = data['day'] if 'day' in data else data['shift_id'].split('-')[1]
    employee_ssn = data['employee_ssn']
    assignment = WorksShift(empid=empid, day=day, employee_ssn=employee_ssn)
    db.session.add(assignment)
    db.session.commit()
    return jsonify({'empid': empid, 'day': day, 'employee_ssn': employee_ssn}), 201

@app.route('/api/worksshift/<empid>/<day>/<employee_ssn>', methods=['DELETE'])
def delete_worksshift(empid, day, employee_ssn):
    assignment = WorksShift.query.get_or_404((int(empid), day, employee_ssn))
    db.session.delete(assignment)
    db.session.commit()
    return jsonify({'message': 'Assignment deleted'})

# --- Patient Diagnoses by PID ---
@app.route('/api/patients/<int:pid>/diagnoses', methods=['GET'])
def get_patient_diagnoses(pid):
    diagnoses = Diagnosis.query.filter_by(pid=pid).all()
    result = []
    for d in diagnoses:
        result.append({
            'pid': d.pid,
            'physicianid': d.physicianid,
            'illnesscode': d.illnesscode,
            'date': d.date.isoformat() if d.date else None,
            'notes': d.notes,
            'comment': d.comment,
            'illness_description': d.illness.description if d.illness else None
        })
    return jsonify(result)

# --- Patient Illnesses by PID ---
@app.route('/api/patients/<int:pid>/illnesses', methods=['GET'])
def get_patient_illnesses(pid):
    diagnoses = Diagnosis.query.filter_by(pid=pid).all()
    illnesses = {}
    for d in diagnoses:
        if d.illness:
            illnesses[d.illness.illnesscode] = d.illness.description
    result = [{'code': code, 'description': desc} for code, desc in illnesses.items()]
    return jsonify(result)

@app.route('/api/patients/<int:pid>/assign_doctor', methods=['POST'])
def assign_doctor_to_patient(pid):
    data = request.get_json()
    doctor_id = data['PhysicianID']
    patient = Patient.query.get_or_404(pid)
    patient.primaryphysician = doctor_id
    db.session.commit()
    return jsonify({'pid': pid, 'primaryphysician': doctor_id})

@app.route('/api/patients/<int:pid>/assign_doctor', methods=['DELETE'])
def remove_doctor_from_patient(pid):
    patient = Patient.query.get_or_404(pid)
    patient.primaryphysician = None
    db.session.commit()
    return jsonify({'pid': pid, 'primaryphysician': None})

@app.route('/api/patients/<int:pid>/assign_nurse', methods=['POST'])
def assign_nurse_to_patient(pid):
    try:
        data = request.get_json()
        nurse_id = data['NurseID']
        from datetime import date
        # Check if already assigned
        exists = AttendsTo.query.filter_by(pid=pid, nurseid=nurse_id, enddate=None).first()
        if exists:
            return jsonify({'error': 'Nurse already assigned'}), 400
        assignment = AttendsTo(pid=pid, nurseid=nurse_id, startdate=date.today())
        db.session.add(assignment)
        db.session.commit()
        return jsonify({'pid': pid, 'nurseid': nurse_id})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@app.route('/api/patients/<int:pid>/assign_nurse', methods=['DELETE'])
def remove_nurse_from_patient(pid):
    data = request.get_json()
    nurse_id = data['NurseID']
    assignment = AttendsTo.query.filter_by(pid=pid, nurseid=nurse_id, enddate=None).first_or_404()
    from datetime import date
    assignment.enddate = date.today()
    db.session.commit()
    return jsonify({'pid': pid, 'nurseid': nurse_id, 'removed': True})

@app.route('/api/nurses_without_skill', methods=['GET'])
def get_nurses_without_skill():
    # Subquery to get all nurseids that have a nurse_skill
    from sqlalchemy.orm import aliased
    skilled_nurseids = db.session.query(Nurse_Skill.nurseid).distinct()
    # Get all nurses whose nurseid is not in skilled_nurseids
    nurses = Nurse.query.filter(~Nurse.nurseid.in_(skilled_nurseids)).all()
    return jsonify([
        {
            'nurseid': n.nurseid,
            'grade': n.grade,
            'years': n.years,
            'first_name': n.employee.first_name if n.employee else '',
            'last_name': n.employee.last_name if n.employee else ''
        } for n in nurses
    ])

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True) 