import codecs

from selenium import webdriver
from bs4 import BeautifulSoup
import tkinter as tk
from tkinter import *
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
                    "insert into record values('" + data[0] + "', '" + data[1] + "', '" + data[2] + "', '" + data[3] + "', '" + data[4] + "', '" + data[5] + "') ")
                cursor.execute("commit");
                print(len(data))
                data = []
                #print("List reset")

    cursor.execute("SELECT * FROM record")
    i = 0
    for ro in cursor:
        tv.insert('', i, text="", values=(ro[0], ro[1], ro[2], ro[3], ro[4], ro[5]))
        i = i + 1
    con.close();
    #MessageBox.showinfo("Data Saved", "Data Saved Successfully");

def ImportFun():
    file_data = []
    fln = filedialog.askopenfilename(initialdir=os.getcwd(), title='Open csv', filetypes=(("csv File", "*.csv"), ("All File", "*.*")))
    con = mysql.connect(host='localhost', user='root', password='', database='scrap')
    cursor = con.cursor()
    with open(fln, 'r') as csv_file:
        csv_reader = csv.reader(csv_file)
        for line in csv_reader:
            cursor.execute(
                "insert into vehicles values('" + line[0] + "', '" + line[1] + "', '" + line[2] + "', '" + line[
                    3] + "', '" + line[4] + "', '" + line[5] + "', '" + line[6] + "', '" + line[7] + "') ")
            cursor.execute("commit");
        cursor.execute("SELECT * FROM vehicles")
        i = 0
        for ro in cursor:
            tv2.insert('', i, text="", values=(ro[0], ro[1], ro[2], ro[3], ro[4], ro[5], ro[6], ro[7]))
            i = i + 1
        con.close();

def Filter():
    current_year = year.get()
    current_make = make.get()
    current_model = model.get()
    con = mysql.connect(host='localhost', user='root', password='', database='scrap')
    cursor = con.cursor()
    #cursor.execute("SELECT * FROM vehicles WHERE Year = '"+current_year+"'  ")
    cursor.execute("SELECT * FROM record where Year='"+current_year+"' AND Make = '"+current_make+"' AND Model = '"+current_model+"' ");
    i = 0
    data_write = []
    data_write1 = []
    data_write2 = []
    data_write3 = []
    data_write4 = []
    data_write5 = []
    for ro in cursor:
        data_write.append(ro[0])
        data_write1.append(ro[1])
        data_write2.append(ro[2])
        data_write3.append(ro[3])
        data_write4.append(ro[4])
        data_write5.append(ro[5])
        tv.insert('', i, text="", values=(ro[0], ro[1], ro[2], ro[3], ro[4], ro[5]))
        i = i + 1
    with open('csv_file.csv', 'w', newline='') as csv_file:
        field_names = ['Notes', 'Year', 'Make', 'Model', 'Trim', 'Engine']
        the_writer = csv.DictWriter(csv_file, fieldnames=field_names)
        the_writer.writeheader()
        for (ro,ro1, ro2, ro3, ro4, ro5) in zip(data_write, data_write1, data_write2, data_write3, data_write4, data_write5):
            the_writer.writerow({'Notes': ro, 'Year':ro1, 'Make':ro2, 'Model':ro3, 'Trim':ro4, 'Engine':ro5})
    con.close();

def OldFilter():
    current_year = year1.get()

    current_make = make1.get()

    current_model = model1.get()

    con = mysql.connect(host='localhost', user='root', password='', database='scrap')
    cursor = con.cursor()
    # cursor.execute("SELECT * FROM vehicles WHERE Year = '"+current_year+"'  ")
    cursor.execute(
        "SELECT * FROM vehicles where Year='" + current_year + "' AND Make = '" + current_make + "' AND Model = '" + current_model + "' ");
    i = 0
    data_write = []
    data_write1 = []
    data_write2 = []
    data_write3 = []
    data_write4 = []
    data_write5 = []
    data_write6 = []
    data_write7 = []
    for ro in cursor:
        print(ro[0])
        data_write.append(ro[0])
        data_write1.append(ro[1])
        data_write2.append(ro[2])
        data_write3.append(ro[3])
        data_write4.append(ro[4])
        data_write5.append(ro[5])
        data_write6.append(ro[6])
        data_write7.append(ro[7])
        tv2.insert('', i, text="", values=(ro[0], ro[1], ro[2], ro[3], ro[4], ro[5], ro[6], ro[7]))
        i = i + 1
    with open('csv_file1995.csv', 'w', newline='') as csv_file:
        field_names = ['SKU', 'Year', 'Make', 'Model', 'Sub Model', 'Front Rotor', 'NO', 'Front Pad']
        the_writer = csv.DictWriter(csv_file, fieldnames=field_names)
        the_writer.writeheader()
        for (ro, ro1, ro2, ro3, ro4, ro5, ro6, ro7) in zip(data_write, data_write1, data_write2, data_write3, data_write4,
                                                 data_write5, data_write6, data_write7):
            the_writer.writerow({'SKU': ro, 'Year': ro1, 'Make': ro2, 'Model': ro3, 'Sub Model': ro4, 'Front Rotor': ro5, 'NO':ro6, 'Front Pad':ro7})
    con.close();


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

