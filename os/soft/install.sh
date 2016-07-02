#!/bin/bash

mount -t proc none /proc
mount -t sysfs none /sys
mount -t devpts /dev/pts

export HOME=/root
export LC_ALL=C

cd /home/soft

# apt-mark hold linux-headers-generic linux-image-generic
# aptitude hold linux-headers-generic linux-image-generic

add-apt-repository ppa:nilarimogard/webupd8
add-apt-repository ppa:ubuntu-wine/ppa
add-apt-repository ppa:webupd8team/sublime-text-3
add-apt-repository ppa:mystic-mirage/pycharm
add-apt-repository ppa:paolorotolo/android-studio
wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - 
sh -c 'echo "deb http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list'

dpkg --add-architecture i386

apt-get update
apt-get upgrade
# apt-get dist-upgrade

# prior to installing new software verify that apt-get download was once successful. In case it wasn't successful/didn't run before, apt-get download whould finish first in order to optimize performance and network load in further attempts to produce the image. In case it did run the dpkg -i should first instsall all the available debs and then apt-get install -f should complete all the dependencies, and
# then the apt-get isntall against software.txt (containing all the same software as used in softwareDEBS.txt for apt-get download) in order to ensure proper installation of all the required packages.

# Include verifications for each step of the execution of the script. Link the mount, install and build scripts into a single execution

apt-get build-dep python-matplotlib

apt-get install $(grep -vE "^\s*#" software.txt  | tr "\n" " ")

# apt-get remove --purge gnome-mines gnome-sudoku gnome-system-tools gnome-themes-standard gnome-themes-standard-data mousepad mugshot pidgin pidgin-data pidgin-libnotify pidgin-otr ristretto thunderbird xfburn xfce4-cpugraph-plugin xfce4-dict xfce4-mailwatch-plugin xfce4-netload-plugin xfce4-notes xfce4-notes-plugin xfce4-places-plugin xfce4-weather-plugin xfce4-xkb-plugin gnomine unity-webapps-common thunderbird shotwell rhythmbox brasero abiword abiword-common abiword-plugin-grammar gimp-data gmusicbrowser gimp xchat gnumeric gnumeric-common gnumeric-doc

python net.py

bash -x netbeans-8.1-linux.sh --silent
bash -x Anaconda3-2.4.1-Linux-x86_64.sh
bash -x Anaconda2-2.4.1-Linux-x86_64.sh

dpkg -i wingide-101-5_5.1.11-1_amd64.deb

pip3 install -r requirements.txt

pip3 install -U tornado

apt-get install -f
# apt-mark unhold linux-headers-generic linux-image-generic
# aptitude unhold linux-headers-generic linux-image-generic
apt-get autoremove
apt-get clean
apt-get autoclean
# comment out the "start on" line in /etc/init/mysql.conf
rm -rf /tmp/* ~/.bash_history
rm /etc/hosts /etc/resolv.conf

umount /proc || umount -lf /proc
umount /sys
umount /dev/pts

rm /etc/apt/sources.list.d/google.list 

rm -r *
#exit
