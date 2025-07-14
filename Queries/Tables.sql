-- =============================================
-- EMPLOYEE-RELATED TABLES
-- =============================================

CREATE TABLE Employee (
    EmpID INT PRIMARY KEY,
    First_Name VARCHAR(50) NOT NULL,
    Last_Name VARCHAR(50) NOT NULL,
    SSN CHAR(11) UNIQUE NOT NULL,
    Salary DECIMAL(10,2) CHECK (Salary BETWEEN 25000 AND 300000 OR Salary IS NULL),
    Gender CHAR(1) CHECK (Gender IN ('M', 'F')),
    EmployeeType VARCHAR(20) NOT NULL CHECK (EmployeeType IN ('Physician', 'Nurse', 'Surgeon', 'Support')),
    Phone VARCHAR(15) NOT NULL,
    Street VARCHAR(100) NOT NULL,
    City VARCHAR(50) NOT NULL,
    State CHAR(2) NOT NULL,
    Zip VARCHAR(10) NOT NULL
);

CREATE TABLE Physician (
    PhysicianID INT PRIMARY KEY,
    Specialty VARCHAR(50) NOT NULL,
    Type VARCHAR(50) NOT NULL,
    FOREIGN KEY (PhysicianID) REFERENCES Employee(EmpID) ON DELETE CASCADE
);

CREATE TABLE Nurse (
    NurseID INT PRIMARY KEY,
    Grade VARCHAR(20) NOT NULL,
    Years INT NOT NULL,
    FOREIGN KEY (NurseID) REFERENCES Employee(EmpID) ON DELETE CASCADE
);

CREATE TABLE Surgeon (
    SurgeonID INT PRIMARY KEY,
    Specialty VARCHAR(50) NOT NULL,
    ContractType VARCHAR(50) NOT NULL,
    ContractDuration INT NOT NULL,
    ContractAmount DECIMAL(10,2),
    FOREIGN KEY (SurgeonID) REFERENCES Employee(EmpID) ON DELETE CASCADE
);

-- =============================================
-- CLINIC-RELATED TABLES
-- =============================================

CREATE TABLE Clinic (
    Name VARCHAR(100) PRIMARY KEY,
    Street VARCHAR(100) NOT NULL,
    City VARCHAR(50) NOT NULL,
    State CHAR(2) NOT NULL,
    Zip VARCHAR(10) NOT NULL,
    OwnerID INT,
    FOREIGN KEY (OwnerID) REFERENCES Physician(PhysicianID) ON DELETE SET NULL
);

CREATE TABLE Corporation (
    Name VARCHAR(100) PRIMARY KEY,
    PercentOwn DECIMAL(5,2) NOT NULL CHECK (PercentOwn BETWEEN 0 AND 100),
    HeadquartersStreet VARCHAR(100) NOT NULL,
    HeadquartersCity VARCHAR(50) NOT NULL,
    HeadquartersState CHAR(2) NOT NULL,
    HeadquartersZip VARCHAR(10) NOT NULL
);

CREATE TABLE Clinic_Bed (
    BedID INT PRIMARY KEY,
    Clinic VARCHAR(100) NOT NULL,
    RoomNum INT NOT NULL,
    BedLetter CHAR(1) NOT NULL CHECK (BedLetter IN ('A', 'B')),
    Unit INT NOT NULL CHECK (Unit BETWEEN 1 AND 7),
    Wing VARCHAR(5) NOT NULL CHECK (Wing IN ('Blue', 'Green')),
    FOREIGN KEY (Clinic) REFERENCES Clinic(Name) ON DELETE CASCADE,
    CONSTRAINT UQ_Bed UNIQUE (Clinic, RoomNum, BedLetter)
);

-- =============================================
-- PATIENT-RELATED TABLES
-- =============================================

CREATE TABLE Patient (
    PID INT PRIMARY KEY,
    PrimaryPhysician INT NOT NULL,
    D_O_B DATE NOT NULL,
    SSN CHAR(11) UNIQUE NOT NULL,
    PFirstName VARCHAR(50) NOT NULL,
    PLastName VARCHAR(50) NOT NULL,
    Gender CHAR(1) CHECK (Gender IN ('M', 'F')),
    BloodType VARCHAR(3) NOT NULL CHECK (BloodType IN ('A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-')),
    PStreet VARCHAR(100) NOT NULL,
    PCity VARCHAR(50) NOT NULL,
    PState CHAR(2) NOT NULL,
    PZip VARCHAR(10) NOT NULL,
    FOREIGN KEY (PrimaryPhysician) REFERENCES Physician(PhysicianID) ON DELETE SET NULL
);

