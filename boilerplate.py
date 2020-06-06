# Daniel Ryaboshapka and Sam Chung 
# Robula+ Implementation in Python 3.7 
# 

### NAME DEFINITIONS 
#  xp = The XPATH expression to specialize --> //td 
#  N  = The length (in nodes/levels) of variable xp --> //td => N=1
#														//*//td => N=2
#  L  = The list of the ancestors of target elem e in the considered DOM,
#       starting and including e 
### 

# Precondition: Xpath xp starts with //* 
#       Action: replace initial * with tag name of the DOM elem L.get(N)
#      Example: INPUT:  xp = //*/td and L.get(2).getTagName() = tr  
#				OUTPUT: //tr//td
def transfConvertStar(xp, tagname):

# Precondition: the Nth level of xp does not already contain any kind of predicates
#       Action: Add the predicate basd on the id (if available) of the DOM element L.get(N)
#               to the higher level of xp 
#      Example: INPUT:  xp = //td and L.get(1).getID() = 'name'
#         		OUTPUT: //td[@id='name']
def transfAddID(xp, nth):

# Precondition: the Nth level of xp does not already contain any predicate on text
# 				or any predicate on position
#       Action: add a predicate on the text contained (if any) in the DOM element L.get(N)
#				to the higher level of xp 
#      Example: INPUT:  
#				OUTPUT: 
def transfAddText():

# Precondition:
#       Action:
#      Example: INPUT:  
#				OUTPUT: 
def transfAddAttribute():

# Precondition:
#       Action:
#      Example: INPUT:  
#				OUTPUT: 
def transfAddAttributeSet():

# Precondition:
#       Action:
#      Example: INPUT:  
#				OUTPUT: 
def transfAddPosition():

# Precondition:
#       Action:
#      Example: INPUT:  
#				OUTPUT: 
def transfAddLevel():
