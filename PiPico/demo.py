# Scroller Demo
# Kevin McAleer May 2022

from scroller import Scroller

from time import sleep

# create a message to display
# message = "KEV"
msg1 = "TIME TO WORK OUT"
msg2 = "Nov BZ 292"
# message = "@kevsmac"
# message = "Subscribe!"
# message = "subs: 6703"
# message = "abdefghijklmnopqrstuvwxyz0123456789"
# message = "? / \ < > ( ) ~ ' | . , "

# create a scroller 0bject
scroll = Scroller()

# set the hue colour (0 is red etc)
hue = 0

scroll.clear()

while True or KeyboardInterrupt:
    for position in range(16,-len(msg1*(5+1)),-1):
        hue = 0
        scroll.show_message(msg1, position, hue)
        sleep(0.04)
        
    for position in range(16,-len(msg2*(5+1)),-1): 
        hue = 1.2
        scroll.show_message(msg2, position, hue)
        sleep(0.04)

scroll.clear()