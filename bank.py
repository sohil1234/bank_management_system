from tkinter import *
from PIL import ImageTk, Image
import pymysql as pym
import tkinter.messagebox
import random
import smtplib
from tkinter import ttk

root = Tk()
root.title('Aegis Bank')
root.iconbitmap('bank.ico')
root.geometry('400x300')

# Connecting to MySQL
conn = pym.connect(host = "localhost", user = "root", passwd = "password", database = "aegis_bank")
# Create cursor
c = conn.cursor()

# Inserting User Information

def submit_register():
	conn = pym.connect(host = "localhost", user = "root", passwd = "password", database = "aegis_bank")
	c = conn.cursor()

	#Insert into table
	c.execute("INSERT INTO customer(first_name, last_name, address, phone, email, aadhar_no) VALUES('{}','{}','{}','{}','{}','{}')".format(
		f_name_register.get(),
		l_name_register.get(),
		address_register.get(),
		phone_register.get(),
		email_register.get(),
		aadhar_register.get()
		))

	conn.commit()
	conn.close()
	tkinter.messagebox.showinfo("Aegis","Account Created!")
	register.destroy()

# Sign Up Window

def signup():
	global register
	register = Tk()
	register.title('Sign Up')
	register.iconbitmap('bank.ico')
	register.geometry('365x200')

	# Create Global variables for text box names
	global f_name_register
	global l_name_register
	global address_register
	global phone_register
	global email_register
	global aadhar_register

	# Create Text Boxes
	f_name_register = Entry(register, width=30)
	f_name_register.grid(row=0, column=1, pady=(10, 0))
	l_name_register = Entry(register, width=30)
	l_name_register.grid(row=1, column=1, padx=20)
	address_register = Entry(register, width=30)
	address_register.grid(row=2, column=1)
	phone_register = Entry(register, width=30)
	phone_register.grid(row=3, column=1)
	email_register = Entry(register, width=30)
	email_register.grid(row=4, column=1)
	aadhar_register = Entry(register, width=30)
	aadhar_register.grid(row=5, column=1)

	# Create Text Box Labels
	f_name_register_label = Label(register, text = 'First Name:')
	f_name_register_label.grid(row=0, column=0, pady=(10, 0))
	l_name_register_label = Label(register, text = 'Last Name:')
	l_name_register_label.grid(row=1, column=0)
	address_register_label = Label(register, text = 'Address:')
	address_register_label.grid(row=2, column=0)
	phone_register_label = Label(register, text = 'Phone Number:')
	phone_register_label.grid(row=3, column=0)
	email_register_label = Label(register, text = 'Email:')
	email_register_label.grid(row=4, column=0)
	aadhar_register_label = Label(register, text = 'Aadhar Number:')
	aadhar_register_label.grid(row=5, column=0)

	# Create Submit Button

	submit_btn_register = Button(register, text = 'Submit', command = submit_register)
	submit_btn_register.grid(row=7, column=0, columnspan=2, pady=10, padx=10, ipadx=100)

# Account Balance 

def acc_sum():
	global acc_sum_window
	acc_sum_window = Tk()
	acc_sum_window.title('Account Summary')
	acc_sum_window.iconbitmap('bank.ico')
	acc_sum_window.geometry('150x100')

	conn = pym.connect(host = "localhost", user = "root", passwd = "password", database = "aegis_bank")
	c = conn.cursor()
    # Label label

	balance_label = Label(acc_sum_window, text = 'Balance:')
	balance_label.grid(row=0, column=0, pady=(10, 0))
	deposit_label = Label(acc_sum_window, text = 'Total Deposited:')
	deposit_label.grid(row=1, column=0)
	withdrawn_label = Label(acc_sum_window, text = 'Total Withdrawn:')
	withdrawn_label.grid(row=2, column=0)

	c.execute("SELECT balance FROM customer WHERE accno={}".format(rec[0][0]))
	b = c.fetchall()
	balance_info_label = Label(acc_sum_window, text = str(b[0][0]))
	balance_info_label.grid(row=0, column=1, pady=(10,0))

	c.execute("SELECT SUM(amount) FROM transation WHERE accno={} AND type='{}'".format(
		rec[0][0],
		'deposit'
		))
	d = c.fetchall()
	deposit_info_label = Label(acc_sum_window, text = str(d[0][0]))
	deposit_info_label.grid(row=1, column=1)

	c.execute("SELECT SUM(amount) FROM transation WHERE accno={} AND type='{}'".format(
		rec[0][0],
		'withdraw'
		))
	w = c.fetchall()
	withdrawn_info_label = Label(acc_sum_window, text = str(w[0][0]))
	withdrawn_info_label.grid(row=2, column=1)



	conn.commit()
	conn.close()
	
