import tkinter as tk
from tkinter import ttk, messagebox

from excel_helper import export_new_categories

class CategoryGUI():
    
    def __init__(self, found_categories, excel_path) -> None:
        self.root = tk.Tk()
        self.root.geometry("800x550")
        self.root.title("Categories-Configurator")
        self.found_categories = found_categories
        self.excel_path = excel_path
        # Outer frames
        frame1 = tk.Frame(self.root, height=75, width=800, bd=2, relief="groove")
        frame1.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        frame3 = tk.Frame(self.root, height=75, width=800)
        frame3.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

        # Outer Content
        # Headline
        label_headline = tk.Label(frame1, text="Categories Custom-Settings", font=("Arial", 23, 'bold'),  fg="black")
        label_headline.pack(side=tk.TOP, pady=30)

        # Checkbox für alle Kategorien
        select_all_var = tk.IntVar()
        select_all_checkbox = tk.Checkbutton(frame3, text="Select All", font=("Arial", 10, 'bold'), variable=select_all_var, command=lambda: select_all(select_all_var.get()))
        select_all_checkbox.pack(side=tk.LEFT, padx=40)

        # Middle frame with scrollbar
        frame2 = tk.Frame(self.root, bd=2, relief="groove")
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
        label_transfer = tk.Label(frame3, text="Add the new categories?", font=('Arial',11, 'bold'))
        label_transfer.pack(side=tk.TOP, padx="80", pady="10", anchor='ne')

        # button for NOT adding the new categories to the excel /transfer the data
        button_dont = tk.Button(frame3, text="No", relief="groove", font=('Arial',11), bg="lightgrey", width=10, command=self.quit)
        button_dont.pack(side=tk.RIGHT, padx="50", pady="10")


        # button for adding the new categories to the excel /transfer the data
        button_do = tk.Button(frame3, text="Yes", relief="groove", font=('Arial',11), width=10, bg="lightgrey", command=self.transfer_categories)
        button_do.pack(side=tk.RIGHT, padx="10", pady="10")
        #button_do.config(command=transfer_categories)


        # LOOPS which create as many checkbuttons as categories and sub categories 
        self.keyword_checkboxes = {}
        index_category = 0
        row_index = 0  # Row index for order of checkbuttons
        for category in self.found_categories:
            label = tk.Label(self.inner_frame, text=category, font=('Arial',10, 'bold'))
            label.grid(row=row_index, column=(index_category%4)*2, padx="5", pady="5", sticky=tk.W)
            
            
            self.keyword_checkboxes[category] = []

            # Order of the subcategory per category
            index_keyword = 0
            for keyword in self.found_categories[category]:
                check_state = tk.IntVar()
                check = tk.Checkbutton(self.inner_frame, text=keyword, font=('Arial',10), bg="white", fg="black", variable=check_state)
                check.grid(row=row_index+1+index_keyword, column=(index_category%4)*2, padx="5", pady="5", sticky=tk.W)
                index_keyword += 1
                
                self.keyword_checkboxes[category].append((keyword, check_state))
            
            # After every fourth category a new row will begin
            index_category += 1
            if index_category % 4 == 0:
                row_index += index_keyword + 40  # +2 für die Lücke zwischen den Kategorien



        self.canvas.create_window((0,0), window=self.inner_frame, anchor="nw")
        self.inner_frame.bind("<Configure>", self.resize_canvas)

        self.root.mainloop()

    def resize_canvas(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    

    def quit(self):
        self.root.destroy()


    def transfer_categories(self):
        categories = {}
        for category in self.keyword_checkboxes:
            for checkbox_status in self.keyword_checkboxes[category]:
                if checkbox_status[1].get():
                    if category not in categories.keys():
                        categories[category] = []
                    categories[category].append(checkbox_status[0])
                                
        print(categories)
        export_new_categories(categories, self.excel_path)
        messagebox.showinfo("Info", "The new categories are now in the excel")
        self.quit()
