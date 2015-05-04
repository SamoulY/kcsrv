#!/usr/bin/env python
import os
import hashlib

from flask import Flask, render_template, send_from_directory, redirect
from flask.ext.migrate import Migrate
from flask.ext.security import Security, SQLAlchemyUserDatastore, current_user

from forms import *
from admin import admin


# --> App setup
app = Flask(__name__)
app.config['DEBUG'] = None
app.config.from_object('config_default')
app.config.from_object('config')

# --> Extension setup
db.init_app(app)
admin.init_app(app)

migrate = Migrate(app, db)

user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore, register_form=MyRegisterForm)

# --> Register blueprints
from modules.play.play import play

app.register_blueprint(play, url_prefix='/play')

from modules.api.core import api_core

app.register_blueprint(api_core, url_prefix='/kcsapi')
from modules.user.user import api_user

app.register_blueprint(api_user, url_prefix='/kcsapi')

from modules.resources import resources

app.register_blueprint(resources, url_prefix='/kcs/resources')

# --> Base application routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/kcs/<path:path>')
def kcs(path):
    return send_from_directory('kcs', path)

@app.route('/kcs/sound/titlecall/a/<path:path>')
def sound(path):
    return send_from_directory('kcs/titlecall/a', path)

@app.route('/kcs/sound/<path:path>')
def shipsound(path):
    return send_from_directory('kcs/sound', path)

@app.route('/update_db')
def update_db():
    curr = current_user
    if hasattr(curr, "roles"):
        if 'admin' in curr.roles:
            x = util.update_db()
            return "Updated {} entries".format(str(x)), 200
        else:
            return "Unauthorized", 403
    else:
        return redirect('/account/login')

if __name__ == '__main__':
    print("Checking for updated api_start2.json...")
    if not os.path.exists("data/api_start2.json.sha256"):
        update = True
        # Generate SHA256 hash
        h = hashlib.sha256((open('data/api_start2.json').read().encode()))
        with open('data/api_start2.json.sha256', 'w') as f:
            f.write(h.hexdigest())
        print("api_start2 hash file not found - updating database.")
    else:
        h = hashlib.sha256(open('data/api_start2.json').read().encode()).hexdigest()
        h2 = open('data/api_start2.json.sha256').read().replace('\n', '')
        if h2 == h:
            print("DB entries are up to date.")
            update = False
        else:
            print("DB entries differ from api_start2.json. Go to admin/update to update.")
            update = True

    app.run(host='0.0.0.0', debug=True)

