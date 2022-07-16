# 构建家庭事件总线lightbus

## nas上安装redis-server
系统实际上是自带redis的，但是为了不搞坏系统自带的哪一个，所以需要再启动一个redis实例，并且做好配置，比如密码之类的

### nas上的服务控制系统
参考资料：http://www.wjhsh.net/kelamoyujuzhen-p-10111596.html
systemctl

那么问题就是如何写一个东西，注册到systemctl下成为一个unit了

参考资料：将程序进程注册为Linux系统服务
http://t.zoukankan.com/fusheng11711-p-12893296.html

简单的说就是，需要把一个后缀名为service的文件，放在/usr/lib/systemd/system下面
从而注册服务

#### service的文件格式
vim /usr/lib/systemd/system/sshd.service

	[Unit]
	Description=OpenSSH server daemon
	Documentation=man:sshd(8) man:sshd_config(5)
	After=network.target sshd-keygen.service
	Wants=sshd-keygen.service

	[Service]
	Type=notify
	EnvironmentFile=/etc/sysconfig/sshd
	ExecStart=/usr/sbin/sshd -D $OPTIONS
	ExecReload=/bin/kill -HUP $MAINPID
	KillMode=process
	Restart=on-failure
	RestartSec=42sPrivateTmp=true

#### 开始编写redis.service
参考资料：Centos7中将redis服务写入systemctl
https://www.cnblogs.com/xzlive/p/16391089.html


[Unit]
Description=lightbus redis #描述内容
#在哪些服务启动之后启动
After=network.target
 
[Service]
Type=forking
#PIDFile和redis.conf配置中一致
PIDFile=/var/run/lightbus_redis.pid
ExecStart=/bin/redis-server /etc/lightbus_redis.conf
#重新加载和停止服务的命令
ExecReload=/bin/kill -s HUP $MAINPID
ExecStop=/bin/kill -s QUIT $MAINPID
PrivateTmp=true
 
#系统以默认多用户方式启动时，此服务自动运行。
[Install]
#Alias:服务别名
WantedBy=multi-user.target

#### redis本身的配置文档redis.conf
lemonhall@nas16t:/var/run$ redis-server -v
Redis server v=6.0.16 sha=03f5dd9e:0 malloc=jemalloc-5.1.0 bits=64 build=790da19d1a8d22f4
lemonhall@nas16t:/var/run$ 

看了一下版本号，是一个6.0.16的redis
ok，到官网上去下载了https://download.redis.io/releases/redis-6.0.16.tar.gz

然后打开了redis.conf
在/etc/目录下新建了一个文件
sudo vim lightbus_redis.conf

##### 修改绑定ip地址

	# IF YOU ARE SURE YOU WANT YOUR INSTANCE TO LISTEN TO ALL THE INTERFACES
	# JUST COMMENT OUT THE FOLLOWING LINE.
	# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
	bind 127.0.0.1

改成0.0.0.0

##### 修改守护进程

	################################# GENERAL #####################################

	# By default Redis does not run as a daemon. Use 'yes' if you need it.
	# Note that Redis will write a pid file in /var/run/redis.pid when daemonized.
	daemonize no

改成 yes

##### 修改pid文件名

	# Creating a pid file is best effort: if Redis is not able to create it
	# nothing bad happens, the server will start and run normally.
	pidfile /var/run/redis_6379.pid

改成pidfile /var/run/lightbus_redis.pid

##### 修改保护模式

	# By default protected mode is enabled. You should disable it only if
	# you are sure you want clients from other hosts to connect to Redis
	# even if no authentication is configured, nor a specific set of interfaces
	# are explicitly listed using the "bind" directive.
	protected-mode yes

改为no

##### 修改监听的端口号
	# Accept connections on the specified port, default is 6379 (IANA #815344).
	# If port 0 is specified Redis will not listen on a TCP socket.
	port 6379

改为 18505，看了一下这个端口号没人用


##### 修改监护行为
	# Note: these supervision methods only signal "process is ready."
	#       They do not enable continuous pings back to your supervisor.
	supervised no

改为 auto，似乎不该就会hang住

