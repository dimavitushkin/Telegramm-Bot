import telebot
from config import keys, TOKEN
from extensions import APIException, CryptoConverter

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start'])
def start(message: telebot.types.Message):
    text = f'Здравствуйте, {message.chat.first_name}. Я - бот конвертирующий валюту. \
     Я обрабатываю команды /start - для начала работы, /help - для помощи с работой,\
    /values - для получение доступных видов валют для конвертации.'
    bot.reply_to(message, text)


@bot.message_handler(commands=['help'])
def help(message: telebot.types.Message):
    text = 'Для начала работы, введите данные через пробел в следующем формате \
    \n<название валюты ИЗ которой хотите перевести> \n<название валюты В которую хотите перевести> \
    \n<количество конвертируемой валюты>'
    bot.reply_to(message, text)


@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = "Доступные валюты для конвертации:"
    for key in keys.keys():
        text = '\n'. join((text, key, ))
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text', ])
def convert(message: telebot.types.Message):
    try:
        values = message.text.split(' ')

        if len(values) != 3:
            raise APIException('Слишком много параметров. Смотри help, там написано как правильно пользоваться ботом.')

        base, quote, amount = values
        total_base = CryptoConverter.get_price(base, quote, amount)
    except APIException as e:
        bot.reply_to(message, f'Ошибка пользователя\n{e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду\n{e}')
    else:
        text = f'Цена {amount} {base} в {quote} - {total_base}'
        bot.send_message(message.chat.id, text)


bot.polling()
