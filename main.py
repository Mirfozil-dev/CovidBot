from telegram import ReplyKeyboardMarkup
from telegram.ext import Updater, CommandHandler, ConversationHandler, MessageHandler, Filters
import config
from covid19 import Covid19

buttons = ReplyKeyboardMarkup(
    [
        ['Statistics'], ['World']
    ],
    resize_keyboard=True
)

covid = Covid19()


def start(update, context):
    update.message.reply_text(
        'Hello {} 👋\nI can provide you information about COVID19🦠'.format(update.message.from_user.first_name), reply_markup=buttons
    )
    return 1


def stats(update, context):
    data = covid.getByCountry('Uzbekistan')

    update.message.reply_html(
        '🇺🇿 <b>Uzbekistan</b>\n\n<b>Total confirmed: </b> {}\n<b>Total recovered: </b> {}\n<b>Total died: </b> {}\n'.format(
            "{:,}".format(data['cases']), "{:,}".format(data['recovered']), "{:,}".format(data['deaths'])),
        reply_markup=buttons
    )


def world(update, context):
    data = covid.getTotal()

    update.message.reply_html(
        '🌎 <b>World</b>\n\n<b>Total confirmed: </b> {}\n<b>Total recovered: </b> {}\n<b>Total died: </b> {}\n'.format(
            "{:,}".format(data['cases']),
            "{:,}".format(data['recovered']),
            "{:,}".format(data['deaths'])),
        reply_markup=buttons
    )


updater = Updater(config.TOKEN, use_context=True)
conv_handler = ConversationHandler(
    entry_points=[CommandHandler('start', start)],
    states={
        1: [
            MessageHandler(Filters.regex('^(Statistics)$'), stats),
            MessageHandler(Filters.regex('^(World)$'), world),
        ]
    },
    fallbacks=[MessageHandler(Filters.text, start)]
)
updater.dispatcher.add_handler(conv_handler)

updater.start_polling()
updater.idle()