option_label = tk.Label(root, text='Filters:', font=('bold, 15'))
option_label.place(x= 430, y=30)
filter_btn = tk.Button(root, text="Fiter", fg="white", bg="green", command=Filter)
filter_btn.place(x=800, y=30)
con = mysql.connect(host='localhost', user='root', password='', database='scrap')
cursor = con.cursor()
cursor.execute("SELECT Year FROM record")
years = []
for y in cursor:
    years.append(y[0])
con.close();
years = list(set(years))
year = StringVar()
if years !=[]:
    year.set(years[0])
else:
    year.set("years")
    years = ['years']
year_menu = OptionMenu(root, year, *years)
year_menu.place(x=500, y=30)
con = mysql.connect(host='localhost', user='root', password='', database='scrap')
cursor = con.cursor()
cursor.execute("SELECT Make FROM record")
makes = []
for mak in cursor:
    makes.append(mak[0])
con.close();
makes = list(set(makes))
make = StringVar()
if makes !=[]:
    make.set(makes[0])
else:
    make.set("make")
    makes = ['makes']
make_menu = tk.OptionMenu(root, make, *makes)
make_menu.place(x=600, y=30)
con = mysql.connect(host='localhost', user='root', password='', database='scrap')
cursor = con.cursor()
cursor.execute("SELECT Model FROM record")
models = []
for m in cursor:
    models.append(m[0])
#models = cursor.fetchall()
con.close();
models = list(set(models))
model = StringVar()
if models !=[]:
    model.set(years[0])
else:
    model.set("model")
    models = ['models']
model_menu = tk.OptionMenu(root, model, *models)
model_menu.place(x=700, y=30)

option_label1 = tk.Label(root, text='Filters:', font=('bold, 15'))
option_label1.place(x= 430, y=400)
filter_btn1 = tk.Button(root, text="Fiter", fg="white", bg="green", command=OldFilter)
filter_btn1.place(x=800, y=400)
con = mysql.connect(host='localhost', user='root', password='', database='scrap')
cursor = con.cursor()
cursor.execute("SELECT Year FROM vehicles")
years = []
for y in cursor:
    years.append(y[0])
con.close();
years = list(set(years))
year1 = StringVar()
if years !=[]:
    year1.set(years[0])
else:
    year1.set("years")
    years = ['years']

year_menu = OptionMenu(root, year1, *years)
year_menu.place(x=500, y=400)
con = mysql.connect(host='localhost', user='root', password='', database='scrap')
cursor = con.cursor()
cursor.execute("SELECT Make FROM vehicles")
makes = []
for mak in cursor:
    makes.append(mak[0])
con.close();
makes = list(set(makes))
make1 = StringVar()
if makes !=[]:
    make1.set(makes[0])
else:
    make1.set("make")
    makes = ['makes']
make_menu = tk.OptionMenu(root, make1, *makes)
make_menu.place(x=600, y=400)
con = mysql.connect(host='localhost', user='root', password='', database='scrap')
cursor = con.cursor()
cursor.execute("SELECT Model FROM vehicles")
models = []
for m in cursor:
    models.append(m[0])
#models = cursor.fetchall()
con.close();
models = list(set(models))
model1 = StringVar()
if models !=[]:
    model1.set(years[0])
else:
    model1.set("model")
    models = ['models']
model_menu = tk.OptionMenu(root, model1, *models)
model_menu.place(x=700, y=400)

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

#con = mysql.connect(host='localhost', user='root', password='', database='scrap')
#cursor = con.cursor()

hsb = ttk.Scrollbar(root, orient= "horizontal")
hsb.configure(command=tv.xview)
tv.configure(xscrollcommand=hsb.set)

tv2_label = tk.Label(root, text='1995 Data', font=('bold, 10'))
tv2_label.place(x=30, y=420)

tv2 = ttk.Treeview(root)
tv2.place(x=30, y=445)
tv2['show'] = 'headings'


tv2["columns"] = ("sku", "year", "make", "model", "submodel", "frontrotor", "no", "frontpad")

tv2.column("sku", width=300, minwidth=300, anchor=tk.CENTER)
tv2.column("year", width=50, minwidth=50, anchor=tk.CENTER)
tv2.column("make", width=50, minwidth=50, anchor=tk.CENTER)
tv2.column("model", width=50, minwidth=50, anchor=tk.CENTER)
tv2.column("submodel", width=150, minwidth=150, anchor=tk.CENTER)
tv2.column("frontrotor", width=300, minwidth=300, anchor=tk.CENTER)
tv2.column("no", width=50, minwidth=50, anchor=tk.CENTER)
tv2.column("frontpad", width=50, minwidth=50, anchor=tk.CENTER)

tv2.heading("sku", text= "SKU#")
tv2.heading("year", text= "Year")
tv2.heading("make", text= "Make")
tv2.heading("model", text= "Model")
tv2.heading("submodel", text= "Sub Model")
tv2.heading("frontrotor", text= "Front Rotor")
tv2.heading("no", text= "NO")
tv2.heading("frontpad", text= "Front Pad")

#con = mysql.connect(host='localhost', user='root', password='', database='scrap')
#cursor = con.cursor()
#cursor.execute("SELECT * FROM vehicles")
#i=0
#for ro in cursor:
    #tv2.insert('', i, text="", values = (ro[0], ro[1], ro[2], ro[3], ro[4], ro[5]))
    #i = i+1
hsb = ttk.Scrollbar(root, orient= "horizontal")
hsb.configure(command=tv.xview)
tv2.configure(xscrollcommand=hsb.set)


root.mainloop()


