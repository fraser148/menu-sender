'''
Sends emails given the recipients and menu.
'''

import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.utils import formataddr
from datetime import date
import os

def send(recipients, menu, error):
  sender_email = os.environ["EMAIL_ACCOUNT"]
  password = os.environ["EMAIL_PASS"]

  text = """\
  Dear user,
  Something has gone wrong (500).
  Many Thanks,
  Menu Sender"""

  vegan = """<span style="background-color:grey;border-radius: 20px; padding: 1px 10px; color: white; background-color: #21B584; margin-left:5px">Vegan</span>"""
  veggie = """<span style="background-color:grey;border-radius: 20px; padding: 1px 10px; color: white; background-color: #21B584; margin-left:5px">Veggie</span>"""
  halal = """<span style="background-color:grey;border-radius: 20px; padding: 1px 10px; color: white; background-color: #21B584; margin-left:5px">Halal</span>"""

  if error:
    with open("problem.html", encoding="UTF-8") as html:
      original = html.read()

  else:
    with open("content.html", encoding="UTF-8") as html:
      original = html.read()


    # Get today's long date
    date_today = date.today().strftime("%d/%m/%y")

    # Replace all inputs
    original = original.replace("{{date}}", date_today)
    for item in menu["mains"]:
      original = original.replace("{{main1}}", item["name"],1)
      if item["vegan"]:
        original = original.replace("{{diet}}", vegan,1)
      elif item["veggie"]:
        original = original.replace("{{diet}}", veggie,1)
      else:
        original = original.replace("{{diet}}", "",1)

      if item["halal"]:
        original = original.replace("{{halal}}", halal, 1)
      else:
        original = original.replace("{{halal}}", "", 1)

    original = original.replace("{{main1}}{{diet}}{{halal}}", "")

    for item in menu["sides"]["names"]:
      original = original.replace("{{side}}", item ,1)

    original = original.replace("{{side}}", "")

    if menu["dessert"]:
      original = original.replace("{{dessert}}", menu["dessert"]["name"])
    else:
      original = original.replace("{{dessert}}", "")

  # Create secure connection with server and send email
  context = ssl.create_default_context()
  try:
    with smtplib.SMTP_SSL("mail.oxtickets.co.uk", 465, context=context) as server:
      server.login(sender_email, password)
      for receiver in recipients:
        name = receiver.split(".")[0].capitalize()
        msg = original.replace("{{name}}",name)

        message = MIMEMultipart("alternative")
        message["Subject"] = "Exeter College Menu"
        message["From"] = formataddr(("Menu Sender", sender_email))

        part1 = MIMEText(text, "plain")
        part2 = MIMEText(msg, "html")

        # Add HTML/plain-text parts to MIMEMultipart message
        # The email client will try to render the last part first
        message.attach(part1)
        message.attach(part2)

        message["To"] = receiver
        print("Sent to: " + receiver)
        server.sendmail(sender_email, receiver, message.as_string())
        message["To"] = ""

  except Exception as e:
    print(e)
    print("failed")
