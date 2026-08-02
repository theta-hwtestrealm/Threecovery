import sys
import json
from datetime import datetime

def dateCocoaPT(timestamp1,timestamp2):
    finale=""

    if timestamp2 and timestamp2-timestamp1 == 1: timestamp2 -= 1 #FIX for weird behavior caused by network delay

    dt1 = datetime.fromtimestamp(timestamp1+978307200).strftime('%Y-%m-%d %H:%M:%S') + " UTC"
    dt2 = datetime.fromtimestamp((timestamp2 or 0)+978307200).strftime('%Y-%m-%d %H:%M:%S') + " UTC"
    if timestamp1 == -1: dt1 = "None" #display invalid dates as invalid rather than negative
    if timestamp2 == -1: dt2 = "None"

    if timestamp1==timestamp2 or not timestamp2:
        if dt1=="None": return ""
        finale = f"Access Date: {dt1}"
    else:
        finale += f"Oldest Usage: {dt1}"
        finale += f"       Latest Usage: {dt2}"
    return finale

def processMiscData(key,data):
    if isinstance(data, dict):
        return f"{key} : {json.dumps(data)}"
    elif isinstance(data, list):
        return f"{key} : {json.dumps(data)}"
    else:
        return f"{key} : {data}"



def txtify():
    if len(sys.argv) != 3:
        print("you might have a space in a system path or something, not designed to handle this")
        sys.exit(1)

    filein = sys.argv[1]
    fileout = sys.argv[2]

    master = None
    output = ""

    with open(filein, "r") as file:
        master = json.load(file)

    output += "\n\n"
    output += "|General Usage|--------------------------------------------------"
    output += "\n\n"
    output += dateCocoaPT(master['FirstUsed'],master['LastUsed'])
    output += "\n\n"
    output += "Top Picks: " + " | ".join(master["AttachedPhoneNumbersAndEmails"])
    output += "\n\n"
    output += "Flags: " + " ".join(master["MiscelaniousFlags"])
    output += "\n\n\n"
    output += "|Accounts|-------------------------------------------------------"
    output += "\n\n"
    for account in master["Accounts"]:
        output += f"    |{account['AccountType']}|\n"
        output += f"    |" + "|".join([account['Username'],account['DisplayUsername']])
        output += "\n"
        if account["AccountOwnerLegalName"] != "": 
            output += f"    |{account['AccountOwnerLegalName']}|\n"
        output += "\n\n"
        output += "    " + dateCocoaPT(account['FirstUsed'],account['LastUsed'])
        output += "\n\n"
        if len(account["AttachedPhoneNumbers"]) > 0:
            output += "    Phone Numbers: " + " ".join(account["AttachedPhoneNumbers"])
            output += "\n\n"
        for k, item in account["MiscelaniousData"].items():
            output += "    " + processMiscData(k,item)
            output += "\n"
        output += "    -------------------------------------------------------\n\n"
    output += "\n\n"
    output += "|Apps|-------------------------------------------------------"
    output += "\n\n"
    for app in master["Apps"]:
        output += f"    |{app['Name']}|\n"
        output += "    " + dateCocoaPT(app['FirstUsed'],app['LastUsed'])
        if app["NumEmojisUsed"] > 0:
            output += f"    Emojis used: {app['NumEmojisUsed']}\n"
        output += "\n\n"
    output += "\n\n"
    output += "|Wi-Fi|-------------------------------------------------------\n\n"
    for network in master["KnownWiFi"]:
        output += f"    |Network Name: {network['SSID']}|\n"
        output += f"    |{dateCocoaPT(network['LastConnection'],None)}|IP: {network['RouterIP']}|\n"

    with open(fileout, "w") as file:
        file.write(output)



if __name__ == "__main__":
    txtify()