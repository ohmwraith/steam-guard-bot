import mysql.connector
import datetime
import uuid
import sys
import configparser
class objectDB():
    @staticmethod
    def create():
        pass

    @staticmethod
    def validate():
        pass

    @staticmethod
    def remove():
        pass

class licenseDB(objectDB):
    
    def create(conn, expire_days):
        """
        Создает в базе данных лицензию и возвращает uuid

        На вход принимает соединение с базой данных и длительность лицензии (в днях)
        """
        cursor = conn.cursor()
        l_uuid = str(uuid.uuid4())
        exp_date = (datetime.datetime.now() + datetime.timedelta(days=expire_days)).strftime('%Y-%m-%d %H:%M:%S')
        cursor.execute(f"INSERT INTO licenses (uuid, expiry_date) VALUES (%s, %s)", (l_uuid, exp_date))
        cursor.close()
        return l_uuid
    

    
    def validate(conn, l_uuid):
        """
        Проверяет, является лицензия действительной или нет

        Возвращает True если лицензия действительна
        """
        cursor = conn.cursor()
        cursor.execute(f"SELECT expiry_date FROM licenses WHERE uuid = '{l_uuid}' LIMIT 1")
        try:
            exp_date = cursor.fetchall()[0][0]
        except IndexError:
            return False
        finally:
            cursor.close()
        return exp_date >= datetime.datetime.now()


    def remove(conn, l_uuid):
        """
        Удаляет запись о лицензии в базе данных
        Возвращает True если удаление успешно
        """
        cursor = conn.cursor()
        cursor.execute(f"DELETE FROM licenses WHERE uuid = '{l_uuid}'")
        rowcount = cursor.rowcount
        cursor.close()
        return rowcount == 1

class userDB(objectDB):
    def create(conn, t_id):
        """
        Создает пользователя в БД с t_id
        """
        cursor = conn.cursor()
        try:
            cursor.execute(f"INSERT INTO owners (telegram_id) VALUES ('{t_id}')")
            rowcount = cursor.rowcount == 1
        except mysql.connector.errors.IntegrityError:
            return False
        finally:
            rowcount = cursor.rowcount == 1
            cursor.close()
        return rowcount == 1


    def remove(conn, t_id):
        """
        Удаляет пользователя из БД по telegram_id
        """
        cursor = conn.cursor()
        cursor.execute(f"DELETE FROM owners WHERE t_id = '{t_id}'")
        rowcount = cursor.rowcount
        cursor.close()
        return rowcount == 1

    # Обновляет имя пользователя в БД по telegram_id
    @staticmethod
    def update_name(conn, t_id, name = ""):
        """
        Обновляет имя пользователя учетной записи
        """
        cursor = conn.cursor()
        cursor.execute(f"UPDATE owners SET owners.username = '{name}' WHERE owners.telegram_id = '{t_id}'")
        rowcount = cursor.rowcount
        cursor.close()
        return rowcount == 1
    

class manageDB():

    @staticmethod
    def get_all():
        pass
    
    @staticmethod
    def clear_all():
        pass

class licenseManageDB():

    def get_all(conn):
        cursor = conn.cursor()
        cursor.execute(f"SELECT * FROM licenses")
        l_list = cursor.fetchall()
        cursor.close()
        return l_list

    def clear_all(conn):
        cursor = conn.cursor()
        cursor.execute("TRUNCATE TABLE licenses CASCADE")
        rowcount = cursor.rowcount
        cursor.close()
        return rowcount

class licenseAssigner():
    
    def assign(conn, l_uuid, t_id):
        """
        Присваивает пользователю существующую лицензию
        """
        cursor = conn.cursor()
        cursor.execute(f"UPDATE owners SET owners.license_uuid = '{l_uuid}' WHERE owners.telegram_id = '{t_id}'")
        rowcount = cursor.rowcount
        cursor.close()
        return rowcount == 1
    
    def unassign(conn, t_id):
        cursor = conn.cursor()
        l_uuid = cursor.execute(f"SELECT license_uuid FROM owners WHERE telegram_id = '{t_id}'")
        cursor.execute(f"UPDATE owners SET owners.license_uuid = NULL WHERE owners.telegram_id = '{t_id}'")
        rowcount = cursor.rowcount
        cursor.close()
        return l_uuid

class userLicense():
    
    @staticmethod
    def get(conn, t_id):
        cursor = conn.cursor()
        cursor.execute(f"SELECT license_uuid FROM owners WHERE telegram_id = '{t_id}'")
        l_uuid = cursor.fetchall()[0][0]
        cursor.close()
        return l_uuid

    

if __name__ == '__main__':
    config = configparser.ConfigParser()
    config.read('config.ini')
    # create a connection to the database
    conn = mysql.connector.connect(
    host=config['MySQL']['host'],
    user=config['MySQL']['user'],
    password=config['MySQL']['password'],
    database=config['MySQL']['database']
    )
    with conn:
        if conn.is_connected():
            print("Соединение с базой данных MySQL установлено")
        else:
            print("Соединение с базой данных MySQL не установлено")
            
        # Do something ...

        
        conn.commit()
        conn.close()
