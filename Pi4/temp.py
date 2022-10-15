from lib.price_management import Price_Manager
from lib.message_management import Message_Manager
from lib.init import create_prices

prices = create_prices()

pm = Price_Manager()
pm.update_prices(prices)

for p in prices:
    pm.print_price(p)

mm = Message_Manager()
msgs = mm.create_messages(prices)

for m in msgs:
    mm.print_message(m)

mm.send_messages_MQTT(msgs)
