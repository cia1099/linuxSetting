#!/bin/bash
set -ex;
cd ~/linuxSetting/shadowsocks/monitor;
source venv/bin/activate;
nohup python3 main.py -i enp1s0 -t 60 > /dev/null 2>&1 &;
