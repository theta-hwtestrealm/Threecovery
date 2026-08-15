#!/usr/bin/env bash

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
[[ -z "$PROJECT_ROOT" ]] && PROJECT_ROOT="$(pwd)"
export PROJECT_ROOT

TOOLS="$PROJECT_ROOT/tools"
BINARIES="$PROJECT_ROOT/bin"

color_R=$(tput setaf 1); color_G=$(tput setaf 2); color_Y=$(tput setaf 208); color_N=$(tput sgr0)
color_C=$(tput setaf 6)

PASSWORD="alpine"

specs_system=""
specs_architecture=""

command="$1"
mode="none"

read -r -d '' USAGE << 'EOF'

Usage: 
    
    -h  --help      information (this)
    -q, --query     check installs and dependencies (recommended for first use)

    -d, --dir   extract information from files of dir (arg #2) to file (arg #3) 
    -s, --ssh   extract information from SSH port (arg #2)  to file (arg #3) 
    optional arg #4: master json to merge from (cannot be jsonl)
    -d can also run on just a singular file

    -f, --format    format record (arg #2) into (arg #3) 
    .txt is obviously not supported by -f, if you need merging, dont use txt
    as a side note, JSON is the original and most compatible format

    example:    ./recover.sh -s 2222 ./example_file.txt 
    example:    ./recover.sh -s 2222 ./example_file.txt ./other_record.json
    example:    ./recover.sh -d ./records_dir ./example_file.txt

    supported formats:  .json, .plist, .txt
    this only supports MacOS at the moment
    
    also, read the github at: https://github.com/theta-hwtestrealm/Threecovery
_
EOF



print() { echo "${color_B}${1}${color_N}"; }
input() { echo "${color_Y}[Input] ${1}${color_N}"; }
log() { echo "${color_G}[Log] ${1}${color_N}"; }
warn() { echo "${color_Y}[WARNING] ${1}${color_N}"; }
error() {
    echo
    echo -e "${color_R}[Error] ${1}${color_N}"
    [[ -n "$2" ]] && echo -e "${color_Y}${*:2}${color_N}"
    echo
    exit 1
}
pause() { input "Press Enter to continue (Ctrl+C to cancel)"; read -s; }

cleanup() {
    if [[ -d "../temp" ]]; then
        cd ..
        rm -r "temp"
    fi
}

execute() {
    local assumed_dir="$BINARIES/${specs_system}_$specs_architecture"
    [[ ! -d "$assumed_dir" && $specs_system == "MacOS" ]] && assumed_dir="$BINARIES/$specs_system"
    [[ ! -d "$assumed_dir" ]] && return 1
    local executable="$assumed_dir/$1"
    if [[ ! -x "$executable" ]]; then
        warn "Binary is unusable!"
        return 1
    fi
    $executable "${@:2}" 
}

send_out() {
    local input_file="$1"; local output_file="$2"
    local input_type="${input_file##*.}" #file extension
    local input_directory="$(dirname "$input_file")" 
    local output_type="${output_file##*.}" #file extension
    local output_directory="$(dirname "$output_file")" 
    
    [[ ! -d "$output_directory" ]] && error "the specified output directory does not exist"
    [[ input_type -ne "json" ]] && error "something is wrong with the result"
    [[ -s "$output_file" ]] && error "'$output_file' already exists and will not be overwritten." 

    case "$output_type" in
    "txt")
    python3 "$TOOLS/utils/txtify.py" "$1" "$2"
    return
    ;;

    "plist")
    python3 -c "import sys, json, plistlib; plistlib.dump(json.load(open(sys.argv[2])), open(sys.argv[1], 'wb'))" "$1" "$2"
    return
    ;;

    "json"|"jsonl");;

    *) 
    warn "the specified output '$output_type' is incorrect and being changed to json (master.json)"
    output_file="$output_directory/master.json" 
    ;;
    esac

    mv "$input_file" "$output_file"
}

ssh_download() { # $1 = port $2 = "-f/-d" checktype $3 = filepath $4 = output
    if execute "sshpass" -p $PASSWORD ssh root@127.0.0.1 -p$1 -o StrictHostKeyChecking=no "test $2 $3"; then
        execute "sshpass" -p $PASSWORD scp -p -P$1 -r -o StrictHostKeyChecking=no "root@127.0.0.1:$3" "$4" || true;
    else
        warn "File $3 doesnt exist"
    fi
}

