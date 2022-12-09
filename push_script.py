from ppadb.client import Client as AdbClient
# Default is "127.0.0.1" and 5037
client = AdbClient(host="127.0.0.1", port=5037)

#connect to device
devices = client.devices()
if len(devices) == 0:
    print("No devices attached")
    quit()
device = devices[0]
device.push("client_usb.py", "/sdcard/PythonChat/client_usb.py")
