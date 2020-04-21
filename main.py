from telegram.ext import Updater, CommandHandler
from telegram import ParseMode
import requests
import re
import logging
import json
from telegram.error import (TelegramError, Unauthorized, BadRequest, 
                            TimedOut, ChatMigrated, NetworkError)
from yahoo_fin import stock_info as si
import math

def get_url():
    contents = requests.get('https://random.dog/woof.json').json()    
    url = contents['url']
    return url


def stock(update, context):
    if len(context.args) < 1:
        update.message.reply_text("Please enter stock code after /stock")

    else:
        output = ""
        for stock_code in context.args:
            stock_value = si.get_live_price(stock_code)
            stock_data = si.get_data(stock_code)
            print(stock_data)
            if math.isnan(stock_value):
               output += stock_code.upper() + ": stock_code not found \n"
            else:
                output += stock_code.upper() + "\nCurrent: " + str(format(stock_value,'.2f')) + "\nDaily Open: " + str(format(stock_data.iloc[-1][0], '.2f')) + "\nDaily High: " + str(format(stock_data.iloc[-1][1],'.2f')) + "\nDaily Low: " + str(format(stock_data.iloc[-1][2],'.2f')) + "\n\n"

        update.message.reply_text(output)

def best(update, context):
    stock_list = si.get_day_gainers()
    output = "Stock Code \t\t\t TTM\n\n"
    for i in range(0,10):
        if math.isnan(stock_list.iloc[i, -1]):
            ttm_val = "---"
        else:
            ttm_val =  str(format(stock_list.iloc[i, -1], '.2f'))
        output +=  str(i+1) + ". " + str(stock_list.iloc[i,0]).upper() +  " \t\t\t " + ttm_val +' \n'
    print(output)
    context.bot.send_message(chat_id=update.effective_chat.id, text=output)

def worst(update, context):
    stock_list = si.get_day_losers()
    output = "Stock Code \t\t\t TTM\n\n"
    for i in range(0,10):
        if math.isnan(stock_list.iloc[i, -1]):
            ttm_val = "---"
        else:
            ttm_val =  str(format(stock_list.iloc[i, -1], '.2f'))
        output +=  str(i+1) + ". " + str(stock_list.iloc[i,0]).upper() +  " \t\t\t " + ttm_val +' \n'
    print(output)
    context.bot.send_message(chat_id=update.effective_chat.id, text=output)

def active(update, context):
    stock_list = si.get_day_most_active()
    output = "Stock Code \t\t\t TTM\n\n"
    for i in range(0,10):
        if math.isnan(stock_list.iloc[i, -1]):
            ttm_val = "---"
        else:
            ttm_val =  str(format(stock_list.iloc[i, -1], '.2f'))
        output +=  str(i+1) + ". " + str(stock_list.iloc[i,0]).upper() +  " \t\t\t " + ttm_val +' \n'
    print(output)
    context.bot.send_message(chat_id=update.effective_chat.id, text=output)

def bop(update, context):
    url = get_url()
    context.bot.send_photo(chat_id=update.effective_chat.id, photo=url)

def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot, please bop me (type /bop) or ask me about stock (type /stock [stock code]!")

def error_callback(update, context):
    try:
        raise context.error

    except Unauthorized:
        # remove update.message.chat_id from conversation list
        print("Unauthorized")
    except BadRequest:
        # handle malformed requests - read more below!
        print("BadRequest")
    except TimedOut:
        # handle slow connection problems
        print("TimedOut")
    except NetworkError:
        # handle other connection problems
        print("NetworkError")
    except ChatMigrated as e:
        # the chat_id of a group has changed, use e.new_chat_id instead
        print("ChatMigrated")
    except TelegramError:
        # handle all other telegram related errors
        print("TelegramError")

def main():
    updater = Updater(token='[Telegram bot token]', use_context=True)
    dp = updater.dispatcher
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)
    dp.add_handler(CommandHandler('start',start))
    dp.add_handler(CommandHandler('stock',stock))
    dp.add_error_handler(error_callback)
    dp.add_handler(CommandHandler('bop',bop))
    dp.add_handler(CommandHandler('worst',worst))
    dp.add_handler(CommandHandler('best',best))
    dp.add_handler(CommandHandler('active',active))

    updater.start_polling()
    updater.idle()
    
if __name__ == '__main__':
    main()
