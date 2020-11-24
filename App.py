import tkinter
from tkinter import *
import PIL.Image, PIL.ImageTk
import csv
import os

def AppManager():
    window.destroy()
    os.system("python AppManager.py")

window = tkinter.Tk()
window.geometry("500x500")

frame = tkinter.Frame(window, bd=2)
frame.grid_rowconfigure(0, weight=1)
frame.grid_columnconfigure(0, weight=1)

xscrollbar = tkinter.Scrollbar(frame, orient=tkinter.HORIZONTAL)
xscrollbar.grid(row=1, column=0, sticky=tkinter.E+tkinter.W)
yscrollbar = tkinter.Scrollbar(frame)
yscrollbar.grid(row=0, column=1, sticky=tkinter.N+tkinter.S)
canvas = tkinter.Canvas(frame, bd=0, xscrollcommand=xscrollbar.set, yscrollcommand=yscrollbar.set)
canvas.grid(row=0, column=0, sticky=tkinter.N + tkinter.S + tkinter.E + tkinter.W)
canvas.config(scrollregion=canvas.bbox(tkinter.ALL))

with open('App.csv', 'r') as csvfile:
    reader = csv.reader(csvfile)
    next(reader, None)
    rows = [row for row in reader]
cnt=0
names=[0 for i in range(len(rows))]
for i in range(len(rows)):
    names[i]="img"+str(i)
while cnt<len(rows):
    names[cnt] = PIL.ImageTk.PhotoImage(PIL.Image.open(rows[cnt][2]).resize((100, 100)))
    print(names[cnt])
    canvas.create_image(200,cnt*100,image=names[cnt], anchor="nw")
    canvas.create_text(100,cnt*100+50,text=rows[cnt][0])
    cnt+=1

canvas.config(scrollregion=canvas.bbox(tkinter.ALL))
canvas.config(width=500,height=500)
xscrollbar.config(command=canvas.xview)
yscrollbar.config(command=canvas.yview)
button_M = Button(canvas, text="APP manager", command = lambda: AppManager())
button_M.place(relx=0.75,rely=0.5)
frame.pack()

window.mainloop()