#!/bin/bash

sudo umount edit/dev

sudo chmod +w extract/mnt/casper/filesystem.manifest
sudo chroot edit dpkg-query -W --showformat='${Package} ${Version}n' | sudo tee extract/mnt/casper/filesystem.manifest

sudo cp extract/mnt/casper/filesystem.manifest extract/mnt/casper/filesystem.manifest-desktop

sudo sed -i '/ubiquity/d' extract/mnt/casper/filesystem.manifest-desktop

sudo sed -i '/casper/d' extract/mnt/casper/filesystem.manifest-desktop
sudo rm extract/mnt/casper/filesystem.squashfs
sudo mksquashfs edit extract/mnt/casper/filesystem.squashfs -b 1048576 -comp xz -Xdict-size 100%

printf $(sudo du -sx --block-size=1 edit | cut -f1) | sudo tee extract/mnt/casper/filesystem.size

cd extract/mnt
sudo rm md5sum.txt

find -type f -print0 | sudo xargs -0 md5sum | grep -v isolinux/boot.cat | sudo tee md5sum.txt

sudo genisoimage -D -r -V "$IMAGE_NAME" -cache-inodes -J -l -b isolinux/isolinux.bin -c isolinux/boot.cat -no-emul-boot -boot-load-size 4 -boot-info-table -o ../lc_16.04_alpha_0.1.iso .
