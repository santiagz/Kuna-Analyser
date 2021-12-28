import time
import requests
import telegram
import pytz
import datetime
import ntplib


from conf import bot_token, chatid


y = 0.000950  # price of bought currency
currency = 'shibuah'  # like BTC/USDT

bot = telegram.Bot(token=bot_token)  # Notifier

message = bot.send_message(text='bufu', chat_id=chatid)

msg_id = message.message_id

LOCALTIMEZONE = pytz.timezone("Europe/Kiev")  # time zone name from Olson database


def utc_to_local(utc_dt):
    return utc_dt.replace(tzinfo=pytz.utc).astimezone(LOCALTIMEZONE)


def get_time_from_NTPClient():
    try:
        c = ntplib.NTPClient()
        response = c.request('europe.pool.ntp.org', version=3)
        formatted_date_with_micro_seconds = datetime.datetime.strptime(
            str(datetime.datetime.utcfromtimestamp(response.tx_time)), "%Y-%m-%d %H:%M:%S.%f")
        local_dt = utc_to_local(formatted_date_with_micro_seconds)
        formatted_date_with_corrections = str(local_dt).split(".")[0]
        return formatted_date_with_corrections
    except:
        return 'Error while getting time!'


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
    formatted_date = get_time_from_NTPClient()

    res = requests.get('https://api.kuna.io/v3/tickers?symbols=' + currency).json()

    price_BID = str(res[0][1])
    percent_24h = str(res[0][6])
    price_last = res[0][7]

    msg_text1 = get_percent_of_change(price_last) + '\n\n' + \
                '🪣Price BID = ' + price_BID + '\n' + \
                '🌡Change by 24h: ' + percent_24h + '%' + '\n' + \
                '💵Last Price: ' + str(price_last) + '\n' + \
                '🕑Last update: ' + str(formatted_date)
    bot.editMessageText(chat_id=368638207, message_id=msg_id, text=msg_text1)

    time.sleep(60)
