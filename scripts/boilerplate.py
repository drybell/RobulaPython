# Daniel Ryaboshapka and Sam Chung 
# Robula+ Implementation in Python 3.7 
# Instead of Robula+, its Robula-  

from bs4 import BeautifulSoup 
from selenium import webdriver 
import argparse
from selenium.webdriver.firefox.options import Options
from lxml import html, etree
import re 
from absolute_xpath import getAbsXpaths
from timeout import timeout, TimeoutError

TARGET = 4
XLIST_TARGET = 100
XLIST_RETURN = 10
blacklist_tags = ['href', 'id', 'role', 'type']
TIMEOUT = 10

# ALL COMMENTS ABOVE TRANSITION FUNCTIONS PROVIDED BY ROBULA+ AUTHORS 
# WE ADAPTED OUR TRANSFORMATION CODE FROM THE ROBULA+ ALGORITHM

#########################################################################
###                        NAME DEFINITIONS                           ###
###                                                                   ###
###  xp = The XPATH expression to specialize --> //td                 ###
###  N  = The length (in nodes/levels) of variable xp                 ###
###                |--> //td => N=1                                   ###
###						//*//td => N=2                                ### 
###  L  = The list of the ancestors of target elem e in the           ### 
###                 considered DOM, starting and including e          ###
###                                                                   ###
#########################################################################

#########################################################################
###                        TRANFORMATIONS                             ###
###                                                                   ###
#########################################################################


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
# TODO: Maybe make attribute parsing a function? Esp with blacklist involved...
def transfAddAttribute(xp, attributes, tagname):
    global blacklist_tags
    temp = xp.replace("//", "")
    elements = temp.split("/")
    target = elements[0]
    xpaths = []
    if "[@" in target: 
        xpaths.append('//' + target + xp[(2+len(target)):])
        return xpaths
    attrstrings = [] 
    seen_keys = []
    if attributes != []: 
        for key in attributes: 
            if key not in blacklist_tags and key not in seen_keys:
                if type(attributes[key]) == list:
                    if key == "class": 
                        full_attribute = ""
                        for item in attributes[key]:
                            full_attribute += item + " "
                        full_attribute = full_attribute[:-1]
                        attrstrings.append("[@" + key + "=\"" + full_attribute + "\"]")
                    else:
                        attrstrings.append("[@" + key + "=\"" + attributes[key][0] + "\"]")
                else: 
                    attrstrings.append("[@" + key + "=\"" + attributes[key] + "\"]")
            seen_keys.append(key)
        for attr in attrstrings: 
            xpaths.append('//' + target + attr + xp[(2+len(target)):])
    return xpaths

# Precondition: the Nth level of xp does not contain already any predicate on position
#       Action: add the position of the element L.get(N) to the higher level of xp 
#      Example: INPUT:  xp = //tr/td and L.get(2).getPosition() = {if tag-name=2, if '*'=3}
#				OUTPUT: //tr[2]/td
def transfRemovePosition(tagname):
    pattern = re.compile(r'(\[[\d]*)')
    match = pattern.findall(tagname)
    fixed = ""
    if len(match) > 0:
        match = pattern.findall(tagname)[0] + "]"
        fixed = tagname.replace(match, "")
    else: 
        fixed = tagname
    return fixed 

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

#########################################################################
###                        AUXILIARY FUNCTIONS                        ###
###                                                                   ###
#########################################################################

# return the depth of the element 
def N(xp): 
    return len(xp.split("/")) - 2

# return the height of the whole path 
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
# Query the document using the xpath passed in
# if the result is similar to elems, then return True,
# else return False 
# TESTING REQUIRED, BUT BEING 1 or 2 off is our current design choice 
# IF IT HAS NO ATTRIBUTES TO WORK WITH, IT IS TOO GENERAL FOR US 
# print("IS %s LOCATABLE IN THE DOM?" % (xpath))
# TODO: Fix documentation
def generalLocates(xpath, document, elem):
    if "[" not in xpath: 
        return False
    else:
        elems = eval(xpath, document)
        elems = [html.tostring(elem).decode('utf-8') for elem in elems]
        return elem in elems

# Parse tagname and remove positions first 
# TODO: Add documentation
def getAttributes(elem, tagname):
    fixed = transfRemovePosition(tagname)
    soup = BeautifulSoup(elem, 'lxml')
    tag = soup.find(fixed)
    if tag == None:
        return [] 
    else:
        return tag.attrs

# TODO: Add documentation
def buildXPath(xpath_list):
    string = "//"
    for elem in xpath_list:
        string += elem + "/"
    return string[:-1]

