import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import pdf_helper
import config_helper

from excel_helper import export_new_categories

class MainGUI(tk.Tk):   # definition of the class

    def __init__(self):
        super().__init__()
        
        self.resizable(0,0)    # Window is not adjustable
        self.geometry("680x450")
        self.title("Path-Configurator")

        # Headline
        self.label = tk.Label(self, text="Bank Account Statement Parser", font=('Arial', 18))   # adds a Label above the entry to let people know what the program expects
        self.label.grid(column=1, row=1, padx="20", pady="50")


        # Lable for the Excel file-path entry
        self.label = tk.Label(self, text="Excel-File path:", font=('Arial',11))   # adds a Label so people know what the program expects
        self.label.grid(column=0, row=2, padx="10", pady="10")
        # entry for the Excel file
        self.entry = tk.Entry (self, text="Hallo", width=50, font=('Arial',11))              # ads the entry field 
        
        excel_path = config_helper.get_excel_path()
        if excel_path != None:
            self.entry.delete(0, "end")
            self.entry.insert(0, excel_path)  
        
        
        self.entry.grid(column=1, row=2, padx="10", pady="10")
        # button for adding an Excel-file path
        self.button = tk.Button(self, text="Choose path", relief="groove" , font=('Arial', 10), bg="lightgrey", command=lambda: self.excel_directory(self.entry))  # if you click on the button the function show_directory will be passed and called whenever the button is clicked
        self.button.grid(column=1, row=3, padx="10", pady="10", sticky=tk.E)

        # adding a check button for default excel path
        self.check_state = tk.IntVar()
        self.check = tk.Checkbutton(self, text="Set to default", font=('Arial',10), variable=self.check_state)
        self.check.grid(column=1, row=3, padx="5", pady="5", sticky=tk.W)


        # Lable for the pdf file-path entry
        self.label_1 = tk.Label(self, text="PDF-File path:", font=('Arial',11))   # adds a Label so people know what the program expects
        self.label_1.grid(column=0, row=4, padx="10", pady="10")
        # entry for the pdf file
        self.entry_1 = tk.Entry (self, width=50, font=('Arial',11))              # ads the entry field 
        self.entry_1.grid(column=1, row=4, padx="10", pady="10")
        # button for adding a pdf-file path
        self.button_1 = tk.Button(self, text="Choose path", relief="groove", font=('Arial', 10), bg="lightgrey", command=lambda: self.pdf_directory(self.entry_1))  # if you click on the button the function show_directory_1 will be passed and called whenever the button is clicked
        self.button_1.grid(column=1, row=5, padx="10", pady="10", sticky=tk.E)

        # adding a check button for choosing a whole folder instead of only one file
        self.check_state_1 = tk.IntVar()
        self.check_1 = tk.Checkbutton(self, text="Choose folder", font=('Arial',10), variable=self.check_state_1)
        self.check_1.grid(column=1, row=5, padx="5", pady="5", sticky=tk.W)
        
        
        #button for transfer the data in the end
        self.button_run = tk.Button(self, text="Transfer", relief="groove", font=('Arial',11), bg="lightgrey", command=self.transfer_data)  # if you click on the button the function transfer data will be passed and called whenever the button is clicked
        self.button_run.grid(column=2, row=6, padx="10",sticky=tk.E, pady="50")
    
    

        
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
                    
   
   # Data transfer
    def transfer_data(self):
        excel_file_path = self.entry.get()
        pdf_file_path = self.entry_1.get()
         # Error message
        if  excel_file_path == '' or pdf_file_path == '':
            messagebox.showerror("Error", "Path incomplete")
        else:
            checkbox_value = self.check_state.get()
            print(f"Excel-Filepath: {excel_file_path}")
            print(f"PDF-Filepath: {pdf_file_path}")
            
            found_categories = pdf_helper.execute_parse(excel_file_path, pdf_file_path, search_categories=True)
            
            if found_categories != None:
                category_window = CategoryGUI(self, found_categories, excel_file_path)
                category_window.grab_set()
                

            if checkbox_value:
                config_helper.safe_default_path(excel_file_path)
                
                

