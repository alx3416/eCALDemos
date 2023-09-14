import sys
import time
import cv2 as cv
import ecal.core.core as ecal_core
from ecal.core.publisher import ProtoPublisher
import proto.mensaje_main_pb2 as mensaje_main_pb2
import lz4.frame

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
    # No compression
    # protobuf_message.frame.data = img.data.tobytes()
    # protobuf_message.frame.imagecompression = (
    #     mensaje_main_pb2.mensaje__data__pb2.compression.Value('UNCOMPRESSED'))
    # protobuf_message.frame.imageformat = (
    #     mensaje_main_pb2.mensaje__data__pb2.format.Value('RGB'))

    # JPEG
    # _, image_bytes = cv.imencode('.jpg', img)
    # protobuf_message.frame.data = image_bytes.tobytes()
    # protobuf_message.frame.imagecompression = (
    #     mensaje_main_pb2.mensaje__data__pb2.compression.Value('JPEG'))
    # protobuf_message.frame.imageformat = (
    #     mensaje_main_pb2.mensaje__data__pb2.format.Value('RGB'))

    # LZ4
    protobuf_message.frame.data = lz4.frame.compress(img.data.tobytes())
    protobuf_message.frame.imagecompression = (
        mensaje_main_pb2.mensaje__data__pb2.compression.Value('LZ4'))
    protobuf_message.frame.imageformat = (
        mensaje_main_pb2.mensaje__data__pb2.format.Value('RGB'))
    pub.send(protobuf_message)

ecal_core.finalize()
cv.destroyAllWindows()
