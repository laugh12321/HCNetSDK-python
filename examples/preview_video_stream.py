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
# File    :   preview_video_stream.py
# Version :   1.0
# Author  :   laugh12321
# Contact :   laugh12321@vip.qq.com
# Date    :   2023/07/16 14:42:54
# Desc    :   预览视频流
# ==============================================================================


from collections import deque

import av
import numpy as np
from loguru import logger

from HCNetSDK import *


class HIKVISION:

    """
    海康威视类

    Args:
        deque_maxlen (int, optional): 队列最大长度. Defaults to 25.
        skip_interval (int, optional): 跳帧间隔. Defaults to 1.
    """

    def __init__(self, deque_maxlen: int = 25, skip_interval: int = 2) -> None:
        # 获取NetSDK对象并初始化
        self.sdk = NetClient()
        self.sdk.Init()
        self.sdk.SetConnectTime(2000, 3)
        self.sdk.SetReconnect(10000, True)
        self.sdk.SetLogToFile(3)
        self.skip_interval = skip_interval         # 跳帧间隔
        self.skip_frame_count = 0                  # 记录已跳过的帧数
        self.cache = deque(maxlen=deque_maxlen)    # 缓存队列

    def login(self, ip: str, username: str, password: str, port: int = 8000) -> bool:
        """
        设备登录

        Args:
            ip (str): ip
            username (str): 用户名
            password (str): 密码
            port (int, optional): 端口号. Defaults to 8000.

        Returns:
            bool: 是否登录成功
        """        
        self.lUserId, device_info = self.sdk.Login_V40(
            ip=ip,
            port=port,
            username=username,
            password=password,
        )

        if self.lUserId < 0:
            self.sdk.Cleanup()
            return False
        return True

    def logout(self) -> None:
        """
        设备登出
        """        
        self.sdk.Logout(self.lUserId)
        self.sdk.Cleanup()

    def play(self) -> bool:
        """
        实时播放

        Returns:
            bool: 是否播放成功
        """
        # 获取播放句柄
        sucess, self.Port = self.sdk.GetPort()
        if not sucess: return False

        # 清空缓冲区
        self.sdk.ResetBuffer(self.Port)
        # 开始预览并且设置回调函数回调获取实时流数据
        self.funcRealDataCallBack_V30 = REALDATACALLBACK(self.__realdata_callback)
        self.lRealPlayHandle = self.sdk.RealPlay_V40(self.lUserId, self.funcRealDataCallBack_V30)
        return self.lRealPlayHandle >= 0

    def stop(self) -> None:
        """
        播放停止
        """        
        if self.lRealPlayHandle >= 0:
            self.sdk.StopRealPlay(self.lRealPlayHandle)
        if self.Port.value >= 0:
            self.sdk.Stop(self.Port)
            self.sdk.CloseStream(self.Port)
            self.sdk.FreePort(self.Port)

    def frameinfo(self) -> dict or None:
        """
        获取帧信息

        Returns:
            dict or None: 帧信息
        """
        return self.cache.pop() if len(self.cache) > 0 else None

    def __realdata_callback(self, lPlayHandle, dwDataType, pBuffer, dwBufSize, pUser) -> None:
        """
        码流回调函数
        """
        if dwDataType == RealDataType.NET_DVR_SYSHEAD:
            # 设置流播放模式
            self.sdk.SetStreamOpenMode(self.Port)
            # 打开码流，送入40字节系统头数据
            if self.sdk.OpenStream(self.Port, pBuffer, dwBufSize):
                # 设置解码回调，可以返回解码后YUV视频数据
                self.FuncDecCB = DECCBFUNWIN(self.__decode_callback)
                self.sdk.SetDecCallBackExMend(self.Port, self.FuncDecCB)
                # 开始解码播放
                if self.sdk.Play(self.Port):
                    logger.success('播放库播放成功')
                else:
                    logger.error('播放库播放成功')
            else:
                logger.error('播放库打开流失败')
        elif dwDataType == RealDataType.NET_DVR_STREAMDATA:
            self.sdk.InputData(self.Port, pBuffer, dwBufSize)
        else:
            logger.warning('其他数据,长度: %s', dwBufSize)

    def __decode_callback(self, nPort, pBuf, nSize, pFrameInfo, nUser, nReserved2) -> None:
        """
        解码回调函数
        """
        timestamp = self.sdk.GetSystemTime(self.Port)
        if pFrameInfo.contents.nType == 3 and (eval(timestamp[:4]) != 0):
            # 解码返回视频YUV数据，将YUV数据转成jpg图片保存到本地
            # 如果有耗时处理，需要将解码数据拷贝到回调函数外面的其他线程里面处理，避免阻塞回调导致解码丢帧
            self.skip_frame_count += 1
            if self.skip_frame_count >= self.skip_interval:
                self.skip_frame_count = 0
                self.__yuv2rgb4ffmpeg(pFrameInfo, pBuf, nSize, timestamp)

    def __yuv2rgb4ffmpeg(self, pFrameInfo, pBuf, nSize, timestamp) -> None:
        width = pFrameInfo.contents.nWidth
        height = pFrameInfo.contents.nHeight
        pYUV = np.frombuffer(pBuf[:nSize], dtype=np.uint8).reshape((height + height // 2, width))
        frame_yuv = av.VideoFrame.from_ndarray(pYUV, format='yuv420p')
        frame_bgr = frame_yuv.to_rgb().to_ndarray()
        self.cache.append(
            {
                'frame': frame_bgr,
                'timestamp': timestamp,
                'framenum': pFrameInfo.contents.dwFrameNum,
                'framerate': pFrameInfo.contents.nFrameRate,
            },
        )


def preview_video_stream(
    ip: str, 
    username: str, 
    password: str, 
    port: int = 8000, 
    skip_interval: int = 1, 
    deque_maxlen: int = 25,
    ) -> None:
    """
    预览视频流

    Args:
        ip (str): ip
        username (str): 用户名
        password (str): 密码
        port (int, optional): 端口号. Defaults to 8000.
        skip_interval (int, optional): 跳帧间隔. Defaults to 1.
        deque_maxlen (int, optional): 队列最大长度. Defaults to 25.
    """
    import cv2

    client = HIKVISION(deque_maxlen=deque_maxlen, skip_interval=skip_interval)
    if (client.login(ip=ip, username=username, password=password, port=port) and client.play()):
        while True:
            if (value := client.frameinfo()) is not None:
                logger.info(f'{value["framenum"]}-{value["timestamp"]}')
                cv2.imshow('frame', value['frame'])
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    client.stop()
                    client.logout()
                    break


if __name__ == '__main__':
    import concurrent

    client_params = [
        {
            'ip': 'camera_ip',
            'username': 'username',
            'password': 'password',
        },
        {
            'ip': 'camera_ip',
            'username': 'username',
            'password': 'password',
        }
    ]

    with concurrent.futures.ProcessPoolExecutor(max_workers=2) as executor:
        futures = [executor.submit(preview_video_stream, **params) for params in client_params]
        concurrent.futures.wait(futures)