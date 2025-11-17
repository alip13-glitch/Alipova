import telebot
from config import API_KEY

bot = telebot.TeleBot(API_KEY)


# База данных для хранения отзывов (временная, для демонстрации)
reviews = {}
popular_games = [
    "🎮 The Witcher 3: Wild Hunt",
    "🎮 Grand Theft Auto V",
    "🎮 The Legend of Zelda: Breath of the Wild",
    "🎮 Red Dead Redemption 2",
    "🎮 Minecraft",
    "🎮 Cyberpunk 2077",
    "🎮 Elden Ring",
    "🎮 God of War"
]


@bot.message_handler(commands=['start'])
def start(message):
    welcome_text = """🕹️ Добро пожаловать в магазин видео-игр!

Доступные команды:
/games - популярные видеоигры
/review - оставить отзыв об игре
/reviews - посмотреть отзывы
/help - список всех команд"""

    bot.send_message(message.chat.id, text=welcome_text)


@bot.message_handler(commands=['about'])
def about(message):
    about_text = """🏪 О нашем магазине:
Мы предлагаем лучшие видеоигры по доступным ценам!
Широкий ассортимент, акции и скидки."""

    bot.send_message(message.chat.id, text=about_text)


@bot.message_handler(commands=['help'])
def help_command(message):
    help_text = """📋 Список команд:

/start - запуск бота
/about - описание магазина  
/games - популярные видеоигры
/review - оставить отзыв об игре
/reviews - посмотреть отзывы
/help - список команд"""

    bot.send_message(message.chat.id, text=help_text)


@bot.message_handler(commands=['games'])
def show_games(message):
    games_text = "🎯 Популярные видеоигры:\n\n" + "\n".join(popular_games)
    games_text += "\n\nЧтобы оставить отзыв, используйте команду /review"
    bot.send_message(message.chat.id, text=games_text)


@bot.message_handler(commands=['review'])
def start_review(message):
    msg = bot.send_message(message.chat.id,
                           "📝 Напишите название игры и ваш отзыв через дефис:\nНапример: The Witcher 3 - Отличная игра!")
    bot.register_next_step_handler(msg, save_review)


def save_review(message):
    try:
        if '-' in message.text:
            game_name, review_text = message.text.split('-', 1)
            game_name = game_name.strip()
            review_text = review_text.strip()

            if game_name not in reviews:
                reviews[game_name] = []

            reviews[game_name].append({
                'user': message.from_user.first_name,
                'text': review_text
            })

            bot.send_message(message.chat.id, f"✅ Спасибо за отзыв об игре '{game_name}'!")
        else:
            bot.send_message(message.chat.id, "❌ Пожалуйста, используйте формат: Название игры - ваш отзыв")
    except Exception as e:
        bot.send_message(message.chat.id, "❌ Произошла ошибка. Попробуйте еще раз.")


@bot.message_handler(commands=['reviews'])
def show_reviews(message):
    if not reviews:
        bot.send_message(message.chat.id, "📝 Пока нет отзывов. Будьте первым!")
        return

    reviews_text = "📋 Отзывы об играх:\n\n"

    for game, game_reviews in reviews.items():
        reviews_text += f"🎮 {game}:\n"
        for i, review in enumerate(game_reviews, 1):
            reviews_text += f"  {i}. {review['user']}: {review['text']}\n"
        reviews_text += "\n"

    bot.send_message(message.chat.id, reviews_text)


@bot.message_handler(content_types=['text'])
def handle_text(message):
    bot.send_message(message.chat.id, "❓ Неизвестная команда. Используйте /help для списка команд.")


if __name__ == "__main__":
    print("Бот запущен...")
    bot.polling()