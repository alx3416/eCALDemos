import sys
import time
import cv2 as cv
import ecal.core.core as ecal_core
from ecal.core.publisher import ProtoPublisher
import proto.mensaje_main_pb2 as mensaje_main_pb2

ecal_core.initialize(sys.argv, "Python webcam Publisher")

pub = ProtoPublisher("webcam_data",
                     mensaje_main_pb2.webcam)
protobuf_message = mensaje_main_pb2.webcam()
cam = cv.VideoCapture(0)

while ecal_core.ok():
    # OpenCV related
    ret_val, img = cam.read()
    if ret_val:
        cv.imshow('my webcam', img)
        if cv.waitKey(1) == 27:
            break  # esc to quit
    # eCAL-protobuff related
    protobuf_message.frame.height = img.shape[0]
    protobuf_message.frame.width = img.shape[1]
    protobuf_message.frame.name = "logitech C920"
    protobuf_message.frame.data = img.data.tobytes()
    pub.send(protobuf_message)

ecal_core.finalize()
cv.destroyAllWindows()
