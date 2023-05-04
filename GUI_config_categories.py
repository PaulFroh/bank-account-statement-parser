import tkinter as tk
import excel_helper

class GUI_config_categories:   # definition of the class
        def __init__(self, found_categories):
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
                
                num_keys = len(found_categories.keys())
                num_values = len([val for sublist in found_categories.values() for val in sublist])
                num_all = num_keys + num_values
                print("Anzahl der Schlüssel: ", num_keys)
                print("Anzahl der Werte: ", num_values)
                print("Anzahl Gesamt: ", num_all)

                
                i = 0
                while i < num_keys:    # Outer While Loop which is active as many loops as keys are there in the dictonary
                    extracted_keys = list(found_categories.keys())[i]
                    extracted_sublist = list(found_categories.values())[i] # Creates a list of the "i-th" sublist
                    count_keys = len(extracted_keys)                       # Counts the amount of elements in the ectracted sublist
                    count_sublist = len(extracted_sublist)

                    for m in range(count_keys):   
                        self.label = tk.Label(self.root, text=extracted_keys[m])                     # creates a label with the first key of the "i-th sublist"
                        self.label.grid(column=1, row=[2+m], padx="5", pady="1", sticky=tk.W)                        
                        for n in range(count_sublist):                                      # creates a label with all elements of the specific sublist
                                self.label = tk.Label(self.root, text=extracted_sublist[n])
                        self.label.grid(column=1, row=[m+n+1], padx="5", pady="1", sticky=tk.W)
                        
                        
                        

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


GUI_config_categories()

