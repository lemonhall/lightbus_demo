
## 群晖上原生安装lightbus

不安装的话，有一些想在群晖的宿主机器上直接执行的命令，就不太好穿透容器了

所以安装的过程需要很小心

	$ python
	Python 3.8.12 (default, Nov 15 2021, 06:04:41)
	[GCC 8.5.0] on linux
	Type "help", "copyright", "credits" or "license" for more information.
	>>> quit()

3.8.12，这还是一个很现代的版本

* [virtualenv](https://virtualenv.pypa.io/en/stable/index.html)

嗯，还是用这个吧，先看一下主页

	python3 -m ensurepip --default-pip

首先还是需要装好pip

	$ python3 -m ensurepip --default-pip
	Defaulting to user installation because normal site-packages is not writeable
	Looking in links: /tmp/tmpbcbz1fm5
	Processing /tmp/tmpbcbz1fm5/setuptools-56.0.0-py3-none-any.whl
	Processing /tmp/tmpbcbz1fm5/pip-21.1.1-py3-none-any.whl
	Installing collected packages: setuptools, pip
	  WARNING: The scripts pip, pip3 and pip3.8 are installed in '/var/services/homes/lemonhall/.local/bin' which is not on PATH.
	  Consider adding this directory to PATH or, if you prefer to suppress this warning, use --no-warn-script-location.
	Successfully installed pip-21.1.1 setuptools-56.0.0

好家伙，这东西被安装到了：/var/services/homes/lemonhall/.local/bin

vim ~/.bashrc

	export PATH=/var/services/homes/lemonhall/.local/bin:$PATH

好了
	source ~/.bashrc

source一下文件

可以看到pip了

哎，有装了一个叫pipx的东西
python3 -m pip install --user pipx

终于可以开始装真正的东西了
pipx install virtualenv #不用这个，这个很烂

python -m pip install --user virtualenv

网速好慢，配置镜像
pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple

### 建立一个虚拟环境

virtualenv lightbus

激活它

source lightbus/bin/activate


### 配置yaml文件

	# Root configuration
	bus:
	  # Bus configuration

	  schema:
	    # Schema configuration

	    transport:
	      # Transport selector config

	      redis:
	        url: "redis://127.0.0.1:18505/0"

	apis:
	  # API configuration listing

	  default:
	    # Api config

	    event_transport:
	      # Transport selector configuration
	      redis:
	        url: "redis://127.0.0.1:18505/0"

	    rpc_transport:
	      # Transport selector configuration
	      redis:
	        url: "redis://127.0.0.1:18505/0"

	    result_transport:
	      # Transport selector configuration
	      redis:
	        url: "redis://127.0.0.1:18505/0"

### 配置全局变量
export LIGHTBUS_CONFIG="/var/services/homes/lemonhall/lightbus/lightbus.yaml"


### 安装lightbus
pip3 install lightbus

### 测试以上是否成功

新建bus.py

	import lightbus
	bus = lightbus.create()

lightbus run

echo $LIGHTBUS_CONFIG


	Traceback (most recent call last):
	  File "/volume1/homes/lemonhall/lightbus/bin/lightbus", line 5, in <module>
	    from lightbus.commands import lightbus_entry_point
	  File "/volume1/homes/lemonhall/lightbus/lib/python3.8/site-packages/lightbus/__init__.py", line 1, in <module>
	    from lightbus.utilities.logging import configure_logging
	  File "/volume1/homes/lemonhall/lightbus/lib/python3.8/site-packages/lightbus/utilities/logging.py", line 6, in <module>
	    from lightbus.config import Config
	  File "/volume1/homes/lemonhall/lightbus/lib/python3.8/site-packages/lightbus/config/__init__.py", line 1, in <module>
	    from .config import Config
	  File "/volume1/homes/lemonhall/lightbus/lib/python3.8/site-packages/lightbus/config/config.py", line 11, in <module>
	    from lightbus.schema.hints_to_schema import python_type_to_json_schemas, SCHEMA_URI
	  File "/volume1/homes/lemonhall/lightbus/lib/python3.8/site-packages/lightbus/schema/__init__.py", line 1, in <module>
	    from .schema import Schema, Parameter, WildcardParameter
	  File "/volume1/homes/lemonhall/lightbus/lib/python3.8/site-packages/lightbus/schema/schema.py", line 27, in <module>
	    from lightbus.transports.registry import SchemaTransportPoolType
	  File "/volume1/homes/lemonhall/lightbus/lib/python3.8/site-packages/lightbus/transports/__init__.py", line 14, in <module>
	    from lightbus.transports.redis.rpc import RedisRpcTransport
	  File "/volume1/homes/lemonhall/lightbus/lib/python3.8/site-packages/lightbus/transports/redis/__init__.py", line 1, in <module>
	    from lightbus.transports.redis.event import RedisEventTransport
	  File "/volume1/homes/lemonhall/lightbus/lib/python3.8/site-packages/lightbus/transports/redis/event.py", line 19, in <module>
	    from aioredis import ConnectionClosedError, ReplyError
	ImportError: cannot import name 'ConnectionClosedError' from 'aioredis' (/volume1/homes/lemonhall/lightbus/lib/python3.8/site-packages/aioredis/__init__.py)



	(lightbus) lemonhall@nas16t:~/lightbus$ pip install aioredis==3.1.0
	Defaulting to user installation because normal site-packages is not writeable
	Looking in indexes: https://pypi.tuna.tsinghua.edu.cn/simple
	ERROR: Could not find a version that satisfies the requirement aioredis==3.1.0 (from versions: 0.0.2, 0.1.0, 0.1.1, 0.1.2, 0.1.3, 0.1.4, 0.1.5, 0.2.0, 0.2.1, 0.2.2, 0.2.3, 0.2.4, 0.2.5, 0.2.6, 0.2.7, 0.2.8, 0.2.9, 0.3.0, 0.3.1, 0.3.2, 0.3.3, 0.3.4, 0.3.5, 1.0.0b1, 1.0.0b2, 1.0.0, 1.1.0, 1.2.0, 1.3.0, 1.3.1, 2.0.0a1, 2.0.0b1, 2.0.0, 2.0.1)
	ERROR: No matching distribution found for aioredis==3.1.0
	(lightbus) lemonhall@nas16t:~/lightbus$

前天这个错误也困扰了我，竟然忘记记录了

source lightbus/bin/activate
pip install pipreqs

	(lightbus) lemonhall@yuningdeMBP:~/Lightbus$ cat requirements.txt
	aioredis==1.3.0
	async-timeout==4.0.2
	attrs==21.4.0
	certifi @ file:///private/var/folders/sy/f16zz6x50xz3113nwtb9bvq00000gp/T/abs_83242e7e-f82d-4a71-8ef2-9d71d212d249gu_wxmeq/croots/recipe/certifi_1655968827803/work/certifi
	charset-normalizer==2.1.0
	docopt==0.6.2
	hiredis==2.0.0
	idna==3.3
	importlib-resources==5.8.0
	jsonschema==4.7.2
	lightbus==1.1.2
	pipreqs==0.4.11
	pyrsistent==0.18.1
	PyYAML==6.0
	requests==2.28.1
	typing_extensions==4.3.0
	urllib3==1.26.10
	yarg==0.1.9
	zipp==3.8.1

OK,那个报错还是因为链接不上导致的

	(lightbus) lemonhall@nas16t:~/lightbus$ lightbus run
	MainThread | lightbus.creation              | Importing bus.py from bus
	MainThread | lightbus.creation              | Loading config from /var/services/homes/lemonhall/lightbus/lightbus.yaml
	MainThread | lightbus.commands.run          | Lightbus is setting up:
	           |                                |     ∙ service_name (set with -s or LIGHTBUS_SERVICE_NAME)  : square-sun-170
	           |                                |     ∙ process_name (with with -p or LIGHTBUS_PROCESS_NAME) : pbhd
	           |                                |
	MainThread | lightbus.commands.run          | Default transports are setup as follows:
	           |                                |     ∙ RPC transport    : TransportPool @ redis://127.0.0.1:18505/0
	           |                                |     ∙ Result transport : TransportPool @ redis://127.0.0.1:18505/0
	           |                                |     ∙ Event transport  : TransportPool @ redis://127.0.0.1:18505/0
	           |                                |     ∙ Schema transport : TransportPool @ redis://127.0.0.1:18505/0
	           |                                |
	MainThread | lightbus.commands.run          | No plugins loaded
	MainThread | lightbus.client.bus_client     | Enabled features (3):
	           |                                |     ∙ rpcs
	           |                                |     ∙ events
	           |                                |     ∙ tasks
	           |                                |
	MainThread | lightbus.client.bus_client     | Disabled features (0):
	           |                                |
	MainThread | lightbus.client.bus_client     | APIs in registry (2):
	           |                                |     ∙ internal.state
	           |                                |     ∙ internal.metrics
	           |                                |
	MainThread | lightbus.client.bus_client     | Loaded the following remote schemas (2):
	           |                                |     ∙ internal.metrics
	           |                                |     ∙ internal.state
	           |                                |
	MainThread | lightbus.client.bus_client     | Loaded the following local schemas (2):
	           |                                |     ∙ internal.state
	           |                                |     ∙ internal.metrics
	           |                                |
	MainThread | lightbus.client.bus_client     | Executing before_worker_start & on_start hooks...
	MainThread | lightbus.client.bus_client     | Execution of before_worker_start & on_start hooks was successful

### 接下来的问题是怎么把lightbus组成的service注册起来

这个就有点麻烦了，说实话，不是root的

接下来再看看，如果使用systemctl也不是不行，就是会不会太重了？