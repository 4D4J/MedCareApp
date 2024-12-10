import sqlite3

# Connexion à la base de données
conn = sqlite3.connect('cabinet_medical.db')
cursor = conn.cursor()

# Création de la table des patients
cursor.execute('''
CREATE TABLE IF NOT EXISTS patients (
    id_patient INTEGER PRIMARY KEY AUTOINCREMENT,
    last_name TEXT NOT NULL,
    first_name TEXT NOT NULL,
    birth_date TEXT,
    phone_number TEXT,
    email TEXT,
    password TEXT
)
''')

# Création de la table des médecins
cursor.execute('''
CREATE TABLE IF NOT EXISTS doctors (
    id_doctor INTEGER PRIMARY KEY AUTOINCREMENT,
    last_name TEXT NOT NULL,
    first_name TEXT NOT NULL,
    speciality TEXT,
    phone_number TEXT,
    email TEXT,
    password TEXT
)
''')

# Création de la table des réservations
cursor.execute('''
CREATE TABLE IF NOT EXISTS appointment (
    id_appointment INTEGER PRIMARY KEY AUTOINCREMENT,
    id_patient INTEGER,
    id_doctor INTEGER,
    appointment_date TEXT NOT NULL,
    appointment_hour TEXT NOT NULL,
    duration INTEGER NOT NULL,
    FOREIGN KEY(id_patient) REFERENCES patients(id_patient),
    FOREIGN KEY(id_doctor) REFERENCES medecins(id_doctor)
)
''')


# Validation des changements dans la base de données
conn.commit()

# Récupération et affichage des réservations avec les détails des patients et médecins
cursor.execute('''
SELECT 
    r.id_appointment, 
    p.last_name || ' ' || p.first_name AS patient, 
    m.last_name || ' ' || m.first_name AS medecin,
    r.appointment_date, 
    r.appointment_hour, 
    r.duration
FROM 
    appointment r
JOIN 
    patients p ON r.id_patient = p.id_patient
JOIN 
    medecins m ON r.id_doctor = m.id_doctor
''')
appointment = cursor.fetchall()

print("Liste des réservations :")
for reservation in appointment:
    print(f"ID: {reservation[0]}, Patient: {reservation[1]}, Médecin: {reservation[2]}, Date: {reservation[3]}, Heure: {reservation[4]}, Durée: {reservation[5]} minutes")




# Fermeture de la connexion
conn.close()