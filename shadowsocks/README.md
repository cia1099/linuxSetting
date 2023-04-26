
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
ssh root@3.38.135.93
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
# don't use script to install, that will conflict native shadowsocks-libev
#wget --no-check-certificate -O shadowsocks-libev-debian.sh https://raw.githubusercontent.com/teddysun/shadowsocks_install/master/shadowsocks-libev-debian.sh
# chmod +x shadowsocks-libev-debian.sh
# sudo ./shadowsocks-libev-debian.sh 2>&1 | tee shadowsocks-libev-debian.log
# uninstall
# ./shadowsocks-libev.sh uninstall
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
```

# 僞裝Http數據流，隱藏SS發送
[v2ray](https://github.com/shadowsocks/v2ray-plugin)
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

# Config example
`/etc/shadowsocks-libev/config.json`
```json
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
brew install shadowsocks-libev v2ray-plugin
ss-local -c seoul22.json --plugin v2ray-plugin
```
[Firefox](https://supporthost.in/how-to-install-shadowsocks-on-ubuntu/)
ref. https://github.com/didibaba/shadowsocks-client-on-Ubuntu

* Terminal proxy
```shell
sudo apt-get install proxychains
sudo vi /etc/proxychains.conf
# Remove default ProxyList content Add "socks5 127.0.0.1 1080" to ProxyList
proxychains curl icanhazip.com

# for macos
brew install proxychains-ng
code /opt/homebrew/etc/proxychains.conf
proxychains4 curl icanhazip.com
```
ref. https://shadowsockshelp.github.io/Shadowsocks/linux.html

macos ref. https://medium.com/@xiaoqinglin2018/mac-osx-%E4%BD%BF%E7%94%A8proxychains-ng-91ba61472fdf

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