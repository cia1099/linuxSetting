#!/bin/bash
set -e;
cd ~/linuxSetting/shadowsocks/monitor
source venv/bin/activate
python3 main.py -i enp1s0 -t 60
# nohup python3 main.py -i enp1s0 -t 60 > console.log 2>&1 &