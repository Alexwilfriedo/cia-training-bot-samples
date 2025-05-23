import os
from openai import OpenAI

from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv()
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')


# Message de bienvenue personnalisé
WELCOME_MESSAGE = (
    "👋 Bonjour et bienvenue !\n\n"
    "Je suis le bot *CIA Assistant*, spécialisé dans la **certification CIA (Certified Internal Auditor)**. "
    "Tu peux me poser toutes les questions en lien avec cette certification — que ce soit sur les parties, le programme, les exigences, ou les bonnes pratiques de préparation.\n\n"
    "Je ferai de mon mieux pour te répondre de manière claire et pertinente."
)


client = OpenAI(api_key=OPENAI_API_KEY)

# Handler pour la commande /start


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(WELCOME_MESSAGE)

# Fonction pour obtenir une réponse depuis ChatGPT


def get_chatgpt_response(question):
    system_context = (
        "Tu es un assistant spécialisé dans la certification CIA (Certified Internal Auditor). "
        "Toutes les réponses que tu donnes doivent être liées à ce domaine, incluant les examens, les contenus des parties, les pratiques d’audit, les exigences de l'IIA, etc."
    )

    response = client.chat.completions.create(model="gpt-4.1",
                                              messages=[{"role": "system", "content": system_context}, {
                                                  "role": "user", "content": question}],
    temperature=0.2,
    max_tokens=500)
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
