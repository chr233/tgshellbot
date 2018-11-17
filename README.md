Telegram shell bot
==================

基于telegram的shell机器人，汉化 by Chr_

[源](https://github.com/byjk/tgshellbot)

PS：Bug还是挺多的，不是我的锅

### 前置
* python3
* pip

### 安装&运行tgshellbot
```
pip install telepot
git clone https://github.com/chr233/tgshellbot.git
cd tgshellbot
python3 tgsbot.py
```
推荐使用systemd运行

### 编写插件
plugins目录是插件目录，默认插件为aliases.py

#### 没有装python3以及pip的解决方式

* python3 编译安装
```
# mkdir /usr/local/python3 # 创建安装目录
# wget --no-check-certificate https://www.python.org/ftp/python/3.6.7/Python-3.6.7.tgz
# tar -xzvf Python-3.6.7.tgz
# cd Python-3.6.7
# ./configure --prefix=/usr/local/python3
# make
# make install
# ln -s /usr/local/python3/bin/python3 /usr/bin/python3
```

* pip 编译安装
```
# wget --no-check-certificate https://github.com/pypa/pip/archive/9.0.1.tar.gz
# tar -zvxf 9.0.1 -C pip-9.0.1
# cd pip-9.0.1
# python3 setup.py install
# ln -s /usr/local/python3/bin/pip /usr/bin/pip3
# pip install --upgrade pip
```
