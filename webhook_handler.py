from flask import Flask, request
import telebot
import os
import threading
import time

# Токен бота
TOKEN = "8373227131:AAFBZpaMQ__XbP2rQXv2JnNVC_LuqBNfInc"

# Создаём Flask приложение
app = Flask(__name__)

# Создаём бота
bot = telebot.TeleBot(TOKEN)

# ===== ТВОИ ОБРАБОТЧИКИ КОМАНД =====
# Скопируй сюда все свои @bot.message_handler функции
# ============================================
# КОМАНДА /start (с кнопками)
# ============================================
@bot.message_handler(commands=['start'])
def start(message):
    name = message.from_user.first_name
    
    # Создаём клавиатуру с кнопками
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    
    # Создаём кнопки
    btn1 = types.KeyboardButton('💰 Курс валют')
    btn2 = types.KeyboardButton('🌤 Погода')
    btn3 = types.KeyboardButton('🎮 Игры')
    btn4 = types.KeyboardButton('😄 Анекдот')
    btn5 = types.KeyboardButton('🐱 Котик')
    btn6 = types.KeyboardButton('❓ Помощь')
    
    # Добавляем кнопки в клавиатуру
    markup.add(btn1, btn2, btn3, btn4, btn5, btn6)
    
    bot.send_message(message.chat.id, 
                    f"Привет, {name}! 👋\nЯ бот с кнопками. Выбирай что хочешь:", 
                    reply_markup=markup)

# ============================================
# ОБРАБОТКА ТЕКСТОВЫХ СООБЩЕНИЙ (кнопки)
# ============================================
@bot.message_handler(func=lambda message: True)
def handle_buttons(message):
    
    # ===== КУРС ВАЛЮТ =====
    if message.text == '💰 Курс валют':
        # Создаём инлайн-кнопки для выбора валюты
        markup = types.InlineKeyboardMarkup(row_width=2)
        btn_usd = types.InlineKeyboardButton('💵 Доллар', callback_data='usd')
        btn_eur = types.InlineKeyboardButton('💶 Евро', callback_data='eur')
        btn_cny = types.InlineKeyboardButton('💴 Юань', callback_data='cny')
        btn_back = types.InlineKeyboardButton('◀ Назад', callback_data='back_to_menu')
        markup.add(btn_usd, btn_eur, btn_cny, btn_back)
        
        bot.send_message(message.chat.id, "Выбери валюту:", reply_markup=markup)
    
    # ===== ПОГОДА =====
    elif message.text == '🌤 Погода':
        markup = types.InlineKeyboardMarkup()
        btn_moscow = types.InlineKeyboardButton('Калининград', callback_data='weather_kgd')
        btn_spb = types.InlineKeyboardButton('Москва', callback_data='weather_moscow')
        btn_other = types.InlineKeyboardButton('🌍 Другой город', callback_data='weather_other')
        btn_back = types.InlineKeyboardButton('◀ Назад', callback_data='back_to_menu')
        markup.add(btn_moscow, btn_spb, btn_other, btn_back)
        
        bot.send_message(message.chat.id, "Выбери город:", reply_markup=markup)
    
    # ===== ИГРЫ =====
    elif message.text == '🎮 Игры':
        markup = types.InlineKeyboardMarkup(row_width=2)
        btn_coin = types.InlineKeyboardButton('🪙 Монетка', callback_data='game_coin')
        btn_dice = types.InlineKeyboardButton('🎲 Кубик', callback_data='game_dice')
        btn_number = types.InlineKeyboardButton('🔢 Случайное число', callback_data='game_number')
        btn_back = types.InlineKeyboardButton('◀ Назад', callback_data='back_to_menu')
        markup.add(btn_coin, btn_dice, btn_number, btn_back)
        
        bot.send_message(message.chat.id, "🎰 Во что поиграем?", reply_markup=markup)
    
    # ===== АНЕКДОТ =====
    elif message.text == '😄 Анекдот':
        jokes = [
            "— Дорогой, я тут платье себе присмотрела...\n— Ну и сколько стоит это 'тут'?",
            "Встречаются два программиста:\n— Ты знаешь, моя жена меня не понимает.\n— А ты пробовал писать код с комментариями?",
            "— Доктор, я себя плохо чувствую.\n— А вы пробовали перезагрузиться?",
            "Лучший способ похудеть — есть только тогда, когда голоден. А голоден я всегда, когда вижу холодильник.",
            "— Что такое аллергия?\n— Это когда организм говорит «нет» тому, что ты ему предлагаешь.",
        ]
        bot.send_message(message.chat.id, f"😄 {random.choice(jokes)}")
        
        # Добавляем кнопку "Ещё"
        markup = types.InlineKeyboardMarkup()
        btn_more = types.InlineKeyboardButton('Ещё анекдот', callback_data='more_joke')
        markup.add(btn_more)
        bot.send_message(message.chat.id, "Хочешь ещё?", reply_markup=markup)
    
    # ===== КОТИК =====
    elif message.text == '🐱 Котик':
        try:
            response = requests.get("https://api.thecatapi.com/v1/images/search")
            data = response.json()
            cat_url = data[0]['url']
            bot.send_photo(message.chat.id, cat_url, caption="🐱 Лови котика!")
            
            # Кнопка для ещё одного котика
            markup = types.InlineKeyboardMarkup()
            btn_more = types.InlineKeyboardButton('Ещё котика', callback_data='more_cat')
            markup.add(btn_more)
            bot.send_message(message.chat.id, "Хочешь ещё?", reply_markup=markup)
        except:
            bot.send_message(message.chat.id, "😿 Котики временно недоступны")
    
    # ===== ПОМОЩЬ =====
    elif message.text == '❓ Помощь':
        help_text = """
📋 **Как пользоваться ботом:**

Просто нажимай на кнопки внизу экрана!

🔹 **Курс валют** - доллар, евро, юань
🔹 **Погода** - Москва, Питер или любой город
🔹 **Игры** - монетка, кубик, случайное число
🔹 **Анекдот** - поднять настроение
🔹 **Котик** - милые фото

Если кнопки пропали, напиши /start
        """
        bot.send_message(message.chat.id, help_text, parse_mode='Markdown')
    
    else:
        # Если написали что-то другое
        bot.send_message(message.chat.id, "Я не понимаю команду. Нажми на кнопку или напиши /start")


