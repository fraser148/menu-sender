'''
Sends emails given the recipients and menu. Will format the menu based on the given template.
'''

import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.utils import formataddr
from datetime import date
import os

def format_menu(menu):
  vegan = """<span style="background-color:grey;border-radius: 20px; padding: 1px 10px; color: white; background-color: #21B584; margin-left:5px">Vegan</span>"""
  veggie = """<span style="background-color:grey;border-radius: 20px; padding: 1px 10px; color: white; background-color: #21B584; margin-left:5px">Veggie</span>"""
  halal = """<span style="background-color:grey;border-radius: 20px; padding: 1px 10px; color: white; background-color: #21B584; margin-left:5px">Halal</span>"""

  with open("content.html", encoding="UTF-8") as html:
    template = html.read()

  # Get today's long date
  date_today = date.today().strftime("%d/%m/%y")

  # Replace all inputs
  template = template.replace("{{date}}", date_today)

  # Replace mains section and add dietary extras.
  for item in menu["mains"]:
    template = template.replace("{{main1}}", item["name"],1)
    if item["vegan"]:
      template = template.replace("{{diet}}", vegan,1)
    elif item["veggie"]:
      template = template.replace("{{diet}}", veggie,1)
    else:
      template = template.replace("{{diet}}", "",1)

    if item["halal"]:
      template = template.replace("{{halal}}", halal, 1)
    else:
      template = template.replace("{{halal}}", "", 1)

  # Remove spare main templates
  template = template.replace("{{main1}}{{diet}}{{halal}}", "")

  # Replace side templates
  for item in menu["sides"]["names"]:
    template = template.replace("{{side}}", item ,1)

  template = template.replace("{{side}}", "")

  # Replace dessert templates
  if menu["dessert"]:
    template = template.replace("{{dessert}}", menu["dessert"]["name"])
  else:
    template = template.replace("{{dessert}}", "")

  # Return the altered template
  return template


def send(recipients, message, menu, error):
  sender_email = os.environ["EMAIL_ACCOUNT"]
  password = os.environ["EMAIL_PASS"]

  text = """\
  Dear user,
  Something has gone wrong (500).
  Many Thanks,
  Menu Sender"""

  if error:
    print("Sending Problem template!")
    with open("problem.html", encoding="UTF-8") as html:
      original = html.read()

  else:
    original = format_menu(menu)

  original = original.replace("{{custom_message}}", message)

  # Create secure connection with server and send email
  context = ssl.create_default_context()

  with smtplib.SMTP_SSL("mail.oxtickets.co.uk", 465, context=context) as server:
    server.login(sender_email, password)
    for receiver in recipients:
      name = ""
      ref_name = ""
      if receiver['name'] == None:
        name = receiver['email'].split(".")[0].capitalize()
        names = receiver['email'].split("@")[0]
        names = names.split(".")
        ref_name = " ".join(names)
      else:
        name = receiver['name'].split(" ")[0].capitalize()
        ref_name = receiver['name']

      msg = original.replace("{{name}}", name)
      msg = msg.replace("{{ref}}",f"https://exeter.oxtickets.co.uk?referral={ref_name}")
      msg = msg.replace("{{ref}}",f"https://exeter.oxtickets.co.uk?referral={ref_name}")

      message = MIMEMultipart("alternative")
      message["Subject"] = "Exeter College Menu"
      message["From"] = formataddr(("Menu Sender", sender_email))

      part1 = MIMEText(text, "plain")
      part2 = MIMEText(msg, "html")

      # Add HTML/plain-text parts to MIMEMultipart message
      # The email client will try to render the last part first
      message.attach(part1)
      message.attach(part2)

      message["To"] = receiver['email']
      print("Sent to: " + receiver['email'])
      server.sendmail(sender_email, receiver['email'], message.as_string())
      message["To"] = ""
