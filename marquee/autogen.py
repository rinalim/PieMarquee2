import sys, os
from subprocess import *

def run_cmd(cmd):
# runs whatever in the cmd variable
    p = Popen(cmd, shell=True, stdout=PIPE)
    output = p.communicate()[0]
    return output
  
input_dir = sys.argv[1].split("/")[0]
input_file = sys.argv[1].split("/")[1]
source_path = "/home/pi/RetroPie/roms/"+input_dir+"/marquee/"
snapshot_parh = "/home/pi/RetroPie/roms/"+input_dir+"/snap/"
dest_path = input_dir+"/"
resize = sys.argv[2]
resize_method = sys.argv[3]
bg_color = sys.argv[4]
bg_trans = str(100-int(sys.argv[5])*100)
marquee_size = sys.argv[6]

run_cmd("convert -size " + resize + " xc:" + bg_color + 
    " -matte -channel A +level 0," + bg_trans + "% +channel ./bg.png")

if os.path.isdir(source_path) == False:
    print "source path is not valid: " + source_path
else:
    if os.path.isdir(os.getcwd()+"/"+dest_path) == False:
        os.mkdir(os.getcwd()+"/"+dest_path)
    if input_file == "*":
        file_list = os.listdir(source_path)
    else:
        file_list = [source_path+"/"+input_file]
    for f in file_list:
        if ".png" in f:
            run_cmd('convert "' + snapshot_parh + f + '" -resize ' + resize + ' "\! bg.png -composite' + dest_path + f + '"')
            run_cmd('convert "' + source_path + f + '" -resize ' + resize + ' logo.png')
            run_cmd('convert logo.png -background black -shadow 80x3+5+5 logo.png -composite shadow.png')
            run_cmd('composite -gravity center shadow.png "' + dest_path + f + ' " "' + dest_path + f + '"')
            print 'Generate "' + dest_path + f + '"'
        elif ".jpg" in f:
            run_cmd('convert "' + source_path + f + '" -resize ' + resize + ' "./' + dest_path + f.replace("jpg","png") + '"')
            print 'Generate "' + dest_path + f + '"'
'''
convert kof97-snap.png -resize 1280x400\! bg.png -composite kof97.png
convert kof97-snap.png -resize 1280x400^ bg.png -composite kof97.png
convert kof97-logo.png -resize 1280x400 -resize 80% logo.png 
convert logo.png -background black -shadow 80x3+5+5 logo.png -composite shadow.png
composite -gravity center shadow.png kof97.png kof97.png 
'''
