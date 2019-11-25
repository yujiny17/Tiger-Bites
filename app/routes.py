#!/usr/bin/env python

#-----------------------------------------------------------------------
# routes.py
# Author: Heidi Kim, Yujin Yamahara, Avi Bendory, Skyler Liu
#-----------------------------------------------------------------------

from app import app

from sys import argv
from time import localtime, asctime, strftime
from flask import Flask, request, make_response, redirect, url_for
from flask import render_template
from flask import render_template, flash, redirect

from app.forms import StudentLoginForm, AdminLoginForm
from os import environ

from flask_login import current_user, login_user, logout_user
from app.models import User, Menu, DayMenu, Meal, Item, Club, Order, Post

import json
from app import wrapper
from app import db
import datetime

#-----------------------------------------------------------------------
def getCurrentPeriod():
    now = datetime.datetime.now().time()
    print(now)
    # we assume the meal times are as follows:
    # 8 - 10 : Breakfast
    # 12 - 14 : Lunch
    # 18 - 20 : Dinner
    B_STARTTIME = datetime.time(8,0,0)
    B_ENDTIME = datetime.time(10,0,0)
    L_STARTTIME = datetime.time(12,0,0)
    L_ENDTIME = datetime.time(14,0,0)
    D_STARTTIME = datetime.time(18,0,0)
    D_ENDTIME = datetime.time(20,0,0)

    # return an array representing [ifValidOrderPeriod, mealPeriod]
    if (now >= B_STARTTIME) and (now < B_ENDTIME): 
        return [1, 'Breakfast']
    elif now >= L_STARTTIME and now < L_ENDTIME: 
        return [1, 'Lunch']
    elif now >= D_STARTTIME and now < D_ENDTIME: 
        return [1, 'Dinner']   
    else:
        return [0, 'Not a meal period']
#-----------------------------------------------------------------------

@app.route('/')
@app.route('/index')
def index():
    html = render_template('index.html')
    response = make_response(html)
    return response

#-----------------------------------------------------------------------

@app.route('/studentlogin', methods=['GET', 'POST'])
def studentlogin():
    if current_user.is_authenticated:
        return redirect(url_for('menu'))
    form = StudentLoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('studentlogin'))
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('menu'))
    html = render_template('studentlogin.html', 
        title='Student Sign In', 
        form=form)
    response = make_response(html)
    return response

#-----------------------------------------------------------------------

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

#-----------------------------------------------------------------------

@app.route('/adminlogin', methods=['GET', 'POST'])
def adminlogin():
    if current_user.is_authenticated:
        return redirect(url_for('adminmenu'))
    form = AdminLoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('adminlogin'))
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('menu'))

    html = render_template('adminlogin.html', 
        title='Admin Sign In', 
        form=form)
    response = make_response(html)
    return response

#-----------------------------------------------------------------------

@app.route('/menu', methods=['GET'])
def menu():
   # rows = User.query.all()

    towerAdmin = User.query.get(1)
    tower = Club.query.filter_by(clubName='Tower Club').first() #need to figure out club later
    #ivy.menus.append(addMen)
    week = datetime.datetime.now() #will need to let them pick later
    print(week)

    #had to pull from some random db column but shows that can be populated from db
    dailyItems = wrapper.getMeal(towerAdmin, week, 6, 2); 
    for i in range (0, len(dailyItems)):
        dailyItems[i] = str(dailyItems[i]).replace('Item ', '')
    print(dailyItems)
    html = render_template('menu.html', dailyItems = dailyItems)

    # html = render_template('menu.html',
    #     currPeriod=getCurrentPeriod())
    # print("Current Meal Period: {}".format(getCurrentPeriod()[0]))

    response = make_response(html)
    return response

#-----------------------------------------------------------------------

@app.route('/adminmenu', methods=['GET', 'POST'])
def adminmenu():

    towerAdmin = User.query.get(1)
    tower = Club.query.filter_by(clubName='Tower Club').first() #need to figure out club later
    #ivy.menus.append(addMen)
    #week = datetime.now() #will need to let them pick later
    #print(week)


    week = datetime.datetime.utcnow() #will need to let them pick later


    currUser = current_user
    print("Current User: {}".format(currUser.username))


    displaySunLunch = wrapper.getMeal(towerAdmin, week, 0, 1)
    dailyItems = wrapper.getMeal(towerAdmin, week, 6, 2)

# From Heidi's branch had to comment out
    # displayItems = wrapper.getMeal(currUser, week, 0, 0); 

    # print("Menu Items: {}".format(displayItems))


    for i in range (0, len(displaySunLunch)):
        displaySunLunch[i] = str(displaySunLunch[i]).replace('Item ', '')
    print(displaySunLunch)

    for x in range (0, len(dailyItems)):
        dailyItems[x] = str(dailyItems[x]).replace('Item ', '')
    print(dailyItems)


   # To get an item to add to the db
    if request.method == 'POST':
        item = request.form['item']
        dayMeal = request.form['dayMeal']
        day = request.form['day']
        add = request.form['add']
       
        if add == 'remove':
             print("item to be removed: " + item)
             removedItem = Item.query.filter_by(name = item).first()
             wrapper.removeItem(removedItem)
        elif add == 'add':
            print("item to be added: " + item)
            print("day Meal to be added to: " + day + " " + dayMeal)
            dayMeal = int(dayMeal)
        
            if (item is not None) and (item.strip() != ''):
               wrapper.addItem(tower, week, day, dayMeal, item, "temporary description")
               #wrapper.addItem(tower, week, 6, 2, item, "temporary description")


    html = render_template('adminmenu.html', 
        displaySunLunch = displaySunLunch,
        currPeriod=getCurrentPeriod(), dailyItems = dailyItems)
    response = make_response(html)

    return response

#-----------------------------------------------------------------------

@app.route('/studentorder', methods=['GET', 'POST'])
def studentorder():

    isValidPeriod=getCurrentPeriod()[0]
    currPeriod = getCurrentPeriod()[1]
    print("Current Period: {}".format(currPeriod))

    currUser = current_user
    print("Current User: {}".format(currUser.username))
    #if isValidPeriod:
    if isValidPeriod:    
        week = datetime.datetime.utcnow() #will need to let them pick later

        #had to pull from some random db column but shows that can be populated from db
        displayItems = wrapper.getMeal(currUser, week, 6, 2); 
        print("Menu Items: {}".format(displayItems))

        html = render_template('studentorder.html', 
            displayItems = displayItems,
            currPeriod=currPeriod)
    else: 
        html = render_template('studentorderinvalid.html')
    response = make_response(html)
    return response



#-----------------------------------------------------------------------

@app.route('/adminorder', methods=['GET', 'POST'])
def adminorder():
    tower = Club.query.filter_by(clubName='Tower Club').first() #need to figure out club later
    displayOrders = wrapper.getOrders(tower)
    # for i in range (0, len(displayOrders)):
    #     displayOrders[i] = str(displayOrders[i]).replace('[', '')
    #     displayOrders[i] = str(displayOrders[i]).replace(']', '')
    print(displayOrders)



    html = render_template('adminorder.html', displayOrders = displayOrders)
    response = make_response(html)
    return response

    





