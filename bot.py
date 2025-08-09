import os
import yt_dlp
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

# ضع التوكن الخاص بك هنا
import os
TOKEN = os.getenv("TOKEN")

# أمر /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 أهلاً! أرسل لي رابط أي فيديو من تيك توك، فيسبوك، يوتيوب، أو إنستغرام لتحميله.")

# وظيفة التحميل
async def download_video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text.strip()

    # خيارات yt-dlp
    ydl_opts = {
        'outtmpl': 'video.%(ext)s',  # اسم الملف
        'format': 'best',            # أفضل جودة
    }

    await update.message.reply_text("⏳ جاري التحميل، انتظر قليلاً...")

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            file_name = ydl.prepare_filename(info)

        # إرسال الفيديو
        await update.message.reply_video(video=open(file_name, 'rb'))
        os.remove(file_name)

    except Exception as e:
        await update.message.reply_text(f"❌ حدث خطأ: {str(e)}")

# تشغيل البوت
app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, download_video))

print("🚀 البوت يعمل... اضغط Ctrl+C للإيقاف")
app.run_polling()
