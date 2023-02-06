import tkinter as tk
import time
from tkinter import ttk
from tkinter import messagebox
from datetime import datetime
import datetime as dt
import sqlite3
#from PIL import imagetk, image
#import serial
#import arduino.py


#emp_heure_entree = dt.datetime.now()




conn = sqlite3.connect('employee.db')
window = tk.Tk()
window.geometry('1000x700+500+200')
window.title('Gestion de base de données')
window.configure(background='#6A6A6A')
window.resizable(width=False, height=False)
icon = tk.PhotoImage(file="mange.png")
window.call("wm", "iconphoto", window._w, icon)
emp_id, emp_name, emp_age = tk.StringVar(), tk.StringVar(), tk.StringVar()
emp_email, emp_phone, emp_heure_entree = tk.StringVar(), tk.StringVar(), tk.StringVar()
cur = conn.cursor()
cur.execute("""CREATE TABLE IF NOT EXISTS emp_data (
	ID TEXT NOT NULL PRIMARY KEY ,Name TEXT NOT NULL,
	Age TEXT NOT NULL,Email TEXT NOT NULL,
	Phone TEXT NOT NULL,heure_entree TEXT NOT NULL,
	Date_save TEXT NOT NULL)
	""")
cur.close()
def get_ids_list():
    cur = conn.cursor()
    ids_query = "SELECT ID FROM emp_data"
    ids_list = cur.execute(ids_query)
    my_ids = ids_list.fetchall()
    int_ids = [x[0] for x in my_ids]
    return int_ids


emp_ids_list = get_ids_list()


def insertData():
    cur = conn.cursor()
    employee_id = emp_id.get();
    employee_name = emp_name.get()
    employee_age = emp_age.get();
    employee_email = emp_email.get()
    employee_phone = emp_phone.get();
    employee_heure_entree = emp_heure_entree.get()
    date_emp = str(datetime.now().date())

    if employee_id == '' or employee_name == '' or employee_age == '' or employee_email == '' or employee_phone == '' or employee_heure_entree == '':
        messagebox.showwarning('Missed values', 'There are some blank fields please check again')
    else:
        employee_heure_entree = dt.datetime.now()
        insertQuery = "INSERT INTO emp_data (ID,Name,Age,Email,Phone,heure_entree,Date_save) VALUES (?,?,?,?,?,?,?)"
        val = (employee_id, employee_name, employee_age, employee_email, employee_phone, employee_heure_entree, date_emp)
        cur.execute(insertQuery, val)

        if insertData:
            messagebox.showinfo("Insertion", "Bel et bien inséré")
            emp_id.set('');
            emp_name.set('');
            emp_age.set('');
            emp_email.set('');
            emp_phone.set('');
            emp_heure_entree.set('');
            date_emp.set('')
        conn.commit()
        get_data()

def updateData(rows):
    trView.delete(*trView.get_children())
    for item in rows:
        trView.insert('', 'end', values=item)


def get_data():
    global myData
    cur = conn.cursor()
    employee_id = emp_id.get()
    # sel_data = ("SELECT * FROM emp_data WHERE ID=?")
    # cur.execute("SELECT * FROM emp_data WHERE ID=?"+employee_id)

    query = "SELECT ID,Name,Age,Email,Phone,heure_entree,heure_sortie FROM emp_data"
    cur.execute(query)
    myData = cur.fetchall()
    updateData(myData)


def search_employee():
    cur = conn.cursor()
    search_name = searchEnt.get()

    if search_name in emp_ids_list:
        query = "SELECT ID,Name,Age,Email,Phone,Salary FROM emp_data WHERE ID LIKE ? OR Name LIKE ?"
        cur.execute(query, (search_name, search_name))
        myData = cur.fetchall()
        updateData(myData)
    else:
        messagebox.showinfo("ID does not exist", "This ID does not exist in the database")


def retrive_employee():
    cur = conn.cursor()
    employee_id = emp_id.get()
    my_data = "SELECT Name,Age,Email,Phone,heure_entree,heure_sortie FROM emp_data WHERE ID = ?"
    emp_ids_list = get_ids_list()

    cur.execute(my_data, (employee_id,))
    selected_data = cur.fetchall()

    if employee_id in emp_ids_list:
        for emp_row in selected_data:
            emp_name.set(str(emp_row[0]))
            emp_age.set(str(emp_row[1]))
            emp_email.set(str(emp_row[2]))
            emp_phone.set(str(emp_row[3]))
            emp_heure_entree.set(str(emp_row[4]))
    else:
        messagebox.showinfo("ID n'existant pas", "Non reconnu")


