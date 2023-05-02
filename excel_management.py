from openpyxl import Workbook

def load_categories_from_excel(excel_workbook: Workbook):
    categories = {}
    last_category = ''
    overview_sheet = excel_workbook.get_sheet_by_name('Overview') # load worksheet overview
    
    category_area = False
    keywords = []
    for row in overview_sheet.iter_rows(max_col=2, values_only=True):
        if category_area == False and row[0] == None and row[1] == None: # a row with double None is the beginning of the categories
            category_area = True

        if category_area and row[0] != None:
            if len(keywords) != 0: # categories without any keywords are unnecessary to check
                categories[last_category] = keywords

            last_category = row[0]
            keywords = []
        
        if category_area and row[1] != None:
            keywords.append(row[1])

        if category_area and row[0] == None and row[1] == None: # a row with double None is also the end of the categories
            break
    
    print(categories)
    return categories