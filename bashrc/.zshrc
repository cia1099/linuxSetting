alias text="open -a TextEdit"
alias ll="ls -alFh"
alias simulator="open -a Simulator --args -CurrentDeviceUDID"
alias ldd="otool -L"
# <<< switch Rosetta
alias x86_64="env /usr/bin/arch -x86_64 /bin/zsh --login"
alias arm64="env /usr/bin/arch -arm64 /bin/zsh --login"
# <<< socks5 and proxy
alias socks5="networksetup -setsocksfirewallproxystate wi-fi"
alias proxy="export http_proxy=socks5://127.0.0.1:1080;export https_proxy=socks5://127.0.0.1:1080;export all_proxy=socks5://127.0.0.1:1080;export no_proxy=socks5://127.0.0.1:1080"
alias unproxy="unset http_proxy;unset https_proxy;unset all_proxy;unset no_proxy"
# <<< fvm used the nearest configuration in flutter project
alias ff="fvm flutter"
alias fd="fvm dart"

# You may need to manually set your language environment
# when your system languange is not English
# export LANG=en_US.UTF-8

# <<< vscode
export PATH=$PATH:/Applications/Visual\ Studio\ Code.app/Contents/Resources/app/bin
# <<< cmake
export PATH=$PATH:/Applications/CMake.app/Contents/bin
# <<< flutter
export PATH=$PATH:/Users/otto/fvm/versions/stable/bin
export CHROME_EXECUTABLE=/Applications/Microsoft\ Edge.app/Contents/MacOS/Microsoft\ Edge
# export PUB_HOSTED_URL=https://pub.flutter-io.cn
# export FLUTTER_STORAGE_BASE_URL=https://storage.flutter-io.cn
## <<< fvm 
export PATH=$PATH:/Users/otto/.fvm_flutter/bin
## Completion scripts setup. Remove the following line to uninstall
[[ -f /Users/otto/.dart-cli-completion/zsh-config.zsh ]] && . /Users/otto/.dart-cli-completion/zsh-config.zsh || true
# <<< dart dev bin
# export PATH=$PATH:$HOME/.pub-cache/bin
# <<< kdiff3
export PATH=$PATH:/usr/local/sbin

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
parse_git_branch() {
 git branch 2> /dev/null | sed -e '/^[^*]/d' -e 's/* \(.*\)/(\1)/'
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


export NVM_DIR="$HOME/.nvm"
[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"  # This loads nvm
[ -s "$NVM_DIR/bash_completion" ] && \. "$NVM_DIR/bash_completion"  # This loads nvm bash_completion

# Add RVM to PATH for scripting. Make sure this is the last PATH variable change.
export PATH="$PATH:$HOME/.rvm/bin"

# <<< Rosetta mode; default PS1="%n@%m %1~ %#"
if [ "i386" = $(arch) ]; then
    export PS1="%B%F{green}%n@%m%f%b:%F{4}%1~%f%# "
    eval "$(/usr/local/bin/brew shellenv)"
    export PATH=$PATH:/usr/local/bin
else
    export PS1='%B%F{195}%n@%m%f%b:%F{103}%1~%f%# '
    eval "$(/opt/homebrew/bin/brew shellenv)"
    # remove certain path in PATH
    local NEWPATH=$( echo ${PATH} | tr -s ":" "\n" | grep -vwE "/usr/local/bin" | tr -s "\n" ":" | sed "s/:$//" )
    export PATH=$NEWPATH
fi

# <<< Optional environmental variable
# --- You can set one of the optional three formats:
# "mm/dd/yyyy"|"dd.mm.yyyy"|"yyyy-mm-dd"
# or set a custom format using the strftime function format specifications,
# see 'man strftime' for details. ---
# HIST_STAMPS="mm/dd/yyyy"

# Uncomment the following line to enable command auto-correction.
# ENABLE_CORRECTION="true"
