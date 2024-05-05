
import paho.mqtt.client as mqtt
import time

MQTT_SERVER = "mqtt.ohstem.vn"
MQTT_PORT = 1883
MQTT_USERNAME = "dashboard_iot"
MQTT_PASSWORD = ""
MQTT_TOPIC_SUB = {"/feeds/V3", "/feeds/V4", "/feeds/V5", "/feeds/V6"}


def mqtt_connected(client, userdata, flags, rc):
    print("Connected succesfully!!")
    for topic_name in MQTT_TOPIC_SUB:
        client.subscribe(MQTT_USERNAME + topic_name)

def mqtt_subscribed(client, userdata, mid, granted_qos):
    print("Subscribed to Topic!!!")

def mqtt_recv_message(client, userdata, message):
    #print("Received: ", message.payload.decode("utf-8"))
    print(" Received message " + message.payload.decode("utf-8")
          + " on topic '" + message.topic
          + "' with QoS " + str(message.qos))

mqttClient = mqtt.Client()
mqttClient.username_pw_set(MQTT_USERNAME, MQTT_PASSWORD)
mqttClient.connect(MQTT_SERVER, int(MQTT_PORT), 60)

#Register mqtt events
mqttClient.on_connect = mqtt_connected
mqttClient.on_subscribe = mqtt_subscribed
mqttClient.on_message = mqtt_recv_message

mqttClient.loop_start()

counter = 0
temp = -10
humi = 0
while True:
    temp += 1
    humi += 2
    if temp == 40:
        temp = 0
    if humi == 100:
        humi = 0
    mqttClient.publish(MQTT_USERNAME + "/feeds/V1", temp)
    mqttClient.publish(MQTT_USERNAME + "/feeds/V2", humi)
    time.sleep(5)