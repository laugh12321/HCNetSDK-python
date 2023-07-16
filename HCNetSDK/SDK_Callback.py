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
# File    :   SDK_Callback.py
# Version :   1.0
# Author  :   laugh12321
# Contact :   laugh12321@vip.qq.com
# Date    :   2023/01/30 10:05:21
# Desc    :   None
# ==============================================================================

from ctypes import *

from .SDK_Struct import CB_FUNCTYPE, FRAME_INFO, NET_DVR_ALARMER, NET_DVR_DEVICEINFO_V40

# 异步登录回调函数
fLoginResultCallBack = CB_FUNCTYPE(None, c_uint32, c_uint32, POINTER(NET_DVR_DEVICEINFO_V40), c_void_p)

# 报警信息回调函数
MSGCallBack_V31 = CB_FUNCTYPE(c_bool, c_uint32, POINTER(NET_DVR_ALARMER), c_void_p, c_ulong, c_void_p)
MSGCallBack = CB_FUNCTYPE(None, c_uint32, POINTER(NET_DVR_ALARMER), c_void_p, c_ulong, c_void_p)

# 码流回调函数
REALDATACALLBACK = CB_FUNCTYPE(None, c_long, c_ulong, POINTER(c_ubyte), c_ulong, c_void_p)

# 显示回调函数
DISPLAYCBFUN = CB_FUNCTYPE(None, c_long, POINTER(c_char), c_long, c_long, c_long, c_long, c_long, c_long)

# 解码回调函数
DECCBFUNWIN = CB_FUNCTYPE(None, c_long, POINTER(c_char), c_long, POINTER(FRAME_INFO), c_void_p, c_void_p)