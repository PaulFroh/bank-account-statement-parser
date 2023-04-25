import tkinter as tk
from tkinter import filedialog
import parse_kontoauszug
import config_managment

class GUI:   # definition of the class

    def __init__(self):
        self.root = tk.Tk()
        self.root.resizable(0,0)    # Window is not ajustabl
        self.root.geometry("680x450")
        self.root.title("Path-Configurator")

        # Headline
        self.label = tk.Label(self.root, text="Bank Account Statement Parser", font=('Arial', 18))   # adds a Label above the entry to let people know what the programm expects
        self.label.grid(column=1, row=1, padx="20", pady="50")


        # Lable for the Excel file-path entry
        self.label = tk.Label(self.root, text="Excel-File path:", font=('Arial',11))   # adds a Label so people know what the programm expects
        self.label.grid(column=0, row=2, padx="10", pady="10")
        # entry for the Excel file
        self.entry = tk.Entry (self.root, width=50, font=('Arial',11))              # ads the entry field 
        self.entry.grid(column=1, row=2, padx="10", pady="10")
        # button for adding an Excel-file path
        self.button = tk.Button(self.root, text="Choose path", font=('Arial', 10), command=lambda: self.excel_directory(self.entry))  # if you klick on the button the funktion show_directory will be passed and called whenever the button is klicked
        self.button.grid(column=1, row=3, padx="10", pady="10", sticky=tk.E)

        # adding a check button for default excel path
        self.check_state = tk.IntVar()
        self.check = tk.Checkbutton(self.root, text="set to default", font=('Arial',10), variable=self.check_state)
        self.check.grid(column=1, row=3, padx="5", pady="5", sticky=tk.W)


        # Lable for the pdf file-path entry
        self.label_1 = tk.Label(self.root, text="PDF-File path:", font=('Arial',11))   # adds a Label so people know what the programm expects
        self.label_1.grid(column=0, row=4, padx="10", pady="10")
        # entry for the pdf file
        self.entry_1 = tk.Entry (self.root, width=50, font=('Arial',11))              # ads the entry field 
        self.entry_1.grid(column=1, row=4, padx="10", pady="10")
        # button for adding a pdf-file path
        self.button_1 = tk.Button(self.root, text="Choose path", font=('Arial', 10), command=lambda: self.pdf_directory(self.entry_1))  # if you klick on the button the funktion show_directory_1 will be passed and called whenever the button is klicked
        self.button_1.grid(column=1, row=5, padx="10", pady="10", sticky=tk.E)

        # adding a check button for choosing a whole folder instead of only one file
        self.check_state_1 = tk.IntVar()
        self.check_1 = tk.Checkbutton(self.root, text="Choose folder", font=('Arial',10), variable=self.check_state_1)
        self.check_1.grid(column=1, row=5, padx="5", pady="5", sticky=tk.W)
        
        
        #button for transfer the data in the end
        self.button_run = tk.Button(self.root, text="Transfer", font=('Arial',11), command=self.transfer_data)  # if you klick on the button the funktion transfer data will be passed and called whenever the button is klicked
        self.button_run.grid(column=2, row=6, padx="10",sticky=tk.E, pady="50")
    

        self.root.mainloop()

        
        # method to open excel path
    def excel_directory(self,entry):
        filepath = filedialog.askopenfilename(title="Choose file", filetypes=[("Excel-File", "*.xlsx"),("All types", "*.*")])
        entry.delete(0, tk.END)  # clear the entry field
        entry.insert(0, filepath)  # insert the selected file path
                    
       
            # method to open pdf or file path
    def pdf_directory(self, entry_1):
        checkbox_value_1 = self.check_state_1.get() 
        if checkbox_value_1 == 0:
            path = filedialog.askopenfilename(title="Choose file", filetypes=[("PDF-File", "*.pdf"),("All types", "*.*")])
            entry_1.delete(0, tk.END)  # clear the entry field
            entry_1.insert(0, path)  # insert the selected file path
                    
        else:
            path = filedialog.askdirectory(title="Choose folder")
            entry_1.delete(0, tk.END)  # clear the entry field
            entry_1.insert(0, path)  # insert the selected file path
                    
   
   # Datentransfer
    def transfer_data(self):
        excel_file_path = self.entry.get()
        pdf_file_path = self.entry_1.get()
         # Errormessage
        if  excel_file_path == '' or pdf_file_path == '':
            tk.messagebox.showerror("Error", "Path incomplete")
        else:
            checkbox_value = self.check_state.get()
            print(f"Excel-Filepath: {excel_file_path}")
            print(f"PDF-Filepath: {pdf_file_path}")
            parse_kontoauszug.execute_parse(excel_file_path, pdf_file_path)

            print(f"Checkbox-Value: {checkbox_value}")
            if checkbox_value:
                config_managment.write_config(excel_file_path)

    
    
GUI()
