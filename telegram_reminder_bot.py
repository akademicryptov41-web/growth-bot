import asyncio
import schedule
import time
import os
from datetime import datetime
from telegram import Bot
from telegram.constants import ParseMode

BOT_TOKEN = os.environ.get("BOT_TOKEN")
CHAT_ID   = os.environ.get("CHAT_ID")

MISI = [
    "📚 Baca buku / artikel selama 30 menit",
    "🏃 Olahraga atau gerak tubuh minimal 20 menit",
    "✍️  Tulis jurnal refleksi harian",
]

JADWAL_PAGI  = "07:00"
JADWAL_SIANG = "12:00"
JADWAL_MALAM = "20:00"

HARI_ID = {
    "Monday":"Senin","Tuesday":"Selasa","Wednesday":"Rabu",
    "Thursday":"Kamis","Friday":"Jumat",
    "Saturday":"Sabtu","Sunday":"Minggu"
}

async def kirim(teks):
    try:
        bot = Bot(token=BOT_TOKEN)
        async with bot:
            await bot.send_message(
                chat_id=CHAT_ID,
                text=teks,
                parse_mode=ParseMode.HTML
            )
        print(f"[{datetime.now().strftime('%H:%M')}] ✅ Terkirim")
    except Exception as e:
        print(f"[{datetime.now().strftime('%H:%M')}] ❌ Error: {e}")

def nama_hari():
    return HARI_ID.get(datetime.now().strftime("%A"), "")

def tanggal():
    return datetime.now().strftime("%d %B %Y")

def notif_pagi():
    asyncio.run(kirim(
        f"🌅 <b>Selamat Pagi!</b>\n"
        f"📅 {nama_hari()}, {tanggal()}\n\n"
        f"✨ <b>3 Misi Hari Ini:</b>\n\n"
        f"1️⃣  {MISI[0]}\n"
        f"2️⃣  {MISI[1]}\n"
        f"3️⃣  {MISI[2]}\n\n"
        f"💪 <i>Setiap hari adalah kesempatan menjadi versi terbaik dirimu.</i>\n\n"
        f"🚀 Ayo mulai! Kamu pasti bisa! 🌱"
    ))

def notif_siang():
    asyncio.run(kirim(
        f"☀️ <b>Pengingat Tengah Hari!</b>\n\n"
        f"Sudah setengah hari berlalu... 🕐\n"
        f"Bagaimana progress 3 misimu?\n\n"
        f"1️⃣  {MISI[0]}\n"
        f"2️⃣  {MISI[1]}\n"
        f"3️⃣  {MISI[2]}\n\n"
        f"💡 <i>Konsistensi kecil setiap hari = perubahan besar dalam setahun.</i>"
    ))

def notif_malam():
    asyncio.run(kirim(
        f"🌙 <b>Waktu Refleksi Malam</b>\n\n"
        f"Hari ini hampir selesai. Mari evaluasi:\n\n"
        f"1️⃣  {MISI[0]}\n"
        f"2️⃣  {MISI[1]}\n"
        f"3️⃣  {MISI[2]}\n\n"
        f"🤔 <b>Renungkan:</b>\n"
        f"• Berapa misi yang berhasil? 🎯\n"
        f"• Apa yang bisa lebih baik besok? 📈\n"
        f"• Apa yang kamu syukuri hari ini? 🙏\n\n"
        f"🌟 <i>Setiap langkah kecil tetap adalah kemajuan.</i>\n"
        f"Istirahat baik, besok kita tumbuh lagi! 💙"
    ))

def notif_mingguan():
    asyncio.run(kirim(
        f"📊 <b>REKAP MINGGUAN</b> 🗓️\n\n"
        f"Selamat! Kamu telah melewati satu minggu lagi!\n\n"
        f"💭 <b>Pertanyaan Refleksi:</b>\n\n"
        f"1. 🌱 Apa pertumbuhan terbesar minggu ini?\n"
        f"2. 🔥 Misi mana yang paling konsisten?\n"
        f"3. 🎯 Target apa untuk minggu depan?\n"
        f"4. 💪 Sudah seberapa jauh keluar dari zona nyaman?\n\n"
        f"🏆 <i>Versi terbaik dirimu sedang dalam proses.</i>\n\n"
        f"Terus semangat minggu depan! 🚀🌟"
    ))

def notif_test():
    asyncio.run(kirim(
        f"🤖 <b>Bot Pengingat Aktif! ✅</b>\n\n"
        f"Bot sudah diperbaiki dan berjalan normal!\n\n"
        f"⏰ <b>Jadwal Notifikasi (WIB):</b>\n"
        f"🌅 {JADWAL_PAGI} — Semangat Pagi\n"
        f"☀️  {JADWAL_SIANG} — Cek Progress\n"
        f"🌙 {JADWAL_MALAM} — Refleksi Malam\n"
        f"📊 Minggu 21:00 — Rekap Mingguan\n\n"
        f"🌱 <i>Selamat tumbuh dan berkembang!</i>"
    ))

if __name__ == "__main__":
    print("🌱 BOT AKTIF")

    notif_test()

    schedule.every().day.at(JADWAL_PAGI).do(notif_pagi)
    schedule.every().day.at(JADWAL_SIANG).do(notif_siang)
    schedule.every().day.at(JADWAL_MALAM).do(notif_malam)
    schedule.every().sunday.at("21:00").do(notif_mingguan)

    print("✅ Jadwal aktif. Bot berjalan...\n")

    while True:
        schedule.run_pending()
        time.sleep(30)
