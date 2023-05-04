import tkinter as tk

class GUI_config_categories:   # definition of the class
        def __init__(self):
                self.root = tk.Tk()
                self.root.resizable(0,0)    # Window is not ajustabl
                self.root.geometry("350x350")
                self.root.title("Categories-Configurator")

                # Headline
                label = tk.Label(self.root, text="Categories Custom-Settings", font=('Arial', 18))   # adds a Label above the entry to let people know what the programm expects
                label.grid(column=1, row=1, padx="20", pady="50")

                # Lable which tells the user that new categories were found 
                self.label = tk.Label(self.root, text="We found following new categories:", font=('Arial',11))   # adds a Label so people know what the programm expects
                self.label.grid(column=1, row=2, padx="10", pady="10")

                # IF-Bdeingung --> Label area where the new categories are shown with checkboxes
                self.check_state_1 = tk.IntVar()
                self.check_1 = tk.Checkbutton(self.root, text="[Has to be named automatically]", font=('Arial',10), variable=self.check_state_1)
                self.check_1.grid(column=1, row=3, padx="5", pady="5", sticky=tk.W)

                # Lable which asks you if you want to add the categories and keywords to the excel file
                self.label = tk.Label(self.root, text="Do you want to add the new categories?", font=('Arial',11))   # adds a Label so people know what the programm expects
                self.label.grid(column=1, row=4, padx="10", pady="10")

                # button for NOT adding the new categories to the excel /transfer the data
                self.button_dont = tk.Button(self.root, text="No", relief="groove", font=('Arial',11), bg="lightgrey", command=self.quit)  # if you klick on the button the funktion transfer data will be passed and called whenever the button is klicked
                self.button_dont.grid(column=1, row=5, padx="10",sticky=tk.W, pady="50")

                # button for adding the new categories to the excel /transfer the data
                self.button_do = tk.Button(self.root, text="Yes", relief="groove", font=('Arial',11), bg="lightgrey", command=self.transfer_categories)  # if you klick on the button the funktion transfer data will be passed and called whenever the button is klicked
                self.button_do.grid(column=1, row=5, padx="10",sticky=tk.E, pady="50")

        
                self.root.mainloop()


        def quit(self):
                self.root.destroy()


        def transfer_categories(self, found_categories):
                return found_categories # change this, the method only returns the categories that the user selects


        # this class needs to be callable with a list of categories
        # Let the user decide which categories he wants
        # return the modified list


GUI_config_categories()

