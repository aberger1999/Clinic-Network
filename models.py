from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import CheckConstraint, UniqueConstraint, ForeignKey, PrimaryKeyConstraint, Date, Time, DECIMAL, Integer, String, Text, Column, CHAR
from sqlalchemy.orm import relationship

# Initialize SQLAlchemy

# --- Base DB ---
db = SQLAlchemy()

# --- EMPLOYEE-RELATED TABLES ---
class Employee(db.Model):
    __tablename__ = 'employee'
    empid = db.Column('empid', db.Integer, primary_key=True)
    first_name = db.Column('first_name', db.String(50), nullable=False)
    last_name = db.Column('last_name', db.String(50), nullable=False)
    ssn = db.Column('ssn', db.String(11), unique=True, nullable=False)
    salary = db.Column('salary', db.Numeric(10,2), nullable=True)
    gender = db.Column('gender', db.CHAR(1), CheckConstraint("gender IN ('M', 'F')"))
    employeetype = db.Column('employeetype', db.String(20), nullable=False)
    phone = db.Column('phone', db.String(15), nullable=False)
    street = db.Column('street', db.String(100), nullable=False)
    city = db.Column('city', db.String(50), nullable=False)
    state = db.Column('state', db.CHAR(2), nullable=False)
    zip = db.Column('zip', db.String(10), nullable=False)
    # Relationships
    physician = relationship('Physician', uselist=False, back_populates='employee')
    nurse = relationship('Nurse', uselist=False, back_populates='employee')
    surgeon = relationship('Surgeon', uselist=False, back_populates='employee')
    shifts = relationship('Shift', back_populates='employee', cascade="all, delete-orphan")

    __table_args__ = (
        CheckConstraint('(salary BETWEEN 25000 AND 300000) OR salary IS NULL'),
        CheckConstraint("employeetype IN ('Physician', 'Nurse', 'Surgeon', 'Support')"),
    )

class Physician(db.Model):
    __tablename__ = 'physician'
    physicianid = db.Column('physicianid', db.Integer, db.ForeignKey('employee.empid', ondelete='CASCADE'), primary_key=True)
    specialty = db.Column('specialty', db.String(50), nullable=False)
    type = db.Column('type', db.String(50), nullable=False)
    employee = relationship('Employee', back_populates='physician')
    clinics_owned = relationship('Clinic', back_populates='owner')
    patients = relationship('Patient', back_populates='primary_physician')
    diagnoses = relationship('Diagnosis', back_populates='physician')
    consultations = relationship('Consultation', back_populates='physician')
    prescriptions = relationship('Prescription', back_populates='prescriber_rel', foreign_keys='Prescription.prescriber')

class Nurse(db.Model):
    __tablename__ = 'nurse'
    nurseid = db.Column('nurseid', db.Integer, db.ForeignKey('employee.empid', ondelete='CASCADE'), primary_key=True)
    grade = db.Column('grade', db.String(20), nullable=False)
    years = db.Column('years', db.Integer, nullable=False)
    employee = relationship('Employee', back_populates='nurse')
    attends_to = relationship('AttendsTo', back_populates='nurse')
    nurse_skills = relationship('Nurse_Skill', back_populates='nurse')
    nurse_surgery_types = relationship('Nurse_Surgery_Type', back_populates='nurse')
    surgery_schedules = relationship('Surgery_Schedule', back_populates='nurse')

class Surgeon(db.Model):
    __tablename__ = 'surgeon'
    surgeonid = db.Column('surgeonid', db.Integer, db.ForeignKey('employee.empid', ondelete='CASCADE'), primary_key=True)
    specialty = db.Column('specialty', db.String(50), nullable=False)
    contracttype = db.Column('contracttype', db.String(50), nullable=False)
    contractduration = db.Column('contractduration', db.Integer, nullable=False)
    contractamount = db.Column('contractamount', db.Numeric(10,2), nullable=True)
    employee = relationship('Employee', back_populates='surgeon')
    surgeries = relationship('Surgery', back_populates='surgeon')

