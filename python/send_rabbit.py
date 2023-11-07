import pika
import time
import proto.mi_mensaje_pb2 as mi_mensaje_pb2

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.queue_declare(queue='hello')
counter = 1
protobuf_message = mi_mensaje_pb2.HelloWorld()
while True:
    protobuf_message.name = "fulano menganillo"
    protobuf_message.id = counter
    protobuf_message.msg = -123.456
    protobuf_message.state = True
    rabbit_message = protobuf_message.SerializeToString()
    channel.basic_publish(exchange='', routing_key='hello', body=rabbit_message)
    print(" [x] Sent 'proto message!'")
    time.sleep(5)
    counter = counter + 1

connection.close()
