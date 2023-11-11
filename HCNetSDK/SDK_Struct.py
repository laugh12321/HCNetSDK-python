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
# File    :   SDK_Struct.py
# Version :   1.0
# Author  :   laugh12321
# Contact :   laugh12321@vip.qq.com
# Date    :   2023/01/30 09:50:10
# Desc    :   None
# ==============================================================================

import os
import platform
from ctypes import *

sys_platform = platform.system().lower().strip()

lib_path_dict = {
    'windows': os.path.dirname(__file__) + '\\Libs\\windows\\',
    'linux': os.path.dirname(__file__) + '/Libs/linux/',
}

netsdkdllpath_dict = {
    'windows': lib_path_dict['windows'] + 'HCNetSDK.dll',
    'linux': lib_path_dict['linux'] + 'libhcnetsdk.so',
}
playsdkdllpath_dict = {
    'windows': lib_path_dict['windows'] + 'PlayCtrl.dll',
    'linux': lib_path_dict['linux'] + 'libPlayCtrl.so',
}
netsdkcomdllpath_dict = {
    'windows': lib_path_dict['windows'] + 'libcrypto-1_1-x64.dll',
    'linux': lib_path_dict['linux'] + 'libcrypto.so.1.1',
}
sslmdllpath_dict = {
    'windows': lib_path_dict['windows'] + 'libssl-1_1-x64.dll',
    'linux': lib_path_dict['linux'] + 'libssl.so.1.1',
}
logdir_dict = {
    'windows' : os.path.dirname(__file__) + '\\Libs\\log',
    'linux': os.path.dirname(__file__) + '/Libs/log',
}

if sys_platform == 'linux':
    load_library = cdll.LoadLibrary
    CB_FUNCTYPE = CFUNCTYPE
elif sys_platform == 'windows':
    load_library = windll.LoadLibrary
    CB_FUNCTYPE = WINFUNCTYPE
else:
    print("************不支持的平台**************")
    exit(0)


netsdkdllpath = netsdkdllpath_dict[sys_platform]
playsdkdllpath = playsdkdllpath_dict[sys_platform]
netsdkcomdllpath = netsdkcomdllpath_dict[sys_platform]
sslmdllpath = sslmdllpath_dict[sys_platform]
logdir = logdir_dict[sys_platform]


class NET_DVR_PTZPOS(Structure):
    _fields_ = [
        ("wAction", c_uint16), # 操作类型，仅在设置时有效。1-定位PTZ参数，2-定位P参数，3-定位T参数，4-定位Z参数，5-定位PT参数
        ("wPanPos", c_uint16), # P参数（水平参数）
        ("wTiltPos", c_uint16), # T参数（垂直参数）
        ("wZoomPos", c_uint16)  # Z参数（变倍参数）
    ]

class NET_DVR_SINGLE_NFS(Structure):
    _fields_ = [
        ("sNfsHostIPAddr", c_char * 16),
        ("sNfsDirectory", c_byte * 16),
    ]


class NET_DVR_NFSCFG(Structure):
    _fields_ = [

    ]