# --- CLINIC-RELATED TABLES ---
class Clinic(db.Model):
    __tablename__ = 'clinic'
    name = db.Column('name', db.String(100), primary_key=True)
    street = db.Column('street', db.String(100), nullable=False)
    city = db.Column('city', db.String(50), nullable=False)
    state = db.Column('state', db.CHAR(2), nullable=False)
    zip = db.Column('zip', db.String(10), nullable=False)
    ownerid = db.Column('ownerid', db.Integer, db.ForeignKey('physician.physicianid', ondelete='SET NULL'), nullable=True)
    owner = relationship('Physician', back_populates='clinics_owned')
    beds = relationship('Clinic_Bed', back_populates='clinic_rel', cascade="all, delete-orphan")

class Corporation(db.Model):
    __tablename__ = 'corporation'
    name = db.Column('name', db.String(100), primary_key=True)
    percentown = db.Column('percentown', db.Numeric(5,2), nullable=False)
    headquartersstreet = db.Column('headquartersstreet', db.String(100), nullable=False)
    headquarterscity = db.Column('headquarterscity', db.String(50), nullable=False)
    headquartersstate = db.Column('headquartersstate', db.CHAR(2), nullable=False)
    headquarterszip = db.Column('headquarterszip', db.String(10), nullable=False)
    medicines = relationship('Medicine', back_populates='corporation')

class Clinic_Bed(db.Model):
    __tablename__ = 'clinic_bed'
    bedid = db.Column('bedid', db.Integer, primary_key=True)
    clinic = db.Column('clinic', db.String(100), db.ForeignKey('clinic.name', ondelete='CASCADE'), nullable=False)
    roomnum = db.Column('roomnum', db.Integer, nullable=False)
    bedletter = db.Column('bedletter', db.CHAR(1), CheckConstraint("bedletter IN ('A', 'B')"), nullable=False)
    unit = db.Column('unit', db.Integer, CheckConstraint('unit BETWEEN 1 AND 7'), nullable=False)
    wing = db.Column('wing', db.String(5), CheckConstraint("wing IN ('Blue', 'Green')"), nullable=False)
    clinic_rel = relationship('Clinic', back_populates='beds')
    admitted_to = relationship('AdmittedTo', back_populates='bed')
    __table_args__ = (
        UniqueConstraint('clinic', 'roomnum', 'bedletter', name='uq_bed'),
    )

# --- PATIENT-RELATED TABLES ---
class Patient(db.Model):
    __tablename__ = 'patient'
    pid = db.Column('pid', db.Integer, primary_key=True)
    primaryphysician = db.Column('primaryphysician', db.Integer, db.ForeignKey('physician.physicianid', ondelete='SET NULL'), nullable=True)
    d_o_b = db.Column('d_o_b', db.Date, nullable=False)
    ssn = db.Column('ssn', db.String(11), unique=True, nullable=False)
    pfirstname = db.Column('pfirstname', db.String(50), nullable=False)
    plastname = db.Column('plastname', db.String(50), nullable=False)
    gender = db.Column('gender', db.CHAR(1), CheckConstraint("gender IN ('M', 'F')"))
    bloodtype = db.Column('bloodtype', db.String(3), CheckConstraint("bloodtype IN ('A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-')"), nullable=False)
    pstreet = db.Column('pstreet', db.String(100), nullable=False)
    pcity = db.Column('pcity', db.String(50), nullable=False)
    pstate = db.Column('pstate', db.CHAR(2), nullable=False)
    pzip = db.Column('pzip', db.String(10), nullable=False)
    primary_physician = relationship('Physician', back_populates='patients')
    medical_data = relationship('Medical_Data', uselist=False, back_populates='patient')
    admitted_to = relationship('AdmittedTo', back_populates='patient')
    attends_to = relationship('AttendsTo', back_populates='patient')
    diagnoses = relationship('Diagnosis', back_populates='patient')
    allergies = relationship('Patient_Allergy', back_populates='patient')
    consultations = relationship('Consultation', back_populates='patient')
    prescriptions = relationship('Prescription', back_populates='patient')

