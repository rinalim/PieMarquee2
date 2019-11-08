sudo cp ./libraspidmx.so.1 /usr/lib
sudo cp ./pngview /usr/bin
sudo chmod 755 /usr/bin/pngview

sudo apt-get install imagemagick -y

rm -rf /opt/retropie/configs/all/PieMarquee/
mkdir /opt/retropie/configs/all/PieMarquee/
cp -f -r ./PieMarquee /opt/retropie/configs/all/

sudo sed -i '/PieMarquee.py/d' /opt/retropie/configs/all/autostart.sh
sudo sed -i '1i\\/usr/bin/python /opt/retropie/configs/all/PieMarquee/PieMarquee.py &' /opt/retropie/configs/all/autostart.sh

echo
echo "Setup Completed. Reboot after 3 Seconds."
sleep 3
reboot
