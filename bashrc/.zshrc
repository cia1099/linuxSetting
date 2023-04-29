
alias text="open -a TextEdit"
alias ll="ls -alF"
alias simulator="open -a Simulator --args -CurrentDeviceUDID"
alias ldd="otool -L"

# <<< brew
eval "$(/opt/homebrew/bin/brew shellenv)"
# <<< vscode
export PATH="$PATH:/usr/local/bin"
# <<< cmake
export PATH=$PATH:/Applications/CMake.app/Contents/bin
# <<< flutter
export PATH=$PATH:/Users/otto/Downloads/flutter/bin
export CHROME_EXECUTABLE=/Applications/Microsoft\ Edge.app/Contents/MacOS/Microsoft\ Edge

# close all emulator
export PATH=$PATH:/Users/otto/Library/Android/sdk/emulator:/Users/otto/Library/Android/sdk/platform-tools
close (){
    if [ -z "$1" ]; then
        echo "Perhaps you want to 'close emulator'?"
    else
        if [ "$1" = "emulator" ]; then
        adb devices | grep emulator | cut -f1 | while read line; do adb -s $line emu kill; done;
        else
        echo "ERROR: strange time detected: $1"
        fi
    fi
}


# >>> conda initialize >>>
# !! Contents within this block are managed by 'conda init' !!
__conda_setup="$('/Users/otto/miniconda3/bin/conda' 'shell.zsh' 'hook' 2> /dev/null)"
if [ $? -eq 0 ]; then
    eval "$__conda_setup"
else
    if [ -f "/Users/otto/miniconda3/etc/profile.d/conda.sh" ]; then
        . "/Users/otto/miniconda3/etc/profile.d/conda.sh"
    else
        export PATH="/Users/otto/miniconda3/bin:$PATH"
    fi
fi
unset __conda_setup
# <<< conda initialize <<<