class NET_DVR_DEVICEINFO_V30(Structure):
    _fields_ = [
        ("sSerialNumber", c_byte * 48),  # 序列号
        ("byAlarmInPortNum", c_byte),  # 模拟报警输入个数
        ("byAlarmOutPortNum", c_byte),  # 模拟报警输出个数
        ("byDiskNum", c_byte),  # 硬盘个数
        ("byDVRType", c_byte),  # 设备类型
        ("byChanNum", c_byte),  # 设备模拟通道个数，数字（IP）通道最大个数为byIPChanNum + byHighDChanNum*256
        ("byStartChan", c_byte),  # 模拟通道的起始通道号，从1开始。数字通道的起始通道号见下面参数byStartDChan
        ("byAudioChanNum", c_byte),  # 设备语音对讲通道数
        ("byIPChanNum", c_byte),  # 设备最大数字通道个数，低8位，高8位见byHighDChanNum
        ("byZeroChanNum", c_byte),  # 零通道编码个数
        (
            "byMainProto",
            c_byte,
        ),  # 主码流传输协议类型：0- private，1- rtsp，2- 同时支持私有协议和rtsp协议取流（默认采用私有协议取流）
        (
            "bySubProto",
            c_byte,
        ),  # 子码流传输协议类型：0- private，1- rtsp，2- 同时支持私有协议和rtsp协议取流（默认采用私有协议取流）
        ("bySupport", c_byte),  # 能力，位与结果为0表示不支持，1表示支持
        # bySupport & 0x1，表示是否支持智能搜索
        # bySupport & 0x2，表示是否支持备份
        # bySupport & 0x4，表示是否支持压缩参数能力获取
        # bySupport & 0x8, 表示是否支持双网卡
        # bySupport & 0x10, 表示支持远程SADP
        # bySupport & 0x20, 表示支持Raid卡功能
        # bySupport & 0x40, 表示支持IPSAN目录查找
        # bySupport & 0x80, 表示支持rtp over rtsp
        ("bySupport1", c_byte),  # 能力集扩充，位与结果为0表示不支持，1表示支持
        # bySupport1 & 0x1, 表示是否支持snmp v30
        # bySupport1 & 0x2, 表示是否支持区分回放和下载
        # bySupport1 & 0x4, 表示是否支持布防优先级
        # bySupport1 & 0x8, 表示智能设备是否支持布防时间段扩展
        # bySupport1 & 0x10,表示是否支持多磁盘数（超过33个）
        # bySupport1 & 0x20,表示是否支持rtsp over http
        # bySupport1 & 0x80,表示是否支持车牌新报警信息，且还表示是否支持NET_DVR_IPPARACFG_V40配置
        ("bySupport2", c_byte),  # 能力集扩充，位与结果为0表示不支持，1表示支持
        # bySupport2 & 0x1, 表示解码器是否支持通过URL取流解码
        # bySupport2 & 0x2, 表示是否支持FTPV40
        # bySupport2 & 0x4, 表示是否支持ANR(断网录像)
        # bySupport2 & 0x20, 表示是否支持单独获取设备状态子项
        # bySupport2 & 0x40, 表示是否是码流加密设备
        ("wDevType", c_uint16),  # 设备型号，详见下文列表
        ("bySupport3", c_byte),  # 能力集扩展，位与结果：0- 不支持，1- 支持
        # bySupport3 & 0x1, 表示是否支持多码流
        # bySupport3 & 0x4, 表示是否支持按组配置，具体包含通道图像参数、报警输入参数、IP报警输入/输出接入参数、用户参数、设备工作状态、JPEG抓图、定时和时间抓图、硬盘盘组管理等
        # bySupport3 & 0x20, 表示是否支持通过DDNS域名解析取流
        ("byMultiStreamProto", c_byte),  # 是否支持多码流，按位表示，位与结果：0-不支持，1-支持
        # byMultiStreamProto & 0x1, 表示是否支持码流3
        # byMultiStreamProto & 0x2, 表示是否支持码流4
        # byMultiStreamProto & 0x40,表示是否支持主码流
        # byMultiStreamProto & 0x80,表示是否支持子码流
        ("byStartDChan", c_byte),  # 起始数字通道号，0表示无数字通道，比如DVR或IPC
        ("byStartDTalkChan", c_byte),  # 起始数字对讲通道号，区别于模拟对讲通道号，0表示无数字对讲通道
        ("byHighDChanNum", c_byte),  # 数字通道个数，高8位
        ("bySupport4", c_byte),  # 能力集扩展，按位表示，位与结果：0- 不支持，1- 支持
        # bySupport4 & 0x01, 表示是否所有码流类型同时支持RTSP和私有协议
        # bySupport4 & 0x10, 表示是否支持域名方式挂载网络硬盘
        ("byLanguageType", c_byte),  # 支持语种能力，按位表示，位与结果：0- 不支持，1- 支持
        # byLanguageType ==0，表示老设备，不支持该字段
        # byLanguageType & 0x1，表示是否支持中文
        # byLanguageType & 0x2，表示是否支持英文
        ("byVoiceInChanNum", c_byte),  # 音频输入通道数
        ("byStartVoiceInChanNo", c_byte),  # 音频输入起始通道号，0表示无效
        ("bySupport5", c_byte),  # 按位表示,0-不支持,1-支持,bit0-支持多码流
        ("bySupport6", c_byte),  # 按位表示,0-不支持,1-支持
        # bySupport6 & 0x1  表示设备是否支持压缩
        # bySupport6 & 0x2  表示是否支持流ID方式配置流来源扩展命令，DVR_SET_STREAM_SRC_INFO_V40
        # bySupport6 & 0x4  表示是否支持事件搜索V40接口
        # bySupport6 & 0x8  表示是否支持扩展智能侦测配置命令
        # bySupport6 & 0x40 表示图片查询结果V40扩展
        ("byMirrorChanNum", c_byte),  # 镜像通道个数，录播主机中用于表示导播通道
        ("wStartMirrorChanNo", c_uint16),  # 起始镜像通道号
        ("bySupport7", c_byte),  # 能力,按位表示,0-不支持,1-支持
        # bySupport7 & 0x1  表示设备是否支持NET_VCA_RULECFG_V42扩展
        # bySupport7 & 0x2  表示设备是否支持IPC HVT 模式扩展
        # bySupport7 & 0x04 表示设备是否支持返回锁定时间
        # bySupport7 & 0x08 表示设置云台PTZ位置时，是否支持带通道号
        # bySupport7 & 0x10 表示设备是否支持双系统升级备份
        # bySupport7 & 0x20 表示设备是否支持OSD字符叠加V50
        # bySupport7 & 0x40 表示设备是否支持主从跟踪（从摄像机）
        # bySupport7 & 0x80 表示设备是否支持报文加密
        ("byRes2", c_byte),
    ]  # 保留，置为0


