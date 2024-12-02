import sqlite3
import hashlib

#Quand on arrive sur la plateforme on se créé un compte patient, sauf si on est déja dans la liste des patients

def ajouter_patient(nom, prenom, date_naissance,telephone, email, password):
    connexion = sqlite3.connect('cabinet_medical.db')
    cursor = connexion.cursor()
    #Password hashing
    password = hashlib.sha256(password.encode()).hexdigest()
    """Ajoute un nouveau patient à la base de données"""
    try:
        cursor.execute('''INSERT INTO patients (nom, prenom, date_naissance, telephone, email, password)VALUES (?, ?, ?, ?, ?, ?)''', (nom, prenom, date_naissance, telephone, email, password))
        connexion.commit()
        print(f"Patient {prenom} {nom} ajouté avec succès.")
        return cursor.lastrowid
    except sqlite3.IntegrityError:
        print("Erreur : Un patient avec cet email existe déjà.")
        return None



#Si on est un docteur on peut voir la liste des patients inscrit sur la plateforme
def lister_patients():
    connexion = sqlite3.connect('cabinet_medical.db')
    cursor = connexion.cursor()
    """Liste tous les patients"""
    cursor.execute('SELECT * FROM patients')
    patients = cursor.fetchall()
    print("\nListe des patients :")
    for patient in patients:
        print(f"ID: {patient[0]}, Nom: {patient[1]} {patient[2]}, Tél: {patient[4]}, Email: {patient[5]}, Password: {patient[6]}")
    connexion.close()