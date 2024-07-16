# client1.py

# client1.py and client2.py is exact the same.

from pubnub.callbacks import SubscribeCallback
from pubnub.enums import PNStatusCategory
from pubnub.pnconfiguration import PNConfiguration
from pubnub.pubnub import PubNub
import time
import os

pnconfig = PNConfiguration()

userId = os.path.basename(__file__)

pnconfig.publish_key = 'pub'
pnconfig.subscribe_key = 'sub'

pnconfig.user_id = userId
pnconfig.ssl = True

pubnub = PubNub(pnconfig)

def my_publish_callback(envelope, status):
    if not status.is_error():
        pass
    return

class MySubscribeCallback(SubscribeCallback):
    def presence(self, pubnub, presence):
        pass
    def status(self, pubnub, status):
        pass
    def message(self, pubnub, message):
        if message.publisher == userId : return
        print (f"From device {message.publisher}: {message.message}")
    
pubnub.add_listener(MySubscribeCallback())
pubnub.subscribe().channels("chan-1").execute()

while True:
    msg = input("")
    if msg == 'exit': os._exit(1)
    pubnub.publish().channel("chan-1").message(str(msg)).pn_async(my_publish_callback)
