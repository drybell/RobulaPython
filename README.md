# A Modified Python Implementation of Robula+ 

Our version takes in an absolute xpath and a url, and outputs a generic xpath that can identify all elements above the element caught by the initial xpath passed in. (TOO WORDY)

# How to Run: 
`python3 boilerplate.py -u https://a-url-that-you-like.com -x "//a/valid/xpath/here"`

# Data log 

## June 6th 2020 
We were able to begin implementing a first draft today, with some small bugs at the end of the session.
Next steps: begin unit testing, fix transfAddlevel, implement removeposition. 

## June 13th 2020
Able to get a general xpath for all urls, descriptions, and dates for newartcenter. 
We found 65 events within newartcenter/classes, their dates, instructors, and descriptions. 
Next steps include starting with an absolute xpath and working up the tree to remove 
text overhead found within example log txt files like mfa-title.txt

## June 20th 2020 
Able to strip all unnecessary html from output logs using simple regex. A little issue with handling UTF-8 encodings of right double quotes, currently ignoring any errors (\x9d is the weirdest encoding we've gotten). We tested on the current log data and outputted "fixed" versions of the logs. Still working on generating absolute xpaths to feed Robula. 

## June 21 2020 
We added absolute_xpath.py to generate absolute xpaths given a piece of text and a url. Further functionality could include testing with id, class, tag_name, and links as well. We integrated absolute_xpath.py to boilerplate (the -t flag) for using this new tool alongside our Robula implementation. We have done some minor unit tests, and found some decent results when testing with text that exists within the page. A fatal error occured at the end of our session, which we believe could have something to do with the timeout library. Restructuring our timing system with Robula and the text flag will ensue. Also added output flags to generate log files (xpaths and scraped html)
