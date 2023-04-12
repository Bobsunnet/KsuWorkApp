from datetime import datetime
import configEditor
import shutil
import os

backup_path = 'backups'
config_file_path = 'config_file.ini'

today_date = datetime.now().date()
directory_objects = os.listdir(os.getcwd())


def create_backup_folder():
    if backup_path not in directory_objects:
        os.mkdir(backup_path)


def create_db_copy(path) -> Exception:  # создает новую копию файла и называет с учетом даты создания
    try:
        shutil.copy('refuges.db', path)
        try:
            os.rename(f'{path}/refuges.db', f'{path}/{today_date}_refuges.db')
        except Exception as ex_rename:
            print(ex_rename)
            return ex_rename
    except Exception as ex_copy:
        print(ex_copy)
        return ex_copy


def create_db_dump(): # создает дамп файл для бд
    pass


def write_backup():
    """ Создает папку (если нету) и записывает файл бекапа БД. Если возникает ошибка - возвращает исключение"""
    create_backup_folder() # creating folder if doesnt exist
    today = str(today_date)
    last_backup_date = configEditor.get_setting(config_file_path, 'backup_settings', 'last_backup_date')
    # reading last_backup_date and making backup copy of db file if it
    if last_backup_date != today:
        record_exception = create_db_copy(backup_path)
        if record_exception:
            return record_exception
        configEditor.update_setting(config_file_path, 'backup_settings', 'last_backup_date', today)


if __name__ == '__main__':
    res = write_backup()
    print(res)

