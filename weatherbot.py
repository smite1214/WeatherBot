# -*- coding: utf-8 -*-
#
# Weather Bot
#
# Monitor the feed provided by the gov (https://data.gov.hk/en-data/provider/ hk-hko) 
# Relay the update to user via telegram bot (https://core.telegram.org/bots)
#
# Johnny Chen
# 2016/08/20

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, Job


import weather

program = {
'name' : 'Weather Bot',
'version' : 'v1.0',
'date' : '2016/08/20',
'author' : 'Johnny Chen'
}

timers = dict()
token = '245256832:AAETq571LhrA86hee4bcqHkcEJvRjqkSlBo'
weather_manager = weather.English()
subscribe_time = 'none'

def help(bot, update):
    bot.sendMessage(update.message.chat_id, text='/current = current weather\n' + 
                                                 '/warning = warning information\n' +
                                                 '/subscribe = subscribe warning message\n' +
                                                 '/unsubscribe = unsubscribe warning message\n' +
                                                 '/english = english display\n' +
                                                 '/繁體中文 = 繁體中文顯示\n' +
                                                 '/简体中文 = 简体中文显示\n' +
                                                 '/version = tool version\n' +
                                                 '/help = help message\n')

def version(bot, update):
    bot.sendMessage(update.message.chat_id, text= program['name'] + ' ' + program['version'] + '\n' + 
                                                  program['date'] + '\n' + program['author'] + '\n')

def current(bot, update):
    bot.sendMessage(update.message.chat_id, text=weather_manager.get_current())

def warning(bot, update):
    bot.sendMessage(update.message.chat_id, text=weather_manager.get_warning())

def english(bot, update):
    global weather_manager
    weather_manager = weather.English()
    bot.sendMessage(update.message.chat_id, text='Got it')

def traditional(bot, update):
    global weather_manager
    weather_manager = weather.Traditional()
    bot.sendMessage(update.message.chat_id, text='知道了')

def simplified(bot, update):
    global weather_manager
    weather_manager = weather.Simplified()
    bot.sendMessage(update.message.chat_id, text='知道了')

def check_warning(bot, job):
    #bot.sendMessage(job.context, text='check')
    global subscribe_time
    temp_time = weather_manager.get_pubdate()

    if temp_time == subscribe_time:
        return
    else:
        bot.sendMessage(job.context, text=weather_manager.get_warning())
        subscribe_time = temp_time
		
def subscribe(bot, update, job_queue):
    chat_id = update.message.chat_id

    try:
        job = Job(check_warning, 1, repeat=True, context=chat_id)
        timers[chat_id] = job
        job_queue.put(job)
        bot.sendMessage(chat_id, text='subscribe OK!')
		
    except (IndexError, ValueError):
        bot.sendMessage(chat_id, text='subscribe fail')
	
def unsubscribe(bot, update, job_queue):
    chat_id = update.message.chat_id

    if chat_id not in timers:
        bot.sendMessage(chat_id, text='You have not subscribe')
        return

    job = timers[chat_id]
    job.schedule_removal()
    del timers[chat_id]

    bot.sendMessage(chat_id, text='unsubscribe OK!')

def main():
    updater = Updater(token)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("current", current))
    dp.add_handler(CommandHandler("warning", warning))
    dp.add_handler(CommandHandler("english", english))
    dp.add_handler(CommandHandler("繁體中文", traditional))
    dp.add_handler(CommandHandler("简体中文", simplified))
    dp.add_handler(CommandHandler("subscribe", subscribe, pass_job_queue=True))
    dp.add_handler(CommandHandler("unsubscribe", unsubscribe, pass_job_queue=True))
    dp.add_handler(CommandHandler("version", version))
    dp.add_handler(CommandHandler("help", help))
    updater.start_polling()

    # Run the bot until the you presses Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()
	
if __name__ == '__main__':
    main()