def delete_employee():
    cur = conn.cursor()
    employee_id = emp_id.get()

    ids = cur.execute("SELECT ID FROM emp_data")
    list_ids = [str(''.join(item)) for item in ids]

    if not employee_id in list_ids:
        messagebox.showinfo("Erreur", "N'existant pas")

    else:
        delMessage = messagebox.askquestion("Supprimer", "Etes vous sur ?")
        if delMessage == 'yes':
            deleteQuery = ("DELETE FROM emp_data WHERE ID = ?")

            deleteEmployee = cur.execute(deleteQuery, (employee_id,))
            messagebox.showinfo("Supprimer", "Suppression terminée")
            emp_id.set('');
            emp_name.set('');
            emp_age.set('');
            emp_email.set('');
            emp_phone.set('');
            emp_heure_entree.set('')
            get_data()
        conn.commit()


App_title_frm = tk.Frame(window, width=1000, height=60, bg='#4F5A60')
App_title_frm.place(x=10, y=10)

app_date = datetime.now()
x_date = app_date.strftime('%Y-%m-%d')
# x_time = app_date.strftime('%H:%M:%S')

date_lbl = tk.Label(App_title_frm, text=x_date, bg='#4F5A60', fg='#E8FEFF', font=('Arial Greek', 10, 'bold'))
date_lbl.place(x=70, y=18)


def app_time():
    string = time.strftime('%H:%M:%S %p')
    time_lbl.config(text=string)
    time_lbl.after(1000, app_time)


time_lbl = tk.Label(App_title_frm, bg='#4F5A60', fg='#E8FEFF', font=('Arial Greek', 10, 'bold'))
time_lbl.place(x=712, y=18)

app_time()


# ========================================== Menu Barr ==========================================
def light_theme():
    App_title_frm.config(bg='#D2FFF7')
    window.config(background='#F4FFFF');
    date_lbl.config(bg='#D2FFF7', fg='#555F5F')
    my_app_title.config(bg='#D2FFF7', fg='#555F5F');
    time_lbl.config(bg='#D2FFF7', fg='#555F5F')
    search_frm.config(bg='#D1FFEC');
    search_lbl.config(bg='#C8FFEA', fg='#363D3D')
    search_btn.config(bg='#8FDEC2', fg='#363D3D'), searchEnt.config(bg='#A8D7D9', fg='#131414')
    filter_btn.config(bg='#BDB7FB', fg='#363D3D')
    buttons_box.config(bg='#D9F2FA');
    filter_date_frm.config(bg='#F4FFFF')
    employee_data.config(bg='#C9FFF8', fg='#2B5667');
    employee_list.config(bg='#F4FFFF', fg='#31766D')

    filter_lbl.config(bg='#F4FFFF', fg='#323739')
    from_date_lbl.config(bg='#F4FFFF');
    to_date_lbl.config(bg='#F4FFFF')
    cal1.config(background='#F4FFFF');
    cal2.config(background='#F4FFFF')
    idlbl.config(bg='#C9FFF8', fg='#323739');
    namelbl.config(bg='#C9FFF8', fg='#323739')
    agelbl.config(bg='#C9FFF8', fg='#323739');
    emaillbl.config(bg='#C9FFF8', fg='#323739')
    phonelbl.config(bg='#C9FFF8', fg='#323739');
    heurelbl.config(bg='#C9FFF8', fg='#323739')

    idEnt.config(bg='#B2D4DF', fg='#131414');
    nameEnt.config(bg='#B2D4DF', fg='#131414')
    ageEnt.config(bg='#B2D4DF', fg='#131414');
    emailEnt.config(bg='#B2D4DF', fg='#131414')
    phoneEnt.config(bg='#B2D4DF', fg='#131414');
    heureEnt.config(bg='#B2D4DF', fg='#131414')

    insertEmployee.config(bg='#77F6E9', fg='#353C3B')
    updateEmployee.config(bg='#82E8D6', fg='#353C3B')
    retrieveEmployee.config(bg='#98B6F5', fg='#353C3B')
    deleteEmployee.config(bg='#FFD393', fg='#353C3B')
    show_data.config(bg='#A5FFCF', fg='#353C3B')


