#!/usr/bin/python

import os
from subprocess import *
from time import *
import xml.etree.ElementTree as ET

INTRO = "/opt/retropie/configs/all/PieMarquee2/intro.mp4"
VIEWER = "omxiv /tmp/marquee.txt -f -d 4 -t 5 -T blend --duration 1000 > omxiv.log &"

def run_cmd(cmd):
# runs whatever in the cmd variable
    p = Popen(cmd, shell=True, stdout=PIPE)
    output = p.communicate()[0]
    return output

def kill_proc(name):
    ps_grep = run_cmd("ps -aux | grep " + name + "| grep -v 'grep'")
    if len(ps_grep) > 1: 
        os.system("killall " + name)
        
def is_running(pname):
    ps_grep = run_cmd("ps -ef | grep " + pname + " | grep -v grep")
    if len(ps_grep) > 1:
        return True
    else:
        return False

def get_publisher(romname):
    filename = romname+".zip"
    publisher = ""
    for item in root:
        if filename in item.findtext('path'):
            publisher = item.findtext('publisher')
            break
    words = publisher.split()
    return words[0].lower()
    
if os.path.isfile(INTRO) == True:
    run_cmd("omxplayer --display 4 " + INTRO)

doc = ET.parse("/opt/retropie/configs/all/PieMarquee2/gamelist_short.xml")
root = doc.getroot()

os.system("echo '/home/pi/PieMarquee2/marquee/maintitle.png' > /tmp/marquee.txt")
os.system(VIEWER)
    
cur_imgname = ""
change_count = 0
while True:
    sleep_interval = 1
    ingame = ""
    romname = ""
    sysname = ""
    pubpath = ""
    instpath = ""
    ps_grep = run_cmd("ps -aux | grep emulators | grep -v 'grep'")
    if len(ps_grep) > 1:
        ingame="*"
        words = ps_grep.split()
        if 'advmame' in ps_grep:
            sysname = "mame-advmame"
            romname = words[-1]
        else:
            for i in words:
                if 'roms' in i:
                    path = i
                    sysname = path.replace('"','').split("/")[-2]
                    romname = path.replace('"','').split("/")[-1].split(".")[0]
                    break

    elif os.path.isfile("/tmp/PieMarquee.log") == True:
        f = open('/tmp/PieMarquee.log', 'r')
        line = f.readline()
        f.close()
        words = line.split()
        if len(words) == 2: # In the gamelist: Game /home/pi/.../*.zip
            sysname = words[1].replace('"','').split("/")[-2]
            romname = words[1].replace('"','').split("/")[-1].split(".")[0]
            sleep_interval = 0.1 # for quick view
        elif len(words) == 1:
            if words[0] == "SystemView":
                romname = "maintitle"
            else:
                romname = words[0]

    else:
        romname = "maintitle"
   
    if os.path.isfile("/home/pi/PieMarquee2/marquee/" + romname + ".png") == True:
        imgname = romname
        if ingame == "*":
            publisher = get_publisher(romname)
            if os.path.isfile("/home/pi/PieMarquee2/marquee/publisher/" + publisher + ".png") == True:
                pubpath = "/home/pi/PieMarquee2/marquee/publisher/" + publisher + ".png"
            if os.path.isfile("/home/pi/PieMarquee2/marquee/instruction/" + romname + ".png") == True:
                instpath = "/home/pi/PieMarquee2/marquee/instruction/" + romname + ".png"
    elif os.path.isfile("/home/pi/PieMarquee2/marquee/" + sysname + ".png") == True:
        imgname = sysname
    else:
        imgname = "maintitle"
        
    if imgname+ingame != cur_imgname: # change marquee images
        kill_proc("omxplayer.bin")
        if imgname == "maintitle" and os.path.isfile("/home/pi/PieMarquee2/marquee/maintitle.mp4") == True:
            os.system("omxplayer --loop --no-osd --display 4 /home/pi/PieMarquee2/marquee/maintitle.mp4 &")
        else:
            '''
            f = open("/tmp/marquee.txt", "w")
            if pubpath != "":
                f.write(pubpath+"\n")
            f.write("/home/pi/PieMarquee2/marquee/" + imgname + ".png")
            if instpath != "":
                f.write("\n"+instpath)
            f.close()
            '''
            imgpath = "/home/pi/PieMarquee2/marquee/" + imgname + ".png"
            if ingame == "*":
                if pubpath != "":
                    imgpath = pubpath+"\n"+imgpath
                if instpath != "":
                    imgpath = imgpath+"\n"+instpath
            os.system("echo '" + imgpath + "' > /tmp/marquee.txt")
            if is_running("omxiv") == False:
                os.system("clear > /dev/tty1")
                os.system(VIEWER)
        cur_imgname = imgname+ingame

    sleep(sleep_interval)
