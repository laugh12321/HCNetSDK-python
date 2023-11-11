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
    [
        {'host_ip_addr': '192.168.1.2', 'directory': '/srv/nfs/ici'},
        {'host_ip_addr': '0.0.0.0', 'directory': ''},
        {'host_ip_addr': '0.0.0.0', 'directory': ''},
        {'host_ip_addr': '0.0.0.0', 'directory': ''},
        {'host_ip_addr': '0.0.0.0', 'directory': ''},
        {'host_ip_addr': '0.0.0.0', 'directory': ''},
        {'host_ip_addr': '0.0.0.0', 'directory': ''},
        {'host_ip_addr': '0.0.0.0', 'directory': ''}
    ],
)

sdk.Logout(user_id)
