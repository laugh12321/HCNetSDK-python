#!/usr/bin/env python
# -*-coding:utf-8 -*-
# ==============================================================================
# Copyright (c) 2023 laugh12321 Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================
# File    :   NetSDK.py
# Version :   1.0
# Author  :   laugh12321
# Contact :   laugh12321@vip.qq.com
# Date    :   2023/01/30 10:44:16
# Desc    :   None
# ==============================================================================

from typing import Any, Dict, Tuple

from .SDK_Callback import *
from .SDK_Enum import *
from .SDK_Struct import *


class Singleton(type):
    def __init__(self, *args, **kwargs) -> None:
        self.__instance = None
        super().__init__(*args, **kwargs)

    def __call__(self, *args, **kwargs) -> Any:
        if self.__instance is None:
            self.__instance = super(Singleton, self).__call__(*args, **kwargs)
        return self.__instance


class NetClient(metaclass=Singleton):
    """
    所有sdk接口都定义为该类的类方法
    all function in sdk which used define in this class
    """

    def __init__(self, *args, **kwargs) -> None:
        self._load_library()
        self.SetSDKInitCfg()


    @classmethod
    def _load_library(cls) -> None:
        try:
            cls.sdk = load_library(netsdkdllpath)
            cls.play_sdk = load_library(playsdkdllpath)
        except OSError as e:
            print('动态库加载失败')

        cls.coding_format = 'gbk' if sys_platform == 'windows' else 'utf-8'

    @classmethod
    def SetSDKInitCfg(cls) -> None:
        """
        设置HCNetSDKCom组件库和SSL库加载路径
        """
        sdk_ComPath = NET_DVR_LOCAL_SDK_PATH()
        sdk_ComPath.sPath = lib_path_dict[sys_platform].encode(cls.coding_format)
        cls.sdk.NET_DVR_SetSDKInitCfg(2, byref(sdk_ComPath))
        cls.sdk.NET_DVR_SetSDKInitCfg(3, create_string_buffer(bytes(netsdkcomdllpath, encoding=cls.coding_format)))
        cls.sdk.NET_DVR_SetSDKInitCfg(4, create_string_buffer(bytes(sslmdllpath, encoding=cls.coding_format)))

    @classmethod
    def GetLastError(cls, lib_type: str = 'play') -> int:
        """
        获取错误号

        Args:
            lib_type (str, optional): 库类型. Defaults to 'play'.

        Returns:
            int: 错误号
        """
        return cls.sdk.NET_DVR_GetLastError() if lib_type != 'play' else cls.play_sdk.PlayM4_GetLastError()

    @classmethod
    def Init(cls) -> None:
        """
        初始化DLL
        """
        cls.sdk.NET_DVR_Init()

    @classmethod
    def SetConnectTime(cls, waittime: int = 2000, trytimes: int = 3) -> None:
        """
        设置网络连接超时时间和连接尝试次数
        """
        cls.sdk.NET_DVR_SetConnectTime(waittime, trytimes)

    @classmethod
    def SetReconnect(cls, interval: int = 10000, enable_recon: bool = True) -> None:
        """
        设置重连功能
        """
        cls.sdk.NET_DVR_SetReconnect(interval, enable_recon)

    @classmethod
    def SetLogToFile(cls, level: int, logdir: str = logdir, auto_del: bool = True) -> None:
        """
        设置日志文件
        """
        cls.sdk.NET_DVR_SetLogToFile(level, logdir.encode(cls.coding_format), auto_del)

    @classmethod
    def Cleanup(cls) -> None:
        """
        释放SDK资源, 在程序结束之前调用
        """
        cls.sdk.NET_DVR_Cleanup()

    @classmethod
    def Login_V40(cls, ip: str, port: int, username: str, password: str, async_login: int = 0, login_mode: int = 0) -> Tuple[c_long, NET_DVR_DEVICEINFO_V40]:
        """
        用户注册设备 (支持异步登录)

        Args:
            ip (str): _description_
            port (int): _description_
            username (str): _description_
            password (str): _description_
            async_login (int, optional): _description_. Defaults to 0.
            login_mode (int, optional): _description_. Defaults to 0.

        Returns:
            Tuple[c_long, NET_DVR_DEVICEINFO_V40]: _description_
        """
        device_info = NET_DVR_DEVICEINFO_V40()
        login_info = NET_DVR_USER_LOGIN_INFO()
        login_info.sUserName = username.encode(cls.coding_format)
        login_info.sPassword = password.encode(cls.coding_format)
        login_info.sDeviceAddress = ip.encode(cls.coding_format)
        login_info.bUseAsynLogin = async_login
        login_info.byLoginMode = login_mode
        login_info.wPort = c_uint16(port)
        lUserId = cls.sdk.NET_DVR_Login_V40(byref(login_info), byref(device_info))
        return lUserId, device_info


    @classmethod
    def Logout(cls, lUserId: c_long) -> bool:
        """
        用户注销

        Args:
            lUserId (c_long): 用户ID号, NET_DVR_Login_V40等登录接口的返回值 

        Returns:
            bool: TRUE表示成功, FALSE表示失败
        """
        return cls.sdk.NET_DVR_Logout(lUserId)

    @classmethod
    def RealPlay_V40(cls, lUserId: c_long, callbackFun: REALDATACALLBACK) -> int:
        preview_info = NET_DVR_PREVIEWINFO()
        preview_info.hPlayWnd = 0
        preview_info.lChannel = 1          # 通道号
        preview_info.dwStreamType = 0      # 主码流
        preview_info.dwLinkMode = 4        # RTP / RTSP
        preview_info.bBlocked = 0          # 非阻塞取流
        preview_info.byProtoType = 0       # 私有协议

        return cls.sdk.NET_DVR_RealPlay_V40(lUserId, byref(preview_info), callbackFun, None)

    @classmethod
    def StopRealPlay(cls, lRealHandle: c_long) -> bool:
        """
        停止预览

        Args:
            lRealHandle (c_long): 预览句柄, NET_DVR_RealPlay或者NET_DVR_RealPlay_V30的返回值

        Returns:
            bool: TRUE表示成功, FALSE表示失败
        """        
        return cls.sdk.NET_DVR_StopRealPlay(lRealHandle)

    @classmethod
    def GetDVRConfig_PTZ(cls, lUserId: c_long) -> Dict[str, float]:
        """
        获取IP快球PTZ参数

        Args:
            lUserId (c_long): 用户ID号, NET_DVR_Login_V40等登录接口的返回值 

        Returns:
            Dict[str, float]: PTZ参数
        """
        ptz_pos = NET_DVR_PTZPOS()
        bytes_returned = c_long(-1)
        result = cls.sdk.NET_DVR_GetDVRConfig(lUserId, NET_DVR_Command.NET_DVR_GET_PTZPOS, 1, byref(ptz_pos), sizeof(ptz_pos), byref(bytes_returned))
        return {'P': ptz_pos.wPanPos, 'T': ptz_pos.wTiltPos, 'Z': ptz_pos.wZoomPos} if result else {'P': 0.0, 'T': 0.0, 'Z': 0.0}


    # **************************
    # **************************
    # 以下都是PlaySDK的接口
    # **************************
    # **************************

    @classmethod
    def GetPort(cls) -> Tuple[bool, c_long]:
        """
        获取未使用的通道号

        Returns:
            Tuple[bool, c_long]: (result, port)
                result: 成功返回True, 否则返回False
                port: 播放通道号
        """
        port = c_long(-1)
        result = cls.play_sdk.PlayM4_GetPort(byref(port))
        return result, port

    @classmethod
    def ResetBuffer(cls, port, buf_type: int = BufType.BUF_VIDEO_SRC) -> bool:
        """
        清空指定缓冲区的剩余数据

        Args:
            port (c_long): 播放通道号
            buf_type (int, optional): 缓冲区类型. Defaults to BufType.BUF_VIDEO_SRC.

        Returns:
            bool: TRUE表示成功, FALSE表示失败
        """
        return cls.play_sdk.PlayM4_ResetBuffer(port, buf_type)

    @classmethod
    def Play(cls, port: c_long, hwnd: c_void_p = None) -> bool:
        """
        开始播放

        Args:
            port (c_long): 播放通道号
            hwnd (c_void_p, optional): 窗口句柄. Defaults to None.

        Returns:
            bool: TRUE表示成功, FALSE表示失败
        """
        return cls.play_sdk.PlayM4_Play(port, hwnd)

    @classmethod
    def SetStreamOpenMode(cls, port: c_long, mode: int = StreamMode.STREAM_REALTIME) -> bool:
        """
        设置流打开模式

        Args:
            port (c_long): 播放通道号
            mode (int): 打开模式

        Returns:
            bool: TRUE表示成功, FALSE表示失败
        """
        return cls.play_sdk.PlayM4_SetStreamOpenMode(port, mode)

    @classmethod
    def OpenStream(cls, port: c_long, pFileHeadBuf: POINTER(c_byte), nSize: c_long, nBufPoolSize: c_long = 1024 * 1024) -> bool:
        """
        打开流

        Args:
            port (c_long): 播放通道号
            pFileHeadBuf (POINTER): 流数据
            nSize (c_long): 流数据长度
            nBufPoolSize (c_long, optional): 缓冲区大小. Defaults to 1024 * 1024.

        Returns:
            bool: TRUE表示成功, FALSE表示失败
        """
        return cls.play_sdk.PlayM4_OpenStream(port, pFileHeadBuf, nSize, nBufPoolSize)

    @classmethod
    def GetSystemTime(cls, port: c_long) -> str:
        """
        获取当前播放帧的全局时间

        Args:
            port (c_long): 播放通道号

        Returns:
            str: 当前播放帧的全局时间
        """
        sys_time = PLAYM4_SYSTEM_TIME()
        cls.play_sdk.PlayM4_GetSystemTime(port, byref(sys_time))
        return '%04d-%02d-%02d-%02d-%02d-%02d-%06d' % (
            sys_time.dwYear,
            sys_time.dwMon,
            sys_time.dwDay,
            sys_time.dwHour,
            sys_time.dwMin,
            sys_time.dwSec,
            sys_time.dwMs,
        )

    @classmethod
    def SetDecCallBackExMend(cls, port: c_long, cbDecCBFun: DECCBFUNWIN) -> bool:
        """
        设置解码回调函数

        Args:
            port (c_long): 播放通道号
            cbDecCBFun (DECCBFUN): 回调函数

        Returns:
            bool: TRUE表示成功, FALSE表示失败
        """
        return cls.play_sdk.PlayM4_SetDecCallBackExMend(port, cbDecCBFun, None, 0, None)

    @classmethod
    def InputData(cls, port: c_long, pBuf: POINTER(c_byte), nSize: int) -> bool:
        """
        输入流数据

        Args:
            port (c_long): 播放通道号
            pBuf (POINTER): 流数据
            nSize (int): 流数据长度

        Returns:
            bool: TRUE表示成功, FALSE表示失败
        """
        return cls.play_sdk.PlayM4_InputData(port, pBuf, nSize)

    @classmethod
    def Stop(cls, port: c_long) -> bool:
        """
        关闭播放

        Args:
            port (c_long): 播放通道号

        Returns:
            bool: TRUE表示成功, FALSE表示失败
        """
        return cls.play_sdk.PlayM4_Stop(port)

    @classmethod
    def CloseStream(cls, port: c_long) -> bool:
        """
        关闭流

        Args:
            port (c_long): 播放通道号

        Returns:
            bool: TRUE表示成功, FALSE表示失败
        """
        return cls.play_sdk.PlayM4_CloseStream(port)

    @classmethod
    def FreePort(cls, port: c_long) -> bool:
        """
        释放已使用的通道号

        Args:
            port (c_long): 播放通道号

        Returns:
            bool: TRUE表示成功, FALSE表示失败
        """        
        return cls.play_sdk.PlayM4_FreePort(port)

    @classmethod
    def GetDVRConfig_NFS(cls, lUserId: c_long) -> list[dict[str, str]]:
        """
        Get NFS disks configuration

        Args:
            lUserId (c_long): a user id as returned from NET_DVR_Login_V40

        Returns:
            list[dict[str, str]]: A list of NFS disks: [{"host_ip_addr": "...", "directory": "..."}, ...]
        """
        nfs_cfg = NET_DVR_NFSCFG()
        bytes_returned = c_uint()

        ok = cls.sdk.NET_DVR_GetDVRConfig(
            lUserId,
            NET_DVR_Command.NET_DVR_GET_NFSCFG,
            1,
            byref(nfs_cfg),
            sizeof(nfs_cfg),
            byref(bytes_returned),
        )

        return [
            {
                "host_ip_addr": disk.sNfsHostIPAddr.decode(),
                "directory": bytes(disk.sNfsDirectory).decode().split("\x00")[0]
            }
            for disk in nfs_cfg.struNfsDiskParam
        ] if ok else []

    @classmethod
    def SetDVRConfig_NFS(cls, lUserId: c_long, nfs_cfg: list[dict[str, str]]):
        """
        Set NFS disks configuration

        Args:
            lUserId (c_long): a user id as returned from NET_DVR_Login_V40

        Returns:

        """
        # c_byte_Array_128 = ctypes.c_byte * 128
        # NET_DVR_NFSCFG(
        #     dwSize=0,
        #     struNfsDiskParam=[NET_DVR_SINGLE_NFS(b"192.168.1.2", c_byte_Array_128.from_buffer(
        #         ctypes.create_unicode_buffer("/srv/nfs/ici", 128)))],
        # ),

        ok = cls.sdk.NET_DVR_SetDVRConfig(
            lUserId,
            NET_DVR_Command.NET_DVR_SET_NFSCFG,
            1,
            byref(nfs_cfg),
            sizeof(nfs_cfg),
        )
        print(ok)

        return
