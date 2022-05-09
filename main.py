import datetime
from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
import emailsender
import pymongo
from dotenv import load_dotenv
import os

load_dotenv()

def getDate():
    today = datetime.date.today() + datetime.timedelta(days=0)
    dayT = today.strftime("%A")
    day = int(today.strftime("%d"))
    if 4 <= day <= 20 or 24 <= day <= 30:
        suffix = "th"
    else:
        suffix = ["st", "nd", "rd"][day % 10 - 1] 
    day = dayT + " " + str(day) + suffix + " " + today.strftime("%b")
    return day

def main():
    page = urlopen("https://www.exeter.ox.ac.uk/students/catering/weekly-dinner-menus/")
    soup = BeautifulSoup(page, "html.parser")

    menu_un = soup.find_all("p")
    menu = []
    for element in menu_un:
        menu.append(element.text)

    index = menu.index(getDate())
    end = index + 6 
    day = menu[index+1:end]

    index_break = day.index("***")

    day = day[0:index_break +2]

    menuFull = {"mains": []}

    veggie = False
    vegan = False

    for i in range(0,index_break-1):
        result = re.findall('\(.*?\)', day[i])
        if result:
            if result[0] == "(VE)":
                vegan = True
                day[i] = day[i].replace("(VE)", "")
            if result[0] == "(V)":
                veggie = True
                day[i] = day[i].replace("(V)", "")
        main = {"name": day[i], "veggie": veggie, "vegan": vegan}
        menuFull["mains"].append(main)

        veggie = False
        vegan = False
    sides = day[-3].split(', ')
    sides = [x.capitalize() for x in sides ]
    menuFull["sides"] = {"names": sides}
    menuFull["dessert"] = {"name": day[-1]}

    mon = os.environ['MONGO_URL']
    myclient = pymongo.MongoClient(mon)
    mydb = myclient["exeterMenu"]
    mycol = mydb["emails"]
    cursor = mycol.find({})
    recipients = []
    for document in cursor:
        recipients.append(document['email'])
        
    emailsender.send(recipients,menuFull)
        
if __name__ == "__main__":
    main()