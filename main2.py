import sqlite3
import hashlib
from datetime import datetime, timedelta
import random

connexion = sqlite3.connect('cabinet_medical.db')
cursor = connexion.cursor()
user_id = None

def check_string(string, characters):
    for character in characters:
        if character in string:
            return False
    return True

def login(table):

    user_mail = input("Enter your mail address: ")
    while check_string(user_mail, ["@", "."]):
        user_mail = input("Invalid format, enter your mail address: ")

    user_password = input("Enter your password: ")
    hashed_password = hashlib.sha256(user_password.encode()).hexdigest()
    #hashed_password = user_password

    cursor.execute(f'''SELECT id_patient FROM {table} WHERE password = ? AND email = ?''', (hashed_password, user_mail))
    result = cursor.fetchone()
    return result


def register():
    pass

def create_appointment():

    try:
        full_name_pt = input("Enter your full name (e.g., 'Pierre Dupont'): ")
        first_name_pt, last_name_pt = full_name_pt.split()
        full_name_dc = input("Enter doctor's full name (e.g., 'Pierre Dupont'): ")
        first_name_dc, last_name_dc = full_name_dc.split()
    except ValueError:
        print("Erreur : veuillez entrer le prénom et le nom séparés par un espace.")
        return

    cursor.execute('''
    SELECT id_patient FROM patients WHERE first_name = ? AND last_name = ?
    ''', (first_name_pt, last_name_pt))
    result_patient = cursor.fetchone()

    if result_patient is None:
        print(f"Aucun patient trouvé pour {first_name_pt} {last_name_pt}.")
        return

    id_patient = result_patient[0]
    print(f"ID du patient trouvé : {id_patient}")

    cursor.execute('''
    SELECT id_doctor FROM doctors WHERE first_name = ? AND last_name = ?
    ''', (first_name_dc, last_name_dc))

    result_doctor = cursor.fetchone()
    if result_doctor is None:
        print("Aucun médecin à ce nom.")
        return

    id_doctor = result_doctor[0]
    print(f"ID du médecin sélectionné : {id_doctor}")


    today = datetime.now()
    appointment_date = today + timedelta(days=random.randint(1, 30))
    appointment_hour = f"{random.randint(8, 17):02}:{random.choice([0, 15, 30, 45]):02}"
    duration = random.choice([15, 30, 45, 60])
    formatted_date = appointment_date.strftime('%Y-%m-%d')

    try:
        cursor.execute('''
        INSERT INTO appointment (id_patient, id_doctor, appointment_date, appointment_hour, duration)
        VALUES (?, ?, ?, ?, ?)
        ''', (id_patient, id_doctor, formatted_date, appointment_hour, duration))
        print(f"Réservation créée avec succès :\n"
              f"Patient {first_name_pt} {last_name_pt}, Médecin {first_name_dc} {last_name_dc},\n"
              f"Date : {formatted_date}, Heure : {appointment_hour}, Durée : {duration} minutes.")
    except sqlite3.Error as e:
        print(f"Erreur lors de la création de la réservation : {e}")



def start():
    global user_id
    choix = int(input("Select an option: "
                          "\n1: Login"
                          "\n2: Register"
                          "\n> "))
    if choix not in (1, 2):
        exit("Not a valid option")

    if choix == 1:
        user_id = login("patients")[0]
        if user_id is not None:
            print(f"Login successful {user_id=} !")
            cursor.execute(f'''SELECT * FROM patients WHERE id_patient=?''',
                               (user_id))
            print(cursor.fetchone())

        else:
            print("Login failed")
    if choix == 2:
        register()

start()
connexion.close()