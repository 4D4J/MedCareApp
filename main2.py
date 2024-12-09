import sqlite3
import hashlib
from datetime import datetime, timedelta
import random
import os


connexion = sqlite3.connect('cabinet_medical.db')
cursor = connexion.cursor()

user_type = None
user_id = None


def check_string(string, characters):
    for character in characters:
        if character not in string:
            return True
    return False

def login():
    os.system('cls')
    user_mail = input("Enter your mail address: ")
    while check_string(user_mail, ["@", "."]):
        user_mail = input("Invalid format, enter your mail address: ")

    user_password = input("Enter your password: ")
    hashed_password = hashlib.sha256(user_password.encode()).hexdigest()

    id = 'id_patient' if user_type == 'patients' else 'id_doctor'
    #print(f'''SELECT {id} FROM {user_type} WHERE password =  AND email = ?''')
    cursor.execute(f'''SELECT {id} FROM {user_type} WHERE password = ? AND email = ?''', (hashed_password, user_mail))
    result = cursor.fetchone()
    return result


def register():
    os.system('cls')
    last_name = input("Enter your lastname: ")
    first_name = input("Enter your firstname: ")
    phone_number = input("Enter your phone number: ")
    email = input("Enter your email: ")
    password = hashlib.sha256(input("Enter your password: ").encode()).hexdigest()
    if user_type == 'patients':
        birth_date = input("Enter your birth date: ")
        try:
            cursor.execute('''INSERT INTO patients (last_name, first_name, birth_date, email, phone_number, password) VALUES (?, ?, ?, ?, ?, ?)''',
                           (last_name, first_name, birth_date, email, phone_number, password))
            connexion.commit()
            print(f"Patient added to the databasse")
            return cursor.lastrowid

        except sqlite3.IntegrityError:
            exit("Error: A doctor with this email already exists.")
    else:
        speciality = input("Enter your speciality: ")
        try:
            cursor.execute('''INSERT INTO doctors (last_name, first_name, speciality, email, phone_number, password) VALUES (?, ?, ?, ?, ?, ?)''',
                           (last_name, first_name, speciality, email, phone_number, password))
            connexion.commit()
            print(f"Doctor added to the databasse")
            return cursor.lastrowid

        except sqlite3.IntegrityError:
            exit("Error: A doctor with this email already exists.")


def create_appointment():
    os.system('cls')
    if user_type != 'patients':
        print("Only patients can create appointments.")
        return

    # Validate doctor's email
    email_doctor = input("Enter doctor's email (example: 'jean.dupont@medecin.com'): ")
    cursor.execute('SELECT id_doctor FROM doctors WHERE email = ?', (email_doctor,))
    result_doctor = cursor.fetchone()

    if result_doctor is None:
        print("No doctor matches this email.")
        return

    id_doctor = result_doctor[0]

    while True:
        try:
            # appointment date
            appointment_date_str = input("Enter appointment date (YYYY-MM-DD): ")
            appointment_date = datetime.strptime(appointment_date_str, '%Y-%m-%d').date()

            if appointment_date <= datetime.now().date():
                print("Please choose a future date.")
                continue

            # appointment time
            appointment_hour = input("Enter appointment time (HH:MM, exemple: 14:30): ")
            datetime.strptime(appointment_hour, '%H:%M')

            # # appointment duration
            duration = int(input("Enter appointment duration in minutes (15/30/45/60): "))
            if duration not in [15, 30, 45, 60]:
                print("Duration must be 15, 30, 45, or 60 minutes.")
                continue

            # Insert appointment
            cursor.execute('''
            INSERT INTO appointment (id_patient, id_doctor, appointment_date, appointment_hour, duration)
            VALUES (?, ?, ?, ?, ?)
            ''', (user_id, id_doctor, appointment_date_str, appointment_hour, duration))
            connexion.commit()

            print(f"Appointment successfully created:\n"
                  f"Date: {appointment_date_str}, Time: {appointment_hour}, Duration: {duration} minutes.")
            break

        except ValueError as e:
            print(f"Invalid input: {e}. Please try again.")
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            connexion.rollback()
            break


def consult_appointment():
    os.system('cls')
    id_column = "id_patient" if user_type == 'patients' else "id_doctor"

    # Fetch all appointments for the user
    cursor.execute(f'''
        SELECT a.*, d.first_name, d.last_name 
        FROM appointment a 
        JOIN doctors d ON a.id_doctor = d.id_doctor 
        WHERE a.{id_column} = ?
    ''', (user_id,))

    appointments = cursor.fetchall()

    if not appointments:
        print("No appointments found.")
        return

    print("Your Appointments:")
    for appointment in appointments:
        doctor_name = f"{appointment[-2]} {appointment[-1]}"
        if user_type == 'patients':
            print(
                f"Doctor: {doctor_name}, Date: {appointment[3]}, Time: {appointment[4]}, Duration: {appointment[5]} minutes")
        else:  # for doctors
            cursor.execute('SELECT first_name, last_name FROM patients WHERE id_patient = ?', (appointment[1],))
            patient = cursor.fetchone()
            patient_name = f"{patient[0]} {patient[1]}"
            print(
                f"Patient: {patient_name}, Date: {appointment[3]}, Time: {appointment[4]}, Duration: {appointment[5]} minutes")


def patient_space():
    os.system('cls')
    current_id = 'id_patient' if user_type == 'patients' else 'id_doctor'
    cursor.execute(f'''SELECT * FROM {user_type} WHERE {current_id}=?''', user_id[0])
    user_data = cursor.fetchone()

    action = int(input(f"Welcome {user_data[2]}, please select an option: "
                       "\n1: Consult your data"
                       "\n2: Create an appointment"
                       "\n3: View your appointments"
                       "\n4: Exit"
                       "\n> "))
    if action == 1:
        #spliting user data without the user id and he's password hashed
        last_name, first_name, date_of_birth, phone_number, email = user_data[1:-1]
        print(f"Data : ")

    elif action == 2:
        if current_id == 'id_doctor':
            print("As a doctor you can't create an appointment")
        else:
            create_appointment()
    elif action == 3:
        consult_appointment()
    elif action == 4:
        exit('Space left')
    else:
        exit('Invalid option')
    # return to the space
    patient_space()



def start():

    global user_id, user_type
    os.system('cls')
    who = int(input("Select an option: "
                      "\n1: Patient"
                      "\n2: Doctor"
                      "\n> "))
    if who not in (1, 2):
        exit("Not a valid option")
    action = int(input("Select an option: "
                          "\n1: Login"
                          "\n2: Register"
                          "\n> "))
    if action not in (1, 2):
        exit("Not a valid option")

    user_type = "patients" if who == 1 else "doctors"

    if action == 1:
        user_id = login()
        if user_id is not None:
            user_id = str(user_id[0])
            print(user_id)
            patient_space()
        else:
            exit("Login failed")
    if action == 2:
        register()
        exit('Registration successful')

start()
connexion.close()