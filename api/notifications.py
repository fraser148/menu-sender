'''
Send notifications to developer.
'''

from urllib.parse import urlencode
from urllib.request import Request, urlopen
import os
from dotenv import load_dotenv

load_dotenv()

private_key = os.getenv('PUSHSAFE')

def send_notification(title, message, icon=4):
  group = 'gs4273'
  title = f'[Menu Sender] {title}'

  if private_key is None:
    raise KeyError('No private key')

  url = 'https://www.pushsafer.com/api'
  post_fields = {
    't' : title,
    'm' : message,
    'v' : 3,
    'i' : icon,
    'd' : group,
    'k' : private_key,
  }

  request = Request(url, urlencode(post_fields).encode())
  json = urlopen(request).read().decode()
  return json