# Withdraw money form account

def withdraw():
	conn = pym.connect(host = "localhost", user = "root", passwd = "password", database = "aegis_bank")
	c = conn.cursor()
	c.execute("SELECT * FROM customer WHERE accno={}".format(rec[0][0]))
	record = c.fetchall()
	if record[0][7] < int(amount_transact_window.get()):
		tkinter.messagebox.showerror("Error","Not Enough Balance!")
	else:
		c.execute("INSERT INTO transation(dot, amount, type, accno) VALUES(CURDATE(),{},'withdraw','{}') ".format(
			amount_transact_window.get(),
			record[0][0]
			))
		new_b = record[0][7] - int(amount_transact_window.get())
		c.execute("UPDATE customer SET balance={} WHERE accno={}".format(
			new_b,
			record[0][0]
			))

	conn.commit()
	conn.close()
	transact_window.destroy()
	tkinter.messagebox.showinfo("Yay!","Transaction Succeful!")

# Deposit money in account

def deposit():
	conn = pym.connect(host = "localhost", user = "root", passwd = "password", database = "aegis_bank")
	c = conn.cursor()

	c.execute("SELECT * FROM customer WHERE accno={}".format(rec[0][0]))
	record = c.fetchall()

	c.execute("INSERT INTO transation(dot, amount, type, accno) VALUES(CURDATE(),{},'deposit','{}')".format(
		amount_transact_window.get(),
		record[0][0]
		))
	new_b = record[0][7] + int(amount_transact_window.get())
	c.execute("UPDATE customer SET balance={} WHERE accno={}".format(
		new_b,
		record[0][0]
		))

	conn.commit()
	conn.close()
	transact_window.destroy()
	tkinter.messagebox.showinfo("Yay!","Transaction Succeful!")

# Transact window	

def transact():
	global transact_window
	transact_window = Tk()
	transact_window.title('Transact')
	transact_window.iconbitmap('bank.ico')
	transact_window.geometry('285x150')

	global amount_transact_window
	amount_transact_window = Entry(transact_window, width=30)
	amount_transact_window.grid(row=0, column=1, pady=(10, 0))

	amount_transact_window_label = Label(transact_window, text = 'Enter Amount: ')
	amount_transact_window_label.grid(row=0, column=0, pady=(10, 0))

	withdraw_transact_window_btn = Button(transact_window, text = 'Withdraw', command = withdraw)
	withdraw_transact_window_btn.grid(row=1, column=0, columnspan=2, pady=10, padx=10, ipadx=100)

	deposit_transact_window_btn = Button(transact_window, text = 'Deposit', command = deposit)
	deposit_transact_window_btn.grid(row=2, column=0, columnspan=2, pady=10, padx=10, ipadx=105)

# Transcript Window

