Repository for the TigerBites web app.

A COS 333 Project by Yujin Yamahara, Heidi Kim, Skyler Liu, and Avi Bendory.

The production app is live at princeton-tigerbites.herokuapp.com
The staging app is live at shrouded-earth-66566.herokuapp.com

Dependencies: Flask, Flask_SQLAlchemy, flask_script, flask_migrate, psycopg2-binary, Heroku, PostgreSQL

Environment Setup:

From the project root directory, open virtual environment: `source ./venv/bin/activate`

Then install the necessary packages:
-`pip install flask`
-`pip install flask_sqlalchemy`
-`pip install flask_script`
-`pip install flask_migrate`
-`pip install psycopg2-binary`
-`pip install python-dotenv`


Heroku setup (don't need unless you're pushing to Heroku):

heroku buildpacks:set heroku/python
heroku addons:add heroku-postgresql:hobby-dev --remote (heroku-staging/ heroku-production)
pip freeze > requirements.txt

Login for the postgres db admin: User: tiger. Password: tigerbites2021. DB name is tigerbites_db# Tiger-Bites
