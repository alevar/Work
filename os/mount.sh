#!/bin/bash

image=$1

if [[ -n "$image" ]]; then
    
    if [ -d "/tmp/livecd" ]; then

		sudo rm -r /tmp/livecd

	fi

	if [ -d "./livecd" ]; then

		sudo rm -r ./livecd

	fi

	if [ -d "./lc_os_custom_ubuntu_1604.iso" ]; then

		sudo rm -r ./lc_os_custom_ubuntu_1604.iso

	fi

	mkdir /tmp/livecd
	mount -o loop "$image" /tmp/livecd

	mkdir -p livecd/cd
	rsync --exclude=/casper/filesystem.squashfs -a /tmp/livecd/ livecd/cd
	mkdir livecd/squashfs  livecd/custom
	modprobe squashfs
	mount -t squashfs -o loop /tmp/livecd/casper/filesystem.squashfs livecd/squashfs/
	cp -a livecd/squashfs/* livecd/custom

	cp /etc/resolv.conf /etc/hosts livecd/custom/etc/
	cp -r ./soft livecd/custom/home/
	cp sources.list livecd/custom/etc/apt/

	chroot livecd/custom /bin/bash -l

else
    echo "Starting Image Argument Missing"
    exit 1
fi