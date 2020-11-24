import tkinter as tk
import os

LARGE_FONT= ("Verdana", 12)
class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        print("StartPage")
        from things import Things
        from recipe import Recipe
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Start Page", font=LARGE_FONT)
        label.pack(pady=10,padx=10)

        button1 = tk.Button(self, text="Things",
                            command=lambda: controller.show_frame(Things))
        button1.pack(pady=10)
        button2 = tk.Button(self, text="Services",
                            command=lambda:os.system("python services.py"))
        button2.pack(pady=10)
        button3 = tk.Button(self, text="Relationship",
                            command=lambda:os.system("python Relationship.py"))
        button3.pack(pady=10)
        button4 = tk.Button(self, text="Recipe",
                            command=lambda: controller.show_frame(Recipe))
        button4.pack(pady=10)
        button5 = tk.Button(self, text="Apps",
                             command=lambda:os.system("python App.py"))
        button5.pack(pady=10)
        button6 = tk.Button(self, text="Quit",
                            command=self.quit)
        button6.pack(pady=10)