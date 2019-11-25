from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

app = Flask(__name__, template_folder='templates')
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login = LoginManager(app)
login.login_view='index'

from app import routes, models, forms, towerdata


from app import routes, models, errors, forms
from app import sampledata, wrapper
from app.models import User, Menu, DayMenu, Meal, Item, Club, Order, Post
from datetime import datetime

#towerdata.generateSampleData()

#-----------------------------------------------------------------------
# testing wrapper method
## bob = User.query.get(16)
## sushi = Item(name="sushi", descrip="I wish this was offered")
# #db.session.add(sushi)
# print(sushi)
# print(wrapper.getMembers(101))
#print(wrapper.getMeal(alice, week ,1, 1))
# print(wrapper.getOrders(102)) 
# print(wrapper.getClub(alice)) 
# print(wrapper.getMenus(101)) #problem
# print(wrapper.getUserOrders(bob)) 
# #print(wrapper.addItem(bob, 102, 2, 2, "hot dog", "or legs"))
# print(wrapper.getAdmins())



#print(wrapper.removeItem(alice, 4))# works and so should removeOrder
#print(wrapper.addOrder(bob, sushi, "none",datetime.utcnow(), datetime.utcnow())) #works



# Things that work, getMembers, getClub, addOrder, removeOrder, addItem, removeItem, getAdmins



