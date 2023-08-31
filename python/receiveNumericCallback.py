import sys
import time

import ecal.core.core as ecal_core
from ecal.core.subscriber import ProtoSubscriber
import proto.mi_mensaje_pb2 as mi_mensaje_pb2


def callback(topic_name, proto_msg, time):
    print("Message {} from {}: {}".format(proto_msg.id,
                                          proto_msg.name, proto_msg.msg))

ecal_core.initialize(sys.argv, "Python Protobuf Subscriber Callback")
sub = ProtoSubscriber("mensaje 1", mi_mensaje_pb2.HelloWorld)
sub.set_callback(callback)

while ecal_core.ok():
    time.sleep(0.5)

ecal_core.finalize()
