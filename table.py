import pymysql as pym

conn = pym.connect(host = "localhost", user = "root", passwd = "password", database = "aegis_bank")

# Create cursor
c = conn.cursor()

# Create table 
c.execute("""CREATE TABLE customer (
	accno integer PRIMARY KEY AUTO_INCREMENT,
	first_name char(30),
	last_name char(30),
	address Varchar(100),
	phone Varchar(15),
	email Varchar(80),
	aadhar_no Varchar(12),
	balance decimal DEFAULT 0
	)""")

c.execute("""CREATE TABLE transation (
	tid integer PRIMARY KEY AUTO_INCREMENT,
	dot date,
	amount int,
	type char(20),
	accno integer
	)""")

# Commit changes
conn.commit()
# Close Connections
conn.close()

