#!/usr/bin/env python3
"""
🌱 DAILY GROWTH REMINDER BOT
Bot Telegram untuk mengingatkan 3 hal pengembangan diri setiap hari.

CARA SETUP:
1. Buat bot di Telegram via @BotFather → /newbot → salin TOKEN
2. Dapatkan CHAT_ID: kirim pesan ke bot, lalu buka:
   https://api.telegram.org/bot<TOKEN>/getUpdates
3. Isi TOKEN dan CHAT_ID di bawah
4. Install: pip install python-telegram-bot schedule
5. Jalankan: python telegram_reminder_bot.py
"""

import asyncio
import schedule
import time
import json
import os
from datetime import datetime
from telegram import Bot
from telegram.constants import ParseMode

# ============================================================
# ⚙️  KONFIGURASI - UBAH BAGIAN INI
# ============================================================
BOT_TOKEN = "8666695458:AAFg2I0Anm9mTrAY1DVrTKzk6W96uBi9xO0"
CHAT_ID   = "8713158763"

# File penyimpanan 3 hal harian
DATA_FILE = "growth_tasks.json"

# Jadwal pengingat (format 24 jam)
JADWAL = {
    "pagi":   "07:00",   # Semangat pagi + 3 tantangan hari ini
    "siang":  "12:00",   # Pengingat tengah hari
    "malam":  "20:00",   # Refleksi malam
}
# ============================================================

bot = Bot(token=BOT_TOKEN)


def load_tasks() -> dict:
    """Load 3 hal harian dari file JSON."""
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    # Default tasks jika file belum ada
    return {
        "tasks": [
            "📚 Baca buku / artikel selama 30 menit",
            "🏃 Olahraga atau gerak tubuh",
            "✍️  Refleksi & tulis jurnal harian"
        ],
        "updated": datetime.now().strftime("%Y-%m-%d")
    }


def save_tasks(tasks: list):
    """Simpan 3 hal harian ke file JSON."""
    data = {
        "tasks": tasks,
        "updated": datetime.now().strftime("%Y-%m-%d")
    }
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"✅ Tasks tersimpan: {tasks}")


async def kirim_pesan(teks: str):
    """Kirim pesan ke Telegram."""
    try:
        await bot.send_message(
            chat_id=CHAT_ID,
            text=teks,
            parse_mode=ParseMode.HTML
        )
        print(f"[{datetime.now().strftime('%H:%M')}] ✅ Pesan terkirim.")
    except Exception as e:
        print(f"[{datetime.now().strftime('%H:%M')}] ❌ Gagal kirim: {e}")


async def notifikasi_pagi():
    """Notifikasi semangat pagi dengan 3 tantangan hari ini."""
    data = load_tasks()
    tasks = data["tasks"]
    hari = datetime.now().strftime("%A, %d %B %Y")
    hari_id = {
        "Monday": "Senin", "Tuesday": "Selasa", "Wednesday": "Rabu",
        "Thursday": "Kamis", "Friday": "Jumat", "Saturday": "Sabtu", "Sunday": "Minggu"
    }
    nama_hari = hari_id.get(datetime.now().strftime("%A"), datetime.now().strftime("%A"))
    tanggal = datetime.now().strftime("%d %B %Y")

    pesan = (
        f"🌅 <b>Selamat Pagi!</b>\n"
        f"📅 {nama_hari}, {tanggal}\n\n"
        f"✨ <b>Hari ini kamu punya 3 misi untuk berkembang:</b>\n\n"
        f"1️⃣  {tasks[0]}\n"
        f"2️⃣  {tasks[1]}\n"
        f"3️⃣  {tasks[2]}\n\n"
        f"💪 <i>\"Setiap hari adalah kesempatan untuk menjadi versi terbaik dirimu.\"</i>\n\n"
        f"🚀 Ayo mulai! Kamu bisa! 🌱"
    )
    await kirim_pesan(pesan)


async def notifikasi_siang():
    """Pengingat tengah hari — cek progress."""
    data = load_tasks()
    tasks = data["tasks"]

    pesan = (
        f"☀️ <b>Pengingat Tengah Hari!</b>\n\n"
        f"Sudah setengah hari berlalu... 🕐\n"
        f"Bagaimana progress 3 misimu hari ini?\n\n"
        f"1️⃣  {tasks[0]}\n"
        f"2️⃣  {tasks[1]}\n"
        f"3️⃣  {tasks[2]}\n\n"
        f"✅ Tandai yang sudah selesai!\n"
        f"💡 <i>Konsistensi kecil setiap hari = perubahan besar dalam setahun.</i>"
    )
    await kirim_pesan(pesan)


