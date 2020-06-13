# A Modified Python Implementation of Robula+ 

Our version takes in an absolute xpath and a url, and outputs a generic xpath that can identify all elements above the element caught by the initial xpath passed in. (TOO WORDY)

# How to Run: 
`python3 boilerplate.py -u https://a-url-that-you-like.com -x //a/valid/xpath/here`

# Data log 

## June 6th 2020 
We were able to begin implementing a first draft today, with some small bugs at the end of the session.
Next steps: begin unit testing, fix transfAddlevel, implement removeposition. 

## June 13th 2020
Able to get a general xpath for all urls, descriptions, and dates for newartcenter. 
We found 65 events within newartcenter/classes, their dates, instructors, and descriptions. 
Next steps include starting with an absolute xpath and working up the tree to remove 
text overhead found within example log txt files like mfa-title.txt
