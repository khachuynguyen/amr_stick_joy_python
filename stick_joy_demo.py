import json
import struct
import time
import socket
import keyboard
from ip_amr import *

# 0x5A + Version + serierNum + jsonLen + reqNum + rsv
PACK_HEAD_FMT_STR = '!BBHLH6s'
PACK_RSV_DATA = b'\x00\x00\x00\x00\x00\x00'


def packMsg(reqId, msgTyp, msg={}):
    msgLen = 0
    jsonStr = json.dumps(msg)
    if(msg != {}):
        msgLen = len(jsonStr)
    rawMsg = struct.pack(PACK_HEAD_FMT_STR, 0x5A, 1, reqId,
                         msgLen, msgTyp, PACK_RSV_DATA)
    if(msg != {}):
        rawMsg += bytearray(json.dumps(msg), 'ascii')
    return rawMsg


def unpackHead(data):
    result = struct.unpack(PACK_HEAD_FMT_STR, data)
    jsonLen = result[3]
    reqNum = result[4]
    return (jsonLen, reqNum)

def send_request(type):
    request_number = 3003 
    data = {}
    if( type == 'go_straight'):
        data = {"dist": 0.5, "vx": 0.5, "vy": 0.5}
        request_number = 3055 
    if( type == 'back'):
        data = {"dist": 0.5, "vx": -0.5, "vy": -0.5}
        request_number = 3055 
    if( type == 'rotation_right'):
        data = {"angle":3.14,"vw":-0.5}
        request_number = 3056  
    if( type == 'rotation_left'):
        data = {"angle":3.14,"vw":0.5}
        request_number = 3056  
    if( type == 'straight_right'):
        # rot radius tam duong tron ben phai la so am, ben trai la so duong
        data = {"rot_radius":-1,"rot_degree":360,"rot_speed":0.5, "mode":0}
        request_number = 3058   
    if( type == 'straight_left'):
        data = {"rot_radius":1,"rot_degree":360,"rot_speed":0.5, "mode":0}
        request_number = 3058   
    if( type == 'back_right'):
        # rot speed so am la theo chieu kim dong ho
        data = {"rot_radius":-1,"rot_degree":360,"rot_speed":-0.5, "mode":0}
        request_number = 3058   
    if( type == 'back_left'):
        data = {"rot_radius":1,"rot_degree":360,"rot_speed":-0.5, "mode":0}
        request_number = 3058   
    so = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    so.connect((IP_ADDRESS, 19206))
    so.settimeout(5)
    so.send(packMsg(1, request_number, data))
    try:
        data = so.recv(16)
    except socket.timeout:
        print('timeout')
        quit()

    jsonDataLen = 0
    backReqNum = 0
    if(len(data) < 16):
        print('pack head error')
        print(data)
        so.close()
        quit()
    else:
        jsonDataLen, backReqNum = unpackHead(data)
        print('json datalen: %d, backReqNum: %d' % (jsonDataLen, backReqNum))
    if(jsonDataLen > 0):
        data = so.recv(1024)
        ret = json.loads(data)
        print(ret)
    so.close()


# Biến lưu trạng thái của từng tổ hợp phím và phím riêng lẻ
wa_is_pressed = False
wd_is_pressed = False
sa_is_pressed = False
sd_is_pressed = False
w_is_pressed = False
s_is_pressed = False
a_is_pressed = False
d_is_pressed = False

while True:
    if keyboard.is_pressed('g'):  # Kiểm tra nếu phím 'g' được nhấn
        print('Phím "g" được nhấn, dừng chương trình.')
        send_request('')
        break  # Thoát vòng lặp
    
    # Kiểm tra tổ hợp phím 'wa'
    if keyboard.is_pressed('w') and keyboard.is_pressed('a'):
        if not wa_is_pressed:
            wa_is_pressed = True  # Cập nhật trạng thái
        send_request('straight_left')  # Gửi yêu cầu
        print('straight_left')
        time.sleep(0.1)
    else:
        if wa_is_pressed:
            print('Phím "wa" được nhả')
            send_request('')
            wa_is_pressed = False

    # Kiểm tra tổ hợp phím 'wd'
    if keyboard.is_pressed('w') and keyboard.is_pressed('d'):
        if not wd_is_pressed:
            wd_is_pressed = True  # Cập nhật trạng thái
        send_request('straight_right')  # Gửi yêu cầu
        print('straight_right')
        time.sleep(0.1)
    else:
        if wd_is_pressed:
            print('Phím "wd" được nhả')
            send_request('')
            wd_is_pressed = False

    # Kiểm tra tổ hợp phím 'sa'
    if keyboard.is_pressed('s') and keyboard.is_pressed('a'):
        if not sa_is_pressed:
            sa_is_pressed = True  # Cập nhật trạng thái
        send_request('back_left')  # Gửi yêu cầu
        print('back_left')
        time.sleep(0.1)
    else:
        if sa_is_pressed:
            print('Phím "sa" được nhả')
            send_request('')
            sa_is_pressed = False

    # Kiểm tra tổ hợp phím 'sd'
    if keyboard.is_pressed('s') and keyboard.is_pressed('d'):
        if not sd_is_pressed:
            sd_is_pressed = True  # Cập nhật trạng thái
        send_request('back_right')  # Gửi yêu cầu
        print('back_right')
        time.sleep(0.1)
    else:
        if sd_is_pressed:
            print('Phím "sd" được nhả')
            send_request('')
            sd_is_pressed = False

    # Kiểm tra riêng phím 'w'
    if keyboard.is_pressed('w') and not keyboard.is_pressed('a') and not keyboard.is_pressed('d'):
        if not w_is_pressed:
            w_is_pressed = True  # Cập nhật trạng thái
        send_request('go_straight')  # Gửi yêu cầu
        print('go_straight')
        time.sleep(0.1)
    else:
        if w_is_pressed:
            print('Phím "w" được nhả')
            send_request('')
            w_is_pressed = False

    # Kiểm tra riêng phím 's'
    if keyboard.is_pressed('s') and not keyboard.is_pressed('a') and not keyboard.is_pressed('d'):
        if not s_is_pressed:
            s_is_pressed = True  # Cập nhật trạng thái
        send_request('back')  # Gửi yêu cầu
        print('back')
        time.sleep(0.1)
    else:
        if s_is_pressed:
            print('Phím "s" được nhả')
            send_request('')
            s_is_pressed = False

    # Kiểm tra riêng phím 'a'
    if keyboard.is_pressed('a') and not keyboard.is_pressed('w') and not keyboard.is_pressed('s'):
        if not a_is_pressed:
            a_is_pressed = True  # Cập nhật trạng thái
        send_request('rotation_left')  # Gửi yêu cầu
        print('rotation_left')
        time.sleep(0.1)
    else:
        if a_is_pressed:
            print('Phím "a" được nhả')
            send_request('')
            a_is_pressed = False

    # Kiểm tra riêng phím 'd'
    if keyboard.is_pressed('d') and not keyboard.is_pressed('w') and not keyboard.is_pressed('s'):
        if not d_is_pressed:
            d_is_pressed = True  # Cập nhật trạng thái
        send_request('rotation_right')  # Gửi yêu cầu
        print('straight_right')
        time.sleep(0.1)
    else:
        if d_is_pressed:
            print('Phím "d" được nhả')
            send_request('')
            d_is_pressed = False
