import telebot
import instaloader
import os

BOT_TOKEN = "8388770582:AAGWe0_fg12fTmGQGqdQtkn-Rs1grQGgbDM"

bot = telebot.TeleBot(BOT_TOKEN)

loader = instaloader.Instaloader(
    download_comments=False,
    download_geotags=False,
    download_pictures=False,
    download_video_thumbnails=False,
    save_metadata=False
)

# start bosilganda
@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Assalomu alaykum. TIJEY STUDIOning Instagramdan video yuklaydigan botiga xush kelibsiz :) ")
    bot.send_message(message.chat.id, "Menga Intagramdagi videoning havolasini yuboring ")
    
@bot.message_handler(func=lambda message: True)
def echo_all(message):
    # habardagi urlni olish
    url = message.text

    # url togriligini tekshrsh
    try:
        shortcode = url.split("/")[-2]
    except IndexError:
        bot.reply_to(message, "❌Siz yuborgan Link notog‘ri! Tekshirib qaytadan yuboring")
        return

    try: 
        loader_message = bot.send_message(message.chat.id, "⏳Video yuklanyapti...")

        # videoni yuklash
        post = instaloader.Post.from_shortcode(loader.context, shortcode)
        loader.download_post(post, target=shortcode)

        # yuklangan vidoeni nomini aniqlash
        video_file = None
        for file in os.listdir(shortcode):
            if file.endswith(".mp4"):
                video_file = os.path.join(shortcode, file)
                break
        # videoni yuborish va comment
        if video_file:
    with open(video_file, "rb") as video:
        bot.send_video(
            message.chat.id,
            video,
            caption="🎥 Siz so‘ragan video tayyor!\n\n✨ @tijeystudio orqali yuklab olindi."
        )
    bot.delete_message(message.chat.id, loader_message.message_id)

            
            # va videoni ochirib tashlash
            for f in os.listdir(shortcode):
                os.remove(os.path.join(shortcode, f))
            os.rmdir(shortcode)
        else: 
            # agar video topilmasa
            bot.delete_message(message.chat.id, loader_message.message_id)
            bot.reply_to(message, "Video topilmadi")

    except Exception:
        # xatolik yuzb bersa
        bot.delete_message(message.chat.id, loader_message.message_id)
        bot.reply_to(message, "😐Video yuklashda xatolik yuz berdi")

while True:
    try:
        bot.infinity_polling(timeout=10, long_polling_timeout=5)
    except Exception as e:
        print(f"Xatolik: {e}")
        continue
