-- =============================================
-- TRIGGERS
-- =============================================

-- Trigger to ensure a nurse is not assigned to more than one surgery type
CREATE OR REPLACE FUNCTION check_nurse_surgery_type_limit()
RETURNS TRIGGER AS $$
BEGIN
    IF (SELECT COUNT(*) FROM Nurse_Surgery_Type WHERE NurseID = NEW.NurseID) > 0 THEN
        RAISE EXCEPTION 'A nurse cannot be assigned to more than one surgery type';
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER check_nurse_surgery_type_limit_trigger
BEFORE INSERT ON Nurse_Surgery_Type
FOR EACH ROW
EXECUTE FUNCTION check_nurse_surgery_type_limit();

-- Trigger to calculate heart risk category when medical data is updated
CREATE OR REPLACE FUNCTION calculate_heart_risk()
RETURNS TRIGGER AS $$
DECLARE
    total_cholesterol DECIMAL(5,1);
    ratio DECIMAL(5,2);
    risk_category CHAR(1);
BEGIN
    -- Calculate total cholesterol
    total_cholesterol := NEW.HDL + NEW.LDL + (NEW.Triglycerides / 5);
    
    -- Calculate ratio
    IF NEW.HDL > 0 THEN
        ratio := total_cholesterol / NEW.HDL;
    ELSE
        ratio := 0;
    END IF;
    
    -- Determine risk category
    IF ratio < 4 THEN
        risk_category := 'N'; -- None
    ELSIF ratio >= 4 AND ratio < 5 THEN
        risk_category := 'L'; -- Low
    ELSIF ratio >= 5 THEN
        risk_category := 'M'; -- Moderate
    ELSE
        risk_category := 'N'; -- Default
    END IF;
    
    -- Update the risk category
    NEW.Heart_Risk := risk_category;
    
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER calculate_heart_risk_trigger
BEFORE INSERT OR UPDATE ON Medical_Data
FOR EACH ROW
EXECUTE FUNCTION calculate_heart_risk();

-- Trigger to handle physician deletion
CREATE OR REPLACE FUNCTION handle_physician_deletion()
RETURNS TRIGGER AS $$
DECLARE
    chief_of_staff INT;
BEGIN
    -- Find the chief of staff
    SELECT PhysicianID INTO chief_of_staff
    FROM Physician
    WHERE Type = 'Chief of Staff'
    LIMIT 1;
    
    -- Reassign patients to chief of staff
    UPDATE Patient
    SET PrimaryPhysician = chief_of_staff
    WHERE PrimaryPhysician = OLD.PhysicianID;
    
    -- Remove prescriptions by this physician
    DELETE FROM Prescription
    WHERE Prescriber = OLD.PhysicianID;
    
    RETURN OLD;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER handle_physician_deletion_trigger
BEFORE DELETE ON Physician
FOR EACH ROW
EXECUTE FUNCTION handle_physician_deletion();

-- Trigger to handle nurse deletion
CREATE OR REPLACE FUNCTION handle_nurse_deletion()
RETURNS TRIGGER AS $$
BEGIN
    -- Temporarily remove associations with in-patients
    UPDATE AttendsTo
    SET End_Date = CURRENT_DATE
    WHERE NurseID = OLD.NurseID AND End_Date IS NULL;
    
    RETURN OLD;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER handle_nurse_deletion_trigger
BEFORE DELETE ON Nurse
FOR EACH ROW
EXECUTE FUNCTION handle_nurse_deletion();