class NET_DVR_DEVICEINFO_V40(Structure):
    _fields_ = [
        ("struDeviceV30", NET_DVR_DEVICEINFO_V30),  # 设备信息
        (
            "bySupportLock",
            c_byte,
        ),  # 设备支持锁定功能，该字段由SDK根据设备返回值来赋值的。bySupportLock为1时，dwSurplusLockTime和byRetryLoginTime有效
        ("byRetryLoginTime", c_byte),  # 剩余可尝试登陆的次数，用户名，密码错误时，此参数有效
        ("byPasswordLevel", c_byte),  # admin密码安全等级
        ("byProxyType", c_byte),  # 代理类型，0-不使用代理, 1-使用socks5代理, 2-使用EHome代理
        ("dwSurplusLockTime", c_uint32),  # 剩余时间，单位秒，用户锁定时，此参数有效
        ("byCharEncodeType", c_byte),  # 字符编码类型
        ("bySupportDev5", c_byte),  # 支持v50版本的设备参数获取，设备名称和设备类型名称长度扩展为64字节
        ("bySupport", c_byte),  # 能力集扩展，位与结果：0- 不支持，1- 支持
        ("byLoginMode", c_byte),  # 登录模式:0- Private登录，1- ISAPI登录
        ("dwOEMCode", c_uint32),  # OEM Code
        (
            "iResidualValidity",
            c_uint32,
        ),  # 该用户密码剩余有效天数，单位：天，返回负值，表示密码已经超期使用，例如“-3表示密码已经超期使用3天”
        ("byResidualValidity", c_byte),  # iResidualValidity字段是否有效，0-无效，1-有效
        (
            "bySingleStartDTalkChan",
            c_byte,
        ),  # 独立音轨接入的设备，起始接入通道号，0-为保留字节，无实际含义，音轨通道号不能从0开始
        ("bySingleDTalkChanNums", c_byte),  # 独立音轨接入的设备的通道总数，0-表示不支持
        ("byPassWordResetLevel", c_byte),  # 0-无效，
        # 1- 管理员创建一个非管理员用户为其设置密码，该非管理员用户正确登录设备后要提示“请修改初始登录密码”，未修改的情况下，用户每次登入都会进行提醒；
        # 2- 当非管理员用户的密码被管理员修改，该非管理员用户再次正确登录设备后，需要提示“请重新设置登录密码”，未修改的情况下，用户每次登入都会进行提醒。
        ("bySupportStreamEncrypt", c_byte),  # 能力集扩展，位与结果：0- 不支持，1- 支持
        # bySupportStreamEncrypt & 0x1 表示是否支持RTP/TLS取流
        # bySupportStreamEncrypt & 0x2 表示是否支持SRTP/UDP取流
        # bySupportStreamEncrypt & 0x4 表示是否支持SRTP/MULTICAST取流
        ("byMarketType", c_byte),  # 0-无效（未知类型）,1-经销型，2-行业型
        ("byRes2", c_byte * 238),  # 保留，置为0
    ]

# 异步登录回调函数
fLoginResultCallBack = CB_FUNCTYPE(None, c_uint32, c_uint32, POINTER(NET_DVR_DEVICEINFO_V40), c_void_p)


class NET_DVR_USER_LOGIN_INFO(Structure):
    _fields_ = [
        ("sDeviceAddress", c_char * 129),  # 设备地址，IP 或者普通域名
        ("byUseTransport", c_byte),  # 是否启用能力集透传：0- 不启用透传，默认；1- 启用透传
        ("wPort", c_uint16),  # 设备端口号，例如：8000
        ("sUserName", c_char * 64),  # 登录用户名，例如：admin
        ("sPassword", c_char * 64),  # 登录密码，例如：12345
        ("cbLoginResult", fLoginResultCallBack),  # 登录状态回调函数，bUseAsynLogin 为1时有效
        ("pUser", c_void_p),  # 用户数据
        ("bUseAsynLogin", c_uint32),  # 是否异步登录：0- 否，1- 是
        ("byProxyType", c_byte),  # 0:不使用代理，1：使用标准代理，2：使用EHome代理
        ("byUseUTCTime", c_byte),
        # 0-不进行转换，默认,1-接口上输入输出全部使用UTC时间,SDK完成UTC时间与设备时区的转换,2-接口上输入输出全部使用平台本地时间，SDK完成平台本地时间与设备时区的转换
        ("byLoginMode", c_byte),  # 0-Private 1-ISAPI 2-自适应
        ("byHttps", c_byte),  # 0-不适用tls，1-使用tls 2-自适应
        ("iProxyID", c_uint32),  # 代理服务器序号，添加代理服务器信息时，相对应的服务器数组下表值
        ("byVerifyMode", c_byte),  # 认证方式，0-不认证，1-双向认证，2-单向认证；认证仅在使用TLS的时候生效;
        ("byRes2", c_byte * 119),
    ]


class NET_DVR_LOCAL_SDK_PATH(Structure):
    _fields_ = [
        ("sPath", c_char * 256),  # 组件库地址
        ("byRes", c_byte * 128),
    ]


