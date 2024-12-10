import sqlite3
import hashlib
from datetime import datetime
import re
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt

console = Console()
connexion = sqlite3.connect('cabinet_medical.db')
cursor = connexion.cursor()

user_type = None
user_id = None


def validate_email(email):
    # robust email validation
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def login():
    # Email validation with re.match
    user_mail = Prompt.ask("Enter your [red]mail address[/red]")
    """while True:
        user_mail = Prompt.ask("Enter your [red]mail address[/red]")
        if validate_email(user_mail):
            break
        console.print("[red]Invalid email format[/red]")"""

    user_password = Prompt.ask("Enter your [red]password[/red]", password=True)
    hashed_password = hashlib.sha256(user_password.encode()).hexdigest()

    if user_type not in ['patients', 'doctors']:
        raise ValueError("Invalid user type")

    id_column = 'id_patient' if user_type == 'patients' else 'id_doctor'
    cursor.execute(f'''SELECT {id_column} FROM {user_type} WHERE password = ? AND email = ?''',
                   (hashed_password, user_mail))
    result = cursor.fetchone()
    return result

def register():
    last_name = Prompt.ask("Enter your [red]lastname[/red]")
    first_name = Prompt.ask("Enter your [red]firstname[/red]")
    phone_number = Prompt.ask("Enter your [red]phone number[/red]")
    email = Prompt.ask("Enter your [red]email[/red]")
    password = hashlib.sha256(Prompt.ask("Enter your [red]password[/red]").encode()).hexdigest()
    if user_type == 'patients':
        birth_date = Prompt.ask("Enter your [red]birth date[/red]")
        try:
            cursor.execute('''INSERT INTO patients (last_name, first_name, birth_date, email, phone_number, password) VALUES (?, ?, ?, ?, ?, ?)''',
                           (last_name, first_name, birth_date, email, phone_number, password))
            connexion.commit()
            print(f"Patient added to the databasse")
            return cursor.lastrowid

        except sqlite3.IntegrityError:
            console.print(f"[red]Error: A {user_type[:-1]} with this email already exists.[/red]")
            return None
        except sqlite3.Error as e:
            console.print(f"[red]Database error: {e}[/red]")
            connexion.rollback()
            return None
    else:
        speciality = Prompt.ask("Enter your [red]speciality[/red]")
        try:
            cursor.execute('''INSERT INTO doctors (last_name, first_name, speciality, email, phone_number, password) VALUES (?, ?, ?, ?, ?, ?)''',
                           (last_name, first_name, speciality, email, phone_number, password))
            connexion.commit()
            console.print(f"[pale_turquoise1]Doctor[/pale_turquoise1] added to the databasse")
            return cursor.lastrowid

        except sqlite3.IntegrityError:
            exit("Error: A doctor with this email already exists.")


def create_appointment():
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

    current_id = 'id_patient' if user_type == 'patients' else 'id_doctor'
    cursor.execute(f'''SELECT * FROM {user_type} WHERE {current_id}=?''', (user_id,))
    user_data = cursor.fetchone()

    action = int(Prompt.ask(f"Welcome [blue]{user_data[2]}[/blue], please select an option: "
                       "\n1: Consult your data"
                       "\n2: Create an appointment"
                       "\n3: View your appointments"
                       "\n4: Exit"
                       "\n> "))
    if action == 1:
        #spliting user data without the user id and he's password hashed
        last_name, first_name, date_of_birth, phone_number, email = user_data[1:-1]
        print(f"Data : {last_name}, {first_name}, {date_of_birth}, {phone_number}, {email}")

    elif action == 2:
        if current_id == 'id_doctor':
            print('You can not create an appointment as a doctor account, please connect on your patient account')
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

    # Clear and attractive initial screen
    console.print(Panel.fit(
        "[bold blue]Medical Cabinet Application[/bold blue]\n\n"
        "[cyan]Select User Type:[/cyan]\n"
        "1. [yellow]Patient[/yellow]\n"
        "2. [green]Doctor[/green]\n\n"
        "[cyan]Select Action:[/cyan]\n"
        "1. [pale_turquoise1]Login[/pale_turquoise1]\n"
        "2. [magenta]Register[/magenta]",
        title="Welcome",
        border_style="bold blue"
    ))

    # User Type Selection
    who = Prompt.ask("Select user type",
                     choices=['1', '2'],
                     show_default=False)

    user_type = "patients" if who == '1' else "doctors"

    # Action Selection
    action = Prompt.ask("Select action",
                        choices=['1', '2'],
                        show_default=False)

    if action == '1':
        user_id = login()
        if user_id is not None:
            user_id = str(user_id[0])
            patient_space()
        else:
            console.print("[red]Login failed[/red]")
    else:
        register_result = register()
        if register_result:
            console.print("[green]Registration successful[/green]")

start()
connexion.close()