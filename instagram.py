import urllib2
import time
import json
import subprocess
import os, shutil, errno
startTime = int(time.time())
polling_interval = 10
running = True
photosDict = {}
printQueue = []
instagram_tag = "#danandjas"
bluetooth_address = "08:EF:3B:41:D4:B6"
def poll_instagram():
    print startTime
    response = urllib2.urlopen("https://api.instagram.com/v1/tags/danandjas/media/recent?access_token=11420543.761e276.3ce68c22f21746acbbf9a4a886c43097").read()
    json_data = json.loads(response)
    for post in json_data['data']:
        if post["id"] not in printQueue:
            if instagram_tag in post["caption"]["text"]:
                if int(post["caption"]["created_time"]) > startTime:
                    photosDict[post["id"]] = {'url': post["images"]["standard_resolution"]["url"], 'username': post["user"]["username"], 'comment': post["caption"]["text"]}
                    printQueue.append(post["id"])
            for comment in post["comments"]["data"]:
                if instagram_tag in comment["text"]:
                    if int(comment["created_time"]) > startTime:
                        photosDict[post["id"]] = {'url': post["images"]["standard_resolution"]["url"], 'username': post["user"]["username"], 'comment': post["caption"]["text"]}
                        printQueue.append(post["id"])

def print_photos():
    if printQueue:
        global startTime
        startTime = int(time.time())
        for id in printQueue:
            running = False
            entity = photosDict.get(id)
	    tempfile = urllib2.urlopen(entity.get('url'))
	    filename = id+'.jpg'
	    filename2 = id+'_template.jpg'
	    filename3 = id+".jpeg"
	    output = open(filename,'wb')
	    output.write(tempfile.read())
	    output.close()
	    print filename+" has been saved."
            apply_template(filename, filename2, entity.get('username'), entity.get('comment'))
	    with open(filename3, "w") as outputfile:
	        subprocess.Popen(["jpegtran", filename2],stdout=outputfile).communicate()
    	    print filename+" has been converted"
            printed = False
	    print "attempting to print"
            count = 0
            while not printed:
                try:
                    count += 1;
	            child = subprocess.Popen(["obexftp", "--nopath", "--noconn", "--uuid", "none", "--bluetooth", bluetooth_address, "--channel", "4", "-p", filename2], stdout=subprocess.PIPE,stderr=subprocess.PIPE)
	            child.communicate()
                    if (child.returncode == 255):
                        printed = True
                    else:
                        if count <= 1:
                            if (child.returncode == 69):
                                print "make sure printer has paper"
                            else:
                                print "make sure printer is on."
	        except:
                    pass
	    os.remove(filename)
	    os.remove(filename2)
	    os.remove(filename3)
	    print filename+" has been printed."
            printQueue.remove(id)
            print "waiting 60 seconds for print to finish"
            time.sleep(6)
            running = True

def apply_template(input_filename, output_filename, username, caption):
    mkdir_p("tmp")
    subprocess.Popen(["convert", input_filename, "-resize", "1000x1000", "-gravity", "center", "-extent", "1000x1000", "tmp/resize.JPG"]).communicate()
    subprocess.Popen(["convert", "template.JPG", "tmp/resize.JPG", "-geometry", "+0+150", "-composite", "tmp/combined.JPG"]).communicate()
    subprocess.Popen(["convert", "tmp/combined.JPG", "-pointsize", "45", "-fill", "rgb(18,86,136)", "-font", "Helvetica-Bold", "-annotate", "+134+78", username, "tmp/text1.JPG"]).communicate()
    subprocess.Popen(["convert", "tmp/text1.JPG", "-pointsize", "45", "-fill", "rgb(18,86,136)", "-font", "Helvetica-Bold", "-annotate", "+34+1267", username, "tmp/text2.JPG"]).communicate()
    caption = insert_new_lines(caption, 45, 0)
    subprocess.Popen(["convert", "tmp/text2.JPG", "-pointsize", "45", "-fill", "black", "-font", "Helvetica", "-weight", "200", "-annotate", "+34+1322", caption, output_filename]).communicate()
    print "Image has been converted."
    shutil.rmtree("tmp")

def insert_new_lines(text, line_length, count):
    if len(text) <= line_length :
        return text
    else :
        k = text[:line_length].rfind(" ")

        if k < 0 :
            return text[:line_length] + "\n" + insert_new_lines(text[line_length:], line_length, count + 1)
        elif count > 2 :
            return text[:k] + ' ...'
        else :
            return text[:k] + "\n" + insert_new_lines(text[k+1:], line_length, count + 1)

def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc: # Python >2.5
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else: raise

while running:
    start= time.clock()
    poll_instagram()
    print_photos()
    print "tick"
    work_duration = time.clock() - start
    time.sleep( polling_interval - work_duration )
