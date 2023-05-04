import unittest

import config_helper
import excel_helper
from GUI_config_categories import *

class ExampleTest(unittest.TestCase):

    def test_example(self):
        self.assertEqual(1,1, "Should be 1")

class ExcelTest(unittest.TestCase):
    
    def test_new_categories(self):
        path_excel = config_helper.load_config()["default_path"]
        
        categories_new = {"Test": ["Keyword_1", "Test2"], "Lebensmittel": ["Test"]}
        
        excel_helper.export_new_categories(categories_new, path_excel)
        
class ConfigGUITest(unittest.TestCase):
    
    def test_startup(self):
        path_excel = config_helper.load_config()["default_path"]
        found_categories = {"Test": ["Keyword_1", "Test2"], "Lebensmittel": ["Test"]}
        
        GUI_config_categories(found_categories, path_excel)
        


if __name__ == '__main__':
    unittest.main()