# ============================================
# ОБРАБОТКА НАЖАТИЙ НА ИНЛАЙН-КНОПКИ
# ============================================
@bot.callback_query_handler(func=lambda call: True)
def handle_callbacks(call):
    
    # ===== ВАЛЮТЫ =====
    if call.data == 'usd':
        try:
            response = requests.get("https://www.cbr-xml-daily.ru/daily_json.js")
            data = response.json()
            usd = data['Valute']['USD']['Value']
            bot.edit_message_text(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                text=f"💵 **Доллар США:** {usd:.2f} руб.",
                parse_mode='Markdown'
            )
        except:
            bot.send_message(call.message.chat.id, "😢 Ошибка получения курса")
    
    elif call.data == 'eur':
        try:
            response = requests.get("https://www.cbr-xml-daily.ru/daily_json.js")
            data = response.json()
            eur = data['Valute']['EUR']['Value']
            bot.edit_message_text(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                text=f"💶 **Евро:** {eur:.2f} руб.",
                parse_mode='Markdown'
            )
        except:
            bot.send_message(call.message.chat.id, "😢 Ошибка получения курса")
    
    elif call.data == 'cny':
        try:
            response = requests.get("https://www.cbr-xml-daily.ru/daily_json.js")
            data = response.json()
            cny = data['Valute']['CNY']['Value']
            bot.edit_message_text(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                text=f"💴 **Китайский юань:** {cny:.2f} руб.",
                parse_mode='Markdown'
            )
        except:
            bot.send_message(call.message.chat.id, "😢 Ошибка получения курса")
    
    # ===== ПОГОДА =====
    elif call.data == 'weather_moscow':
        try:
            response = requests.get("https://wttr.in/Moscow?format=%t+%c+%w+%h&lang=ru")
            bot.edit_message_text(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                text=f"🌤 **Погода в Москве:**\n{response.text.strip()}"
            )
        except:
            bot.send_message(call.message.chat.id, "😢 Ошибка получения погоды")
    
    elif call.data == 'weather_kgd':
        try:
            response = requests.get("https://wttr.in/Калининград?format=%t+%c+%w+%h&lang=ru")
            bot.edit_message_text(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                text=f"🌤 **Погода в Калининграде:**\n{response.text.strip()}"
            )
        except:
            bot.send_message(call.message.chat.id, "😢 Ошибка получения погоды")
    
    elif call.data == 'weather_other':
        msg = bot.send_message(call.message.chat.id, "Напиши название города:")
        bot.register_next_step_handler(msg, get_city_weather)
    
    # ===== ИГРЫ =====
    elif call.data == 'game_coin':
        result = random.choice(["Орёл 🦅", "Решка 🪙"])
        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text=f"🪙 **Монетка показала:** {result}",
            parse_mode='Markdown'
        )
    
    elif call.data == 'game_dice':
        result = random.randint(1, 6)
        dice_emoji = ["⚀", "⚁", "⚂", "⚃", "⚄", "⚅"][result-1]
        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text=f"🎲 **Кубик:** {result} {dice_emoji}",
            parse_mode='Markdown'
        )
    
    elif call.data == 'game_number':
        result = random.randint(1, 100)
        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text=f"🔢 **Случайное число:** {result}",
            parse_mode='Markdown'
        )
    
    # ===== ЕЩЁ АНЕКДОТ =====
    elif call.data == 'more_joke':
        jokes = [
            "Программист просыпается и говорит жене:\n— Дорогая, мне приснилось, что я удалил все твои фотки с телефона!\n— А они там были?\n— Сначала были...",
            "— Почему программисты путают Хэллоуин и Рождество?\n— Потому что 31 Oct = 25 Dec",
            "Вовочка: Мама, а почему папа лысый?\nМама: Потому что он много думает.\nВовочка: А почему ты такая лохматая?",
        ]
        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text=f"😄 {random.choice(jokes)}"
        )
    
    # ===== ЕЩЁ КОТИК =====
    elif call.data == 'more_cat':
        try:
            response = requests.get("https://api.thecatapi.com/v1/images/search")
            data = response.json()
            cat_url = data[0]['url']
            bot.send_photo(call.message.chat.id, cat_url, caption="🐱 Ещё котик!")
        except:
            bot.send_message(call.message.chat.id, "😿 Ошибка")
    
    # ===== НАЗАД В МЕНЮ =====
    elif call.data == 'back_to_menu':
        bot.delete_message(call.message.chat.id, call.message.message_id)
        bot.send_message(call.message.chat.id, "Выбери действие из меню внизу 👇")