class NET_DVR_PREVIEWINFO(Structure):
    _fields_ = [
        ("lChannel", c_uint32),  # 通道号
        (
            "dwStreamType",
            c_uint32,
        ),  # 码流类型，0-主码流，1-子码流，2-码流3，3-码流4, 4-码流5,5-码流6,7-码流7,8-码流8,9-码流9,10-码流10
        (
            "dwLinkMode",
            c_uint32,
        ),  # 0：TCP方式,1：UDP方式,2：多播方式,3 - RTP方式，4-RTP/RTSP,5-RSTP/HTTP ,6- HRUDP（可靠传输） ,7-RTSP/HTTPS
        ("hPlayWnd", c_uint32),  # 播放窗口的句柄,为NULL表示不播放图象
        (
            "bBlocked",
            c_uint32,
        ),  # 0-非阻塞取流, 1-阻塞取流, 如果阻塞SDK内部connect失败将会有5s的超时才能够返回,不适合于轮询取流操作
        ("bPassbackRecord", c_uint32),  # 0-不启用录像回传,1启用录像回传
        ("byPreviewMode", c_ubyte),  # 预览模式，0-正常预览，1-延迟预览
        ("byStreamID", c_ubyte * 32),  # 流ID，lChannel为0xffffffff时启用此参数
        ("byProtoType", c_ubyte),  # 应用层取流协议，0-私有协议，1-RTSP协议,
        # 2-SRTP码流加密（对应此结构体中dwLinkMode 字段，支持如下方式, 为1，表示udp传输方式，信令走TLS加密，码流走SRTP加密，为2，表示多播传输方式，信令走TLS加密，码流走SRTP加密）
        ("byRes1", c_ubyte),
        ("byVideoCodingType", c_ubyte),  # 码流数据编解码类型 0-通用编码数据 1-热成像探测器产生的原始数据
        ("dwDisplayBufNum", c_uint32),  # 播放库播放缓冲区最大缓冲帧数，范围1-50，置0时默认为1
        ("byNPQMode", c_ubyte),  # NPQ是直连模式，还是过流媒体：0-直连 1-过流媒体
        ("byRecvMetaData", c_ubyte),  # 是否接收metadata数据
        # 设备是否支持该功能通过GET /ISAPI/System/capabilities 中DeviceCap.SysCap.isSupportMetadata是否存在且为true
        ("byDataType", c_ubyte),  # 数据类型，0-码流数据，1-音频数据
        ("byRes", c_ubyte * 213),
    ]


class NET_DVR_JPEGPARA(Structure):
    _fields_ = [
        ("wPicSize", c_ushort),
        ("wPicQuality", c_ushort),
    ]


class NET_DVR_SHOWSTRINGINFO(Structure):
    _fields_ = [
        ("wShowString", c_ushort),
        ("wStringSize", c_ushort),
        ("wShowStringTopLeftX", c_ushort),
        ("wShowStringTopLeftY", c_ushort),
        ("sString", c_ubyte * 44),
    ]


class NET_DVR_SHOWSTRING_V30(Structure):
    _fields_ = [
        ("dwSize", c_uint32),
        ("struStringInfo", NET_DVR_SHOWSTRINGINFO * 8),
    ]


class NET_DVR_XML_CONFIG_OUTPUT(Structure):
    _fields_ = [
        ("dwSize", c_uint32),
        ("lpOutBuffer", c_void_p),
        ("dwOutBufferSize", c_uint32),
        ("dwReturnedXMLSize", c_uint32),
        ("lpStatusBuffer", c_void_p),
        ("dwStatusSize", c_uint32),
        ("byRes", c_ubyte * 32),
    ]


class NET_DVR_XML_CONFIG_INPUT(Structure):
    _fields_ = [
        ("dwSize", c_uint32),
        ("lpRequestUrl", c_void_p),
        ("dwRequestUrlLen", c_uint32),
        ("lpInBuffer", c_void_p),
        ("dwInBufferSize", c_uint32),
        ("dwRecvTimeOut", c_uint32),
        ("byForceEncrpt", c_ubyte),
        ("byNumOfMultiPart", c_ubyte),
        ("byRes", c_ubyte * 30),
    ]


class NET_DVR_ALARMER(Structure):
    _fields_ = [
        ("byUserIDValid", c_byte),  # UserID是否有效 0-无效，1-有效
        ("bySerialValid", c_byte),  # 序列号是否有效 0-无效，1-有效
        ("byVersionValid", c_byte),  # 版本号是否有效 0-无效，1-有效
        ("byDeviceNameValid", c_byte),  # 设备名字是否有效 0-无效，1-有效
        ("byMacAddrValid", c_byte),  # MAC地址是否有效 0-无效，1-有效
        ("byLinkPortValid", c_byte),  # login端口是否有效 0-无效，1-有效
        ("byDeviceIPValid", c_byte),  # 设备IP是否有效 0-无效，1-有效
        ("bySocketIPValid", c_byte),  # socket ip是否有效 0-无效，1-有效
        ("lUserID", c_uint32),  # NET_DVR_Login()返回值, 布防时有效
        ("sSerialNumber", c_byte * 48),  # 序列号
        ("dwDeviceVersion", c_uint32),  # 版本信息 高16位表示主版本，低16位表示次版本
        ("sDeviceName", c_byte * 32),  # 设备名字
        ("byMacAddr", c_byte * 6),  # MAC地址
        ("wLinkPort", c_uint16),  # link port
        ("sDeviceIP", c_byte * 128),  # IP地址
        ("sSocketIP", c_byte * 128),  # 报警主动上传时的socket IP地址
        ("byIpProtocol", c_byte),  # Ip协议 0-IPV4, 1-IPV6
        ("byRes2", c_byte * 11),
    ]


