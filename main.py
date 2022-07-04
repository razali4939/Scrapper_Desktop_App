import codecs

from selenium import webdriver
from bs4 import BeautifulSoup
import tkinter as tk
from  tkinter import  ttk, filedialog
from tkinter import messagebox as MessageBox
import os
import csv
import mysql.connector as mysql
import numpy as np
import pandas as pd

def scrap():
    web_link = e_link.get()
    print(web_link)
    options = webdriver.ChromeOptions()
    options.add_argument('--headles')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')

    #print(web_link)
    site = web_link #'https://www.ebay.com/itm/353672691115'

    wd = webdriver.Chrome('C:/Program Files/Google/Chrome/Application/chromedriver', options=options)
    wd.get(site)

    html = wd.page_source

    soup = BeautifulSoup(html, 'html.parser')
    tables = soup.find_all(id="w1-29ctbl")

    data = []

    con = mysql.connect(host='localhost', user='root', password='', database='scrap')
    cursor = con.cursor()

    for t in tables:
        rows = t.find_all('tr')
        for row in rows:
            records = row.find_all('td')
            for i in range(len(records)):
                if records[i] != None:
                    print("")
                    data.append(records[i].text)
                    #print("Column is ended")
                    #print(data)
            if len(data) !=0:

                cursor.execute(
                    "insert into vehicles values('" + data[0] + "', '" + data[1] + "', '" + data[2] + "', '" + data[3] + "', '" + data[4] + "', '" + data[5] + "') ")
                cursor.execute("commit");
                print(len(data))
                data = []
                #print("List reset")
    con.close();
    #MessageBox.showinfo("Data Saved", "Data Saved Successfully");

def ImportFun():
    file_data = []
    fln = filedialog.askopenfilename(initialdir=os.getcwd(), title='Open csv', filetypes=(("xlsx File", "*.xlsx"), ("All File", "*.*")))

    #c1, c2, c3, c4, c5, c6, c6, c8, c9, c10 = np.loadtxt(fln, unpack=True, delimiter=',')
    data = pd.read_csv(fln, encoding='utf-8')
    print(data)
    #with open(fln, encoding="cp437") as myfile:
    #csvread = csv.reader(codecs.open(fln, 'rU', 'utf-16-be'), delimiter=",")
    #for i in csvread:
       # file_data.append(i)
       # print(i)


root = tk.Tk()
root.geometry("1500x1000")
root.title("Scraper App")

link = tk.Label(root, text='Link of Website', font=('bold, 15'))
link.place(x=30, y=30)


e_link = tk.Entry()
e_link.place(x=200, y=30)


#canvas = tk.Canvas(root, height=700, width=700, bg="#263D42")
#canvas.pack()
#frame = tk.Frame(root, bg="white")
#frame.place(relheight=0.8, relwidth=0.8, relx=0.1, rely=0.1)

openFileBtn = tk.Button(root, text="Scrap Data", fg="white", bg="green", command=scrap)
openFileBtn.place(x=150, y=70)

saveBtn = tk.Button(root, text="Save File", fg="white", bg="green", command=ImportFun)
saveBtn.place(x=270, y=70)

tv1_label = tk.Label(root, text='Scraped Data', font=('bold, 10'))
tv1_label.place(x=30, y=105)

tv = ttk.Treeview(root)
tv.place(x=30, y=130)
tv['show'] = 'headings'


tv["columns"] = ("note", "year", "make", "model", "trim", "engine")

tv.column("note", width=300, minwidth=300, anchor=tk.CENTER)
tv.column("year", width=50, minwidth=50, anchor=tk.CENTER)
tv.column("make", width=50, minwidth=50, anchor=tk.CENTER)
tv.column("model", width=50, minwidth=50, anchor=tk.CENTER)
tv.column("trim", width=150, minwidth=150, anchor=tk.CENTER)
tv.column("engine", width=300, minwidth=300, anchor=tk.CENTER)

tv.heading("note", text= "Notes")
tv.heading("year", text= "Year")
tv.heading("make", text= "Make")
tv.heading("model", text= "Model")
tv.heading("trim", text= "Trim")
tv.heading("engine", text= "Engine")

con = mysql.connect(host='localhost', user='root', password='', database='scrap')
cursor = con.cursor()
cursor.execute("SELECT * FROM vehicles")
i=0
for ro in cursor:
    tv.insert('', i, text="", values = (ro[0], ro[1], ro[2], ro[3], ro[4], ro[5]))
    i = i+1
hsb = ttk.Scrollbar(root, orient= "horizontal")
hsb.configure(command=tv.xview)
tv.configure(xscrollcommand=hsb.set)

tv2_label = tk.Label(root, text='Old Data', font=('bold, 10'))
tv2_label.place(x=30, y=375)

tv2 = ttk.Treeview(root)
tv2.place(x=30, y=400)
tv2['show'] = 'headings'


tv2["columns"] = ("note", "year", "make", "model", "trim", "engine")

tv2.column("note", width=300, minwidth=300, anchor=tk.CENTER)
tv2.column("year", width=50, minwidth=50, anchor=tk.CENTER)
tv2.column("make", width=50, minwidth=50, anchor=tk.CENTER)
tv2.column("model", width=50, minwidth=50, anchor=tk.CENTER)
tv2.column("trim", width=150, minwidth=150, anchor=tk.CENTER)
tv2.column("engine", width=300, minwidth=300, anchor=tk.CENTER)

tv2.heading("note", text= "Notes")
tv2.heading("year", text= "Year")
tv2.heading("make", text= "Make")
tv2.heading("model", text= "Model")
tv2.heading("trim", text= "Trim")
tv2.heading("engine", text= "Engine")

con = mysql.connect(host='localhost', user='root', password='', database='scrap')
cursor = con.cursor()
cursor.execute("SELECT * FROM vehicles")
i=0
for ro in cursor:
    tv2.insert('', i, text="", values = (ro[0], ro[1], ro[2], ro[3], ro[4], ro[5]))
    i = i+1
hsb = ttk.Scrollbar(root, orient= "horizontal")
hsb.configure(command=tv.xview)
tv2.configure(xscrollcommand=hsb.set)


root.mainloop()


