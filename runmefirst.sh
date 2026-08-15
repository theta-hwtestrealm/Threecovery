#!/usr/bin/env bash

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
[[ -z "$PROJECT_ROOT" ]] && PROJECT_ROOT="$(pwd)"
export PROJECT_ROOT

color_R=$(tput setaf 1); color_G=$(tput setaf 2); color_Y=$(tput setaf 208); color_N=$(tput sgr0)
color_C=$(tput setaf 6)

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

echo
echo "${color_C}----------------------- FIRST USE 🌕 -----------------------${color_N}"
echo

if [[ $OSTYPE == "linux"* ]]; then
    specs_system="Linux"
    [[ $(uname -m) == "a"* && $(getconf LONG_BIT) == 64 ]] && specs_architecture="arm64" || specs_architecture="x86_64"
elif [[ $OSTYPE == "darwin"* ]]; then
    specs_system="MacOS"
    specs_architecture="$(uname -m)"
fi

if ! command -v python3 &> /dev/null; then
    warn "Python3 is required to run this application and was not found."
fi

if ! command -v perl &> /dev/null; then
    warn "perl is not REQUIRED but is RECOMMENDED for more precise filter features"
fi

log "Chmoding main shell scripts.."
chmod +x "$PROJECT_ROOT/runmefirst.sh"
chmod +x "$PROJECT_ROOT/recover.sh"

if [[ -d "$PROJECT_ROOT/bin" ]]; then
    for bins in "$PROJECT_ROOT/bin/*"; do
        for bin in "$bins/*"; do
            [[ ! -f "$bin" ]] && continue
            log "Fixing binary $bin"
            chmod +x "$bin"
            [[ "$specs_system" == "MacOS" ]] && xattr -d com.apple.quarantine "$bin"
        done
    done
fi

echo
echo "${color_C}All done!* ☀️${color_N}"
print "if something didnt go as expected, read the github"
echo