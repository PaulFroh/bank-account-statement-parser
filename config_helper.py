import os
import json

config_path = '.' + os.sep + 'parser_config' + os.sep + 'config.json'

def load_config():
    global config_path
    if os.path.exists(config_path):
        f = open(config_path)
        config_json = json.load(f)

        return config_json
    
    return None

def get_excel_path():
    config = load_config()

    if config == None:
        return None

    return config['default_path']

def write_config(path_excel):
    config = {}
    config['default_path'] = path_excel

    json_object = json.dumps(config, indent=4)

    if not os.path.exists('.' + os.sep + 'parser_config'):
        os.mkdir("parser_config")

    with open(config_path, 'w+') as outfile:
        outfile.write(json_object)

def load_config_categories(config_path):
    with open(config_path) as f:
        data = json.load(f)
    categories = data['categories']
    return categories

    