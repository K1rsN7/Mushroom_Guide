# -*- coding: utf-8 -*-
# Подключение бота
import os
import numpy as np
from aiogram import Bot, Dispatcher, executor, types
from tensorflow import keras
from PIL import Image

API_TOKEN = '6358373859:AAGD1m4DIZN5pkaCS00zrKYSteSLycMtulw'  # Токен бота

path = 'C:\\K1rsN7\\IT\\Pet project mushrooms\\photos'  # Путь к фото

# Объявление бота
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
classes = ['No mushrooms', 'Edible', 'Hallucinogenic', 'Inedible', 'Poisonous']


def predict_mushrooms():
    result = []
    for name_img in os.listdir(path):
        img = Image.open(f'{path}\\{name_img}')
        img = img.convert('RGB')
        img = img.resize((224, 224))
        img_array = keras.preprocessing.image.img_to_array(img)
        img_array = np.expand_dims(img_array, axis=0)
        final_img = keras.applications.densenet.preprocess_input(img_array)
        model = keras.models.load_model('my_model.h5')
        result.append(np.argmax(model.predict(final_img)))
        os.remove(os.path.join(path, name_img))
    return result


# Реакция на команду старт
@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await message.reply("Hello! I can tell the type of mushroom from the photo. "
                        "At the moment, I can say that the mushroom is: edible, inedible, poisonous or hallucinogenic.")


# Реакция бота на команду помощи
@dp.message_handler(commands=['help'])
async def process_help_command(message: types.Message):
    await message.reply("Send me a photo of the mushroom, and I'll tell you whether you can eat it or not.")


# Реакция бота на фото
@dp.message_handler(content_types=['photo'])
async def handle_docs_photo(message):
    await message.photo[-1].download()
    predict = predict_mushrooms()
    for number_predict in predict:
        if number_predict == 0:
            await message.reply("I didn't find any mushrooms in the photo.")
        else:
            await message.reply("I found mushrooms in the photo.\n"
                                f"This mushroom belongs to the species: {classes[number_predict]}")


# Реакция бота на случайное сообщение
@dp.message_handler()
async def process_help_command(message: types.Message):
    await message.reply("I'm sorry, but I'm just a bot for identifying mushrooms and I don't understand you :(\n"
                        "Send me a photo of the mushroom, and I'll tell you whether you can eat it or not.")


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
