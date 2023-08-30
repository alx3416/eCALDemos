import sys

import ecal.core.core as ecal_core
from ecal.core.subscriber import ProtoSubscriber
import proto.mi_mensaje_pb2 as mi_mensaje_pb2

ecal_core.initialize(sys.argv, "Python Protobuf Subscriber")
sub = ProtoSubscriber("mensaje 1", mi_mensaje_pb2.HelloWorld)
protobuf_message = mi_mensaje_pb2.HelloWorld()

while ecal_core.ok():
    is_received, protobuf_message, time = sub.receive(1)
    if is_received:
        print(protobuf_message.id)

ecal_core.finalize()
