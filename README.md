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
#注意要添加 * 號前面的反斜槓轉義，否則會無法找到
```
#### 簡單輸出
```shell
cat -n filename #輸出filename的內容於terminal，其中-n包含行號
nl -b a filename #與'cat -n'相同
tail -f filename 
＃可以實時顯示filename內容的最後10行(默認10行，可以用'-n [INT]'來設定顯示的INT行)
#監控crontab後台執行系統日誌
sudo tail -f /var/log/syslog
#crontab 是 Linux 系统中添加计划任务，定时执行一些必要的脚本所必不可少的工具(實驗9)
```
#### 文件權限
一個目錄同時具有讀權限和執行權限才可以打開並查看內部文件，而一個目錄要有寫權限才允許在其中創建其它文件
```shell
chmod 765 filename #將filename的權限修改成：擁有者(rwx)、所屬用戶(rw-)、其他用戶(r-x)
chown [所有者] [filename] #將filename的所有者修改為[所有者]，可以用ll命令查看
```
#### 文件打包與解壓縮
1_1. zip壓縮打包程序
```shell
zip -r -q -o shiyanlou.zip /home/shiyanlou/Desktop #[1]
du -h shiyanlou.zip #使用 du 命令查看打包後文件的大小
'''
這裡添加了一個參數用於設置壓縮級別
 -[1-9]，1 表示最快壓縮但體積大，9 表示體積最小但耗時最久。
 最後那個 -x 是為了排除我們上一次創建的 zip 文件，否則又會被打包進這一次的壓縮文件中，
 注意：這裡只能使用絕對路徑，否則不起作用。
'''
zip -r -9 -q -o shiyanlou_9.zip /home/shiyanlou/Desktop -x ~/*.zip
zip -r -1 -q -o shiyanlou_1.zip /home/shiyanlou/Desktop -x ~/*.zip
#---使用 -e 參數可以創建加密壓縮包
zip -r -e -o shiyanlou_encryption.zip /home/shiyanlou/Desktop
#加上 -l 參數將LF轉換為CR+LF符合Windows系統文本格式
zip -r -l -o shiyanlou.zip /home/shiyanlou/Desktop
```
[1]上面命令將目錄 /home/shiyanlou/Desktop 打包成一個文件，並查看了打包後文件的大小和類型。第一行命令中，-r 參數表示遞歸打包包含子目錄的全部內容，-q 參數表示為安靜模式，即不向屏幕輸出信息，-o，表示輸出文件，需在其後緊跟打包輸出文件名。

1_2. unzip
```shell
unzip shiyanlou.zip #將 shiyanlou.zip 解壓到當前目錄
'''
-q 使用安靜模式，-d 將文件解壓到指定目錄
指定目錄不存在，將會自動創建。
'''
unzip -q shiyanlou.zip -d [指定目錄]
#---如果你不想解壓只想查看壓縮包的內容你可以使用 -l 參數
unzip -l shiyanlou.zip
'''
在Windows的中文編碼預設為GBK，而Linux默認為UTF-8
未避免解壓造成亂碼，可以指定編碼類型。
使用 -O（英文字母，大寫 o）參數指定編碼類型
'''
unzip -O GBK 中文壓縮文件.zip
```
2_1. tar打包工具
```shell
tar -P -cf shiyanlou.tar /home/shiyanlou/Desktop #[1]
#---解包一個文件（-x 參數）到指定路徑的已存在目錄（-C 參數）
tar -xf shiyanlou.tar -C [指定目錄]
tar -tf shiyanlou.tar #只查看不解包文件 -t 參數
```
[1]上面命令中，-P 保留絕對路徑符，-c 表示創建一個 tar 包文件，-f 用於指定創建的文件名，注意文件名必須緊跟在 -f 參數之後，比如不能寫成 tar -fc shiyanlou.tar，可以寫成 tar -f shiyanlou.tar -c ~。你還可以加上 -v 參數以可視的的方式輸出打包的文件。

我們要使用其它的壓縮工具創建或解壓相應文件只需要更改一個參數即可：
|壓縮文件格式|參數|
|---|---|
|*.tat.gz|-z|
|*.tar.xz|-J|
|*.tar.bz2|-j|
```shell
#在創建 tar 文件的基礎上添加 -z 參數，使用 gzip 來壓縮文件
tar -czf shiyanlou.tar.gz /home/shiyanlou/Desktop
tar -xzf shiyanlou.tar.gz #解壓 *.tar.gz 文件，-x解包
```
#### 查看磁盤和目錄容量
```shell
#查看硬碟的容量
df -h #其中-h為human readable的意思
#查看文件或資料夾的容量
du -h -d 1 ~ #參數 -d 指定查看目錄的深度
#----找出当前目录下面占用最大的前十个文件
cd /path/to/some/where
du -hsx * | sort -rh | head -10
# du -hsx /path/to/some/where/* | sort -rh | head -10

ls -l /lib/modules/$(uname -r)/kernel/fs #查看Linux支持哪些文件系統
```

#### 有選擇的執行命令
```shell
which cmatrix>/dev/null && echo "exist" || echo "not exist"
echo $? #該暫存執行的結果，如果有裝cmatrix就會0，表示which指令成功
```
終端機會以執行成功與否返回0與非0，當執行成功返回0，失敗返回非0；在`&&`前面的指令返回0成功，才會執行`&&`後面的指令，但是`||`是前面返回非0失敗，則執行`||`後面的指令。上面範例就是當`which`成功執行返回0的話，就接續執行`&&`後面的`echo "exist"`，執行失敗返回非0，就只執行`||`後面的指令`echo "not exist"`。

1. 管道，直譯就是將前面每一個進程的輸出(stdout)直接作為下一個進程的輸入(stdin)。我們在使用一些過濾程序時經常會用到的就是匿名管道，在命令行中由`|`分隔符表示。
```shell
ls -al /etc | less
```
通過管道將前一個命令(ls)的輸出作為下一個命令(less)的輸入，然後就可以一行一行地看。

2. cut，打印每一行的某一字段，類似C#的split的操作
```shell
ll | cut -c 30- #截斷'll'之後30個字串的顯示
ll | cut -c -30 #只顯示'll'的前30個字串顯示
```

3. grep命令，在文本中或stdin中查找匹配字符串
```shell
ll -a | grep project #只顯示匹配project的文件
ll -a | grep ".$" #多字串符""沒啥用，其中$就表示一行的末尾
```

4. wc 命令用於統計並輸出一個文件中行、單詞和字節的數目

|命令參數|統計的東西|
|---|---|
|wc -l|行數|
|wc -w|單詞數|
|wc -c|字節數|
|wc -m|字符數|
|wc -L|最長行字節數|
```shell
#---統計 /etc 下面所有目錄數
ls -dl /etc/*/ | wc -l
```

#### 簡單的文本處理
1. tr 命令可以用來刪除一段文本信息中的某些文字。或者將其進行轉換
```shell
'''
使用方式
tr [option]...SET1 [SET2]
'''
# 刪除 "hello shiyanlou" 中所有的'o','l','h'
echo 'hello shiyanlou' | tr -d 'olh'
# 將"hello" 中的ll,去重為一個l
echo 'hello' | tr -s 'l'
# 將輸入文本，全部轉換為大寫或小寫輸出
echo 'input some text here' | tr '[:lower:]' '[:upper:]'
# 上面的'[:lower:]' '[:upper:]'你也可以簡單的寫作'[a-z]' '[A-Z]',當然反過來將大寫變小寫也是可以的
```
2. col 命令可以將Tab換成對等數量的空格鍵，或反轉這個操作

|選項|說明|
|---|---|
|-x|將Tab轉換為空格|
|-h|將空格轉換為Tab(默認選項)|
```shell
# 查看 /etc/protocols 中的不可見字符，可以看到很多 ^I ，這其實就是 Tab 轉義成可見字符的符號
cat -A /etc/protocols
# 使用 col -x 將 /etc/protocols 中的 Tab 轉換為空格,然後再使用 cat 查看，你發現 ^I 不見了
cat /etc/protocols | col -x | cat -A
```
3. join 將兩個文件中包含相同內容的那一行合併在一起
```shell
#創建兩個文件
echo '1 hello' > file1
echo '1 shiyanlou' > file2
join file1 file2
#>> 1 hello shiyanlou
#兩文件都包含'1'的這行合併在一起
```
4. paste 在不對比數據的情況下，簡單地將多個文件合併一起，以Tab隔開

|選項|說明|
|---|---|
|-d|指定合併的分隔符，默認為Tab|
|-s|不合併到一行，每個文件為一行|
```shell
'''
使用方式
paste [option] file...
'''
echo hello > file1
echo shiyanlou > file2
echo www.shiyanlou.com > file3
paste -d ',' file1 file2 file3
#>>hello,shiyanlou,www.shiyanlou.com
paste -s file1 file2 file3
#>>hello
#>>shiyanlou
#>>www.shiyanlou.com
```
5. 章節總結：
斷行符 Windows 為 CR+LF(\r\n)，Linux/UNIX 為 LF(\n)。使用cat -A 文本 可以看到文本中包含的不可見特殊字符。Linux 的\n表現出來就是一個`$`，而 Windows/dos 的表現為`^M$`，可以直接使用dos2unix和unix2dos工具在兩種格式之間進行轉換，使用file命令可以查看文件的具體類型。

#### 數據流重定向
你可能對重定向這個概念感到些許陌生，但你應該在前面的課程中多次見過>或>>操作了，並知道他們分別是將標準輸出導向一個文件或追加到一個文件中。這其實就是重定向，將原本輸出到標準輸出的數據重定向到一個文件中，因為標準輸出(/dev/stdout)本身也是一個文件，我們將命令輸出導向另一個文件自然也是沒有任何問題的。

初學者這裡要注意不要將管道和重定向混淆，**管道默認是連接前一個命令的輸出到下一個命令的輸入**，而重定向通常是需要一個文件來建立兩個命令的連接。

2.3 使用tee命令同时重定向到多个文件
你可能還有這樣的需求，除了需要將輸出重定向到文件,也需要將信息打印在終端。那麼你可以使用tee命令來實現。
```shell
echo 'hello shiyanlou' | tee hello
#不但輸出至終端，還生成一個hello
cat hello
```
2.7 完全屏蔽命令的輸出
在 Linux 中有一個被稱為「黑洞」的設備文件,所有導入它的數據都將被「吞噬」。
>在類 UNIX 系統中，/dev/null，或稱空設備，是一個特殊的設備文件，它通常被用於丟棄不需要的輸出流，或作為用於輸入流的空文件，這些操作通常由重定向完成。讀取它則會立即得到一個 EOF。

我們可以利用/dev/null屏蔽命令的輸出：
```shell
cat Documents/test.c 1>/dev/null 2>&1
#這樣的操作將使你得不到任何輸出結果
```
Linux 默認提供了三個特殊設備，用於終端的顯示和輸出，分別為stdin（標準輸入,對應於你在終端的輸入），stdout（標準輸出，對應於終端的輸出），stderr（標準錯誤輸出，對應於終端的輸出）。

|文件描述符|設備文件|說明|
|---|---|---|
|0|/dev/stdin|標準輸入|
|1|/dev/stdout|標準輸出|
|2|/dev/stderr|標準錯誤|

**注意你應該在輸出重定向文件描述符前加上&,否則 shell 會當做重定向到一個文件名為 1 的文件中。**

2.8 使用 xargs 分割參數列表
>xargs 是一條 UNIX 和類 UNIX 操作系統的常用命令。它的作用是將參數列表轉換成小塊分段傳遞給其他命令，以避免參數列表過長的問題。

這個命令在有些時候十分有用，特別是當用來處理產生大量輸出結果的命令如 find，locate 和 grep 的結果，詳細用法請參看 man 文檔。
```shell
ls -a | sort | xargs echo
#加上echo可以將原本的分行變成空格來顯示'ls -a'
```

##### [挑戰]統計文本內容
有一個命令日誌檔`data1`在`wget https://labfile.oss.aliyuncs.com/courses/1/data1`

