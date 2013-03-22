from flask import Flask, render_template, request, redirect
import model

app = Flask(__name__) # make a new instance of the Flask class

# a decorated function aka a 'view'
@app.route("/") # this is the decorate that tells Flask what URL/route is attached to this index function, i.e. maps URL to function
def index():
	return render_template("index.html", user_name="kwugirl") # the return value that's sent back to the browser as read from our index html file

@app.route("/tasks")
def list_tasks():
	db = model.connect_db()
	tasks_from_db = model.get_tasks(db, None) # this returns a list of dictionaries
	
	user_id_list = []
	for dictionary in tasks_from_db:
		user_id_list.append(dictionary["user_id"]) # makes a list of user IDs

	users = {}
	for user_id in user_id_list:
		users_from_db = model.get_user(db, user_id) # returns dict of all user fields
		users[users_from_db["id"]] = users_from_db["email"] # makes a dictionary of just user ID to email address mappings as keys/values

	return render_template("list_tasks.html", tasks=tasks_from_db, users=users)

@app.route("/new_task")
def new_tasks():
	return render_template("new_task.html")

@app.route("/save_task", methods=["POST"]) # this url will respond to posted forms rather than just get url requests
def save_task():
	task_title = request.form['task_title'] # request object representing state of user browser, contents from form at pur into dictionary on the 'request' object
	task_description = request.form['task_description']
	task_due_date = request.form['task_due_date']
	db = model.connect_db()
	# Assume that all tasks are attached to user 1
	task_id = model.new_task(db, task_title, task_description, task_due_date, 1)
	return redirect("/tasks")

if __name__ == "__main__": # start web app server when we run program from command line
	app.run(debug=True) # start server in debug mode