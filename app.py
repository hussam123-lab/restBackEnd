from flask import Flask, request,render_template
app = Flask(__name__)



@app.route('/', methods = ["POST","GET"])

@app.route('/main')
def getMain():
    return ('welcome to main')

@app.route('/about')
def getAbout():
    return ('welcome to about')

@app.route("/hello")
def hello():
    return "Hello, AIOps Team!"