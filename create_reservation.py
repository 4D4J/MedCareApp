from datetime import datetime
import sqlite3


#Si on est un patient on peut passer une reservation
def ajouter_reservation(id_patient, id_medecin, date_reservation, heure_reservation, duree_minutes):
    connexion = sqlite3.connect('cabinet_medical.db')
    cursor = connexion.cursor()

    """Ajoute une nouvelle réservation"""
    try:
        # Validation de la date et de l'heure
        datetime.strptime(date_reservation, '%Y-%m-%d')
        datetime.strptime(heure_reservation, '%H:%M')

        cursor.execute('''
        INSERT INTO reservations (id_patient, id_medecin, date_reservation, heure_reservation, duree_minutes)
        VALUES (?, ?, ?, ?, ?)
        ''', (id_patient, id_medecin, date_reservation, heure_reservation, duree_minutes))
        connexion.commit()
        print("Réservation ajoutée avec succès.")
        return cursor.lastrowid
    except ValueError:
        print("Erreur : Format de date ou d'heure incorrect. Utilisez AAAA-MM-JJ pour la date et HH:MM pour l'heure.")
        return None
    except sqlite3.IntegrityError:
        print("Erreur : Patient ou médecin inexistant.")
        return None



#Focntion qui permet de voir deux choses
    #Si on est un patient, alors on peut rechercher nos reservations
    #Si on est un docteur, alor on peut rechercher toutes nos reservations


def lister_reservations():
    connexion = sqlite3.connect('cabinet_medical.db')
    cursor = connexion.cursor()

    """Liste toutes les réservations avec détails"""
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
    print("\nListe des réservations :")
    for reservation in reservations:
        print(f"ID: {reservation[0]}, Patient: {reservation[1]}, Médecin: {reservation[2]}, "
              f"Date: {reservation[3]}, Heure: {reservation[4]}, Durée: {reservation[5]} minutes")
    connexion.close()