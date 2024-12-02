import sqlite3
import hashlib

def check_password(email_client, pwd):
    connexion = sqlite3.connect('cabinet_medical.db')
    cursor = connexion.cursor()
    hash_password = hashlib.sha256(pwd.encode()).hexdigest()
    cursor.execute('''
       SELECT 
           id_patient
       FROM 
           patients
       WHERE
           password = ? AND email = ?
       ''', (hash_password, email_client))


    result = cursor.fetchone()
    print(result)
    connexion.close()

    return result is not None


print(check_password('dpntjean@mail.com', 'carameldu04'))


