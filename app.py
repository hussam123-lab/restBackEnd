from flask import Flask, request,render_template
import sys
import json
app = Flask(__name__)


ls = []
container_logs = {
    "am-usage" : {},
    "insights-logs-appservicehttplogs" : {},
    "insights-metrics-pt1m": {}
}
@app.route('/', methods = ["POST","GET"])

@app.route('/main',methods = ["POST","GET"])
def getMain():
    x = None

    if request.method == 'POST':
        x = request.data.decode("utf-8") # gets data then goes from bytes to string
        x = json.loads(x)
        container_logs[x["name"]] = x["data"]
    
    

        

    return ('Rest API')

