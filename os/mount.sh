#!/bin/bash

curPath=$(pwd)
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
    imageName=${image##*/}
    sudo mount -o loop "$imageName" mnt
    mkdir extract
    sudo rsync --exclude=/casper/filesystem.squashfs -a mnt extract
    sudo unsquashfs mnt/casper/filesystem.squashfs
    sudo mv squashfs-root edit
    
    mv edit/etc/hosts edit/etc/hosts.old
    mv edit/etc/resolv.conf edit/etc/resolv.conf.old
	cp /etc/resolv.conf /etc/hosts edit/etc/
	cp -r $curPath/soft edit/home/
	cp $curPath/sources.list edit/etc/apt/
    cp $curPath/build.sh ./

    sudo mount --bind /dev/ edit/dev
    sudo mount -o bind /run/ edit/run
    sudo chroot edit ./home/soft/install.sh
    #sudo chroot edit
    sudo ./build.sh

	# chroot livecd/custom /bin/bash -l

    # sudo umount edit/dev

else
    echo "Starting Image Argument Missing"
    exit 1
fi
