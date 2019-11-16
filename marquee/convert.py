import sys, os
from subprocess import *

def run_cmd(cmd):
# runs whatever in the cmd variable
    p = Popen(cmd, shell=True, stdout=PIPE)
    output = p.communicate()[0]
    return output
  
source_path = sys.argv[1]

if os.path.isdir(source_path) == True:
    file_list = os.listdir(source_path)
    file_list.sort()
    for f in file_list:
        if ".png" in f:
            run_cmd("convert " + source_path + f + " -resize 800x480 ./" + f)
            print "convert " + source_path + f + " -resize 800x480 ./" + f

