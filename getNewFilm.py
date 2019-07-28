import urllib
from bs4 import BeautifulSoup
import requests
import re
import base64
import json

#http://kino-dom.tv/fec542a02ba81b9fb2bf63eaeda613cf/play/The-Outpost-2018-LostFilm.txt.json
BASEURL ="http://kino-dom.tv/"
Film = {}

page = requests.get("http://kino-dom.org/fantastika/3947-chernoe-zerkalo.html")

soup = BeautifulSoup(page.content, 'html.parser')

side_page_blocks = soup.find("div",class_ = "post-player") #.find_all("div")
Result = re.search('window.videoplayer = new Uppod\(\{m\:\"video\"\,uid\:\"videoplayer\"\,pl\:\"\/(.*?)\"', side_page_blocks.text)
if Result:
    session_str = Result.groups()[0] #  session ID

#get info
# div[class=post-content] -> div[class=post-title-eng]
side_page_blocks = soup.find("div",class_ = "post-content").find("div",class_="post-title-eng")
title = side_page_blocks.text
print(title)
Film['name'] = title
Film['provider_list'] = []
#img
# div[class=post-info] -> img[class=b-img-radius] src
side_page_blocks = soup.find("div",class_ = "post-info").find("img",class_="b-img-radius")
img_url = side_page_blocks.get('src')
imgB64 = base64.b64encode(requests.get(img_url).content) # img
provider = {}

#Film['imgB64'] = imgB64

#get provider
results = soup.select('span[data-link]')  #  player list (provider)
for prov in results:
    if prov.text == 'Основной плеер':
        continue
    datalink = prov.get('data-link')
    provider_ = {}
    provider_['season_list'] = []
    provider_name = prov.text
    jsonurl = BASEURL+session_str+datalink+'.json'
    djson = str(requests.get(jsonurl).text)
    data = json.loads(djson)
    for season in data['playlist']:
        season_ = {}
        season_name = season['comment'][-1]
        for part in season['playlist']:
            part_ = {"name":part['comment'][-1],"url":part['file'],"flag":"0"}
            #part_url = part['file']
            part_name = part['comment'][-1]
            season_[part_name] = part_
        provider_['season_list'].append({"name":season_name,"season":season_})
            # provider_[season_name] = season_
    provider_list = {"name":provider_name,"provider_list":provider_,"flagnew":0}
    Film['provider_list'].append(provider_)  #provider_list #= provider_ #[season_name][part_name] = {'name':part_name,'part_url':part_url}
    
    with open('output.json', 'w') as json_file:
        json.dump(Film, json_file)

    exit()
#results = soup.select('div[data-link]')

print(session_str)
print(Film)
#print(side_page_blocks)