將`data1`文本裡面找出出現頻率前3次的命令保存在`result`
>2016百度校招面試題
```shell
cat data1 |cut -c 8-|sort|uniq -dc|sort -rn -k1 |head -3 > /home/shiyanlou/result
```

#### 正則表達式(Regular Expression)
主要用在[grep](#ch5), [sed](#regex_sed), [awk](#regex_awk)。
1. grep命令用於打印輸出文本中匹配的模式串，它使用正則表達式作為模式匹配的條件。

|參數|說明|
|---|---|
-b|將二進制文件作為文本來進行匹配
-c|統計以模式匹配的數目
-i|忽略大小寫
-n|顯示匹配文本所在行的行號
-v|反選，輸出不匹配行的內容
-r|遞歸匹配查找
-A n|n 為正整數，表示 after 的意思，除了列出匹配行之外，還列出後面的 n 行
-B n|n 為正整數，表示 before 的意思，除了列出匹配行之外，還列出前面的 n 行
--color=auto|將輸出中的匹配項設置為自動顏色顯示
-E|POSIX 擴展正則表達式，ERE
-G|POSIX 基本正則表達式，BRE(預設)
-P|Perl 正則表達式，PCRE

使用基本正則表達式：
```shell
# 将匹配以'z'开头以'o'结尾的所有字符串
echo 'zero\nzo\nzoo' | grep 'z.*o'
>>zero
>>zo
>>zoo
# 将匹配以'z'开头以'o'结尾，中间包含一个任意字符的字符串
echo 'zero\nzo\nzoo' | grep 'z.o'
>>zoo
# 将匹配以'z'开头,以任意多个'o'结尾的字符串
echo 'zero\nzo\nzoo' | grep 'zo*'
>>zero
>>zo
>>zoo
```
使用擴展正則表達式，ERE
```shell
# 只匹配"zo"
echo 'zero\nzo\nzoo' | grep -E 'zo{1}'
>>zo
>>zoo
# 匹配以"zo"開頭的所有單詞
echo 'zero\nzo\nzoo' | grep -E 'zo{1,}'
>>zo
>>zoo

# 或者匹配不包含"baidu"的内容，因为.号有特殊含义，所以需要转义
echo 'www.shiyanlou.com\nwww.baidu.com\nwww.google.com' | grep -Ev 'www\.baidu\.com'
>>www.shiyanlou.com
>>www.google.com
```
**注意**：推薦掌握{n,m}即可，+,?,*，這幾個不太直觀，且容易弄混淆。
* <font color=ff00ff>+</font>表示前面的字符必須出現至少一次(1 次或多次)，例如，"goo+gle",可以匹配"gooogle","goooogle"等；==等價於{1,}==

* <font color=ff00ff>?</font>表示前面的字符最多出現一次(0 次或 1 次)，例如，"colou?r",可以匹配"color"或者"colour";==等價於{0,1}==
    
* <font color=ff00ff>\*</font>星號代表前面的字符可以不出現，也可以出現一次或者多次（0 次、或 1 次、或多次），例如，「0*42」可以匹配 42、042、0042、00042 等。==等價於{0,}==
* <font color=ff00ff>{n,m}</font>n 和 m 均為非負整數，其中 n<=m。最少匹配 n 次且最多匹配 m 次。例如，「o{1,3}」將匹配「fooooood」中的前三個 o。==其中m可以不填表示無上限。當沒有逗號{n}表示n\=m，即至少要匹配n次。==
* <font color=ff00ff>.</font>**匹配除「\n」之外的任何單個字符。** 要匹配包括「\n」在內的任何字符，請使用像「(.｜\n)」的模式。
----
<span id="regex_sed"></span>
2. sed流編輯器"stream editor for filtering and transforming text"，意即，用於過濾和轉換文本的流編輯器。
```shell
'''
sed [参数]... [执行命令] [输入文件]...
# 形如：
sed -i 's/sad/happy/' test # 表示将test文件中的"sad"替换为"happy"
'''
cp /etc/passwd ~ #複製用於練習的文件
# 打印2-5行
nl passwd | sed -n '2,5p'
# 打印奇數行
nl passwd | sed -n '1~2p'
# 將輸入文本中"shiyanlou" 全局替換為"hehe",並只打印替換的那一行，注意這裡不能省略最後的"p"命令
sed -n 's/shiyanlou/hehe/gp' passwd
# 刪除第30行
sed -i '30d' passwd
```
|參數|說明|執行命令|說明|
|---|---|---|---|
-n|安靜模式，只打印受影響的行，默認打印輸入數據的全部內容|s|行內替換
-e|用於在腳本中添加多個執行命令一次執行，在命令行中執行多個命令通常不需要加該參數|c|整行替換
-f filename|指定執行 filename 文件中的命令|a|插入到指定行的後面
-r|使用擴展正則表達式，默認為標準正則表達式|i|插入到指定行的前面
-i|將直接修改輸入文件內容，而不是打印到標準輸出設備|p|打印指定行，通常與-n參數配合使用
|||d|刪除指定行
---
<span id="regex_awk">3. awk文本處理語言</span>
AWK是一種優良的文本處理工具，它允許您創建簡短的程序，這些程序讀取輸入文件、為數據排序、處理數據、對輸入執行計算以及生成報表。最簡單地說，AWK 是一種用於處理文本的編程語言工具。
```shell
awk [-F fs] [-v var=value] [-f prog-file | 'program text'] [file...]
```
其中-F參數用於預先指定前面提到的字段分隔符（還有其他指定字段的方式） ，-v用於預先為awk程序指定變量，-f參數用於指定awk命令要執行的程序文件，或者在不加-f參數的情況下直接將程序語句放在這裡，最後為awk需要處理的文本輸入，且可以同時輸入多個文本文件。
```shell
'''
vim test #創建一個test文件
#輸入內容
I like linux
www.shiyanlou.com
'''
#使用awk將文本內容打印到終端
awk '{print}' test

#將test的第一行的每個字段單獨顯示為一行
awk '{
> if(NR==1){
> OFS="\n"
> print $1, $2, $3
> } else {
> print}
> }' test
```
你需要注意的是==NR==與==OFS==，這兩個是awk內建的變量，==NR==表示當前讀入的記錄數，你可以簡單的理解為當前處理的行數，==OFS==表示輸出時的字段分隔符，默認為" "空格，如上圖所見，我們將字段分隔符設置為\n換行符，所以第一行原本以空格為字段分隔的內容就分別輸出到單獨一行了。然後是 ==\$N==其中 N 為相應的字段號，這也是awk的內建變量，它表示引用相應的字段，因為我們這裡第一行只有三個字段，所以只引用到了 ==\$3==。除此之外另一個這裡沒有出現的 ==\$0==，它表示引用當前記錄（當前行）的全部內容。
```shell
# 將 test 的第二行的以點為分段的字段換成以空格為分隔
awk -F'.' '{
> if(NR==2){
> print $1 "\t" $2 "\t" $3
> }}' test

# 或者
awk '
> BEGIN{
> FS="."
> OFS="\t"  # 如果寫為一行，兩個動作語句之間應該以";"號分開
> }{
> if(NR==2){
> print $1, $2, $3
> }}' test
```
說明：這裡的 ==-F==參數，前面已經介紹過，它是用來預先指定待處理記錄的字段分隔符。我們需要注意的是除了指定 ==OFS==我們還可以在print 語句中直接打印特殊符號如這裡的 ==\t==，**print 打印的非變量內容都需要用""一對引號包圍起來。** 上面另一個版本，展示了實現預先指定變量分隔符的另一種方式，即使用 ==BEGIN==，就這個表達式指示了，其後的動作將在所有動作之前執行，這裡是 ==FS==賦值了新的"."點號代替默認的" "空格。