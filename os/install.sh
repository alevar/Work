#!/bin/bash

mount -t proc none /proc
mount -t sysfs none /sys
mount -t devpts /dev/pts

export HOME=/root
export LC_ALL=C

cd /home/soft

# apt-mark hold linux-headers-generic linux-image-generic
# aptitude hold linux-headers-generic linux-image-generic

add-apt-repository ppa:nilarimogard/webupd8 -y
# add-apt-repository ppa:ubuntu-wine/ppa -y
add-apt-repository ppa:webupd8team/sublime-text-3 -y
add-apt-repository ppa:mystic-mirage/pycharm -y
add-apt-repository ppa:paolorotolo/android-studio -y
wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - 
sh -c 'echo "deb http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list'

dpkg --add-architecture i386

apt-get -qq update
apt-get -qq upgrade
# apt-get dist-upgrade

# prior to installing new software verify that apt-get download was once successful. In case it wasn't successful/didn't run before, apt-get download whould finish first in order to optimize performance and network load in further attempts to produce the image. In case it did run the dpkg -i should first instsall all the available debs and then apt-get install -f should complete all the dependencies, and
# then the apt-get isntall against software.txt (containing all the same software as used in softwareDEBS.txt for apt-get download) in order to ensure proper installation of all the required packages.

# Include verifications for each step of the execution of the script. Link the mount, install and build scripts into a single execution

apt-get build-dep python-matplotlib

# below line defines installation of all software components
# apt-get install $(grep -vE "^\s*#" software.txt  | tr "\n" " ")

# below command defines installation of the base functionality packages
apt-get -qq install $(grep -vE "^\s*#" softwareINSTALL.txt  | tr "\n" " ")

apt-get -qq remove --purge $(grep -vE "^\s*#" softwareREMOVE.txt  | tr "\n" " ")

# removes the unwanted clutter in the unity dash
gsettings set com.canonical.Unity.Dash scopes "['home.scope', 'applications.scope']"

python net.py

for dir in ~/Work/os2/soft/progs/*; do
    filename=$(basename "$dir")
    extension="${filename##*.}"
    if [ "$extension" == "sh" ]; then
        bash -x $dir --silent
    elif [ "$extension" == "deb" ]; then
        dpkg -i $dir
    elif [ "$extension" == "py" ]; then
        python3 $dir
    else
        echo "SORRY, NOT GOING TO HAPPEN WITH THIS FILETYPE" 
    fi
done

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
mv /etc/hosts.old /etc/hosts /etc/resolv.conf.old /etc/resolv.conf

umount /proc || umount -lf /proc
umount /sys
umount /dev/pts

rm /etc/apt/sources.list.d/google.list 

cd ..

rm -rf soft/
#exit
