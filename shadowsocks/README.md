
# Shadowsocks Setup AWS

[github wiki](https://github.com/shadowsocks/shadowsocks/wiki)

# 取消`pem`登入ssh
1. 切换到root用户：sudo -i
2. 编辑配置文件：vim /etc/ssh/sshd_config
3. 修改参数：PermitRootLogin yes
4. 修改参数：PasswordAuthentication yes
5. 修改密码：passwd
6. 重启ssh服务：systemctl restart ssh

使用gcp的VM要注意安装的操作系统，Ubuntu不能用密码登入ssh，要安装Debian系统才可以密码登入ssh。还有gcp的防火墙记得要新增规则，细节操作参考[gcp最轻量设定](#gcp)。

# Connect Instance with SSH
```shell
chmod 400 <download_key_file>
ssh -i "test2.pem" ubuntu@ec2-3-39-224-5.ap-northeast-2.compute.amazonaws.com
ssh -i "aws_key.pem" ubuntu@ec2-13-125-5-7.ap-northeast-2.compute.amazonaws.com
```
* ##### 中断卡住的SSH会话在服务器里
```sh
who #查看谁在会话
# 删除所有人
sudo pkill -KILL -u $(who | awk '{print $1}' | sort | uniq)
#sudo pkill -9 -t pts/*
# 删除谁
sudo pkill -9 -t pts/<id>
```
# Remember set available port range
ref. https://www.vpndada.com/how-to-setup-shadowsocks-server-on-amazon-ec2/

[Generate ssh key](#ssh-keygen)\
[Firewall](#firewall)

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

* ##### Check listening ports are availiable in server
In client terminal:
```shell
nc -zw 1 <server_ip> <used_port>
#nc -z -w 5 35.206.218.39 55123 #tw-gcp
```
https://stackoverflow.com/questions/52509512/how-can-i-verify-that-the-shadowsocks-server-is-ready

# Client
```shell
sudo apt-get update -qq && sudo apt-get install -y shadowsocks-libev
#nohup ss-local -c $YOUR_CONFIG >/dev/null &
nohup ss-local -c seoul22.json > /dev/null &
# For macos
brew install shadowsocks-libev v2ray-plugin simple-obfs
# ss-local -c seoul22.json --plugin v2ray-plugin
# ss-local -c taiwan-one.json --plugin obfs-local
nohup ss-local -c myHome.json --plugin obfs-local > /dev/null &
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
<span id="gcp"></span>
# GCP最轻量设定
* #### 新增防火墙规则
进入gcp网页，从侧边栏进入
<kbd>VPC network</kbd>&#8594;<kbd>Firewall</kbd>&#8594;<kbd>CREATE FIREWALL RULE</kbd>\
新增好了一个规则的`tag`后，就可以在VM的<kbd>Edit</kbd>里面`Network tags`项目输入你定义的规则的`tag`名称。\
https://www.geeksforgeeks.org/how-to-open-port-in-gcp-vm/

* #### 最轻量便宜的方案
1. 在安装操作系统的disk，记得选择standard磁碟硬盘。
2. 在VM的`Network`项目，要展开`Network interfaces`列表内的`default`，里面有一个项目`Network Service Tier`要选择`Standard`，才会是最便宜的方案。

<span id="ssh-keygen"></span>
* #### 生成`ssh-key`
想要产生登入服务器，某个用户登入的key，可以用`ssh-keygen`指令；如果省略<user_name>则会用本地电脑的用户名：
```shell
ssh-keygen -t rsa -f ~/.ssh/<key_filename> -C <user_name>
#ssh-keygen -t rsa -f ~/.ssh/gcp_rsa -C cia1099
```
生成好公钥的`~/.ssh/<key_filename>.pub`贴上到VM的编辑页里的`Security and access`中`SSH Keys`点<kbd>ADD ITEM</kbd>:
```shell
# 直接复制这个内容全部到gcp的ssh key
cat ~/.ssh/<key_filename>.pub
# 连线通过本地私钥
ssh -i ~/.ssh/<key_filename> <user_name>@<ip_address>
```
参考[方法2：ssh -i](https://ithelp.ithome.com.tw/articles/10251134)

## Create and use ssh key
#### 1. Generate PEM key
```sh
ssh-keygen -t rsa -b 2048 -m PEM -f ~/.ssh/my_pem_key -C "Custom comment"
# Do not format
ssh-keygen -t rsa -b 4096 -f ~/.ssh/my_key -C "<user>@<machine_name>"
```
* `-t rsa`: Specifies the type of key to create, which is RSA.
* `-b 2048`: Specifies the number of bits in the key. 2048 is a common and secure key size.
* `-m PEM`: Ensures the key is in PEM format.
* `-f ~/.ssh/my_pem_key`: Specifies the file in which to save the private key (my_pem_key). You can choose a different file name or location if desired.

**Set a passphrase** (optional). After running the command, you'll be prompted to enter a passphrase. This is optional but recommended for additional security.

This command will generate two files:
* `~/.ssh/my_pem_key`: Your private key (keep this secure and do not share it).
* `~/.ssh/my_pem_key.pub`: Your public key (you will share this with the remote server).

#### 2. Copy the Public Key to the Remote Server
To use the newly generated PEM key for SSH access, you need to copy the public key to the `~/.ssh/authorized_keys` file on the remote server.\
Copy the public key to the remote server using the ssh-copy-id command:
```sh
ssh-copy-id -i ~/.ssh/my_pem_key.pub <user>@<remote-server-ip>
```
If `ssh-copy-id` is not available, manually copy the public key:
```sh
scp ~/.ssh/my_pem_key.pub <user>@<remote-server-ip>:~/.ssh/authorized_keys
```
##### (Optional) Setting remote `sshd_conf` to enable multiple public keys
```sh
PubkeyAuthentication yes
AuthorizedKeysFile .ssh/my_pem_key.pub .ssh/authorized_keys
# then
sudo systemctl restart ssh
```
Create `~/.ssh/config` to make VScode can remote server
```sh
Host <server name (custom name)>
  User <user>
  HostName <remote-server-ip>
  IdentityFile ~/.ssh/my_pem_key
Host *
  ForwardX11 yes
  ForwardX11Trusted yes
```

#### 3. Connect to the Remote Server Using the Private Key
```sh
# Ensure your private key has the correct permissions
chmod 600 ~/.ssh/my_pem_key
ssh -i ~/.ssh/my_pem_key <user>@<remote-server-ip>
```

---
<span id="firewall"></span>
# Firewall
如果你没有开放端口的话，需要防火墙将端口放开出来。
```sh
sudo ufw allow 22/tcp comment 'SSH port'
sudo ufw allow from any to any port 8325 proto tcp comment 'Shadowsocks server'
sudo ufw allow from any to any port 8325 proto udp comment 'Shadowsocks server'
```
[ufw 相关指令](https://www.cyberciti.biz/faq/howto-adding-comments-to-ufw-firewall-rule/)

ref. https://teddysun.com/342.html

ref. https://www.youtube.com/watch?v=y3FL_GI28mY&t=2s
# start server
```shell
shadowsocks-rust.ssserver -s "[::]:55123" -m "aes-256-gcm" -k "hello" -v
```
# 後臺運行
```shell
nohup shadowsocks-rust.ssserver -s "[::]:55123" -m "aes-256-gcm" -k "hello" -v > /dev/null &

shadowsocks-rust.ssserver -p 55123 -m aes-256-cfb -k test123 -d start 
```

# kill server
```shell
killall ssserver
```
ref. https://linuxconfig.org/how-to-use-curl-to-get-public-ip-address
