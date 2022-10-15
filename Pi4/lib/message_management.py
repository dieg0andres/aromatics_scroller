from lib.secrets import *

import time
import paho.mqtt.client as paho

from paho import mqtt
from lib.config import RED, GREEN, YELLOW, BZ


class Message:

    def __init__(self, display_text, price, color):
        self.display_text = display_text
        self.price = price
        self.color = color



class Message_Manager:

    def __init__(self):
        pass


    def create_messages(self, prices):
        msgs = []

        for p in prices:
            if p.last != -1:

                desc = p.desc.replace(p.desc.split()[1], p.month)

                if p.desc == "BZ FM HOU DDP":
                    desc = BZ

                m = Message(desc, p.last, self.__get_color(p.last, p.prev_close))
                msgs.append(m)

        return msgs


    def send_messages_MQTT(self, msgs):

        wrapped_msgs = self.__wrap_messages(msgs)
        print(wrapped_msgs)

        # setting callbacks for different events to see if it works, print the message etc.
        def on_connect(client, userdata, flags, rc, properties=None):
            print("CONNACK received with code %s." % rc)

        # with this callback you can see if your publish was successful
        def on_publish(client, userdata, mid, properties=None):
            print("mid: " + str(mid))

        # print which topic was subscribed to
        def on_subscribe(client, userdata, mid, granted_qos, properties=None):
            print("Subscribed: " + str(mid) + " " + str(granted_qos))

        # print message, useful for checking if it was successful
        def on_message(client, userdata, msg):
            print(msg.topic + " " + str(msg.qos) + " " + str(msg.payload))

        # using MQTT version 5 here, for 3.1.1: MQTTv311, 3.1: MQTTv31
        # userdata is user defined data of any type, updated by user_data_set()
        # client_id is the given name of the client
        client = paho.Client(client_id="", userdata=None, protocol=paho.MQTTv5)
        client.on_connect = on_connect

        # enable TLS for secure connection
        client.tls_set(tls_version=mqtt.client.ssl.PROTOCOL_TLS)
        # set username and password
        client.username_pw_set(MQ_username, MQ_password)
        # connect to HiveMQ Cloud on port 8883 (default for MQTT)
        client.connect(MQ_host, MQ_port)

        # setting callbacks, use separate functions like above for better visibility
        client.on_subscribe = on_subscribe
        client.on_message = on_message
        client.on_publish = on_publish

        # subscribe to all topics of prices by using the wildcard "#"
        client.subscribe("prices/#", qos=1)

        # a single publish, this can also be done in loops, etc.
        for m in wrapped_msgs:

            client.publish("prices", payload=str.encode(m), qos=0)
            print("published ", m)
            time.sleep(1)


    def print_message(self, msg):
        print(msg.display_text, " ", msg.price, " ", msg.color)


    def __get_color(self, last, prev_close):

        if last > 1.01 * prev_close:
            return GREEN
        if last < 0.99 * prev_close:
            return RED
        return YELLOW


    def __wrap_messages(self, msgs):

        wrapped_msgs = []

        for msg in msgs:
            m = str(msg.display_text)+" "+str(msg.price)+" "+str(msg.color)
            wrapped_msgs.append(m)

        return wrapped_msgs
