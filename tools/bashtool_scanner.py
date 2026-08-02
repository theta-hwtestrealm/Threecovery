import os
import sys
import json
import shutil
import subprocess
import sqlite3
from pathlib import Path

def run_sqlite(db,sql):
    with sqlite3.connect(str(db)) as conn:
        cursor = conn.cursor()
        plainsql = sql.read_text()
        cursor.executescript(plainsql)
        conn.commit()

def run_python(file,*args):
    command = ["python3", str(file)] + [str(item) for item in args]
    with subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, bufsize=1) as process: 
         for line in process.stdout: print(f"{line}", end="") 
         if process.returncode != None: print(f"\nFailed {process.returncode}")

def scan():
    if len(sys.argv) != 3:
        print("you might have a space in a system path or something, not designed to handle this")
        sys.exit(1)

    tools = Path(sys.argv[0]).resolve().parent
    work = sys.argv[1]
    downloads = sys.argv[2]
    master = Path(work)/"master.json"

    if not master.is_file():  #create new master
        master = Path(tools)/"utils"/"template.json"
        with open(str(master), "r") as file:
            master = json.load(file)
        with open(str(Path(work)/"master.json"), "w") as file:
            json.dump(master, file, indent=4)


    def merge_with_master():
        result = Path(work)/"result.json"
        if not result.is_file():
            print("No result was generated, skipping")
            return
        elif not (Path(work)/"master.json").is_file():
            print("No master exists, skipping")
            os.remove(str(result))
            return
        else:
            shutil.move(result,Path(work)/"master.json")
            print("finished overwrite")


    for item in Path(downloads).iterdir():
        print(f"dumping readable info from {item.name}")

        if item.name == "Accounts3.sqlite":
            live_path = Path(work)/"live_file.sqlite"
            shutil.copy2(item, live_path)
            run_sqlite(live_path, Path(tools)/"utils"/"acc3_cleanup_applejunk.sql")
            run_python(tools/"acc3_sort.py", work)
            merge_with_master()
        elif item.name == "com.apple.commcenter.device_specific_nobackup.plist":
            live_path = Path(work)/"live_file.plist"
            shutil.copy2(item, live_path)
            run_python(tools/"device_specific_nobackup_sort.py", work)
            merge_with_master()
        elif item.name == "com.apple.springboard.plist":
            live_path = Path(work)/"live_file.plist"
            shutil.copy2(item, live_path)
            run_python(tools/"springboard_sort.py", work)
            merge_with_master()
        elif item.name == "dhcpclient":
            run_python(tools/"dhcpclient_sort.py", work, item)
            merge_with_master()
        elif item.name == "TCC":
            run_python(tools/"TCC_sort.py", work, item)
            merge_with_master()
        else:
            print("nothing to dump, skipping invalid file/directory")


    # final cleanup
    with open(str(Path(work)/"master.json"), "r") as file:
        master = json.load(file)
    del master["TemplatePieces"]
    master["AttachedPhoneNumbersAndEmails"] = list(set(master["AttachedPhoneNumbersAndEmails"]))
    master["MiscelaniousFlags"] = list(set(master["MiscelaniousFlags"]))
    with open(str(Path(work)/"master.json"), "w") as file:
        json.dump(master, file, indent=4)


if __name__ == "__main__":
    scan()