import os
from models import db, Corporation, Clinic, Employee, Physician, Nurse, Surgeon, Shift, Patient, Medical_Data, Allergy, Illness, Patient_Allergy, Diagnosis, Consultation, Medicine, Prescription, Surgery_Type, Surgery_Skill, Surgery_Type_Skill, Nurse_Skill, Nurse_Surgery_Type, Surgery_Schedule, Clinic_Bed, AdmittedTo, AttendsTo, WorksShift
from flask import Flask
from sqlalchemy.exc import IntegrityError

def main():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://postgres:Admin@localhost:5432/postgres'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    with app.app_context():
        # Optionally clear tables (uncomment if you want to reset data)
        # db.session.query(...).delete()  # In FK order
        # db.session.commit()

        # Corporations
        corp1 = Corporation(name='HealthCorp', percentown=60.0, headquartersstreet='100 Main St', headquarterscity='Metropolis', headquartersstate='NY', headquarterszip='10001')
        corp2 = Corporation(name='MediGroup', percentown=40.0, headquartersstreet='200 Elm St', headquarterscity='Gotham', headquartersstate='NJ', headquarterszip='07001')
        db.session.add_all([corp1, corp2])

        # Clinics
        clinic1 = Clinic(name='Central Clinic', street='123 Clinic Ave', city='Metropolis', state='NY', zip='10001', ownerid=None)
        clinic2 = Clinic(name='Westside Clinic', street='456 West St', city='Gotham', state='NJ', zip='07001', ownerid=None)
        db.session.add_all([clinic1, clinic2])

        # Employees (Physician, Nurse, Surgeon, Support)
        emp1 = Employee(empid=1, first_name='Alice', last_name='Smith', ssn='111-11-1111', salary=120000, gender='F', employeetype='Physician', phone='555-1001', street='1 Doctor Rd', city='Metropolis', state='NY', zip='10001')
        emp2 = Employee(empid=2, first_name='Bob', last_name='Jones', ssn='222-22-2222', salary=90000, gender='M', employeetype='Nurse', phone='555-1002', street='2 Nurse Ln', city='Metropolis', state='NY', zip='10001')
        emp3 = Employee(empid=3, first_name='Carol', last_name='Lee', ssn='333-33-3333', salary=150000, gender='F', employeetype='Surgeon', phone='555-1003', street='3 Surgery Blvd', city='Gotham', state='NJ', zip='07001')
        emp4 = Employee(empid=4, first_name='Dan', last_name='Brown', ssn='444-44-4444', salary=50000, gender='M', employeetype='Support', phone='555-1004', street='4 Support Ct', city='Gotham', state='NJ', zip='07001')
        db.session.add_all([emp1, emp2, emp3, emp4])

        # Physician, Nurse, Surgeon
        db.session.add(Physician(physicianid=1, specialty='Cardiology', type='Attending'))
        db.session.add(Nurse(nurseid=2, grade='RN', years=5))
        db.session.add(Surgeon(surgeonid=3, specialty='Orthopedics', contracttype='Full-Time', contractduration=24, contractamount=200000))

        # Shifts
        db.session.add(Shift(empid=1, day='Monday', begintime='08:00:00', endtime='16:00:00'))
        db.session.add(Shift(empid=2, day='Monday', begintime='08:00:00', endtime='16:00:00'))
        db.session.add(Shift(empid=3, day='Tuesday', begintime='10:00:00', endtime='18:00:00'))
        db.session.add(Shift(empid=4, day='Wednesday', begintime='09:00:00', endtime='17:00:00'))

        # Patients
        pat1 = Patient(pid=1, primaryphysician=1, d_o_b='1980-01-01', ssn='555-55-5555', pfirstname='Eve', plastname='White', gender='F', bloodtype='A+', pstreet='10 Patient Rd', pcity='Metropolis', pstate='NY', pzip='10001')
        pat2 = Patient(pid=2, primaryphysician=1, d_o_b='1975-05-05', ssn='666-66-6666', pfirstname='Frank', plastname='Green', gender='M', bloodtype='O-', pstreet='20 Patient Rd', pcity='Gotham', pstate='NJ', pzip='07001')
        db.session.add_all([pat1, pat2])

        # Medical Data
        db.session.add(Medical_Data(pid=1, bloodsugar=90.0, cholesterol=180.0, triglycerides=120.0, hdl=50.0, ldl=100.0, lastupdate='2024-05-01', heart_risk='L'))
        db.session.add(Medical_Data(pid=2, bloodsugar=110.0, cholesterol=200.0, triglycerides=150.0, hdl=45.0, ldl=120.0, lastupdate='2024-05-02', heart_risk='M'))

        # Allergies & Illnesses
        allergy1 = Allergy(allergycode=1, description='Penicillin')
        allergy2 = Allergy(allergycode=2, description='Peanuts')
        illness1 = Illness(illnesscode=1, description='Hypertension')
        illness2 = Illness(illnesscode=2, description='Diabetes')
        db.session.add_all([allergy1, allergy2, illness1, illness2])

        # Patient_Allergy & Diagnosis
        db.session.add(Patient_Allergy(pid=1, allergycode=1))
        db.session.add(Patient_Allergy(pid=2, allergycode=2))
        db.session.add(Diagnosis(pid=1, physicianid=1, illnesscode=1, date='2024-05-01', notes='Stable', comment='Monitor'))
        db.session.add(Diagnosis(pid=2, physicianid=1, illnesscode=2, date='2024-05-02', notes='Needs insulin', comment='Urgent'))

        # Consultations
        db.session.add(Consultation(pid=1, physicianid=1, date='2024-05-03', type='Routine'))
        db.session.add(Consultation(pid=2, physicianid=1, date='2024-05-04', type='Follow-up'))

        # Medicines
        med1 = Medicine(code=1, madeby='HealthCorp', name='Aspirin', usage='Pain relief', unitcost=0.10, quantity=1000, qtyordered=100)
        med2 = Medicine(code=2, madeby='MediGroup', name='Metformin', usage='Diabetes', unitcost=0.20, quantity=500, qtyordered=50)
        db.session.add_all([med1, med2])

        # Prescriptions
        db.session.add(Prescription(prescriptionid=1, pid=1, medicinecode=1, prescriber=1, dateprescrbed='2024-05-05', dosage='100mg', duration='7 days', frequency='Once daily', quantity=30))
        db.session.add(Prescription(prescriptionid=2, pid=2, medicinecode=2, prescriber=1, dateprescrbed='2024-05-06', dosage='500mg', duration='14 days', frequency='Twice daily', quantity=60))

        # Surgery Types, Skills, and Assignments
        stype1 = Surgery_Type(surgerycode=1, name='Knee Replacement', type='H', anatomiclocation='Knee', specialneeds='Physical therapy')
        stype2 = Surgery_Type(surgerycode=2, name='Appendectomy', type='O', anatomiclocation='Abdomen', specialneeds='None')
        skill1 = Surgery_Skill(skillcode=1, description='Orthopedic')
        skill2 = Surgery_Skill(skillcode=2, description='General Surgery')
        db.session.add_all([stype1, stype2, skill1, skill2])
        db.session.add(Surgery_Type_Skill(surgerycode=1, skillcode=1))
        db.session.add(Surgery_Type_Skill(surgerycode=2, skillcode=2))
        db.session.add(Nurse_Skill(nurseid=2, skillcode=1))
        db.session.add(Nurse_Surgery_Type(nurseid=2, surgerycode=1))
        db.session.add(Surgery_Schedule(nurseid=2, surgeryshift='Morning', date='2024-05-10'))

        # Clinic Beds, Admissions, AttendsTo
        bed1 = Clinic_Bed(bedid=1, clinic='Central Clinic', roomnum=101, bedletter='A', unit=1, wing='Blue')
        bed2 = Clinic_Bed(bedid=2, clinic='Central Clinic', roomnum=101, bedletter='B', unit=1, wing='Blue')
        db.session.add_all([bed1, bed2])
        db.session.add(AdmittedTo(pid=1, bedid=1, date_in='2024-05-01', date_out=None))
        db.session.add(AttendsTo(nurseid=2, pid=1, startdate='2024-05-01', enddate=None))

        # Seed WorksShift assignments: assign each employee to their own shift
        db.session.add(WorksShift(empid=1, day='Monday', employee_ssn='111-11-1111'))
        db.session.add(WorksShift(empid=2, day='Monday', employee_ssn='222-22-2222'))
        db.session.add(WorksShift(empid=3, day='Tuesday', employee_ssn='333-33-3333'))
        db.session.add(WorksShift(empid=4, day='Wednesday', employee_ssn='444-44-4444'))

        try:
            db.session.commit()
            print('Sample data inserted successfully.')
        except IntegrityError as e:
            db.session.rollback()
            print('IntegrityError:', e)
        except Exception as e:
            db.session.rollback()
            print('Error:', e)

if __name__ == '__main__':
    print('This script does not run automatically. To insert data, call main() from an interactive shell or another script.') 