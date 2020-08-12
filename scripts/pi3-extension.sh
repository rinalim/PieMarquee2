sudo cp /opt/retropie/supplementary/emulationstation/emulationstation /opt/retropie/supplementary/emulationstation/emulationstation_org
sudo cp ./ES-pi3/emulationstation /opt/retropie/supplementary/emulationstation/emulationstation
sudo chmod 755 /opt/retropie/supplementary/emulationstation/emulationstation

echo
echo "Setup Completed. Reboot after 3 Seconds."
sleep 3
reboot
