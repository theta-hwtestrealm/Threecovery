import sys
import json
import sqlite3
import subprocess
import shutil
from pathlib import Path

toolkit = None

def fetchTimestampComp(firstused, lastused, *timestamps):
    for timestamp in timestamps:
        if timestamp == None or timestamp == -1: continue
        if firstused == -1 or timestamp < firstused: firstused = timestamp
        if timestamp > lastused: lastused = timestamp
    return firstused, lastused

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

def parseDB(master,cursor):
    cursor.execute("SELECT client, last_modified FROM access")
    apps = cursor.fetchall()

    for accountitem in apps:
        name = accountitem["client"]
        lastmod = accountitem["last_modified"]-978307200

        result,code = fetchFromPerl("appNameReformat.pl", name, "strict")
        final = ""

        if code == None:
            final = name
        elif code == 10:
            continue
        elif code != 0:
            final = f"|| {name} || - Perl ran into a problem ({ code })"
            print(final)
            continue
        else:
            final = result

        appbody = None

        for anyapp in master["Apps"]:
            if anyapp["Name"] == final:
                appbody = anyapp
                break
        if appbody is None:
            appbody = master["TemplatePieces"]["App"].copy()
            appbody["Name"] = final
            master["Apps"].append(appbody)

        firstused,lastused = fetchTimestampComp(appbody["FirstUsed"],appbody["LastUsed"],lastmod)
        appbody["FirstUsed"] = firstused; appbody["LastUsed"] = lastused
        mfirstused,mlastused = fetchTimestampComp(master["FirstUsed"], master["LastUsed"], firstused,lastused)
        master["FirstUsed"] = mfirstused; master["LastUsed"] = mlastused

def extract():
    global toolkit
        
    if len(sys.argv) != 3:
        print("you might have a space in a system path or something, not designed to handle this")
        sys.exit(1)

    tools = Path(sys.argv[0]).resolve().parent
    work = sys.argv[1]
    dir = sys.argv[2]

    toolkit = tools

    master = str(Path(work)/"master.json")
    result_path = str(Path(work)/"result.json")

    with open(master, "r") as file:
        master = json.load(file)

    db = Path(dir)/"TCC.db"

    if db.is_file(): 
        db = sqlite3.connect(str(db))
        db.row_factory = sqlite3.Row
        cursor = db.cursor()
        parseDB(master,cursor)
    else:
        print("TCC.db does not exist")

    # package into output
    with open(result_path, "w") as file:
        json.dump(master, file, indent=4)

if __name__ == "__main__":
    extract()