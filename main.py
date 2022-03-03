import requests
import urllib3
import json
import dns.resolver
import pandas as pd
import time
import sys
import matplotlib.pyplot as plt
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
#api_token = sys.argv[1]
#action = sys.argv[2]+'()'

def auth_user():
   
   session = requests.Session()
   session.verify = False
   url = 'https://ucns01.dlas1.ucloud.int/authenticate'
   data = {
	        "username": "admin",
		    "password": "***"
	        }
   res=session.put(url, data=json.dumps(data))
   print(res.status_code)
   for i in res:
       print(i)


def add_records():
    session = requests.Session()
    session.verify = False
    df = pd.read_csv('data/records.csv', sep=',')
    records = df.values
    length = len(records)
    answer =[]
    for i in range(length):
        url = "https://ucns01."+records[i][0]+".ucloud.int/zone/"+records[i][0]+".ucloud.int"
        headers = {"Content-Type": "application/json", "x-authentication-token": "**"}
        data = {
	        "records": [{
		    "name": records[i][1],
		    "type": records[i][2],
		    "content": records[i][3],
		    "ttl": records[i][4]
	            }]
            }
        
        res=session.put(url, data=json.dumps(data), headers=headers)
        print(res.status_code)
        if res.status_code != 200:
            print(f"adding of record failed for {url} ")
        try: 
            start = time.time()   
            a=dns.resolver.resolve(records[i][1],records[i][2])
            end = time.time()
            answer.append(a)
        except Exception as e:
            print(f"exception :" ,e)

        x = records[i][0]
        y = end - start

        for a,b in a.rrset.items.items():
            print(f"{a} has a resolution of {y} secs")
        
        plt.scatter(x,y)
    
    plt.xlabel('DC/zone')
    plt.ylabel('time to resolution (seconds)') 
    plt.show()
    plt.close()     
        

def delete_records():
    session = requests.Session()
    session.verify = False
    df = pd.read_csv('data/records.csv', sep=',')
    records = df.values
    length = len(records)
    answer =[]
    for i in range(length):
        url = "https://ucns01."+records[i][0]+".ucloud.int/zone/"+records[i][0]+".ucloud.int"
        headers = {"Content-Type": "application/json", "x-authentication-token": "xGaFvNnTDOy_Z8h22wrei_Gti8lR3XOavENitlWX0eU="}
        data = {
	        "records": [{
		    "name": records[i][1],
		    "type": records[i][2],
		    "content": records[i][3],
		    "ttl": records[i][4],
            "mode": "delete"
	            }]
            }
        res=session.post(url, data=json.dumps(data), headers=headers)
        print(res.status_code)
        if res.status_code != 200:
            print(f"deleting of record failed for {url} ")
       

    
if (__name__ == '__main__'):
    add_records()
    #auth_user()
    #delete_records()
