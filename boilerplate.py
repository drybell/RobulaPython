# Daniel Ryaboshapka and Sam Chung 
# Robula+ Implementation in Python 3.7 
# 

from bs4 import BeautifulSoup 
from selenium import webdriver 
import argparse
from selenium.webdriver.firefox.options import Options
from lxml import html
import re 

TARGET = 2

# ALL COMMENTS ABOVE TRANSITION FUNCTIONS PROVIDED BY ROBULA+ AUTHORS 
# INSERT LINK HERE

### NAME DEFINITIONS 
#  xp = The XPATH expression to specialize --> //td 
#  N  = The length (in nodes/levels) of variable xp --> //td => N=1
#														//*//td => N=2
#  L  = The list of the ancestors of target elem e in the considered DOM,
#       starting and including e 
### 

### DESIGN CHOICES ### 
# 
# WE ARE TRYING TO MAKE GENERIC ROBUST XPATHS, NOT JUST A RELATIVE FROM ABSOLUTE THAT 
# HAS THE SAME AMOUNT OF SPECIFIC INFO
# 
# EXAMPLE AND PROTOTYPE WORKFLOW: if i like to peruse newartcenter.org, 
#                                 and I know that there is an events page, let's pull the
#                                 first event as the xpath from inspect element and shove it
#                                 into Russian Robula, or our Robula when it's functional
#                                 this can be done by any human. 
#                                 WHAT WE WANT IS THE GENERIC XPATH THAT GIVES US ALL OF THE EVENTS 
# 
# WE WANT TO ADD TRANSFCLASS AND REMOVE ANY DETAILED TRANSFORMATIONS LIKE TRANSFADDTEXT AND ADDPOSITION
# ADD WEIGHTS TO CREATE A PRIORITY LIST WITH BEST CHOICES FOR GENERIC XPATH AT THE FRONT OF THE LIST

### 7 TRANFORMATIONS

# Precondition: Xpath xp starts with //* 
#       Action: replace initial * with tag name of the DOM elem L.get(N)
#      Example: INPUT:  xp = //*/td and L.get(2).getTagName() = tr  
#				OUTPUT: //tr//td
def transfConvertStar(xp, tagname):
    if xp.startswith('//*'):
        xp = xp.replace('*',tagname)
    return xp 

# Precondition: the Nth level of xp does not contain already any kind of predicates 
#       Action: for each available attribute-value pair of the DOM element L.get(N), generate a 
#				candidate locator by adding a predicate based on such value 
#				to the higher level of xp
#      Example: INPUT:  xp = //tr/td & L.get(2).getAttributes() = {name: 'data', class: 'table-row'}
#				OUTPUT: //tr[@name='data']/td & //tr[@class='table-row']/td


def transfAddAttribute(xp, attributes, tagname):
    # parse attributes 
    temp = xp.replace("//", "")
    elements = temp.split("/")
    target = elements[0]
    attrstrings = []
    xpaths = [] 
    if attributes != []: 
        for key in attributes: 
            attrstrings.append("[@" + key + "=\"" + attributes[key][0] + "\"]")
        for attr in attrstrings: 
            xpaths.append('//' + target + attr + xp[(2+len(target)):])
    return xpaths

# Precondition: the Nth level of xp does not contain already any predicate on position
#       Action: add the position of the element L.get(N) to the higher level of xp 
#      Example: INPUT:  xp = //tr/td and L.get(2).getPosition() = {if tag-name=2, if '*'=3}
#				OUTPUT: //tr[2]/td
def transfRemovePosition():
    return None 

# Precondition: N < L.length()
#       Action: add //* at the top of xp 
#      Example: INPUT:  //tr//td
#				OUTPUT: //*/tr/td
def transfAddLevel(xp, n, l):
    if n < l: 
        xp = xp.replace("//", "/")
        return "//*" + xp
    else: 
        return xp 

# assert transfAddLevel('') == 


### AUXILARY FUNCTIONS 

# return the depth of the element 
def N(xp): 
    return len(xp.split("/")) - 2

def L(xpath): 
    temp = xpath.replace("//", "")
    elements = temp.split("/")
    if temp[-1] == "/":
        elements.pop()
    
    return elements


# returns the element in dom selected by the xpath locator xpath
def eval(xpath, document):
    return document.xpath(xpath)

# TRUE iff eval(x, d) contains only e
# Has to be changed to uniquely locates as we are making a generic xpath
# Algorithm: If the xpath generated sends us back the same list of elems,
# then the xpath can generalize to finding a group of elems
def generalLocates(xpath, document, elem):
    # Query the document using the xpath passed in
    # if the result is similar to elems, then return True,
    # else return False 
    # TESTING REQUIRED, BUT BEING 1 or 2 off is our current design choice 
    elems = eval(xpath, document)
    elems = [html.tostring(elem).decode('utf-8') for elem in elems]
    # print("XPATH: " + xpath)
    # print("ELEM: " + elem)
    # print("ELEMS: ", elems)
    return elem in elems

