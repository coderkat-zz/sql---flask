import sqlite3
import datetime

def connect_db():
	return sqlite3.connect("taskapp.db")

def new_user(db, email, password, first_name, last_name):
    c = db.cursor()
    query = """INSERT INTO Users VALUES (NULL, ?, ?, ?, ?)"""
    result = c.execute(query, (email, password, first_name, last_name))
    db.commit()
    return result.lastrowid

def authenticate(db, username, password):
    c = db.cursor()
    query = """SELECT * FROM Users WHERE email = ? AND password = ?"""
    c.execute(query, (username, password))
    row = c.fetchone()
    if row:
        fields = ['id', 'email', 'password', 'first_name', 'last_name']
        return dict(zip(fields, row)) # this returns a dictionary where the keys are the fields and the values are what's returned from the DB. zip attached two lists together.

    return None

def get_user(db, user_id):
    c = db.cursor()
    user_id = str(user_id)
    query = """SELECT * FROM Users WHERE id = ?"""
    c.execute(query, (user_id))
    row = c.fetchone()
    if row:
        fields = ['id', 'email', 'password', 'first_name', 'last_name']
        return dict(zip(fields, row))

    return None

def new_task(db, title, description, due_date, user_id):
    timestamp = datetime.datetime.today()
    user_id = str(user_id)
    c = db.cursor()
    query = """INSERT into Tasks VALUES (NULL, ?, ?, ?, ?, NULL, ?)"""
    result = c.execute(query, (title, description, timestamp, due_date, user_id))
    db.commit()
    return result.lastrowid

def change_task(db, task_id, title, description, due_date):
    c = db.cursor()
    query = """UPDATE Tasks SET title = ?, description = ?, due_date = ? WHERE id = ?"""
    c.execute(query, (title, description, due_date, task_id))
    db.commit()
    return

def complete_task(db, task_id):
    timestamp = datetime.datetime.today()
    task_id = str(task_id)
    c = db.cursor()
    query = """UPDATE Tasks SET completed_at = ? WHERE id = ?"""
    c.execute(query, (timestamp, task_id))
    db.commit()
    return

# get tasks by user or get all tasks by all users
def get_tasks(db, user_id): 
    c = db.cursor()
    
    if user_id:
        user_id = str(user_id)
        query = """SELECT * FROM Tasks WHERE user_id = ?"""
        c.execute(query, (user_id))
    else:
        query = """SELECT * FROM Tasks"""
        c.execute(query)

    rows = c.fetchall()

    if rows:
        fields = ['id', 'title', 'description', 'created_at', 'due_date', 'completed_at', 'user_id']
        tasks = []
        for row in rows:
            task = dict(zip(fields, row))
            tasks.append(task) #adds in dictionary as an item in the list, will end up with a list of dictionaries

        return tasks #we return a list of dictionaries so that later we can use the keys in the dict as attributes when displaying variables in the HTML templates or just pull values through keys directly

    return None

# get single task by task ID
def get_task(db, task_id):
    c = db.cursor()
    task_id = str(task_id)
    query = """SELECT * FROM Tasks WHERE id = ?"""
    c.execute(query, (task_id))
    row = c.fetchone()
    if row:
        fields = ['id', 'title', 'description', 'created_at', 'due_date', 'completed_at', 'user_id']
        return dict(zip(fields, row))

    return None
