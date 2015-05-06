#!/usr/bin/bash

cp process_kill.py /usr/local/bin
cp initiation_logout.sh /usr/local/bin
cp com.logout_hook.agent.plist /Library/LaunchDaemons/

chmod 755 /usr/local/bin/process_kill.py
sudo chown root:wheel /usr/local/bin/process_kill.py

chmod 755 /usr/local/bin/initiation_logout.sh
sudo chown root:wheel /usr/local/bin/initiation_logout.sh

defaults write com.apple.loginwindow LogoutHook /usr/local/bin/process_kill.py
launchctl load /Library/LaunchDaemons/com.logout_hook.agent.plist
