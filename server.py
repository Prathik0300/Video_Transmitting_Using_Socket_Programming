import cv2 as cv
import pickle as pkl
import struct
import secrets
import string
import socket 

N=7
MAX_CLIENT = 100
server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server_name = socket.gethostname()
server_ip = socket.gethostbyname(server_name)
port = 1001
socket_address = (server_ip,port)
server.bind(socket_address)

server.listen(MAX_CLIENT)
joinKey = ''.join(secrets.choice(string.ascii_uppercase + string.digits) for i in range(N))
save = {server_ip:joinKey}
pkl.dump(save,open("JoiningKey.pkl","wb"))
print("--------------------- SERVER IS ACTIVE AND LISTENING AT  ",socket_address," ---------------------")
flag = True
while flag==True:
    try:
        client,client_address = server.accept()
        print("\nACCEPTING CONNECTION FROM ",client_address)
        if client:
            video = cv.VideoCapture(0)
            while video.isOpened():
                _,frame = video.read()
                frame = cv.flip(frame,1)
                data = pkl.dumps(frame)
                msg = struct.pack("Q",len(data))+data
                client.sendall(msg)
                cv.imshow("TRANSMITTING",frame)
                if cv.waitKey(1) & 0xFF== ord('q'):
                    print("SERVER EXITING..")
                    client.close()
                    flag=False
                    break   
    except:
        break
    




