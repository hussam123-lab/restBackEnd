from flask import Flask, request,render_template
import sys

app = Flask(__name__)


ls = []
@app.route('/', methods = ["POST","GET"])

@app.route('/main',methods = ["POST","GET"])
def getMain():
#     print(request.data, file=sys.stderr)
#     status_code = flask.Response(data = request)
#     return status_code
    ls.append(1)
    return str(request)
#     return (str(len(ls)))

@app.route('/about')
def getAbout():
    return ('welcome to about')

@app.route("/hello")
def hello():
    return "Hello, AIOps Team!"
