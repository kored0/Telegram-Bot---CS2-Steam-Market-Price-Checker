# Telegram Bot - CS2 Steam Market Price Checker

Telegram бот для поиска цен предметов CS2 на торговой площадке Steam.

## 🚀 Функционал

- Поиск цен предметов CS2
- Отображение информации о предметах
- Поддержка административных команд

## 📋 Требования

- Python 3.8+
- Telegram Bot Token

## 🔧 Установка

1. Клонируйте репозиторий:
```bash
git clone https://github.com/kored0/Telegram-Bot---CS2-Steam-Market-Price-Checker
cd Telegram-Bot---CS2-Steam-Market-Price-Checker
```

2. Создайте виртуальное окружение:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

3. Установите зависимости:
```bash
pip install -r requirements.txt
```

4. Создайте файл `.env` на основе `.env.example`:
```bash
    cp .env.example .env
    ```

5. Заполните `.env` своими данными:
```env
BOT_TOKEN=ваш_токен_бота
ADMIN_ID=ваш_telegram_id
```

## ▶️ Запуск
```bash
python main.py
```

## 🤝 Вклад

Pull requests приветствуются!

## 📝 Лицензия

MIT License
