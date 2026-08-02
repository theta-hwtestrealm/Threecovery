import sys
import json
import subprocess
import pickle
from pathlib import Path

def fetchFromPytool(tool, stdin, *args):
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

    for plist in (Path(dir)/"leases").iterdir():
        with open(plist, "rb") as data:
            wifi = fetchFromPytool("pytool_NSKAOpener.py", data.read(), "stream")
            wifibody = master["TemplatePieces"]["WifiNetwork"].copy()

            if "SSID" in wifi:
                wifibody["SSID"] = wifi["SSID"]
            if "LeaseStartDate" in wifi:
                wifibody["LastConnection"] = wifi["LeaseStartDate"]
            if "RouterIPAddress" in wifi:
                wifibody["RouterIP"] = wifi["RouterIPAddress"]

            master["KnownWiFi"].append(wifibody)

    # package into output
    with open(result_path, "w") as file:
        json.dump(master, file, indent=4)

if __name__ == "__main__":
    extract()