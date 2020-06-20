# -*- coding: utf-8 -*-
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.firefox.options import Options
import argparse
import re
import html

undict ={'â€¦': '…',"â€ž":"„" ,'â€“': '–', 'â€™': '’', "â€\x9d":"”",
         "â€š":"„","â€°":"‰",
         'â€œ': '“', "â€”":'—', "Â\xad":" ",'Ã©':"é",'â‚¬':'€',
         "â€˜":"‘",'Â£':"£","Ã¢":"â","Â©":"©",'Ã£':"ã","Ãº":'ú',
         'Ã¤':'ä',"â€¢":"•",'Ã¡':'á','Ã¼':'ü',"Â¢":'¢',"Ã±":"ñ",
         'Â½':'Ž','Ã‰':'É','Â¥':'¥','Ã§':'ç','Ã´':'´','Â®':'®',
         'Â¦':'¦',"Ã¯":"ï",'Ã¶':'ö','Â´':"´","Ëœ":"˜",'Â»':'»',
         'Ã«':"ë","Ã‡":"Ç","Ã³":"ó","Ãµ":"õ","Ã®":"î","Â¾":'¾',
         "Â¼":"¼","Â°":"°","Ã–":"Ö","Ã¥":'å',"Ã¨":"è","Â¯":"¯",
         "Â¬":"¬","Ã„":"Ä","Â§":"§","Ãœ":"Ì","Â¤":"¤","Â·":'·',
         "Â±":"±","Ã²":"ò","Ãƒ":"Ã","ÃŸ":"ß","Ã’":"Ò",
         "Â¡":"¡","Ãª":"ê","Â«":"«",
         "Ã\x8d":"Í","Ã\x81":'Á',"Ã\xad":"í","Ã¦":"æ","Â¿":"¿","Ã¸":"ø",
         "Ã®":"î","Ã½":"ý","Ã»":"û","Ã¹":"ù","Å½":"Ž","Â¨":"¨","Âµ":"µ",
         "Â²":"²","Â³":"³","Ã¨":"è","Â¹":"¹","â„¢":"™","Ã¤":"ä","Ã“":"Ó"}

parser = argparse.ArgumentParser(description='Returns all text data, removing as much html as possible from the input text')

parser.add_argument('-a', dest="all", help="Scrape text from the whole html from a website, requires url")
parser.add_argument('-r', dest="robula", help="Scrape text from Robula output, requires a txt file filled with html")
parser.add_argument('-f', dest="fix", help="Slow down computation time, but fix some incorrectly encoded strings", action='store_true')
parser.add_argument('-o', dest="output", help="Write to an output file")

args = parser.parse_args()

flag = ""
if not (args.all or args.robula): 
    print("Need at least one argument")
    exit()

regex = "(?<=\>)[^>]+(?=\<)"
pattern = re.compile(regex)

if args.all: 
    flag = "ALL"
    opts = Options()
    opts.headless = True
    driver = webdriver.Firefox(options=opts)
    driver.get(args.all)
    page = driver.execute_script("return document.body.innerHTML")
    soup = BeautifulSoup(page, "html.parser")
    result = soup.find_all
    matches = pattern.findall(result)
    print(matches)
elif args.robula:
    flag = "ROBULA"
    text = ""
    all_matches = []
    with open(args.robula, "r") as f: 
        text = f.readlines()
    for line in text:
        all_matches.append(pattern.findall(line))
    filtered = []
    for item in all_matches: 
        if len(item) != 0: 
            for text in item: 
                if "\t" not in text:
                    true_text = html.unescape(text).encode('utf-8')
                    true_text = true_text.decode('utf-8')
                    if args.fix:
                        for item in undict: 
                            if item in true_text: 
                                # print(item)
                                fixed_text = true_text.replace(item, undict[item])
                                filtered.append(fixed_text)
                    else:
                        filtered.append(html.unescape(text).encode('cp1252', errors='ignore').decode('utf-8', errors='ignore'))
    
    if args.output: 
        with open(args.output, "w", encoding="utf-8") as f: 
            for line in filtered: 
                f.write(line + "\n")
    else: 
        print(filtered)
else: 
    flag = "NONE"

