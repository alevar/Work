#!/usr/bin/python3

import os
import argparse
import sys
import subprocess

def main(argv):
    curPath = os.path.dirname(os.path.realpath(__file__))

    inputFile = 'ubuntu.iso'
    outputFile = 'custom.iso'
    programList = []
    softwareINSTALL = ''
    softwareREMOVE = ''
    pyReq = ''

    parser=argparse.ArgumentParser(description='''Help Page''')
    parser.add_argument('-i','--ifile',required=True,type=str,help="path to the base image. Provided image will be used to produce custom iso.")
    parser.add_argument('-o','--ofile',type=str,help="path and name for saving the output custom image")
    parser.add_argument('-p','--progs',nargs='*',type=str,help="Any number of .deb applications downloaded for the new image may be specified here")
    parser.add_argument('-a','--add',type=str,help="Path to the softwareINSTALL.txt file containing a list of all packages to be isntalled via apt-get install")
    parser.add_argument('-r','--remove',type=str,help='Path to the softwareREMOVE.txt file containing a list of all packages to be removed via apt-get remove --purge')
    parser.add_argument('-t', '--req',type=str,help='Path to the requirements.txt file which contains python modules and libraries to isntall via pip3')

    args = parser.parse_args()
    inputFile = args.ifile
    outputFile = args.ofile
    programList = args.progs
    softwareINSTALL = args.add
    softwareREMOVE = args.remove
    pyReq = args.req

    print("INPUT ", inputFile)
    print("OUTPUT ", outputFile)
    print("programList ", programList)
    print("softwareINSTALL ", softwareINSTALL)
    print("softwareREMOVE ", softwareREMOVE)

    if(os.path.exists(curPath+"/soft")):
        os.system("rm -r soft")
        os.makedirs(curPath+"/soft")

    else:
        os.makedirs(curPath+"/soft")

    if(args.progs):
        os.makedirs(curPath+"/soft/progs/")
        for program in programList:
            command = "cp -r "+program+" "+curPath+"/soft/progs"
            os.system(command)

    if(args.add):
        os.system("cp "+softwareINSTALL+" ./soft/softwareINSTALL.txt")
    if(args.remove):
        os.system("cp "+softwareREMOVE+" ./soft/softwareREMOVE.txt")
    if(args.req):
        os.system("cp "+pyReq+" ./soft/requirements.txt")

    os.system("cp install.sh net.py ./soft")

    os.system("./mount.sh "+inputFile)

if __name__ == "__main__":
    main(sys.argv[1:])
