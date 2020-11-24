from tkinter import *
import tkinter.ttk as ttk
from PIL import ImageTk, Image
import csv

LARGE_FONT = ("Verdana", 12)

class Things(Frame):
    def __init__(self, parent, controller):
        from startpage import StartPage
        Frame.__init__(self, parent)

        #self.SortDir = True
        #set title of columns
        self.dataCols = ('Smart Space Thing Name','Thing IP Address')
        self.tree = ttk.Treeview(self, columns=self.dataCols, height = 5)
        self.tree.grid(row=0, column=0, sticky=NSEW)

        # Setup column heading
        self.tree.heading('#0', text='Pic', anchor='center')
        self.tree.heading('#1', text='Smart Space Thing Name', anchor='center')
        self.tree.heading('#2', text='Thing IP Address', anchor='center')
        
        style = ttk.Style(self)
        style.configure('Treeview', rowheight=80)
        img = ImageTk.PhotoImage(Image.open("./image/pi.jpg").resize((80,80), Image.ANTIALIAS))
    
        with open('thing.csv','r') as csvfile:
            reader = csv.reader(csvfile)
            rows= [row for row in reader]
        for i in range(len(rows)):
            self.tree.insert('', 'end', image=img, value=(rows[i][0], rows[i][1]))
            self.tree.image = img

        #add back button
        button1 = Button(self, text="Back to Home", command=lambda: controller.show_frame(StartPage))
        button1.place(x=650, y=400)
