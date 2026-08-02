import sys
import copy
import sqlite3
import json
import subprocess
import pickle
import shutil
from pathlib import Path

email_type_markers = [
    "appleID", "apple-id", "email-address", "primaryEmail", "forwardingEmail", "authorizationEmailSelection",
    "appleId",
]

date_type_markers_cocoa = [
    "AuthModeTimeStamp","lastAuthenticated", "auth-token-receipt-date", "WarmUpVerificationTimeStamp",
    "InRegistrationExpirationDate", "iCloudNotificationLastRegisterDate", "AKFollowUpAccountRefreshTimestamp",
    "altDSID-5-mod-date", "GKCredentialScope-5-mod-date",
]; 

date_type_markers_unix = [
    "add-timestampe", "LastEmailAliasesSyncDate",
]; 


onlyshowiftrue_type_markers = [
    "isManagedAppleID", "DMCIsManagementProfileLocked", "isSandboxAcct", "DeviceTrustRevoked", "isUnderage",
    "custodianEnabled", "iCloudFamily"
]

toolkit = None



def fetchAccountTypes(cursor): #get all accounttypes (their names) that werent of filtered accounts
    cursor.execute("SELECT Z_PK, ZACCOUNTTYPEDESCRIPTION FROM ZACCOUNTTYPE")
    types = cursor.fetchall()
    largest=0

    for row in types:
        index = row["Z_PK"]
        if index > largest: largest = index
    
    result = ["Unknown/Deleted/Filtered"] * (largest+1)

    for row in types:
        result[row["Z_PK"]] = row["ZACCOUNTTYPEDESCRIPTION"]

    return result

def fetchFromPytool(tool, stdin, *args): #pickling
    global toolkit

    command = [sys.executable, str(Path(toolkit)/"utils"/tool), *args]
    data = subprocess.run(command, input=stdin, capture_output=True, text=False)

    if not data.stdout and data.stderr:
        print("----------------------------------")
        print(data.stderr.decode('utf-8', errors='ignore'))
        print("----------------------------------")

    try:
        return pickle.loads(data.stdout)
    except Exception as e:
        print(f"pickle may have encountered an issue")
        return data.stdout.decode('utf-8', errors='ignore').strip()

def fetchFromPerl(tool, *args): #input, mode, etc arguments
    global toolkit

    if not shutil.which("perl"):
        return None, None

    try:
        command = ["perl", str(Path(toolkit)/"utils"/tool), *args]
        res = subprocess.run(command, capture_output=True, text=True, check=True)
        return res.stdout, 0
    except subprocess.CalledProcessError as e:
        return "", e.returncode

def formatPhone(number):
    result,code = fetchFromPerl("numPhReformat.pl", number, "strict")

    if code == None:
        return number
    elif code != 0:
        return f"|| {number} || Perl ran into a problem ({ code })"
    else:
        return result

def formatEmail(email):
    result,code = fetchFromPerl("emailReformat.pl", email, "strict")

    if code == None:
        return email
    elif code == 10:
        return None
    elif code != 0:
        return f"|| {email} || Perl ran into a problem ({ code })"
    else:
        return result


def fetchTimestampComp(firstused, lastused, *timestamps):
    for timestamp in timestamps:
        if timestamp == None or timestamp == -1: continue
        if firstused == -1 or timestamp < firstused: firstused = timestamp
        if timestamp > lastused: lastused = timestamp
    return firstused, lastused

def StupidClearSubDuplicates(anydict):
    origsql = str(Path(toolkit)/"utils"/"acc3_cleanup_applejunk.sql")

    with open(origsql, "r") as file:
        content = file.read()

    filtered_dict = {key: value for key, value in anydict.items() if key not in content}
    return filtered_dict




