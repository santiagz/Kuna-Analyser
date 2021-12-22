import time
import requests
import telegram

from conf import bot_token, chatid

bot = telegram.Bot(token=bot_token)  # Ticket Notifier

message = bot.send_message(text='bufu', chat_id=chatid)

msg_id = message.message_id

while True:
    try:
        res = requests.get('https://api.kuna.io/v3/tickers?symbols=shibuah').json()

        price_BID = res[0][1]
        percent_24h = res[0][6]
        price_last = res[0][7]

        x = price_last  # current
        y = 0.000950    # was bought
        z = (x - y) * 100 / x

        if z > 0:
            msg_text1 = '💹 UP for +' + str(round(z, 2)) + '%' + '\n\n' + \
                        'Price BID = ' + str(price_BID) + '\n' + \
                        'Change by 24h: ' + str(percent_24h) + '%' + '\n' + \
                        'Last Price: ' + str(price_last)
            bot.editMessageText(chat_id=368638207, message_id=msg_id, text=msg_text1)

        elif z < 0:
            msg_text2 = '〽️ ️️Down for ' + str(round(z, 2)) + ' %' + '\n\n' + \
                        'Price BID = ' + str(price_BID) + '\n' + \
                        'Change by 24h: ' + str(percent_24h) + '%' + '\n' + \
                        'Last Price: ' + str(price_last)
            bot.editMessageText(chat_id=368638207, message_id=msg_id, text=msg_text2)
        elif z == 0:
            msg_text2 = '☑️ Equal ☑️️️' + '\n' + \
                        'Price BID = ' + str(price_BID) + '\n' + \
                        'Change by 24h: ' + str(percent_24h) + '%' + '\n' + \
                        'Last Price: ' + str(price_last)
            bot.editMessageText(chat_id=368638207, message_id=msg_id, text=msg_text2)

        time.sleep(60)

    except:
        pass
