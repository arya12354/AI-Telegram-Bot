import os
from openai import OpenAI
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters
)


# دریافت کلیدها از Railway Variables
TELEGRAM_TOKEN = os.environ.get("8852051053:AAGtQNiwmIcCGJ2xcKVIkda7hsNxsic03_o")
NVIDIA_API_KEY = os.environ.get("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")


# بررسی کلیدها
if not TELEGRAM_TOKEN:
    raise Exception("TELEGRAM_TOKEN پیدا نشد")

if not NVIDIA_API_KEY:
    raise Exception("NVIDIA_API_KEY پیدا نشد")


# اتصال به NVIDIA Inkling
client = OpenAI(
    base_url="https://integrate.api.nvidia.com/v1",
    api_key=NVIDIA_API_KEY
)


# دستور شروع
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "✅ ربات Inkling فعال شد.\nپیام خود را ارسال کنید."
    )


# دریافت پیام و ارسال به Inkling
async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user_message = update.message.text

    await update.message.reply_text("⏳ در حال فکر کردن...")


    try:

        response = client.chat.completions.create(
            model="thinkingmachines/inkling",
            messages=[
                {
                    "role": "user",
                    "content": user_message
                }
            ],
            temperature=0.7,
            max_tokens=2000
        )


        answer = response.choices[0].message.content


        await update.message.reply_text(
            answer
        )


    except Exception as e:

        await update.message.reply_text(
            f"❌ خطا از Inkling:\n{e}"
        )



# اجرای ربات
def main():

    app = Application.builder().token(
        TELEGRAM_TOKEN
    ).build()


    app.add_handler(
        CommandHandler(
            "start",
            start
        )
    )


    app.add_handler(
        MessageHandler(
            filters.TEXT & ~filters.COMMAND,
            chat
        )
    )


    print("Bot Started Successfully")


    app.run_polling()



if __name__ == "__main__":
    main()
