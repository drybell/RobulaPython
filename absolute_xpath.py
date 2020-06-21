# GIVEN A KEYWORD AND A DOM, FIND THE WEBELEMENT (USING SELENIUM) CONTAINING THE TEXT, THEN LOCATE THE ABS XPATH 

from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.firefox.options import Options
from lxml import html, etree

text_keywords = ['event', 'Event', 'Art', 'art']
class_keywords = ['event', 'title',]
id_keywords = ['event', 'title']

url = "https://newartcenter.org/classes"

opts = Options()
opts.headless = True
driver = webdriver.Firefox(options=opts)
driver.get(url)
page = driver.execute_script("return document.body.innerHTML").encode('utf-8')
document = html.fromstring(page)

def getAbsXpaths(document, text):
    tree = etree.ElementTree(document)
    e = document.xpath('//*[contains(text(),' + '"' + text + '")]')
    return ["//*" + tree.getpath(sub) for sub in e]

driver.close()




