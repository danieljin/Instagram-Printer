import urllib2
import time
import json
import subprocess
startTime = int(time.time())
polling_interval = 10
running = True
photosDict = {}
printedIds = []
instagram_tag = "#danandjas"
bluetooth_address = "08:EF:3B:41:D4:B6"
print startTime
def poll_instagram(): #program does nothing as written
    response = urllib2.urlopen("https://api.instagram.com/v1/tags/danandjas/media/recent?access_token=11420543.761e276.3ce68c22f21746acbbf9a4a886c43097").read()
    json_data = json.loads(response)
    for post in json_data['data']:
        if instagram_tag in post["caption"]["text"]:
            # if int(post["caption"]["created_time"]) > startTime:
            if post["id"] not in photosDict:
                photosDict[post["id"]] = post["images"]["standard_resolution"]["url"]
        for comment in post["comments"]["data"]:
            if instagram_tag in comment["text"]:
                # if int(comment["created_time"]) > startTime:
                if post["id"] not in photosDict:
                    photosDict[post["id"]] = post["images"]["standard_resolution"]["url"]
def print_photos():
    for id, url in photosDict.iteritems():
        if id not in printedIds:
            printedIds.append(id)
            tempfile = urllib2.urlopen(url)
            filename = id+'.jpg'
            output = open(filename,'wb')
            output.write(tempfile.read())
            output.close()
            print filename+" has been saved."
            subprocess.call(["obexftp", "--nopath", "--noconn", "--uuid", "none", "--bluetooth", bluetooth_address, "--channel", "4", "-p", filename],shell=True)
            os.remove(filename)
            print filenam+" has been printed."


while running:
    start= time.clock()
    poll_instagram()
    print_photos()
    print "tick"
    work_duration = time.clock() - start
    time.sleep( polling_interval - work_duration )
