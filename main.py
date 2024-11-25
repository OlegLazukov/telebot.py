import telebot
from config import *
from telebot import types
from emoji import emojize
from neiro import Text2ImageAPI
import base64


bot = telebot.TeleBot(TOKEN)
api = Text2ImageAPI(url_api, api_key, secret_key)
name_bot = str(bot.get_me().first_name)


@bot.message_handler(commands=["start"])
def welcome(message):
    stick = open("5203978965076680784.tgs", "rb")
    name_my = str(message.chat.first_name)
    bot.send_sticker(message.chat.id, stick)
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("Найти картинку!")
    item2 = types.KeyboardButton("Хочу начать зарабатывать!")
    markup.add(item1, item2)
    bot.send_message(message.chat.id, f"Привет {name_my}!!! Добро пожаловать!\nЯ {name_bot} - телеграмм бот для проекта Олега.",
    parse_mode="html", reply_markup=markup)

def message_input_step(message):
    text = message.text
    model_id = api.get_model()
    uuid = api.generate(text.lower(), model_id)
    images = api.check_generation(uuid)
    image_base64 = images[0]
    image_data = base64.b64decode(image_base64)
    with open("image.jpg", "wb") as file:
        file.write(image_data)
        bot.reply_to(message, "Вот, что удалось найти по твоему запросу.\nНадеюсь это то, что ты искал дружище😇")
    return bot.send_photo(message.chat.id, photo=image_data)


@bot.message_handler(content_types=["text"])
def funcy(message):
    if message.chat.type == "private":
        if message.text == "Найти картинку!":
            bot.reply_to(message, "Введи текст, а я в свою очередь сгенерирую картинку!\nТолько придется немного подождать😉")
            bot.register_next_step_handler(message, message_input_step)
        elif message.text == "Хочу начать зарабатывать!":
            markup = types.InlineKeyboardMarkup(row_width=2)
            item1 = types.InlineKeyboardButton(emojize("Уверен:grinning_face:"), callback_data="sure")
            item2 = types.InlineKeyboardButton(emojize("Передумал:unamused_face:"), callback_data="change my mind")
            markup.add(item1, item2)

            bot.send_message(message.chat.id, "Прекрасное желание, точно хочешь стать миллионером!", reply_markup=markup)
        else:
            bot.send_message(message.chat.id, f"{name_bot} не может помочь тебе")

@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    try:
        if call.data == "sure":
            bot.send_message(call.message.chat.id, emojize("Тогда регистрируйся дружище:smiling_face_with_sunglasses:"))
            bot.send_message(call.message.chat.id, "Промокод: Luckyman\n https://videoforme.ru/course/crypto-trading-courses")

        elif call.data == "change my mind":
            bot.send_message(call.message.chat.id, emojize("Как надумаешь возвращайся:smiling_face_with_halo:"))

            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Хочу начать зарабатывать!", reply_markup=False)


    except:
        bot.send_message(call.message.chat.id, f"{name_bot} не может помочь тебе")

if __name__ == '__main__':
    bot.polling(none_stop=True)
