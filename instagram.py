import urllib2
import time
import json
startTime = int(time.time())
polling_interval = 10
running = True
photosDict = {}
instagram_tag = "#danandjas"

def poll_instagram(): #program does nothing as written
    response = urllib2.urlopen("https://api.instagram.com/v1/tags/danandjas/media/recent?access_token=11420543.761e276.3ce68c22f21746acbbf9a4a886c43097").read()
    json_data = json.loads(response)
    for post in json_data['data']:
        for comment in post["comments"]["data"]:
            if instagram_tag in comment["text"]:
                if int(comment["created_time"]) > startTime:
                    if post["id"] not in photosDict:
                        photosDict[post["id"]] = post["images"]["standard_resolution"]["url"]

while running:
    start= time.clock()
    poll_instagram()
    print photosDict;
    work_duration = time.clock() - start
    time.sleep( polling_interval - work_duration )