CREATE TABLE Medical_Data (
    PID INT PRIMARY KEY,
    BloodSugar DECIMAL(5,1),
    Cholesterol DECIMAL(5,1),
    Triglycerides DECIMAL(5,1),
    HDL DECIMAL(5,1),
    LDL DECIMAL(5,1),
    LastUpdate DATE NOT NULL,
    Heart_Risk CHAR(1) CHECK (Heart_Risk IN ('N', 'L', 'M', 'H')),
    FOREIGN KEY (PID) REFERENCES Patient(PID) ON DELETE CASCADE
);

CREATE TABLE AdmittedTo (
    PID INT,
    BedID INT,
    Date_IN DATE NOT NULL,
    Date_OUT DATE,
    PRIMARY KEY (PID, BedID),
    FOREIGN KEY (PID) REFERENCES Patient(PID) ON DELETE CASCADE,
    FOREIGN KEY (BedID) REFERENCES Clinic_Bed(BedID) ON DELETE CASCADE,
    CHECK (Date_OUT IS NULL OR Date_OUT >= Date_IN)
);

CREATE TABLE AttendsTo (
    NurseID INT,
    PID INT,
    StartDate DATE NOT NULL,
    EndDate DATE,
    PRIMARY KEY (NurseID, PID),
    FOREIGN KEY (NurseID) REFERENCES Nurse(NurseID) ON DELETE CASCADE,
    FOREIGN KEY (PID) REFERENCES Patient(PID) ON DELETE CASCADE,
    CHECK (EndDate IS NULL OR EndDate >= StartDate)
);

-- =============================================
-- ILLNESS AND ALLERGY TABLES
-- =============================================

CREATE TABLE Illness (
    IllnessCode INT PRIMARY KEY,
    Description VARCHAR(255) NOT NULL
);

CREATE TABLE Allergy (
    AllergyCode INT PRIMARY KEY,
    Description VARCHAR(255) NOT NULL
);

CREATE TABLE Diagnosis (
    PID INT,
    PhysicianID INT,
    IllnessCode INT,
    Date DATE NOT NULL,
    Notes TEXT,
    Comment TEXT,
    PRIMARY KEY (PID, PhysicianID, IllnessCode),
    FOREIGN KEY (PID) REFERENCES Patient(PID) ON DELETE CASCADE,
    FOREIGN KEY (PhysicianID) REFERENCES Physician(PhysicianID) ON DELETE CASCADE,
    FOREIGN KEY (IllnessCode) REFERENCES Illness(IllnessCode) ON DELETE CASCADE
);

CREATE TABLE Patient_Allergy (
    PID INT,
    AllergyCode INT,
    PRIMARY KEY (PID, AllergyCode),
    FOREIGN KEY (PID) REFERENCES Patient(PID) ON DELETE CASCADE,
    FOREIGN KEY (AllergyCode) REFERENCES Allergy(AllergyCode) ON DELETE CASCADE
);

-- =============================================
-- CONSULTATION AND PRESCRIPTION TABLES
-- =============================================

CREATE TABLE Consultation (
    PID INT,
    PhysicianID INT,
    Date DATE,
    Type VARCHAR(50) NOT NULL,
	Notes VARCHAR(250),
    PRIMARY KEY (PID, PhysicianID, Date),
    FOREIGN KEY (PID) REFERENCES Patient(PID) ON DELETE CASCADE,
    FOREIGN KEY (PhysicianID) REFERENCES Physician(PhysicianID) ON DELETE CASCADE
);

CREATE TABLE Medicine (
    Code INT PRIMARY KEY,
    MadeBy VARCHAR(100),
    Name VARCHAR(100) NOT NULL,
    Usage VARCHAR(255),
    UnitCost DECIMAL(10,2) NOT NULL,
    Quantity INT NOT NULL,
    QtyOrdered INT NOT NULL,
    FOREIGN KEY (MadeBy) REFERENCES Corporation(Name) ON DELETE SET NULL
);

CREATE TABLE ReactsWith (
    Medicine1 INT,
    Medicine2 INT,
    Severity CHAR(1) NOT NULL CHECK (Severity IN ('S', 'M', 'L', 'N')),
    PRIMARY KEY (Medicine1, Medicine2),
    FOREIGN KEY (Medicine1) REFERENCES Medicine(Code) ON DELETE CASCADE,
    FOREIGN KEY (Medicine2) REFERENCES Medicine(Code) ON DELETE CASCADE,
    CHECK (Medicine1 < Medicine2) -- Prevent duplicate entries
);