ssh_download_all() {
    echo "${color_R}Dont touch the device${color_N}...   "
    if [ "$specs_system" = 'Linux' ]; then #SSHRD_Script
        sudo systemctl stop usbmuxd > /dev/null 2>&1 | true
        sudo killall usbmuxd > /dev/null 2>&1 | true
        sleep .1
        sudo usbmuxd -pf > /dev/null 2>&1 &
        sleep .1
    fi
    execute "iproxy" "$2" 22 > /dev/null 2>&1 &
    execute "sshpass" -p alpine ssh root@127.0.0.1 "-p$2" -o StrictHostKeyChecking=no "/usr/bin/mount_filesystems || true"
    ssh_download "$2" "-f" "/mnt2/mobile/Library/Preferences/com.apple.springboard.plist" "$1"
    ssh_download "$2" "-f" "/mnt2/mobile/Library/Accounts/Accounts3.sqlite" "$1"
    ssh_download "$2" "-d" "/mnt2/mobile/Library/TCC" "$1"
    ssh_download "$2" "-f" "/mnt2/mobile/Library/Keyboard/langlikelihood.dat" "$1"
    #ssh_download "$2" "-d" "/mnt2/db/dhcpclient" "$1" #TODO INSPECT OTHER CONTENTS
    
    killall iproxy > /dev/null 2>&1 | true
    if [ "$specs_system" = 'Linux' ]; then
        sudo killall usbmuxd > /dev/null 2>&1 | true
    fi
    echo "Done!"
}

scan_directory() {
    python3 "$TOOLS/bashtool_scanner.py" "$PWD" "$1"
}



echo
echo "${color_C}----------------------- THREECOVERY ☀️ -----------------------${color_N}"
echo "${color_C}RELEASE (0.0 🌕)${color_N}"

trap cleanup EXIT

case "$command" in
    "-q"|"--query") 
    mode="skip"
    ;;
    "-d"|"--dir")
    mode="file/directory"
    [[ ! -d "$2" && ! -f "$2" ]] && error '"$2" is an invalid file/directory'
    ;;
    "-s"|"--ssh")
    mode="ssh"
    ;;

    "-f"|"--format")
    error "Sorry, this doesnt exist yet."
    ;;

    "-h"|"--help"|*) 
    print "$USAGE"
    exit
    ;;
esac

if [[ $OSTYPE == "linux"* ]]; then
    specs_system="Linux"
    [[ $(uname -m) == "a"* && $(getconf LONG_BIT) == 64 ]] && specs_architecture="arm64" || specs_architecture="x86_64"
elif [[ $OSTYPE == "darwin"* ]]; then
    specs_system="MacOS"
    specs_architecture="$(uname -m)"
fi

if [[ ! -d "$BINARIES" ]]; then
    BINARIES="$(dirname "$(dirname "$PROJECT_ROOT")")"/bin
    if [[ ! -d "$BINARIES" ]]; then
        error "Something is wrong with the binaries"
    fi
fi


noresourcetxt=""
noresource=0
if ! command -v python3 &> /dev/null; then
    noresource+="Python3 is required to run this application and was not found. "
    noresource=1
fi

if ! command -v perl &> /dev/null; then
    warn "perl is not REQUIRED but is RECOMMENDED for more precise filter features"
fi

[[ noresource == 1 ]] && error "noresourcetxt"
[[ "$mode" == "skip" ]] && echo && print "Test finished successfully! ☀️" && echo && exit
print "running in $mode mode"
print "from source $2"
echo

mkdir -p temp
cd temp

if [[ "$mode" == "file/directory" ]]; then
    if [[ -f "$2" ]]; then
        mkdir -p collection
        cp "$2" collection
        scan_directory collection
    elif [[ -d "$2" ]]; then
        scan_directory "$2"
    fi

    send_out master.json "$3"
elif [[ "$mode" == "ssh" ]]; then
    mkdir -p collection 
    ssh_download_all collection "$2"
    scan_directory collection
    send_out master.json "$3"
fi

cd ..
rm -r temp

echo
echo "${color_C}All done!* ☀️${color_N}"
[[ "$mode" == "ssh" || "$mode" == "file/directory" ]] && print "Wrote to $3"
print "if something didnt go as expected, read the github"
echo