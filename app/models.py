#-----------------------------------------------------------------------
# models.py
# Authors: Avi Bendory, Skyler Liu
# Reviewed by: Heidi Kim, Yujin Yamahara
# References: https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-iv-database
#             https://realpython.com/flask-by-example-part-2-postgres-sqlalchemy-and-alembic/
#             https://stackoverflow.com/questions/31715078/postgressqlalchemy-converting-time-to-utc-when-using-default-func-now
#-----------------------------------------------------------------------

from app import db
from datetime import datetime

from sqlalchemy.dialects.postgresql import JSON

# Login functionality
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import login

#-----------------------------------------------------------------------



# class Prototype(db.Model): 
#     id = db.Column(db.Integer, primary_key=True)
#     day = db.Column(db.String(10))
#     meal_category = db.Column(db.String(20))
#     item = db.Column(db.String(100))

   # def __init__(self):

    #def __repr__(self):
    #    return '<Menu owner: {}'.format(self)

# To represent the menu table 
class Menu(db.Model):
    __tablename__ = 'menus'
    id = db.Column(db.Integer, primary_key=True)
    week = db.Column(db.DateTime(timezone=True), index=True, default=datetime.now())
    dayMenus = db.relationship('DayMenu', backref='Menu', lazy='dynamic')
    club_id = db.Column(db.Integer, db.ForeignKey('clubs.id'))

    def __init__(self):
        self.week = datetime.now()

    def __repr__(self):
        return '<Menus: {}>'.format(DayMenu.query.with_parent(self).all()) 


#-----------------------------------------------------------------------

# To represent a certain day's menu
class DayMenu(db.Model):
    __tablename__ = 'daymenus'
    id = db.Column(db.Integer, primary_key=True)
    day = db.Column(db.Integer, index=True) # 0-6 for sunday-saturday
    menu_id = db.Column(db.Integer, db.ForeignKey('menus.id'))
    meals = db.relationship('Meal', backref='DayMenu', lazy='dynamic')

    def __init__(self, day):
        self.day = day

    def __repr__(self):
        return '<DayMenu {}>'.format(self.day)

#-----------------------------------------------------------------------

# To represent an individual meal
class Meal(db.Model):
    __tablename__ = 'meals'
    id = db.Column(db.Integer, primary_key=True)
    mealNum = db.Column(db.Integer, index=True) # 0 for breakfast, 1 for lunch, 2 for dinner, 3 for brunch
    dayMenu_id = db.Column(db.Integer, db.ForeignKey('daymenus.id'))
    items = db.relationship('Item', backref='Meal', lazy='dynamic')

    def __init__(self, mealNum):
        self.mealNum = mealNum

    def __repr__(self):
        return '<Meal {}>'.format(self.mealNum)

    def getItems(self):
        ret = []
        for item in self.items:
            ret.append(item)
        return ret

#-----------------------------------------------------------------------

# To represent a food item
class Item(db.Model):
    __tablename__ = 'items'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), index=True)
    descrip = db.Column(db.String(140), index=True)
    meal_id = db.Column(db.Integer, db.ForeignKey('meals.id'))
    # can probably get rid of backref from item to meal
    # may also want to go from item to order
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'))

    def __init__(self, name, descrip):
        self.name = name
        self.descrip = descrip


    def __repr__(self):
        return '{}'.format(self.name)

#-----------------------------------------------------------------------

# To represent an order
class Order(db.Model):
    __tablename__ = 'orders'
    id = db.Column(db.Integer, primary_key=True)
    items = db.relationship('Item', backref='Order', lazy='dynamic') # don't need items to backref orders
    modifications = db.Column(db.String(140))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    club_id = db.Column(db.Integer, db.ForeignKey('clubs.id')) # might be able to get rid of this, since we can go order -> user -> club
    orderTime = db.Column(db.DateTime(timezone=True), index=True, default=datetime.now())
    pickupTime = db.Column(db.DateTime(timezone=True), index=True, default=datetime.now()) #right now set to currenttime
    
    

    def __init__(self, pickupTime, modifications):
        self.orderTime = datetime.now()
        self.pickupTime = pickupTime
        self.modifications = modifications

    def __repr__(self):
        return '{}'.format(Item.query.with_parent(self).all())


#-----------------------------------------------------------------------

# To represent orders for a club
# Note: probably don't need this, can just have club directly reference orders
# class Orders(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     club_id = db.Column(db.Integer, db.ForeignKey('club.id'))
#     orders = db.relationship("Order", backref="club")

#     def __init__(self, club_id):
#         self.club_id = club_id

#     def __repr__(self):
#         return 'Orders{}'.format(self.orders)

#-----------------------------------------------------------------------

# To represent a club
class Club(db.Model):
    __tablename__ = 'clubs'
    id = db.Column(db.Integer, primary_key=True)
    clubName = db.Column(db.String(120), index=True, unique=True)
    orders = db.relationship('Order', backref='Club', lazy='dynamic')
    users = db.relationship('User', backref='Club', lazy='dynamic')
    menus = db.relationship('Menu', backref='Club', lazy='dynamic')

    def __init__(self, clubName):
        self.clubName = clubName

    def __repr__(self):
        return '<{}>'.format(self.clubName)

#-----------------------------------------------------------------------

# Example code for more complex DB relations
class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    posts = db.relationship('Post', backref='User', lazy='dynamic')
    club_id = db.Column(db.Integer, db.ForeignKey('clubs.id'))
    is_admin = db.Column(db.Boolean, index=True, unique=False)
    orders = db.relationship('Order', backref='User', lazy='dynamic')

    def __init__(self, username, email, password, is_admin):
        self.username = username
        self.email = email # TODO: email validation
        self.password_hash = generate_password_hash(password)
        self.is_admin = is_admin

    def __repr__(self):
        return '<User {}>'.format(self.username)
        
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


@login.user_loader
def load_user(id):
    return User.query.get(int(id))

#-----------------------------------------------------------------------
# can possibly adapt the following code for User reviews (ie feedback)
# not currently needed

class Post(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime(timezone=True), index=True, default=datetime.now())
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __init__(self, body, user_id):
        self.body = body
        self.timestamp = datetime.now()

    def __repr__(self):
        return '<Post {}>'.format(self.body)


#-----------------------------------------------------------------------
