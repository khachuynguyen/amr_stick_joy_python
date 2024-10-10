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


def send_request():
    so = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    so.connect((IP_ADDRESS, 19206))
    so.settimeout(5)
    so.send(packMsg(1, 3055, {"dist": 0.5, "vx": 0.5, "vy": 0.5}))
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
def cancle_navigate():
    so = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    so.connect((IP_ADDRESS, 19206))
    so.settimeout(5)
    so.send(packMsg(1, 3003, {}))
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

# Biến lưu trạng thái của phím 'w'
w_is_pressed = False

while True:
    if keyboard.is_pressed('s'):  # Kiểm tra nếu phím 's' được nhấn
        print('Phím "s" được nhấn, dừng chương trình.')
        break  # Thoát vòng lặp
    
    # Kiểm tra nếu phím 'w' được nhấn
    if keyboard.is_pressed('w'):
        if not w_is_pressed:  # Nếu trước đó phím 'w' chưa được nhấn
            w_is_pressed = True  # Cập nhật trạng thái
        send_request()  # Gửi yêu cầu
        time.sleep(0.5)  # Đợi 0.5 giây trước khi gửi lại
    else:
        if w_is_pressed:  # Nếu phím 'w' đã được nhả
            cancle_navigate()
            w_is_pressed = False  # Cập nhật trạng thái