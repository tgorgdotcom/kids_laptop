#!/bin/bash

sudo rpm-ostree install malcontent malcontent-tools malcontent-control

# remove firefox icon
sudo mkdir -p /usr/local/share/applications && \
sudo cp /usr/share/applications/org.mozilla.firefox.desktop /usr/local/share/applications/ && \
sudo sed -i "2a\\NoDisplay=true" /usr/local/share/applications/org.mozilla.firefox.desktop && \
sudo update-desktop-database /usr/local/share/applications/

# install google chrome
flatpak install com.google.Chrome

# set up chrome policy to use welcome webpage as new tab page
sudo mkdir -p /etc/opt/chrome/policies/managed
sudo cp ntp_policy.json /etc/opt/chrome/policies/managed

# install pihole container
sudo cp pihole.container /etc/containers/systemd
sudo mkdir /etc/pihole

# setup pihole
read -rps "Enter a password to login to pihole: " pihole_pass
echo -n "$pihole_pass" | sudo podman secret create pihole_password -

sudo systemctl daemon-reload

# wait until pihole is up
sudo podman wait --condition=healthy systemd-pihole

# get pihole ip
pihole_dns=$(sudo podman container inspect systemd-pihole | jq -r '.[0].NetworkSettings.IPAddress') 
nmcli -g name,type connection show --active | awk -F: '/ethernet|wireless/ { print $1 }' | while read connection
do
  sudo nmcli con mod "$connection" ipv6.ignore-auto-dns yes
  sudo nmcli con mod "$connection" ipv4.ignore-auto-dns yes
  sudo nmcli con mod "$connection" ipv4.dns "$pihole_dns"
  sudo nmcli con down "$connection" && nmcli con up "$connection"
done

reboot