def transcript():
	global transcript_window
	transcript_window = Tk()
	transcript_window.title('Transcript')
	transcript_window.iconbitmap('bank.ico')
	transcript_window.geometry('500x400')

	conn = pym.connect(host = "localhost", user = "root", passwd = "password", database = "aegis_bank")
	c = conn.cursor()

	c.execute("SELECT * FROM transation WHERE accno={} ORDER BY dot".format(rec[0][0])) 
	record = c.fetchall()

	tree = ttk.Treeview(transcript_window)
	tree["columns"] = ["Transaction ID","Date of Transaction","Amount","Type"]
	tree['show'] = 'headings'

	s = ttk.Style(transcript_window)
	s.theme_use("clam")

	s.configure(".", font=('Helvetica',11))
	s.configure("Treeview.Heading", font=('Helvetica',11,'bold'))


	tree.column("Transaction ID", width=140, minwidth=140, anchor=tkinter.CENTER)
	tree.column("Date of Transaction", width=150, minwidth=150, anchor=tkinter.CENTER)
	tree.column("Amount", width=75, minwidth=75, anchor=tkinter.CENTER)
	tree.column("Type", width=75, minwidth=75, anchor=tkinter.CENTER)

	tree.heading("Transaction ID", text="Transaction ID", anchor=tkinter.CENTER)
	tree.heading("Date of Transaction", text="Date of Transaction", anchor=tkinter.CENTER)
	tree.heading("Amount", text="Amount", anchor=tkinter.CENTER)
	tree.heading("Type", text="Type", anchor=tkinter.CENTER)

	i=0
	for row in record:
		tree.insert('', i, text="", values=(row[0],row[1],row[2],row[3]))
		i += 1

	hsb = ttk.Scrollbar(transcript_window, orient='vertical')
	hsb.configure(command = tree.yview)
	tree.configure(yscrollcommand = hsb.set)
	hsb.pack(fill=Y, side=RIGHT)
	tree.pack()


	conn.commit()
	conn.close()

# Updating profile changes

def edit():
	conn = pym.connect(host = "localhost", user = "root", passwd = "password", database = "aegis_bank")
	c = conn.cursor()
	c.execute("""UPDATE customer SET
		first_name = '{}',
		last_name = '{}',
		address = '{}',
		phone = '{}',
		email = '{}',
		aadhar_no = '{}'

		WHERE accno = {}
		""".format(
			f_name_editor.get(),
			l_name_editor.get(),
			address_editor.get(),
			phone_editor.get(),
			email_editor.get(),
			aadhar_editor.get(),
			rec[0][0]
			))



	conn.commit()
	conn.close()
	editor.destroy()

# Edit Profile window

def update():
	global editor
	editor = Tk()
	editor.title('Edit Your Profile')
	editor.iconbitmap('bank.ico')
	editor.geometry('350x400')

	personinfo_window.destroy()

	conn = pym.connect(host = "localhost", user = "root", passwd = "password", database = "aegis_bank")
	c = conn.cursor()

	c.execute("SELECT * FROM customer WHERE accno={}".format(rec[0][0]))
	record = c.fetchall()

	
	global f_name_editor
	global l_name_editor
	global address_editor
	global phone_editor
	global email_editor
	global aadhar_editor
	

	# Create Text Boxes
	accno_editor = Label(editor, width=30, text = record[0][0]) # Account number Label info
	accno_editor.grid(row=0, column=1, pady=(10, 0))
	f_name_editor = Entry(editor, width=30)
	f_name_editor.grid(row=1, column=1, padx=20)
	l_name_editor = Entry(editor, width=30)
	l_name_editor.grid(row=2, column=1)
	address_editor = Entry(editor, width=30)
	address_editor.grid(row=3, column=1)
	phone_editor = Entry(editor, width=30)
	phone_editor.grid(row=4, column=1)
	email_editor = Entry(editor, width=30)
	email_editor.grid(row=5, column=1)
	aadhar_editor = Entry(editor, width=30)
	aadhar_editor.grid(row=6, column=1)
	# Create Text Box Labels
	accno_label_editor = Label(editor, text = 'Accno')
	accno_label_editor.grid(row=0, column=0, pady=(10, 0))
	f_name_label_editor = Label(editor, text = 'First Name')
	f_name_label_editor.grid(row=1, column=0)
	l_name_label_editor = Label(editor, text = 'Last Name')
	l_name_label_editor.grid(row=2, column=0)
	address_label_editor = Label(editor, text = 'Address')
	address_label_editor.grid(row=3, column=0)
	phone_label_editor = Label(editor, text = 'Phone number')
	phone_label_editor.grid(row=4, column=0)
	email_label_editor = Label(editor, text = 'Email')
	email_label_editor.grid(row=5, column=0)
	aadhar_label_editor = Label(editor, text = 'Zipcode')
	aadhar_label_editor.grid(row=6, column=0)

	f_name_editor.insert(0, record[0][1])
	l_name_editor.insert(0, record[0][2])
	address_editor.insert(0, record[0][3])
	phone_editor.insert(0, record[0][4])
	email_editor.insert(0, record[0][5])
	aadhar_editor.insert(0, record[0][6])

	# Create a Save edited record
	update_btn = Button(editor, text='Save Changes', command=edit)
	update_btn.grid(row=7, column=0, columnspan=2, pady=10, padx=10, ipadx=120)

	conn.commit()
	conn.close()

