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

def parseAllDetectedApps(master,plist):
    appnames=[]

    if "SBDisplayIDsWithBadgingEnabled" in plist:
        for app in plist["SBDisplayIDsWithBadgingEnabled"]:
            appnames.append(app)

    if "SBDefaultKeyCommandTabPlistRepresentation" in plist:
        for subitem in plist["SBDefaultKeyCommandTabPlistRepresentation"]:
            appnames.append(subitem["bundleID"])

    if "SBDefaultKeyDockRecentsPlistRepresentation" in plist:
        for subitem in plist["SBDefaultKeyDockRecentsPlistRepresentation"]:
            appnames.append(subitem["bundleID"])

    for name in appnames:
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

        app_exists = False
        for anyapp in master["Apps"]:
            if anyapp["Name"] == final: app_exists = True
        if app_exists: continue
        newapp = master["TemplatePieces"]["App"].copy()
        newapp["Name"] = final
        master["Apps"].append(newapp)

def parseWallpaperNames(master,plist):
    if "SBHomeScreenWallpapers" in plist:
        for theme,item in plist["SBHomeScreenWallpapers"].items():
            newpaper = master["TemplatePieces"]["Wallpaper"].copy()
            newpaper["imageName"] = item["SBWallpaperNameKey"]
            master["Media"]["wallpapers"]["homescreen"][theme] = newpaper
    if "SBLockScreenWallpapers" in plist:
        for theme,item in plist["SBLockScreenWallpapers"].items():
            newpaper = master["TemplatePieces"]["Wallpaper"].copy()
            newpaper["imageName"] = item["SBWallpaperNameKey"]
            master["Media"]["wallpapers"]["lockscreen"][theme] = newpaper

def parseOther(master,plist):
    if "SBParentalControlsMCContentRestrictions" in plist:
        master["MiscelaniousFlags"].append("SpringboardChildRestrictions")

    

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
    plist = str(Path(work)/"live_file.plist")

    with open(master, "r") as file:
        master = json.load(file)

    with open(plist, "rb") as file:
        plist = plistlib.load(file)


    parseAllDetectedApps(master,plist)
    parseWallpaperNames(master,plist)
    parseOther(master,plist)

    # package into output
    with open(result_path, "w") as file:
        json.dump(master, file, indent=4)

if __name__ == "__main__":
    extract()