async def notifikasi_malam():
    """Refleksi malam — evaluasi hari ini."""
    data = load_tasks()
    tasks = data["tasks"]

    pesan = (
        f"🌙 <b>Waktu Refleksi Malam</b>\n\n"
        f"Hari ini hampir selesai. Mari evaluasi:\n\n"
        f"1️⃣  {tasks[0]}\n"
        f"2️⃣  {tasks[1]}\n"
        f"3️⃣  {tasks[2]}\n\n"
        f"🤔 <b>Renungkan:</b>\n"
        f"• Berapa misi yang berhasil? 🎯\n"
        f"• Apa yang bisa lebih baik besok? 📈\n"
        f"• Apa yang kamu syukuri hari ini? 🙏\n\n"
        f"🌟 <i>Setiap langkah kecil tetap adalah kemajuan.</i>\n"
        f"Istirahat yang baik, besok kita tumbuh lagi! 💙"
    )
    await kirim_pesan(pesan)


async def notifikasi_minggu():
    """Rekap mingguan setiap Minggu malam."""
    pesan = (
        f"📊 <b>REKAP MINGGUAN 🗓️</b>\n\n"
        f"Selamat! Kamu telah melewati satu minggu lagi!\n\n"
        f"💭 <b>Pertanyaan Refleksi Minggu Ini:</b>\n\n"
        f"1. 🌱 Apa pertumbuhan terbesar yang kamu rasakan?\n"
        f"2. 🔥 Kebiasaan mana yang paling konsisten?\n"
        f"3. 🎯 Target apa yang ingin dicapai minggu depan?\n"
        f"4. 💪 Seberapa besar kamu sudah keluar dari zona nyaman?\n\n"
        f"🏆 <i>\"Versi terbaik dirimu sedang dalam proses.\"</i>\n\n"
        f"Terus semangat minggu depan! 🚀🌟"
    )
    await kirim_pesan(pesan)


def run_async(coro):
    """Helper untuk menjalankan coroutine dari schedule."""
    asyncio.run(coro)


def setup_jadwal():
    """Setup semua jadwal pengingat."""
    schedule.every().day.at(JADWAL["pagi"]).do(run_async, notifikasi_pagi())
    schedule.every().day.at(JADWAL["siang"]).do(run_async, notifikasi_siang())
    schedule.every().day.at(JADWAL["malam"]).do(run_async, notifikasi_malam())
    schedule.every().sunday.at("21:00").do(run_async, notifikasi_minggu())

    print("✅ Jadwal aktif:")
    print(f"   🌅 Pagi   : {JADWAL['pagi']}")
    print(f"   ☀️  Siang  : {JADWAL['siang']}")
    print(f"   🌙 Malam  : {JADWAL['malam']}")
    print(f"   📊 Mingguan: Minggu 21:00")


async def test_koneksi():
    """Test kirim pesan pertama saat bot dijalankan."""
    data = load_tasks()
    tasks = data["tasks"]
    pesan = (
        f"🤖 <b>Bot Pengingat Aktif!</b>\n\n"
        f"✅ Koneksi berhasil!\n\n"
        f"📋 <b>3 Misi Pengembangan Dirimu:</b>\n"
        f"1️⃣  {tasks[0]}\n"
        f"2️⃣  {tasks[1]}\n"
        f"3️⃣  {tasks[2]}\n\n"
        f"⏰ <b>Jadwal Pengingat:</b>\n"
        f"🌅 {JADWAL['pagi']} — Semangat Pagi\n"
        f"☀️  {JADWAL['siang']} — Cek Progress\n"
        f"🌙 {JADWAL['malam']} — Refleksi Malam\n"
        f"📊 Minggu 21:00 — Rekap Mingguan\n\n"
        f"🌱 <i>Selamat tumbuh dan berkembang!</i>"
    )
    await kirim_pesan(pesan)


if __name__ == "__main__":
    print("=" * 50)
    print("🌱 DAILY GROWTH REMINDER BOT")
    print("=" * 50)

    if BOT_TOKEN == "MASUKKAN_TOKEN_BOT_ANDA_DISINI":
        print("\n❌ ERROR: Harap isi BOT_TOKEN dan CHAT_ID terlebih dahulu!")
        print("   Lihat instruksi di bagian atas file ini.\n")
        exit(1)

    print("\n🔗 Menghubungkan ke Telegram...")
    asyncio.run(test_koneksi())

    print("\n⏰ Mengatur jadwal pengingat...")
    setup_jadwal()

    print("\n✅ Bot berjalan! Tekan Ctrl+C untuk menghentikan.\n")

    while True:
        schedule.run_pending()
        time.sleep(30)
