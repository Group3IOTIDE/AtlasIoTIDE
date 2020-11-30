import collections
from tkinter import *
from tkinter import ttk, scrolledtext
from tkinter import filedialog
from tkinter import messagebox
from PIL import Image
import os
import csv
from itertools import islice
import socket
import shutil
import time
import datetime
import pandas as pd
import threading

work_directory = './work'
mode = 0
appname_log=collections.defaultdict(list)

class Application(Tk):
    def __init__(self):
        Tk.__init__(self)
        self.title("App Manager [Normal Mode]")

        self.flag = 1

        self.menu = Menu(self)
        self['menu']=self.menu
        self.menu.add_command(label = 'Change Mode', command = self.change_mode)
        self.b_save = ttk.Button(self, text="save", command = self.save)
        self.b_save.pack(expand=1)
        self.b_upload = ttk.Button(self, text="upload", command=self.upload)
        self.b_upload.pack(expand=1)
        self.b_activate = ttk.Button(self, text="activate", command=self.activate)
        self.b_activate.pack(expand=1)
        self.b_status = ttk.Button(self, text="Status Panel", command=self.Status)
        self.b_status.pack(expand=1)
        self.b_delete = ttk.Button(self, text="delete", command=self.delete)
        self.b_delete.pack(expand=1)

    def change_mode(self):
        global mode
        if mode == 0:
            mode = 1
            self.title("App Manager [Developement Mode]")
        else:
            mode = 0
            self.title("App Manager [Normal Mode]")
        print(mode)

    def save(self):
        #自定文件名并在指定目录保存，返回不带后缀的绝对路径
        if mode == 0:
            messagebox.showwarning('Denied', 'Save only valid under developement mode!' )
        else:
            spath = filedialog.asksaveasfilename(title='save', filetypes=[("TXT", ".txt")], initialdir = work_directory)
            if spath != '':
                spath1 = os.path.splitext(spath)
                filename = os.path.split(spath1[0])
                print(filename[1])
                #加上后缀的完整绝对路径
                full_path = spath + '.txt'

                #读取recipe生成的文件并更改content的内容
                f = open("finalize_app.txt", 'r')
                lines_file = f.readlines()
                services = lines_file[0][:-1].split(',')
                f.close()
                with open("service.csv", 'r') as csvfile:
                    reader = csv.reader(csvfile)
                    ser_rows = [row for row in reader]

                single_service = []
                single_service_tweet = []
                '''for row in ser_rows:
                    if row[0] in services:
                        single_service += [row[0]]
                        tweet = "{ \"Tweet Type\" : \"Service call\",\"Thing ID\" : \"" + row[1] + "\",\"Space ID\" : \"Group3SmartSpace\",\"Service Name\" : \"" + row[0] + "\",\"Service Inputs\" : \"()\" }"
                        single_service_tweet += [tweet]'''
                for service in services:
                    for row in ser_rows:
                        if service == row[0]:
                            single_service += [row[0]]
                            tweet = "{ \"Tweet Type\" : \"Service call\",\"Thing ID\" : \"" + row[1] + "\",\"Space ID\" : \"Group3SmartSpace\",\"Service Name\" : \"" + row[0] + "\",\"Service Inputs\" : \"()\" }"
                            single_service_tweet += [tweet]
                            break
        
                content = ''
                for i in range(len(single_service)):
                    content += single_service[i] + ',' + single_service_tweet[i] + '\n'

                file = open(full_path, 'w')
                #写入Recipe中生成的tweet，这里的content我测试是定义在文件顶部的那个全局变量，你们整合的话需要改成读Recipe的结果
                file.write(content)
                file.close()
                #生成空白图标，把app名、文件路径、图标路径写入csv
                currentpath = os.getcwd()
                #img = Image.new('RGB', (100, 100), (0, 0, 0))
                img = Image.open('./image/RGG.png').copy()
                img.save('./image/' + filename[1] + '.png')
                with open('./App.csv', mode='a',newline='') as cfa:
                    wf = csv.writer(cfa)
                    data = [[filename[1], full_path, currentpath + '\image\\' + filename[1] + '.png']]
                    for i in data:
                        wf.writerow(i)
                with open('./Status.csv', mode='a',newline='') as sta:
                    wf = csv.writer(sta)
                    data = [[filename[1], 'inactive', '', '']]
                    for i in data:
                        wf.writerow(i)

    def upload(self):
        #选择文件并返回文件的绝对路径
        upath = filedialog.askopenfilename(title='upload', filetypes=[("TXT", ".txt")], initialdir = work_directory)
        if upath != '':
        #对绝对路径进行分离以提取文件名字
            uname1 = os.path.splitext(upath)
            uname2 = os.path.split(uname1[0])
            print(uname2[1])

            currentpath = os.getcwd()
            #img = Image.new('RGB', (100, 100), (0, 0, 0))
            img = Image.open('./image/RGG.png').copy()
            img.save('./image/' + uname2[1] + '.png')
            with open(r'./App.csv', mode='a',newline='') as cfa:
                wf = csv.writer(cfa)
                data = [[uname2[1], upath, currentpath + '\image\\' + uname2[1] + '.png']]
                for i in data:
                    wf.writerow(i)
            with open('./Status.csv', mode='a', newline='') as sta:
                wf = csv.writer(sta)
                data = [[uname2[1], 'inactive', '', '']]
                for i in data:
                    wf.writerow(i)

    def activate(self):
        act = Toplevel()
        act.title("activate")
        act.geometry('400x300')

        csv_file = open('./App.csv')  # 打开csv文件
        csv_reader_lines = csv.reader(csv_file)  # 逐行读取csv文件
        data = []  # 创建列表准备接收csv各行数据
        for one_line in islice(csv_reader_lines, 1, None):
            data.append(one_line[0])
        actlist = Listbox(act, width = 50)
        for item in data:
            actlist.insert("end", item)
        actlist.pack()
        csv_file.close()

        def Run():
            active_service = []
            index = actlist.get(actlist.curselection())#获取当前选中项内容
            run_file = open('./App.csv')  # 打开csv文件
            comparefile = csv.reader(run_file)  # 逐行读取csv文件
            for name in islice(comparefile, 1, None):
                if name[0] == index:
                    path = name[1]
                    print(path)
                    break
            run_file.close()
            '''with open(path, "r") as f:
                tweet = f.read()
                print(tweet)'''
            for line in open(path, 'r'):
                active_service += [line.split(',')[0]]
            df = pd.read_csv('./Status.csv')
            df.loc[df['AppName'] == index, 'Status'] = 'active'
            df.loc[df['AppName'] == index, 'Date'] = time.strftime('%Y-%m-%d')
            df.loc[df['AppName'] == index, 'Time'] = time.strftime('%H:%M:%S')
            df.to_csv('./Status.csv', index=False)
            self.manual = 0
            for service in active_service:
                if self.flag == 1:
                    self.send_tweet(service)
                    appname_log[index].append(str(service) + " is running")  # 有新的服务正在运行
                    time.sleep(20)
                    self.manual = 2
                else:
                    df1 = pd.read_csv('./Status.csv')
                    df1.loc[df1['AppName'] == index, 'Status'] = 'inactive'
                    df1.loc[df1['AppName'] == index, 'Stop'] = time.strftime('%H:%M:%S')
                    df1.to_csv('./Status.csv', index=False)
                    self.flag = 1
                    self.manual = 1
                    break
            appname_log[index].append(str(index) + " has stopped")  # app 已经停止
            if self.manual == 2:
                df2 = pd.read_csv('./Status.csv')
                df2.loc[df2['AppName'] == index, 'Status'] = 'Completed'
                df2.loc[df2['AppName'] == index, 'Stop'] = time.strftime('%H:%M:%S')
                df2.to_csv('./Status.csv', index=False)
        Button(act, text="Run!", command= lambda: threading.Thread(target=Run).start()).pack()

    def Status(self):
        status = Toplevel()
        status.title("status")
        status.geometry('600x400')

        def process():
            statu_file = open('./Status.csv')  # 打开csv文件
            sfile = csv.reader(statu_file)  # 逐行读取csv文件
            cnt = 1

            def log(s, n):
                if s != "active":
                    pass
                else:
                    def show_msg(count=None):
                        if count is not None:
                            if count <= 1000:
                                txt = str(appname_log[n][-1]) + "\n"
                                textw.insert('end', txt)
                                count += 1
                                top2.after(5432, lambda: show_msg(count))
                        else:
                            show_msg(1)

                    top2 = Toplevel(status)
                    textw = scrolledtext.ScrolledText(top2, width=40, height=25)
                    textw.grid(column=0, row=1, sticky='nsew')
                    textw.config(background='light grey', foreground='black', font='arial 20 bold', wrap='word',
                                 relief='sunken', bd=5)
                    top2.after(1, lambda: show_msg())
                    top2.focus_set()
                    top2.grab_set()

            for rows in islice(sfile, 1, None):
                if rows[1] == 'active':
                    Button(status, text=rows[0], command=lambda: log(rows[1], rows[0])).place(x=30, y=cnt * 50)
                    Label(status, text='status: ' + rows[1]).place(x=120, y=cnt * 50)
                    Label(status, text='start time: ' + rows[2] + ' ' + rows[3]).place(x=220, y=cnt * 50)
                    cnt = cnt + 1
                elif rows[4] != '':
                    current1 = time.strftime('%H:%M:%S')
                    current2 = datetime.datetime.strptime(current1, '%H:%M:%S')
                    print(current2)
                    stopt = datetime.datetime.strptime(rows[4], '%H:%M:%S')
                    delta = current2 - stopt
                    print(delta.seconds)
                    if delta.seconds >= 0 and delta.seconds < 300:
                        Button(status, text = rows[0], command = lambda: log(rows[1], rows[0])).place(x = 30, y = cnt*50)
                        Label(status, text = 'status: ' + rows[1]).place(x = 120, y = cnt*50)
                        Label(status, text='start time: ' + rows[2] +' ' + rows[3]).place(x=220, y=cnt * 50)
                        cnt = cnt + 1
                    else:
                        Button(status, text = rows[0], command = lambda: log(rows[1], rows[0])).place(x = 30, y = cnt*50)
                        Label(status, text='status: removed').place(x=120, y=cnt * 50)
            statu_file.close()

            def Stop():
                stop = Toplevel()
                stop.title("Stop")
                stop.geometry('400x300')

                csv_file = open('./Status.csv')  # 打开csv文件
                csv_reader_lines = csv.reader(csv_file)  # 逐行读取csv文件
                data = []  # 创建列表准备接收csv各行数据
                for one_line in islice(csv_reader_lines, 1, None):
                    if one_line[1] == 'active':
                        data.append(one_line[0])
                stoplist = Listbox(stop, width=50)
                for item in data:
                    stoplist.insert("end", item)
                stoplist.pack()
                csv_file.close()

                def Ok():
                    index = stoplist.get(stoplist.curselection())  # 获取当前选中项名字
                    self.flag = 0
                    df = pd.read_csv('./Status.csv')
                    df.loc[df['AppName'] == index, 'Status'] = 'inactive'
                    df.loc[df['AppName'] == index, 'Stop'] = time.strftime('%H:%M:%S')
                    df.to_csv('./Status.csv', index=False)
                Button(stop, text="Ok!", command=lambda: Ok()).pack()

            Button(status, text="Stop", command=lambda: Stop()).place(x = 285, y = 10)
            status.after(20000,process)
        process()

    def delete(self):
        #同upload，选择文件并得到文件名字和路径
        dpath = filedialog.askopenfilename(title='upload', filetypes=[("TXT", ".txt")], initialdir=work_directory)
        if dpath != '':
            dname1 = os.path.splitext(dpath)
            dname2 = os.path.split(dname1[0])
            print(dname2[1])
            #删除本地app文件
            os.remove(dpath)
            os.remove('./image/' + dname2[1] + '.png')

            file_old = './App.csv'
            file_temp = './temp.csv'
            with open(file_old, 'r', newline='', encoding='gbk') as f_old, open(file_temp, 'w', newline='', encoding='gbk') as f_temp:
                f_csv_old = csv.reader(f_old)
                f_csv_temp = csv.writer(f_temp)
                for i, rows in enumerate(f_csv_old):  # 保留header
                    if i == 0:
                        f_csv_temp.writerow(rows)
                        break
                for rows in f_csv_old:
                    if rows[0] != dname2[1]:  # 删除第一列值为指定文件名的行
                        f_csv_temp.writerow(rows)
            os.remove(file_old)
            os.rename(file_temp, file_old)

    def send_tweet(self, serviceid):
        with open("service.csv", 'r') as csvfile:
            reader = csv.reader(csvfile)
            ser_rows = [row for row in reader]
        
        for row in ser_rows:
            if row[0] == serviceid:
                tweet = "{ \"Tweet Type\" : \"Service call\",\"Thing ID\" : \"" + row[1] + "\",\"Space ID\" : \"Group3SmartSpace\",\"Service Name\" : \"" + row[0] + "\",\"Service Inputs\" : \"()\" }"
                thingid = row[1]
                break
        
        with open("thing.csv", 'r') as csvfile:
            reader = csv.reader(csvfile)
            thing_rows = [row for row in reader]
        
        for row in thing_rows:
            if row[0] == thingid:
                ip = row[1]
                break

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((ip, 6668))
        sock.send(tweet.encode())
        sock.close()

#退出时启动App tab使其重新构造完成显示刷新
def back():
    root.destroy()
    os.system("python App.py")

root = Application()
root.geometry('400x300')
root.protocol("WM_DELETE_WINDOW", back)
root.mainloop()