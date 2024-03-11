import requests
import json

def runner():
    url = "http://localhost:5001/api/v1/run/ETL"

    payloadAmery = json.dumps({"location": ["Amery"]})
    payloadProtec = json.dumps({"location": ["Protec"]})
    headers = {"Content-Type": "application/json"}

    response = requests.request("POST", url, headers=headers, data=payloadProtec)

    print(response.text)

    response = requests.request("POST", url, headers=headers, data=payloadAmery)

    print(response.text)

    return "Run Successful For Amery & Protec"