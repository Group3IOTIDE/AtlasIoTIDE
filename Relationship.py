from tkinter import *
import pandas as pd
from tkinter import ttk
import csv

class Application(Tk):
    def __init__(self):
        Tk.__init__(self)
        self.title("Relationships")

        df = pd.DataFrame(pd.read_csv('relationship.csv'))
        columns = list(df.columns)
        self.tree = ttk.Treeview(self)
        self.combo = ttk.Combobox(self, postcommand = self.refresh, state="readonly")
        self.combo.pack()
        self.combo.bind("<<ComboboxSelected>>", self.filter_Type)
        self.tree["columns"] = columns
        self.tree.pack(expand=TRUE, fill=BOTH)

        for i in columns:
            self.tree.column(i, anchor="w")
            self.tree.heading(i, text=i, anchor="w")

        for index, row in df.iterrows():
            self.tree.insert("", "end", text=index, values=list(row))

        self.VScroll1 = Scrollbar(self, orient='vertical', command=self.tree.yview)
        self.VScroll1.place(relx=0.971, rely=0.028, relwidth=0.024, relheight=0.958)
        self.VScroll2 = Scrollbar(self, orient='horizontal', command=self.tree.xview)
        self.VScroll2.place(relx=0.028, rely=0.971, relwidth=0.958, relheight=0.024)
        #add configuration to treeview
        self.tree.configure(yscrollcommand=self.VScroll1.set)
        self.tree.configure(xscrollcommand=self.VScroll2.set)

        self.tree.bind('<Double-1>', func = self.set_cell_value)
        self.create = ttk.Button(self, text="Create New Relationship", command=self.newrow)
        self.create.pack(expand = 1)

    def refresh(self):
        df = pd.DataFrame(pd.read_csv('Relationship.csv'))
        self.combo['values'] = [""] + list(df["Type"].unique())

    def set_cell_value(self,event):
        for item in self.tree.selection():
            item_text = self.tree.item(item, "values")
        column = self.tree.identify_column(event.x)  #colum
        entryedit = Text(root, width=10, height=1)
        entryedit.place(x=220, y=300)
        def saveedit():
            self.tree.set(item, column=column, value=entryedit.get(0.0, "end"))
            entryedit.destroy()
            okb.destroy()
            self.save_csv()
        okb = ttk.Button(root, text='OK', width=4, command=saveedit)
        okb.place(x=300, y=290)

    def newrow(self):
        df = pd.DataFrame(pd.read_csv('relationship.csv'))
        rows = len(list(df.index))
        self.tree.insert('', "end",text=rows, values=['nah','nah','nah','nah'])
        self.tree.update()

    def filter_Type(self,event=None):
        df = pd.DataFrame(pd.read_csv('relationship.csv'))
        self.tree.delete(*self.tree.get_children())
        cnt = 0
        for index, row in df.loc[df["Type"].eq(self.combo.get())].iterrows():
            self.tree.insert("", "end", text=index, values=list(row))
            cnt = cnt +1
        if cnt == 0:
            for index, row in df.iterrows():
                self.tree.insert("", "end", text=index, values=list(row))

    def save_csv(self):
        with open("relationship.csv", "w", newline='') as myfile:
            csvwriter = csv.writer(myfile, delimiter=',')
            csvwriter.writerow(['Name','Type','Service1','Service2'])

            for row_id in self.tree.get_children():
                row = self.tree.item(row_id)['values']
                print('save row:', row)
                csvwriter.writerow(row)

root = Application()
root.geometry('600x400')
root.mainloop()