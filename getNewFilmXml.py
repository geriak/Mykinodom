import sys,os
import urllib
from bs4 import BeautifulSoup
import requests
import re
import base64
import json
import mod.tolatin as convertLatin

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
with open('output.xml', 'w',encoding='utf-8') as xfile:
    xfile.write("<film>")
    
    side_page_blocks = soup.find("div",class_ = "post-content").find("div",class_="post-title-eng")
    title = side_page_blocks.text
    print(title)
    xfile.write("<name>%s</name>" % title)
    #img
    # div[class=post-info] -> img[class=b-img-radius] src
    side_page_blocks = soup.find("div",class_ = "post-info").find("img",class_="b-img-radius")
    img_url = side_page_blocks.get('src')
    imgB64 = base64.b64encode(requests.get(img_url).content) # img
    provider = {}
    
    xfile.write("<img>%s</img>" % os.path.basename(img_url))
    xfile.write("<imgsrc>%s</imgsrc>" % img_url)
    
    #Film['imgB64'] = imgB64

    xfile.write("<players>")
    results = soup.select('span[data-link]')  #  player list (provider)
    for prov in results:
        if prov.text == 'Основной плеер':
            continue
        
        datalink = prov.get('data-link')
      
        idpls = convertLatin.translit1(prov.text)
        xfile.write('<player id="%s" name="%s" flagnew="0">' % (idpls,prov.text,))
        jsonurl = BASEURL+session_str+datalink+'.json'
        djson = str(requests.get(jsonurl).text)
        data = json.loads(djson)
        xfile.write("<seasons>")
        for season in data['playlist']:
            
            xfile.write('<season id="%s" name="Season %s" flagnew="0">' % (season['comment'][-1],season['comment'][-1],))
            xfile.write("<parts>")
            for part in season['playlist']:
                #part_ = {"name":part['comment'][-1],"url":part['file'],"flag":"0"}
                #part_url = part['file']
                #part_name = part['comment'][-1]
                xfile.write('<part id="%s" name="Part %s" flagnew="0" prefixurl="" resolution=""/>' %
                            (part['comment'][-1], part['comment'][-1],))
           
            xfile.write('</parts>')
            xfile.write("</season>")
        xfile.write("</seasons>")
        xfile.write("</player>")
        
    xfile.write("</players>")
    xfile.write("</film>")
    xfile.close()

print(session_str)

#print(side_page_blocks)
