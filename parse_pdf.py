from pypdf import PdfReader
from tkinter import messagebox
import re
import openpyxl
import traceback
import datetime
import os

import excel_helper
import config_helper

path_xlsx = ""
bank = ""


def get_info(path):
    global bank

    reader = PdfReader(path)
    page = reader.pages[0]
    text = page.extract_text()

    if re.search("Sparkasse*", text): # search for the bank name
        bank = "SPARKASSE"
        text = re.search("Kontoauszug [0-9\/]*", text).group()
        date_text = text.split(' ')[1]
        print(date_text)
    
    elif re.search("Sparda- Bank", text):
        bank = "SPARDA"
        text = re.search("Kontoauszug Nr. [0-9\/]*", text).group()
        date_text = text.split(' ')[2]
        print(date_text)
    
    else:
        messagebox.showerror(title='Error', message='This bank is not known!')
        exit()

    date = datetime.datetime.strptime(date_text, '%m/%Y').date()
    month = date.strftime("%B %Y")

    return len(reader.pages), month

def get_text(path, page_number=0):
    reader = PdfReader(path)
    page = reader.pages[page_number]
    text = page.extract_text()
    
    return text

def parse_number(string):
    result = re.search('\S+,[0-9]+', string).group()
    result = result.replace('.', '')
    result = result.replace(',', '.')
    number = float(result)

    if re.search('-$', string):
        number = number * -1
    
    return number


def get_relevant_lines(path, page_count):
    all_lines = []

    for i in range(page_count):
        text = get_text(path, i)
        text = re.sub(' +', ' ', text) # cut all doubles of whitespace

        lines = text.splitlines()
        unwanted_chars = {' ', '  '}
        lines = [ele for ele in lines if ele not in unwanted_chars] # cut all empty elements

        i = 0
        for element in lines:
            i += 1
            if re.search('Betrag EUR', element) or re.search('Betrag in EUR', element): # First is for Sparkasse and second for Sparda
                break
        all_lines += lines[i:]
    
    return all_lines

def identify_category(dealings, categories):
    for row in dealings:
        use = row[excel_helper.USE_ROW]
        upper_use = use.upper()

        if row[excel_helper.CATEGORY_ROW] == 'Sonstiges':
            for category in categories:
                for keyword in categories[category]:
                    keyword_str = str(keyword).upper()
                    if re.search('\\b' + re.escape(keyword_str) + '\\b', upper_use):
                        row[excel_helper.CATEGORY_ROW] = category
                        row[excel_helper.KEYWORD_ROW] = keyword

    return dealings


def get_dealings(lines):
    use = ''
    date = ''
    index = 0
    array = []
    for element in lines:
        #print(element)
        if re.search("^[0-3]?[0-9][/.][0-3]?[0-9][/.][0-9]{4}", element) and date == '': # start of a deal
            use = ''
            date = element.split()[0]
            #print(date)

            if(bank == "SPARDA"):
                use = re.sub('^[0-3]?[0-9][/.][0-3]?[0-9][/.][0-9]{4}', '', element)

        else:
            use += element

        if re.search("-?[0-9]+,[0-9]{1,2}[-|+]?$", element):   # last entry of deal has the price at the end

            if bank == "SPARDA" and re.search("RECHNUNGSABSCHLUSS", use):
                use = "Rechnungsabschluss "
                continue

            use = re.sub(' -?[0-9]+,[0-9]{1,2}[-|+]?$', '', use) # cut the price out of the use
            #print(use)
            price = parse_number(element.split()[-1])
            #print(price)

            if date != '':
                array.append([index, date, 'Sonstiges', use, keyword, price])

            use = ''
            date = ''
            keyword = ''
            index += 1
            #print('')

        if re.search("Kontostand", element) and len(array) > 1:
            kontostand = parse_number(element.split()[-1])
            date = re.search('[0-3]?[0-9][/.][0-3]?[0-9][/.][0-9]{4}', element).group()

            array.append([index, date, "KONTOSTAND", element, '', kontostand])
            break
        

    return array # erster Eintrag ist alter Kontostand


def parse_pdf(path):
    print("Path to PDF: " + path)
    first_row = ["", "Date", "Category", "Use", "Keyword", "Price"]
    
    page_count, month = get_info(path)
    lines = get_relevant_lines(path, page_count)
    dealings = get_dealings(lines)

    return first_row, dealings, month


def execute_parse(path_excel, path_to_pdfs, search_categories = False):
    # get signal if the search for new categories is active

    try:
        excel_file = openpyxl.load_workbook(path_excel)
        categories = excel_helper.load_categories_from_excel(excel_file)

        if os.path.isfile(path_to_pdfs):
            first_row, dealings, month = parse_pdf(path_to_pdfs)
            dealings = excel_helper.check_for_manual_changes(excel_file, dealings, month)
            dealings = identify_category(dealings, categories)
            # if signal is true load categories from config an check for new categories
            # if there are new categories call the config gui to let the user decide which one he wants
            # update the categories dict
            if search_categories:
                config_helper.search_for_new_categories(dealings, path_excel)
                categories = excel_helper.load_categories_from_excel(excel_file)
                dealings = identify_category(dealings, categories)

            excel_helper.export_to_excel(excel_file, first_row, dealings, month, path_excel)
            

        elif os.path.isdir(path_to_pdfs):
            if not path_to_pdfs[-1] == os.sep:
                path_to_pdfs += os.sep

            for pdf in os.listdir(path_to_pdfs):
                first_row, dealings, month = parse_pdf(pdf)
                dealings = excel_helper.check_for_manual_changes(excel_file, dealings, month)
                excel_helper.export_to_excel(excel_file, first_row, dealings, month, path_excel)
                print('')
        
        else:
            messagebox.showerror(title='Error', message='This PDF file does not exist!')
            return False
        
        # update the overview table in the excel with the new categories
    except Exception as e:
        print(traceback.format_exc())
        messagebox.showerror(title='Error', message='An error has occurred!\n' + str(e))
        return False
    return True
