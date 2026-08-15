# Threecovery ☀️
Apple has had a bad habit for more than a decade, locking devices to their original owners without permission or knowledge. When one receives another’s old device, its more often than not locked without any of the two parties knowledge.

- Jump to the bottom for the reason this exists

- This is __NOT__ a bruteforce tool.. but maybe check out the bottom of the page~!

- The device cannot be reset. All information is scrubbed, and i haven't found any unobfuscated data

- This tool is also a good way to see usage statistics and other very unique information that would take you hours to collect otherwise

- Use this at your own peril, at your own demise! ⛈️ 
    <sub>(Please only use if you're confident in your usage and it's permissibility)</sub>

## How this works:
  On vulnerable devices, you can [boot SSH Ramdisks](https://theapplewiki.com/wiki/SSH_Ramdisk) and download ["Class D" files](https://support.apple.com/guide/security/data-protection-classes-secb010e978a/web). This includes metadata, which can still contain valuable information you might not expect. However, processing this data is also a challenge. The files come in proprietary formats and its hard to sort through valuable and worthless data.

## Usage Guide
- Threecovery only works on MacOS silicon and MacOS x86 right now. Linux support will come and perhaps Windows support too (ONLY x86 is planned for these)
- Threecovery targets any iOS device, provided you can mount filesystems and download unprotected files from `/mnt2`
- It must be noted that this tool is in desperate need of testing, and is focusing on iOS 10.3-15.8.8


### You must start by booting an SSH Ramdisk and mounting filesystems. Start by reading *"A Cheat-sheet of tools to use with Threecovery"*

before first use, run `sudo bash ./runmefirst.sh`

  __-h  --help__      information
  
  __-q, --query__      check installs and dependencies quickly

  __-d, --dir__   extract information from files of dir <sub>(arg #2)</sub> to file <sub>(arg #3)</sub> *<sub>optional arg #4: master json to merge from</sub>*
  
  __-s, --ssh__   extract information from SSH port <sub>(arg #2)</sub> to file <sub>(arg #3)</sub> *<sub>optional arg #4: master json to merge from</sub>*

  __-f, --format__    format record <sub>(arg #2)</sub> into <sub>(arg #3)</sub>  *<sub>(.txt is obviously not supported by -f, if you need merging, dont use txt)</sub>*
  
  as a side note, JSON is the original and most compatible format, and __-d__ can also run on just a singular file

  ### Examples
```zsh
./recover.sh -h
```
```zsh
./recover.sh -s 2222 ./example_file.txt
```
```zsh
./recover.sh -s 2222 ./example_file.txt ./other_record.json
```
```zsh
./recover.sh -d ./records_dir ./example_file.txt
```
  Remember, use 6414 for Legacy iOS Kit

  Supported formats:  .json, .plist, .txt

## A Cheat-sheet of tools to use with Threecovery

__10.0-10.3.3, 64 bit:__ This is a very mixed bag, getting an SSH Ramdisk to work can be challenging and i wasn't able to on A7. Provided you can download from /mnt2 without crashing, Threecovery supports it.

__A7 (iPhone 5s, iPad Air, iPad Mini 2/3) iOS 11.0-12.5.8:__ Boot an SSH Ramdisk with Legacy iOS kit, mount filesystems, then do `./recover.sh -s 6414 arg ./OUTPUT.txt`

__A8, A9, A10, A11, iOS 10.3-15.8.8__: SSHRD_Script (Or its forks, such as iPh0ne4s SSHRD_Script), then `./recover.sh -s 2222 ./OUTPUT.txt`

__A9x, A10x, A11, iOS 16.0-18.7.9:__ No recommended tools yet, but it should definitely be possible

__A12/A13:__ No recommended tools yet, but it should definitely be possible

## Unsupported, see below for other, better tools to use.
- __Threecovery is still the only public tool for armv7/armv6 devices with alphanumeric, or infinite passcodes__
  
__A7/A8, iOS 7.0-8.4.1:__ iPh0ne4s SSHRD_Script `--bruteforce` command (it also removes Disabled)

__armv6/armv7 devices (Disabled+Infinite Attempt) iOS 1.0-8.4.1:__ download `/mnt2/mobile/Library/Preferences/com.apple.springboard.plist` in Legacy iOS Kit SSH Ramdisk, set failed attempts to `-9999` and reupload it. You can also __fully delete and remove__ other SBDeviceLockedBlocked values to remove disabled.

__armv7 devices:__ [you'd better use this](https://github.com/tuanemss/32bit-Bruteforce-Passcode/releases) (but if you have a 6 digit device, you may use [iwannabrute](https://github.com/platinumstufff/iwannabrute))

__armv7 devices (Disabled+Infinite Attempt) (iOS 9-10):__ [Legacy iOS Kit instead of Sliver, use XPlist instead of plist edit pro, i use FileZilla instead of cyberduck](https://youtube.com/watch?v=DT_NlKdSCHw)
  
__Any device where you already have infinite passcode attempts:__ [look at this convenient tool designed to assist you](https://github.com/theta-hwtestrealm/pwd-and-teleprompter)

__9.0-9.3.6, 64 bit:__ Likely this kind of tool is impossible and there isn't any other public information, which is unfortunate due to Activation Error. You cannot download from SSH

## Bugs
- Cellular-related data is not implemented due to only testing on a 15.8.8 ipad air 2
- a LOT should be added to the formatting tools, its still very empty
- code is also very messy, i was a little rushed.
- "Binary is unusable" means you must run `sudo bash ./runmefirst.sh`
- "REMOTE HOST IDENTIFICATION HAS CHANGED!", run `rm -f ~/.ssh/known_hosts`
- if you use this with a tool like "Legacy iOS Kit" the ramdisk will be unusable after and you must reboot manually.
- "All"

## Describing notable features
- Opens NSKeyedArchivers (very roughly, prone to bugs, and in python)
- Interacts with various other linked data formats (e.g, understanding Apple Core Data logic)
- Various tools for different situations
- Intuitive enough to use
    
## This project is meant to demonstrate numerous subjects, but it mostly focuses on unreset BFU devices
### Myself and others feel like dodging activation lock is like stepping through a minefield. This is a small documentation about the phenomenon. Also, lot of the quotes below are personal observations, but it must be noted, that Apple and Android devote mass effort keeping device owners anonymous unless they choose not to be (Medical ID, Lost Mode contact, Wallpaper, Etc). 
`^` means i am looking for a source or more info on a fact.
### A summary about Activation Lock: 
iDevices with this feature enabled, will cease to work, showing a message that they are locked to e******@icloud.com or e******@e******.com or (***) ***-1234. [This lock enables immediately when you log into an iDevice via iCloud, it is controlled by "Find My"](https://support.apple.com/en-us/108794) and is strictly tied to apples servers unlike its often only partial implementation on Android`^`. Apple may, for certain devices running iOS 11+, allow you to unlock a device with its previous passcode, but it is unreliable.`^`
### Apple will also, by default [not allow you to preserve the current version of iOS from BFU](https://support.apple.com/en-us/118430?iphone-authentication-type=iphone-with-face-id), excluding [remote or panic wipes](https://support.apple.com/guide/deployment/erase-devices-dep0a819891e/web). Some reported being asked to log into icloud on device just to reset without updating.`^`
### Trying to log into an iCloud account too many times may disable it.`^` Accounts may be permanently disabled without your knowledge for other reasons. [There is no reliable way to remove Activation Lock on these devices](https://discussions.apple.com/thread/256152582?sortBy=rank)
- [If you turn off Activation Lock remotely, and don't log out on-device after 30 days, when you reconnect to the internet Activation Lock will re-enable](https://support.apple.com/guide/icloud/remove-a-device-mmfc0eeddd/icloud). but some claim, and from my experience, this doesnt always happen.
- Many do not know about, n/or [do not understand how Activation Lock works](https://www.ifixit.com/News/34072/apples-activation-lock-will-make-it-very-difficult-to-refurbish-macs) due to a lack of [documentation](https://support.apple.com/en-us/108794).
- In my own testing, BFU iDevices will use SIM/ESIM, and may connect to public Wi-Fi with no password if it has a familiar name *However this can be used as an unlock method, or to trigger a remote wipe.*
- In my personal analysis, roughly 60% of iDevices are unreset, 80% are Activation Locked, 5% have a visible "Lost" message, and 50% of contacts are unreachable but it depends on your item sources
- [Apple removed their official Activation Lock checking website around or before January 2017](https://www.macrumors.com/2017/01/30/activation-lock-website-used-in-hack/), leaving users with [unreliable third-party websites](https://discussions.apple.com/thread/8086519?sortBy=rank) that often demand payment, or are full of ads, yet i find are usually correct. However people are always sorry when they aren't.
- People are frustrated, saying Apple has [ignored, shortsighted, or manufactured this problem and are benefiting from its consequences](https://www.ifixit.com/News/34072/apples-activation-lock-will-make-it-very-difficult-to-refurbish-macs)
- Apple hasn't found or wont publish a solution to this problem, nor will document it themselves.
- Apple has no known incentive to fix this problem, [everyone knows buying new is more profitable](https://www.ifixit.com/News/61140/what-is-right-to-repair)
- [Despite being a Right to repair issue, few are talking about it, though it has gotten more attention recently](https://www.ifixit.com/News/98249/activation-locks-are-trashing-millions-of-usable-phones-refurbishers-tell-the-fcc)
- Apple historically, when they solved issues or added Right to repair features, [they did not apply to older devices/software or had oversights](https://medium.com/@denis_service36/hi-my-name-is-denis-6d60c01b56db)
- [This isn't an Apple specific problem](https://www.samsung.com/nz/support/mobile-devices/what-is-google-frp/), but they have [very clearly pioneered it](https://www.macrumors.com/2013/06/11/ios-7s-activation-lock-delivers-cautious-optimism-to-officials-concerned-over-mobile-device-thefts/)
- Apple is letting people get scammed, [phones are a staple on third party resale sites](https://export.ebay.com/en/resources/seasonal-guide-for-ebay-sellers/high-demand-items/), where often no party except apple is aware they are locked.
- Apple's only, undocumented, solution for "non-owners" is to take the device to an Apple store, where they are likely disposed of `^` or to "contact" the uncontactable owner who has the right to privacy, which apple silently enforces, even if that original owner may want the device back.
- "Lost" mode devices may not say they are lost if they're Activation Locked^
- Apple's only official solution for original owners or those immediate to them is a [death certificate, receipt, or other forms of proof](https://al-support.apple.com/#/al/agreement)
- Apple, around a decade ago would often just remove activation lock if you asked them, according to [Hugh Jeffreys](https://www.hughjeffreys.com/)`^`
- Apple appears to have started denying most forms of proof in late 2025 even from original owners, due to fraud. (especially eBay or unoriginal invoices)`^`
- [Many state apple has sub-par customer service in modern](https://youtu.be/efiO5UMd5rU), it is unfortunately a characteristic. Their approach is to solve issues before they occur, not after.`^`
- Often, older devices (around iOS 10 and lower) will "Deactivate" meaning when connected to Wi-Fi, around 2 minutes to 36 hours later it will Activation Lock`^`
- "Deactivated" devices also trap all personal information on them just due to their nature
- [On iOS 9 and earlier, it may be impossible or hard to log in on-device depending on the menu](https://discussions.apple.com/thread/256199780?sortBy=rank). Even iOS 11 servers are lacking upkeep, (eg, App Store is dead`^`), [with the release of Xcode 27, there's no guarantee the same wont happen to iOS 13 and 14](https://developer.apple.com/xcode/system-requirements/)
- Millions of iDevices are affected by this issue, and the number will only rise, it can be a larger issue than parts pairing.`^`
- On a lighter note, it *__is, now,__* possible to find who these BFU devices belonged to *__sometimes, and with this tool__*
### Okay, so what is activation?
"Activation" was [introduced in iOS 5 to replace the legacy iTunes setup which required a computer.](https://support.apple.com/en-us/102998), Apple controls the activation process, meaning every device needs a response, and to collect accurate data from apple (including which enables cellular). This was never originally an issue, [but with iOS 7 and Tim Cook, Activation Lock was added.](https://www.apple.com/newsroom/2013/06/10Apple-Unveils-iOS-7/), and [apples policies toughened](https://www.ifixit.com/News/34072/apples-activation-lock-will-make-it-very-difficult-to-refurbish-macs) over years [and they now offer high bounties](https://security.apple.com/bounty/categories/) for those able to crack it. Additionally, older systems face problems such as the [iOS 9 64 bit activation issue](https://www.youtube.com/watch?v=Qs6--1np7Rg&t=21s), and other more recent problems like the [8th July, 2026 Baseband unsigning incident](https://www.macrumors.com/2026/07/09/apple-pulls-ability-to-restore-iphone-5c-and-more/) but people still reported activation issue impacts afterwards `^`. [Additionally, most iDevices that have an IMEI starting with `9900` will activation error or activation loop](https://discussions.apple.com/thread/256149288?sortBy=rank) or *most* devices with a bad baseband or Audio IC failure, this is because apple always needs to verify many (dead) characteristics of your device to activate it (specifically, to prevent serial swapping)`^` Another issue that occurs is ["Please update this iDevice to Activate"](https://discussions.apple.com/thread/8552696?sortBy=rank) , and finally another issue is [Insert SIM to activate](https://support.apple.com/en-us/108914).
### But wait, there's also MDM Lock (Mobile Device Management) "Waiting for ____ to configure your device"
- MDM is much more complex, and something regular users wont see. However, it is extremely damaging at a large scale.
- John Bumstead [published a detailed video](https://youtu.be/uGgR4srMwLQ) which contained most of the key differences
- MDM comes after Activation Lock, if your device isn't activation locked you can often bypass it and retain all iCloud functionality`^`
### So, what are *my, current* feelings on Apple?
I still like Apple, and I love their solutions (especially pre-Cook). Some of these problems are extremely hard to work through whether you accept that or not, however, I feel disappointed that for over a decade Apple has pushed a sub-par policy or at the very least a policy with not enough exceptions, which they've only made more integral, and it's only gotten worse over time device by device amendment by amendment. Beyond this, they used quite unreasonable methods to seemingly hide this issue. Also, whether Apple likes it or not, I am here to temporarily solve the problem for them (they had a decade). Solved!

Final notes, some point out you can often find an email or number in plaintext if you know where to look. This is a good strategy, but there is other, unexpected and valuable data hidden too! Unrelated, I sour on people in Jailbreak communities who police data recovery discussion (or owners of paid tools) hiding this simple in practice information from those who need it.
