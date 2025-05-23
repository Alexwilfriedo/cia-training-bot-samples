import os
import openai
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv()
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

openai.api_key = OPENAI_API_KEY

# Message de bienvenue personnalisé
WELCOME_MESSAGE = (
    "👋 Bonjour ! Je suis le bot CIA 🤖.\n\n"
    "Je t'aide dans ta maîtrise des sujets relatifs au CIA. "
    "Tu peux me poser toutes tes questions et je ferai de mon mieux pour y répondre."
)

# Handler pour la commande /start


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(WELCOME_MESSAGE)

# Fonction pour obtenir une réponse depuis ChatGPT


def get_chatgpt_response(question):
    response = openai.ChatCompletion.create(
        model="gpt-4-turbo",
        messages=[{"role": "user", "content": question}],
        temperature=0.2,
        max_tokens=500,
    )
    return response.choices[0].message.content.strip()

# Handler pour gérer tous les messages utilisateurs


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    question = update.message.text
    await update.message.chat.send_action(action="typing")
    answer = get_chatgpt_response(question)
    await update.message.reply_text(answer)

# Fonction principale pour lancer le bot
if __name__ == "__main__":
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    # Commande de démarrage
    app.add_handler(CommandHandler("start", start))

    # Message handler pour toutes les autres questions
    app.add_handler(MessageHandler(
        filters.TEXT & (~filters.COMMAND), handle_message))

    print("🤖 Le bot Telegram CIA est en ligne et prêt à répondre !")
    app.run_polling()
