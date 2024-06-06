import socket
import cv2
import pickle
import struct
import threading
import time

answer = 0
MODE = 1

client_sockets = []

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('0.0.0.0', 8485))
server_socket.listen()

conn, addr = server_socket.accept()

data = b""
payload_size = struct.calcsize("Q")

print("####################################")
print("1. 사용자 확인")
print("2. 사용자 영상 출력")
print("3. 저장된 qr코드 확인")
print("####################################")
class Viewer:
    pass
class Communication:
    pass
class Administartor:
    pass

    def chat():
        global answer
        while True:
            answer = input()
        
    t = threading.Thread(target=chat)

    t.start()

     
while True:
    while len(data) < payload_size + 1:
        packet = conn.recv(4096)
        if not packet: break
        data += packet

    data_type, packed_msg_size = data[0], data[1:payload_size+1]
    data = data[payload_size+1:]
    msg_size = struct.unpack("Q", packed_msg_size)[0]

    while len(data) < msg_size:
        data += conn.recv(4096)

    frame_data = data[:msg_size]
    data = data[msg_size:]


    if data_type == ord('A'):  # Message
        message = frame_data.decode()
        client_sockets.append(message)
        
    elif data_type == ord('M'):  # Message
        message = frame_data.decode()
    

    if answer == '1':
        if data_type == ord('F'):  # Video Frame
            frame = pickle.loads(frame_data)
            cv2.imshow("Receiving Video", frame)
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                break
    elif answer == '2':
        print("###사용자 리스트###")
        print("1." + client_sockets[0])
        answer = '0'
   

t.join()
conn.close()