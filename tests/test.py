import unittest
import openpyxl

import config_helper
import excel_helper
from GUI_config_categories import *

class ExampleTest(unittest.TestCase):

    def test_example(self):
        self.assertEqual(1,1, "Should be 1")

class ExcelTest(unittest.TestCase):
    
    def test_new_categories(self):
        path_excel = config_helper.get_excel_path()
        
        categories_new = {"Test": ["Keyword_1", "Test2"], "Lebensmittel": ["Test"]}
        
        excel_helper.export_new_categories(categories_new, path_excel)
        
class ConfigGUITest(unittest.TestCase):
    
    def test_startup(self):
        path_excel = config_helper.get_excel_path()
        found_categories = {"TOP CATEGORY Nr.1": ["Keyword Nr. 1", "Keyword Nr. 2"], "TOP CATEGORY Nr. 2": ["Keyword Nr. 1", "Keyword Nr. 2", "Keyword Nr. 3"], "TOP CATEGORY Nr. 3": ["Keyword Nr. 1", "Keyword Nr. 2", "Keyword Nr. 3", "Keyword Nr. 4"], "TOP CATEGORY Nr. 4": ["Keyword Nr. 1", "Keyword Nr. 2", "Keyword Nr. 3"], "TOP CATEGORY Nr.5": ["Keyword Nr. 1", "Keyword Nr. 2", "Keyword Nr. 3", "Keyword Nr. 4"], "TOP CATEGORY Nr.6": ["Keyword Nr. 1", "Keyword Nr. 2", "Keyword Nr. 3"], "TOP CATEGORY Nr.7": ["Keyword Nr. 1", "Keyword Nr. 2", "Keyword Nr. 3", "Keyword Nr. 4", "Keyword Nr. 5"], "TOP CATEGORY Nr.8": ["Keyword Nr. 1", "Keyword Nr. 2"], "TOP CATEGORY Nr.9": ["Keyword Nr. 1", "Keyword Nr. 2", "Keyword Nr. 3"]}
        
        CategoryGUI(found_categories, path_excel)
        
        
class ExportCategories(unittest.TestCase):
    
    def test_export_config(self):
        path_excel = config_helper.get_excel_path()
        
        workbook = openpyxl.load_workbook(path_excel)
        categories = excel_helper.load_categories_from_excel(workbook, all=True)
        config_helper.safe_categories(categories)
        
        
        
        
        


if __name__ == '__main__':
    unittest.main()