class CategoryGUI(tk.Toplevel):
    
    def __init__(self, parent, found_categories, excel_path) -> None:
        super().__init__(parent)
        self.parent = parent
        
        self.geometry("800x550")
        self.title("Categories-Configurator")
        self.found_categories = found_categories
        self.excel_path = excel_path
        # Outer frames
        frame1 = tk.Frame(self, height=75, width=800, bd=2, relief="groove")
        frame1.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        frame3 = tk.Frame(self, height=75, width=800)
        frame3.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

        # Outer Content
        # Headline
        label_headline = tk.Label(frame1, text="Categories Custom-Settings", font=("Helvetica", 23, 'bold underline'),  fg="black")
        label_headline.pack(side=tk.TOP, pady=30)

        # Checkbox für alle Kategorien
        select_all_var = tk.IntVar()
        select_all_checkbox = tk.Checkbutton(frame3, text="Select All", font=("Arial", 10, 'bold'), variable=select_all_var, command=lambda: select_all(select_all_var.get()))
        select_all_checkbox.pack(side=tk.LEFT, padx=40)

        # Middle frame with scrollbar
        frame2 = tk.Frame(self, bd=2, relief="groove")
        frame2.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        self.canvas = tk.Canvas(frame2, bg="white")
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scrollbar = ttk.Scrollbar(frame2, orient=tk.VERTICAL, command=self.canvas.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.canvas.configure(yscrollcommand=scrollbar.set)

        # Inner content
        self.inner_frame = tk.Frame(self.canvas, bg="white")

        # Funktion zum Auswählen/Abwählen aller Checkboxen in frame2
        def select_all(value):
            for widget in self.inner_frame.winfo_children():
                if isinstance(widget, tk.Checkbutton):
                    widget.deselect()
                    if value == 1:
                        widget.select()

        # Lable which asks you if you want to add the categories and keywords to the excel file
        label_transfer = tk.Label(frame3, text="Add the selected categories?", font=('Helvetica',11, 'bold'))
        label_transfer.pack(side=tk.TOP, padx="80", pady="10", anchor='ne')

        # button for NOT adding the new categories to the excel /transfer the data
        button_dont = tk.Button(frame3, text="No", relief="groove", font=('Helvetica',11), bg="lightgrey", width=10, command=self.quit)
        button_dont.pack(side=tk.RIGHT, padx="50", pady="10")


        # button for adding the new categories to the excel /transfer the data
        button_do = tk.Button(frame3, text="Yes", relief="groove", font=('Helvetica',11), width=10, bg="lightgrey", command=self.transfer_categories)
        button_do.pack(side=tk.RIGHT, padx="10", pady="10")
        #button_do.config(command=transfer_categories)


        # LOOPS which create as many checkbuttons as categories and sub categories 
        self.keyword_checkboxes = {}
        index_category = 0
        row_index = 0  # Row index for order of checkbuttons
        for category in self.found_categories:
            label = tk.Label(self.inner_frame, text=category, font=('Helvetica',10, 'bold underline'),bg="white", fg="black",)
            label.grid(row=row_index, column=(index_category%4)*2, padx="20", pady="5", sticky=tk.W)
            
            self.keyword_checkboxes[category] = []

            # Order of the subcategory per category
            index_keyword = 0
            for keyword in self.found_categories[category]:
                check_state = tk.IntVar()
                check = tk.Checkbutton(self.inner_frame, text=keyword, font=('Helvetica',10), bg="white", fg="black", variable=check_state)
                check.grid(row=row_index+1+index_keyword, column=(index_category%4)*2, padx="30", pady="5", sticky=tk.W)
                index_keyword += 1
                
                self.keyword_checkboxes[category].append((keyword, check_state))
            
            # After every fourth category a new row will begin
            index_category += 1
            if index_category % 4 == 0:
                row_index += index_keyword + 40  # +2 für die Lücke zwischen den Kategorien


        self.canvas.create_window((0,0), window=self.inner_frame, anchor="nw")
        self.inner_frame.bind("<Configure>", self.resize_canvas)

    def resize_canvas(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    

    def quit(self):
        self.destroy()


    def transfer_categories(self):
        new_categories = {}
        for category in self.keyword_checkboxes:
            for checkbox_status in self.keyword_checkboxes[category]:
                if checkbox_status[1].get():
                    if category not in new_categories.keys():
                        new_categories[category] = []
                    new_categories[category].append(checkbox_status[0])
                                
        export_new_categories(new_categories, self.excel_path)
        messagebox.showinfo("Info", "The new categories are now in the excel")
        
        excel_file_path = self.parent.entry.get()
        pdf_file_path = self.parent.entry_1.get()
        pdf_helper.execute_parse(excel_file_path, pdf_file_path, search_categories=False)
        
        self.quit()



    
if __name__ == '__main__':
    app = MainGUI()
    app.mainloop()
