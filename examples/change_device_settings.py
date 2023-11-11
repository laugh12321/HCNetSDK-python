import ctypes

import HCNetSDK

sdk = HCNetSDK.NetClient()

sdk.Init()
sdk.SetConnectTime(2000, 3)
sdk.SetReconnect(10000, True)
sdk.SetLogToFile(3)

user_id, device_info = sdk.Login_V40("192.168.1.61", 8000, "admin", "126202cmcc")

nfs_disks = sdk.GetDVRConfig_NFS(user_id)
print(nfs_disks)

sdk.SetDVRConfig_NFS(
    user_id,
    [{}],
)

sdk.Logout(user_id)
