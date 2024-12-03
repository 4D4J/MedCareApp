import sqlite3

#Si on est un docteur alors on peut s'inscrire sauf si on est déja inscrit dans l'application
def ajouter_medecin(nom, prenom, password, specialite, telephone, email):
    connexion = sqlite3.connect('cabinet_medical333.db')
    cursor = connexion.cursor()

    """Ajoute un nouveau médecin à la base de données"""
    try:
        cursor.execute('''INSERT INTO medecins (nom, prenom, specialite, telephone, email, password) VALUES (?, ?, ?, ?, ?, ?)''', (nom, prenom, specialite, telephone, email, password))
        connexion.commit()
        print(f"Médecin {prenom} {nom} ajouté avec succès.")
        return cursor.lastrowid
    except sqlite3.IntegrityError:
        print("Erreur : Un médecin avec cet email existe déjà.")
        return None


#Si on est un patient on peut voir les medecins inscrit sur le site
def lister_medecins():
    connexion = sqlite3.connect('cabinet_medical333.db')
    cursor = connexion.cursor()

    """Liste tous les médecins"""
    cursor.execute('SELECT * FROM medecins')
    medecins = cursor.fetchall()
    print("\nListe des médecins :")
    for medecin in medecins:
        print(f"ID: {medecin[0]}, Nom: {medecin[1]} {medecin[2]}, Spécialité: {medecin[3]}, Tél: {medecin[4]} Password : {medecin[5]}")

    connexion.close()

ajouter_medecin("Martin", "Claire", "securepass456", "Dentiste", "0605060708", "claire.martin@mail.com")