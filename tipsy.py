from flask import Flask, render_template
import model

app = Flask(__name__) # make a new instance of the Flask class

# a decorated function aka a 'view'
@app.route("/") # this is the decorate that tells Flask what URL/route is attached to this index function, i.e. maps URL to function
def index():
	return "Woo I'm tipsy" # the return value that's sent back to the browser

if __name__ == "__main__": # start web app server when we run program from command line
	app.run(debug=True) # start server in debug mode