from deep_api import dpsk, close_chromedrivers
import time

# Закрываем старые процессы
close_chromedrivers()
time.sleep(2)

# Создаём подключение
ai = dpsk(
    "5Hyk2crRPU3BMu3dmqsOV34uhB9Df1Ce9CBmHHyRr11gcsxgAdN+jA3ca/XqExq2",  # Вставь новый токен
    prompt="Ты полезный ассистент",
    install_chromedriver=True
)

# Пробуем отправить запрос
print("Отправляю запрос...")
response = ai.chat("Привет! Как дела?")
print(f"Ответ: {response}")