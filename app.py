from flask import Flask, request,render_template
import sys
import json
import opsgenie_sdk
app = Flask(__name__)
opsgenie_api_key = '8fedb235-e7c0-4e2a-907f-05ef3dff1d01' #or your teams opsgenie key


count = 0


ls = []
container_logs = {
    "am-usage":{
    },
    "insights-logs-appservicehttplogs":[
     {
       "metricName":"CsBytes",
       "anomalies":{
        "anomalies":[
          
        ],
        "anomaly_labels":[
          
        ],
        "anomaly_indexes":[
          
        ]
       }
     },
     {
       "metricName":"ScStatus",
       "anomalies":{
        "anomalies":[
        ],
        "anomaly_labels":[
        ],
        "anomaly_indexes":[
        ]
       }
     },
     {
       "metricName":"TimeTaken",
       "anomalies":{
        "anomalies":[
          
        ],
        "anomaly_labels":[
         
        ],
        "anomaly_indexes":[
          
        ]
       }
     }
    ],
    "insights-metrics-pt1m":[
     {
       "metricName":"CpuTime",
       "anomalies":{
        "anomalies":[
        ],
        "anomaly_labels":[
        ],
        "anomaly_indexes":[
        ]
       }
     },
     {
       "metricName":"BytesSent",
       "anomalies":{
        "anomalies":[
        ],
        "anomaly_labels":[
        ],
        "anomaly_indexes":[
        ]
       }
     },
     {
       "metricName":"HttpResponseTime",
       "anomalies":{
        "anomalies":[
        ],
        "anomaly_labels":[
        ],
        "anomaly_indexes":[
        ]
       }
     }
    ]
  }

# {
#     "am-usage" : {},
#     "insights-logs-appservicehttplogs" : {},
#     "insights-metrics-pt1m": {}
# }

# count_of_accesses = {

# }

# for i in container_logs["insights-logs-appservicehttplogs"]:
#     count_of_accesses[i["metricName"]] = {
#         "count" : 0,
#         "latest_index" : 0
#     }
    
# for i in container_logs["insights-metrics-pt1m"]:
#     count_of_accesses[i["metricName"]] = {
#         "count" : 0,
#         "latest_index" : 0
#     }
# print(count_of_accesses)


