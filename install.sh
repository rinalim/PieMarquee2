#!/bin/bash
#get script path
scriptfile=$(readlink -f $0)
installpath=`dirname $scriptfile`

#run as root user
if [ "$(whoami)" != "root" ]; then
	echo "Switching to root user..."
	sudo bash $scriptfile $*
	exit 1
fi
apt-get update
apt-get install omxplayer libjpeg8 imagemagick -y

rm -rf /opt/retropie/configs/all/PieMarquee2/
mkdir /opt/retropie/configs/all/PieMarquee2/
cp -f -r ./PieMarquee2 /opt/retropie/configs/all/

sudo chmod 755 /opt/retropie/configs/all/PieMarquee2/omxiv-marquee

sudo sed -i '/PieMarquee2.py/d' /opt/retropie/configs/all/autostart.sh
sudo sed -i '1i\\/usr/bin/python3 /opt/retropie/configs/all/PieMarquee2/PieMarquee2.py > /dev/null 2>&1 &' /opt/retropie/configs/all/autostart.sh

echo
echo "Setup Completed. Reboot after 3 Seconds."
sleep 3
reboot