def dark_theme():
    App_title_frm.config(bg='#4F5A60')
    window.config(background='#6A6A6A');
    date_lbl.config(bg='#4F5A60', fg='#E8FEFF')
    my_app_title.config(bg='#4F5A60', fg='#D1FFF9');
    time_lbl.config(bg='#4F5A60', fg='#E8FEFF')
    search_frm.config(bg='#53595D');
    search_lbl.config(bg='#53595D', fg='white')

    search_btn.config(bg='#56545D', fg='white'), searchEnt.config(bg='#445A72', fg='black')
    filter_btn.config(bg='#497D7D', fg='white')

    buttons_box.config(bg='#5C6463');
    filter_date_frm.config(bg='#6A6A6A', fg='white')
    employee_data.config(bg='#6A6A6A', fg='#A4FFFB');
    employee_list.config(bg='#6A6A6A', fg='#E7FFD8')
    filter_lbl.config(bg='#6A6A6A', fg='#DFF9FF')
    from_date_lbl.config(bg='#6A6A6A');
    to_date_lbl.config(bg='#6A6A6A')
    cal1.config(background='#536063');
    cal2.config(background='#536063')

    idlbl.config(bg='#6A6A6A', fg='white');
    namelbl.config(bg='#6A6A6A', fg='white')
    agelbl.config(bg='#6A6A6A', fg='white');
    emaillbl.config(bg='#6A6A6A', fg='white')
    phonelbl.config(bg='#6A6A6A', fg='white');
    heurelbl.config(bg='#6A6A6A', fg='white')
    idEnt.config(bg=ent_color, fg='#131414');
    nameEnt.config(bg=ent_color, fg='#131414')
    ageEnt.config(bg=ent_color, fg='#131414');
    emailEnt.config(bg=ent_color, fg='#131414')
    phoneEnt.config(bg=ent_color, fg='#131414');
    heureEnt.config(bg=ent_color, fg='#131414')

    insertEmployee.config(bg='#2D7A87', fg='white')
    updateEmployee.config(bg='#435C6B', fg='white')
    retrieveEmployee.config(bg='#476265', fg='white')
    deleteEmployee.config(bg='#6C6354', fg='white')
    show_data.config(bg='#416853', fg='white')


def help_window():
    help_win = tk.Toplevel()
    help_win.geometry('700x500+400+500')
    help_win.title('Gestion de pointage')
    help_win.configure(background='#6A6A6A')
    help_win.resizable(width=False, height=False)

    help_win.mainloop()


def about_app():
    pass


def contact_app():
    pass


menubarr = tk.Menu(window)
window.config(menu=menubarr)

file_menu = tk.Menu(menubarr, tearoff=0)
menubarr.add_cascade(label="Themes", menu=file_menu)
file_menu.add_command(label="Lumiere", command=light_theme)
# file_menu.add_separator()
file_menu.add_command(label="Mode Sombre", command=dark_theme)

Help_menu = tk.Menu(menubarr, tearoff=0)
menubarr.add_cascade(label="Aide", menu=Help_menu)
Help_menu.add_command(label="Options", command=help_window)

about_menu = tk.Menu(menubarr, tearoff=0)
menubarr.add_cascade(label="A propos", menu=about_menu)
about_menu.add_command(label="A propos", command=about_app)
about_menu.add_command(label="Contact", command=contact_app)

my_app_title = tk.Label(App_title_frm, text='ıllıllı\tGestion de base de données\tıllıllı', bg='#4F5A60',
                        fg='#D1FFF9', font=('Arial Greek', 12, 'bold'))
my_app_title.place(x=222, y=15)

search_frm = tk.Frame(window, width=1000, height=60, bg='#53595D')
search_frm.place(x=10, y=75)

search_lbl = tk.Label(search_frm, text='Entrer un ID ou le nom que vous recherchez', bg='#53595D',
                      fg='white', font=('Arial Greek', 13))
search_lbl.place(x=20, y=16)

searchEnt = tk.Entry(search_frm, width=22, font=('Arial Greek', 12),
                     bg='#445A72', fg='#131414', relief=tk.RIDGE)
searchEnt.place(x=450, y=19)

search_btn = tk.Button(search_frm, width=12, padx=2, pady=2,
                       font=("Arial Greek", 10), bd=1, text="☥ Rechercher", bg="#56545D", fg='white', relief=tk.RIDGE,
                       command=search_employee)
search_btn.place(x=700, y=16)

filter_date_frm = tk.LabelFrame(window, width=1000, height=60, bg='#6A6A6A', bd=3,
                                font=('Arial Greek', 9, 'bold'), fg='white')
filter_date_frm.place(x=10, y=140)

employee_data = tk.LabelFrame(window, width=1000, height=150, bd=3, font=('Arial Greek', 10, 'bold'),
                              text='Informations', bg='#6A6A6A', fg='#A4FFFB')
buttons_box = tk.LabelFrame(window, width=1000, height=80, bd=3, font=('Arial Greek', 10, 'bold'),
                            bg='#5C6463')