class NET_DVR_SETUPALARM_PARAM(Structure):
    _fields_ = [
        ("dwSize", c_uint32),  # 结构体大小
        ("byLevel", c_byte),  # 布防优先级：0- 一等级（高），1- 二等级（中），2- 三等级（低）
        ("byAlarmInfoType", c_byte),
        # 上传报警信息类型（抓拍机支持），0-老报警信息（NET_DVR_PLATE_RESULT），1-新报警信息(NET_ITS_PLATE_RESULT)2012-9-28
        ("byRetAlarmTypeV40", c_byte),
        # 0- 返回NET_DVR_ALARMINFO_V30或NET_DVR_ALARMINFO,
        # 1- 设备支持NET_DVR_ALARMINFO_V40则返回NET_DVR_ALARMINFO_V40，不支持则返回NET_DVR_ALARMINFO_V30或NET_DVR_ALARMINFO
        (
            "byRetDevInfoVersion",
            c_byte,
        ),  # CVR上传报警信息回调结构体版本号 0-COMM_ALARM_DEVICE， 1-COMM_ALARM_DEVICE_V40
        (
            "byRetVQDAlarmType",
            c_byte,
        ),  # VQD报警上传类型，0-上传报报警NET_DVR_VQD_DIAGNOSE_INFO，1-上传报警NET_DVR_VQD_ALARM
        ("byFaceAlarmDetection", c_byte),
        ("bySupport", c_byte),
        ("byBrokenNetHttp", c_byte),
        ("wTaskNo", c_uint16),
        # 任务处理号 和 (上传数据NET_DVR_VEHICLE_RECOG_RESULT中的字段dwTaskNo对应 同时 下发任务结构 NET_DVR_VEHICLE_RECOG_COND中的字段dwTaskNo对应)
        ("byDeployType", c_byte),  # 布防类型：0-客户端布防，1-实时布防
        ("byRes1", c_byte * 3),
        ("byAlarmTypeURL", c_byte),
        # bit0-表示人脸抓拍报警上传
        # 0-表示二进制传输，1-表示URL传输（设备支持的情况下，设备支持能力根据具体报警能力集判断,同时设备需要支持URL的相关服务，当前是”云存储“）
        ("byCustomCtrl", c_byte),
    ]  # Bit0- 表示支持副驾驶人脸子图上传: 0-不上传,1-上传


class NET_DVR_ALARMINFO_V30(Structure):
    _fields_ = [
        ("dwAlarmType", c_uint32),  # 报警类型
        ("dwAlarmInputNumber", c_uint32),  # 报警输入端口，当报警类型为0、23时有效
        ("byAlarmOutputNumber", c_byte * 96),
        # 触发的报警输出端口，值为1表示该报警端口输出，如byAlarmOutputNumber[0]=1表示触发第1个报警输出口输出，byAlarmOutputNumber[1]=1表示触发第2个报警输出口，依次类推
        (
            "byAlarmRelateChannel",
            c_byte * 64,
        ),  # 触发的录像通道，值为1表示该通道录像，如byAlarmRelateChannel[0]=1表示触发第1个通道录像
        (
            "byChannel",
            c_byte * 64,
        ),  # 发生报警的通道。当报警类型为2、3、6、9、10、11、13、15、16时有效，如byChannel[0]=1表示第1个通道报警
        ("byDiskNumber", c_byte * 33),
    ]  # 发生报警的硬盘。当报警类型为1，4，5时有效，byDiskNumber[0]=1表示1号硬盘异常


class NET_DVR_SETUPALARM_PARAM(Structure):
    _fields_ = [
        ("dwSize", c_uint32),  # 结构体大小
        ("byLevel", c_byte),  # 布防优先级：0- 一等级（高），1- 二等级（中），2- 三等级（低）
        ("byAlarmInfoType", c_byte),
        # 上传报警信息类型（抓拍机支持），0-老报警信息（NET_DVR_PLATE_RESULT），1-新报警信息(NET_ITS_PLATE_RESULT)2012-9-28
        ("byRetAlarmTypeV40", c_byte),
        # 0- 返回NET_DVR_ALARMINFO_V30或NET_DVR_ALARMINFO,
        # 1- 设备支持NET_DVR_ALARMINFO_V40则返回NET_DVR_ALARMINFO_V40，不支持则返回NET_DVR_ALARMINFO_V30或NET_DVR_ALARMINFO
        (
            "byRetDevInfoVersion",
            c_byte,
        ),  # CVR上传报警信息回调结构体版本号 0-COMM_ALARM_DEVICE， 1-COMM_ALARM_DEVICE_V40
        (
            "byRetVQDAlarmType",
            c_byte,
        ),  # VQD报警上传类型，0-上传报报警NET_DVR_VQD_DIAGNOSE_INFO，1-上传报警NET_DVR_VQD_ALARM
        ("byFaceAlarmDetection", c_byte),
        ("bySupport", c_byte),
        ("byBrokenNetHttp", c_byte),
        ("wTaskNo", c_uint16),
        # 任务处理号 和 (上传数据NET_DVR_VEHICLE_RECOG_RESULT中的字段dwTaskNo对应 同时 下发任务结构 NET_DVR_VEHICLE_RECOG_COND中的字段dwTaskNo对应)
        ("byDeployType", c_byte),  # 布防类型：0-客户端布防，1-实时布防
        ("byRes1", c_byte * 3),
        ("byAlarmTypeURL", c_byte),
        # bit0-表示人脸抓拍报警上传
        # 0- 表示二进制传输，1- 表示URL传输（设备支持的情况下，设备支持能力根据具体报警能力集判断,同时设备需要支持URL的相关服务，当前是”云存储“）
        ("byCustomCtrl", c_byte),
    ]  # Bit0- 表示支持副驾驶人脸子图上传: 0-不上传,1-上传,(注：只在公司内部8600/8200等平台开放)