# Personal Information Window

def personinfo():
	global personinfo_window
	personinfo_window = Tk()
	personinfo_window.title('Personal Information')
	personinfo_window.iconbitmap('bank.ico')
	personinfo_window.geometry('320x400')

	conn = pym.connect(host = "localhost", user = "root", passwd = "password", database = "aegis_bank")
	c = conn.cursor()

	c.execute("SELECT * FROM customer WHERE accno={}".format(rec[0][0]))
	record = c.fetchall()

	# label label
	accno_personinfo_window_label = Label(personinfo_window, text = 'Accno')
	accno_personinfo_window_label.grid(row=0, column=0, pady=(10, 0))

	f_name_personinfo_window_label = Label(personinfo_window, text = 'First Name:')
	f_name_personinfo_window_label.grid(row=1, column=0)

	l_name_personinfo_window_label = Label(personinfo_window, text = 'Last Name:')
	l_name_personinfo_window_label.grid(row=2, column=0)

	address_personinfo_window_label = Label(personinfo_window, text = 'Address:')
	address_personinfo_window_label.grid(row=3, column=0)

	phone_personinfo_window_label = Label(personinfo_window, text = 'Phone Number:')
	phone_personinfo_window_label.grid(row=4, column=0)

	email_personinfo_window_label = Label(personinfo_window, text = 'Email:')
	email_personinfo_window_label.grid(row=5, column=0)

	aadhar_personinfo_window_label = Label(personinfo_window, text = 'Aadhar Number:')
	aadhar_personinfo_window_label.grid(row=6, column=0)

	# label label info
	accno_personinfo_window_info_label = Label(personinfo_window, text = record[0][0])
	accno_personinfo_window_info_label.grid(row=0, column=1, pady=(10, 0))

	f_name_personinfo_window_info_label = Label(personinfo_window, text = record[0][1])
	f_name_personinfo_window_info_label.grid(row=1, column=1)

	l_name_personinfo_window_info_label = Label(personinfo_window, text = record[0][2])
	l_name_personinfo_window_info_label.grid(row=2, column=1)

	address_personinfo_window_info_label = Label(personinfo_window, text = record[0][3])
	address_personinfo_window_info_label.grid(row=3, column=1)

	phone_personinfo_window_info_label = Label(personinfo_window, text = record[0][4])
	phone_personinfo_window_info_label.grid(row=4, column=1)

	email_personinfo_window_info_label = Label(personinfo_window, text = record[0][5])
	email_personinfo_window_info_label.grid(row=5, column=1)

	aadhar_personinfo_window_info_label = Label(personinfo_window, text = record[0][6])
	aadhar_personinfo_window_info_label.grid(row=6, column=1)

	edit_personinfo_window_btn = Button(personinfo_window, text = 'Edit your Profile', command = update)
	edit_personinfo_window_btn.grid(row=7, column=0, columnspan=2, pady=10, padx=10, ipadx=100)

	conn.commit()
	conn.close()

def signout():
	menu.destroy()

# Main Menu 

