'''
Menu Sender API
'''

import datetime
import re
import os
from urllib.request import urlopen
from bs4 import BeautifulSoup
import emailsender
import pymongo
from dotenv import load_dotenv

load_dotenv()

def get_date():
  today = datetime.date.today() + datetime.timedelta(days=-25)
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
  except Exception as e:
    print(e)
    return "error"


def main():
  mon = os.environ["MONGO_URL"]
  myclient = pymongo.MongoClient(mon)
  mydb = myclient["exeterMenu"]
  mycol = mydb["tester"]
  cursor = mycol.find({})
  recipients = []
  # for document in cursor:
  #   recipients.append(document["email"])

  recipients = ["fjrennie1@outlook.com"]

  full_menu = get_menu()
  error = full_menu == "error"

  emailsender.send(recipients,full_menu,error)

if __name__ == "__main__":
  main()