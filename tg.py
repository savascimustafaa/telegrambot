import datetime
import pytz  # Zaman dilimi ayarı için
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler

# --- AYARLAR ---
TOKEN = "8915997234:AAH_MywwUF_df-7o63BiHwROXSIsSGKB04Q"
SAAT = 9
DAKIKA = 0
ZAMAN_DILIMI = pytz.timezone('Europe/Istanbul') 

# 1. Her sabah çalışacak olan fonksiyon
async def gunaydin_mesaji(context: ContextTypes.DEFAULT_TYPE):
    job = context.job
    await context.bot.send_message(
        chat_id=job.chat_id, 
        text="☀️ Günaydın! Bugün harika bir gün olacak. İşte senin için sabah özeti..."
    )

# 2. Zamanlayıcıyı başlatan komut (/baslat)
async def baslat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_message.chat_id
    
    # 1. HEMEN ŞİMDİ BİR MESAJ AT (Test için)
    await update.message.reply_text("✅ Kaydını aldım! Şimdi bir test mesajı gönderiyorum. Bundan sonra her sabah 09:00'da görüşürüz! ☀️")

    # 2. SABAH 9 İÇİN AJANDAYA KAYDET
    target_time = datetime.time(hour=SAAT, minute=DAKIKA, tzinfo=ZAMAN_DILIMI)
    context.job_queue.run_daily(
        gunaydin_mesaji, 
        time=target_time, 
        chat_id=chat_id, 
        name=str(chat_id)
    )

    await update.message.reply_text(
        f"✅ Başarılı! Her sabah saat {SAAT:02d}:{DAKIKA:02d}'da sana günaydın mesajı atacağım."
    )

if __name__ == '__main__':
    # JobQueue özelliğini aktif ederek uygulamayı başlatıyoruz
    app = ApplicationBuilder().token(TOKEN).build()

    # Komutları ekliyoruz
    app.add_handler(CommandHandler("start", baslat))
    app.add_handler(CommandHandler("baslat", baslat))

    print("Bot çalışıyor... Her sabah 09:00'da mesaj atmak için hazır.")
    app.run_polling()