class Medical_Data(db.Model):
    __tablename__ = 'medical_data'
    pid = db.Column('pid', db.Integer, db.ForeignKey('patient.pid', ondelete='CASCADE'), primary_key=True)
    bloodsugar = db.Column('bloodsugar', db.Numeric(5,1))
    cholesterol = db.Column('cholesterol', db.Numeric(5,1))
    triglycerides = db.Column('triglycerides', db.Numeric(5,1))
    hdl = db.Column('hdl', db.Numeric(5,1))
    ldl = db.Column('ldl', db.Numeric(5,1))
    lastupdate = db.Column('lastupdate', db.Date, nullable=False)
    heart_risk = db.Column('heart_risk', db.CHAR(1), CheckConstraint("heart_risk IN ('N', 'L', 'M', 'H')"))
    patient = relationship('Patient', back_populates='medical_data')

class AdmittedTo(db.Model):
    __tablename__ = 'admittedto'
    pid = db.Column('pid', db.Integer, db.ForeignKey('patient.pid', ondelete='CASCADE'), primary_key=True)
    bedid = db.Column('bedid', db.Integer, db.ForeignKey('clinic_bed.bedid', ondelete='CASCADE'), primary_key=True)
    date_in = db.Column('date_in', db.Date, nullable=False)
    date_out = db.Column('date_out', db.Date, nullable=True)
    patient = relationship('Patient', back_populates='admitted_to')
    bed = relationship('Clinic_Bed', back_populates='admitted_to')
    __table_args__ = (
        CheckConstraint('date_out IS NULL OR date_out >= date_in'),
    )

class AttendsTo(db.Model):
    __tablename__ = 'attendsto'
    nurseid = db.Column('nurseid', db.Integer, db.ForeignKey('nurse.nurseid', ondelete='CASCADE'), primary_key=True)
    pid = db.Column('pid', db.Integer, db.ForeignKey('patient.pid', ondelete='CASCADE'), primary_key=True)
    startdate = db.Column('startdate', db.Date, nullable=False)
    enddate = db.Column('enddate', db.Date, nullable=True)
    nurse = relationship('Nurse', back_populates='attends_to')
    patient = relationship('Patient', back_populates='attends_to')
    __table_args__ = (
        CheckConstraint('enddate IS NULL OR enddate >= startdate'),
    )

# --- ILLNESS AND ALLERGY TABLES ---
class Illness(db.Model):
    __tablename__ = 'illness'
    illnesscode = db.Column('illnesscode', db.Integer, primary_key=True)
    description = db.Column('description', db.String(255), nullable=False)
    diagnoses = relationship('Diagnosis', back_populates='illness')

class Allergy(db.Model):
    __tablename__ = 'allergy'
    allergycode = db.Column('allergycode', db.Integer, primary_key=True)
    description = db.Column('description', db.String(255), nullable=False)
    patient_allergies = relationship('Patient_Allergy', back_populates='allergy')

class Diagnosis(db.Model):
    __tablename__ = 'diagnosis'
    pid = db.Column('pid', db.Integer, db.ForeignKey('patient.pid', ondelete='CASCADE'), primary_key=True)
    physicianid = db.Column('physicianid', db.Integer, db.ForeignKey('physician.physicianid', ondelete='CASCADE'), primary_key=True)
    illnesscode = db.Column('illnesscode', db.Integer, db.ForeignKey('illness.illnesscode', ondelete='CASCADE'), primary_key=True)
    date = db.Column('date', db.Date, nullable=False)
    notes = db.Column('notes', db.Text)
    comment = db.Column('comment', db.Text)
    patient = relationship('Patient', back_populates='diagnoses')
    physician = relationship('Physician', back_populates='diagnoses')
    illness = relationship('Illness', back_populates='diagnoses')

class Patient_Allergy(db.Model):
    __tablename__ = 'patient_allergy'
    pid = db.Column('pid', db.Integer, db.ForeignKey('patient.pid', ondelete='CASCADE'), primary_key=True)
    allergycode = db.Column('allergycode', db.Integer, db.ForeignKey('allergy.allergycode', ondelete='CASCADE'), primary_key=True)
    patient = relationship('Patient', back_populates='allergies')
    allergy = relationship('Allergy', back_populates='patient_allergies')

# --- CONSULTATION AND PRESCRIPTION TABLES ---
class Consultation(db.Model):
    __tablename__ = 'consultation'
    pid = db.Column('pid', db.Integer, db.ForeignKey('patient.pid', ondelete='CASCADE'), primary_key=True)
    physicianid = db.Column('physicianid', db.Integer, db.ForeignKey('physician.physicianid', ondelete='CASCADE'), primary_key=True)
    date = db.Column('date', db.Date, primary_key=True)
    type = db.Column('type', db.String(50), nullable=False)
    notes = db.Column('notes', db.Text, nullable=True)
    patient = relationship('Patient', back_populates='consultations')
    physician = relationship('Physician', back_populates='consultations')

