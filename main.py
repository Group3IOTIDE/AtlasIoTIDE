import tkinter as tk
from initpage import InitPage
from startpage import StartPage
from things import Things
from recipe import Recipe

LARGE_FONT= ("Verdana", 12)

class Main(tk.Tk):

    def __init__(self, *args, **kwargs):
        print("1")
        tk.Tk.__init__(self, *args, **kwargs)
        self.geometry('%dx%d' % (800, 500))
        self.container = tk.Frame(self)
        self.container.pack(side="top", fill="both", expand = True)

        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        #start with StartPage
        #self.show_frame(StartPage)
        self.show_frame(InitPage)

    #show new frame
    def show_frame(self, cont):
        for F in (InitPage, StartPage, Things, Recipe):
            frame = F(self.container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        frame = self.frames[cont]
        frame.tkraise()

app = Main()
app.mainloop()