#!/bin/sh

rm /usr/local/lc_unity_full_2.iso
mkdir /Volumes/Data
mount -t smbfs smb://kbox:alum4pwd@lis-software.luther.edu/Software/Macintosh /Volumes/Data/
cp /Volumes/Data/lc_unity_full_3.iso /usr/local
umount -f /Volumes/Data
chmod a+r /usr/local/lc_unity_full_3.iso