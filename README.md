# linuxSetting

Linux
----
 * 安裝環境
```shell
sudo apt-get install build-essential #install make
sudo apt-get install g++
//----安裝新酷音
sudo apt-get install ibus-chewing

//-----安裝VSCode
//先去官網下載.deb檔案
sudo dpkg -i [code file name].deb

//------安裝小畫家
sudo apt-get install kolourpaint //記得別裝到kolourpaint4，是舊版
```
[Ubuntu install Chewing](https://medium.com/@racktar7743/ubuntu-%E5%9C%A8-ubuntu-18-04-%E4%B8%AD%E6%96%B0%E5%A2%9E%E6%96%B0%E9%85%B7%E9%9F%B3%E8%BC%B8%E5%85%A5%E6%B3%95-4aa85782f656)
* 檢查安裝包

#### 1.  apt
```shell
apt-cache search all | grep xx
apt-cache search all
apt-cache search xx
```
#### 2. dpkg
```shell
dpkg -l #完整
dpkg -l 軟件名
whereis 軟件名
dpkg -l | grep ftp
dpkg --get-selections | grep 軟件名 #顯示軟件已安裝
```
* 刪除安裝包
 ```
 sudo apt-get --purge remove [安裝包名] #刪除單一包
 sudo apt autoremove [安裝包名] #刪除安裝包與相依包
 ```

#### 3. 支援網頁播放視頻
If those streaming services use DRM, you must enable DRM in Firefox's settings: Preferences -> General -> Play DRM-controlled content You might also have to install package libavcodec-extra to get the codecs:
```
sudo apt install libavcodec-extra
```
[Playing Videos in Firefox](https://askubuntu.com/questions/1035661/playing-videos-in-firefox)

* 安裝CMake
```shell
wget https://cmake.org/files/v3.15/cmake-3.15.6.tar.gz 
tar xzvf cmake-3.15.6.tar.gz
sudo apt-get install libncurses5-dev #in order to install ccmake 
cd cmake-3.15.6
cmake -D BUILD_CursesDialog=ON
./bootstrap --qt-gui
make -j8
make install
```

* 圖形介面
##### 注意要先安裝Xming或VCXrc
```shell
sudo apt install xfce4 xfce4-terminal  #注意命令里是xfce不是xface
echo "export DISPLAY=:0" >> ~/.bashrc
source ~/.bashrc
echo $DISPLAY  # 检验一下
startxfce4  # 启动
```

* Qt安裝[1]
首先去官網 http://download.qt.io/archive/qt/ 下載安裝包，等待安裝完成
#### 路徑配置
```
sudo vim /usr/lib/x86_64-linux-gnu/qt-default/qtchooser/default.conf
```
将第一行改为自己安装路径下的bin目录的路径，第二行改为Qt5.12.3目录的路径
```
/opt/Qt5.11.3/5.11.3/gcc_64/bin
/opt/Qt5.11.3
```
[1] https://blog.csdn.net/anyuliuxing/article/details/90369822

##### optional
```
sudo apt-get install qtchooser
```
在(/usr/lib/x86_64-linux-gnu/下一個qtchooser)
```
sudo vim /usr/lib/x86_64-linux-gnu/qtchooser/default.conf
```
把路径换为安装过的路径
```shell
/opt/Qt5.11.3/5.11.3/gcc_64/bin
/opt/Qt5.11.3
```

* VTK安裝
直接使用apt-get安裝：
'sudo apt-get install libvtk7-dev'
要注意dash（-）後有dev的才有包含header可以做編譯，最好都安裝帶有-dev的安裝包。
在安裝VTK包時，會遇到相依性衝突，這大部分是libboost安裝包版本衝突造成，先刪除舊版libboost安裝包，
直接安裝VTK會自動安裝相應的相依libboost版本包，之後再依對應的版本安裝完整的libboost包即可。
```shell
sudo apt-get install libglu1-mesa-dev freeglut3-dev mesa-common-dev #安裝OpenGL
sudo apt-get install doxygen #文檔生成庫

cmake -DCMAKE_INSTALL_PREFIX=/usr/local \
      -DCMAKE_BUILD_TYPE=Release \
      -DVTK_QT_VERSION:STRING=5 \
      -DQT_QMAKE_EXECUTABLE:PATH=/opt/Qt5.11.3/5.11.3/gcc_64/bin/qmake \
      -DVTK_GROUP_ENABLE_Qt:STRING=YES \
      -DCMAKE_PREFIX_PATH:PATH=/opt/Qt5.11.3/5.11.3/gcc_64/lib/cmake  \
      -DBUILD_SHARED_LIBS:BOOL=ON \
      -DVTK_FORBID_DOWNLOADS:BOOL=ON \
      -DVTK_BUILD_DOCUMENTATION:BOOL=ON \
      -DVTK_PYTHON_VERSION-STRINGS=3 \
      ..
```

* PCL安裝
```shell
sudo apt-get install  libboost-all-dev libeigen3-dev libflann-dev libusb-1.0-0-dev

cmake -DCMAKE_INSTALL_PREFIX=/usr/local \
-DCMAKE_BUILD_TYPE=Release \
-DCMAKE_PREFIX_PATH:PATH=/opt/Qt5.11.3/5.11.3/gcc_64/lib/cmake  \
-DQt5_DIR:PATH=/opt/Qt5.11.3/5.11.3/gcc_64 \
-DBUILD_SHARED_LIBS:BOOL=ON \
-DBUILD_examples:BOOL=ON \
-DQT5_QMAKE_EXECUTABLE:PATH=/opt/Qt5.11.3/5.11.3/gcc_64/bin/qmake \
..
```

* WSL文件位置
如果想在 Linux 查看其他分区，WSL 将其它盘符挂载在 /mnt 下。
如果想在 Windows 下查看 WSL 文件位置，文件位置在：C:\Users\用户名\AppData\Local\Packages\CanonicalGroupLimited.Ubuntu18.04onWindows_79rhkp1fndgsc\LocalState\rootfs 下。

* 系統環境變量(待續)
```shell
### 查看環境變量
env | grep PATH
echo $PATH
```

#### * Kdiff3安裝
先去官網下載Kdiff3的tar.gz檔案，準備編譯環境，這裡是<span style="background-color:yellow">只裝Qt版的</span>
```shell
sudo apt-get install gettext qtbase5-dev qt5-qmake
tar zxvf kdiff.tar.gz
./config qt4 #就算沒裝qt4，只裝了qt5，也是建置qt5的版本
# 安裝語言包
cd .../kdiff3-0.9.98/po
sh create_qm_files install
sh create_qm_files local #上面失敗就再加這句

#編輯 .gitconfig
code /home/cia1099/.gitconfig
### 編輯範例：
[difftool "kdiff3"]
	cmd = '/home/cia1099/Downloads/kdiff3-0.9.98/releaseQt/kdiff3' \"$LOCAL\" \"$REMOTE\"
[mergetool "kdiff3"]
	cmd = '/home/cia1099/Downloads/kdiff3-0.9.98/releaseQt/kdiff3' \"$BASE\" \"$LOCAL\" \"$REMOTE\" -o \"$MERGED\"
```

#### 安裝GPU
[reference](https://gitpress.io/@chchang/install-nvidia-driver-cuda-pgstrom-in-ubuntu-1804)
[Official](https://gist.github.com/wangruohui/df039f0dc434d6486f5d4d098aa52d07)
```shell
sudo add-apt-repository ppa:graphics-drivers/ppa
sudo apt update
sudo apt install ubuntu-drivers-common

ubuntu-drivers devices #看現在的驅動程式狀態
sudo apt install nvidia-driver-440 
sudo reboot
lsmod|grep nvidia #查看基本資訊，無顯示表示沒有成功載入驅動
nvidia-smi #查看GPU資訊
nvidia-modprobe #將驅動手動啟動載入至系統
```
<font color=ff00>如果找不到驅動，要將BIOS的Secure Boot設為Disable</font>
* 安裝CUDA
同樣採用官網下載deb 回來安裝的方法
到這邊 https://developer.nvidia.com/cuda-downloads 
選擇 Linux -- x86_64 -- Ubuntu -- 18.04 -- deb(local)
畫面上就會有安裝步驟，照著做就沒問題了
一樣，安裝完成後重新開機，然後來編譯一個 deviceQuery 的小程式來看看資訊
```shell
cd /usr/local/cuda-10.2/samples/1_Utilities/deviceQuery
sudo make
```
會產生一個叫 deviceQuery 的執行檔，執行後，會有相關資訊
* 安裝cuDNN
The recommended way for installing cuDNN is to first copy the `tgz` file to `/usr/local` and then extract it, and then remove the `tgz` file if necessary. This method will preserve symbolic links. At last, execute `sudo ldconfig` to update the shared library cache.

* 讓vcpkg支援CUDA
https://github.com/microsoft/vcpkg/issues/8247
```shell
cd vcpkg
export CUDA_PATH=/usr/local/cuda;
export CUDA_BIN_PATH=/usr/local/cuda/bin;
./vcpkg install cuda
```
### 基本操作，參考實驗樓《Linux基礎入門》
#### 文件查找
有時候剛添加的文件，有可能會找不到，需要手動執行一次`updatedb`命令。
* whereis簡單快速
whereis只能搜索二進制文件(-b)、man幫助文檔(-m)和源代碼文件(-s)。
* which小而精
我們通常使用which來確定是否安裝了某個指定的程序，因為它只能從<font color=ff00ff>PATH</font>環境變量指定的路徑中去搜索命令並且返回第一個搜索到的結果。
* find精而細
注意find命令的路徑是作為第一個參數，基本命令格式為 find [path][option][action]
```shell
find /etc -name \*.list
#查找在/etc底下所有.list有關聯的檔名
```
#### 簡單輸出
```shell
cat -n filename #輸出filename的內容於terminal，其中-n包含行號
nl -b a filename #與'cat -n'相同
tail -f filename 
＃可以實時顯示filename內容的最後10行(默認10行，可以用'-n [INT]'來設定顯示的INT行)
```
#### 文件權限
一個目錄同時具有讀權限和執行權限才可以打開並查看內部文件，而一個目錄要有寫權限才允許在其中創建其它文件
```shell
chmod 765 filename #將filename的權限修改成：擁有者(rwx)、所屬用戶(rw-)、其他用戶(r-x)
chown [所有者] [filename] #將filename的所有者修改為[所有者]，可以用ll命令查看
```