"""
Class for Handling Nova events in OpenStack's RabbitMQ

Uses the pika library for handling the AMQP protocol, implementing the necessary callbacks for Nova events
"""

__authors__ = "Claudio Marques, David Palma, Luis Cordeiro"
__copyright__ = "Copyright (c) 2014 OneSource Consultoria Informatica, Lda"
__license__ = "Apache 2"
__contact__ = "www.onesource.pt"
__date__ = "01/09/2014"

__version__ = "1.0"

import json
import pika
from common import log

class CeilometerEvents:

    def __init__(self, rabbit_host, rabbit_user, rabbit_pass, zabbix_sender, zabbix_eventlet_pool):

        """
        TODO
        :type self: object
        """
        self.rabbit_host = rabbit_host
        self.rabbit_user = rabbit_user
        self.rabbit_pass = rabbit_pass
        self.zabbix_sender = zabbix_sender
        self.pool = zabbix_eventlet_pool
        log.info('Ceilometers listener started ...')

    def ceilometer_amq(self):
        """
        Method used to listen to nova events

        """
        connection = pika.BlockingConnection(pika.ConnectionParameters(host=self.rabbit_host,
                                                                       credentials=pika.PlainCredentials(
                                                                           username=self.rabbit_user,
                                                                           password=self.rabbit_pass)))
        channel = connection.channel()
        result = channel.queue_declare(exclusive=True)
        queue_name = result.method.queue
        channel.exchange_declare(exchange='ceilometer', type='topic')
        channel.queue_bind(exchange='ceilometer', queue=queue_name, routing_key='notifications.#')
        channel.queue_bind(exchange='ceilometer', queue=queue_name, routing_key='metering')

        #channel.queue_bind(exchange='ceilometer.agent.notification_fanout', queue=queue_name)
        #channel.queue_bind(exchange='ceilometer.collector_fanout', queue=queue_name)
        channel.basic_consume(self.ceilometer_callback, queue=queue_name, no_ack=True)
        channel.start_consuming()

    def ceilometer_callback(self, ch, method, properties, body):
        """
        Method used by method ceilometer_amq() to filter messages by type of message.

        :param ch: refers to the head of the protocol
        :param method: refers to the method used in callback
        :param properties: refers to the proprieties of the message
        :param body: refers to the message transmitted
        """
        payload = json.loads(body)
        try:
            message_body = json.loads(payload['oslo.message'])
            samples = message_body['args']['data']
            #print "--------------------------------------------------"
            self.pool.spawn_n(self.zabbix_sender.consume_samples,samples)
        except Exception,e:
            log.warn(str(e))          

