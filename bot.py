import yt_dlp
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackContext, MessageHandler, Filters

TOKEN = "7652198177:AAGrlaR1J2E7nKm2158N7VSlCo_kqe_qpqs"

def start(update: Update, context: CallbackContext):
    keyboard = [
        [InlineKeyboardButton("📥 Download YouTube Video", callback_data='download_video')],
        [InlineKeyboardButton("🎵 Download YouTube Song", callback_data='download_audio')],
        [InlineKeyboardButton("🎬 Download Movie / TV Series", callback_data='download_movie')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text("Welcome! Choose an option below:", reply_markup=reply_markup)

def button_click(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()
    if query.data == "download_video":
        query.edit_message_text("Send me a YouTube link to download the video!")
    elif query.data == "download_audio":
        query.edit_message_text("Send me a YouTube link to download the song!")

def download_youtube(update: Update, context: CallbackContext):
    url = update.message.text
    keyboard = [
        [InlineKeyboardButton("🔹 1080p", callback_data=f"quality_1080p_{url}")],
        [InlineKeyboardButton("🔹 720p", callback_data=f"quality_720p_{url}")],
        [InlineKeyboardButton("🔹 480p", callback_data=f"quality_480p_{url}")],
        [InlineKeyboardButton("🔹 MP3", callback_data=f"quality_mp3_{url}")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text("Select the quality:", reply_markup=reply_markup)

def download_selected_quality(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()
    data = query.data.split("_")
    quality = data[1]
    url = data[2]

    update.callback_query.message.reply_text("Downloading... Please wait.")

    ydl_opts = {
        'outtmpl': 'downloaded_video.%(ext)s',
    }

    if quality == "1080p":
        ydl_opts['format'] = 'bestvideo[height<=1080]+bestaudio/best'
    elif quality == "720p":
        ydl_opts['format'] = 'bestvideo[height<=720]+bestaudio/best'
    elif quality == "480p":
        ydl_opts['format'] = 'bestvideo[height<=480]+bestaudio/best'
    elif quality == "mp3":
        ydl_opts['format'] = 'bestaudio/best'
        ydl_opts['postprocessors'] = [{'key': 'FFmpegExtractAudio', 'preferredcodec': 'mp3', 'preferredquality': '192'}]

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

    file_extension = "mp3" if quality == "mp3" else "mp4"
    update.callback_query.message.reply_text("Download complete! Sending file...")
    update.callback_query.message.reply_video(video=open(f"downloaded_video.{file_extension}", "rb"))

def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, download_youtube))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, download_selected_quality))
    
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()