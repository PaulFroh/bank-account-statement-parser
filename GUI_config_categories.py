import tkinter as tk
import excel_helper

class GUI_config_categories:   # definition of the class
        def __init__(self, found_categories, path_excel):
                self.found_categories = found_categories
                self.root = tk.Tk()
                self.root.resizable(0,0)    # Window is not ajustabl
                self.root.geometry("350x350")
                self.root.title("Categories-Configurator")
                
                # Headline
                self.label_headline = tk.Label(self.root, text="Categories Custom-Settings", font=('Arial', 18))   # adds a Label above the entry to let people know what the programm expects
                self.label_headline.grid(column=1, row=1, padx="20", pady="50")

                # Lable which tells the user that new categories were found 
                self.label_new = tk.Label(self.root, text="We found following new categories:", font=('Arial',11))   # adds a Label so people know what the programm expects
                self.label_new.grid(column=1, row=2, padx="10", pady="10")

                # FOR-LOOP --> Label area where the new categories are shown with checkboxes
                index_category = 0
                for category in found_categories:
                        
                        self.label = tk.Label(self.root, text=category)                     # creates a label with the first key of the "i-th sublist"
                        self.label.grid(column=1, row=[2+index_category], padx="5", pady="1", sticky=tk.W)
                        
                        index_keyword = 0
                        for keyword in found_categories[category]:                                      # creates a label with all elements of the specific sublist
                                self.label = tk.Label(self.root, text=keyword)
                                self.label.grid(column=1, row=[index_category+index_keyword+2], padx="5", pady="1", sticky=tk.W)
                                index_keyword += 1
                        index_category += 1   

                # Lable which asks you if you want to add the categories and keywords to the excel file
                self.label_transfer = tk.Label(self.root, text="Do you want to add the new categories?", font=('Arial',11))   # adds a Label so people know what the programm expects
                self.label_transfer.grid(column=1, row=4, padx="10", pady="10")




                # BUTTONS

                # button for NOT adding the new categories to the excel /transfer the data
                self.button_dont = tk.Button(self.root, text="No", relief="groove", font=('Arial',11), bg="lightgrey", command=self.quit)  # if you klick on the button the funktion transfer data will be passed and called whenever the button is klicked
                self.button_dont.grid(column=1, row=5, padx="10",sticky=tk.W, pady="50")

                # button for adding the new categories to the excel /transfer the data
                self.button_do = tk.Button(self.root, text="Yes", relief="groove", font=('Arial',11), bg="lightgrey", command=self.transfer_categories)  # if you klick on the button the funktion transfer data will be passed and called whenever the button is klicked
                self.button_do.grid(column=1, row=5, padx="10",sticky=tk.E, pady="50")

                
                self.root.mainloop()

        

        def quit(self):
                self.root.destroy()


        def transfer_categories(self):
                categories = {}
                excel_helper.export_new_categories(categories)


        # this class needs to be callable with a list of categories
        # Let the user decide which categories he wants
        # return the modified list

