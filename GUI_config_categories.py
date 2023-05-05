import tkinter as tk
import excel_helper

class GUI_config_categories:   # definition of the class
        def __init__(self, found_categories, path_excel):
                self.found_categories = found_categories

                self.root = tk.Tk()
                #self.root.resizable(0,0)    # Window is not ajustabl
                self.root.geometry("800x550")
                self.root.resizable(width=0, height=0)
                self.root.title("Categories-Configurator")

                # Create a Grid-Layout for the window
                for i in range(3):
                        for j in range(1):
                                tk.Label(self.root).grid(row=i, column=j)

                # Create a frame for the top of the window
                self.frame_headline = tk.Frame(self.root, width = 800, height = 200, background = "#e68d00")
                # Create a Grid-Layout for this specific frame
                for i in range(3):
                        for j in range(3):
                                tk.Label(self.frame_headline).grid(row=i, column=j)
                self.frame_headline.grid(row = 0, column = 1)




                # Create a frame for the middle of the window
                self.frame_checkboxes = tk.Frame(self.root, width = 800, height = 100, background = "#ffc600")
                # Create a Grid-Layout for this specific frame
                for i in range(10):
                        for j in range(10):
                                tk.Label(self.root).grid(row=i, column=j)
                self.frame_checkboxes.grid(row = 1, column = 1)




                # Create a frame for the bottom of the window
                self.frame_buttons = tk.Frame(self.root, width = 800, height = 100, background = "#e68d00")
                # Create a Grid-Layout for this specific frame
                for i in range(10):
                        for j in range(10):
                                tk.Label(self.root).grid(row=i, column=j)
                self.frame_buttons.grid(row = 2, column = 1)

                # Headline
                self.label_headline = tk.Label(self.frame_headline, text="Categories Custom-Settings", justify='center', font=('Arial', 18))   # adds a Label above the entry to let people know what the programm expects
                self.label_headline.grid(column=5, row=0, padx="20", pady="50")

                # Lable which tells the user that new categories were found 
                self.label_new = tk.Label( self.frame_headline, text="We found following new categories:", font=('Arial',11))   # adds a Label so people know what the programm expects
                self.label_new.grid(column=5, row=1, padx="10", pady="10")

                # FOR-LOOP --> Label area where the new categories are shown with checkboxes
                
                keyword_checkboxes = {}
                index_category = 0
                for category in found_categories:
                        
                        check_state = tk.IntVar()
                        self.check = tk.Checkbutton(self.frame_checkboxes, text=category, font=('Arial',10, 'bold'), variable=check_state)
                        self.check.grid(column=[index_category], row=[2], padx="5", pady="5", sticky=tk.W)
                        
                        keyword_checkboxes[category] = []
                        
                
                        
                        index_keyword = 0
                        for keyword in found_categories[category]:                                      # creates a label with all elements of the specific sublist
                                
                                check_state = tk.IntVar()
                                self.check = tk.Checkbutton(self.frame_checkboxes, text=keyword, font=('Arial',10), variable=check_state)
                                self.check.grid(column=[index_category], row=[index_keyword+3], padx="5", pady="5", sticky=tk.W)
                                
                                keyword_checkboxes[category].append((keyword, check_state))

                                index_keyword += 1
                        index_category += 1

                # ADD CHECKBOXES TO THE CATEGORIES AND KEYWORDS
                # INDENT THE SUB CATEGORIES
                # CREATE FRAMES FOR DIFFERENT PARTS: ONE FOR THE HEADLINE THE STATEMENT THE QUESTION AND THE BUTTONS AND ANOTHER ONE FOR THE CHECKBOXES AND THE CATEGORIES
                # ADD A CHECKBOX "CHOOSE ALL SUGGESTIONS"

                # Lable which asks you if you want to add the categories and keywords to the excel file
                self.label_transfer = tk.Label(self.frame_buttons, text="Do you want to add the new categories?", font=('Arial',11))   # adds a Label so people know what the programm expects
                self.label_transfer.grid(column=4, row=[80], padx="10", pady="10")




                # BUTTONS

                # button for NOT adding the new categories to the excel /transfer the data
                self.button_dont = tk.Button(self.frame_buttons, text="No", relief="groove", font=('Arial',11), bg="lightgrey", command=self.quit)  # if you klick on the button the funktion transfer data will be passed and called whenever the button is klicked
                self.button_dont.grid(column=4, row=[81], padx="10",sticky=tk.W, pady="50")

                # button for adding the new categories to the excel /transfer the data
                self.button_do = tk.Button(self.frame_buttons, text="Yes", relief="groove", font=('Arial',11), bg="lightgrey", command=self.transfer_categories)  # if you klick on the button the funktion transfer data will be passed and called whenever the button is klicked
                self.button_do.grid(column=4, row=[81], padx="10",sticky=tk.E, pady="50")

                
                self.root.mainloop()

        

        def quit(self):
                self.root.destroy()


        def transfer_categories(self):
                categories = {}
                excel_helper.export_new_categories(categories)


        # this class needs to be callable with a list of categories
        # Let the user decide which categories he wants
        # return the modified list

