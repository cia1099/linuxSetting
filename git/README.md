##### 使用Xcode预设的FileMerge工具来做代码比较工具
```shell
[user]
	email = steven-ph@bobi.homes
	name = Steven Dante Torres

[diff]
  tool = opendiff
  guitool = opendiff
[difftool]
  prompt = false #general disable prompt
[merge]
  tool = code
[alias]
  tree = log --graph --decorate --pretty=oneline --abbrev-commit --all
# [http]
	# cookiefile = /home/cia1099/.gitcookies

[difftool "kdiff3"]
	cmd = kdiff3 \"$LOCAL\" \"$REMOTE\"
	trustExitCode = true
	prompt = false
[mergetool "kdiff3"]
	cmd = /usr/local/sbin/kdiff3 \"$BASE\" \"$LOCAL\" \"$REMOTE\" -o \"$MERGED\"
	trustExitCode = false
	keepBackup = false

[difftool "opendiff"]
  cmd = opendiff \"$LOCAL\" \"$REMOTE\"
  path = /Applications/Xcode.app/Contents/Developer/usr/bin/opendiff
  trustExitCode = true #kill the process
  prompt = false
[mergetool "opendiff"]
  cmd = opendiff \"$LOCAL\" \"$REMOTE\" -ancestor \"$BASE\" -merge \"$MERGED\"
  trustExitCode = false #must save before confirm merge
  keepBackup = false

[difftool "code"]
  cmd = code -n --disable-extensions --wait --diff $LOCAL $REMOTE
  trustExitCode = true
	prompt = false
[mergetool "code"]
  cmd = code -n --disable-extensions --wait -- --merge $LOCAL $REMOTE $BASE $MERGED
  trustExitCode = false
	keepBackup = false
```
#### Used VSCode as Comparator
记得要将restrict mode给关掉：\
Setting搜寻`restrict`把Banner设成never，这样才不会每次开启diff window的时候都问你trust。

其他系统没有`opendiff`这么酷的工具，但有类似的工具[Meld](http://meldmerge.org)

https://superuser.com/questions/22360/difftool-for-ubuntu-like-os-xs-opendiff
