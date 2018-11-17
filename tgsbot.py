#/usr/bin/python3
#-*- coding:utf-8 -*-

import os
import time
import json
import telepot
import importlib
from telepot.loop import MessageLoop


class TelegramShellBot:
    _token = ''
    _bot = None
    _adm_chat_id = 0
    _cmdList = []
    _config_filename = os.path.join(os.path.dirname(os.path.abspath(__file__)),'config.json')
    _plugins = []

    def loadplugins(self):
        path = os.path.abspath(__file__)
        path = os.path.join(os.path.dirname(path),'plugins')
        for filename in os.listdir(path):
            name, ext = os.path.splitext(filename)
            if ext == '.py':
                try:
                    p = importlib.import_module('plugins.'+name)
                    p.plugin_init(self)
                    self._plugins.append(p)
                except Exception as e:
                    print ("加载插件 {0} 出错：{1}".format(filename, e))

    def find_plugincmd(self, c):
        for p in self._plugins:
            try:
                if p.plugin_ismycmd(c):
                    return p
            except:
                pass
        return None

    def saveconfig(self):
        c = {}
        c['token'] = self._token
        c['chat_id'] = self._adm_chat_id
        with open(self._config_filename, 'w') as outfile:
            json.dump(c, outfile)

    def loadconfig(self):
        try:
            with open(self._config_filename) as json_data_file:
                c = json.load(json_data_file)
                self._token = c['token']
                self._adm_chat_id = c['chat_id']
                return True
        except Exception:
            pass
        return False

    def setup(self):
        print('输入Bot Token：', end='')
        self._token = input()
        self._bot = telepot.Bot(self._token)
        p = self._bot.getMe()
        print('Bot名：', p['username'])
        print('等待管理员发送消息 (Ctrl+C 退出)...')
        p = []
        offset = None 
        while True:
            p = self._bot.getUpdates(offset=offset)
			# print(p)
            for m in p:
                if 'update_id' in m.keys():
                    offset = m['update_id']+1
                print('管理员ID是 [ "', m['message']['chat']['username'], '" ] 吗? (Y/n)', end='')
                s = input()
                if s in ['', 'y', 'Y']:
                    self._adm_chat_id = m['message']['chat']['id']
                    return True
            time.sleep(1)
        return False

    def handle(self, msg):
        content_type, chat_type, chat_id = telepot.glance(msg)
        # print(content_type, chat_type, chat_id)
        # print(msg)
        try:
            if self._adm_chat_id == chat_id:
                self.handle_master(msg)
            else:
                self.sendMessage("你没有权利这么做")
        except Exception as err:
            self.sendMessage("错误：{0}".format(err))

    def cmdHandler(self, txt):
        cmd = txt.split(' ')
        c = cmd[0].lower()
        if c == '/start':
            self.sendMessage('机器人已连接')
        elif c == '/stop':
            self.sendMessage('机器人停止中……')
			exit()
        else:
            plug = self.find_plugincmd(c[1:])
            if plug:
                plug.plugin_handler(txt)
            else:
                self.sendMessage('未知命令：'+c)

    def call_shell(self, text):
        t = text
        p = os.popen(t)
        out = p.read()
        cod = p.close()
        if out:
            while len(out) > 4000:
                o2, out = out[:4000], out[4000:]
                self.sendMessage(o2)                            
            if out:
                self.sendMessage(out)
        elif cod:
            self.sendMessage("错误，退出码：" + str(cod))
        else:
            self.sendMessage("无返回值")

    def handle_master(self, msg):
        content_type, chat_type, chat_id = telepot.glance(msg)
        if content_type == 'text':
            t = msg['text']
            s = t.split(' ')
            if t[0] == '/':
                self.cmdHandler(t)        
            elif len(s) > 0 and s[0].lower() == 'cd':
                if len(s) > 1:
                    os.chdir(s[1])
                self.sendMessage(os.getcwd())
            else:
                self.call_shell(t)
        elif content_type == 'document':
            doc = msg['document']
            f = os.path.join(os.getcwd(), doc['file_name'])
            self._bot.download_file(doc['file_id'], f)
            self.sendMessage(f)        

    def sendMessage(self, msg):
        self._bot.sendMessage(self._adm_chat_id, msg)

    def __init__(self):
        if not self.loadconfig():
            if not self.setup():
                print('不支持的启动方式')
                exit()
            else:
                self.saveconfig()
        self._bot = telepot.Bot(self._token)
        self.loadplugins()
        MessageLoop(self._bot, self.handle).run_as_thread()
        print('开始监听消息 ...')
        # Keep the program running.
        while 1:
            time.sleep(50)

if __name__ == '__main__':
    print('Telegram shell bot 启动')
    TelegramShellBot()
