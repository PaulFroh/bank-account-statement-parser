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
                
                self.root.mainloop()


GUI_Categories()

