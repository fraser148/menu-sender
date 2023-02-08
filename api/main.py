"""""""""
Menu Sender API
"""

import datetime
import re
import os
from urllib.request import urlopen
from bs4 import BeautifulSoup
import emailsender
import pymongo
from dotenv import load_dotenv
import logging
import notifications

load_dotenv()

logging.basicConfig(
  handlers=[logging.FileHandler(filename="./logs.log",
    encoding="utf-8",
    mode="a+")
  ],
  level=logging.DEBUG,
  format="%(asctime)s %(message)s",
  datefmt="%m/%d/%Y %I:%M:%S %p"
)

def get_date(delta=0):
  today = datetime.date.today() + datetime.timedelta(days=delta)
  day_full = today.strftime("%A")
  day = int(today.strftime("%d"))
  if 4 <= day <= 20 or 24 <= day <= 30:
    suffix = "th"
  else:
    suffix = ["st", "nd", "rd"][day % 10 - 1]
  day = day_full + " " + str(day) + suffix + " " + today.strftime("%B")
  print(day)
  return day

def get_menu():
  try:
    with urlopen("https://www.exeter.ox.ac.uk/students/catering/weekly-dinner-menus/") as page:
      soup = BeautifulSoup(page, "html.parser")

    menu_un = soup.find_all("h5")
    menu = []
    for element in menu_un:
      menu.append(element.text)

    index = menu.index(get_date())
    end = index + 6
    day = menu[index+1:end]

    index_break = day.index("***")

    day = day[0:index_break +2]

    menu_full = {"mains": []}

    veggie = False
    vegan = False
    halal = False

    # Check for dietary changes.
    for i in range(0,index_break-1):
      result = re.findall(r"\(.*?\)", day[i])
      if result:
        open_b = day[i].find("(")
        day[i] = day[i][:(open_b-1)]

        result = result[0][1:-1]
        results = result.split(", ")
        if "VE" in results:
          vegan = True
        if "V" in results:
          veggie = True
        if "halal" in results:
          halal = True
      main_meal = {"name": day[i], "veggie": veggie, "vegan": vegan, "halal": halal}
      menu_full["mains"].append(main_meal)

      veggie = False
      vegan = False
    sides = day[-3].split(", ")
    sides = [x.capitalize() for x in sides ]
    menu_full["sides"] = {"names": sides}
    menu_full["dessert"] = {"name": day[-1]}
    return menu_full
  except ValueError as e:
    print("Day is likely not included in menu")
    logging.exception(e)
    logging.info("Menu is not on website")
    notifications.send_notification("Menu not up", "The menu is not up on the website!")
    return "error"


def main():
  mon = os.environ["MONGO_URL"]
  myclient = pymongo.MongoClient(mon)
  mydb = myclient["exeterMenu"]
  mycol = mydb["tester"]
  cursor = mycol.find({})
  recipients = []

  try:
    env = os.environ["ENVIRONMENT"]

  except KeyError as e:
    logging.exception(e)
    notifications.send_notification("Error", "Environment variable not found")
    logging.error("Environment variable not found")
    return

  if env == "developer":
    try:
      dev_email = os.environ["DEV_EMAIL"]
      dev_name = os.environ["DEV_NAME"]
    except KeyError:
      print("Cannot find dev email")
      return

    recipients = [{'email': dev_email, 'name' : dev_name}]
    print(f"Dev email set to {dev_email}")

  elif env == "production":
    logging.info("Environment set to production. Sending to full list.")
    notifications.send_notification("Activated", "(Prod) Menu Sender has begun...")
    for document in cursor:
      try:
        temp = {'email': document["email"], 'name': document['name']}
      except:
        temp = {'email': document["email"], 'name': ''}
      recipients.append(temp)

    logging.info(recipients)

  else:
    logging.error("Invalid environment type")
    notifications.send_notification("Error", "Invalid environment type")
    raise Exception

  full_menu = get_menu()
  error = full_menu == "error"

  emailsender.send(recipients, full_menu, error)

if __name__ == "__main__":
  main()
