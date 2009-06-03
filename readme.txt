  WebSniffer 0.1.5 - The web debug proxy
===============================================================================

Copyright(C) 2009 yinzhigang <sxin.net@gmail.com>
All rights reserved.

1.安装
-----------------
本软件为纯绿色软件
Windows:
    系统需求：Windows 2000/XP/Vista
    解压缩到任意文件夹，推荐Profram Files文件夹，双击 WebSniffer.exe 执行。
Linux:
    系统需求：GTK 2.13以上，libwx_gtk2 unicode 2.8.7以上
    解压缩至任意目录，推荐/opt目录。
MacOS:
    系统需求：Intel平台，Leopard下测试通过
    双击DMG文件打开，复制WebSniffer至应用程序文件夹。

2.使用说明
-----------------
本软件使用代理模式来抓取浏览器请求信息，使用前要先设置浏览器http代理为127.0.0.1:8789
此端口及IP可通过软件设置界面修改

设置完成后点击WebSniffer工具栏第一个按钮启动监听模式，此后浏览器所有通信会被记录，点击左侧记录树
可查看相关记录详细信息，包括请求与回应头信息、Cookie、文本、图像等。

点击工具栏第二个按钮可清空监听记录。