# ============================================
# ФУНКЦИЯ ДЛЯ ПОГОДЫ ПО ЗАПРОСУ
# ============================================
def get_city_weather(message):
    city = message.text.strip()
    try:
        response = requests.get(f"https://wttr.in/{city}?format=%t+%c+%w+%h&lang=ru")
        if response.status_code == 200 and response.text.strip():
            bot.send_message(message.chat.id, f"🌤 **Погода в {city}:**\n{response.text.strip()}")
        else:
            bot.send_message(message.chat.id, "❌ Город не найден. Попробуй ещё раз через /start")
    except:
        bot.send_message(message.chat.id, "❌ Ошибка. Попробуй ещё раз через /start")

# ===== ВЕБХУК =====
@app.route(f'/{TOKEN}', methods=['POST'])
def webhook():
    update = telebot.types.Update.de_json(request.stream.read().decode('utf-8'))
    bot.process_new_updates([update])
    return 'OK', 200

@app.route('/')
def index():
    return 'Бот работает!', 200

# ===== ЗАПУСК =====
if __name__ == '__main__':
    # Удаляем старый вебхук
    bot.remove_webhook()
    time.sleep(1)
    
    # Устанавливаем новый вебхук (URL будет выглядеть как https://твой-бот.onrender.com/ТОКЕН)
    bot.set_webhook(url=f'https://твой-бот.onrender.com/{TOKEN}')
    
    # Запускаем Flask сервер
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))