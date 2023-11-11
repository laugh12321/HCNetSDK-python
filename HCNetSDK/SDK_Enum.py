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
# File    :   SDK_Enum.py
# Version :   1.0
# Author  :   laugh12321
# Contact :   laugh12321@vip.qq.com
# Date    :   2023/01/30 10:25:36
# Desc    :   None
# ==============================================================================

from enum import IntEnum


class Macros(IntEnum):
    """
    Macros (starting from HCNetSDK.h:97)
    """
    PATHNAME_LEN = 128


class PTZCommand(IntEnum):
    """
    云台控制命令
    """
    LIGHT_PWRON = 2  # 接通灯光电源
    WIPER_PWRON = 3  # 接通雨刷开关
    FAN_PWRON = 4  # 接通风扇开关
    HEATER_PWRON = 5  # 接通加热器开关
    AUX_PWRON1 = 6  # 接通辅助设备开关
    AUX_PWRON2 = 7  # 接通辅助设备开关
    ZOOM_IN = 11  # 焦距变大(倍率变大)
    ZOOM_OUT = 12  # 焦距变小(倍率变小)
    FOCUS_NEAR = 13  # 焦点前调
    FOCUS_FAR = 14  # 焦点后调
    IRIS_OPEN = 15  # 光圈扩大
    IRIS_CLOSE = 16  # 光圈缩小
    TILT_UP = 21  # 云台上仰
    TILT_DOWN = 22  # 云台下俯
    PAN_LEFT = 23  # 云台左转
    PAN_RIGHT = 24  # 云台右转
    UP_LEFT = 25  # 云台上仰和左转
    UP_RIGHT = 26  # 云台上仰和右转
    DOWN_LEFT = 27  # 云台下俯和左转
    DOWN_RIGHT = 28  # 云台下俯和右转
    PAN_AUTO = 29  # 云台左右自动扫描
    TILT_DOWN_ZOOM_IN = 58  # 云台下俯和焦距变大(倍率变大)
    TILT_DOWN_ZOOM_OUT = 59  # 云台下俯和焦距变小(倍率变小)
    PAN_LEFT_ZOOM_IN = 60  # 云台左转和焦距变大(倍率变大)
    PAN_LEFT_ZOOM_OUT = 61  # 云台左转和焦距变小(倍率变小)
    PAN_RIGHT_ZOOM_IN = 62  # 云台右转和焦距变大(倍率变大)
    PAN_RIGHT_ZOOM_OUT = 63  # 云台右转和焦距变小(倍率变小)
    UP_LEFT_ZOOM_IN = 64  # 云台上仰和左转和焦距变大(倍率变大)
    UP_LEFT_ZOOM_OUT = 65  # 云台上仰和左转和焦距变小(倍率变小)
    UP_RIGHT_ZOOM_IN = 66  # 云台上仰和右转和焦距变大(倍率变大)
    UP_RIGHT_ZOOM_OUT = 67  # 云台上仰和右转和焦距变小(倍率变小)
    DOWN_LEFT_ZOOM_IN = 68  # 云台下俯和左转和焦距变大(倍率变大)
    DOWN_LEFT_ZOOM_OUT = 69  # 云台下俯和左转和焦距变小(倍率变小)
    DOWN_RIGHT_ZOOM_IN = 70  # 云台下俯和右转和焦距变大(倍率变大)
    DOWN_RIGHT_ZOOM_OUT = 71  # 云台下俯和右转和焦距变小(倍率变小)
    TILT_UP_ZOOM_IN = 72  # 云台上仰和焦距变大(倍率变大)
    TILT_UP_ZOOM_OUT = 73  # 云台上仰和焦距变小(倍率变小)


class RealDataType(IntEnum):
    """
    码流回调数据类型
    """
    NET_DVR_SYSHEAD = 1           # 系统头数据
    NET_DVR_STREAMDATA = 2        # 流数据 (包括复合流和音视频分开的视频流数据)
    NET_DVR_AUDIOSTREAMDATA = 3   # 音频数据
    NET_DVR_PRIVATE_DATA = 112    # 私有数据,包括智能信息


