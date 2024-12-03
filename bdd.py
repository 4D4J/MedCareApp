import sqlite3

# Connexion à la base de données
conn = sqlite3.connect('cabinet_medical.db')
cursor = conn.cursor()

# Création de la table des patients
cursor.execute('''
CREATE TABLE IF NOT EXISTS patients (
    id_patient INTEGER PRIMARY KEY AUTOINCREMENT,
    nom TEXT NOT NULL,
    prenom TEXT NOT NULL,
    date_naissance TEXT,
    telephone TEXT,
    email TEXT,
    password TEXT
)
''')

# Création de la table des médecins
cursor.execute('''
CREATE TABLE IF NOT EXISTS medecins (
    id_medecin INTEGER PRIMARY KEY AUTOINCREMENT,
    nom TEXT NOT NULL,
    prenom TEXT NOT NULL,
    specialite TEXT,
    telephone TEXT,
    email TEXT,
    password TEXT
)
''')

# Création de la table des réservations
cursor.execute('''
CREATE TABLE IF NOT EXISTS reservations (
    id_reservation INTEGER PRIMARY KEY AUTOINCREMENT,
    id_patient INTEGER,
    id_medecin INTEGER,
    date_reservation TEXT NOT NULL,
    heure_reservation TEXT NOT NULL,
    duree_minutes INTEGER NOT NULL,
    FOREIGN KEY(id_patient) REFERENCES patients(id_patient),
    FOREIGN KEY(id_medecin) REFERENCES medecins(id_medecin)
)
''')


# Validation des changements dans la base de données
conn.commit()

# Récupération et affichage des réservations avec les détails des patients et médecins
cursor.execute('''
SELECT 
    r.id_reservation, 
    p.nom || ' ' || p.prenom AS patient, 
    m.nom || ' ' || m.prenom AS medecin,
    r.date_reservation, 
    r.heure_reservation, 
    r.duree_minutes
FROM 
    reservations r
JOIN 
    patients p ON r.id_patient = p.id_patient
JOIN 
    medecins m ON r.id_medecin = m.id_medecin
''')
reservations = cursor.fetchall()

print("Liste des réservations :")
for reservation in reservations:
    print(f"ID: {reservation[0]}, Patient: {reservation[1]}, Médecin: {reservation[2]}, Date: {reservation[3]}, Heure: {reservation[4]}, Durée: {reservation[5]} minutes")

# Fermeture de la connexion
conn.close()