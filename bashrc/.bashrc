# <<< CUDA ENV
export CUDA_HOME=/usr/local/cuda
export LD_LIBRARY_PATH=/usr/local/cuda/lib64
export PATH=$PATH:$CUDA_HOME/bin
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/usr/local/lib

# close all emulator
export PATH=$PATH:/home/keroro/Android/Sdk/emulator:/home/keroro/Android/Sdk/platform-tools
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

# <<< flutter
export PATH=$PATH:/home/keroro/Program_Files/flutter/bin
export ANDROID_SDK_ROOT=/home/keroro/Android/Sdk
export CHROME_EXECUTABLE=/opt/microsoft/msedge-beta/microsoft-edge-beta

# <<< CPU and memory check in process
function procpu(){
    function sysmem(){
    #ref. https://linuxhint.com/check_memory_usage_process_linux/
    # https://www.networkworld.com/article/3516319/showing-memory-usage-in-linux-by-process-and-user.html
        RAWIN=$(ps -o pid,%cpu,%mem,command ax | grep -v PID | awk '/[0-9]*/{print $1 ":" $2 ":" $3 ":" $4}') 

        for i in $RAWIN
        do
            PID=$(echo $i | cut -d: -f1)
            CPU=$(echo $i | cut -d: -f2)
            MEM=$(echo $i | cut -d: -f3)
            MEMORY=$(pmap $PID | tail -n 1 | awk '/[0-9]/{print $2}')
            COMMAND=$(echo $i | cut -d: -f4)

            printf "%-10s%-8s%-15s%s\n" "$PID" "$CPU" "$MEM/$MEMORY" "$COMMAND"
        done
    }
    printf "%-10s%-8s%-15s%s\n" "PID" "%CPU" "%MEM/MEM" "COMMAND"
    sysmem | sort -bnr -k2 | head -5
}
