import time
import requests
import telegram
import datetime

from conf import bot_token, chatid

y = 0.000950  # price of bought currency
shib_uah = 'shibuah'  # like BTC/USDT
eth_uah = 'ethuah'  # like BTC/USDT

bot = telegram.Bot(token=bot_token)  # Notifier

message_eth_uah = bot.send_message(text='ethuah', chat_id=chatid)
msg_id_eth_uah = message_eth_uah.message_id

message_shib_uah = bot.send_message(text='shibuah', chat_id=chatid)
msg_id_shib_uah = message_shib_uah.message_id




def get_time():
    now = datetime.datetime.now()
    without_hours = now.strftime("%M:%S %Y-%m-%d")
    hours = int(now.strftime("%H")) + 2
    return str(hours) + ':' + without_hours


def get_percent_of_change_SHIB(x):
    z = (x - y) * 100 / x  # percent of change

    started_value = 562  # UAH

    if z > 0:
        var_plus = started_value + (started_value * round(z, 2) / 100)

        msg = '💹 UP for +' + str(round(z, 2)) + '%' + '\n' + '💸Current value = ' + str(var_plus)
        return msg

    elif z < 0:
        var = started_value - (started_value * -round(z, 2) / 100)
        msg = '〽️ ️️Down for ' + str(round(z, 2)) + '%' + '\n' + '💸Current value = ' + str(var)
        return msg
    elif z == 0:
        msg = '☑️ Equal ☑️️️'
        return msg


def get_percent_of_change_ETH(x):
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
    try:
        res_shib = requests.get('https://api.kuna.io/v3/tickers?symbols=' + shib_uah).json()
        res_eth = requests.get('https://api.kuna.io/v3/tickers?symbols=' + eth_uah).json()

        price_BID_shib = str(res_shib[0][1])
        percent_24h_shib = str(res_shib[0][6])
        price_last_shib = res_shib[0][7]

        price_BID_eth = str(res_eth[0][1])
        percent_24h_eth = str(res_eth[0][6])
        price_last_eth = res_eth[0][7]

        msg_text1 = 'SHIB \n' + get_percent_of_change_SHIB(price_last_shib) + '\n\n' + \
                    '🪣Price BID = ' + price_BID_shib + '\n' + \
                    '🌡Change by 24h: ' + percent_24h_shib + '%' + '\n' + \
                    '💵Last Price: ' + str(price_last_shib) + '\n' + \
                    '🕑Last update: ' + str(get_time())
        bot.editMessageText(chat_id=368638207, message_id=msg_id_shib_uah, text=msg_text1)

        msg_text2 = 'ETH \n' + \
                    '🪣Price BID = ' + price_BID_eth + '\n' + \
                    '🌡Change by 24h: ' + percent_24h_eth + '%' + '\n' + \
                    '💵Last Price: ' + str(price_last_eth) + '\n' + \
                    '🕑Last update: ' + str(get_time())
        # + get_percent_of_change_ETH(price_last_eth) + '\n\n'
        bot.editMessageText(chat_id=368638207, message_id=msg_id_eth_uah, text=msg_text2)

        time.sleep(60)

    except:
        pass
