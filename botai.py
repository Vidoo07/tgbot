import telebot
from telebot import types
from openai import OpenAI
import requests
import random
import time

# ============================================
# НАСТРОЙКИ (ВСТАВЬ СВОИ ДАННЫЕ)
# ============================================
TELEGRAM_TOKEN = "5405510749:AAEBRA50OwaK17O9mA4LZTGbilOVVjPpp8w"  # Токен от BotFather
DEEPSEEK_API_KEY = "5Hyk2crRPU3BMu3dmqsOV34uhB9Df1Ce9CBmHHyRr11gcsxgAdN+jA3ca/XqExq2"  # Ключ от DeepSeek

# Инициализация Telegram бота
bot = telebot.TeleBot(TELEGRAM_TOKEN)

# Инициализация DeepSeek клиента (совместим с OpenAI API)
deepseek_client = OpenAI(
    api_key=DEEPSEEK_API_KEY,
    base_url="https://api.deepseek.com"  # Важно! Указываем URL DeepSeek
)

# Хранилище истории диалогов (для каждого пользователя)
user_conversations = {}

# ============================================
# КОМАНДА /start
# ============================================
@bot.message_handler(commands=['start'])
def start(message):
    name = message.from_user.first_name
    
    # Создаём клавиатуру
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    btn1 = types.KeyboardButton('🤖 Спросить DeepSeek')
    btn2 = types.KeyboardButton('💰 Курс валют')
    btn3 = types.KeyboardButton('🌤 Погода')
    btn4 = types.KeyboardButton('😄 Анекдот')
    btn5 = types.KeyboardButton('🐱 Котик')
    btn6 = types.KeyboardButton('❓ Помощь')
    markup.add(btn1, btn2, btn3, btn4, btn5, btn6)
    
    bot.send_message(message.chat.id, 
                    f"Привет, {name}! 👋\n"
                    f"Я бот на базе **DeepSeek** — мощного и недорогого ИИ!\n"
                    f"Можешь просто спросить меня о чём угодно или выбрать кнопку.", 
                    reply_markup=markup,
                    parse_mode='Markdown')

# ============================================
# ФУНКЦИЯ ЗАПРОСА К DEEPSEEK
# ============================================
def ask_deepseek(user_id, user_message):
    """Отправляет запрос к DeepSeek и возвращает ответ"""
    
    # Получаем историю диалога пользователя (или создаём новую)
    if user_id not in user_conversations:
        user_conversations[user_id] = [
            {"role": "system", "content": "Ты дружелюбный помощник в Telegram. Отвечай кратко, но по делу. Используй эмодзи."}
        ]
    
    # Добавляем сообщение пользователя в историю
    user_conversations[user_id].append({"role": "user", "content": user_message})
    
    # Ограничиваем историю последними 10 сообщениями
    if len(user_conversations[user_id]) > 11:
        user_conversations[user_id] = [user_conversations[user_id][0]] + user_conversations[user_id][-10:]
    
    try:
        # Отправляем запрос к DeepSeek
        response = deepseek_client.chat.completions.create(
            model="deepseek-chat",  # Модель DeepSeek
            messages=user_conversations[user_id],
            max_tokens=500,
            temperature=0.7
        )
        
        # Получаем ответ
        answer = response.choices[0].message.content
        
        # Добавляем ответ в историю
        user_conversations[user_id].append({"role": "assistant", "content": answer})
        
        return answer
        
    except Exception as e:
        print(f"Ошибка DeepSeek: {e}")
        return "😵 Извини, у меня временные проблемы с мозгами. Попробуй позже!"

