import csv
import os
import platform
import subprocess
import re
import logging
import time
from pprint import pprint

currentPlatform = platform.system()
if currentPlatform == "Windows":
    from _winreg import *

colorCodes = [ "color",
               "pcl"]

colorQueues = [ "ca_111_ac",
                "cf_cm_cc",
                "cf_cp_ac",
                "fm_fm_ac",
                "jn_210_ac",
                "ko_122_ac",
                "la_sd_ac",
                "lo_da_cc",
                "ma_ps_ac",
                "ma_rg_ac",
                "pl_ss_bc",
                "rc_at_cc",
                "rc_at_ec",
                "un_ad_ec",
                "un_dc_bc",
                "un_de_bc",
                "un_ds_cc",
                "un_pi_ac",
                "va_243_ac",
                "pl_2nd_cc",
                "un_so_bc",
                "lo_da_dc",
                "ma_it_bc",
                "pl_ss_ac",
                "pl_wr_ac",
                "sh_bio_ac",
                "un_ar_ac",
                "ko_323_bc",
                "lo_da_gc",
                "ma_hr_ac",
                "pl_pac_ac",
                "un_pu_cc"]

def report(queue):
    pass

def identifyBW(printers,queues):
    bws = []
    regex = re.compile(' [Bb][ ]*&[ ]*[Ww]')
    for queue in queues:
        for subqueue in queue.lower().split():
            if regex.search(printers[0][printers[1].index(queue)]) != None:
                bws.append(printers[0][printers[1].index(queue)])
    return list(set(bws))

def identifyColor(queues):
    colors = []
    for queue in queues:
        for subqueue in queue.lower().split():
            if subqueue in colorQueues or "color" in queue.lower():
                colors.append(queue)
    return list(set(colors))

def linRun(column):
    testCaseWS = '6841'
    if testCaseWS in column["WS#"]:
        WS_DB_index = column["WS#"].index(testCaseWS)
        printers = column["Printers"][WS_DB_index]
        colors = identifyColor(printers[1])
        bws = identifyBW(list(set(printers[1])-set(colors)))

        if len(colors) == 0 and len(bws) == 0:
            report(None)
        elif len(colors) != 0 and len(bws) == 0:
            print("WOO Color")
        elif len(colors) == 0 and len(bws) != 0:
            print("WOO BWS")
        else:
            print("WOO Both")

