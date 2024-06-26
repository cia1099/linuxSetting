# Set up shadowsocks server in home

This project is used to keep continuously modified LAN address which was distributed by switcher randomly. For example, when shutdown, reboot or power abruptly stop, the address will be resetting.\
So we have to take an automatic calibration program to supervise what LAN is it in present. Moreover we need to tell switcher to revise the forwarding address.

## Web App
网页能够在手机主屏幕上显示自定义图标，是通过一种叫做“Web App Manifest”的文件来实现的。这种文件允许网站开发者为网页应用提供元数据，包括名称、图标、启动 URL 和其他信息，从而使网页应用在添加到主屏幕时表现得像一个原生应用。

1. 创建 [Web App Manifest](https://github.com/cia1099/linuxSetting/blob/master/shadowsocks/monitor/manifest.json) 文件。\
注意在`manifest.json`文件中，icons 的 src 属性可以使用网络图片的 URL。
2. 引用 Manifest 文件\
在你的 HTML 文件的\<head>部分[引用这个manifest](https://github.com/cia1099/linuxSetting/blob/master/shadowsocks/monitor/templates/record_base.html?plain=#L12)文件。
3. iPhone等设备\
因为苹果设备不完全支持 Web App Manifest 文件中的所有功能，还需要在[HTML文件](https://github.com/cia1099/linuxSetting/blob/master/shadowsocks/monitor/templates/record_base.html?plain=#L14-L18)的 \<head> 部分添加一些额外的 \<link> 标签:
* apple-touch-icon：为 iOS 主屏幕图标设置图标。
* apple-mobile-web-app-capable：启用 Web 应用程序的全屏显示。
* apple-mobile-web-app-status-bar-style：设置状态栏的样式。
* apple-mobile-web-app-title：设置添加到主屏幕后显示的应用标题。

苹果在HTML文件中的图标连接用URL，本地端似乎抓不到。



## Access Router Devices Externally
要通过外部IP地址访问连接到你的路由器的设备，你需要进行端口转发和动态DNS设置。以下是具体步骤：

1. 获取你的外部IP地址
你的外部IP地址是你在互联网上的唯一标识符。你可以通过以下方法获取：
    * 访问`curl cip.cc`或类似的网站。
    * 在路由器的管理界面中查看WAN设置。

2. 配置路由器的端口转发
端口转发允许外部请求通过特定端口访问你的内部设备。
    * 登录到你的路由器管理界面（通常是通过在浏览器地址栏中输入192.168.66.1或192.168.x.1）。
    * 找到“端口转发”或“虚拟服务器”设置。
    * 添加新的端口转发规则：
        * 外部端口：你希望用于外部访问的端口号（例如，8080）。
        * 内部IP地址：你内部设备的IP地址（例如，192.168.66.100），内部地址要查看`ifconfig`在被router连接的设备，有时候router的界面会没显示。
        * 内部端口：内部设备的服务端口（例如，80用于HTTP）。
        * 通常内部和外部用一样的端口方便。
        <img src="https://github.com/cia1099/linuxSetting/raw/master/img/forwarding.png" style="width:640px;height:300px;"/>

## Setting Hotspot shared
只使用`nmcli`来开启AP模式。NetworkManager本身就能够处理大多数的AP配置，不需要额外的`hostapd`。以下是具体步骤：
1. 步骤 1：创建新的热点连接

___建议直接使用Ubuntu GUI来建立热点，这样第一步可以跳过，除非热点的设定档名称(Hotspot)想换别的。___
```sh
sudo nmcli connection add type wifi ifname <your_wifi_interface> con-name Hotspot autoconnect no ssid <Your_SSID>
sudo nmcli c modify Hotspot ipv4.method shared 802-11-wireless.mode ap
sudo nmcli c modify Hotspot wifi-sec.key-mgmt wpa-psk wifi-sec.psk <Your_Password>
```
替换以下内容：
* <your_wifi_interface>：替换为你的无线网卡接口名称，例如wlp2s0。
* <Your_SSID>：替换为你想要的Wi-Fi名称。
* <Your_Password>：替换为你想要的Wi-Fi密码。
* `con-name`参数是连接设定档的名称，可以自定义，预设是Hotspot。
2. 步骤 2：设定连接5G模式，和自动连接
5G模式是a
```sh
sudo nmcli c modify Hotspot connection.autoconnect yes 802-11-wireless.band a 802-11-wireless.channel 149
# 查看热点相关设定参数
nmcli c show Hotspot |grep ipv4
```
使用`iw list`查看网络卡支援5G频段，看Frequencies内容；也能检查是否能开AP模式：
```sh
Frequencies:
        * 5180.0 MHz [36] (20.0 dBm) (no IR)
        * 5200.0 MHz [40] (20.0 dBm) (no IR)
        * 5220.0 MHz [44] (20.0 dBm) (no IR)
        * 5240.0 MHz [48] (20.0 dBm) (no IR)
        # ...
        * 5745.0 MHz [149] (20.0 dBm)
        * 5765.0 MHz [153] (20.0 dBm) (no IR)
        * 5785.0 MHz [157] (20.0 dBm)
        * 5805.0 MHz [161] (20.0 dBm) (no IR)
        * 5825.0 MHz [165] (20.0 dBm) (no IR)
```
后面有(no IR)的频段就是不支援，所以上述例子只能选择`802-11-wireless.channel`为149或157。
3. 步骤 3：连接热点设定档
```sh
sudo nmcli c down Hotspot #断开热点，每次调整热点后，都要断开重连
sudo nmcli c up Hotspot

nmcli d #查看连接设备
nmcli d show wlp2s0 #查看设备wlp2s0
iw dev wlp2s0 info #检查发射频段
nmcli c show #查看有哪些连接设定档
nmcli c delete <name> #删除设定档
nmcli d wifi show-password #show QRcode
```
refs.:\
https://ubuntu.com/core/docs/networkmanager/edit-connections

read://https_www.fosslinux.com/?url=https%3A%2F%2Fwww.fosslinux.com%2F127522%2Fcreate-a-wireless-access-point-on-ubuntu.htm

## Construct Domain Name
注册[Cloudns](https://www.cloudns.net)申请一个免费的网域，再用[Cloudflare](https://www.cloudflare.com)代理解析这个域名，将网域解析到想要的IP地址。\
ref. https://www.youtube.com/watch?v=0YFZRggVqtI&t=66s

## Port rewording
可以使用 iptables 进行端口转发，让 80 端口的请求转发到一个高端口，比如 8080。
```sh
sudo iptables -t nat -A PREROUTING -p tcp --dport 80 -j REDIRECT --to-port 8080
#查看现有的规则
sudo iptables -t nat -L --line-numbers
#删除特定的转发规则，假设这条规则在 PREROUTING 链的第 1 行
#sudo iptables -t nat -D PREROUTING 1
sudo iptables -t nat -L #确认规则已删除
#保存更改
sudo sh -c "iptables-save > /etc/iptables/rules.v4"
```
如果你只是输入`sudo iptables-save`，它不会自动保存到文件，而是会将规则列表打印到屏幕上。\
如果要删除，直接删除`/etc/iptables/rules.v4`这个文件即可；因为原本就没有这个文件。

---
## How to Install
```sh
git clone --sparse --depth=1 https://github.com/cia1099/linuxSetting.git
cd linuxSetting
git sparse-checkout add shadowsocks/monitor
cd shadowsocks/monitor
python3 -m venv venv
source venv/bin/activate
python -m pip install pipenv
python -m pipenv install
```
* ### Set start up program
使用systemd服务，在`/usr/lib/systemd/system/`目录下创建一个新的服务文件。\
`sudo vim /usr/lib/systemd/system/monitor.service`\
在文件中添加以下内容：
```sh
[Unit]
Description=Keep forwarding LAN address on this machine
After=network.target

[Service]
Type=simple
ExecStart=/home/yoyo/linuxSetting/shadowsocks/monitor/cmd.sh
Restart=on-failure
User=yoyo

[Install]
WantedBy=multi-user.target
```
重新加载systemd管理器配置，并启用`monitor.service`服务：
```sh
sudo systemctl daemon-reload
sudo systemctl enable monitor.service
sudo systemctl start monitor.service
# 语法检查monitor.service的内容
systemd-analyze verify /usr/lib/systemd/system/monitor.service
systemctl status monitor.service
```