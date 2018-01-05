
**被动式扫描框架 sscan v1.0**


----------


目录结构
----

 1. proxy
    - 代理模块。支持http(s)，https需安装openssl
 2. scan 
    - 扫描模块。现阶段包含mysql注入、命令注入、php代码注入插件。
 3. web
    - web模块。Django + bootstrap-table 的简单扫描结果展示。
 4. handler.py
    - 启动脚本。
 5. whitelist.txt
    - host白名单。若为空则表示无白名单。

使用说明
----

 1. 启动代理 + 扫描，第一个参数为监听端口

    python handler.py 8088

 2. 启动Django manage

    python web/manage.py runserver 8089
    
环境依赖
----

 1. redis
 2. openssl
 3. 第三方模块
    - requests
    - redis
    - django
    - chardet


**该项目仍在完善中...**