from run_robula import RunRobula
from test_robula_json import robula_output
from random import sample
from pathlib import Path
from selenium_interface import * 
from urllib.parse import urlparse
from time import sleep 

def fromJsonToRobula(robula_output, TARGET, TIMEOUT, blacklist=['href', 'id', 'role', 'type', 'script'], driver=None, log_dir=""): 
    for item in robula_output: 
        url = item["url"]
        print("Current URL:  %s" % (url))
        url_temp = urlparse(url)
        url_temp = url_temp.netloc.replace("www.", "")
        log_name = url_temp.split(".")[0]
        titles = item["title"]
        descs = item["desc"]
        dates = item["dates"]

        # current algo --> pick 3 random titles, pick both descriptions, pick 3 random dates
        # Time flat 8 runs of robula. Estimate before testing: 8-10min <-- SLOW 
        # Actual performance time after  1  run: 3:22.52 
        # NY performance: 3:43:31 
        try: 
            titles = sample(titles, 3)
        except ValueError: 
            titles = sample(titles, len(titles))
        try: 
            dates = sample(dates, 3)
        except ValueError:
            dates = sample(dates, len(dates))

        base_dir = log_dir + "/" + log_name + "/" 
        Path(base_dir).mkdir(parents=True, exist_ok=True)
        page = driver.get_script(url)
        for i, title in enumerate(titles): 
            title_name = "title" + str(i)
            print("Using title:  %s" % (title))
            RunRobula(url, title, base_dir + title_name , base_dir + "xpath" + title_name, TARGET=TARGET, blacklist_tags=blacklist, TIMEOUT=TIMEOUT, page=page)

        for i, date in enumerate(dates): 
            date_name = "date" + str(i)
            print("Using date:  %s" % (date))
            RunRobula(url, date, base_dir + date_name , base_dir + "xpath" + date_name, TARGET=TARGET, blacklist_tags=blacklist, TIMEOUT=TIMEOUT, page=page)
        
        for i, desc in enumerate(descs): 
            desc_name = "desc" + str(i)
            print("Using description:  %s" % (desc[:30]))
            RunRobula(url, desc[:30], base_dir + desc_name , base_dir + "xpath" + desc_name, TARGET=TARGET, blacklist_tags=blacklist, TIMEOUT=TIMEOUT, page=page)

        print()
        sleep(1)


driver = FireDriver(None)
fromJsonToRobula(robula_output, 4, 10, driver=driver, log_dir="logs")
driver.kill()