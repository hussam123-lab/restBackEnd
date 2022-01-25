from flask import Flask, request,render_template
import sys
import json
import opsgenie_sdk
app = Flask(__name__)
opsgenie_api_key = '8fedb235-e7c0-4e2a-907f-05ef3dff1d01' #or your teams opsgenie key

ls = []
container_logs = {
    "am-usage" : {},
    "insights-logs-appservicehttplogs" : {},
    "insights-metrics-pt1m": {}
}

class opsgenieConfig:
    def __init__(self, opsgenie_api_key):
        self.conf = self.conf = opsgenie_sdk.configuration.Configuration()
        self.conf.api_key['Authorization'] = opsgenie_api_key 

        self.api_client = opsgenie_sdk.api_client.ApiClient(configuration=self.conf)
        self.alert_api = opsgenie_sdk.AlertApi(api_client=self.api_client)

    def create(self):
        body = opsgenie_sdk.CreateAlertPayload(
        message='Sample',
        alias='python_sample',
        description='Sample of SDK v2',
        responders=[{
            'name': 'SampleTeam',
            'type': 'team'
        }],
        visible_to=[
        {'name': 'Sample',
        'type': 'team'}],
        actions=['Restart', 'AnExampleAction'],
        tags=['OverwriteQuietHours'],
        details={'key1': 'value1',
                'key2': 'value2'},
        entity='An example entity',
        priority='P3')
        
        try:
            create_response = self.alert_api.create_alert(create_alert_payload=body)
            print(create_response)
            return create_response
        except opsgenie_sdk.ApiException as err:
            print("Exception when calling AlertApi->create_alert: %s\n" % err)

@app.route('/', methods = ["POST","GET"])

@app.route('/main',methods = ["POST","GET"])
def getMain():
    x = None

    if request.method == 'POST':
        x = request.data.decode("utf-8") # gets data then goes from bytes to string
        x = json.loads(x)
        container_logs[x["name"]] = x["data"]
        
    return ('Rest API')

if __name__ == "__main__" :
     print('retard code')