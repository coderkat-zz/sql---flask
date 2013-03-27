from flask import Flask, flash, session, render_template, request, redirect, url_for, g
import model # our other Python file that has the SQL query functions
import urllib # used for URL encoding
import re # to do regex date validation

app = Flask(__name__) # make a new instance of the Flask class
app.secret_key = 'some_secret'

# function that we can call before each view is executed
@app.before_request
def set_up_db():
	g.db = model.connect_db() # global variable, db

# function to close db connection after each view is rendered
@app.teardown_request
def close_db(e): # e is to allow this function to still be called even if some error happens
	g.db.close()

# a decorated function aka a 'view'
@app.route("/") # this is the decorate that tells Flask what URL/route is attached to this index function, i.e. maps URL to function
def index():
	return render_template("index.html") # the return value that's sent back to the browser as read from our index html file

# login page
@app.route('/login')
def login():
	return render_template("login.html")

# verifying login credentials
@app.route('/authenticate', methods=["POST"])
def authenticate():
	email = request.form['username']
	password = request.form['password']

	user_info = model.authenticate(g.db, email, password)

	# if credentials are wrong or incomplete
	if not user_info:
		flash("Incorrect username or password")
		return redirect(url_for("login"))

	else: # adding user info into session dictionary to pull out and use later
		session['user_id'] = user_info['id']
		session['username'] = user_info['email']
		return redirect(url_for("index"))

@app.route('/logout')
def logout():
	# remove existing username from session
	session.pop('username', None)
	session.pop('user_id', None)
	flash("Successfully logged out!")
	return redirect(url_for('index'))

@app.route("/tasks")
def list_tasks():
	#TODO: Make another thing that returns everything nessecary for this view, by using a join instead of having python do multiple queries.
	tasks_from_db = model.get_tasks(g.db, None) # this returns a list of dictionaries

	for dicts in tasks_from_db:
		for key in ("title", "description"):
			dicts[key] = urllib.unquote(dicts[key])

	return render_template("list_tasks.html", tasks=tasks_from_db)

@app.route("/new_task")
def new_tasks():
	if 'username' not in session:
		flash("You must be logged in to create a new task for yourself.")
		return redirect(url_for("index"))

	else:
		return render_template("new_task.html")

@app.route("/save_task", methods=["POST"]) # this url will respond to posted forms rather than just get url requests
def save_task():
	task_title = urllib.quote(request.form['task_title']) # request object representing state of user browser, contents from form are put into dictionary on the 'request' object
	# encoding all input

	# check for title in task form: if none, flash error & redirect
	if not task_title:
		flash("You must enter a title for your task")
		return redirect(url_for('new_tasks'))
	
	task_description = urllib.quote(request.form['task_description'])
	
	task_due_date = urllib.quote(request.form['task_due_date'])
	
	# using regex to check that date is in format of MM-DD-YY [1-12]-[1-31]-[13-99]
	date_comparison = re.match(r'^((0[0-9])|(1[0-2]))-((0[1-9])|(1|2)[0-9]|(3[0|1]))-((1[3-9])|([2-9][0-9]))', task_due_date)
	
	if date_comparison:
		# set new task specific to user_id
		task_id = model.new_task(g.db, task_title, task_description, task_due_date, session['user_id'])
		return redirect(url_for('list_tasks'))

	else:
		flash("Your date is not in the right format!") #flashing system basically makes it possible to record a message at the end of a request and access it next request and only next request
		return redirect(url_for('new_tasks'))

@app.route("/task_complete", methods=["POST"])
def complete_task():
	task_id = request.form['task_id']
	model.complete_task(g.db, task_id)
	flash("Marked task #" + task_id + " as complete!")
	return redirect(url_for('list_tasks'))

@app.route("/change_task", methods=["POST"])
def change_task():
	return render_template("change_task.html")

@app.route("/save_changes", methods=["POST"])
# TODO: Solve id kerfuffle
def save_changes():
	task_title = urllib.quote(request.form['task_title']) 
	# follows formatting for save_task 
	if not task_title:
		flash("You must enter a title for your task")
		return redirect(url_for('change_task'))
	
	task_description = urllib.quote(request.form['task_description'])
	
	task_due_date = urllib.quote(request.form['task_due_date'])

	date_comparison = re.match(r'^((0[0-9])|(1[0-2]))-((0[1-9])|(1|2)[0-9]|(3[0|1]))-((1[3-9])|([2-9][0-9]))', task_due_date)
	
	if date_comparison:
		task_change = model.change_task(g.db, task_title, task_description, task_due_date, task_id)
 		return redirect(url_for('list_tasks'))


	else:
		flash("Your date is not in the right format!") 
		return redirect(url_for('change_task'))


if __name__ == "__main__":
	app.run(debug=True) # start server in debug mode