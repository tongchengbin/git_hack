# git_hack
git文件泄露源码爆破漏洞 源码恢复

## Use
```
git clone https://github.com/tongchengbin/git_hack.git
pip install -r requirements.txt
python3 run.py
# 项目默认下载到执行目录的的create文件夹下
cd create
# 直接恢复到最后一次源码 可以使用git log 查看提交历史
git checkout .
```