class NET_DVR_TIME(Structure):
    _fields_ = [
        ("dwYear", c_uint32),  # 年
        ("dwMonth", c_uint32),  # 月
        ("dwDay", c_uint32),  # 日
        ("dwHour", c_uint32),  # 时
        ("dwMinute", c_uint32),  # 分
        ("dwSecond", c_uint32), # 秒
    ]  


class NET_DVR_IPADDR(Structure):
    _fields_ = [
        ("sIpV4", c_byte * 16),  # 设备IPv4地址 
        ("sIpV6", c_byte * 128), # 设备IPv6地址
    ]


class NET_DVR_ACS_EVENT_INFO(Structure):
    _fields_ = [
        ("dwSize", c_uint32),  # 结构体大小
        ("byCardNo", c_byte * 32),  # 卡号
        (
            "byCardType",
            c_byte,
        ),  # 卡类型：1- 普通卡，2- 残障人士卡，3- 黑名单卡，4- 巡更卡，5- 胁迫卡，6- 超级卡，7- 来宾卡，8- 解除卡，为0表示无效
        ("byAllowListNo", c_byte),  # 白名单单号，取值范围：1~8，0表示无效
        ("byReportChannel", c_byte),  # 报告上传通道：1- 布防上传，2- 中心组1上传，3- 中心组2上传，0表示无效
        ("byCardReaderKind", c_byte),  # 读卡器类型：0- 无效，1- IC读卡器，2- 身份证读卡器，3- 二维码读卡器，4- 指纹头
        ("dwCardReaderNo", c_uint32),  # 读卡器编号，为0表示无效
        ("dwDoorNo", c_uint32),  # 门编号（或者梯控的楼层编号），为0表示无效（当接的设备为人员通道设备时，门1为进方向，门2为出方向）
        ("dwVerifyNo", c_uint32),  # 多重卡认证序号，为0表示无效
        ("dwAlarmInNo", c_uint32),  # 报警输入号，为0表示无效
        ("dwAlarmOutNo", c_uint32),  # 报警输出号，为0表示无效
        ("dwCaseSensorNo", c_uint32),  # 事件触发器编号
        ("dwRs485No", c_uint32),  # RS485通道号，为0表示无效
        ("dwMultiCardGroupNo", c_uint32),  # 群组编号
        ("wAccessChannel", c_uint16),  # 人员通道号
        ("byDeviceNo", c_byte),  # 设备编号，为0表示无效
        ("byDistractControlNo", c_byte),  # 分控器编号，为0表示无效
        ("dwEmployeeNo", c_uint32),  # 工号，为0无效
        ("wLocalControllerID", c_uint16),  # 就地控制器编号，0-门禁主机，1-255代表就地控制器
        ("byInternetAccess", c_byte),  # 网口ID：（1-上行网口1,2-上行网口2,3-下行网口1）
        ("byType", c_byte),
        # 防区类型，0:即时防区,1-24小时防区,2-延时防区,3-内部防区,4-钥匙防区,5-火警防区,6-周界防区,7-24小时无声防区,
        # 8-24小时辅助防区,9-24小时震动防区,10-门禁紧急开门防区,11-门禁紧急关门防区，0xff-无
        ("byMACAddr", c_byte * 6),  # 物理地址，为0无效
        ("bySwipeCardType", c_byte),  # 刷卡类型，0-无效，1-二维码
        ("byMask", c_byte),  # 是否带口罩：0-保留，1-未知，2-不戴口罩，3-戴口罩
        ("dwSerialNo", c_uint32),  # 事件流水号，为0无效
        ("byChannelControllerID", c_byte),  # 通道控制器ID，为0无效，1-主通道控制器，2-从通道控制器
        ("byChannelControllerLampID", c_byte),  # 通道控制器灯板ID，为0无效（有效范围1-255）
        ("byChannelControllerIRAdaptorID", c_byte),  # 通道控制器红外转接板ID，为0无效（有效范围1-255）
        ("byChannelControllerIREmitterID", c_byte),  # 通道控制器红外对射ID，为0无效（有效范围1-255）
        ("byHelmet", c_byte),  # 可选，是否戴安全帽：0-保留，1-未知，2-不戴安全, 3-戴安全帽
        ("byRes", c_byte * 3),
    ]  # 保留，置为0


