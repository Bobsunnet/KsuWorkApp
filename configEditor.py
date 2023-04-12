import os
from configparser import ConfigParser


def create_config_file(path):
    """ creates a config file"""
    config = ConfigParser()
    config.add_section("backup_settings")
    config.set('backup_settings', 'last_backup_date', 'None')
    config.set('backup_settings', 'backup_size', 'None')
    config.set('backup_settings', 'backup_type', 'db_copy')

    with open(path, 'w') as config_file:
        config.write(config_file)


def get_config(path):
    """reads and return configparser object"""
    if not os.path.exists(path):
        create_config_file(path)

    config = ConfigParser()
    config.read(path)
    return config


def get_setting(path, section, option):
    config = get_config(path)
    setting_value = config.get(section, option)

    return setting_value


def update_setting(path, section, option, value):
    config = get_config(path)
    config.set(section, option, value)

    with open(path, 'w') as config_file:
        config.write(config_file)


def delete_setting(path, section, option):
    config = get_config(path)
    config.remove_option(section,option)

    with open(path, 'w') as config_file:
        config.write(config_file)


if __name__ == "__main__":
    path = 'config_file.ini'
    value=get_setting(path,section='backup_settings', option='last_backup_date')
    print(value)