# TODO: Add documentation and threading functionality
@timeout(TIMEOUT)
def RobulaPlus(xpath, elems, pathL, doc): 
    xpath_list = []
    reverseL = pathL[::-1]
    for elem in elems:
        stringified = html.tostring(elem).decode('utf-8')
        XList = ["//*"]
        while True:
            xp = XList.pop(0) # pop front of list
            temp = []
            currN = pathL[N(xp) - 1]
            new_elems = eval(buildXPath(reverseL[:-(N(xp) - 1)]), doc)
            new_elem = ""
            if len(new_elems) >= 1:    
                new_elem = html.tostring(new_elems[0]).decode('utf-8')
            xp1 = transfConvertStar(xp, currN)
            temp.append(xp1)
            xp2 = transfAddAttribute(xp1, getAttributes(new_elem, currN), currN)

            if len(xp2) >= 1:
                for x in xp2: 
                    temp.append(x)
                    temp.append(transfAddLevel(x, N(x), len(pathL)))
            else:             
                temp.append(transfAddLevel(xp1,N(xp1), len(pathL)))

            for i, item in enumerate(temp): 
                temp[i] = transfRemovePosition(item)
            # print(temp)
            for t in temp[::-1]: 
                if generalLocates(t, doc, stringified):
                    xpath_list.append(t)
                    if len(xpath_list) == TARGET: 
                        return xpath_list
                else: 
                    XList.append(t)

# Argument parsing function, returns the arguments passed in 
# TODO: Add boolean flag to just return the highest scoring xpath and its html 
def Parse():
    parser = argparse.ArgumentParser(description='First attempt to auto-generate unique descriptive xpaths')

    parser.add_argument('-u', dest="url", help="Specify a url to capture valid xpaths")
    parser.add_argument('-x', dest="xpath", help="Specify an xpath, if quotes (\"\") are included, please backslash escape them")
    parser.add_argument('-t', dest="text", help="Specify text to generate the absolute xpaths for you, instead of providing an xpath")
    parser.add_argument('-o', dest="output", help="Specify an output file to capture filtered xpaths. Defaults to logs/filtered/test.txt", default="logs/filtered/test.txt")
    parser.add_argument('-o2', dest="html_output", help="Specify an output file to capture scraped html with the first xpath returned")
    args = parser.parse_args()
    if not ((args.url and args.xpath) or (args.url and args.text)):
        print("Please use url and xpath flag, or url and text flags")
        exit()
    else:
        return args

# TODO: Clean up main 
def main(): 
    args = Parse()
    url = args.url
    xpath = ""
    print("Working url: %s" % (url))
    args_flag = ""
    if args.xpath:
        print("Working xpath: %s" % (xpath))
        xpath = args.xpath
        args_flag = "XPATH"
    else: 
        print("Working text xpath: %s" % ('//*[contains(text(),' + '"' + args.text + '")]'))
        xpath = args.text
        args_flag = "TEXT"
    opts = Options()
    opts.headless = True
    driver = webdriver.Firefox(options=opts)
    driver.get(url)
    page = driver.execute_script("return document.body.innerHTML").encode('utf-8')
    driver.close()
    driver.quit()
    document = html.fromstring(page)
    filtered = []
    if args_flag == "XPATH":
        elems = eval(xpath, document)
        pathL = L(xpath)
        print(pathL)
        new_xpaths = RobulaPlus(xpath, elems, pathL[::-1], document)
        # filter out all xpaths with star as final check 
        for xp in new_xpaths: 
            if not xp.startswith("//*"): 
                filtered.append(xp)
        print("OVERALL XPATHS FOUND: ", new_xpaths)
        print("FILTERED XPATHS FOUND: ", filtered)
    else:  
        xpaths = getAbsXpaths(document, xpath)
        print(xpaths)
        for i,xp in enumerate(xpaths):
            elems = eval(xp, document)
            pathL = L(xp)
            print("Iteration %d" % (i))
            new_xpaths = []
            try: 
                new_xpaths = RobulaPlus(xpath, elems, pathL[::-1], document)
            except TimeoutError:
                continue
            if new_xpaths is not None:
                for xp2 in new_xpaths: 
                    if not xp2.startswith("//*"): 
                        filtered.append(xp2) 
            print("FILTERED XPATHS FOUND: ", filtered)

    final_list = [] 
    for item in filtered: 
        if item not in final_list: 
            final_list.append(item)
    
    if len(final_list) == 0:
        print("Robula could not find any xpaths in time. Try again...")
        exit(1)

    with open(args.output, "w") as f: 
        for line in final_list:
            f.write(line + "\n")
        
    if args.html_output:
        lens = []
        for i,item in enumerate(final_list): 
            xpath = item
            elems = eval(xpath, document)
            elems = [html.tostring(elem).decode('utf-8') for elem in elems]
            lens.append(len(elems))
            with open(args.html_output, "a") as f:
                f.write("Score: %d\n" % (len(elems)))
                for elem in elems: 
                    f.write(elem + "\n")
                f.write("\n")
        best_index = lens.index(max(lens))
        print("Best XPATH found is: %s" % (final_list[best_index]))

    else: 
        xpath = filtered[0]
        elems = eval(xpath, document)
        elems = [html.tostring(elem).decode('utf-8') for elem in elems]
        with open(args.html_output, "w") as f:
            for elem in elems: 
                print(elem)
    # exit(1) # So Firefox Headless can close 

if __name__ == '__main__':
    main()
