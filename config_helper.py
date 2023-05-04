import os
import json
import re

import excel_helper
from GUI_config_categories import *

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


def search_for_new_categories(dealings, path_excel):
    categories = load_config_categories(config_path)
    print(categories)
    found_categories = {}
    
    for row in dealings:
        use = row[excel_helper.USE_ROW]
        upper_string = use.upper()

        if row[excel_helper.CATEGORY_ROW] == 'Sonstiges': # check only rows that do not have any category
            for category in categories:
                for keyword in categories[category]:
                    keyword_str = str(keyword).upper()
                    if re.search('\\b' + re.escape(keyword_str) + '\\b', upper_string):
                        found_categories[category] = keyword

    test = GUI_config_categories(found_categories, path_excel)


    