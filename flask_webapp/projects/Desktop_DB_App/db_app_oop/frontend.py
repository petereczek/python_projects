from tkinter import *
import numpy as np
#import backend class we created using SQLite3 to connect app to Database
from backend import Database
#create a database object
database = Database("employees.db")
#traces noof entries made into db
#size = 0


#Frontend ::: Graphical User Interface using Tkinter
class Window(object):

	def __init__(self, window):
		#holds the list of labels for search parameters
		self.labelist = ["Emplid", "Last Name", "First Name", "Department", "Salary", "Position"]
		# a list of button labels
		self.buttonlabels = ["View All", "Search Entry", "Add Entry", "Update Selected", "Delete Selected","Clear All", "Close"]
		# assign vartype to labels and create a list of entrybox labels
		self.emplid_text, self.lastname_text, self.firstname_text, self.department_text, self.salary_text, self.position_text = (StringVar() for i in range(6))
		self.entryboxlabels =[self.emplid_text,self.lastname_text, self.firstname_text, self.department_text, self.salary_text, self.position_text]
		# lists holding Label, entrybox title objects(StringVar), Entry, and Button objects
		self.labels, self.entryboxtitle, self.entries, self.buttons = ([] for i in range(4))
		# list of functions to execute corresponding to buttons
		self.buttonfuncs = [self.view_comm, self.search_comm, self.add_comm, self.update_comm, self.delete_comm, self.clear_comm]

		for i, j in (np.ndindex(2,6)):
			#use 1st iteration to populate label and entrybox object lists
			if i==0:
				self.labels.append(Label(window,text=self.labelist[j]))
				self.entries.append(Entry(window, textvariable = self.entryboxlabels[j]))
			#use remaining iterations to place the labels on 0th,2nd,4th cols, entries on 1st, 3rd, 5th cols
			else:
				self.labels[j].grid(row = j//3, column = (j*2)%6)
				self.entries[j].grid(row = j//3, column = (j*2+1)%6)

		for k in range(7):
			#populate buttonlabels and button object lists, pass wrapper functions to command,
			#inside these we will call the functions from within backend that we need
			#Place the buttons in the 5th column along rows 3-10
			if k == 6:
				self.buttons.append(Button(window, text = self.buttonlabels[k], width = 20, command = window.destroy))
			else:
				self.buttons.append(Button(window, text = self.buttonlabels[k], width = 20, command = self.buttonfuncs[k]))
			self.buttons[k].grid(row = k+3, column = 5)

		#create listbox object
		self.box1 = Listbox(window, height = 20, width = 60)
		self.box1.grid(row = 2, column= 0, rowspan = 8, columnspan = 4)

		#create the scrollbar object
		self.sb1 = Scrollbar(window)
		self.sb1.grid(row = 2, column = 4, rowspan = 8)

		#tell box it will be using scrollbar, and tell scrollbar it will be scrolling box(y is for vertical)
		self.box1.configure(yscrollcommand = self.sb1.set)
		self.sb1.configure(command = self.box1.yview)

		#Bind listbox selection event to function returning rowvals for selection, & passing to backend func
		self.box1.bind('<<ListboxSelect>>',self.get_selected_row)


	def get_selected_row(self,event):
	#function to be binded to listbox selection event via bind
	#assign the first element of the selected row to index, then get input vals from row with given index into entry boxes
	#use try/except to avoid indexing error associated with selections in empty box or selections outside of box
		try:
			index= self.box1.curselection()[0]
			selected_tuple = self.box1.get(index)
	#Only allow entries of selected lines if they are actual db positions, not user addressed messages
			if type(selected_tuple[0]) == int:
				for i in range(6):
					self.entries[i].delete(0,END)
					self.entries[i].insert(END,selected_tuple[i])
			else:
				pass
		except IndexError:
			pass

	#define the button functions:
	def view_comm(self):
	#empty list inside box, view all db entries
		self.box1.delete(0,END)
		for row in database.view():
			self.box1.insert(END,row)

	def search_comm(self):
	#empty listbox, pass entries from entryboxlabels to search function in backend,capitalize for case-insensitive entry
		self.box1.delete(0,END)
		for row in database.search(*map(lambda x:x.get().upper(),self.entryboxlabels[:])):
			self.box1.insert(END, row)

	def add_comm(self):
	#empty listbox, insert entry with given entryboxlabels vals into db, capitalize for case-insensitive entry
		#global size
		self.box1.delete(0,END)
		getlist = list(map(lambda x:x.get().upper(),self.entryboxlabels[1:]))
		if '' not in getlist:
			database.insert(*getlist)
			#size += 1
			self.box1.insert(END, "Successfully added employee "+self.entryboxlabels[2].get()+" "+self.entryboxlabels[1].get()+".")
		else:
			self.box1.insert(END, "Please enter all information for employee.")

	def update_comm(self):
	#empty listbox, update entry with given entryboxlabels vals into db, capitalize for case-insensitive entry
		self.box1.delete(0,END)
		getlist = list(map(lambda x:x.get().upper(),self.entryboxlabels[:]))
		if '' not in getlist:
			database.update(*getlist)
			self.box1.insert(END, "Successfully updated employee "+self.entryboxlabels[0].get()+".")
		else:
			self.box1.insert(END, "Please enter Emplid and all information for employee.")

	def  delete_comm(self):
	#empty listbox, delete entry with given entryboxlabels vals into db, capitalize for case-insensitive entry
		self.box1.delete(0,END)
		getlist = list(map(lambda x:x.get().upper(),self.entryboxlabels[:]))
		if getlist[0] != '' and int(getlist[0]) > 0: #and int(getlist[0]) <= size:
			database.delete(self.entryboxlabels[0].get())
			self.box1.insert(END, "Successfully deleted employee "+self.entryboxlabels[0].get()+".")
		else:
			self.box1.insert(END, "Please enter valid Emplid")

	def clear_comm(self):
	#Button func to clear listbox and all entry boxes
		self.box1.delete(0,END)
		for i in range(6):
			self.entries[i].delete(0,END)


window = Tk()
Window(window)
window.mainloop()
