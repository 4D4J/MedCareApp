import sqlite3
from datetime import datetime
from multiprocessing.resource_tracker import register

from create_patient import ajouter_patient, lister_patients
from create_doctor import ajouter_medecin, lister_medecins
from create_reservation import ajouter_reservation, lister_reservations
from connexion import check_connexion
import time
import os





def fermer_connexion(self):
    """Ferme la connexion à la base de données"""
    self.conn.close()
    print("Connexion à la base de données fermée.")

# Continuation du script précédent
def register_login():

    choix = int(input("Que voulez-vous faire ? "
                      "\n1: Login"
                      "\n2: Register"
                      "\n> "))




    if choix == 1:
        email = input('Email: ')
        while '@' not in email or '.' not in email:
            email = input('Email is wrongly written: ')
        password = input('Password: ')

        if check_connexion(email,password,table='patients',id='id_patient') is not False:
            print("Connexion to your Patient dashboard ...")
        elif check_connexion(email,password,table='medecins',id='id_medecin') is not False:
            print("Connexion to your Doctor dashboard ...")




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