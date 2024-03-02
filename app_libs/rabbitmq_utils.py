import json

import pika
from django.conf import settings
from opentelemetry import trace
from opentelemetry.trace.propagation.tracecontext import TraceContextTextMapPropagator

from app_libs.mongo_utils import insert_data
from apps.twitter.models import UserPostServingHistory


def publish_message(queue_name, message):
    parameters = pika.URLParameters(settings.RABBITMQ_URL)
    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()

    channel.queue_declare(queue=queue_name, durable=True)
    channel.basic_publish(exchange='',
                          routing_key=queue_name,
                          body=message,
                          properties=pika.BasicProperties(
                              delivery_mode=2,  # make message persistent
                          ))
    connection.close()

def consume_message(queue_name, callback):
    print("----"*100)
    parameters = pika.URLParameters(settings.RABBITMQ_URL)
    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()

    channel.queue_declare(queue=queue_name, durable=True)
    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue=queue_name, on_message_callback=callback)

    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()


def callback(ch, method, properties, body):
    tracer = trace.get_tracer(__name__)
    carrier = properties.headers
    propagator = TraceContextTextMapPropagator()
    context = propagator.extract(carrier=carrier)
    print("---"*100)
    print("context", context)
    # Continue the trace using the extracted context
    with tracer.start_as_current_span("consume_message", context=context):
        print(f"Received {body}")
        print("==="*100)
        print(f" [x] Received {body}")
        all_data = json.loads(body.decode('utf-8'))
        print("all_data", all_data)
        tracer = trace.get_tracer(__name__)
        # with tracer.start_as_current_span('mongo_insertion'):
        insert_data(all_data.get('data'))
        # Acknowledge the message
        ch.basic_ack(delivery_tag=method.delivery_tag)