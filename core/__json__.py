import json

def load_json(path, encoding='utf8'):
    with open(path, 'r', encoding=encoding) as f:
        return json.load(f)

def write_json(path, data, encoding='utf8'):
    with open(path, 'w', encoding=encoding) as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def get_setting_data():
    return load_json('./json/setting.json')

def get_commands_data():
    return load_json('./json/commands.json')

def get_descriptions_data():
    return load_json('./json/descriptions.json')

def set_commands_data(data):
    write_json('./json/commands.json', data)

def set_descriptions_data(data):
    write_json('./json/descriptions.json',data)
