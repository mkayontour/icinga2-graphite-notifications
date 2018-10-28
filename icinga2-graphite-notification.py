#!/usr/bin/env python

import os
import base64
import argparse
import requests
import smtplib
import socket
from bs4 import BeautifulSoup
from jinja2 import Environment, FileSystemLoader
from requests.auth import HTTPBasicAuth
from email.MIMEImage import MIMEImage
from email.MIMEText import MIMEText
from email.MIMEMultipart import MIMEMultipart

ap = argparse.ArgumentParser()
ap.add_argument("-H", "--hostname", required=True, help="Icinga Hostname")
ap.add_argument("-a", "--hostaddress", help="Hostaddress")
ap.add_argument("-s", "--service", help="Icinga Servicename")
ap.add_argument("-S", "--state", help="Service /Host state")
ap.add_argument("-d", "--date", help="Date problem occured")
ap.add_argument("-t", "--template", help="Choose template",
  default="graphite-body.html.j2", nargs='?')
ap.add_argument("-c", "--comment", help="Comment")
ap.add_argument("-A", "--author", help="Comment Author")
ap.add_argument("-n", "--notification_type", help="notification_type")
ap.add_argument("-P", "--perfdata", help="perfdata")
ap.add_argument("-C", "--contact", help="Mail Recipient")
ap.add_argument("-o", "--output", help="Service or Host ouptut")
args = vars(ap.parse_args())

# Setup Defaults
# local postfix credentials only if needed
mailServer = 'localhost'
smtpPassword = ''
smtpUsername = ''
# Icinga Web Basic Auth Credentials
icingaWeb = 'http://localhost'
username = 'username'
password = 'password'
sender = 'no-reply@icinga.mail'
logo = 'icinga-logo.png'


i2 = {}
perf = {}
img_url = []
img_dict = {}
contact = args['contact']
i2['web_host'] = icingaWeb
i2["hostname"] = args["hostname"]
i2["service"] = args["service"]
i2["hostaddress"] = args["hostaddress"]
i2["state"] = args["state"]
i2["date"] = args["date"]
i2["template"] = args["template"]
i2["state"] = args['state']
i2["notification_type"] = args['notification_type']
i2["date"] = args['date']
i2["comment"] = args['comment']
i2["author"] = args['author']
i2["perfdata"] = args['perfdata']
i2["output"] = args['output']


if i2['service']:
  subject = i2['notification_type'] + ' at ' + i2['hostname'] + ' ' + i2['service']
else:
  subject = i2['notification_type'] + ' at ' + i2['hostname']

wd = os.path.dirname(os.path.abspath(__file__))
tpl = wd + '/templates'
#index = wd + '/index.html'
icinga_logo = wd + '/img/' + logo
env = Environment(loader=FileSystemLoader(tpl))

if i2['service']:
  url = i2['web_host'] + '/icingaweb2/graphite/list/'
  url += 'services?host=' + i2['hostname']
  url += '&service_description=' + i2["service"]
else:
  url = i2['web_host'] + '/icingaweb2/graphite/list/'
  url += 'hosts?host=' + i2['hostname']

if username and password:
  try:
    html = requests.get(url, auth=(username, password))
  except requests.exceptions.RequestException as e:
    print "Request to Icinga Web 2 failed: " + e.message
    os.sys.exit(e.errno)
else:
  try:
    html = requests.get(url)
  except requests.exceptions.RequestException as e:
    print "Request to Icinga Web 2 failed: " + e.message
    os.sys.exit(e.errno)

soup = BeautifulSoup(html.text, 'html.parser')

for html in soup.find_all('div', attrs={"class":"images"}):
  for src in html.find_all('img'):
    src_url = i2['web_host'] + src.get('src')
    src_url = src_url.replace("width=350","width=640")
    img_url.append(src_url)

counter = int()
for g in img_url:
    try:
      graph_img = requests.get(g)
    except requests.exceptions.RequestException as e:
      print "Request to Icinga Web 2 failed: " + e.message
      continue
    counter += 1
    img_dict[str(counter)]= graph_img.content

pdata = i2['perfdata'].split(" ")
for p in pdata:
    if '=' not in p:
        continue

    (label,data) = p.split("=")
    if (len(data.split(";")) is 5):
        perf[label] = {}
        (perf[label]["val"],
        perf[label]["warn"],perf[label]["crit"]
        ,perf[label]["min"],perf[label]["max"]) = data.split(";")

    elif (len(data.split(";")) is 4):
        perf[label] = {}
        (perf[label]["val"],perf[label]["warn"]
        ,perf[label]["crit"],perf[label]["min"]) = data.split(";")

    else:
        perf[label] = {}
        perf[label]['val'] = data

template = env.get_template(i2['template'])
html_mail = template.render(d_i2=i2,img_dict=img_dict,perfdata=perf)

mailBase = MIMEMultipart('related')
mailBase['Subject'] = subject
mailBase['From'] = sender
mailBase['To'] = contact
mailBase.preamble = 'This is a multi-part message in MIME format.'
mailAlt = MIMEMultipart('alternative')
mailBase.attach(mailAlt)

mailText = MIMEText(html_mail, 'html')
mailAlt.attach(mailText)

if os.path.exists(icinga_logo):
    logo = open(icinga_logo, 'rb')
    mailImage = MIMEImage(logo.read())
    logo.close()
    mailImage.add_header('Content-ID', '<icinga-logo>')
    mailBase.attach(mailImage)

if img_dict:
  for key, value in img_dict.items():
    mailImage = MIMEImage(value, _subtype="png")
    mailImage.add_header('Content-ID', '<graphite-graph-' + key + '>')
    mailBase.attach(mailImage)

smtp = smtplib.SMTP()
try:
  smtp.connect(mailServer)
except socket.error as e:
  print "Unable to connect to SMTP server '" + mailServer + "': " + e.strerror
  os.sys.exit(e.errno)

if (smtpUsername and smtpPassword):
  smtp.login(smtpUsername, smtpPassword)

try:
  smtp.sendmail(sender, contact, mailBase.as_string())
  smtp.quit()
except Exception as e:
  print "Cannot send mail using SMTP: " + e.message
  os.sys.exit(e.errno)

os.sys.exit(0)
