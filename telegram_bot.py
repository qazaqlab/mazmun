"""
Әдебиет Бот (Мазмұн мен Пішін) - Telegram Bot
Кітапхана: aiogram (3.x) немесе telebot

Орнату:
    pip install aiogram

Іске қосу:
    1. @BotFather арқылы Telegram бот жасап, TOKEN алыңыз.
    2. Төмендегі BOT_TOKEN айнымалысына қойыңыз.
    3. python telegram_bot.py арқылы іске қосыңыз.
"""

import asyncio
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import CommandStart
from aiogram.utils.keyboard import InlineKeyboardBuilder

BOT_TOKEN = "YOUR_BOT_TOKEN_HERE"

# 14 сұрақ пен жауап базасы
QUESTIONS_DATA = {
    1: {
        "q": "1. Әдеби шығармадағы мазмұн деген не?",
        "a": "📖 <b>1-жауап:</b>\n\nМазмұн — шығармада бейнеленген оқиғалар, кейіпкерлер, тақырып пен идея, сондай-ақ автордың көзқарасы мен бағалауының жиынтығы."
    },
    2: {
        "q": "2. Пішін дегеніміз не?",
        "a": "🎨 <b>2-жауап:</b>\n\nПішін — шығарма мазмұнының көркемдік тұрғыдан берілу жолы. Оған сюжет, кейіпкерлер бейнесі, тіл және басқа да көркемдік құралдар жатады."
    },
    3: {
        "q": "3. Мазмұн мен пішін қандай сұрақтарға жауап береді?",
        "a": "❓ <b>3-жауап:</b>\n\nМазмұн — «Шығармада не айтылды?», ал пішін — «Ол қалай айтылды?» деген сұрақтарға жауап береді."
    },
    4: {
        "q": "4. Мазмұн қалай қалыптасады?",
        "a": "✍️ <b>4-жауап:</b>\n\nҚаламгердің өмір құбылыстарын бейнелеуі, оқиғаларды баяндауы, маңызды құбылыстарды іріктеуі және оларға авторлық баға беруі арқылы қалыптасады."
    },
    5: {
        "q": "5. Бейнелеуші және баяндаушы бастаулар?",
        "a": "👁️ <b>5-жауап:</b>\n\nБейнелеуші бастау өмір құбылыстары мен кейіпкерлерді көрсетеді, ал баяндаушы бастау оқиғаларды жеткізіп, авторлық ой мен көзқарастың ашылуына көмектеседі."
    },
    6: {
        "q": "6. Неге оларды бөліп қарауға болмайды?",
        "a": "🔗 <b>6-жауап:</b>\n\nӨйткені мазмұн пішін арқылы көрініс табады, ал пішін мазмұнды жеткізеді. Екеуі бірігіп, шығарманың көркемдік тұтастығын қалыптастырады."
    },
    7: {
        "q": "7. Автордың субъективті көзқарасының әсері?",
        "a": "💡 <b>7-жауап:</b>\n\nАвтордың көзқарасы оқиғаларды іріктеуінен, кейіпкерлерді бағалауынан және негізгі идеяны жеткізуінен көрінеді."
    },
    8: {
        "q": "8. Фемида кім және нені білдіреді?",
        "a": "⚖️ <b>8-жауап:</b>\n\nФемида — ежелгі грек мифологиясындағы әділ қазылықтың символы."
    },
    9: {
        "q": "9. Фемиданың көзіндегі таңғыш нені білдіреді?",
        "a": "🙈 <b>9-жауап:</b>\n\nТаңғыш адамдардың бет-жүзіне, дәрежесіне қарамай, бәріне бірдей қарауды білдіреді."
    },
    10: {
        "q": "10. Фемиданың таразысы мен семсері нені білдіреді?",
        "a": "⚔️ <b>10-жауап:</b>\n\nТаразы — әділ бағалау мен өлшеудің, ал семсер — әділ шешімнің орындалуы мен жазаның символы."
    },
    11: {
        "q": "11. Фемида мысалындағы мазмұн мен пішін?",
        "a": "🏛️ <b>11-жауап:</b>\n\nМазмұн — әділ қазылық ұғымы. Пішін — Фемиданың бейнесі және оның қолындағы таңғыш, таразы мен семсер сияқты белгілер."
    },
    12: {
        "q": "12. Мазмұн күрделенген сайын пішін қандай болады?",
        "a": "📈 <b>12-жауап:</b>\n\nМазмұн күрделенген сайын оны толық әрі әсерлі жеткізетін пішін де бай, алуан түрлі болуы керек."
    },
    13: {
        "q": "13. Сюжет пен кейіпкерлер тілі қандай қызмет атқарады?",
        "a": "🗣️ <b>13-жауап:</b>\n\nСюжет оқиғалардың дамуын көрсетіп, шығарманың идеясын ашуға көмектеседі. Кейіпкерлердің тілі олардың мінезін, көзқарасын және дара ерекшелігін танытады."
    },
    14: {
        "q": "14. Өнердегі мазмұн мен пішіннің басты ерекшелігі?",
        "a": "🌟 <b>14-жауап:</b>\n\nОлардың басты ерекшелігі — образдылық. Өнер өмір шындығын көркем образдар, кейіпкерлер, оқиғалар мен тіл арқылы бейнелейді."
    }
}

