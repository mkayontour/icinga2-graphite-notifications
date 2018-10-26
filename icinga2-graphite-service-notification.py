#!/usr/bin/env python

from bs4 import BeautifulSoup
from jinja2 import Environment, FileSystemLoader
import requests
import base64

file_loader = FileSystemLoader('templates')

env = Environment(loader=file_loader)

icingaweb_host = "http://192.168.33.5"
icinga_hostname = "icinga2"
icinga_srv_desc = "http Icinga RT"

url = icingaweb_host + '/icingaweb2/graphite/list/'
url += 'services?host=' + icinga_hostname
url += '&service_description=' + icinga_srv_desc

html = requests.get(url)
html_content = html.text
img_url = []
img_list = []
soup = BeautifulSoup(html_content, 'html.parser')

for html in soup.find_all('div', attrs={"class":"images"}):
  for src in html.find_all('img'):
    src_url = icingaweb_host + src.get('src')
    img_url.append(src_url)

print(img_url)

for g in img_url:
    graph_img = requests.get(g)
    img_list.append(base64.b64encode(graph_img.content))
    #print(img_list) + "\n"


template = env.get_template("test-jinja")
output = template.render(img_list=img_list)
file = open("index.html","w")
file.write(output)
file.close()

#HTML = '<table class="editorDemoTable" style="vertical-align: top;">'
#HTML +='\n<thead>'
#HTML +='\n<tr style="height: 83px;">'
#HTML +='\n<td style="background-color: #1093bc; height: 83px;" colspan="3"><img src="https://icinga.com/wp-content/uploads/2014/06/logo_icinga_white-e1407071914762.png" alt="icinga_logo" width="200" height="78" /></td>'
#HTML +='\n</tr>'
#HTML +='\n</thead></table>'
#for i in img_list:
#  HTML +='\n<p><img src="data:image/png;base64 ,' + i + '",alt="red Dot" style="display: block; margin-left: auto; margin-right: auto;"/></p>'



#file = open("testfile","w")
#file.write(HTML)
#file.close()
#
