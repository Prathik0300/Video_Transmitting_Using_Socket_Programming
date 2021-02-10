import cv2 as cv
import pickle as pkl
import struct
import secrets
import string
import socket 
import sys

client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server_ip = '192.168.1.17'
key =None
try:
    JoinKey = pkl.load(open("JoiningKey.pkl","rb"))
    if server_ip in JoinKey:
        key = JoinKey[server_ip]
        print(key)
    else:
        key=None
except:
    print("there are no active servers!")
if key==None:
    sys.exit()
for i in range(4):
    if i==3:
        print("Three incorrect joining attempts..")
        sys.exit()
    join = input("Enter the Joining key : ")
    if join!=key:
        continue
    else:
        print("successfully connected the server Node!")
        break
port = 1001
socket_address = (server_ip,port)
client.connect(socket_address)

data = b''
payload_size = struct.calcsize('Q')
while True:
    while len(data)<payload_size:
        packet = client.recv(4*1024)
        if not packet:
            print("No packets received..")
            break
        data+=packet
    packed_msg_size = data[:payload_size]
    data = data[payload_size:]
    msg_size = struct.unpack("Q",packed_msg_size)[0]
    while len(data)<msg_size:
        data+=client.recv(4*1024)
    frame_data = data[:msg_size]
    data = data[msg_size:]
    frame = pkl.loads(frame_data)
    cv.imshow("Received",frame)
    if cv.waitKey(1) & 0xFF==ord('q'):
        print("CLIENT EXITING..")
        break
client.close()

    
