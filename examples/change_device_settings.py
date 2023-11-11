import HCNetSDK
from ctypes import *


client = HCNetSDK.NetClient()
sdk = client.sdk

client.Init()
client.SetConnectTime(2000, 3)
client.SetReconnect(10000, True)
client.SetLogToFile(3)

user_id, device_info = client.Login_V40("192.168.1.61", 8000, "admin", "126202cmcc")

buf = create_string_buffer(2048)
bytes_returned = c_uint()
sdk.NET_DVR_GetDVRConfig(
    user_id,
    HCNetSDK.NET_DVR_Command.NET_DVR_GET_NFSCFG,
    1,
    byref(buf),
    sizeof(buf),
    byref(bytes_returned),
)
print(bytes_returned)
print(repr(buf.raw))


# sdk.sdk.NET_DVR_SetDVRConfig
# sdk.sdk.NET_DVR_GetDeviceConfig(user_id, sdk.sdk.)
# sdk.NET_DVR_SetDeviceConfig
# sdk.sdk.NET_DVR_GetTransparentParam(user_id, )
# sdk.NET_DVR_SetTransparentParam


client.Logout(user_id)
