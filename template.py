import urllib2
import time
import json
import subprocess
import shutil
import os, errno
def apply_template(input_filename, output_filename, username, caption):
    mkdir_p("tmp")
    subprocess.Popen(["convert", input_filename, "-resize", "1000x1000", "-gravity", "center", "-extent", "1000x1000", "tmp/resize.JPG"]).communicate()
    subprocess.Popen(["convert", "template.JPG", "tmp/resize.JPG", "-geometry", "+0+150", "-composite", "tmp/combined.JPG"]).communicate()
    subprocess.Popen(["convert", "tmp/combined.jpg", "-pointsize", "45", "-fill", "rgb(18,86,136)", "-font", "HelveticaLTStd-Bold", "-annotate", "+134+63", username, "tmp/text1.JPG"]).communicate()
    subprocess.Popen(["convert", "tmp/text1.jpg", "-pointsize", "45", "-fill", "rgb(18,86,136)", "-font", "HelveticaLTStd-Bold", "-annotate", "+34+1267", username, "tmp/text2.JPG"]).communicate()
    caption = insert_new_lines(caption, 40, 0)
    subprocess.Popen(["convert", "tmp/text2.jpg", "-pointsize", "45", "-fill", "black", "-font", "HelveticaLTStd-Light.otf", "-annotate", "+34+1322", caption, output_filename]).communicate()
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

apply_template("IMG_0195.JPG", "final.JPG", "dankjin","Hi baby I love you so much and I want to be with you forever and ever! You feel me? #danandjas")