from flask import Flask, flash, render_template, request, redirect, url_for
import model
import urllib
import re

app = Flask(__name__) # make a new instance of the Flask class
app.secret_key = 'some_secret'

# a decorated function aka a 'view'
@app.route("/") # this is the decorate that tells Flask what URL/route is attached to this index function, i.e. maps URL to function
def index():
	return render_template("index.html", user_name="kwugirl") # the return value that's sent back to the browser as read from our index html file

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
	return render_template("new_task.html")

# @app.route("/new_task/<error_msg>")
# def new_tasks_error(error_msg):
# 	return render_template("new_task_error.html", error=error_msg)


@app.route("/save_task", methods=["POST"]) # this url will respond to posted forms rather than just get url requests
def save_task():
	task_title = urllib.quote(request.form['task_title']) # request object representing state of user browser, contents from form are put into dictionary on the 'request' object
	# encoding all input

	#TODO: make title required
	
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