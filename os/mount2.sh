#!/bin/bash

image=$1

if [[ -n "$image" ]]; then
    
    if [ -d "./livecdtmp" ]; then

		sudo rm -r ./livecdtmp

	fi

	if [ -d "./lc_os_custom_ubuntu_1604.iso" ]; then

		sudo rm -r ./lc_os_custom_ubuntu_1604.iso

	fi

	mkdir ./livecdtmp
    cp "$image" ./livecdtmp
    cd ./livecdtmp

    mkdir mnt
    mount -o loop "$image" mnt

    mkdir extract-cd
    rsync --exclude=/casper/filesystem.squashfs -a mnt/ extract-cd

    unsquashfs mnt/casper/filesystem.squashfs
    mv squashfs-root edit

#	mount --bind /dev/ edit/dev
    
    # command line argument to specify directory holding all files to be copied
    # command line argument to specify ...
    cp /etc/resolv.conf /etc/hosts ../livecdtmp/edit/etc/
	cp -r ../soft ../livecdtmp/edit/home/
	cp ../sources.list ../livecdtmp/edit/etc/apt/

    # mount --bind /dev/ ../livecdtmp/edit/dev

    # chroot edit ./home/soft/install.sh
    chroot edit /bin/bash -l
else
    echo "Starting Image Argument Missing"
    exit 1
fi
