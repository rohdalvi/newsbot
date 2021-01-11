from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from apiclient import errors
from nyt import getHeadlines
from iex import getQuote, getSeries
import base64
from datetime import date
import codecs
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path
import mimetypes


# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://mail.google.com/', 'https://www.googleapis.com/auth/gmail.compose']

def main():
    """Shows basic usage of the Gmail API.
    Lists the user's Gmail labels.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('gmail', 'v1', credentials=creds)

    # Call the Gmail API
    results = service.users().labels().list(userId='me').execute()
    labels = results.get('labels', [])

    #create message
    
    date_today = date.today().strftime("%B %d, %Y")
    
    subject = "Newsbot " + date_today
    message = "<html>"
    message = "<h2>" + "Newsbot " + date_today + "</h2>" 

    nyt_dict = getHeadlines("world")
    message = write_nyt_message(nyt_dict, message, "World")
    message = message + '<a href="https://www.nytimes.com/section/world">NYT World</a>'

    nyt_dict = getHeadlines("us")
    message = write_nyt_message(nyt_dict, message, "US")
    message = message + '<a href="https://www.nytimes.com/section/us">NYT US</a>'

    
    message = message + '<h2 style="font-style: italic;">' + "Selected Stock Prices" + "</h2>" 
    iex_quote = getQuote("BA")
    message = write_iex_quote(iex_quote, message, "BA")

    iex_quote = getQuote("VTI")
    message = write_iex_quote(iex_quote, message, "VTI")

    iex_quote = getQuote("VOO")
    message = write_iex_quote(iex_quote, message, "VOO")

    iex_series = getSeries("BA", "1y")
    x = np.linspace(0, 252, 253)
    plt.plot(x, iex_series, label="BA")
    plt.xlabel('1 Year')
    plt.ylabel('Price ($)')
    plt.savefig(os.path.join(os.path.dirname(__file__), "BA.png"), dpi=300, format='png')

    
    message = message +  '<img src="cid:mailImage"/>'

    #message = message + "<\html>"
    m = create_message('rdalvin24@gmail.com', 'rdalvin24@gmail.com', subject, message, 'BA.png')
    send_message(service, 'me', m)

def write_nyt_message(infodict, message, topic):
  message = message + '<h2 style="font-style: italic;">' + topic + "</h2>" 
  for key in infodict:
    message =  message + "<h4>" + key + "</h4>" + "<p>" + infodict[key] + "</p>"
  return message

def write_iex_quote(quote, message, symbol):
  quote_str = str(quote)
  message = message + "<h4>" + symbol + ": " + quote_str + "</h4>"  
  return message

def create_message(sender, to, subject, message_text, filename):
  """Create a message for an email.

  Args:
    sender: Email address of the sender.
    to: Email address of the receiver.
    subject: The subject of the email message.
    message_text: The text of the email message.

  Returns:
    An object containing a base64url encoded email object.
  """
  msg = MIMEMultipart()
  msg['to'] = to
  msg['from'] = sender
  msg['subject'] = subject

  message = MIMEText(message_text, 'html')

  msg.attach(message)

  filepath = Path('BA.png').absolute()
  content_type, encoding = mimetypes.guess_type(str(filepath))

  if content_type is None or encoding is not None:
    content_type = 'application/octet-stream'
  main_type, sub_type = content_type.split('/',1)
  if main_type == 'text':
    fp = open(filepath, 'rb')
    message = MIMEText(fp.read(), _subtype=sub_type)
    fp.close()
  elif main_type == 'image':
    fp = open(filepath, 'rb')
    message = MIMEImage(fp.read(), _subtype=sub_type)

  msg.add_header('Content-Disposition', 'attachment', filename=filename)
  msg.attach(message)
  return {'raw': base64.urlsafe_b64encode(message.as_string().encode()).decode()}

def send_message(service, user_id, message):
  """Send an email message.

  Args:
    service: Authorized Gmail API service instance.
    user_id: User's email address. The special value "me"
    can be used to indicate the authenticated user.
    message: Message to be sent.

  Returns:
    Sent Message.
  """
  try:
    message = (service.users().messages().send(userId=user_id, body=message)
               .execute())
    print('Message Id: %s' % message['id'])
    return message
  except Exception as error:
    print('An error occurred: %s' % error)  

if __name__ == '__main__':
    main()