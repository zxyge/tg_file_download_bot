## Tg文件下载机器人：

将文件发送给机器人后自动下载文件到本地或上传到网盘中
上传网盘需要rclone配合

---
原项目：
https://github.com/EverythingSuckz/TG-FileStreamBot

----
安装方法
```
git clone https://github.com/zxyge/tg_file_download_bot.git
cd tg_file_download_bot
mv .env.example .env
pip3 install -r requirements.txt
python3 -m WebStreamer
```

使用方法：
```
API_ID : 去 my.telegram.org 获取.
API_HASH : 去 my.telegram.org 获取.
BOT_TOKEN : @BotFather获取
BIN_CHANNEL : 创建一个频道（公开私有都行），把bot拉进去设置成管理员，转发给bot的消息都会发送到这个频道，删除频道内的消息后对应的url将不可用
其他参数参考env文件中的注释自行修改。
将文件转发给bot
```

如要开启上传，需安装rclone，并配置好网盘。