def winRun(column):
    
    logger = logging.getLogger('printerRenameApp')
    hdlr = logging.FileHandler('C:\Users\Administrator\printerRenameApp.log')
    formatter = logging.Formatter('%(message)s')
    hdlr.setFormatter(formatter)
    logger.addHandler(hdlr)
    logger.setLevel(logging.INFO)

    reportStr = ""

    logger.warning("MACHINE: %s",platform.node()[2:])
    logger.warning("OS: %s",currentPlatform)
    logger.warning("DATE/TIME: %s",time.strftime("%c") )

    def findPrinters():
        regPrintersPort = []
        regPrintersName = []
        
        aReg = ConnectRegistry(None,HKEY_LOCAL_MACHINE)
        logger.info("==========================")
        logger.info("ALL IDENTIFIED PRINTERS")
        logger.info("==========================")

        aKey = OpenKey(aReg,r"SYSTEM\CurrentControlSet\Control\Print\Printers")
        for i in range(1024):
            try:
                asubkey_name=EnumKey(aKey,i)
                asubKey=OpenKey(aKey,asubkey_name)
                ports=QueryValueEx(asubKey,"Port")
                names=QueryValueEx(asubKey,"Name")
                regPrintersPort.append(ports[0])
                regPrintersName.append(names[0])
                logger.warning('PRINTER_NAME/PORT: "%s"/"%s"',names[0],ports[0])
            except EnvironmentError:
                pass
        return [regPrintersName, regPrintersPort]

    def removeColors(colors):
        removed = []
        for color in colors:
            portIndex = printers[1].index(color)
            printName = printers[0][portIndex]
            command = 'printui.exe /dl /n "'+printName+'" /q'
            os.system(command)
            removed.append(printName)
        return removed

    def renameBW(bws):
        regex = re.compile(' [Bb][ ]*&[ ]*[Ww]')
        renamed = {}
        for bw in bws:
            if regex.search(bw.lower()) != None:
                newName = re.sub(' [Bb][ ]*&[ ]*[Ww]','',bw)
                print(newName)
                command = 'cscript C:\Windows\System32\Printing_Admin_Scripts\en-US\prncnfg.vbs -x -p "'+str(bw)+'" -z "'+newName+'"'
                os.system(command)
                renamed[bw] = newName
        return renamed
    
    WS_Number = platform.node()[2:]
    # if WS_Number in column["WS#"]:
    #     WS_DB_index = column["WS#"].index(WS_Number)
    #     printers2 = column["Printers"][WS_DB_index]
    printers = findPrinters()
    colors = identifyColor(printers[1])
    bws = identifyBW(printers,list(set(printers[1])-set(colors)))

    if len(colors) == 0 and len(bws) == 0:
        logger.warning("+++++++++++++++++++")
        logger.warning("WARNING: NO COLOR AND B&W PRINTERS FOUND")
        logger.warning("+++++++++++++++++++")
        report(None)
    elif len(colors) != 0 and len(bws) == 0:
        logger.warning("+++++++++++++++++++")
        logger.warning("WARNING: NO B&W PRINTERS FOUND")
        logger.warning("THE FOLLOWING COLOR PRINTERS WERE REMOVED")
        logger.warning("+++++++++++++++++++")
        removed = removeColors(colors)
        logger.warning(" ".join(removed))
    elif len(colors) == 0 and len(bws) != 0:
        logger.warning("+++++++++++++++++++")
        logger.warning("WARNING: NO COLOR PRINTERS FOUND")
        logger.warning("THE FOLLOWING B&W PRINTERS WERE RENAMED")
        logger.warning("+++++++++++++++++++")
        renamed = renameBW(bws)
        for key,value in renamed.items():
            logger.warning("WARNING: "+key+" RENAMED TO "+value)
    else:
        logger.warning("+++++++++++++++++++")
        logger.warning("THE FOLLOWING COLOR PRINTERS WERE REMOVED")
        logger.warning("+++++++++++++++++++")
        removed = removeColors(colors)
        logger.warning(" ".join(removed))
        logger.warning("+++++++++++++++++++")
        logger.warning("THE FOLLOWING B&W PRINTERS WERE RENAMED")
        logger.warning("+++++++++++++++++++")
        renamed = renameBW(bws)
        for key,value in renamed.items():
            logger.warning(key+" RENAMED TO "+value)

    # else:
    #     log.error("ERROR: %s","WORKSTATION IS NOT ON THE LIST")

def macRun(column):
    WS_Number = platform.node().strip(".")[0]
    if WS_Number in column["WS#"]:
        WS_DB_index = column["WS#"].index(WS_Number)
        printers = column["Printers"][WS_DB_index]
        colors = identifyColor(printers)
        bws = identifyBW(list(set(printers)-set(colors)))

        if len(colors) == 0 and len(bws) == 0:
            report(None)
        elif len(colors) != 0 and len(bws) == 0:
            print("WOO Color")
        elif len(colors) == 0 and len(bws) != 0:
            print("WOO BWS")
        else:
            print("WOO Both")

        print(WS_DB_index)
        print(printers)
        print(colors)
        print(bws)
    else:
        print("WS NOT ON THE LIST")

def main():

    with open('dataset_sep.csv', 'rb') as csvfile:
        reader = csv.reader(csvfile,delimiter=",")
        headers = reader.next()
        column = {h:[] for h in headers}
        for row in reader:
            for h, v in zip(headers, row):
                if(h == "Printers"):
                    column[h].append(v.split("\n"))
                else:
                    column[h].append(v)
                    
        if currentPlatform == "Linux":
            linRun(column)

        elif currentPlatform == "Windows":
            winRun(column)

        else:
            macRun(column)

if __name__ == "__main__":
    main()