class NET_DVR_ACS_ALARM_INFO(Structure):
    _fields_ = [
        ("dwSize", c_uint32),  # 结构体大小
        ("dwMajor", c_uint32),  # 报警主类型，具体定义见“Remarks”说明
        ("dwMinor", c_uint32),  # 报警次类型，次类型含义根据主类型不同而不同，具体定义见“Remarks”说明
        ("struTime", NET_DVR_TIME),  # 报警时间
        ("sNetUser", c_byte * 16),  # 网络操作的用户名
        ("struRemoteHostAddr", NET_DVR_IPADDR),  # 远程主机地址
        ("struAcsEventInfo", NET_DVR_ACS_EVENT_INFO),  # 报警信息详细参数
        ("dwPicDataLen", c_uint32),  # 图片数据大小，不为0是表示后面带数据
        ("pPicData", c_void_p),  # 图片数据缓冲区
        (
            "wInductiveEventType",
            c_uint16,
        ),  # 归纳事件类型，0-无效，客户端判断该值为非0值后，报警类型通过归纳事件类型区分，否则通过原有报警主次类型（dwMajor、dwMinor）区分
        ("byPicTransType", c_byte),  # 图片数据传输方式: 0-二进制；1-url
        ("byRes1", c_byte),  # 保留，置为0
        ("dwIOTChannelNo", c_uint32),  # IOT通道号
        (
            "pAcsEventInfoExtend",
            c_void_p,
        ),  # byAcsEventInfoExtend为1时，表示指向一个NET_DVR_ACS_EVENT_INFO_EXTEND结构体
        ("byAcsEventInfoExtend", c_byte),  # pAcsEventInfoExtend是否有效：0-无效，1-有效
        ("byTimeType", c_byte),  # 时间类型：0-设备本地时间，1-UTC时间（struTime的时间）
        ("byRes2", c_byte),  # 保留，置为0
        ("byAcsEventInfoExtendV20", c_byte),  # pAcsEventInfoExtendV20是否有效：0-无效，1-有效
        (
            "pAcsEventInfoExtendV20",
            c_void_p,
        ),  # byAcsEventInfoExtendV20为1时，表示指向一个NET_DVR_ACS_EVENT_INFO_EXTEND_V20结构体
        ("byRes", c_byte * 4),
    ]  # 保留，置为0


class NET_VCA_POINT(Structure):
    _fields_ = [("fX", c_float), ("fY", c_float)]


class NET_DVR_ID_CARD_INFO_EXTEND(Structure):
    _fields_ = [
        ("byRemoteCheck", c_ubyte),
        ("byThermometryUnit", c_ubyte),
        ("byIsAbnomalTemperature", c_ubyte),
        ("byRes2", c_ubyte),
        ("fCurrTemperature", c_float),
        ("struRegionCoordinates", NET_VCA_POINT),
        ("dwQRCodeInfoLen", c_uint32),
        ("dwVisibleLightDataLen", c_uint32),
        ("dwThermalDataLen", c_uint32),
        ("pQRCodeInfo", POINTER(c_byte)),
        ("pVisibleLightData", POINTER(c_byte)),
        ("pThermalData", POINTER(c_byte)),
        ("byRes", c_ubyte * 1024),
    ]


class NET_DVR_DATE(Structure):
    _fields_ = [("wYear", c_ushort), ("byMonth", c_ubyte), ("byDay", c_ubyte)]


class NET_DVR_ID_CARD_INFO(Structure):
    _fields_ = [
        ("dwSize", c_uint),
        ("byName", c_ubyte * 128),
        ("struBirth", NET_DVR_DATE),
        ("byAddr", c_ubyte * 280),
        ("byIDNum", c_ubyte * 32),
        ("byIssuingAuthority", c_ubyte * 128),
        ("struStartDate", NET_DVR_DATE),
        ("struEndDate", NET_DVR_DATE),
        ("byTermOfValidity", c_ubyte),
        ("bySex", c_ubyte),
        ("byNation", c_ubyte),
        ("byRes", c_ubyte * 101),
    ]


class NET_DVR_TIME(Structure):
    _fields_ = [
        ("dwYear", c_uint32),
        ("dwMonth", c_uint32),
        ("dwDay", c_uint32),
        ("dwHour", c_uint32),
        ("dwMinute", c_uint32),
        ("dwSecond", c_uint32),
    ]


class NET_DVR_TIME_V30(Structure):
    _fields_ = [
        ("wYear", c_ushort),
        ("byMonth", c_ubyte),
        ("byDay", c_ubyte),
        ("byHour", c_ubyte),
        ("byMinute", c_ubyte),
        ("bySecond", c_ubyte),
        ("byISO8601", c_ubyte),
        ("wMilliSec", c_ushort),
        ("cTimeDifferenceH", c_ubyte),
        ("cTimeDifferenceM", c_ubyte),
    ]


class NET_DVR_IPADDR(Structure):
    _fields_ = [("sIpV4", c_ubyte * 16), ("byIPv6", c_ubyte * 128)]


