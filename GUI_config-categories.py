import tkinter as tk

class GUI_Categories:   # definition of the class
        def __init__(self):
                self.root = tk.Tk()
                self.root.resizable(0,0)    # Window is not ajustabl
                self.root.geometry("680x450")
                self.root.title("Categories-Configurator")

                # Headline
                label = tk.Label(self.root, text="Categories Custom-Settings", font=('Arial', 18))   # adds a Label above the entry to let people know what the programm expects
                label.grid(column=1, row=1, padx="20", pady="50")

                # Lable which tells the user that new categories were found 
                self.label = tk.Label(self.root, text="We found following new categories:", font=('Arial',11))   # adds a Label so people know what the programm expects
                self.label.grid(column=1, row=2, padx="10", pady="10")

                # button for NOT adding the new categories to the excel /transfer the data
                self.button_dont = tk.Button(self.root, text="No", font=('Arial',11), bg="lightgrey", command=self.quit)  # if you klick on the button the funktion transfer data will be passed and called whenever the button is klicked
                self.button_dont.grid(column=0, row=6, padx="10",sticky=tk.E, pady="50")

                # button for adding the new categories to the excel /transfer the data
                self.button_do = tk.Button(self.root, text="Yes", font=('Arial',11), bg="lightgrey", command=self.transfer_categories)  # if you klick on the button the funktion transfer data will be passed and called whenever the button is klicked
                self.button_do.grid(column=2, row=6, padx="10",sticky=tk.E, pady="50")

               
                        
        
                self.root.mainloop()

        def quit(self):
                self.root.destroy()


        def transfer_categories(self):
                pass


GUI_Categories()

