#!/usr/bin/python

import os
import sys, traceback

def main():
	print("ADDING KALI REPOSITORY KEYS \n")
	cmd1 = os.system("apt-key adv --keyserver pgp.mit.edu --recv-keys ED444FF07D8D0BF6")
	cmd2 = os.system("echo '# Kali linux repositories | Added by Katoolin\ndeb http://http.kali.org/kali kali-rolling main contrib non-free\ndeb http://repo.kali.org/kali kali-bleeding-edge main' >> /etc/apt/sources.list")
	
	print("UPDATING KALI REPOSITORIES \n")
	cmd3 = os.system("apt-get update -m")

	print("INSTALLING INFORMATION GATHERING UTILITIES")
	cmd = os.system("apt-get install -y acccheck ace-voip amap automater braa casefile cdpsnarf cisco-torch cookie-cadger copy-router-config dmitry dnmap dnsenum dnsmap dnsrecon dnstracer dnswalk dotdotpwn enum4linux enumiax exploitdb fierce firewalk fragroute fragrouter ghost-phisher golismero goofile lbd maltego-teeth masscan metagoofil miranda nmap p0f parsero recon-ng set smtp-user-enum snmpcheck sslcaudit sslsplit sslstrip sslyze thc-ipv6 theharvester tlssled twofi urlcrazy wol-e xplico ismtp intrace hping3 && wget http://www.morningstarsecurity.com/downloads/bing-ip2hosts-0.4.tar.gz && tar -xzvf bing-ip2hosts-0.4.tar.gz && cp bing-ip2hosts-0.4/bing-ip2hosts /usr/local/bin/")

	print("REMOVING KALI REPOSITORIES \n")
	infile = "/etc/apt/sources.list"
	outfile = "/etc/apt/sources.list"

	delete_list = ["# Kali linux repositories | Added by Katoolin\n", "deb http://http.kali.org/kali kali-rolling main contrib non-free\n","deb http://repo.kali.org/kali kali-bleeding-edge main\n"]
	fin = open(infile)
	os.remove("/etc/apt/sources.list")
	fout = open(outfile, "w+")
	for line in fin:
	    for word in delete_list:
	        line = line.replace(word, "")
	    fout.write(line)
	fin.close()
	fout.close()
	print "KALI REPOSITORIES REMOVED \n"

if __name__ == "__main__":
    main()