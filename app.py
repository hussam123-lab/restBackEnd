from flask import Flask, request,render_template
app = Flask(__name__)


ls = []
@app.route('/', methods = ["POST","GET"])

@app.route('/main')
def getMain():
    ls.append(1)
    return (str(len(ls)))

@app.route('/about')
def getAbout():
    return ('welcome to about')

@app.route("/hello")
def hello():
    return "Hello, AIOps Team!"