def submit_otp_window():
	
	if otp_otp_window.get() == otp:
		otp_window.destroy()
		login.destroy()
		# New Window for menu label
		global menu
		menu = Tk()
		menu.title('Accounts')
		menu.iconbitmap('bank.ico')
		menu.geometry('415x250')

		menu_label_menu = Label(menu, text = 'Account Details', font=('Arial','25','bold'))
		menu_label_menu.grid(row=0, column=0, columnspan=3, padx=50, pady=(10, 0))

		# Create Account summary Button

		account_summary_btn_menu = Button(menu, text = 'Account Summary', command = acc_sum)
		account_summary_btn_menu.grid(row=1, column=0, columnspan=2, pady=(10,10), padx=10, ipadx=105)

		# Create a Transact Button

		transact_btn_menu = Button(menu, text='Transact', command=transact)
		transact_btn_menu.grid(row=2, column=0, columnspan=2, pady=10, padx=10, ipadx=132)

		# Create a Delete Button

		transcript_btn_menu = Button(menu, text='Transcript', command=transcript)
		transcript_btn_menu.grid(row=3, column=0, columnspan=2, pady=10, padx=10, ipadx=129)

		# Create a Update Button

		personinfo_btn_menu = Button(menu, text='Personal Information', command=personinfo)
		personinfo_btn_menu.grid(row=4, column=0, columnspan=2, pady=10, padx=10, ipadx=100)

		# Sign Out

		quit_btn_menu = Button(menu, text='Sign Out', command=signout)
		quit_btn_menu.grid(row=0, column=4, padx=0, pady=0)




	else:
		otp_window.destroy()
		tkinter.messagebox.showerror("Wrong OTP","Uho! Wrong OTP \n Pls Enter Email Again ")

# Account verification and OTP 

def submit_login():

	conn = pym.connect(host = "localhost", user = "root", passwd = "password", database = "aegis_bank")
	c = conn.cursor()

	if email_login.get():
		c.execute("SELECT * FROM customer WHERE email='{}'".format(email_login.get()))
		global rec
		rec = c.fetchall()
		
		if rec:
			if rec[0][5] == email_login.get():
				smtp_object = smtplib.SMTP('smtp.gmail.com',587)
				smtp_object.ehlo()
				smtp_object.starttls()
				email = 'aegisbank101@gmail.com'
				password = 'txvmnhgyeiaaglzl' 
				smtp_object.login(email, password)
				global otp
				otp = str(random.randint(1000, 9999))

				from_address = email
				to_address = email_login.get()
				subject = "One Time Password(OTP) - Verify your Login"
				message = "\nBelow is your OTP, Please do not share it with anyone:\n"+ otp + "\nNot you, please contact us."

				msg = "Subject: "+subject+'\n'+message
				smtp_object.sendmail(from_address, to_address, msg)
				smtp_object.quit()

				global otp_window
				otp_window = Tk()
				otp_window.title('Enter OTP')
				otp_window.iconbitmap('bank.ico')
				otp_window.geometry('300x100')

				global otp_otp_window
				otp_otp_window = Entry(otp_window, width=30)
				otp_otp_window.grid(row=0, column=1, pady=(10, 0))

				otp_otp_window_label = Label(otp_window, text = 'Enter 4 Digit OTP:')
				otp_otp_window_label.grid(row=0, column=0, pady=(10, 0))

				submit_btn_otp_window = Button(otp_window, text = 'Submit ', command = submit_otp_window)
				submit_btn_otp_window.grid(row=1, column=0, columnspan=2, pady=10, padx=10, ipadx=100)


		
		else:
			tkinter.messagebox.showerror("Invalid","Invalid Email \n Please Enter your Email Again")


	conn.commit()
	conn.close()
	
# Create Sign In Window

def signin():
	global login
	login = Tk()
	login.title('Log In')
	login.iconbitmap('bank.ico')
	login.geometry('300x100')

	global email_login
	# Create Text Boxes
	email_login = Entry(login, width=30)
	email_login.grid(row=0, column=1, pady=(10, 0))

	# Create Text Box Labels
	email_login_label = Label(login, text = 'Enter your Email:')
	email_login_label.grid(row=0, column=0, pady=(10, 0))

	# Create Submit Button

	submit_btn_login = Button(login, text = 'Get OTP', command = submit_login)
	submit_btn_login.grid(row=1, column=0, columnspan=2, pady=10, padx=10, ipadx=100)


welcome_label = Label(root, text='Welcome to Aegis', font=('Arial','25','bold'))
welcome_label.grid(column=2, row=3, columnspan=2, padx=50, pady=50)

sign_up = Button(root, text = 'Sign Up', command=signup)
sign_up.grid(column=2, row=4, pady=(10,0), ipadx=50)

sign_in = Button(root, text = 'Sign In', command=signin)
sign_in.grid(column=3, row=4, pady=(10,0), ipadx=50)

# Commit changes
conn.commit()

# Close Connections
conn.close()
root.mainloop()