##### 使用Xcode预设的FileMerge工具来做比较工具
```shell
[user]
  name = Steven
  email = steven-ph@bobi.homes
[diff]
  tool = opendiff
  guitool = opendiff
[difftool "opendiff"]
  cmd = /usr/bin/opendiff \"$LOCAL\" \"$REMOTE\"
  path = /Applications/Xcode.app/Contents/Developer/usr/bin/opendiff
  trustExitCode = true #kill the process
  prompt = false
[merge]
  tool = opendiff
[mergetool "opendiff"]
  cmd = opendiff \"$LOCAL\" \"$REMOTE\" -ancestor \"$BASE\"
  path = /usr/bin/opendiff
  trustExitCode = true
  keepBackup = false
[alias]
  tree = log --graph --decorate --pretty=oneline --abbrev-commit --all
[difftool]
  prompt = false #general disable prompt
```

其他系统没有`opendiff`这么酷的工具，但有类似的工具[Meld](http://meldmerge.org)

https://superuser.com/questions/22360/difftool-for-ubuntu-like-os-xs-opendiff