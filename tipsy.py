from flask import Flask, flash, session, render_template, request, redirect, url_for
import model
import urllib
import re

app = Flask(__name__) # make a new instance of the Flask class
app.secret_key = 'some_secret'

current_user = None

# a decorated function aka a 'view'
@app.route("/") # this is the decorate that tells Flask what URL/route is attached to this index function, i.e. maps URL to function
def index():
	if 'username' in session and 'password' in session:
		db = model.connect_db()
		authenticate_result = model.authenticate(db, session['username'], session['password'])
		if authenticate_result:
			current_user = session['username']
		else:
			flash("Incorrect username or password")
			return redirect("/login")

	elif ('username','password') in session:
		flash("You need to enter both a username and a password")
		return redirect("/login")

	else:
		current_user = "Not signed in"

	return render_template("index.html", user_name=current_user) # the return value that's sent back to the browser as read from our index html file

@app.route('/login', methods=['GET', 'POST'])
def login():
	if request.method == 'POST':
		session['username'] = request.form['username']
		session['password'] = request.form['password']
		return redirect("/")
	return render_template("login.html")

@app.route('/logout')
def logout():
	# remove existing username from session
	session.pop('username', None)
	session.pop('password', None)
	return redirect("/")

@app.route("/tasks")
def list_tasks():
	#TODO: Make another thing that returns everything nessecary for this view, by using a join instead of having python do multiple queries.
	db = model.connect_db()
	tasks_from_db = model.get_tasks(db, None) # this returns a list of dictionaries

	for dicts in tasks_from_db:
		for key in ("title", "description"):
			dicts[key] = urllib.unquote(dicts[key])

	return render_template("list_tasks.html", tasks=tasks_from_db)

@app.route("/new_task")
def new_tasks():
	if 'username' not in session:
		flash("You must be logged in to create a new task for yourself.")
		return redirect("/")

	else:
		return render_template("new_task.html")

@app.route("/save_task", methods=["POST"]) # this url will respond to posted forms rather than just get url requests
def save_task():
	task_title = urllib.quote(request.form['task_title']) # request object representing state of user browser, contents from form are put into dictionary on the 'request' object
	# encoding all input

	# check for title in task form: if none, flash error & redirect
	if not task_title:
		flash("You must enter a title for your task")
		return redirect("/new_task")
	
	task_description = urllib.quote(request.form['task_description'])
	
	task_due_date = urllib.quote(request.form['task_due_date'])
	
	# using regex to check that date is in format of MM-DD-YY [1-12]-[1-31]-[13-99]
	date_comparison = re.match(r'^((0[0-9])|(1[0-2]))-((0[1-9])|(1|2)[0-9]|(3[0|1]))-((1[3-9])|([2-9][0-9]))', task_due_date)
	
	if date_comparison:
		db = model.connect_db()
			# Assume that all tasks are attached to user 1
		task_id = model.new_task(db, task_title, task_description, task_due_date, 1)
		return redirect("/tasks")

	else:
		flash("Your date is not in the right format!") #flashing system basically makes it possible to record a message at the end of a request and access it next request and only next request
		return redirect("/new_task")


if __name__ == "__main__": # start web app server when we run program from command line
	app.run(debug=True) # start server in debug mode