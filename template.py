import urllib2
import time
import json
import subprocess
import shutil
import os, errno
def apply_template(username, caption):
    mkdir_p("tmp")
    subprocess.Popen(["convert", "IMG_0195.JPG", "-resize", "1000x1000", "-gravity", "center", "-extent", "1000x1000", "resize.JPG"]).communicate()
    subprocess.Popen(["convert", "template.JPG", "resize.JPG", "-geometry", "+0+145", "-composite", "combined.JPG"]).communicate()
    subprocess.Popen(["convert", "combined.jpg", "-pointsize", "45", "-fill", "rgb(18,86,136)", "-font", "HelveticaLTStd-Bold", "-annotate", "+134+58", username, "text1.JPG"]).communicate()
    subprocess.Popen(["convert", "text1.jpg", "-pointsize", "45", "-fill", "rgb(18,86,136)", "-font", "HelveticaLTStd-Bold", "-annotate", "+34+1260", username, "text2.JPG"]).communicate()
    caption = insert_new_lines(caption, 40, 0)
    subprocess.Popen(["convert", "text2.jpg", "-pointsize", "45", "-fill", "black", "-font", "HelveticaLTStd-Light.otf", "-annotate", "+34+1315", caption, "final.JPG"]).communicate()
    print "fuck."
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

apply_template("dankjin","Hi baby I love you so much and I want to be with you forever and ever! You feel me? #danandjas")