#### 写入service文件，并注册服务
参考资料：Centos7中将redis服务写入systemctl
https://www.cnblogs.com/xzlive/p/16391089.html

sudo vim lightbus_redis.service

sudo systemctl daemon-reload 重载所有的命令

sudo systemctl list-units --all 看不到units，很有趣吧

list-units：依据unit列出目前有启动的unit。若加上--all才会列出没启动的。（等价于无参数）

-rw-------  1 root root   509 Jul 16 17:59 lightbus_redis.service
-rw-r--r--  1 root root   388 Dec 24  2021 sshd.service

然后看了一下，感觉是权限的问题

##### 修改文件权限

参考资料：Linux中将文件权限和所有权复制到另一个文件
https://blog.csdn.net/xyajia/article/details/111225677

sudo chmod --reference=sshd.service lightbus_redis.service
-rw-r--r-- 1 root root  509 Jul 16 17:59 lightbus_redis.service


sudo systemctl start lightbus_redis.service


##### 启动
lemonhall@nas16t:/usr/lib/systemd/system$ sudo systemctl start lightbus_redis.service
lemonhall@nas16t:/usr/lib/systemd/system$ sudo systemctl list-units --all | grep lightbus
  lightbus_redis.service                                                                                               loaded    active     running   lightbus redis #描述内容
lemonhall@nas16t:/usr/lib/systemd/system$ 

sudo systemctl stop lightbus_redis.service

##### 命令
	start：立刻启动后面接的unit
	stop：立刻关闭后面接的unit
	restart：立刻关闭后启动后面接的unit，亦即执行stop再start的意思
	reload：不关闭后面接的unit的情况下，重载配置文件，让设定生效
	enable：设定下次开机时，后面接的unit会被启动
	disable：设定下次开机时，后面接的unit 不会被启动
	status：目前后面接的这个unit 的状态，会列出是否正在执行、是否开机启动等信息。
	is-active：目前有没有正在运行中
	is-enable：开机时有没有预设要启用这个unit
	list-units：依据unit列出目前有启动的unit。若加上--all才会列出没启动的。（等价于无参数）
	list-unit-files：列出所有以安装unit以及他们的开机启动状态（enabled、disabled、static、mask）。
	--type=TYPE：就是unit type，主要有service，socket，target等
	get-default： 取得目前的 target
	set-default：设定后面接的 target 成为默认的操作模式
	isolate：切换到后面接的模式
	list-dependencies ：列出unit之间依赖性
	list-sockets：查看监听socket的unit


sudo systemctl status lightbus_redis.service


	lemonhall@nas16t:/usr/lib/systemd/system$ sudo systemctl status lightbus_redis.service
	● lightbus_redis.service - lightbus redis #描述内容
	   Loaded: loaded (/usr/lib/systemd/system/lightbus_redis.service; disabled; vendor preset: disabled)
	   Active: active (running) since Sat 2022-07-16 18:21:57 CST; 2min 8s ago
	  Process: 13314 ExecStop=/bin/kill -s QUIT $MAINPID (code=exited, status=0/SUCCESS)
	  Process: 14017 ExecStart=/bin/redis-server /etc/lightbus_redis.conf (code=exited, status=0/SUCCESS)
	 Main PID: 14021 (redis-server)
	   Memory: 1.3M
	   CGroup: /system.slice/lightbus_redis.service
	           └─14021 /bin/redis-server 0.0.0.0:18505

	Jul 16 18:21:57 nas16t systemd[1]: Starting lightbus redis #描述内容...
	Jul 16 18:21:57 nas16t systemd[1]: PID file /var/run/lightbus_redis.pid not readable (yet?) after start.
	Jul 16 18:21:57 nas16t systemd[1]: Started lightbus redis #描述内容.
	lemonhall@nas16t:/usr/lib/systemd/system$ cat /var/run/lightbus_redis.pid
	14021
	lemonhall@nas16t:/usr/lib/systemd/system$ 

状态是OK的，然后enable一下看看

sudo systemctl enable lightbus_redis.service

这样就会下一次开机自启动了