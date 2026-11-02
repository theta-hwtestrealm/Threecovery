# Threecovery ☀️
- README2.MD for why this exists

- This is __NOT__ a bruteforce tool.. but check README2.MD~!

- The device cannot be reset. All information is scrubbed and to my knowledge is not redownloaded or still stored

- This tool is also a good way to see usage statistics and other unique information.

- Use at your own peril, at your own demise ⛈️ 
    <sub>(Only use if you're confident it's permissable)</sub>

## Usage Guide
- Threecovery only works on MacOS silicon and MacOS x86 right now.
- Threecovery targets any iOS device, provided you can mount filesystems and download unprotected files from `/mnt2`
- This tool is focusing on iOS 10.3-15.8.8


### You must start by booting an SSH Ramdisk. Start by reading *"A Cheat-sheet of tools to use with Threecovery"*

before first use, run `sudo bash ./runmefirst.sh`

  __-h  --help__      information
  
  __-q, --query__      check installs and dependencies quickly

  __-d, --dir__   extract information from files of dir <sub>(arg #2)</sub> to file <sub>(arg #3)</sub> *<sub>optional arg #4: master json to merge from</sub>*
  
  __-s, --ssh__   extract information from SSH port <sub>(arg #2)</sub> to file <sub>(arg #3)</sub> *<sub>optional arg #4: master json to merge from</sub>*

  __-f, --format__    format record <sub>(arg #2)</sub> into <sub>(arg #3)</sub>  *<sub>(.txt is obviously not supported by -f, if you need merging, dont use txt)</sub>*

  *<sub>optional arg #4: master json to merge from is actually not complete and i dont know if i intend to fix it </sub>*
  
  as a side note, JSON is the original and most compatible format, and __-d__ can also run on just a singular file

  ### Examples
Example below displays all help info
```zsh
./recover.sh -h
```
Example below connects to port 2222, downloads files, and outputs extraction result to example_file.txt 
```zsh
./recover.sh -s 2222 ./example_file.txt
```
instead of downloading from a device, you can also specify a folder with the files inside
```zsh
./recover.sh -d ./records_dir ./example_file.txt
```
  Remember, use 6414 for Legacy iOS Kit, 2222 for SSHRD_Script and its forks, 2236 is default for QwQramdisk

  Supported formats:  .json, .plist, .txt, omitting filetype will create a folder with all resources + txtify

## A Cheat-sheet of tools to use with Threecovery

__9.0-9.3.6, 64 bit:__ Very early in development, not tested,  try QwQramdisk

__10.0-10.3.3, 64 bit:__ This is a very mixed bag, getting an SSH Ramdisk to work can be challenging and i wasn't able to on A7. Provided you can download from /mnt2 without crashing, Threecovery supports it.

__A7 (iPhone 5s, iPad Air, iPad Mini 2/3) iOS 11.0-12.5.8:__ Boot an SSH Ramdisk with Legacy iOS kit, mount filesystems, then do `./recover.sh -s 6414 arg ./OUTPUT.txt`

__A8, A9, A10, A11, iOS 10.3-15.8.8__: SSHRD_Script (Or it's forks, such as iPh0ne4s SSHRD_Script), then `./recover.sh -s 2222 ./OUTPUT.txt`

__A9x, A10x, A11, iOS 16.0-18.7.9:__ No recommended tools yet, but it should definitely be possible

__A12/A13:__ No recommended tools yet, but it should be possible

## Unsupported, see below for other, better tools to use.
  
__A7/A8/A8x, iOS 7.0-8.4.1 (Disabled+Infinite Attempt):__ iPh0ne4s/SSHRD_Script `--bruteforce` command
__A7/A8/A8x, iOS 7.0-8.4.1 find passcode:__ [j1ans/QwQRamdisk](https://github.com/j1ans/QwQramdisk) and [j1ans/Brute](https://github.com/j1ans/Brute)

__armv6/armv7 devices (Disabled+Infinite Attempt) iOS 1.0-8.4.1:__ download `/mnt2/mobile/Library/Preferences/com.apple.springboard.plist` in Legacy iOS Kit SSH Ramdisk, set failed attempts to `-9999` and reupload it. You should also __fully delete and remove__ other SBDeviceLockedBlocked values to remove disabled.

__armv7 devices (Disabled+Infinite Attempt) (iOS 9-10):__ [Legacy iOS Kit instead of Sliver, use XPlist instead of plist edit pro, i use FileZilla instead of cyberduck](https://youtube.com/watch?v=DT_NlKdSCHw) 

__armv7 devices:__ [you'd better use this](https://github.com/tuanemss/32bit-Bruteforce-Passcode/releases) (but if you have a 6 digit device, you may use [iwannabrute](https://github.com/platinumstufff/iwannabrute))
  
__Any device with infinite passcode attempts but no automatic method:__ [look at this tool](https://github.com/theta-hwtestrealm/pwd-and-teleprompter)

## Bugs
- Cellular-related data is not implemented for now
- "Binary is unusable" means you must run `sudo bash ./runmefirst.sh`
- "REMOTE HOST IDENTIFICATION HAS CHANGED!", run `rm -f ~/.ssh/known_hosts`
- if you use this with "Legacy iOS Kit" the ramdisk menu will be unusable after and you must reboot manually.
- if you use this while having another SSH window open, it will close.

## Notable features
- Opens NSKeyedArchivers (very roughly, prone to bugs, and in python)
- Interacts with various other linked data formats (e.g, understanding Apple Core Data logic)
- Various tools for different situations
- Intuitive enough to use

## How this works:
  On vulnerable devices, you can [boot SSH Ramdisks](https://theapplewiki.com/wiki/SSH_Ramdisk) and download ["Class D" files](https://support.apple.com/guide/security/data-protection-classes-secb010e978a/web). This includes metadata, which contains valuable information despite not being encrypted. The files come in proprietary formats and it's hard to sort through valuable and worthless data.

## Continue with README2.MD