"""
Opsgenie handles alerts and routes them to the right team. Routing and alerts are configured through the webapp.
Config the api_key for your team, here. This api can create, delete, and change alerts. Only create function is defined here.  
"""
class opsgenieConfig:
    def __init__(self, opsgenie_api_key):
        self.conf = self.conf = opsgenie_sdk.configuration.Configuration()
        self.conf.api_key['Authorization'] = opsgenie_api_key 

        self.api_client = opsgenie_sdk.api_client.ApiClient(configuration=self.conf)
        self.alert_api = opsgenie_sdk.AlertApi(api_client=self.api_client)

    def create(self, description, meteric, value):
        body = opsgenie_sdk.CreateAlertPayload(
        message= 'Anomaly Detected in Web App {}:{}'.format(meteric,value),
        alias='python_sample', #nneds to be unique unless you are overwriting
        description= description,
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


checked = False


@app.route('/', methods = ["POST","GET"])

@app.route('/main',methods = ["POST","GET"])
def getMain():
    x = None

    if request.method == 'POST':
        x = request.data.decode("utf-8") # gets data then goes from bytes to string
        x = json.loads(x)
        container_logs[x["name"]] = x["data"]

        anomalies_csbytes = None
        anomalies_Scbytes = None
        anomalies_timeTaken = None

        anomalies_CpuTime = None
        anomalies_BytesSent = None
        anomalies_HttpResponseTime = None

        if x["name"] == "insights-logs-appservicehttplogs":


            anomalies_csbytes = x["data"][0]["anomalies"]["anomalies"] #Csbytes

        
            anomalies_Scbytes = x["data"][1]["anomalies"]["anomalies"] #ScStatus
 

            anomalies_timeTaken = x["data"][2]["anomalies"]["anomalies"] #TimeTaken


            if len(anomalies_csbytes) > 0 :
                createAlert("insights-logs-appservicehttplogs", "CsBytes", -1)
                
        
            if len(anomalies_Scbytes) > 0:
                createAlert("insights-logs-appservicehttplogs", "ScBytes", -1)
                

            if len(anomalies_timeTaken)>0:
                createAlert("insights-logs-appservicehttplogs", "Time Taken", -1)
                
        if x["name"] == "insights-metrics-pt1m":
            anomalies_CpuTime = x["data"][0]["anomalies"]["anomalies"] # CpuTime
    
            anomalies_BytesSent = x["data"][1]["anomalies"]["anomalies"] # Bytes Sent
    
            anomalies_HttpResponseTime = x["data"][2]["anomalies"]["anomalies"] # HTTP Response Time

            if len(anomalies_CpuTime) > 0 :
                createAlert("insights-metrics-pt1m", "CpuTime", -1)
                
        
            if len(anomalies_BytesSent) > 0:
                createAlert("insights-metrics-pt1m", "BytesSent", -1)
                

            if len(anomalies_HttpResponseTime)>0:
                createAlert("insights-metrics-pt1m", "HttpResponseTime", -1)
                
        # for i in range(0,len(container_logs["insights-logs-appservicehttplogs"])):
        #     curr_len = len(container_logs["insights-logs-appservicehttplogs"][i]["anomalies"]["anomalies"])
        #     curr_count = count_of_accesses[container_logs["insights-logs-appservicehttplogs"][i]["metricName"]["count"]]
        #     curr_indx = count_of_accesses[container_logs["insights-logs-appservicehttplogs"][i]["metricName"]["latest_index"]]

        #     if curr_indx != len(container_logs["insights-logs-appservicehttplogs"][0]["anomalies"]["anomalies"]):
        #         temp_count = len(container_logs["insights-logs-appservicehttplogs"][0]["anomalies"]["anomalies"])
        #         if temp_count > curr_count:
        #             if temp_count > 5:
        #                 count_of_accesses[container_logs["insights-logs-appservicehttplogs"][i]["metricName"]["count"]] = 0
        #                 print('send email')
        #             else:
        #                 count_of_accesses[container_logs["insights-logs-appservicehttplogs"][i]["metricName"]["count"]] = temp_count
        #             count_of_accesses[container_logs["insights-logs-appservicehttplogs"][i]["metricName"]["latest_index"]] = curr_len - 1



        # for i in range(0,len(container_logs["insights-metrics-pt1m"])):
        #     curr_len = len(container_logs["insights-metrics-pt1m"][i]["anomalies"]["anomalies"])
        #     curr_count = count_of_accesses[container_logs["insights-metrics-pt1m"][i]["metricName"]["count"]]
        #     curr_indx = count_of_accesses[container_logs["insights-metrics-pt1m"][i]["metricName"]["latest_index"]]

        #     if curr_indx != len(container_logs["insights-metrics-pt1m"][0]["anomalies"]["anomalies"]):
        #         # temp_count = len(x["insights-metrics-pt1m"][0]["anomalies"]["anomalies"])
 

        #         if temp_count > curr_count:
        #             if temp_count > 5:
        #                 count_of_accesses[container_logs["insights-metrics-pt1m"][i]["metricName"]["count"]] = 0
        #                 print('send email')
        #             else:
        #                 count_of_accesses[container_logs["insights-metrics-pt1m"][i]["metricName"]["count"]] = temp_count
        #             count_of_accesses[container_logs["insights-metrics-pt1m"][i]["metricName"]["latest_index"]] = curr_len - 1
        
                

        # First Scenario repeat Scenarios 
        



        
        




        
    return ('Rest API')

def createAlert(description, meteric, value):
    the_genie = opsgenieConfig(opsgenie_api_key)
    the_genie.create(description, meteric, value)




