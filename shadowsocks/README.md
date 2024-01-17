
# Shadowsocks Setup AWS

[github wiki](https://github.com/shadowsocks/shadowsocks/wiki)

# 取消`pem`登入ssh
1. 切换到root用户：sudo -i
2. 编辑配置文件：vim /etc/ssh/sshd_config
3. 修改参数：PermitRootLogin yes
4. 修改参数：PasswordAuthentication yes
5. 修改密码：passwd
6. 重启ssh服务：systemctl restart ssh
* In client input:
```shell
ssh root@35.201.209.161 #taiwan-one
ssh root@35.196.78.109 #usa-free
```

# Connect Instance with SSH
```shell
chmod 400 <download_key_file>
ssh -i "test2.pem" ubuntu@ec2-3-39-224-5.ap-northeast-2.compute.amazonaws.com
ssh -i "aws_key.pem" ubuntu@ec2-13-125-5-7.ap-northeast-2.compute.amazonaws.com
```
# Remember set available port range
ref. https://www.vpndada.com/how-to-setup-shadowsocks-server-on-amazon-ec2/
# Using C to deploy
```shell
# for 22
sudo apt-get update -qq && sudo apt-get install -y shadowsocks-libev shadowsocks-v2ray-plugin
# for below 22
sudo apt-get update -qq && sudo apt-get install -y shadowsocks-libev simple-obfs
```
ref. https://www.tititing.life/2020/10/11/ubuntu-20-04-shadowsocks-%E7%BF%BB%E7%89%86%E8%A8%98%E9%8C%84/
```shell
wget --no-check-certificate https://raw.githubusercontent.com/M3chD09/shadowsocks-with-v2ray-plugin-install/master/ubuntu-ss-install.sh
chmod +x ubuntu-ss-install.sh

```

* 可以在`config.json`的`server`屬性直接用`0.0.0.0`接受所有IP數據。
```shell
systemctl status shadowsocks-libev.service
systemctl restart shadowsocks-libev.service
journalctl -u shadowsocks-libev -f
```
* 檢查防火牆
```shell
ufw status
ufw allow <port>
apt-get install ufw
ufw enable
```
Port 22 是ssh用的，一定要开通，再来就是80,443是给服务端用的，剩下就开通shadowsocks对外的Port即可。 

# 僞裝Http數據流，隱藏SS發送
* ## [v2ray](https://github.com/shadowsocks/v2ray-plugin)
```shell
sudo apt-get install shadowsocks-v2ray-plugin
```
在`/etc/shadowsocks-libev/config.json`加入
```json
{
    "plugin": "ss-v2ray-plugin",
    "plugin_opts": "server;tls;host=mydomain.me"
}
```
* ## [simple-obfs](https://github.com/shadowsocks/simple-obfs)
检查`v2ray`和`obfs`在哪里？
```shell
which ss-v2ray-plugin
#--> /usr/bin/ss-v2ray-plugin
ls /usr/bin/ |grep obfs
#--> obfs-local
#--> obfs-server
```
```json
{
    "plugin": "obfs-server",
    "plugin_opts": "obfs=http;obfs-host=www.baidu.com"
}
```

# Config example
`/etc/shadowsocks-libev/config.json`
```json
//v2ray
{
    "server":["::0","0.0.0.0"],
    "mode":"tcp_and_udp",
    "server_port":8325,
    "local_port":1080,
    "password":"sonic747",
    "timeout":300,
    "method":"rc4-md5",
    "fast_open":true,
    "plugin": "ss-v2ray-plugin",
    "plugin_opts": "server;loglevel=info"
}
//obfs
{
    "server":["::0", "0.0.0.0"],
    "mode":"tcp_and_udp",
    "server_port":54321,
    "local_port":1080,
    "password":"smoke755",
    "timeout":400,
    "fast_open":true,
    "plugin":"obfs-server",
    "plugin_opts":"obfs=http;obfs-host=www.baidu.com",
    "method":"chacha20-ietf-poly1305"
}
```

* check
```shell
/etc/init.d/shadowsocks status
/etc/init.d/shadowsocks restart
/etc/init.d/shadowsocks stop
/etc/init.d/shadowsocks start
```

# Client
```shell
sudo apt-get update -qq && sudo apt-get install -y shadowsocks-libev
#nohup ss-local -c $YOUR_CONFIG & >/dev/null
nohup ss-local -c seoul22.json & >/dev/null
# for macos
brew install shadowsocks-libev v2ray-plugin simple-obfs
ss-local -c seoul22.json --plugin v2ray-plugin
ss-local -c taiwan-one.json --plugin obfs-local
```
[Firefox](https://supporthost.in/how-to-install-shadowsocks-on-ubuntu/)
ref. https://github.com/didibaba/shadowsocks-client-on-Ubuntu

* Terminal proxy
```shell
sudo apt-get install proxychains
sudo vi /etc/proxychains.conf
# Remove default ProxyList content Add "socks5 127.0.0.1 1080" to ProxyList
proxychains curl icanhazip.com
```
ref. https://shadowsockshelp.github.io/Shadowsocks/linux.html

macos ref. https://medium.com/@xiaoqinglin2018/mac-osx-%E4%BD%BF%E7%94%A8proxychains-ng-91ba61472fdf

https://apple.stackexchange.com/questions/226544/how-to-set-proxy-on-os-x-terminal-permanently

__MacOS 直接用`export`来设定terminal的proxy__\
不需要proxychains这个垃圾。
```shell
export all_proxy=socks5://127.0.0.1:1080
curl cip.cc
```

#### MacOS quickly turn on/off socks
```shell
# setup socks5
networksetup -setsocksfirewallproxy wi-fi localhost 1080
# turn on/off
networksetup -setsocksfirewallproxystate wi-fi on
networksetup -setsocksfirewallproxystate wi-fi off
```

# To get external IP address
```shell
curl icanhazip.com
curl -4 icanhazip.com
curl -6 icanhazip.com
```

* seoul.json
```json
{
    "server":"3.38.135.93",
    "server_port":8325,
    "local_address":"127.0.0.1",
    "local_port":1080,
    "password":"sonic747",
    "timeout":400,
    "method":"rc4-md5",
    "fast_open":false,
    "plugin":"ss-v2ray-plugin"
}
```
* taiwan-one.json
```json
{
    "server": "35.201.209.161",
    "server_port": 54321,
    "local_address": "127.0.0.1",
    "local_port": 1080,
    "password": "smoke755",
    "timeout": 400,
    "method": "chacha20-ietf-poly1305",
    "fast_open": true,
    "plugin": "obfs-local",
    "plugin_opts": "obfs=http;obfs-host=www.baidu.com"
}
```


---
#Useless

# Firewall
sudo vi /etc/ssh/sshd_config
# 查找PasswordAuthentication no，把no改为yes
sudo systemctl restart ssh.service

* look config 
cat /etc/shadowsocks.json
* 如果你没有开放端口的话，需要防火墙将端口放开出来。
sudo ufw allow 57878

ref. https://teddysun.com/342.html


ref. https://www.youtube.com/watch?v=y3FL_GI28mY&t=2s
# start server
shadowsocks-rust.ssserver -s "[::]:55123" -m "aes-256-gcm" -k "hello" -v

# 後臺運行
nohup shadowsocks-rust.ssserver -s "[::]:55123" -m "aes-256-gcm" -k "hello" -v & >/dev/null

shadowsocks-rust.ssserver -p 55123 -m aes-256-cfb -k test123 -d start 


# kill server
killall ssserver

ref. https://linuxconfig.org/how-to-use-curl-to-get-public-ip-address