from tkinter import *
from tkinter.ttk import *
from tkinter import ttk
import  csv
from PIL import Image, ImageTk
import collections
import tkinter.messagebox
class Services(Frame):
    def __init__(self, parent,rows):
        Frame.__init__(self, parent)
        self.CreateUI()
        self.LoadTable(rows)
        self.grid(sticky = (N,S,W,E))
        parent.grid_rowconfigure(0, weight = 1)
        parent.grid_columnconfigure(0, weight = 1)
        style = Style(parent)
        style.configure('Treeview', rowheight=100)

    def CreateUI(self):
        tv = Treeview(self)
        tv['columns'] = ('Device Num', 'endtime')
        tv.heading("#0", text='Service Name', anchor='w')
        tv.column("#0", anchor="w")
        tv.heading('Device Num', text='Thing ID')
        tv.column('Device Num', anchor='center', width=100)
        tv.grid(sticky = (N,S,W,E))
        self.treeview = tv
        self.grid_rowconfigure(0, weight = 1)
        self.grid_columnconfigure(0, weight = 1)

    def LoadTable(self,details):
        global image, image_dict
        garbage = []
        cnt=0
        cnt_image = 0
        for d in details:
            cnt_image += 1
            if d not in image_dict:
                image.append(ImageTk.PhotoImage(Image.open("./image/"+str(cnt_image)+".jpg").resize((50, 50), Image.ANTIALIAS)))
                image_dict[d] = image[cnt_image-1]
            for element in details[d]:
                #image.append(ImageTk.PhotoImage(Image.open("./image/"+str(cnt_image+1)+".png").resize((50, 50), Image.ANTIALIAS)))
                self.treeview.insert('', 'end', text=str(element[0]), values=(d))
                self.treeview.insert('', 'end', image=image_dict[d])
                label = Label()
                label.image = image_dict[d]
                garbage += [label]
                cnt+=1


def filter(*args):
    global key
    global key1
    global mainapp2
    global mainapp
    global comboxlist
    global comboxlist2
    global comboxlist1
    if comboxlist:
        key = comboxlist.get()
        if key != 'default':
            if mainapp:
                mainapp.destroy()
            if mainapp2:
                mainapp2.destroy()
            #key = comboxlist.get()
            #if key != 'default':
            buffer={}
            buffer[key]=buffer.get(key,[])+id_detail[key]
            mainapp2=Services(root, buffer)
            comboxlist = ttk.Combobox(root)
            comboxlist["values"] = ["default"] + id
            comboxlist.current(0)
            comboxlist.place(relx = 0.640, rely = 0.001)
            comboxlist.bind("<<ComboboxSelected>>", filter)
        else:
            tkinter.messagebox.showinfo('Error','Please select an appropiate item!')


root = Tk()
with open('service.csv', 'r') as csvfile:
    reader = csv.reader(csvfile)
    rows = [row for row in reader]
id_detail=collections.defaultdict(list)
for r in rows:
    id_detail[r[1]].append([r[0]])
id = list(set([row[1] for row in rows]))
image = []
image_dict = {}
key=None
key1=None
mainapp2=None
mainapp=None
comboxlist1=None
comboxlist=None
mainapp=Services(root,id_detail)
comboxlist = ttk.Combobox(root)
comboxlist["values"] = ["default"]+id
comboxlist.current(0)
comboxlist.place(relx = 0.640, rely = 0.001)
comboxlist.bind("<<ComboboxSelected>>",filter)
root.mainloop()