class BufType(IntEnum):
    """
    缓冲区类型
    """
    BUF_VIDEO_SRC = 1             # 视频数据源缓冲区,调用后清空库内部所有数据缓冲
    BUF_AUDIO_SRC = 2             # 音频数据源缓冲区
    BUF_VIDEO_RENDER = 3          # 解码后视频缓冲区总节点个数,以帧为单位
    BUF_AUDIO_RENDER = 4          # 解码后音频缓冲区总节点个数,以帧为单位
    BUF_VIDEO_DECODED = 5         # 视频解码缓冲区节点个数,以帧为单位
    BUF_AUDIO_DECODED = 6         # 音频解码缓冲区节点个数,以帧为单位
    BUF_VIDEO_SRC_EX = 7          # 未挂起的视频节点个数 (重置缓冲区需要设定这个参数), 以帧为单位


class StreamMode(IntEnum):
    """
    码流模式
    """
    STREAM_REALTIME = 0           # 实时流
    STREAM_FILE = 1               # 文件流


class NET_DVR_Command(IntEnum):
    """
    设备配置命令, 不同的获取功能对应不同的结构体和命令号
    """
    NET_DVR_GET_TRACK_PARAMCFG = 197              # 获取球机本地菜单规则, 对应结构体 NET_DVR_TRACK_PARAMCFG
    NET_DVR_GET_NFSCFG = 231                      # Sorry cannot write Chinese, this one is for getting NFS storage settings, returns NET_DVR_NFSCFG struct
    NET_DVR_GET_PTZPOS = 293                      # 获取IP快球PTZ参数， 对应结构体 NET_DVR_PTZPOS
    NET_DVR_GET_PTZSCOPE = 294                    # 获取IP快球PTZ范围参数， 对应结构体 NET_DVR_PTZSCOPE
    NET_DVR_GET_MOTION_TRACK_CFG = 3228           # 获取网络球机跟踪参数， 对应结构体 NET_DVR_MOTION_TRACK_CFG
    NET_DVR_GET_BASICPARAMCFG = 3270              # 获取PTZ基本参数信息， 对应结构体 NET_DVR_PTZ_BASICPARAMCFG
    NET_DVR_GET_PTZOSDCFG = 3272                  # 获取PTZ OSD配置参数， 对应结构体 NET_DVR_PTZ_OSDCFG
    NET_DVR_GET_POWEROFFMEMCFG = 3274             # 获取掉电记忆模式参数， 对应结构体 NET_DVR_PTZ_POWEROFFMEMCFG
    NET_DVR_GET_PRIORITIZECFG = 3281              # 获取云台优先配置信息， 对应结构体 NET_DVR_PTZ_PRIORITIZECFG
    NET_DVR_GET_PRIVACY_MASKS_ENABLECFG = 3291    # 获取云台隐私遮蔽全局使能， 对应结构体 NET_DVR_PRIVACY_MASKS_ENABLECFG
    NET_DVR_GET_SMARTTRACKCFG = 3293              # 获取智能运动跟踪配置信息， 对应结构体 NET_DVR_SMARTTRACKCFG
    NET_DVR_GET_PTZ_PARKACTION_CFG = 3314         # 获取云台守望参数， 对应结构体 NET_DVR_PTZ_PARKACTION_CFG
    NET_DVR_GET_SCH_TASK = 3381                   # 获取云台定时任务， 对应结构体 NET_DVR_TIME_TASK
    NET_DVR_GET_SCHEDULE_AUTO_TRACK_CFG = 3400    # 获取定时智能跟踪参数， 对应结构体 NET_DVR_SCHEDULE_AUTO_TRACK_CFG
    NET_DVR_GET_PHY_RATIO = 3606                  # 获取物理倍率坐标信息， 对应结构体 NET_DVR_PHY_RATIO