def get_questions_keyboard():
    builder = InlineKeyboardBuilder()
    for q_id, data in QUESTIONS_DATA.items():
        builder.button(text=data["q"], callback_data=f"q_{q_id}")
    builder.adjust(1)  # Әр қатарда 1 сұрақ батырмасы
    return builder.as_markup()

dp = Dispatcher()

@dp.message(CommandStart())
async def start_handler(message: types.Message):
    welcome_text = (
        "Сәлеметсіз бе! 👋\n\n"
        "Мен әдебиет теориясының <b>«Мазмұн мен пішін»</b> тақырыбы бойынша ботпын.\n\n"
        "Төмендегі батырмалардың бірін басыңыз немесе сұрақтың нөмірін жіберіңіз (мысалы, 1):"
    )
    await message.answer(welcome_text, parse_mode="HTML", reply_markup=get_questions_keyboard())

@dp.callback_query(F.data.startswith("q_"))
async def answer_callback(callback: types.CallbackQuery):
    q_id = int(callback.data.split("_")[1])
    item = QUESTIONS_DATA.get(q_id)
    if item:
        builder = InlineKeyboardBuilder()
        builder.button(text="⬅️ Барлық сұрақтарға қайту", callback_data="back_to_menu")
        await callback.message.edit_text(
            f"<b>Сұрақ:</b> {item['q']}\n\n{item['a']}",
            parse_mode="HTML",
            reply_markup=builder.as_markup()
        )
    await callback.answer()

@dp.callback_query(F.data == "back_to_menu")
async def back_to_menu_callback(callback: types.CallbackQuery):
    await callback.message.edit_text(
        "Қай сұрақтың жауабын білгіңіз келеді? Төменнен таңдаңыз:",
        reply_markup=get_questions_keyboard()
    )
    await callback.answer()

@dp.message()
async def text_handler(message: types.Message):
    text = message.text.strip().lower()
    # Нөмір бойынша іздеу
    matched = None
    for q_id, data in QUESTIONS_DATA.items():
        if str(q_id) in text or data["q"].lower() in text:
            matched = data
            break
    
    if matched:
        await message.answer(matched["a"], parse_mode="HTML")
    else:
        await message.answer(
            "Төмендегі дайын батырмалар арқылы сұрақты таңдаңыз:",
            reply_markup=get_questions_keyboard()
        )

async def main():
    bot = Bot(token=BOT_TOKEN)
    print("Бот іске қосылды...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    # async/await арқылы ботты іске қосу
    asyncio.run(main())
