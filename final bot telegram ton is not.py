import requests
import telebot
from telebot import types

CMC_API_KEY = '7f1cc06a-cc12-476b-add3-417478879451'
BOT_TOKEN = '7042690182:AAGRGjWXTlOp7sE7F0jr_4XTYyK7xXNqoRk'


# crypto price
def get_crypto_price(crypto_symbol, base_currency='USD'):
    url = f'https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest?symbol={crypto_symbol}&convert={base_currency}'
    headers = {
        'Accepts': 'application/json',
        'X-CMC_PRO_API_KEY': '7f1cc06a-cc12-476b-add3-417478879451'
    }

    response = requests.get(url, headers=headers)
    data = response.json()

    if 'data' in data and crypto_symbol in data['data']:
        price = data['data'][crypto_symbol]['quote'][base_currency]['price']
        return price
    else:
        return None


TON_price = get_crypto_price('TON')
NOT_price = get_crypto_price('NOT')
BTC_price = get_crypto_price('BTC')


# bot

bot = telebot.TeleBot(BOT_TOKEN)


# handler

@bot.message_handler(commands=['price', 'start'])
def Price_ask(message):
    markup = types.InlineKeyboardMarkup(row_width=1)

    TON = types.InlineKeyboardButton('TON price', callback_data='TON')
    NOT = types.InlineKeyboardButton('NOT price', callback_data='NOT')
    BTC = types.InlineKeyboardButton('BTC price', callback_data='BTC')

    markup.add(TON, NOT, BTC)

    bot.send_message(message.chat.id, 'chose a cryptocurrency to show the price:', reply_markup=markup)


@bot.callback_query_handler(func=lambda call:True)
def price(callback):
    if callback.message:
        if callback.data == 'TON':
            bot.send_message(callback.message.chat.id, f'TON price is :{TON_price}')
        elif callback.data == 'NOT':
            bot.send_message(callback.message.chat.id, f'NOT price is :{NOT_price}')
        elif callback.data == 'BTC':
            bot.send_message(callback.message.chat.id, f'BTC price is :{BTC_price}')
        else :
            price("this crypto is not supported in our bot. we're sorry! ")


bot.polling()