employee_list = tk.LabelFrame(window, width=1000, height=150, bd=3, font=('Arial Greek', 10, 'bold'),
                              text='Employees List', bg='#6A6A6A', fg='#E7FFD8')

employee_data.place(x=10, y=200)
buttons_box.place(x=10, y=358)
employee_list.place(x=10, y=438)

# =============================== Filter Per Date ==========================
filter_lbl = tk.Label(filter_date_frm, text='La date que vous recherchez?', bg='#6A6A6A',
                      fg='#DFF9FF', font=('Arial Greek', 13))
filter_lbl.place(x=20, y=12)

cal1 = tk.Entry(filter_date_frm, width=12, background='#536063', foreground='white', borderwidth=1)
cal1.place(x=400, y=16)

from_date_lbl = tk.Label(filter_date_frm, text='From', font=('Arial Greek', 10), bg='#6A6A6A', fg='white')
from_date_lbl.place(x=360, y=15)

cal2 = tk.Entry(filter_date_frm, width=12, background='#536063', foreground='white', borderwidth=1)
cal2.place(x=553, y=16)

to_date_lbl = tk.Label(filter_date_frm, text='To', font=('Arial Greek', 10), bg='#6A6A6A', fg='white')
to_date_lbl.place(x=528, y=16)


def filter_per_date():
    cur = conn.cursor()
    filter_last_date = str(cal1.get_date())
    filter_next_date = str(cal2.get_date())

    query = "SELECT ID,Name,Age,Email,Phone,Salary FROM emp_data WHERE Date_save BETWEEN ? AND ?"
    cur.execute(query, (filter_last_date, filter_next_date))
    myData = cur.fetchall()
    updateData(myData)


filter_btn = tk.Button(filter_date_frm, width=12, padx=2, pady=2,
                       font=("Arial Greek", 10), bd=1, text="〄 Filter", bg="#497D7D", fg='white', relief=tk.RIDGE,
                       command=filter_per_date)
filter_btn.place(x=698, y=13)


# =============================== Filter Per Date ==========================


def update_employee():
    global int_ids
    cur = conn.cursor()
    employee_id = emp_id.get()
    update_query = "UPDATE emp_data SET Name=?,Age=?,Email=?,Phone=?,Date_save=? WHERE ID=?"

    values_update = (emp_name.get(), emp_age.get(), emp_email.get(), emp_phone.get(),
                     str(cal1.get()), employee_id)
    cur.execute(update_query, values_update)

    if employee_id in emp_ids_list:
        messagebox.showinfo("Modifier", "Modifications enregistrées")
        emp_id.set('');
        emp_name.set('');
        emp_age.set('');
        emp_email.set('');
        emp_phone.set('');
        emp_heure_entree.set('current_datatime()');

    else:
        messagebox.showinfo("Impossible", "Cette personnne n'existe pas")
    conn.commit()
    get_data()


# ========================= Employee Information start =========================
ent_color = '#56666B'
idlbl = tk.Label(employee_data, text='Numero ID', font=('Arial Greek', 10, 'bold'), bg='#6A6A6A',
                 fg='white')
idlbl.place(x=20, y=20)

idEnt = tk.Entry(employee_data, width=18, textvariable=emp_id, font=('Arial Greek', 12),
                 bg=ent_color, fg='#131414', relief=tk.RIDGE)
idEnt.place(x=150, y=20)

namelbl = tk.Label(employee_data, text='Nom', font=('Arial Greek', 10, 'bold'), bg='#6A6A6A',
                   fg='white')
namelbl.place(x=400, y=20)

nameEnt = tk.Entry(employee_data, width=22, textvariable=emp_name, font=('Arial Greek', 12),
                   bg=ent_color, fg='#131414', relief=tk.RIDGE)
nameEnt.place(x=520, y=20)

agelbl = tk.Label(employee_data, text='Age', font=('Arial Greek', 10, 'bold'), bg='#6A6A6A',
                  fg='white')
agelbl.place(x=20, y=50)

ageEnt = tk.Entry(employee_data, width=14, textvariable=emp_age, font=('Arial Greek', 12),
                  bg=ent_color, fg='#131414', relief=tk.RIDGE)
ageEnt.place(x=150, y=50)

emaillbl = tk.Label(employee_data, text='Email', font=('Arial Greek', 10, 'bold'), bg='#6A6A6A',
                    fg='white')
emaillbl.place(x=400, y=50)

emailEnt = tk.Entry(employee_data, width=24, textvariable=emp_email, font=('Arial Greek', 12),
                    bg=ent_color, fg='#131414', relief=tk.RIDGE)
