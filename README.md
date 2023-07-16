# HCNetSDK-python

海康威视网络SDK的Python封装，支持Windows和Linux。

欢迎使用，欢迎提出建议。

## 安装

你可以通过 `pip` 来安装 `HCNetSDK-python`:

```shell
pip install HCNetSDK-python
```

也可以自己构建安装包:

```shell
python setup.py bdist_wheel --library-dirs your_CH-HCNetSDKV/Libs your_MediaPlayControl/Libs --platform {win64, linux64, win32, linux32}

pip install dist/HCNetSDK_python-{version}-py3-none-{platform}.whl
```

## 使用

具体使用方法请参考 `examples` 。

```python
from HCNetSDK import *

# 获取NetSDK对象并初始化
sdk = NetClient()
sdk.Init()
sdk.SetConnectTime(2000, 3)
sdk.SetReconnect(10000, True)
sdk.SetLogToFile(3)

# 登录设备
lUserId, device_info = sdk.Login_V40(ip, port, username, password)

# 登出设备
sdk.Logout(lUserId)
```