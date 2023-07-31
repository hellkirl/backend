from telegram import ForceReply, Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
    Application,
    MessageHandler,
    filters,
)
from config import TOKEN


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    await update.message.reply_html(
        rf"Hi, {user.mention_html()}!",
        reply_markup=ForceReply(selective=True),
    )


async def contacts(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /help is issued."""
    await update.message.reply_text("You can contact us via phone - X XXX XXXXXXXX or via e-mail - reservation@bot.com")


async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """to be continued"""
    await update.message.reply_text("Hi!")


def main(token: str) -> None:
    application = Application.builder().token(token).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("contacts", contacts))

    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main(TOKEN)
