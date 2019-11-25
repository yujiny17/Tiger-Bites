#!/usr/bin/env python

#-----------------------------------------------------------------------
# sampledata.py
# Author: Avi Bendory
# References: https://flask-sqlalchemy.palletsprojects.com/en/2.x/quickstart/#quickstart
#-----------------------------------------------------------------------

from app import db
from app.models import Menu, DayMenu, Meal, Item, Order, Club, User, Post
from datetime import datetime
from app import wrapper

#-----------------------------------------------------------------------


# Generate sample data for the database
def generateSampleData():

	#db.create_all()
	#db.session.commit()

	#-------------
	# Sample Clubs
	#-------------

	ivy = Club(clubName='Ivy Inn')
	cottage = Club(clubName='Cottage Club')
	ti = Club(clubName='Tiger Inn')
	cap = Club(clubName='Cap & Gown')
	cannon = Club(clubName='Cannon Club')

	clubs = [ivy, cottage, ti, cap, cannon]

	#-------------
	# Sample Users
	#-------------

	alice = User(username='alice', email='alice@example.com', password='12345', is_admin=True)
	bob = User(username='bob', email='bob@example.com', password='12345', is_admin=True)
	cathy = User(username='cathy', email='cathy@example.com', password='12345', is_admin=False)
	dave = User(username='dave', email='dave@example.com', password='12345', is_admin=True)
	eric = User(username='eric', email='eric@example.com', password='12345', is_admin=True)

	users = [alice, bob, cathy, dave, eric]

	ivy.users.append(alice)
	cottage.users.append(bob)
	ti.users.append(cathy)
	cap.users.append(dave)
	cannon.users.append(eric)

	#-------------
	# Sample Menus
	#-------------

	weekOne = Menu()
	weekTwo = Menu()
	weekThree = Menu()
	weekFour = Menu()

	menus = [weekOne, weekTwo, weekThree, weekFour]

	for menu in menus:
		ivy.menus.append(menu)

	#----------------
	# Sample DayMenus
	#----------------

	sunday = DayMenu(day=0)
	monday = DayMenu(day=1)
	tuesday = DayMenu(day=2)
	wednesday = DayMenu(day=3)
	thursday = DayMenu(day=4)
	friday = DayMenu(day=5)
	saturday = DayMenu(day=6)

	dayMenus = [sunday, monday, tuesday, wednesday, thursday, friday, saturday]

	for dayMenu in dayMenus:
		weekOne.dayMenus.append(dayMenu)

	#-------------
	# Sample Meals
	#-------------

	breakfast = Meal(mealNum=0)
	lunch = Meal(mealNum=1)
	dinner = Meal(mealNum=2)

	meals = [breakfast, lunch, dinner]

	for meal in meals:
		monday.meals.append(meal)

	#-------------
	# Sample Items
	#-------------

	eggs = Item(name="Eggs", descrip="Objectively the best breakfast food")
	bacon = Item(name="Bacon", descrip="Not kosher")
	grits = Item(name="grits", descrip="Hash browns")

	items = [eggs, bacon, grits]

	for item in items:
		breakfast.items.append(item)

	#--------------
	# Sample Orders
	#--------------

	togoBreakfast1 = Order(pickupTime=datetime.utcnow(), modifications='None')
	togoBreakfast2 = Order(pickupTime=datetime.utcnow(), modifications='None')
	togoBreakfast3 = Order(pickupTime=datetime.utcnow(), modifications='None')

	orders = [togoBreakfast1, togoBreakfast2, togoBreakfast3]

	togoBreakfast1.items.append(eggs)
	togoBreakfast2.items.append(bacon)
	togoBreakfast3.items.append(grits)

	alice.orders.append(togoBreakfast1)
	ivy.orders.append(togoBreakfast1)
	bob.orders.append(togoBreakfast2)
	cottage.orders.append(togoBreakfast2)
	ti.orders.append(togoBreakfast3)
	cathy.orders.append(togoBreakfast3)

	#----------------------
	# Add sample data to db
	#----------------------

	for club in clubs:
		db.session.add(club)

	for user in users:
		db.session.add(user)

	for menu in menus:
		db.session.add(menu)

	for dayMenu in dayMenus:
		db.session.add(dayMenu)

	for meal in meals:
		db.session.add(meal)

	for item in items:
		db.session.add(item)

	for order in orders:
		db.session.add(order)

	db.session.commit()


#-----------------------------------------------------------------------