# ============================================
# ОБРАБОТКА ТЕКСТОВЫХ СООБЩЕНИЙ
# ============================================
@bot.message_handler(func=lambda message: True)
def handle_all_messages(message):
    user_id = message.from_user.id
    text = message.text
    
    # ===== КНОПКА "СПРОСИТЬ DEEPSEEK" =====
    if text == '🤖 Спросить DeepSeek':
        bot.send_message(message.chat.id, 
                        "Задай мне любой вопрос! Я подключён к DeepSeek.\n"
                        "Например: расскажи о космосе, придумай тост, объясни квантовую физику...")
    
    # ===== КУРС ВАЛЮТ =====
    elif text == '💰 Курс валют':
        try:
            response = requests.get("https://www.cbr-xml-daily.ru/daily_json.js")
            data = response.json()
            usd = data['Valute']['USD']['Value']
            eur = data['Valute']['EUR']['Value']
            cny = data['Valute']['CNY']['Value']
            bot.send_message(message.chat.id, 
                           f"💵 Доллар: {usd:.2f} руб.\n"
                           f"💶 Евро: {eur:.2f} руб.\n"
                           f"💴 Юань: {cny:.2f} руб.")
        except:
            bot.send_message(message.chat.id, "😢 Не удалось получить курс валют")
    
    # ===== ПОГОДА =====
    elif text == '🌤 Погода':
        markup = types.InlineKeyboardMarkup()
        btn_moscow = types.InlineKeyboardButton('Москва', callback_data='weather_moscow')
        btn_spb = types.InlineKeyboardButton('СПб', callback_data='weather_spb')
        btn_other = types.InlineKeyboardButton('🌍 Другой город', callback_data='weather_other')
        markup.add(btn_moscow, btn_spb, btn_other)
        bot.send_message(message.chat.id, "Выбери город:", reply_markup=markup)
    
    # ===== АНЕКДОТ =====
    elif text == '😄 Анекдот':
        jokes = [
            "— Дорогой, я тут платье себе присмотрела...\n— Ну и сколько стоит это 'тут'?",
            "Встречаются два программиста:\n— Ты знаешь, моя жена меня не понимает.\n— А ты пробовал писать код с комментариями?",
            "— Доктор, я себя плохо чувствую.\n— А вы пробовали перезагрузиться?",
            "Лучший способ похудеть — есть только тогда, когда голоден. А голоден я всегда, когда вижу холодильник.",
        ]
        bot.send_message(message.chat.id, f"😄 {random.choice(jokes)}")
    
    # ===== КОТИК =====
    elif text == '🐱 Котик':
        try:
            response = requests.get("https://api.thecatapi.com/v1/images/search")
            data = response.json()
            cat_url = data[0]['url']
            bot.send_photo(message.chat.id, cat_url, caption="🐱 Лови котика!")
        except:
            bot.send_message(message.chat.id, "😿 Котики временно недоступны")
    
    # ===== ПОМОЩЬ =====
    elif text == '❓ Помощь':
        help_text = """
📋 **Как пользоваться ботом:**

🤖 **Спросить DeepSeek** - просто задай любой вопрос
💰 **Курс валют** - доллар, евро, юань
🌤 **Погода** - Москва, Питер или любой город
😄 **Анекдот** - поднять настроение
🐱 **Котик** - милые фото

Или просто **напиши мне что угодно** - я отвечу как DeepSeek!
        """
        bot.send_message(message.chat.id, help_text, parse_mode='Markdown')
    
    # ===== ЛЮБОЙ ДРУГОЙ ТЕКСТ (ОТПРАВЛЯЕМ В DEEPSEEK) =====
    else:
        # Показываем, что бот печатает
        bot.send_chat_action(message.chat.id, 'typing')
        
        # Отправляем запрос к DeepSeek
        answer = ask_deepseek(user_id, text)
        
        # Отправляем ответ
        bot.send_message(message.chat.id, answer)

# ============================================
# ОБРАБОТКА ИНЛАЙН-КНОПОК
# ============================================
@bot.callback_query_handler(func=lambda call: True)
def handle_callbacks(call):
    
    if call.data == 'weather_moscow':
        try:
            response = requests.get("https://wttr.in/Moscow?format=%t+%c+%w+%h&lang=ru")
            bot.edit_message_text(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                text=f"🌤 **Погода в Москве:**\n{response.text.strip()}"
            )
        except:
            bot.send_message(call.message.chat.id, "😢 Ошибка получения погоды")
    
    elif call.data == 'weather_spb':
        try:
            response = requests.get("https://wttr.in/Санкт-Петербург?format=%t+%c+%w+%h&lang=ru")
            bot.edit_message_text(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                text=f"🌤 **Погода в Санкт-Петербурге:**\n{response.text.strip()}"
            )
        except:
            bot.send_message(call.message.chat.id, "😢 Ошибка получения погоды")
    
    elif call.data == 'weather_other':
        msg = bot.send_message(call.message.chat.id, "Напиши название города:")
        bot.register_next_step_handler(msg, get_city_weather)

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
            bot.send_message(message.chat.id, "❌ Город не найден. Попробуй ещё раз")
    except:
        bot.send_message(message.chat.id, "❌ Ошибка. Попробуй ещё раз")

# ============================================
# ЗАПУСК БОТА
# ============================================
print("🚀 Бот с DeepSeek запущен!")
print(f"🤖 Модель: deepseek-chat")
print(f"💬 Жду сообщения...")

if __name__ == "__main__":
    bot.polling(none_stop=True)