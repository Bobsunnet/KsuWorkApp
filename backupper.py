from datetime import datetime
import shutil
import os

today_date = datetime.now().date()
directory_objects = os.listdir(os.getcwd())


def create_backup_folder():
    if 'backups' not in directory_objects:
        os.mkdir('backups')


def create_db_backup() -> Exception:  # создает новую копию файла и называет с учетом даты создания
    try:
        shutil.copy('refuges.db', 'backups')
        try:
            os.rename('backups/refuges.db', f'backups/{today_date}_refuges.db')
        except Exception as ex_rename:
            print(ex_rename)
            return ex_rename
    except Exception as ex_copy:
        print(ex_copy)
        return ex_copy


def create_config_file():
    if 'boot_config.txt' not in directory_objects:
        try:
            with open('boot_config.txt', 'w') as conf_file:
                conf_file.write('first run')
        except Exception as ex_create_file:
            print(ex_create_file)


def read_config_file() -> str:
    try:
        with open('boot_config.txt', 'r') as conf_file:
            last_update = conf_file.read()
            return last_update
    except Exception as ex_read_file:
        print(ex_read_file)


def write_date_config_file():
    try:
        with open('boot_config.txt', 'w') as conf_file:
            conf_file.write(str(today_date))
    except Exception as ex_write_file:
        print(ex_write_file)


def write_backup():
    #creating config file and folder if doesnt exist
    create_backup_folder()
    create_config_file()
    #reading config data(date) and making backup copy of db file
    config_data = read_config_file()
    if config_data != str(today_date) and config_data is not None:
        record_exception = create_db_backup()
        if not record_exception:
            write_date_config_file()


if __name__ == '__main__':
    write_backup()
    # print(os.listdir(os.getcwd()))
