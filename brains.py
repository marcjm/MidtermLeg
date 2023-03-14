#brains.py
import time
import machine
Import mqtt_CBR

from secrets import Tufts_eecs as wifi

# This code is run on the RP2040 and sends info to the mosquitto broker

mqtt_broker = '10.245.61.77'
topic_sub = 'angles'
topic_pub = 'angles'
client_id = 'Marc'


mqtt_CBR.connect_wifi(wifi)
led = machine.Pin(6, machine.Pin.OUT)  # 6 for 2040

def blink(delay = 0.1):
    led.off()
    time.sleep(delay)
    led.on()

def whenCalled(topic, msg):
    print((topic.decode(), msg.decode()))
    blink()
    time.sleep(0.01)
    blink()

def send_val(value):
    fred = mqtt_CBR.mqtt_client(client_id, mqtt_broker, whenCalled)
    fred.publish(topic_pub, value)


def main():
    fred = mqtt_CBR.mqtt_client(client_id, mqtt_broker, whenCalled)
    #fred.subscribe(topic_sub)
#This is our set of angles that we want to move through
t1 = [0.000000,4.507333,3.959869,3.493355,3.075768,2.687122,2.314154,1.947819,1.582076,1.213316,0.840106,0.463070,0.084745,0.290677,0.657797,1.010647,1.343453,1.651390,1.931216,2.181649,0.000000,0.846694,0.848872,0.850872,0.852697,0.854354,0.855847,0.857181,0.858362,0.859396,0.860287,0.861040,0.861663,0.862159,0.862535,0.862795,0.862946,0.862993,0.862941,0.862795,0.000000,1.765587,1.848833,1.921962,1.986612,2.044550,2.097617,2.147694,2.196683,2.246505,2.299116,2.356550,2.420986,2.494846,2.580949,2.682740,2.804644,2.970771,4.093062,8.457961]
t2 = [0.000000,7.107475,6.274471,5.584270,4.988083,4.455852,3.967780,3.510192,3.073360,2.650320,2.236201,1.827837,1.423499,1.022668,0.625768,0.233844,0.151806,0.530011,0.900071,1.262008,0.000000,0.323694,0.330836,0.337908,0.344909,0.351842,0.358706,0.365504,0.372236,0.378904,0.385509,0.392053,0.398537,0.404962,0.411331,0.417645,0.423906,0.430115,0.436275,0.442388,0.000000,0.974975,1.157372,1.335042,1.508949,1.680195,1.850016,2.019784,2.191017,2.365408,2.544869,2.731598,2.928181,3.137746,3.364181,3.612485,3.889303,4.241255,6.503390,14.752157]

for i in range(len(t1)-1):
    x = t1[i]
    y = t2[i]
    msg = (x,y)
    messages = str(msg)
    fred.publish(topic,messages)
    

    old = 0
    i = 0
    while True:
        try:
            fred.check()
            if (time.time() - old) > 5:
                msg = 'iteration %d' % i
                fred.publish(topic_pub, msg)
                old = time.time()
                i += 1
                blink()
        except OSError as e:
            print(e)
            fred.connect()
        except KeyboardInterrupt as e:
            fred.disconnect()
            print('done')
            break

main()
