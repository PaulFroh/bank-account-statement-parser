import os
import json
import re

import excel_helper


def get_config_folder():
    return '.' + os.sep + 'parser_config' + os.sep

def load_config(config_name):
    config_path = get_config_folder() + config_name + '.json'
    if os.path.exists(config_path):
        f = open(config_path)
        config_json = json.load(f)

        return config_json
    
    return None

def get_excel_path():
    config = load_config('user_config')

    if config == None:
        return None

    return config['default_path']

def write_config(config_name, config):
    json_object = json.dumps(config, indent=4)

    if not os.path.exists('.' + os.sep + 'parser_config'):
        os.mkdir("parser_config")

    with open(get_config_folder() + config_name + '.json', 'w+') as outfile:
        outfile.write(json_object)
        
def safe_categories(categories):
    config = load_config('category_config')
    
    if config == None:
        config = {}
    
    config['categories'] = categories
    
    write_config('categories_config', config)
        
def safe_default_path(path):
    print("New default Path")
    config = load_config('user_config')
    
    if config == None:
        config = {}
    
    config['default_path'] = path
    
    write_config('user_config', config)

def load_config_categories():
    config_path = get_config_folder() + 'categories_config.json'
    with open(config_path) as f:
        data = json.load(f)
    categories = data['categories']
    return categories


def search_for_new_categories(dealings, path_excel):
    categories = load_config_categories()
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
                        if category not in found_categories.keys():
                            found_categories[category] = []
                        
                        if keyword not in found_categories[category]:
                            found_categories[category].append(keyword)

    return found_categories


    