import asyncio
import logging
import os
import random

from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command, CommandStart
from aiogram.types import (
    CallbackQuery,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Message,
)

from data import LEVELS, WORDS

TOKEN = os.getenv("BOT_TOKEN")
if not TOKEN:
    raise SystemExit("BOT_TOKEN topilmadi. Avval: export BOT_TOKEN='tokeningiz'")

logging.basicConfig(level=logging.INFO)
dp = Dispatcher()

# Foydalanuvchi test holati (oddiy xotirada): {user_id: {...}}
STATE: dict[int, dict] = {}


def norm(text: str) -> str:
    """Apostrof turlarini birxillashtirib, kichik harfga o'tkazadi."""
    for ch in ("ʻ", "ʼ", "’", "‘", "`", "'"):
        text = text.replace(ch, "'")
    return text.lower().strip()


def main_menu() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📝 Testlar", callback_data="menu:tests")],
        [InlineKeyboardButton(text="📖 Lug'at", callback_data="menu:dict")],
    ])


def levels_menu() -> InlineKeyboardMarkup:
    rows = [[InlineKeyboardButton(text=v["title"], callback_data=f"lvl:{k}")]
            for k, v in LEVELS.items()]
    rows.append([InlineKeyboardButton(text="⬅️ Orqaga", callback_data="menu:main")])
    return InlineKeyboardMarkup(inline_keyboard=rows)


def question_kb(level: str, qi: int) -> InlineKeyboardMarkup:
    q = LEVELS[level]["questions"][qi]
    rows = [[InlineKeyboardButton(text=opt, callback_data=f"ans:{level}:{qi}:{oi}")]
            for oi, opt in enumerate(q["o"])]
    return InlineKeyboardMarkup(inline_keyboard=rows)


def question_text(level: str, qi: int) -> str:
    total = len(LEVELS[level]["questions"])
    q = LEVELS[level]["questions"][qi]
    return f"{LEVELS[level]['title']}\n\nSavol {qi + 1}/{total}\n\n{q['q']}"


def format_word(w: tuple) -> str:
    word, pos, meaning, example = w
    return (f"📖 <b>{word}</b> ({pos})\n\n"
            f"<b>Maʼnosi:</b> {meaning}\n"
            f"<b>Misol:</b> <i>{example}</i>")


def search_words(query: str) -> list[tuple]:
    q = norm(query)
    exact = [w for w in WORDS if norm(w[0]) == q]
    if exact:
        return exact
    starts = [w for w in WORDS if norm(w[0]).startswith(q)]
    if starts:
        return starts
    return [w for w in WORDS if q in norm(w[0])]


@dp.message(CommandStart())
async def start(message: Message):
    await message.answer(
        "Assalomu alaykum! 👋\n\n"
        "Men ona tilini 0 dan oʻrganishda yordam beraman:\n"
        "📝 daraja-daraja testlar\n"
        "📖 lugʻat — soʻz yozing, maʼnosini topaman\n\n"
        "Nimadan boshlaymiz?",
        reply_markup=main_menu(),
    )


@dp.message(Command("menu"))
async def menu_cmd(message: Message):
    await message.answer("Asosiy menyu:", reply_markup=main_menu())


@dp.callback_query(F.data == "menu:main")
async def cb_main(call: CallbackQuery):
    await call.message.edit_text("Asosiy menyu:", reply_markup=main_menu())
    await call.answer()


@dp.callback_query(F.data == "menu:tests")
async def cb_tests(call: CallbackQuery):
    await call.message.edit_text("Darajani tanlang:", reply_markup=levels_menu())
    await call.answer()


@dp.callback_query(F.data == "menu:dict")
async def cb_dict(call: CallbackQuery):
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🎲 Tasodifiy soʻz", callback_data="dict:random")],
        [InlineKeyboardButton(text="⬅️ Orqaga", callback_data="menu:main")],
    ])
    await call.message.edit_text(
        "📖 Lugʻat\n\nQidirish uchun soʻzni yozib yuboring (masalan: <b>ona</b>).",
        reply_markup=kb,
        parse_mode="HTML",
    )
    await call.answer()


@dp.callback_query(F.data == "dict:random")
async def cb_random(call: CallbackQuery):
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🎲 Yana", callback_data="dict:random")],
        [InlineKeyboardButton(text="⬅️ Orqaga", callback_data="menu:dict")],
    ])
    await call.message.edit_text(
        format_word(random.choice(WORDS)), reply_markup=kb, parse_mode="HTML"
    )
    await call.answer()


@dp.callback_query(F.data.startswith("lvl:"))
async def cb_level(call: CallbackQuery):
    level = call.data.split(":")[1]
    if level not in LEVELS:
        await call.answer("Daraja topilmadi", show_alert=True)
        return
    STATE[call.from_user.id] = {"level": level, "score": 0}
    await call.message.edit_text(question_text(level, 0), reply_markup=question_kb(level, 0))
    await call.answer()


@dp.callback_query(F.data.startswith("ans:"))
async def cb_answer(call: CallbackQuery):
    _, level, qi_s, oi_s = call.data.split(":")
    qi, oi = int(qi_s), int(oi_s)
    st = STATE.get(call.from_user.id)
    if not st or st["level"] != level or st.get("answered") == qi:
        await call.answer("Bu savol allaqachon javoblangan.", show_alert=False)
        return

    questions = LEVELS[level]["questions"]
    q = questions[qi]
    st["answered"] = qi
    correct = oi == q["a"]
    if correct:
        st["score"] += 1
        await call.answer("✅ Toʻgʻri!")
    else:
        await call.answer(f"❌ Notoʻgʻri. Javob: {q['o'][q['a']]}", show_alert=True)

    nxt = qi + 1
    if nxt < len(questions):
        await call.message.edit_text(question_text(level, nxt), reply_markup=question_kb(level, nxt))
        return

    score, total = st["score"], len(questions)
    STATE.pop(call.from_user.id, None)
    if score == total:
        comment = "Ajoyib! Hammasi toʻgʻri 🎉"
    elif score >= total * 0.6:
        comment = "Yaxshi natija! Yana mashq qiling 👍"
    else:
        comment = "Hechqisi yoʻq, qayta urinib koʻring 💪"
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🔁 Qayta yechish", callback_data=f"lvl:{level}")],
        [InlineKeyboardButton(text="📝 Boshqa daraja", callback_data="menu:tests")],
        [InlineKeyboardButton(text="🏠 Menyu", callback_data="menu:main")],
    ])
    await call.message.edit_text(
        f"{LEVELS[level]['title']}\n\nNatija: <b>{score}/{total}</b>\n{comment}",
        reply_markup=kb,
        parse_mode="HTML",
    )


@dp.message(F.text & ~F.text.startswith("/"))
async def lookup(message: Message):
    results = search_words(message.text)
    if not results:
        await message.answer(
            "Bu soʻz lugʻatda topilmadi 😔\nBoshqa soʻz yozib koʻring yoki /menu ni bosing."
        )
        return
    await message.answer(
        "\n\n".join(format_word(w) for w in results[:5]), parse_mode="HTML"
    )


async def main():
    bot = Bot(TOKEN)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
