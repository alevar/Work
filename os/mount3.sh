#!/bin/bash

image=$1

if [[ -n "$image" ]]; then
    
    if [ -d "./custom-img" ]; then
        echo "Removing previous builds - custom-img"
		sudo rm -r ./custom-img

	fi

    gsettings set org.gnome.desktop.media-handling autorun-never true

    mkdir ./custom-img
    cp "$image" ./custom-img
    cd ./custom-img
    mkdir mnt
    sudo mount -o loop "$image" mnt
    mkdir extract
    sudo rsync --exclude=/casper/filesystem.squashfs -a mnt extract
    sudo unsquashfs mnt/casper/filesystem.squashfs
    sudo mv squashfs-root edit
    
    mv edit/etc/hosts edit/etc/hosts.old
    mv edit/etc/resolv.conf edit/etc/resolv.conf.old
	cp /etc/resolv.conf /etc/hosts edit/etc/
	cp -r ~/Work/os/soft edit/home/
	cp ~/Work/os/sources.list edit/etc/apt/
    cp ~/Work/os/build.sh ./

    sudo mount --bind /dev/ edit/dev
    sudo chroot edit ./home/soft/install.sh

    sudo ./build.sh

	# chroot livecd/custom /bin/bash -l

    # sudo umount edit/dev

else
    echo "Starting Image Argument Missing"
    exit 1
fi