class Medicine(db.Model):
    __tablename__ = 'medicine'
    code = db.Column('code', db.Integer, primary_key=True)
    madeby = db.Column('madeby', db.String(100), db.ForeignKey('corporation.name', ondelete='SET NULL'), nullable=True)
    name = db.Column('name', db.String(100), nullable=False)
    usage = db.Column('usage', db.String(255))
    unitcost = db.Column('unitcost', db.Numeric(10,2), nullable=False)
    quantity = db.Column('quantity', db.Integer, nullable=False)
    qtyordered = db.Column('qtyordered', db.Integer, nullable=False)
    corporation = relationship('Corporation', back_populates='medicines')
    prescriptions = relationship('Prescription', back_populates='medicine')

class ReactsWith(db.Model):
    __tablename__ = 'reactswith'
    medicine1 = db.Column('medicine1', db.Integer, db.ForeignKey('medicine.code', ondelete='CASCADE'), primary_key=True)
    medicine2 = db.Column('medicine2', db.Integer, db.ForeignKey('medicine.code', ondelete='CASCADE'), primary_key=True)
    severity = db.Column('severity', db.CHAR(1), CheckConstraint("severity IN ('S', 'M', 'L', 'N')"), nullable=False)
    __table_args__ = (
        CheckConstraint('medicine1 < medicine2'),
    )

class Prescription(db.Model):
    __tablename__ = 'prescription'
    prescriptionid = db.Column('prescriptionid', db.Integer, primary_key=True)
    pid = db.Column('pid', db.Integer, db.ForeignKey('patient.pid', ondelete='CASCADE'), nullable=False)
    medicinecode = db.Column('medicinecode', db.Integer, db.ForeignKey('medicine.code', ondelete='CASCADE'), nullable=False)
    prescriber = db.Column('prescriber', db.Integer, db.ForeignKey('physician.physicianid', ondelete='CASCADE'), nullable=False)
    dateprescrbed = db.Column('dateprescrbed', db.Date, nullable=False)
    datefilled = db.Column('datefilled', db.Date, nullable=True)
    dosage = db.Column('dosage', db.String(50), nullable=False)
    duration = db.Column('duration', db.String(50), nullable=False)
    frequency = db.Column('frequency', db.String(50), nullable=False)
    quantity = db.Column('quantity', db.Integer, nullable=False)
    patient = relationship('Patient', back_populates='prescriptions')
    medicine = relationship('Medicine', back_populates='prescriptions')
    prescriber_rel = relationship('Physician', back_populates='prescriptions', foreign_keys=[prescriber])
    __table_args__ = (
        UniqueConstraint('pid', 'medicinecode', name='uq_patient_medicine'),
    )

# --- SURGERY-RELATED TABLES ---
class Surgery_Type(db.Model):
    __tablename__ = 'surgery_type'
    surgerycode = db.Column('surgerycode', db.Integer, primary_key=True)
    name = db.Column('name', db.String(100), nullable=False)
    type = db.Column('type', db.CHAR(1), CheckConstraint("type IN ('H', 'O')"), nullable=False)
    anatomiclocation = db.Column('anatomiclocation', db.String(100), nullable=False)
    specialneeds = db.Column('specialneeds', db.String(255))
    surgery_type_skills = relationship('Surgery_Type_Skill', back_populates='surgery_type')
    surgeries = relationship('Surgery', back_populates='surgery_type')
    nurse_surgery_types = relationship('Nurse_Surgery_Type', back_populates='surgery_type')

class Surgery_Skill(db.Model):
    __tablename__ = 'surgery_skill'
    skillcode = db.Column('skillcode', db.Integer, primary_key=True)
    description = db.Column('description', db.String(255), nullable=False)
    surgery_type_skills = relationship('Surgery_Type_Skill', back_populates='surgery_skill')
    nurse_skills = relationship('Nurse_Skill', back_populates='surgery_skill')

