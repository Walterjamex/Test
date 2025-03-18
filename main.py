import os
import random
import openai
import asyncio
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, CommandHandler, ContextTypes

# Configurar API Keys
openai.api_key = os.getenv("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")
TOKEN = os.getenv("8140584479:AAGh3VDJROpHC3oG0pv2jHQK4TE1dIIY")

if not openai.api_key or not TOKEN:
    raise ValueError("Faltan las variables de entorno OPENAI_API_KEY y TELEGRAM_TOKEN")

# Lista de emojis posibles
emojis_lista = ["💼", "🚀", "😊", "✨", "📈", "💡", "🔥", "🙌", "🤖", "💰"]

# Almacenar el historial de conversación por usuario
user_conversations = {}

# Función para obtener respuesta de ChatGPT con memoria de contexto
async def chatgpt_response(user_id, text):
    if user_id not in user_conversations:
        user_conversations[user_id] = []

    # Agregar el mensaje del usuario al historial
    user_conversations[user_id].append({"role": "user", "content": text})

    # Limitar la memoria a los últimos 10 mensajes para evitar demasiado consumo de tokens
    if len(user_conversations[user_id]) > 10:
        user_conversations[user_id] = user_conversations[user_id][-10:]

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=user_conversations[user_id]
    )

    # Obtener respuesta y agregarla al historial
    bot_response = response["choices"][0]["message"]["content"]
    user_conversations[user_id].append({"role": "assistant", "content": bot_response})

    return bot_response

# Función de bienvenida
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("¡Hola! Soy un asistente inteligente de Upwork y trabajo remoto. Puedes preguntarme lo que quieras y responderé con base en el contexto. 😊")

# Función para manejar cualquier mensaje
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text
    user_id = update.message.chat_id

    # Obtener respuesta de ChatGPT con contexto
    ai_response = await chatgpt_response(user_id, user_message)

    # 50% de probabilidad de agregar un emoji al final
    if random.random() < 0.5:
        ai_response += f" {random.choice(emojis_lista)}"

    await update.message.reply_text(ai_response)

# Iniciar el bot
async def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("Bot iniciado... Esperando mensajes.")
    await app.run_polling()

if __name__ == "__main__":
    asyncio.run(main())u