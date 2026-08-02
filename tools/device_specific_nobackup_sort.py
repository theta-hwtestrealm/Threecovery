import sys
import json
import plistlib
import subprocess
import shutil
from pathlib import Path

toolkit = None

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
    plist = str(Path(work)/"live_fileplist")

    with open(master, "r") as file:
        master = json.load(file)

    plist = plistlib.load(plist)
    number = "None"

    #TODO extract

    result,code = fetchFromPerl("numPhReformat.pl", number, "strict")
    
    if code == None:
        pass #copied
    elif code != 0:
        number = f"|| {number} || Perl ran into a problem ({ code })"
    else:
        number = result

    master["AttachedPhoneNumbersAndEmails"].append(number)

    # package into output
    with open(result_path, "w") as file:
        json.dump(master, file, indent=4)

if __name__ == "__main__":
    extract()