import pymongo
from dotenv import load_dotenv
import os
import requests

load_dotenv()

mon = os.environ["MONGO_URL"]
myclient = pymongo.MongoClient(mon)
mydb = myclient["exeterMenu"]
mycol = mydb["emails"]
cursor = mycol.find({})

recipients = []

for document in cursor:
  temp = {}
  try:
    temp['email'] = document["email"]
  except:
    temp['email'] = None
  try:
    temp['name'] = document["name"]
  except:
    temp['name'] = None
  try:
    temp['referral'] = document["referral"]
  except:
    temp['referral'] = None
  recipients.append(temp)

url = 'http://localhost:5000/recipient/subscribe'

for recipient in recipients:
  r = requests.post(url, json=recipient)
