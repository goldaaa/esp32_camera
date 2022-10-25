import time
import network


import camera
camera.init(0, format=camera.JPEG)
camera.flip(1)
camera.mirror(1)
def photo(framesize=camera.FRAME_HD,
          special_effects=camera.EFFECT_NONE,
          white_balance=camera.WB_NONE,
          saturation=0, brightness=0, contrast=0, quality=10,
          ):
    camera.framesize(framesize)
    # The options are the following:
    # FRAME_96X96 FRAME_QQVGA FRAME_QCIF FRAME_HQVGA FRAME_240X240
    # FRAME_QVGA FRAME_CIF FRAME_HVGA FRAME_VGA FRAME_SVGA
    # FRAME_XGA FRAME_HD FRAME_SXGA FRAME_UXGA FRAME_FHD
    # FRAME_P_HD FRAME_P_3MP FRAME_QXGA FRAME_QHD FRAME_WQXGA
    # FRAME_P_FHD FRAME_QSXGA

    camera.speffect(special_effects)
    # The options are the following:
    # EFFECT_NONE (default) EFFECT_NEG EFFECT_BW EFFECT_RED EFFECT_GREEN EFFECT_BLUE EFFECT_RETRO

    camera.whitebalance(white_balance)
    # The options are the following:
    # WB_NONE (default) WB_SUNNY WB_CLOUDY WB_OFFICE WB_HOME

    camera.saturation(saturation)
    # -2,2 (default 0). -2 grayscale 

    camera.brightness(brightness)
    # -2,2 (default 0). 2 brightness

    camera.contrast(contrast)
    #-2,2 (default 0). 2 highcontrast

    camera.quality(quality)
    # 10-63 lower number means higher quality

    buf = camera.capture()
    return buf


class Wifi():
    def __init__(self, name):
        self.sta_if = network.WLAN(network.STA_IF)
        self.sta_if.config(dhcp_hostname=name)

    def scan(self):
        return self.sta_if.scan()

    def isconnected(self):
        return self.sta_if.isconnected()

    def connect(self, essid, password, timeout=30000):
        self.sta_if.active(True)
        if not self.sta_if.isconnected():
            print("Connecting to WiFi network...")
            self.sta_if.connect(essid, password)
            t = time.ticks_ms()
            while not self.sta_if.isconnected():
                if time.ticks_diff(time.ticks_ms(), t) > timeout:
                    self.sta_if.disconnect()
                    print("Timeout. Could not connect.")
                    return False
            print("Successfully connected to " + essid)
            return True
        else:
            print("Already connected")
            return True

    def disconnect(self):
        self.sta_if.disconnect()

    def ipaddress(self):
        ip, subnetmask, gateway, dns = self.sta_if.ifconfig()
        return ip


class Hotspot:
    def __init__(self):
        self.ap_if = network.WLAN(network.AP_IF)

    def connect(self, essid, password):
        self.ap_if.active(True)
        self.ap_if.config(essid=essid, authmode=network.AUTH_WPA_WPA2_PSK, password=password)

    def disconnect(self):
        self.ap_if.active(False)

    def ipaddress(self):
        ip, subnetmask, gateway, dns = self.ap_if.ifconfig()
        return ip, subnetmask, gateway, dns

#hotspot = Hotspot()
#hotspot.connect(essid="TP-Navid", password="123456789")
#hotspot.disconnect()

#wifi = Wifi("TestWifi")
#print(wifi.scan())
#print(wifi.isconnected())
#wifi.connect('navid', "'goldman&*****'")
#wifi.disconnect()
#print(wifi.ipaddress())


from machine import Pin
from time import sleep
def ControlePin(pin):
    try:
        if 'open' in pin:
            pin = int(pin.split('+')[1])
            led = Pin(pin, Pin.OUT)
            led.value(1)
        elif 'close' in pin:
            pin = int(pin.split('+')[1])
            led = Pin(pin, Pin.OUT)
            led.value(0)
        else:
            pin = int(pin)
            led = Pin(pin, Pin.OUT)
            led.value(not led.value())
    except:
        pass

def LoopControlePin(pin):
    led = Pin(pin, Pin.OUT)
    while True:
      led.value(not led.value())
      sleep(0.5)

#ControlePin(pin=16)
#LoopControlePin(pin=16)

try:
  import usocket as socket
except:
  import socket
import esp
esp.osdebug(None)
class Server:
    def __init__(self, html):
        self.html = html

    def run(self, ip='192.168.4.1', port=80):
        hotspot = Hotspot()
        hotspot.connect(essid="TP-SERVER", password="123456789")
        # hotspot.ifconfig((ip, '255.255.255.0', ip, ip))
        print(hotspot.ipaddress())

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((ip, port))
        s.listen(5)

        while True:
            try:
                if gc.mem_free() < 102000: gc.collect()

                conn, addr = s.accept()
                conn.send(photo())
                conn.close()
            except OSError as e:
                conn.close()
                print('Connection closed')
            print('_____________________________________________________')
server = Server("""
<html>
	<head>
	</head>
	<body>
		<form method="POST">
			<input type="text" name="pen" value="16">
			<button type="submit" class="btn-submit">save</button>
		</form>
	</body>
</html>
""")
server.run()





# Core  0 register dump:
# PC      : 0x400938dc  PS      : 0x00060d33  A0      : 0x80090d49  A1      : 0x3ffcb6f0
# A2      : 0x0000004c  A3      : 0xb33fffff  A4      : 0x0000abab  A5      : 0x0000cdcd
# A6      : 0x00060d23  A7      : 0x00060d20  A8      : 0x0000cdcd  A9      : 0xffffffff
# A10     : 0x00000003  A11     : 0x00060123  A12     : 0x00060120  A13     : 0x0000cdcd
# A14     : 0x003fffff  A15     : 0x00060723  SAR     : 0x00000020  EXCCAUSE: 0x0000001d
# EXCVADDR: 0x0000004c  LBEG    : 0x4008db42  LEND    : 0x4008db4d  LCOUNT  : 0x00000000

