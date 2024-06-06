import socket
import cv2
import pickle
import struct
import time
import threading

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('localhost', 8485))
camera = cv2.VideoCapture(0)
conn, addr = client_socket.accept()

def send_frame(): 
    while camera.isOpened():
        ret, frame = camera.read()
        data = pickle.dumps(frame)
        message = struct.pack("B", ord('F')) + struct.pack("Q", len(data)) + data
        client_socket.sendall(message)
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break

def send_text():
    text = "user1"
    data = text.encode()
    message = struct.pack("B", ord('A')) + struct.pack("Q", len(data)) + data
    client_socket.sendall(message)
    text = input()
    data = text.encode()
    message = struct.pack("B", ord('M')) + struct.pack("Q", len(data)) + data
    client_socket.sendall(message)

def id_connect():
    return "user1"
    
t = threading.Thread(target=send_frame)
t1 = threading.Thread(target=send_text)
t.start()
t1.start()
t.join()
t1.join()
camera.release()
client_socket.close()