def getAttributes(elem, tagname):
    # Parse tagname and remove positions first 
    pattern = re.compile(r'(\[[\d]*)')
    match = pattern.findall(tagname)
    fixed = ""
    if len(match) > 0:
        match = pattern.findall(tagname)[0] + "]"
        fixed = tagname.replace(match, "")
    else: 
        fixed = tagname
    soup = BeautifulSoup(elem, 'lxml')
    # print("Tagname: " + fixed)
    tag = soup.find(fixed)
    if tag == None:
        # tags = soup.find("class")
        return [] 
    else:
        return tag.attrs

def RobulaPlus(xpath, elems, pathL, doc): 
    xpath_list = []
    for elem in elems:
        # print("IM HERE")
        stringified = html.tostring(elem).decode('utf-8')
        print("ELEM: " + stringified)
        XList = ["//*"]
        while True:
            xp = XList.pop(0) # pop front of list
            temp = []
            currN = pathL[N(xp) - 1]
            xp1 = transfConvertStar(xp, currN)
            temp.append(xp1)
            # print("BEFORE ADD ATTRIBUTES: ", temp)
            xp2 = transfAddAttribute(xp1, getAttributes(stringified, currN), currN)
            if len(xp2) >= 1:
                for x in xp2: 
                    temp.append(x) 
                    temp.append(transfAddLevel(x, N(x), len(pathL)))
                    # print("AFTER ADD ATTRIBUTES: ", temp)
            else: 
                temp.append(transfAddLevel(xp1,N(xp1), len(pathL)))
                # print("AFTER ADD ATTRIBUTES ELSE: ", temp)

            # print(temp)
            for t in temp[::-1]: 
                if generalLocates(t, doc, stringified):
                    xpath_list.append(t)
                    if len(xpath_list) == TARGET: 
                        return xpath_list
                else: 
                    XList.append(t)

def Parse():
    parser = argparse.ArgumentParser(description='First attempt to auto-generate unique descriptive xpaths')

    parser.add_argument('-u', dest="url", help="Specify a url to capture valid xpaths")
    parser.add_argument('-x', dest="xpath", help="Specify an xpath, if quotes (\"\") are included, please backslash escape them", default="//*")

    args = parser.parse_args()
    if (not args.url) or (not args.xpath):
        print("use both url flag AND xpath flag")
        exit()
    else:
        return args

def main(): 
    args = Parse()
    url = args.url
    xpath = args.xpath
    print("Working url: %s" % (url))
    print("Working xpath: %s" % (xpath))
    opts = Options()
    opts.headless = True
    driver = webdriver.Firefox(options=opts)
    driver.get(url)
    page = driver.execute_script("return document.body.innerHTML").encode('utf-8')
    # soup = BeautifulSoup(page, "html.parser")
    document = html.fromstring(page)
    # print(html.tostring(document).decode('utf-8'))

    elems = eval(xpath, document)
    pathL = L(xpath)
    print(pathL)
    new_xpaths = RobulaPlus(xpath, elems, pathL[::-1], document)
    # filter out all xpaths with star as final check 
    filtered = []
    for xp in new_xpaths: 
        if "//*" not in xp: 
            filtered.append(xp)

    print("OVERALL XPATHS FOUND: ", new_xpaths)
    print("FILTERED XPATHS FOUND: ", filtered)

    # TAKING ALL URLS FROM FIRST XPATH FROM FILTERED
    # with open("mfa-urls.txt", "w") as f: 
    #     xpath = filtered[0]
    #     elems = eval(xpath, document)
    #     elems = [html.tostring(elem).decode('utf-8') for elem in elems]
    #     for elem in elems: 
    #         url = elem.split("href=")
    #         f.write(url[1])

    # TAKING ALL ps FROM FILTERED     
    # with open("desc.txt", "w") as f: 
    #     xpath = filtered[0]
    #     elems = eval(xpath, document)
    #     elems = [html.tostring(elem).decode('utf-8') for elem in elems]
    #     for elem in elems: 
    #         url = elem.split("<p>")
    #         f.write(url[1])

    # DATES
    with open("mfa-title.txt", "w") as f: 
        xpath = filtered[0]
        elems = eval(xpath, document)
        elems = [html.tostring(elem).decode('utf-8') for elem in elems]
        for elem in elems: 
            f.write(elem + "\n")
        print(len(elems))
    driver.close()
    driver.quit()

if __name__ == '__main__':
    main()


# title       : //a[@class="url"]/text()
# description : //div[3][@class="fusion-post-content-container"]
# date        : //span[1][@class="tribe-event-date-start"]
    