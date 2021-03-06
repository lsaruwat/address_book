#Assignment 3 Address Book
#CS310 Python
#By: Logan Saruwatari
#Date: 3/30/2016
#Copyright MIT license

import sqlite3
from os import system
from os import name as osName


class Interface(object):

	enumColumn = ('fName', 'lName', 'phone', 'email')

	def __init__(self): # Pretty much don't do anything. It feels wrong to connect the db automatically
		print("Welcome to the Address Book")
		self.running = True

	def connect(self): # Connect to the db. Want to make singleton pattern if time permits

		self.connection = sqlite3.connect("contact.db")
		self.cur = self.connection.cursor()

	def close(self): # close db connection. Not sure how what will happen if I don't do this
		self.connection.close()

	def insertContact(self, contact): # create a new entry based on the contact object.
		sql = "INSERT INTO contact VALUES (?,?,?,?)"
		self.cur.execute(sql, (contact.fName, contact.lName, contact.phone, contact.email))
		self.connection.commit()

	def getAllContacts(self): # return everyone in the address book
		sql = "SELECT ROWID, fName, lName, phone, email FROM contact"
		self.cur.execute(sql)
		return self.cur.fetchall()

	def removeByName(self, _fName, _lName): #remove a contact by full name. Potential for this not being a unique entry...dangerous
		sql = "DELETE FROM contact WHERE fName=? AND lName=?"
		self.cur.execute(sql, (_fName, _lName))
		self.connection.commit()

	def removeById(self, _id): #remove a contact by id. Using built in ROWID which seems to be a unique identifier
		sql = "DELETE FROM contact WHERE ROWID=?"
		self.cur.execute(sql, (_id))
		self.connection.commit()

	def removeByPhone(self, _phone): # remove by phone number.
		sql = "DELETE FROM contact WHERE phone=?"
		self.cur.execute(sql, (_phone))
		self.connection.commit()

	def prettyPrint(self, fetchAllQuery):
		for i in fetchAllQuery:
			print("{}   {} {}   {}   {}".format(i[0], i[1],i[2], i[3], i[4]))

	def createContact(self):
		fname = input("Enter First Name: ")
		lname = input("Enter Last Name: ")
		phone = input("Enter Phone Number: ")
		email = input("Enter Email Address: ")

		self.insertContact(Contact(fname, lname, phone, email))

	def searchByName(self, searchPrompt="Enter a Name to search for: "):
		search = input(searchPrompt)

		sql = "SELECT ROWID, fName, lName, phone, email FROM contact WHERE fName LIKE ? OR lName LIKE ? OR email LIKE ?"
		self.cur.execute(sql, ("%"+search+"%", "%"+search+"%", "%"+search+"%")) # % is the wildcard that sqlite3 uses
		return self.cur.fetchall()

	def updateById(self, rowId):

		fname = input("Enter New First Name: ")
		lname = input("Enter New Last Name: ")
		phone = input("Enter New Phone Number: ")
		email = input("Enter New Email Address: ")

		sql="UPDATE contact SET fName=?, lName=?, phone=?, email=? WHERE ROWID=?"
		self.cur.execute(sql, (fname, lname, phone, email, rowId))
		self.connection.commit()

	def selectThisThing(self, thing):
		sql = "SELECT ? FROM contact"
		self.cur.execute( sql, (thing,) )
		return self.cur.fetchall()

	def sortByColumn(self):
		self.clearScreen()
		print("How would you like your contacts sorted?\n")
		print("1. First Name           2. Last Name")
		print("3. Phone Number         4. Email")

		columnToSort = input("Please select a Number: ")
		if columnToSort.isdigit() and int(columnToSort) > 0 and int(columnToSort) < 5:# input is a valid int
			sql = "SELECT ROWID, fName, lName, phone, email FROM contact ORDER BY {} ASC".format(self.enumColumn[int(columnToSort)-1]) # the question mark escape doesn't work for strings in program memory. Idk why
			self.cur.execute(sql)
			self.prettyPrint(self.cur.fetchall())
			input("Press any key to continue")
		else:	self.sortByColumn()

	def routeInput(self, intInput):
		#wow I just realized there is no switch/case in python.
		#Although that makes this harder I understand why they left it out.

		if intInput == 1:
			self.clearScreen()
			self.createContact()

		elif intInput == 2:
			self.clearScreen()
			self.prettyPrint(self.getAllContacts())
			input("press any key to continue")

		elif intInput == 3:
			self.clearScreen()
			self.prettyPrint(self.searchByName())
			input("press any key to continue")

		elif intInput == 4:
			self.clearScreen()
			self.prettyPrint(self.searchByName("Enter a Name to Update: "))
			idToUpdate = input("Enter the id you wish to update or letter to cancel: ")
			if idToUpdate.isdigit():
				self.updateById(int(idToUpdate))

		elif intInput == 5:
			self.clearScreen()
			self.prettyPrint(self.searchByName("Enter a Name to Delete: "))
			idToUpdate = input("Enter the id you wish to Delete or letter to cancel: ")
			if idToUpdate.isdigit():
				self.removeById(int(idToUpdate))

		elif intInput == 6:
			self.sortByColumn()

		elif intInput == 7:
			self.running = False
			print("KTHXBAI")
		else:
			print("Edge case occurred! This is why unit testing exists Logan... I think... I'll know ten years from now")


	def clearScreen(self):
		system('cls' if osName == 'nt' else 'clear') 
		# cross platform clearing of terminal. clear and cls are system calls

	def showOptions(self, message="Please select a number: "): # Show the user what they can do to the address book.
		self.clearScreen()

		print("-------------Address Book-------------")
		print("-"*40)
		print("\n")
		print("1. Create Contact          2. List Contacts")
		print("3. Search Contact          4. Update Contact")
		print("5. Delete Contact          6. Sort Contacts")
		print("7. Quit Address Book")
		print("\n")
		userChoice = input(message)

		if userChoice.isdigit() and int(userChoice) > 0 and int(userChoice) < 8: # input is between 1 and 6
			print(userChoice, " is valid")
			running = self.routeInput(int(userChoice))
		else: # if the users input is nonsense recurse with error message
			self.showOptions("Invalid Selection!\nPlease select a number")



	def run(self):
		
		while self.running:
			self.showOptions()


class Contact(object):


	def __init__(self, _fName, _lName, _phone, _email):
		self.fName = _fName
		self.lName = _lName
		self.phone = _phone
		self.email = _email


addressBook = Interface()

addressBook.connect()
print(addressBook.getAllContacts())
addressBook.run()

addressBook.close()
