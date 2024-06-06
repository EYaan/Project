import socket
import cv2
import pickle
import struct
import time
import threading

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('localhost', 8485))
camera = cv2.VideoCapture(0)
data = b""
payload_size = struct.calcsize("W")
conn, addr = client_socket.accept()
userID = ''

class Communication:
    def __init__(self):
        global userID
        userID = "user1" #서버 접속시 ID전송
        data = userID.encode()
        message = struct.pack("B", ord('A')) + struct.pack("Q", len(data)) + data
        client_socket.sendall(message)
        
    def send_frame():
        while camera.isOpened():
            ret, frame = camera.read()
            data = pickle.dumps(frame)
            message = struct.pack("B", ord(userID+'F')) + struct.pack("Q", len(data)) + data
            client_socket.sendall(message)
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                break

    def send_text():
        text = input() #인식한 사물이름 텍스트 전송 
        data = text.encode()
        message = struct.pack("B", ord(userID+'M')) + struct.pack("Q", len(data)) + data
        client_socket.sendall(message)
        
    def get_data():
        while len(data) < payload_size + 1:
            packet = conn.recv(4096)
            if not packet: break
            data += packet

        data_type, packed_msg_size = data[0], data[1:payload_size+1]
        data = data[payload_size+1:]
        msg_size = struct.unpack(userID+"W", packed_msg_size)[0]

        while len(data) < msg_size:
            data += conn.recv(4096)

        frame_data = data[:msg_size]
        data = data[msg_size:]


        if data_type == ord(userID+'N'):  # Message
            message = frame_data.decode()
            print("text "+message)
        elif data_type == ord(userID+'V'):  # Message
            message = frame_data.decode()
            print("coordinate "+message)

    def __del__(self): 
        data = userID.encode() #접속 종료시 ID전송
        message = struct.pack("B", ord('E')) + struct.pack("Q", len(data)) + data
        client_socket.sendall(message)
        
t = threading.Thread(target=Communication.send_frame)
t1 = threading.Thread(target=Communication.send_text)
t.start()
t1.start()
t.join()
t1.join()

camera.release()
client_socket.close()