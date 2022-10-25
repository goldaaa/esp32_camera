import network
import socket
import camera
class Camera:
    def __init__(self):
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


ssid = "navid"
password = "'goldman&*****'"
print('SSID:', ssid)
sta_if = network.WLAN(network.STA_IF)
sta_if.active(True)
sta_if.connect(ssid, password)
print(sta_if.ifconfig())


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('', 80))

cam = Camera()

while True:
    s.listen(1024)
    conn, addr = s.accept()
    conn.send(cam.photo())
    conn.close()
