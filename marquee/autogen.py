import sys, os
from subprocess import *

def run_cmd(cmd):
# runs whatever in the cmd variable
    p = Popen(cmd, shell=True, stdout=PIPE)
    output = p.communicate()[0]
    return output
  
input_dir = sys.argv[1].split("/")[0]
source_path = "/home/pi/RetroPie/roms/"+input_dir+"/marquee/"
snapshot_path = "/home/pi/RetroPie/roms/"+input_dir+"/snap/"
dest_path = input_dir+"/"
resize = sys.argv[2]
resize_method = sys.argv[3]
logo_ratio = int(sys.argv[4])
bg_color = sys.argv[5]
bg_trans = str(int(100-int(sys.argv[6])))

logo_x = int(int(resize.split('x')[0])*logo_ratio/100)
logo_y = int(int(resize.split('x')[1])*logo_ratio/100)
logo_size = str(logo_x)+"x"+str(logo_y)

run_cmd("convert -size " + resize + " xc:" + bg_color + 
    " -matte -channel A +level 0," + bg_trans + "% +channel ./bg.png")

if os.path.isdir(source_path) == False:
    print "source path is not valid: " + source_path
else:
    if os.path.isdir(os.getcwd()+"/"+dest_path) == False:
        os.mkdir(os.getcwd()+"/"+dest_path)
    if dest_path == sys.argv[1]:
        file_list = os.listdir(source_path)
    else:
        file_list = [sys.argv[1].split("/")[1]]
    file_list.sort()
    for f in file_list:
        if ".png" in f:
            if os.path.isfile(snapshot_path+f) == True:
                if resize_method == "fill":
                    run_cmd('convert "' + snapshot_path + f + 
                            '" -trim -resize ' + resize + '\! bg.png -composite "' + dest_path + f + '"')
                elif resize_method == 'crop':
                    run_cmd('convert "' + snapshot_path + f + 
                            '" -trim -resize ' + resize + '^ -gravity center -extent ' + resize + 
                            ' bg.png -composite "' + dest_path + f + '"')
                else:
                    print 'Resize option error'
            else:
                run_cmd('cp bg.png ' + dest_path + f) 
            run_cmd('convert "' + source_path + f + '" -trim -resize ' + logo_size + ' logo.png')
            run_cmd('convert logo.png -background black -shadow 80x3+5+5 logo.png -composite shadow.png')
            run_cmd('composite -gravity center shadow.png "./' + dest_path + f + '" "./' + dest_path + f + '"')
            print 'Generate "' + dest_path + f + '"'
        elif ".jpg" in f:
            run_cmd('convert "' + source_path + f + '" -resize ' + 
                    resize + ' "./' + dest_path + f.replace("jpg","png") + '"')
            print 'Generate "' + dest_path + f + '"'
