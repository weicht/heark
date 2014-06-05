#from flask import Flask
from __future__ import with_statement
from contextlib import closing
import os.path
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash, _app_ctx_stack, json, jsonify
from pymongo import MongoClient


#"g" is a special variable for our db connection

# configuration
#DATABASE = '/tmp/addressBook.db'
DEBUG = True
SECRET_KEY = 'development key'
USERNAME = 'admin'
PASSWORD = 'default'


def connect():
	connection = MongoClient()
	handle = connection["totorial"]
	return handle


app = Flask(__name__)
#load config variables from this file itself - all UPPERCASE vars will be used (see above)
app.config.from_object(__name__)


handle = connect()


##### Views stuff*****
@app.route('/')
def show_entries():
    users = [x for x in handle.users.find()]
    return render_template('show_entries.html', users=users)

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME']:
            error = 'Invalid username'
        elif request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid password'
        else:
            session['logged_in'] = True
            flash('You were logged in')
            return redirect(url_for('show_entries'))
    return render_template('login.html', error=error)

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('show_entries'))


#### RESTful Services stuff****
@app.route('/data/<username>', methods=['GET'])
def get_user(username):
#    users = [x for x in handle.users.find()]
#    return render_template('show_entries.html', users=users)
#    return 'User %s requested: '% username
#    return jsonify( {'user': username} )
#    users = [x for x in handle.users.find_one(username)]
    user = handle.users.find_one({'username': username})
    if user == None:
        abort(404)
    else:
        user_info = {}
        for field in user:
            if field != '_id':
                user_info[field] = user[field]
#    return jsonify( {'user': user_info} )
    return jsonify( user_info )


@app.route('/data/', methods=['GET'])
def get_users():
    users = [x for x in handle.users.find()]
#    return jsonify( { 'users': users } )
    return show_entries()


if __name__ == "__main__":
	app.run()

