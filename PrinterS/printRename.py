import csv
import os
import platform
from pprint import pprint

# what about un_dc_ac, un_dc_b queue? is it color?

# write mac and win side scripts to get all printer names

# Write mac and win side scripts to change the printers

# Also write a reporter:
    # Will send a note notifying the os, ws# and what has been changed

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
    print("REPORT")

def identifyBW(queues):
    bws = []
    for queue in queues:
        for subqueue in queue.lower().split():
            if "b&w" in queue.lower():
                bws.append(queue)
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

def winRun(column):
    testCaseWS = '9552'
    if testCaseWS in column["WS#"]:
        WS_DB_index = column["WS#"].index(testCaseWS)
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

def macRun(column):
    testCaseWS = '9552'
    if testCaseWS in column["WS#"]:
        WS_DB_index = column["WS#"].index(testCaseWS)
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

def main():

    currentPlatform = platform.system()
    # Need to know how to get the workstation number from mac or pc

    with open('dataset_sep.csv', 'rb') as csvfile:
        reader = csv.reader(csvfile,delimiter=",")
        headers = reader.next()
        print(headers)
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