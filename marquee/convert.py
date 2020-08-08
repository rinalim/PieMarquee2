import sys, os
from subprocess import *

def run_cmd(cmd):
# runs whatever in the cmd variable
    p = Popen(cmd, shell=True, stdout=PIPE)
    output = p.communicate()[0]
    return output
  
source_path = sys.argv[1]
dest_path = sys.argv[2]
resize = sys.argv[3]

if source_path.endswith("/") == False:
    source_path = source_path+"/"
if dest_path.endswith("/") == False:
    dest_path = dest_path+"/"

if os.path.isdir(source_path) == False:
    print "source path is not valid"
else:
    if os.path.isdir(os.getcwd()+"/"+dest_path) == False:
        os.mkdir(os.getcwd()+"/"+dest_path)
    file_list = os.listdir(source_path)
    file_list.sort()
    for f in file_list:
        if ".png" in f:
            run_cmd('convert "' + source_path + f + '" -background black -alpha remove -resize ' + resize + ' "./' + dest_path + f + '"')
            print 'convert "' + source_path + f + '" -background black -alpha remove -resize ' + resize + ' "./' + dest_path + f + '"'
        elif ".jpg" in f:
            run_cmd('convert "' + source_path + f + '" -resize ' + resize + ' "./' + dest_path + f.replace("jpg","png") + '"')
            print 'convert "' + source_path + f + '" -resize ' + resize + ' "./' + dest_path + f.replace("jpg","png") + '"'
        