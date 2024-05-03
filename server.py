import base64
import cv2
import zmq


class server:
    def __init__(self):
        context = zmq.Context()
        self.footage_socket = context.socket(zmq.PUB)
        self.footage_socket.connect('tcp://172.16.0.2:5555')

    def place_frame(self,frame):
        frame = cv2.resize(frame, (1920, 1080))  # resize the frame
        encoded, buffer = cv2.imencode('.jpg', frame)
        jpg_as_text = base64.b64encode(buffer)
        self.footage_socket.send(jpg_as_text)