class Surgery_Type_Skill(db.Model):
    __tablename__ = 'surgery_type_skill'
    surgerycode = db.Column('surgerycode', db.Integer, db.ForeignKey('surgery_type.surgerycode', ondelete='CASCADE'), primary_key=True)
    skillcode = db.Column('skillcode', db.Integer, db.ForeignKey('surgery_skill.skillcode', ondelete='CASCADE'), primary_key=True)
    surgery_type = relationship('Surgery_Type', back_populates='surgery_type_skills')
    surgery_skill = relationship('Surgery_Skill', back_populates='surgery_type_skills')

class Nurse_Skill(db.Model):
    __tablename__ = 'nurse_skill'
    nurseid = db.Column('nurseid', db.Integer, db.ForeignKey('nurse.nurseid', ondelete='CASCADE'), primary_key=True)
    skillcode = db.Column('skillcode', db.Integer, db.ForeignKey('surgery_skill.skillcode', ondelete='CASCADE'), primary_key=True)
    nurse = relationship('Nurse', back_populates='nurse_skills')
    surgery_skill = relationship('Surgery_Skill', back_populates='nurse_skills')

class Nurse_Surgery_Type(db.Model):
    __tablename__ = 'nurse_surgery_type'
    nurseid = db.Column('nurseid', db.Integer, db.ForeignKey('nurse.nurseid', ondelete='CASCADE'), primary_key=True)
    surgerycode = db.Column('surgerycode', db.Integer, db.ForeignKey('surgery_type.surgerycode', ondelete='CASCADE'), primary_key=True)
    nurse = relationship('Nurse', back_populates='nurse_surgery_types')
    surgery_type = relationship('Surgery_Type', back_populates='nurse_surgery_types')

class Surgery_Schedule(db.Model):
    __tablename__ = 'surgery_schedule'
    nurseid = db.Column('nurseid', db.Integer, db.ForeignKey('nurse.nurseid', ondelete='CASCADE'), primary_key=True)
    surgeryshift = db.Column('surgeryshift', db.String(20), primary_key=True)
    date = db.Column('date', db.Date, primary_key=True)
    nurse = relationship('Nurse', back_populates='surgery_schedules')

class Surgery(db.Model):
    __tablename__ = 'surgery'
    pid = db.Column('pid', db.Integer, db.ForeignKey('patient.pid', ondelete='CASCADE'), primary_key=True)
    surgeonid = db.Column('surgeonid', db.Integer, db.ForeignKey('surgeon.surgeonid', ondelete='RESTRICT'), primary_key=True)
    surgerycode = db.Column('surgerycode', db.Integer, db.ForeignKey('surgery_type.surgerycode', ondelete='CASCADE'), primary_key=True)
    date = db.Column('date', db.Date, primary_key=True)
    theater = db.Column('theater', db.String(50), nullable=False)
    surgeryshift = db.Column('surgeryshift', db.String(20), nullable=True)
    patient = relationship('Patient')
    surgeon = relationship('Surgeon', back_populates='surgeries')
    surgery_type = relationship('Surgery_Type', back_populates='surgeries')

# --- SHIFT MANAGEMENT ---
class Shift(db.Model):
    __tablename__ = 'shift'
    empid = db.Column('empid', db.Integer, db.ForeignKey('employee.empid', ondelete='CASCADE'), primary_key=True)
    day = db.Column('day', db.String(10), primary_key=True)
    begintime = db.Column('begintime', db.Time, nullable=False)
    endtime = db.Column('endtime', db.Time, nullable=False)
    employee = relationship('Employee', back_populates='shifts')
    __table_args__ = (
        CheckConstraint('endtime > begintime'),
    )

class WorksShift(db.Model):
    __tablename__ = 'worksshift'
    empid = db.Column('empid', db.Integer, db.ForeignKey('employee.empid', ondelete='CASCADE'), primary_key=True)
    day = db.Column('day', db.String(10), primary_key=True)
    employee_ssn = db.Column('employee_ssn', db.String(11), db.ForeignKey('employee.ssn', ondelete='CASCADE'), primary_key=True)
    # Optionally, add relationships if needed
    # employee = relationship('Employee', foreign_keys=[employee_ssn])
    # shift = relationship('Shift', primaryjoin="and_(WorksShift.empid==Shift.empid, WorksShift.day==Shift.day)") 