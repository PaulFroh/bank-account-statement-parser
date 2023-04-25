from pypdf import PdfReader
from tkinter import messagebox
import re
import json
import pandas as pd
import datetime
import os
import sys

categories = {}
path_xlsx = ""
bank = ""

def load_categories_from_excel(path):
    global categories
    categories_raw = pd.read_excel(path, sheet_name='Overview', usecols="A:B", names=["CATEGORY", "KEYWORD"])
    #print(categories)

    last_category = ''
    category_start = False
    for index, row in categories_raw.iterrows():
        print(row)
        if not category_start and pd.isna(row["CATEGORY"]) and pd.isna(row["KEYWORD"]):
            category_start = True
            continue
        
        if category_start and pd.isna(row["CATEGORY"]) and pd.isna(row["KEYWORD"]):
            break


        if category_start and not pd.isna(row['CATEGORY']):
            last_category = row['CATEGORY']
            categories[row['CATEGORY']] = []
        
        if category_start and not pd.isna(row['KEYWORD']):
            categories[last_category].append(row['KEYWORD'])

    print(categories)


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

def identify_category(string):
    global categories
    upper_string = string.upper()

    for category in categories:
        for keyword in categories[category]:
            keyword_str = str(keyword).upper()
            if re.search('\\b' + re.escape(keyword_str) + '\\b', upper_string):
                return category, keyword

    return "Sonstiges", ""


def get_dealings(lines):
    use = ''
    date = ""
    array = []
    for element in lines:
        #print(element)
        if re.search("^[0-3]?[0-9][/.][0-3]?[0-9][/.][0-9]{4}", element): # start of a deal
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
            category, keyword = identify_category(use)

            if date != '':
                array.append([date, category, use, keyword, price])

            use = ''
            date = ''
            keyword = ''
            #print('')

        if re.search("Kontostand", element) and len(array) > 1:
            kontostand = parse_number(element.split()[-1])
            date = re.search('[0-3]?[0-9][/.][0-3]?[0-9][/.][0-9]{4}', element).group()

            array.append([date, "KONTOSTAND", element, '', kontostand])
            break
        

    return array # erster Eintrag ist alter Kontostand


def parse_pdf(path):
    print("Path to PDF: " + path)
    colums = ["Date", "Category", "Use", "Keyword", "Price"]
    
    page_count, month = get_info(path)
    lines = get_relevant_lines(path, page_count)
    df = pd.DataFrame(get_dealings(lines), columns=colums)

    print(df.to_markdown())
    return df, month


def execute_parse(path_excel, path_to_pdfs):

    try:
        load_categories_from_excel(path_excel)

        if os.path.isfile(path_to_pdfs):
            df, month = parse_pdf(path_to_pdfs)
            export_to_excel(path_excel, df, month)
            

        elif os.path.isdir(path_to_pdfs):
            if not path_to_pdfs[-1] == os.sep:
                path_to_pdfs += os.sep

            for pdf in os.listdir(path_to_pdfs):
                df, month = parse_pdf(path_to_pdfs + pdf)
                export_to_excel(path_excel, df, month)
                print('')
        
        else:
            messagebox.showerror(title='Error', message='This PDF file does not exist!')
            return False
    except Exception as e:
        messagebox.showerror(title='Error', message='An error has occurred!\n' + str(e))
        return False
    return True


def export_to_excel(path_excel, dataframe, sheet_name):
    with pd.ExcelWriter(path_excel, mode='a', if_sheet_exists="overlay") as writer:
        dataframe.to_excel(writer, sheet_name=sheet_name)
