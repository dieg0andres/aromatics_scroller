import network
import uasyncio as asyncio

from scroller import Scroller
from time import sleep
from umqtt.simple import MQTTClient


SSID = 'Crowne Plaza' #'mauriegio'
PSSWRD = 'carmen19'
FUTURES_URL = 'https://finviz.com/futures.ashx'

BRENT = 'QA'
RBOB = 'RB'
HH = 'NG'
LAST = 'LAST'
PREVCLOSE = 'PREVCLOSE'
LABEL = 'LABEL'

RED = 0
GREEN = 1.2
YELLOW = 0.12

tickers = [BRENT, RBOB, HH]


def connect_to_network(wlan):
    wlan.active(True)
    wlan.connect(SSID, PSSWRD)

    # wait to connect or fail
    max_wait = 10
    while max_wait > 0:
        if wlan.status() < 0 or wlan.status() >=3:
            break
        max_wait -= 1
        print('Waiting for connection...')
        sleep(1)
    
    if wlan.status() != 3:
        raise RuntimeError('Network connection failed :(')
        
    else:
        print('Connected!')
        status = wlan.ifconfig()
        print('ip = ' + status[0])
           
           
def get_data(url):
    
    print('in get data')

    r = urequests.get(FUTURES_URL)
    temp = str(r.content)
    r.close()

    temp = temp[temp.find('tiles'):]
    temp = temp[8:temp.find(';')].upper()

    #data = str(temp).upper().split('TILES')[1]
    #data = data[3:]
    data = json.loads(temp)
    del temp
    print('successfully got new data')
    
    _write_to_file(data, 'data.bin')
    

def _write_to_file(data, file_name):
    file = open(file_name, 'w')
    file.write(str(data))
    file.close()


def _read_from_file(file_name):
    file = open(file_name, 'r')
    data = file.read()
    file.close()
    
    json_acceptable_string = data.replace("'", "\"")
    data = json.loads(json_acceptable_string)
    
    return data
    

async def text_to_scroller(messages, scroll):

    while True:
        
        for msg in messages:
            hue = msg[1]
            message = msg[0]

            for position in range(16,-len(message*(5+1)),-1):
                scroll.show_message(message, position, hue)
                sleep(0.002)
                
        await asyncio.sleep(5)
    
    
def get_color(ticker_data):
    
    if ticker_data[LAST] > 1.02 * ticker_data[PREVCLOSE]:
        return GREEN
    if ticker_data[LAST] < 0.98 * ticker_data[PREVCLOSE]:
        return RED

    return YELLOW
    

def build_msg(data):
    
    message = []
    
    for ticker in tickers:
        msg = data[ticker][LABEL] + ' ' + str(data[ticker][LAST]) + ' '
        message.append( (msg, get_color(data[ticker])) )
    
    return message

        
async def fetch_data():
    while True: 
        data = get_data(FUTURES_URL)
        await asyncio.sleep(10)
        

async def main():
    
    scroll = Scroller()
    scroll.clear()

    wlan = network.WLAN(network.STA_IF)
    connect_to_network(wlan)
    
    mqtt_server = 'broker.hivemq.com'
    client_id = 'clientId-QSrJd1EDc5'
    username = 'dieg0andres19'
    password = '$Carmen19'
    topic_sub = b'testing123diego'
    
    def sub_cb(topic, message):
        print('topic: ' + str(topic))
        print('/n/nmessage: ' + str(message))
    
    def mqtt_connect():
        print('in here')
        client = MQTTClient(client_id, mqtt_server, port=8884, user=username, password=password, keepalive=60)
        client.set_callback(sub_cb)
        client.connect()
        print('Connected to %s MQTT Broker'%(mqtt_server))
        return client
        
    def reconnect():
        print('Failed to connect to MQTT Broker. Reconnecting...')
        sleep(5)
        machine.reset()
    
    try:
        client = mqtt_connect()
        
        
    except OSError as e:
        reconnect()
        
    while True:
        client.subscribe(topic_sub)
        print('subscribed to ' + str(topic_sub))
        sleep(30)    
        
    
#    get_data(FUTURES_URL)        
    
#    data = _read_from_file('data.bin')
#    message = build_msg(data)
#    sleep(5)
#    get_data(FUTURES_URL)
    
   # print(message)
    msg = [('BZ 290', 0), ('PX 1100', 1.2)]
   # asyncio.create_task( scroll.continously_display_prices(msg) )
   # asyncio.create_task(fetch_data())
            
    #while True:
    #    print('i')
    #    await asyncio.sleep(60)
       



asyncio.run(main())









