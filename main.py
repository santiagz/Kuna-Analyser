import time
import telegram
import datetime
import kuna
from loguru import logger

from conf import bot_token, chatid, pr, pb

bot = telegram.Bot(token=bot_token)  # Notifier
graph_kuna = kuna.KunaAPI(public_key=pb, private_key=pr)

message_eth_uah = bot.send_message(text='eth/btc/doge', chat_id=chatid)
msg_id_eth_uah = message_eth_uah.message_id

message_shib_uah = bot.send_message(text='shibuah', chat_id=chatid)
msg_id_shib_uah = message_shib_uah.message_id


def get_time():
    now = datetime.datetime.now()
    without_hours = now.strftime("%M:%S %Y-%m-%d")
    hours = int(now.strftime("%H")) + 2
    return str(hours) + ':' + without_hours


def get_percent_of_change_SHIB(x):
    y = 0.000950  # price of bought currency
    z = (x - y) * 100 / x  # percent of change

    value = 0
    BID_SHIB = graph_kuna.tickers('shibuah')[0][7]
    for wallet in graph_kuna.auth_r_wallets():
        if wallet[1] == 'SHIB':
            value += wallet[2]
    cur_val = value * BID_SHIB

    if z > 0:
        msg = '💹 UP for +' + str(round(z, 2)) + '%' + '\n' + '💸Current value = ' + str(round(cur_val, 2))
        return msg

    elif z < 0:
        msg = '〽️ ️️Down for ' + str(round(z, 2)) + '%' + '\n' + '💸Current value = ' + str(round(cur_val, 2))
        return msg

    elif z == 0:
        msg = '☑️ Equal ☑️️️'
        return msg




def check_if_positive(number):
    if float(number) > 0:
        return '[+]'
    if float(number) < 0:
        return '[-]'
    if float(number) == 0:
        return '[0]'


@logger.catch
def main():
    try:
        while True:
            price_BID_shib = graph_kuna.tickers('shibuah')[0][1]
            percent_24h_shib = graph_kuna.tickers('shibuah')[0][6]
            price_last_shib = graph_kuna.tickers('shibuah')[0][7]

            BID_eth = graph_kuna.tickers('ethusdt')[0][1]
            percent_24h_eth = graph_kuna.tickers('ethusdt')[0][6]

            BID_btc = graph_kuna.tickers('btcusdt')[0][1]
            percent_24h_btc = graph_kuna.tickers('btcusdt')[0][6]

            BID_doge = graph_kuna.tickers('dogeusdt')[0][1]
            percent_24h_doge = graph_kuna.tickers('dogeusdt')[0][6]



            msg_text1 = 'SHIB \n' + get_percent_of_change_SHIB(float(price_last_shib)) + '\n\n' + \
                        '🪣Price BID = ' + str(price_BID_shib) + '\n' + \
                        '🌡Change by 24h: ' + str(percent_24h_shib) + '%' + '\n' + \
                        '💵Last Price: ' + str(price_last_shib) + '\n' + \
                        '🕑Last update: ' + str(get_time())
            bot.editMessageText(chat_id=368638207, message_id=msg_id_shib_uah, text=msg_text1)

            msg_text2 = check_if_positive(percent_24h_eth) + ' ETH = ' + str(BID_eth) + ' ' + str(percent_24h_eth) + '\n' + \
                        check_if_positive(percent_24h_btc) + ' BTC = ' + str(BID_btc) + ' ' + str(percent_24h_btc) + '\n' + \
                        check_if_positive(percent_24h_doge) + ' DOGE = ' + str(BID_doge) + ' ' + str(percent_24h_doge) + '\n' + \
                        '\n' + '🕑Last update: ' + str(get_time())

            bot.editMessageText(chat_id=368638207, message_id=msg_id_eth_uah, text=msg_text2)

            time.sleep(60)

    except Exception as e:
        logger.error(f"{e}")


if __name__ == '__main__':
    main()
