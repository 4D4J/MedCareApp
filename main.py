import sqlite3
from datetime import datetime
from multiprocessing.resource_tracker import register

from create_patient import ajouter_patient, lister_patients
from create_doctor import ajouter_medecin, lister_medecins
from create_reservation import ajouter_reservation, lister_reservations
from connexion import check_password







def fermer_connexion(self):
    """Ferme la connexion à la base de données"""
    self.conn.close()
    print("Connexion à la base de données fermée.")

# Continuation du script précédent
def register_login():

    choix = int(input("Que voulez-vous faire ? "
                  "\n1 : Se connecter en tant que patient, "
                  "\n2 : Se connecter en tant que patient"
                  "\n3 : S'inscrire en tant que patient, "
                  "\n4 : S'inscrire en tant que médecin, "
                  "\n> "))

    if choix == 1:
        if type(check_password(email_client=input('Enter your mail adress: '),pwd = input('Enter your password: '))) is int:
            print('Connected')
            #appel de la fonction pour le client
        else:
            print("email and password didn't match")




    elif choix == 3:

        ajouter_patient(
            nom=input('Indiquez votre nom de famille :'),
            prenom=input('Indiquez votre prenom :'),
            date_naissance=input("Indiquez votre date de naissance sous la forme : 1999-01-01 : "),
            telephone=input('Indiquez votre numéro de téléphone : '),
            email=input('Indiquez votre email : '),
            password=input('Indiquez votre password : ')
        )
    elif choix == 4:
        ajouter_medecin(
            nom=input('Indiquez votre nom de famille : '),
            prenom=input('Indiquez votre prenom : '),
            specialite=input('Indiquez vorte spécialité : '),
            telephone=input('Indiquez votre numéro de téléphone : '),
            email=input('Indiquez votre email : '),
            password=input('Indiquez votre password : ')
        )



    # Lister les informations
"""    print(lister_patients())
    print(lister_medecins())
    print(lister_reservations())"""


# Exécution du programme
if __name__ == "__main__":
    register_login()