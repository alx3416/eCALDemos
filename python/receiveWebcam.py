import sys
import cv2 as cv
import numpy as np

import ecal.core.core as ecal_core
from ecal.core.subscriber import ProtoSubscriber
import proto.mensaje_main_pb2 as mensaje_main_pb2

ecal_core.initialize(sys.argv, "Python webcam Subscriber")
sub = ProtoSubscriber("webcam_data", mensaje_main_pb2.webcam)
protobuf_message = mensaje_main_pb2.webcam()

while ecal_core.ok():
    is_received, protobuf_message, time = sub.receive(1)
    if is_received:
        print(protobuf_message.frame.name)
        buffer = np.frombuffer(protobuf_message.frame.data,
                               dtype=np.uint8)
        frame = np.reshape(buffer, (protobuf_message.frame.height,
                                    protobuf_message.frame.width, 3))
        cv.imshow('my webcam received', frame)
        if cv.waitKey(1) == 27:
            break  # esc to quit


ecal_core.finalize()
cv.destroyAllWindows()
