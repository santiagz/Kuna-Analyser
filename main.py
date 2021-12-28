import time
import requests
import telegram

from conf import bot_token, chatid
from datetime import datetime


y = 0.000950  # price of bought currency
currency = 'shibuah'  # like BTC/USDT

bot = telegram.Bot(token=bot_token)  # Notifier

message = bot.send_message(text='bufu', chat_id=chatid)

msg_id = message.message_id


def get_percent_of_change(x):
    z = (x - y) * 100 / x  # percent of change

    if z > 0:
        msg = '💹 UP for +' + str(round(z, 2)) + '%'
        return msg
    elif z < 0:
        msg = '〽️ ️️Down for ' + str(round(z, 2)) + '%'
        return msg
    elif z == 0:
        msg = '☑️ Equal ☑️️️'
        return msg


while True:
    now = datetime.now()

    dt_string = now.strftime("%H:%M:%S %d/%m/%Y")
    print("date and time =", )

    res = requests.get('https://api.kuna.io/v3/tickers?symbols=' + currency).json()

    price_BID = str(res[0][1])
    percent_24h = str(res[0][6])
    price_last = res[0][7]

    msg_text1 = get_percent_of_change(price_last) + '\n\n' + \
                '🪣Price BID = ' + price_BID + '\n' + \
                '🌡Change by 24h: ' + percent_24h + '%' + '\n' + \
                '💵Last Price: ' + str(price_last) + '\n' + \
                '🕑Last update: ' + dt_string
    bot.editMessageText(chat_id=368638207, message_id=msg_id, text=msg_text1)

    time.sleep(60)
