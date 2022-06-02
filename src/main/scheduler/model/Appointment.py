import sys
sys.path.append("../db/*")
from db.ConnectionManager import ConnectionManager
import pymssql
from hashlib import sha1

def collate_row(row):
    caregiver = row['Caregiver']
    patient = row['Patient']
    date = row['Time']
    vaccine = row['Vaccine']
    a = Appointment(patient, vaccine, date, caregiver)
    return (a.get_appointment_id(), vaccine, date, caregiver, patient)

def get_appointments_for_caregiver(caregiver):
    cm = ConnectionManager()
    conn = cm.create_connection()
    cursor = conn.cursor(as_dict=True)
    
    get_appointment_details = "SELECT Caregiver, Patient, Vaccine, Time FROM Appointments WHERE Caregiver = %s"
    try:
        cursor.execute(get_appointment_details, caregiver.username)
        results = []
        for row in cursor:
            print(row)
            results.append(collate_row(row))
        cm.close_connection()
        return results
    except pymssql.Error as e:
        raise e
    finally:
        cm.close_connection()
    return None
 
def get_appointments_for_patient(patient):
    cm = ConnectionManager()
    conn = cm.create_connection()
    cursor = conn.cursor(as_dict=True)
    
    get_appointment_details = "SELECT Caregiver, Patient, Vaccine, Time FROM Appointments WHERE Patient = %s"
    try:
        cursor.execute(get_appointment_details, patient.username)
        results = []
        for row in cursor:
            results.append(collate_row(row))
        cm.close_connection()
        return results
    except pymssql.Error as e:
        raise e
    finally:
        cm.close_connection()
    return None
 
def book_appointment(caregiver, patient, vaccine, date):
    a = Appointment(patient, vaccine, date, caregiver)
    a.save_to_db()
    return a.get_appointment_id()

class Appointment:
    def __init__(self, patient, vaccine, date, caregiver):
        self.patient = patient
        self.vaccine = vaccine
        self.date = date
        self.caregiver = caregiver

       
    def get_appointment_id(self):
        def short_hash(obj):
            obj = str(obj)
            obj = obj.encode('utf-8')
            return sha1(obj).hexdigest()[:4]

        return short_hash(self.patient) + short_hash(self.vaccine) + short_hash(self.date) + short_hash(self.caregiver)

    def save_to_db(self):
     #   if self.available_doses is None or self.available_doses <= 0:
     #       raise ValueError("Argument cannot be negative!")
        cm = ConnectionManager()
        conn = cm.create_connection()
        cursor = conn.cursor()

        upload_appointment = "INSERT INTO Appointments VALUES (%s, %s, %s, %s)"
        try:
            cursor.execute(upload_appointment, (self.caregiver, self.patient, self.vaccine, self.date))
            # you must call commit() to persist your data if you don't set autocommit to True
            conn.commit()
        except pymssql.IntegrityError:
            print(f"Appointment already booked for {self.patient} on {self.date} with {self.caregiver} for vaccine {self.vaccine}")
            return
        except pymssql.Error:
            # print("Error occurred when insert Vaccines")
            raise
        finally:
            cm.close_connection()


