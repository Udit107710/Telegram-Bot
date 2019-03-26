from selenium import webdriver
import time
import os
import random

import telegram
from telegram.ext import Updater,CommandHandler,MessageHandler, Filters

def main():

    token = os.environ['TELEGRAM_TOKEN']

    updater = Updater(token)

    dispatcher = updater.dispatcher

    def startCommand(bot, update):
        bot.send_message(chat_id=update.message.chat_id, text="I'm a Cyanide and Happiness bot, I just fetch your daily gags directly from explosm.net")

    def echo(bot, update):
        response = ["No commands as " + update.message.text, "Fuck You! Sorry no such command"]
        bot.send_message(chat_id=update.message.chat_id, text = random.choice(response))

    def dailyCommand(bot, update):
        browser = webdriver.PhantomJS()
        bot.send_chat_action(chat_id=update.message.chat_id, action=telegram.ChatAction.TYPING)
        bot.send_message(chat_id=update.message.chat_id, text="Here is your daily dose")
        browser.get("http://explosm.net")
        image = browser.find_element_by_id("main-comic");
        src = image.get_attribute('src')
        bot.send_photo(chat_id=update.message.chat_id, photo=src)
        browser.close()

    def randomCommand(bot, update):
        bot.send_chat_action(chat_id=update.message.chat_id, action=telegram.ChatAction.TYPING)
        bot.send_message(chat_id=update.message.chat_id, text="Finding random shit...")
        browser = webdriver.PhantomJS()
        browser.get("http://explosm.net")
        random = browser.find_element_by_class_name("nav-random")
        random.click()
        time.sleep(5)
        image = browser.find_element_by_id("main-comic");
        src = image.get_attribute('src')
        bot.send_photo(chat_id=update.message.chat_id, photo=src)
        browser.close()

    start_handler = CommandHandler('start', startCommand)
    dispatcher.add_handler(start_handler)

    echo_handler = MessageHandler(Filters.text, echo)
    dispatcher.add_handler(echo_handler)

    daily_handler = CommandHandler('daily', dailyCommand)
    dispatcher.add_handler(daily_handler)

    random_handler = CommandHandler('random', randomCommand)
    dispatcher.add_handler(random_handler)

    updater.start_polling(clean = True)

    updater.idle()

if __name__ == '__main__':
    main()
