import datetime
import requests
import telebot
import textwrap

open_weather_token = '36be4fbd051fa5cd63f4f5c972328481'
API_KEY = '5614300837:AAEBTPkZtCKUce97aIbf10xZvkmOhaOEE80'

bot = telebot.TeleBot(API_KEY)


@bot.message_handler(commands=['start'])
def hello(message):
    bot.send_message(message.chat.id, 'Приветик! Введите имя вашего города, чтобы узнать текущую погоду:')


@bot.message_handler(func=lambda message: True)
def get_weather(message):
    code_to_smile = {
        "Clear": "Ясно ☀️",
        "Clouds": "Облачно ☁️",
        "Rain": "Дождь 🌧️",
        "Drizzle": "Дождь 🌧️",
        "Thunderstorm": "Гроза ⛈️",
        "Snow": "Снег 🌨️",
        "Mist": "Туман 🌫️"
    }

    try:
        r = requests.get(
            f"http://api.openweathermap.org/data/2.5/weather?q={message.text}&appid={open_weather_token}&units=metric"
        )
        data = r.json()

        city = data["name"]
        cur_weather = data["main"]["temp"]

        weather_description = data["weather"][0]["main"]
        if weather_description in code_to_smile:
            wd = code_to_smile[weather_description]
        else:
            wd = "Ну тут уже сам разбирайся, что у тебя там происходит!"

        humidity = data["main"]["humidity"]
        pressure = data["main"]["pressure"]
        wind = data["wind"]["speed"]
        sunrise_timestamp = datetime.datetime.fromtimestamp(data["sys"]["sunrise"])
        sunset_timestamp = datetime.datetime.fromtimestamp(data["sys"]["sunset"])
        length_of_day = datetime.datetime.fromtimestamp(data["sys"]["sunset"]) - datetime.datetime.fromtimestamp(
            data["sys"]["sunrise"])

        weather_str = f"---------{datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}---------\n" \
                      f"Погода в городе: {city}\nТемпература: {cur_weather}C° {wd}\n" \
                      f"Влажность: {humidity}%\nДавление: {pressure} мм.рт.ст\nВетер: {wind} м/с\n" \
                      f"Восход солнца: {sunrise_timestamp}\nЗакат солнца: {sunset_timestamp}\nПродолжительность дня: {length_of_day}\n" \
                      f"---------Хорошего дня!---------"


        bot.send_message(message.chat.id, {weather_str})

    except:
        bot.send_message(message.chat.id, "\U00002620 Название города не верно, проверьте правильность написания! \U00002620")


if __name__ == '__main__':
    bot.polling()

#