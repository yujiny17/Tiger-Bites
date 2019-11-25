#!/usr/bin/env python

#-----------------------------------------------------------------------
# towerdata.py
# Author: Avi Bendory
# References: https://flask-sqlalchemy.palletsprojects.com/en/2.x/quickstart/#quickstart
#-----------------------------------------------------------------------

from app import db
from app.models import Menu, DayMenu, Meal, Item, Order, Club, User, Post
from datetime import datetime
from app import wrapper

#-----------------------------------------------------------------------


# Generate sample data for the database- specific to Tower club
def generateSampleData():

	#db.create_all()
	#db.session.commit()

	#-------------
	# Club
	#-------------

	tower = Club(clubName='Tower Club')

	#-------------
	# User
	#-------------

	towerAdmin = User(username='towerAdmin', email='tower@example.com', password='12345', is_admin=True)
	tower.users.append(towerAdmin)

	#-------------
	# Sample Menus
	#-------------

	weekOne = Menu()
	weekTwo = Menu()
	weekThree = Menu()
	weekFour = Menu()

	menus = [weekOne, weekTwo, weekThree, weekFour]

	for menu in menus:
		tower.menus.append(menu)

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
		for menu in menus:
			menu.dayMenus.append(dayMenu)

	#-------------
	# Sample Meals
	#-------------

	lunch = Meal(mealNum=1)
	dinner = Meal(mealNum=2)

	meals = [lunch, dinner]

	for meal in meals:
		for dayMenu in dayMenus:
			dayMenu.meals.append(meal)

	#-------------
	# Sample Items
	#-------------

	theBuffalo = Item(name="The Buffalo", descrip="Coated in Hot Sauce & Topped w/ Bleu Cheese & Celery Salt")
	theParmigiana = Item(name="The Parmigiana", descrip="Topped w/ Marinara, Provolone & Parmesean Cheese")
	theTSS = Item(name='The T.S.S (Tower Signature Sandwich)', descrip='Topped w/Monterey Jack, Lettuce, Tomato, Pickle, Frizzled Onions & Special Sauce')
	theRoadhouse = Item(name='The Roadhouse', descrip='BBQ Sauce, Bacon, Cheddar, Frizzled Onions, Lettuce, Tomato & Pickle')
	theMaulWowie = Item(name='The Maul Wowie', descrip='Teriyaki Sauce, Avocado, Cucumber & Fresh Pineapple')
	theItaliano = Item(name='The Italiano', descrip='Melted Provolone, Roasted Garlic Aioli, Sautéed Red Onions & Picked Peppers w/ Parm Cheese')
	theNacho = Item(name='The Nacho', descrip='Pico de Gallo, Cheddar, Avocado, Lettuce, Tomato, Chalula Ranch & Tortilla Strips')
	theBistro = Item(name='The Bistro', descrip='Swiss Cheese, Remoulade Sauce, Bacon, Lettuce, Tomato & French Fried Potatoes')
	theCalifornia = Item(name='The California', descrip='Avocado, Lettuce, Tomato, Red Onion, Mayo (cheese upon request')
	theFrenchPig = Item(name='The French Pig', descrip='Bacon, Brie & Caramelized Onions on Sourdough')
	theChipotle = Item(name='The Chipotle', descrip='Chipotle BBQ, Monterey Jack, Fried Tortilla & Pico de Gallo')
	theCiao = Item(name='The Ciao', descrip='Fresh Mozzarella, Marinated Roasted Tomato & Pesto on a Sourdough Panini')
	blueBayou = Item(name='Blue Bayou', descrip='Cajun Seasoning, Blue Cheese Crumbles & Shallot Marmalade')
	theKamikaze = Item(name='The Kamikaze', descrip='Avocado, Red Onion, Cucumber, Wasabu Mayo & Swiss Cheese')

	items = [theBuffalo, theParmigiana, theTSS, theRoadhouse, theMaulWowie, theItaliano, theNacho, theBistro, theCalifornia, theFrenchPig, theChipotle, theCiao, blueBayou, theKamikaze]

	for item in items:
		lunch.items.append(item)
		dinner.items.append(item)

	#--------------
	# Sample Orders
	#--------------

	togoLunch1 = Order(pickupTime=datetime.utcnow(), modifications='None')
	togoLunch2 = Order(pickupTime=datetime.utcnow(), modifications='None')
	togoLunch3 = Order(pickupTime=datetime.utcnow(), modifications='None')

	orders = [togoLunch1, togoLunch2, togoLunch3]

	togoLunch1.items.append(theBuffalo)
	togoLunch2.items.append(theParmigiana)
	togoLunch3.items.append(theTSS)

	for order in orders:
		towerAdmin.orders.append(order)
		tower.orders.append(order)

	#----------------------
	# Add sample data to db
	#----------------------

	db.session.add(tower)

	db.session.add(towerAdmin)

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


