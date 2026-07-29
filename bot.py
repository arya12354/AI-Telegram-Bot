import os
from openai import OpenAI
from telegram import Update
from telegram.ext import (
    Application,
    MessageHandler,
    CommandHandler,
    ContextTypes,
    filters
)


TELEGRAM_TOKEN = os.getenv("8765492194:AAEQMOhdXdquOy61rK_z-xk-Zg6Y0yq0VvI")
NVIDIA_API_KEY = os.getenv("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")


client = OpenAI(
    base_url="https://integrate.api.nvidia.com/v1",
    api_key=NVIDIA_API_KEY
)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "✅ ربات هوش مصنوعی Inkling فعال شد.\nپیامت را بفرست."
    )


async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user_text = update.message.text

    await update.message.reply_text("⏳ در حال پردازش...")


    try:

        response = client.chat.completions.create(
            model="thinkingmachines/inkling",
            messages=[
                {
                    "role": "user",
                    "content": user_text
                }
            ],
            temperature=0.7,
            max_tokens=2000
        )


        answer = response.choices[0].message.content


        await update.message.reply_text(answer)


    except Exception as e:

        await update.message.reply_text(
            f"❌ خطا:\n{e}"
        )



def main():

    app = Application.builder().token(
        TELEGRAM_TOKEN
    ).build()


    app.add_handler(
        CommandHandler("start", start)
    )


    app.add_handler(
        MessageHandler(
            filters.TEXT & ~filters.COMMAND,
            chat
        )
    )


    print("Bot Started...")


    app.run_polling()



if __name__ == "__main__":
    main()
