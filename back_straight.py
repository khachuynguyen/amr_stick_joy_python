import json
import struct
import time
import json
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
    # so.connect(('127.0.0.1', API_PORT_STATE))
    so.settimeout(5)
    so.send(packMsg(1, 3055, {"dist":-0.5,"vx":0.5,"vy":0.5}))
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
        print('json datalen: %d, backReqNum: %d' %(jsonDataLen, backReqNum))
    if(jsonDataLen > 0):
        data = so.recv(1024)
        ret = json.loads(data)
        print(ret)
    so.close()
while True:
    if keyboard.is_pressed('s'):  # Kiểm tra nếu phím 's' được nhấn
        print('Phím "s" được nhấn, dừng chương trình.')
        break  # Thoát vòng lặp
    send_request()
    time.sleep(0.5)
    