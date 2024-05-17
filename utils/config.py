import configparser

config = configparser.ConfigParser()

def load_config(config_file):
    config.read(config_file)
    print(f"Configuration loaded from {config_file}")

def get_config(section, option):
    return config.get(section, option)

def set_config(section, option, value):
    if section not in config:
        config.add_section(section)
    config.set(section, option, value)

def save_config(config_file):
    with open(config_file, 'w') as file:
        config.write(file)
    print(f"Configuration saved to {config_file}")
