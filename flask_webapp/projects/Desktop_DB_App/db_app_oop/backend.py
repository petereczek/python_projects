import sqlite3 as sql

#self.connect to db(if doesn't exist, create and self.connect), create table if doesn't exist yet
class Database:
#Constructor, takes parameters for class instance, and any other constructor parameters.
	def __init__(self, db):
		self.conn = sql.connect(db)
		self.cur = self.conn.cursor()
		self.cur.execute("CREATE TABLE IF NOT EXISTS employee(Emplid integer PRIMARY KEY, LastName text, FirstName text,  Department text, Salary real, Position text)")
		self.conn.commit()

	#insert values into table
	#Insertion order was not same as table definition order had it wrong!!!, so changed table def to match
	def insert(self,LastName, FirstName, Department, Salary, Position):
	#Don't need to enter Primary Key, Sqlite automatically assigns serial number
		self.cur.execute("INSERT INTO employee VALUES(NULL,?, ?, ?, ?,?)", (LastName, FirstName, Department, Salary, Position))
		self.conn.commit()


	def view(self):

		self.cur.execute("SELECT * FROM employee")
		rows = self.cur.fetchall()
		return rows

	#set default input parameters to zero, if user doesn't enter some parameter, it'll return empty list
	def search(self, Emplid="", LastName="", FirstName="", Department="", Salary="", Position=""):

		self.cur.execute("SELECT * FROM employee WHERE Emplid = ? OR LastName = ? OR FirstName = ? OR Department = ? OR Salary = ? OR Position = ?", (Emplid, LastName, FirstName, Department, Salary,  Position))
		rows = self.cur.fetchall()
		return rows


	def delete(self,Emplid):

		self.cur.execute("DELETE FROM employee WHERE Emplid = ?", (Emplid,))
		self.conn.commit()


	def update(self, Emplid,LastName, FirstName, Department, Salary, Position):

		self.cur.execute("UPDATE employee SET LastName = ?, FirstName = ?, Department= ?, Salary = ?, Position = ? WHERE Emplid = ?", (LastName, FirstName, Department, Salary, Position,Emplid))
		self.conn.commit()

	def __del__(self):
		self.conn.close()
