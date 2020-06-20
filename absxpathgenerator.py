

from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.firefox.options import Options

url = "https://newartcenter.org/classes/"
WHITELIST = ["li", "tr", "p", "h2", "h3"]
TEST = 'div'

def xpath_soup(element):
    components = []
    child = element if element.name else element.parent
    for parent in child.parents:  # type: bs4.element.Tag
        siblings = parent.find_all(child.name, recursive=False)
        components.append(
            child.name if 1 == len(siblings) else '%s[%d]' % (
                child.name,
                next(i for i, s in enumerate(siblings, 1) if s is child)
                )
            )
        child = parent
    components.reverse()
    return '/%s' % '/'.join(components)

def get_paths(els):
    abs_xpaths = []
    for elem in els: 
        abs_xpaths.append("//*" + xpath_soup(elem))
    return abs_xpaths

opts = Options()
opts.headless = True
driver = webdriver.Firefox(options=opts)
driver.get(url)
page = driver.execute_script("return document.body.innerHTML").encode('utf-8')
soup = BeautifulSoup(page, "html.parser")
# print(soup.find_all)

elems = soup.find_all(TEST)

paths = get_paths(elems)
print(paths)



# def elems():
#     global elems
#     return elems