emailEnt.place(x=520, y=50)

phonelbl = tk.Label(employee_data, text='Phone', font=('Arial Greek', 10, 'bold'), bg='#6A6A6A',
                    fg='white')
phonelbl.place(x=20, y=80)

phoneEnt = tk.Entry(employee_data, width=18, textvariable=emp_phone, font=('Arial Greek', 12),
                    bg=ent_color, fg='#131414', relief=tk.RIDGE)
phoneEnt.place(x=150, y=80)

heurelbl = tk.Label(employee_data, text='Heure', font=('Arial Greek', 10, 'bold'), bg='#6A6A6A',
                     fg='white')
heurelbl.place(x=400, y=80)

heureEnt = tk.Entry(employee_data, width=17, text=emp_heure_entree, font=('Arial Greek', 12),
                     bg=ent_color, fg='#131414', relief=tk.RIDGE )
heureEnt.place(x=520, y=80)

# ============================ Employee Information End =======================
trView = ttk.Treeview(employee_list, columns=(1, 2, 3, 4, 5, 6,7), show="headings", height=10)
trView.pack(fill='both')

trView.heading(1, text="ID");
trView.heading(2, text="Nom")
trView.heading(3, text="Age");
trView.heading(4, text="Email")
trView.heading(5, text="Phone");
trView.heading(6, text="heure_entrée")
trView.heading(7,text="heure_sortie")


trView.column(1, width=80, anchor="n");
trView.column(2, width=150, anchor="n");
trView.column(3, width=120, anchor="n");
trView.column(4, width=200, anchor="n");
trView.column(5, width=150, anchor="n");
trView.column(6, width=120, anchor="n");
trView.column(7,width=90,anchor="n");

insertEmployee = tk.Button(buttons_box, width=12, padx=2, pady=2,
                           font=("Arial Greek", 12), bd=1, text="√ Inserer", bg="#2D7A87", fg='white', relief=tk.RIDGE,
                           command=insertData)
insertEmployee.place(x=35, y=20)

updateEmployee = tk.Button(buttons_box, width=12, padx=2, pady=2,
                           font=("Arial Greek", 12), bd=1, text="© Modifier", bg="#435C6B", fg='white', relief=tk.RIDGE,
                           command=update_employee)
updateEmployee.place(x=355, y=20)

retrieveEmployee = tk.Button(buttons_box, width=12, padx=2, pady=2,
                             font=("Arial Greek", 12), bd=1, text="ㆁ Retirer", bg="#476265", fg='white',
                             relief=tk.RIDGE, command=retrive_employee)
retrieveEmployee.place(x=195, y=20)

deleteEmployee = tk.Button(buttons_box, width=12, padx=2, pady=2,
                           font=("Arial Greek", 12), bd=1, text="〤 Supprimer", bg="#6C6354", fg='white', relief=tk.RIDGE,
                           command=delete_employee)
deleteEmployee.place(x=515, y=20)

show_data = tk.Button(buttons_box, width=12, padx=2, pady=2,
                      font=("Arial Greek", 12), bd=1, text="⎋ Liste", bg="#416853", fg='white', relief=tk.RIDGE,
                      command=get_data)
show_data.place(x=674, y=20)
accès=tk.Button(buttons_box, width=12, padx=2, pady=2,
                      font=("Arial Greek", 12), bd=1, text="⎋ Accès", bg="#416853", fg='white', relief=tk.RIDGE,command=lambda:acces())
accès.place(x=800,y=20)

def acces():
  fenetre= tk.Toplevel(window)
  fenetre.geometry("300x200")
  current_datetime = dt.datetime.now()
  current_datetime = tk.Label(fenetre,text=current_datetime,bg="darkgrey")
  current_datetime.grid(row=0, column=0)
#Changement de come
  device = 'COM4'
  try:
        essai = tk.Label(fenetre, text="Veuillez patienter", bg="darkgrey")
        arduino = serial.Serial(device, 9600)
        essai.grid(row=1, column=0)
  except:
        echec = tk.Label(fenetre, text="Accès interdit", bg="darkgrey")
        echec.grid(row=2, column=0)
  while True:
        data = arduino.readline()
        data = tk.Label(fenetre, text=data)
        data.grid(row=3, column=0)
        accept = tk.Label(fenetre, text="Accès autorisé", bg="darkgrey")
        accept.grid(row=4, column=0)
        pieces = data.split()
        pieces.grid(row=5, column=0)
        now = datetime.now()
        ctime = now.strftime("%H:%M:%S")

        day = datetime.today()
        nday = day.sfrtime("%d-%m-%Y")

window.mainloop()