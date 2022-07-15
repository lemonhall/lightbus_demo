
# 新建一个环境
conda create --name lightbus python=3.8 --channel https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/free/

# 激活这个环境
conda activate lightbus

# 安装lightbus
pip3 install lightbus

# 测一下
新建和一个
bus.py

内容如下：

import lightbus

bus = lightbus.create()

然后运行
lightbus run

(lightbus) lemonhall@yuningdeMacBook-Pro:~/Lightbus$ lightbus run
Traceback (most recent call last):
  File "/Users/lemonhall/opt/anaconda3/envs/lightbus/bin/lightbus", line 5, in <module>
    from lightbus.commands import lightbus_entry_point
  File "/Users/lemonhall/opt/anaconda3/envs/lightbus/lib/python3.8/site-packages/lightbus/__init__.py", line 1, in <module>
    from lightbus.utilities.logging import configure_logging
  File "/Users/lemonhall/opt/anaconda3/envs/lightbus/lib/python3.8/site-packages/lightbus/utilities/logging.py", line 6, in <module>
    from lightbus.config import Config
  File "/Users/lemonhall/opt/anaconda3/envs/lightbus/lib/python3.8/site-packages/lightbus/config/__init__.py", line 1, in <module>
    from .config import Config
  File "/Users/lemonhall/opt/anaconda3/envs/lightbus/lib/python3.8/site-packages/lightbus/config/config.py", line 11, in <module>
    from lightbus.schema.hints_to_schema import python_type_to_json_schemas, SCHEMA_URI
  File "/Users/lemonhall/opt/anaconda3/envs/lightbus/lib/python3.8/site-packages/lightbus/schema/__init__.py", line 1, in <module>
    from .schema import Schema, Parameter, WildcardParameter
  File "/Users/lemonhall/opt/anaconda3/envs/lightbus/lib/python3.8/site-packages/lightbus/schema/schema.py", line 27, in <module>
    from lightbus.transports.registry import SchemaTransportPoolType
  File "/Users/lemonhall/opt/anaconda3/envs/lightbus/lib/python3.8/site-packages/lightbus/transports/__init__.py", line 14, in <module>
    from lightbus.transports.redis.rpc import RedisRpcTransport
  File "/Users/lemonhall/opt/anaconda3/envs/lightbus/lib/python3.8/site-packages/lightbus/transports/redis/__init__.py", line 1, in <module>
    from lightbus.transports.redis.event import RedisEventTransport
  File "/Users/lemonhall/opt/anaconda3/envs/lightbus/lib/python3.8/site-packages/lightbus/transports/redis/event.py", line 19, in <module>
    from aioredis import ConnectionClosedError, ReplyError
ImportError: cannot import name 'ConnectionClosedError' from 'aioredis' (/Users/lemonhall/opt/anaconda3/envs/lightbus/lib/python3.8/site-packages/aioredis/__init__.py)
(lightbus) lemonhall@yuningdeMacBook-Pro:~/Lightbus$

报错，我觉得这几乎就是废话

这个人写得文档这一点我很无语，redis启动好难道不是先配置么

真是


# 配置
https://lightbus.org/latest/reference/configuration/

# Root configuration
bus:
  # Bus configuration

  schema:
    # Schema configuration

    transport:
      # Transport selector config

      redis:
        url: "redis://192.168.50.233:6379/0"


# 新启了一个redis
Could not connect: DENIED Redis is running in protected mode because protected mode is enabled, no bind address was specified, no authentication password is requested to clients. In this mode connections are only accepted from the loopback interface. If you want to connect from external computers to Redis you may adopt one of the following solutions: 1) Just disable protected mode sending the command 'CONFIG SET protected-mode no' from the loopback interface by connecting to Redis from the same host the server is running, however MAKE SURE Redis is not publicly accessible from internet if you do so. Use CONFIG REWRITE to make this change permanent. 2) Alternatively you can just disable the protected mode by editing the Redis configuration file, and setting the protected mode option to 'no', and then restarting the server. 3) If you started the server manually just for testing, restart it with the '--protected-mode no' option. 4) Setup a bind address or an authentication password. NOTE: You only need to do one of the above things in order for the server to start accepting connections from the outside.

CONFIG SET protected-mode no

--protected-mode no

# aioredis又报错了，哎，python这些包啊

ERROR: Could not find a version that satisfies the requirement aioredis==3.0.0 (from versions: 0.0.2, 0.1.0, 0.1.1, 0.1.2, 0.1.3, 0.1.4, 0.1.5, 0.2.0, 0.2.1, 0.2.2, 0.2.3, 0.2.4, 0.2.5, 0.2.6, 0.2.7, 0.2.8, 0.2.9, 0.3.0, 0.3.1, 0.3.2, 0.3.3, 0.3.4, 0.3.5, 1.0.0b1, 1.0.0b2, 1.0.0, 1.1.0, 1.2.0, 1.3.0, 1.3.1, 2.0.0a1, 2.0.0b1, 2.0.0, 2.0.1)

# 上面那一堆的报错说到底就是个恶心人的东西

export LIGHTBUS_CONFIG="/Users/lemonhall/Lightbus/lightbus.yaml"

每一个client还是server记得都导出文件就行

# 终于跑通
MainThread | lightbus.client.bus_client     | Executing before_worker_start & on_start hooks...
MainThread | lightbus.client.bus_client     | Execution of before_worker_start & on_start hooks was successful
MainThread | lightbus.client.subclients.rpc_result | ⚡  Executed hello.world in 1.23 milliseconds
MainThread | lightbus.client.subclients.rpc_result | ⚡  Executed hello.world in 0.54 milliseconds


# 吐槽
真的需要吐槽一下，这个作者的文档写作思路极其反人类，文档里的错误多得很


