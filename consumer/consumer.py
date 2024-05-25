
import pika
import json


# Stablish the connection to RabbitMQ
connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

# declare the queue
queue = channel.queue_declare('order_report')
queue_name = queue.method.queue

# bind the exchange to the queue 
channel.queue_bind(
    exchange='order', # the exchange
    queue=queue_name, # the queue
    routing_key='order.report' # binding key
)

# Consume the messages:

def callback(ch, method, properties, body):
    payload = json.loads(body)
    print('[x] Generating report')
    print(f"""
          plate: {payload.get('plate')}
          path: {payload.get('path')}
          """)
    print('[x] Done')
    # we will send an aknowledgement to RabbitMQ that we received the message, and RabbitMQ is free to delete the message
    ch.basic_ack(delivery_tag=method.delivery_tag)


channel.basic_consume(on_message_callback=callback, queue=queue_name)

print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()


# import pika
# import time
# import os

# # read rabbitmq connection url from environment variable
# amqp_url = os.environ['AMQP_URL']
# url_params = pika.URLParameters(amqp_url)

# # connect to rabbitmq
# connection = pika.BlockingConnection(url_params)
# chan = connection.channel()

# # declare a new queue
# # durable flag is set so that messages are retained
# # in the rabbitmq volume even between restarts
# chan.queue_declare(queue='hello', durable=True)


# def receive_msg(ch, method, properties, body):
#     """function to receive the message from rabbitmq
#     print it
#     sleep for 2 seconds
#     ack the message"""

#     print('received msg : ', body.decode('utf-8'))
#     # time.sleep(2)
#     # print('acking it')
#     ch.basic_ack(delivery_tag=method.delivery_tag)


# # to make sure the consumer receives only one message at a time
# # next message is received only after acking the previous one
# chan.basic_qos(prefetch_count=1)

# # define the queue consumption
# chan.basic_consume(queue='hello',
#                    on_message_callback=receive_msg)

# print("Waiting to consume")
# # start consuming
# chan.start_consuming()