class NET_DVR_ID_CARD_INFO_ALARM(Structure):
    _fields_ = [
        ("dwSize", c_uint32),  # 结构长度
        ("struIDCardCfg", NET_DVR_ID_CARD_INFO),  # 身份证信息
        ("dwMajor", c_uint32),  # 报警主类型，参考宏定义
        ("dwMinor", c_uint32),  # 报警次类型，参考宏定义
        ("struSwipeTime", NET_DVR_TIME_V30),  # 刷卡时间
        ("byNetUser", c_ubyte * 16),  # 网络操作的用户名
        ("struRemoteHostAddr", NET_DVR_IPADDR),  # 远程主机地址
        ("dwCardReaderNo", c_uint32),  # 读卡器编号，为0无效
        ("dwDoorNo", c_uint32),  # 门编号，为0无效
        ("dwPicDataLen", c_uint32),  # 图片数据大小，不为0是表示后面带数据
        ("pPicData", c_void_p),  # 身份证图片数据缓冲区，dwPicDataLen不为0时缓冲区里面存放身份证头像的图片数据
        (
            "byCardType",
            c_ubyte,
        ),  # 卡类型，1-普通卡，2-残疾人卡，3-黑名单卡，4-巡更卡，5-胁迫卡，6-超级卡，7-来宾卡，8-解除卡，为0无效
        ("byDeviceNo", c_ubyte),  # 设备编号，为0时无效（有效范围1-255）
        ("byMask", c_ubyte),  # 是否带口罩：0-保留，1-未知，2-不戴口罩，3-戴口罩
        ("byRes2", c_ubyte),  # 保留，置为0
        ("dwFingerPrintDataLen", c_uint32),  # 指纹数据大小，不为0是表示后面带数据
        ("pFingerPrintData", c_void_p),  # 指纹数据缓冲区，dwFingerPrintDataLen不为0时缓冲区里面存放指纹数据
        ("dwCapturePicDataLen", c_uint32),  # 抓拍图片数据大小，不为0是表示后面带数据
        (
            "pCapturePicData",
            c_void_p,
        ),  # 抓拍图片数据缓冲区，dwCapturePicDataLen不为0时缓冲区里面存放设备上摄像机抓拍上传的图片数据
        ("dwCertificatePicDataLen", c_uint32),  # 证件抓拍图片数据大小，不为0是表示后面带数据
        (
            "pCertificatePicData",
            c_void_p,
        ),  # 证件抓拍图片数据缓冲区，dwCertificatePicDataLen不为0时缓冲区里面存放设备上摄像机抓拍上传的证件抓拍图片数据
        ("byCardReaderKind", c_ubyte),  # 读卡器属于哪一类：0-无效，1-IC读卡器，2-身份证读卡器，3-二维码读卡器，4-指纹头
        ("byRes3", c_ubyte * 2),  # 保留，置为0
        ("byIDCardInfoExtend", c_ubyte),  # pIDCardInfoExtend是否有效：0-无效，1-有效
        ("pIDCardInfoExtend", POINTER(NET_DVR_ID_CARD_INFO_EXTEND)),  # 身份证刷卡扩展事件信息
        ("byRes", c_ubyte * 172),  # 身份证刷卡扩展事件信息
    ]


class NET_DVR_ALARM_ISAPI_PICDATA(Structure):
    _fields_ = [
        ("dwPicLen", c_uint32),  # 图片数据长度
        ("byPicType", c_ubyte),  # 图片格式: 1- jpg
        ("byRes", c_ubyte * 3),  #
        ("szFilename", c_ubyte * 256),  # 图片名称
        ("pPicData", c_void_p),  # 图片数据
    ]


class NET_DVR_ALARM_ISAPI_INFO(Structure):
    _fields_ = [
        ("pAlarmData", c_void_p),  # 报警数据
        ("dwAlarmDataLen", c_uint32),  # 报警数据长度
        ("byDataType", c_ubyte),  # 0-invalid,1-xml,2-json
        ("byPicturesNumber", c_ubyte),  # 图片数量
        ("byRes[2]", c_ubyte * 2),  # 保留字节
        ("pPicPackData", c_void_p),  # 图片变长部分
        ("byRes1[32]", c_ubyte * 32),  # 保留字节
    ]


class NET_DVR_LOCAL_GENERAL_CFG(Structure):
    _fields_ = [
        ("byExceptionCbDirectly", c_ubyte),  # 0-通过线程池异常回调，1-直接异常回调给上层
        ("byNotSplitRecordFile", c_ubyte),  # 回放和预览中保存到本地录像文件不切片 0-默认切片，1-不切片
        ("byResumeUpgradeEnable", c_ubyte),  # 断网续传升级使能，0-关闭（默认），1-开启
        (
            "byAlarmJsonPictureSeparate",
            c_ubyte,
        ),  # 控制JSON透传报警数据和图片是否分离，0-不分离，1-分离（分离后走COMM_ISAPI_ALARM回调返回）
        ("byRes", c_ubyte * 4),  # 保留
        ("i64FileSize", c_uint64),  # 单位：Byte
        ("dwResumeUpgradeTimeout", c_uint32),  # 断网续传重连超时时间，单位毫秒
        ("byAlarmReconnectMode", c_ubyte),  # 0-独立线程重连（默认） 1-线程池重连
        ("byStdXmlBufferSize", c_ubyte),  # 设置ISAPI透传接收缓冲区大小，1-1M 其他-默认
        ("byMultiplexing", c_ubyte),  # 0-普通链接（非TLS链接）关闭多路复用，1-普通链接（非TLS链接）开启多路复用
        ("byFastUpgrade", c_ubyte),  # 0-正常升级，1-快速升级
        ("byRes1", c_ubyte * 232),  # 预留
    ]


class FRAME_INFO(Structure):
    _fields_ = [
        ('nWidth', c_uint32),
        ('nHeight', c_uint32),
        ('nStamp', c_uint32),
        ('nType', c_uint32),
        ('nFrameRate', c_uint32),
        ('dwFrameNum', c_uint32)
    ]


class PLAYM4_SYSTEM_TIME(Structure):
    _fields_ = [
        ("dwYear", c_uint32),
        ("dwMon", c_uint32),
        ("dwDay", c_uint32),
        ("dwHour", c_uint32),
        ("dwMin", c_uint32),
        ("dwSec", c_uint32),
        ("dwMs", c_uint32),
    ]