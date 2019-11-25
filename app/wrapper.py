#!/usr/bin/env python

#-----------------------------------------------------------------------
# wrapper.py
# Author: Heidi Kim, Yujin Yamahara, Avi Bendory, Skyler Liu
# Wrapper functions that help frontend access backend info
#-----------------------------------------------------------------------


from app import app
from app import db

from sys import argv
from time import localtime, asctime, strftime
from flask import Flask, request, make_response, redirect, url_for
from flask import render_template
from flask import render_template, flash, redirect

from sqlalchemy import asc, desc

from os import environ

from flask_login import current_user, login_user, logout_user
from app.models import User, Menu, DayMenu, Meal, Item, Club, Order, Post

#-----------------------------------------------------------------------
# Method to get correct items for a certain user on certain day and certain meal
def getMeal(User, week, day, mealNum):
	club_id = User.club_id
	print("Club ID: {}".format(club_id))
	#club = Club.query.get(club_id)
	#menus = club.menus
	#menus = Menu.query.filter_by(club_id=club_id, week=week).all()

	# get the most recent menu
	menu_id = Menu.query.filter_by(club_id=club_id).order_by(desc(Menu.week)).first().id
	print(menu_id)
	dayMenu_id = DayMenu.query.filter_by(menu_id=menu_id, day=day).first().id
	print(dayMenu_id)
	meal = Meal.query.filter_by(mealNum=mealNum, dayMenu_id=dayMenu_id).first()
	print(meal)
	return meal.getItems()

	# From Heidi's branch commented out

	# menu_id = Menu.query.filter_by(club_id=club_id).first().id #will need to figure out week later
	# print("Menu ID: {}".format(menu_id))
	# dayMenu_id = DayMenu.query.filter_by(menu_id=menu_id, day=day).first().id
	# print("Day Menu ID: {}".format(dayMenu_id))
	# meal = Meal.query.filter_by(mealNum=mealNum, dayMenu_id=dayMenu_id).first()
	# print("Meal: {}".format(meal))
	# # return meal.items
	# return Item.query.with_parent(meal).all()


#-----------------------------------------------------------------------
# Method to return all the admins
def getAdmins():
	return User.query.filter_by(is_admin=True).all()

#-----------------------------------------------------------------------
# Method to return all the members of a certain club
def getMembers(Club):
	club_name = Club.clubName
	return Club.query.filter_by(club_name).users.all()


#-----------------------------------------------------------------------
# Method to return all the orders for a certain club for a certain meal
def getOrders(Club):
	club_id = Club.id
	return Order.query.with_parent(Club.query.get(club_id)).all()


#-----------------------------------------------------------------------
# Method to return club for a certain user
def getClub(User):
	return User.club_id

 
#-----------------------------------------------------------------------
# Method to return all the menus for a club
def getMenus(Club):
	club_id = Club.id
	return Menu.query.with_parent(Club.query.get(club_id)).all()

#-----------------------------------------------------------------------
# Method to return all the orders for a user
def getUserOrders(User):
	return User.query.filter_by(username=User.username).orders.all()


#-----------------------------------------------------------------------
# Method to add item for a certain club on a certain day and certain meal
def addItem(Club, week, day, mealCategory, name, descrip):

	#need to figure out a way to validate user later
	# if(mealCategory < 4 and User.checkIsAdmin()):
	# 	club_id = Club.id
	# 	newItem = Item(name=name, descrip=descrip)
		
	# 	menu_id = Menu.query.filter_by(club_id=club_id, week=week).first().id
	# 	dayMenu_id = DayMenu.query.filter_by(menu_id=menu_id, day=day).id
	# 	meal = Meal.query.filter_by(meanNum=mealCateogry, dayMenu_id=dayMenu_id)
	# 	meal.items.append(newItem)
	# 	db.session.add(newItem)
	# 	#db.session.add(meal)
	# 	db.session.commit()
	# 	print("added item")
	# else:
	# 	print("unable to add item")

		club_id = Club.id
		print("Club ID: {}".format(club_id))
		newItem = Item(name=name, descrip=descrip)
		
		menu_id = Menu.query.filter_by(club_id=club_id).first().id
		#if menu_id is None : #need to make a new meal for this week

		print("Menu ID: {}".format(menu_id))

		dayMenu_id = DayMenu.query.filter_by(menu_id=menu_id, day=day).first().id
		dayMenu_day = DayMenu.query.filter_by(menu_id=menu_id, day=day).first().day
		dayMenu_menu = DayMenu.query.filter_by(menu_id=menu_id, day=day).first().menu_id
		if dayMenu_id is None:
			newDay = DayMenu(day=day)
			week.dayMenus.append(newDay)


		print(dayMenu_id)


		meal = Meal.query.filter_by(mealNum=mealCategory, dayMenu_id=dayMenu_id).first()
		if meal is None:
			print("no known meal")
			newMeal = Meal(mealNum=mealCategory)
			print(DayMenu.query.get(dayMenu_id))
			DayMenu.query.filter_by(day= dayMenu_day,menu_id=dayMenu_menu).first().meals.append(newMeal)
			db.session.add(newMeal)
			#db.session.commit()
			meal = newMeal


		print(meal)
		db.session.add(newItem)
		meal.items.append(newItem)
		
		#db.session.add(meal)
		db.session.commit()
		print("added item")	

#-----------------------------------------------------------------------
# Method to remove item from db and from the meals -- does this need to be separate?
def removeItem(Item):
	# will need to check later
	#if(User.checkIsAdmin()):
	#item = Item.query.get(item_id)
	db.session.delete(Item)
	db.session.commit()
		#DOES THIS DELETE THE ITEM FROM MEALS TOO?
	print("removed item")
	# else:
	# 	print("unable to remove item")

#-----------------------------------------------------------------------
# Method to add order from student side
# Need to add order to clubs and also to user
def addOrder(User, Item, modifications, orderTime, pickupTime):
	if(Item.query.get(Item.id) is not None):
		newOrder = Order(modifications=modifications, pickupTime=pickupTime)
		newOrder.items.append(Item)
		User.orders.append(newOrder)
		Club.query.get(User.club_id).orders.append(newOrder)
		db.session.add(newOrder)
		db.session.commit()
		print("added newOrder")
	else:
		print("unable to addOrder")


#-----------------------------------------------------------------------
# Method to remove order from admin side
# Need to remove order to clubs but don't remove it from user history?
def removeOrder(User, Order):
	if(User.checkIsAdmin()):
		db.session.delete(Order)
		db.session.commit()
		print("removed order")
	else:
		print("unable to remove order")




#-----------------------------------------------------------------------

# For testing:

if __name__ == '__main__':
    currUser = User.query.filter_by(username=towerAdmin).first()
    print(currUser.username)

