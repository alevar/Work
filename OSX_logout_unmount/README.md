The logoutHook is designed for easy implementation on OSX 10.4 and later (has only been tested on OSX 10.9 so far).

The package includes the following:

1. installer.sh - a bash installer that copies the files over to their destinations, sets the permissions and ownership and binds the necessary files to other services.
2. com.logout_hook.agent.plist - the xml hook placed under LaunchDaemons
3. initiation_logout.sh - a bash script that in turn executes the python script
4. process_kill.py - the main program that is executed at logout, checks for the remaining processes, kills the unnecessary ones and follows by unmounting the home directory from both "/home/" and "Volumes/Macintosh\ HD/home/"
