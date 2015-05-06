#!/usr/bin/python

import sys
import os
import subprocess

important_proc = [
	'/sbin/launchd',
	'/usr/sbin/distnoted',
	'/usr/sbin/cfprefsd',
	'/usr/libexec/xpcd',
	'/System/Library/PrivateFrameworks/TCC.framework/Resources/tccd',
	'com.apple.IconSe',
	'/usr/libexec/secd',
	'com.apple.imdpersistence.IMDPersistenceAgent',
	'/System/Library/Frameworks/Security.framework/Versions/A/Resources/CloudKeychainProxy.bundle/Contents/MacOS/CloudKeychainProxy',
	'NetAuthSysAgent',
	'gssd',
	'mdworker',
	'/System/Library/Frameworks/CoreServices.framework/Frameworks/Metadata.framework/Versions/A/Support/mdflagwriter',
	'/System/Library/PrivateFrameworks/SyncedDefaults.framework/Support/syncdefaultsd',
	'lsregister',
	'CVMCompiler',
	'com.apple.ShareK',
	'com.apple.NotesM',
	'SandboxedService',
	'com.apple.sbd',
	'DataDetectorsDyn',
	'com.apple.InputM',
	'com.apple.NotesM',
	'com.apple.iCloud',
	'com.apple.BKAgen',
	'com.apple.appsto',
	'com.apple.geod',
	'com.apple.speech',
	'SSPasteboardHelp',
	'com.apple.Charac',
	'com.apple.audio.',
	'com.apple.intern',
	'com.apple.CoreSi',
	'com.apple.hiserv',
	'mdworker32',
	'iCloudAccountsMi',
	'pkd',
	'secinitd',
	'findNames',
	'com.apple.CloudP',
	'pluginkit',
	'ssh-agent',
	'com.apple.Speech',
	'Dropbox',
	'dbfseventsd',
	'Dropbox109',
	'seaf-daemon',
	'ccnet'
]

users = os.listdir("/home")

print(users)

ps = subprocess.check_output(['/bin/ps', '-u', users[0]])
ps = ps.splitlines()
active_process = []
for process in ps:
    temp = process.split()
    active_process.append(temp[4])
    active_process = list(set(active_process))

leftovers = set(active_process)-set(important_proc)

print(leftovers)

for user in users:
    home_directory = "/Volumes/Macintosh\ HD/home/"+user
    home_dir = "/home/"+user
    try:
        for process in leftovers:
                subprocess.call(['/usr/bin/killall', process, '-u', user])
        subprocess.call(['/sbin/umount', '-f', home_directory])
	subprocess.call(['/sbin/umount', '-f', home_dir])
    except subprocess.CalledProcessError:
		try:
			subprocess.call(['/sbin/umount', '-f', home_directory])
		except subprocess.CalledProcessError:
			continue
    continue