CREATE TABLE Prescription (
    PrescriptionID INT PRIMARY KEY,
    PID INT NOT NULL,
    MedicineCode INT NOT NULL,
    Prescriber INT NOT NULL,
    DatePrescrbed DATE NOT NULL,
    DateFilled DATE,
    Dosage VARCHAR(50) NOT NULL,
    Duration VARCHAR(50) NOT NULL,
    Frequency VARCHAR(50) NOT NULL,
	Quantity INT NOT NULL DEFAULT 0,
    FOREIGN KEY (PID) REFERENCES Patient(PID) ON DELETE CASCADE,
    FOREIGN KEY (MedicineCode) REFERENCES Medicine(Code) ON DELETE CASCADE,
    FOREIGN KEY (Prescriber) REFERENCES Physician(PhysicianID) ON DELETE CASCADE,
    UNIQUE (PID, MedicineCode), -- No two physicians can prescribe same medicine to same patient
	CONSTRAINT check_quantity_positive CHECK (Quantity >= 0)
);

-- =============================================
-- SURGERY-RELATED TABLES
-- =============================================

CREATE TABLE Surgery_Type (
    SurgeryCode INT PRIMARY KEY,
    Name VARCHAR(100) NOT NULL,
    Type CHAR(1) NOT NULL CHECK (Type IN ('H', 'O')), -- H for hospitalization, O for outpatient
    AnatomicLocation VARCHAR(100) NOT NULL,
    SpecialNeeds VARCHAR(255)
);

CREATE TABLE Surgery_Skill (
    SkillCode INT PRIMARY KEY,
    Description VARCHAR(255) NOT NULL
);

CREATE TABLE Surgery_Type_Skill (
    SurgeryCode INT,
    SkillCode INT,
    PRIMARY KEY (SurgeryCode, SkillCode),
    FOREIGN KEY (SurgeryCode) REFERENCES Surgery_Type(SurgeryCode) ON DELETE CASCADE,
    FOREIGN KEY (SkillCode) REFERENCES Surgery_Skill(SkillCode) ON DELETE CASCADE
);

CREATE TABLE Nurse_Skill (
    NurseID INT,
    SkillCode INT,
    PRIMARY KEY (NurseID, SkillCode),
    FOREIGN KEY (NurseID) REFERENCES Nurse(NurseID) ON DELETE CASCADE,
    FOREIGN KEY (SkillCode) REFERENCES Surgery_Skill(SkillCode) ON DELETE CASCADE
);

CREATE TABLE Nurse_Surgery_Type (
    NurseID INT,
    SurgeryCode INT,
    PRIMARY KEY (NurseID, SurgeryCode),
    FOREIGN KEY (NurseID) REFERENCES Nurse(NurseID) ON DELETE CASCADE,
    FOREIGN KEY (SurgeryCode) REFERENCES Surgery_Type(SurgeryCode) ON DELETE CASCADE
);

CREATE TABLE Surgery_Schedule (
    NurseID INT,
    SurgeryShift VARCHAR(20),
    Date DATE,
    PRIMARY KEY (NurseID, SurgeryShift, Date),
    FOREIGN KEY (NurseID) REFERENCES Nurse(NurseID) ON DELETE CASCADE
);

CREATE TABLE Surgery (
    PID INT,
    SurgeonID INT,
    SurgeryCode INT,
    Date DATE,
    Theater VARCHAR(50) NOT NULL,
    SurgeryShift VARCHAR(20),
    PRIMARY KEY (PID, SurgeonID, SurgeryCode, Date),
    FOREIGN KEY (PID) REFERENCES Patient(PID) ON DELETE CASCADE,
    FOREIGN KEY (SurgeonID) REFERENCES Surgeon(SurgeonID) ON DELETE RESTRICT, -- Cannot delete surgeon with surgery records
    FOREIGN KEY (SurgeryCode) REFERENCES Surgery_Type(SurgeryCode) ON DELETE CASCADE
);

-- =============================================
-- SHIFT MANAGEMENT
-- =============================================

CREATE TABLE Shift (
    EmpID INT,
    Day VARCHAR(10),
    BeginTime TIME NOT NULL,
    EndTime TIME NOT NULL,
    PRIMARY KEY (EmpID, Day),
    FOREIGN KEY (EmpID) REFERENCES Employee(EmpID) ON DELETE CASCADE,
    CHECK (EndTime > BeginTime)
);