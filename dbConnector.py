import sqlite3 as sq

refugees_database = 'refuges.db'
table = 'refugees'

create_db_query = '''
    CREATE TABLE refugees (
    contact_id INTEGER PRIMARY KEY,
	name TEXT,
	city TEXT,
	phone TEXT, 
	description TEXT 
	);
'''


def insert_into_refugees(contact_id='', name='', city='', description=''):
    insert_into_db_query = f'''
            INSERT INTO {table} (contact_id, name, city, description)
            VALUES (
            '{contact_id}', 
            '{name}',
            '{city}', 
            '{description}' ); '''
    with sq.connect(refugees_database) as connection:
        try:
            cursor = connection.cursor()
            cursor.execute(insert_into_db_query)
            return 'Success', None
        except sq.IntegrityError as integrity_error:
            print(f'[ERROR] problem: {integrity_error}')
            return 'integrity_error', integrity_error
        except Exception as ex:
            print(f'[ERROR] problem: {ex}')
            return False, ex


def select_all_from_refugees():
    select_all_query = f'''
    SELECT * FROM {table};
'''
    with sq.connect(refugees_database) as connection:
        try:
            cursor = connection.cursor()
            cursor.execute(select_all_query)
        except Exception as ex:
            print(f'[ERROR] problem: {ex}')

    return cursor.fetchall()


def update_city_refugees(id, city):
    update_query = f'''
    UPDATE {table}
    SET city = '{city}'
    WHERE id = {id};
'''
    with sq.connect(refugees_database) as connection:
        try:
            cursor = connection.cursor()
            cursor.execute(update_query)
        except Exception as ex:
            print(f'[ERROR] problem: {ex}')


def update_name_refugees(id, name):
    update_query = f'''
    UPDATE {table}
    SET name = '{name}'
    WHERE id = {id};
'''
    with sq.connect(refugees_database) as connection:
        try:
            cursor = connection.cursor()
            cursor.execute(update_query)
        except Exception as ex:
            print(f'[ERROR] problem: {ex}')


def update_description_refugees(id, description):
    update_query = f'''
    UPDATE {table}
    SET name = '{description}'
    WHERE id = {id};
'''
    with sq.connect(refugees_database) as connection:
        try:
            cursor = connection.cursor()
            cursor.execute(update_query)
        except Exception as ex:
            print(f'[ERROR] problem: {ex}')


def update_contact_id_refugees(id, contact_id):
    update_query = f'''
    UPDATE {table}
    SET name = '{contact_id}'
    WHERE id = {id};
'''
    with sq.connect(refugees_database) as connection:
        try:
            cursor = connection.cursor()
            cursor.execute(update_query)
        except Exception as ex:
            print(f'[ERROR] problem: {ex}')


def delete_row(contact_id):
    del_query = f'''
    DELETE FROM {table}
    WHERE contact_id = '{contact_id}';
'''
    with sq.connect(refugees_database) as connection:
        try:
            cursor = connection.cursor()
            cursor.execute(del_query)
        except Exception as ex:
            print(f'[ERROR] problem: {ex}')


if __name__ == '__main__':
    insert_into_refugees()