def appendPropertiesToAccount(properties, account):
    firstname=""
    lastname=""

    def spotIrregularities(message,look,reference): #lets you to print unknown values for debuggging
        for k,v in look.items(): 
            if k in reference: continue 
            print(message,k,"|",v)

    def onObject(aPT, aP):
        nonlocal firstname,lastname
        global email_type_markers

        if aPT == "firstName": firstname += aP
        elif aPT == "lastName": lastname += aP
        elif aPT == "FullUserName": account["DisplayUsername"] += aP
        elif aPT in email_type_markers: 
            formatted = formatEmail(aP)
            if formatted is not None: account["Electromail"].append(formatted)
        elif aPT in date_type_markers_cocoa:
            firstused,lastused = fetchTimestampComp(account["FirstUsed"], account["LastUsed"], aP)
            account["FirstUsed"] = firstused; account["LastUsed"] = lastused; 
        elif aPT in date_type_markers_unix:
            firstused,lastused = fetchTimestampComp(account["FirstUsed"], account["LastUsed"], aP - 978307200)
            account["FirstUsed"] = firstused; account["LastUsed"] = lastused; 
        elif aPT in onlyshowiftrue_type_markers: 
            if aP: account["MiscelaniousData"][aPT] = aP
        elif aPT == "appleIDAliases":
            if len(aP) > 0: account["MiscelaniousData"][aPT] = aP
        elif aPT == "invitation-context":
            if aP["extra"]: account["invitation-context-extras"] = aP["extra"]
            #aP["region-id"] == "R:US"
            account["AttachedPhoneNumbers"].append(aP["base-phone-number"])
            spotIrregularities(f"UNKNOWN invitation-context VALUE: ",aP,["base-phone-number","region-id","extra"])
        elif aPT == "handles":
            for i,handle in enumerate(aP):
                formatted = formatEmail(handle["uri"])
                if formatted is not None: account["Electromail"].append(formatted)
                spotIrregularities(f"handles UNKNOWN PIECE IN HANDLE {i}: ",handle,["status","is-user-visible","uri"])
                #handle["status"] == 5051
        elif aPT == "additionalInfo":
            for k,v in StupidClearSubDuplicates(aP).items():
                onObject(k,v)
        elif aPT == "phoneNumbers":
            for i,item in enumerate(aP):
                account["MiscelaniousData"][str(i)+"_"+item["type"]+"_phoneNumbers_subinfo"] = item["phoneNumber"]
                account["AttachedPhoneNumbers"].append(item["phoneNumber"])
                spotIrregularities(f"phoneNumbers UNKNOWN: ",item,["type","recentlyUsed","phoneNumber"])
                #["type"] == "2fa" ["recentlyUsed"] == 1
        elif aPT == "lastAgreedTerms": #irdk i'm too tired
            # ["metadata"] == "cylon,cyrus200"
            # ["countryCode"] == "R:US"
            #other data, not worth. a spotIrregularities as most info is junk and not worth saving
            pass
        else: account["MiscelaniousData"][aPT] = aP

    for row in properties:
        aPT = row["ZKEY"] #property type
        aP = fetchFromPytool("pytool_NSKAOpener.py", row["ZVALUE"], "stream")
        onObject(aPT,aP)
        
    if firstname != "" and lastname != "":
        account["AccountOwnerLegalName"] = ('"' + firstname + '" ' + lastname)

def parseAccountInformation(cursor, master):
    cursor.execute("SELECT Z_PK, ZACCOUNTTYPE, ZDATE, ZACCOUNTDESCRIPTION, ZUSERNAME FROM ZACCOUNT")
    accounts= cursor.fetchall()
    accounttypes = fetchAccountTypes(cursor)

    for account in accounts:
        index = account["Z_PK"]
        minor_username = account["ZUSERNAME"] or "No username"
        account_type_name = accounttypes[account["ZACCOUNTTYPE"]] or "Error - try without filter"

        cursor.execute("SELECT ZKEY, ZVALUE FROM ZACCOUNTPROPERTY WHERE ZOWNER = ?", (index,))
        properties = cursor.fetchall()
        Lusername = "Error"
        email = "None"

        accountBody = copy.deepcopy(master["TemplatePieces"]["Account"])

        if account["ZACCOUNTDESCRIPTION"] is None:
            Lusername = minor_username
        else:
            Lusername = (account["ZACCOUNTDESCRIPTION"] + " - " + minor_username)

        if minor_username.count('@') == 1 and minor_username.count('.') >= 1:
            email = minor_username
            pass

        formattedEmail = formatEmail(email)
        accountBody["AccountType"] = account_type_name
        accountBody["Username"] = Lusername
        if formattedEmail is not None: accountBody["Electromail"].append(formattedEmail)
        
        #properties contain all the good stuff
        appendPropertiesToAccount(properties, accountBody)

        firstused,lastused = fetchTimestampComp(accountBody["FirstUsed"], accountBody["LastUsed"], account["ZDATE"])
        accountBody["FirstUsed"] = firstused; accountBody["LastUsed"] = lastused; 


        #filter out duplicate emails
        accountBody["Electromail"] = list(set(accountBody["Electromail"]))
        accountBody["AttachedPhoneNumbers"]=list(set(formatPhone(item) for item in accountBody["AttachedPhoneNumbers"]))

        #SYNC WITH TEMPLATE
        #sync account timestamps with toplevel timestamps
        firstused,lastused = fetchTimestampComp(
            master["FirstUsed"], master["LastUsed"], accountBody["FirstUsed"],accountBody["LastUsed"]
        )
        master["FirstUsed"] = firstused; master["LastUsed"] = lastused

        #sync account emails/nums
        for email in accountBody["Electromail"]:
            master["AttachedPhoneNumbersAndEmails"].append(email)
        for num in accountBody["AttachedPhoneNumbers"]:
            master["AttachedPhoneNumbersAndEmails"].append(num)

        #skip local account (which wont have interesting information)
        if accountBody["MiscelaniousData"].get("isLocalAccount") is True:
            continue

        master["Accounts"].append(accountBody)



def extract():
    global toolkit

    if len(sys.argv) != 2:
        print("you might have a space in a system path or something, not designed to handle this")
        sys.exit(1)

    tools = Path(sys.argv[0]).resolve().parent
    work = sys.argv[1]

    toolkit = tools

    master = str(Path(work)/"master.json")
    result_path = str(Path(work)/"result.json")
    db = str(Path(work)/"live_file.sqlite")
    db = sqlite3.connect(db)
    db.row_factory = sqlite3.Row
    cursor = db.cursor()

    with open(master, "r") as file:
        master = json.load(file)

    parseAccountInformation(cursor, master)

    # package into output
    with open(result_path, "w") as file:
        json.dump(master, file, indent=4)


if __name__ == "__main__":
    extract()