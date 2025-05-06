import os
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

API_URL = "https://api.exchangerate.host/convert"
TOKEN = os.getenv("BOT_TOKEN")
APP_URL = os.getenv("APP_URL")  # ejemplo: https://tu-nombre.onrender.com

async def convert(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        amount = float(context.args[0])
        response = requests.get(API_URL, params={"from": "JPY", "to": "EUR", "amount": amount})
        data = response.json()
        result = data["result"]
        await update.message.reply_text(f"{amount} JPY = {result:.2f} EUR")
    except (IndexError, ValueError):
        await update.message.reply_text("Por favor, usa el comando así: /yen 1000")
    except Exception as e:
        await update.message.reply_text(f"Error al convertir: {e}")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("¡Hola! Usa /yen <cantidad> para convertir a euros.")

def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("yen", convert))

    app.run_webhook(
        listen="0.0.0.0",
        port=int(os.environ.get("PORT", 5000)),
        webhook_url=f"{APP_URL}/webhook/{TOKEN}"
    )

if __name__ == "__main__":
    main()
