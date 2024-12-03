import sqlite3
import hashlib

def check_connexion(email_connexion, pwd_connexion, table, id):
    try :
        connexion = sqlite3.connect('cabinet_medical333.db')
        cursor = connexion.cursor()
        hash_password = hashlib.sha256(pwd_connexion.encode()).hexdigest()
        cursor.execute(f'''
           SELECT 
               {id}
           FROM 
               {table}
           WHERE
               password = ? AND email = ?
           ''', (hash_password, email_connexion))
    except sqlite3.OperationalError as e:
        print("E-mail and password do not match, try again. Maybe you are not registered yet.")
        print(e)

    result = cursor.fetchone()
    connexion.close()

    return result is not None


#print(check_connexion('dpntjean@mail.com', 'caraeldu04', 'patients'))


