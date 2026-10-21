"""Ona tili boti — pastki tugmalar (reply keyboard) + Telegram quiz. Qo'shimcha kutubxona kerak emas."""
import html
import json
import os
import random
import sys
import time
import urllib.error
import urllib.request

from data import WORDS
from testlar import LEVELS

QUIZ_SIZE = 10  # har urinishda nechta savol

TOKEN = os.getenv("BOT_TOKEN", "").strip()
if ":" not in TOKEN:
    sys.exit("BOT_TOKEN noto'g'ri yoki yo'q. U shunday ko'rinadi: 123456789:AAH...\n"
             "Yozing: export BOT_TOKEN=\"butun_token\"")

URL = f"https://api.telegram.org/bot{TOKEN}/"
STATE = {}  # {user_id: {"level","qs","i","score","chat_id","poll_id"}}
LAST = {}   # {user_id: oxirgi yechilgan daraja}

# Tugma matnlari
B_TESTS = "📝 Testlar"
B_DICT = "📖 Lug'at"
B_ABOUT = "ℹ️ Bot haqida"
B_MENU = "🏠 Menyu"
B_BACK = "⬅️ Orqaga"
B_RANDOM = "🎲 Tasodifiy so'z"
B_STOP = "⛔ Testni to'xtatish"
B_AGAIN = "🔁 Qayta yechish"
B_OTHER = "📝 Boshqa daraja"

TITLE2KEY = {v["title"]: k for k, v in LEVELS.items()}


# ------------------------------------------------------------------ Telegram
def api(method, **params):
    req = urllib.request.Request(
        URL + method,
        data=json.dumps(params).encode("utf-8"),
        headers={"Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.loads(r.read().decode("utf-8"))


def safe_api(method, **params):
    try:
        return api(method, **params)
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", "ignore")
        if "not modified" not in body:
            print("API xato:", method, e.code, body[:200])
    except Exception as e:
        print("Tarmoq xatosi:", e)
    return None


def send(chat_id, text, markup=None, parse_mode=None):
    p = {"chat_id": chat_id, "text": text}
    if markup:
        p["reply_markup"] = markup
    if parse_mode:
        p["parse_mode"] = parse_mode
    return safe_api("sendMessage", **p)


# ------------------------------------------------------------------ Tugmalar
def rk(rows):
    """Pastki (reply) klaviatura."""
    return {
        "keyboard": [[{"text": t} for t in row] for row in rows],
        "resize_keyboard": True,
        "is_persistent": True,
    }


def main_kb():
    return rk([[B_TESTS, B_DICT], [B_ABOUT]])


def levels_kb():
    rows = [[v["title"]] for v in LEVELS.values()]
    rows.append([B_BACK])
    return rk(rows)


def dict_kb():
    return rk([[B_RANDOM], [B_BACK]])


def quiz_kb():
    return rk([[B_STOP]])


def result_kb():
    return rk([[B_AGAIN, B_OTHER], [B_MENU]])


def levels_text():
    lines = ["Darajani tanlang:\n"]
    for v in LEVELS.values():
        lines.append(f"{v['title']}\n— {v['desc']}\n")
    return "\n".join(lines)


def norm(text):
    for ch in ("ʻ", "ʼ", "’", "‘", "`", "'"):
        text = text.replace(ch, "'")
    return text.lower().strip()


def fresh(q):
    """Savolning variantlarini yana aralashtiradi."""
    right = q["o"][q["a"]]
    opts = q["o"][:]
    random.shuffle(opts)
    return {"q": q["q"], "o": opts, "a": opts.index(right)}


# ------------------------------------------------------------------ Lug'at
def format_word(w):
    word, pos, meaning, example = (html.escape(x) for x in w)
    return (f"📖 <b>{word}</b> ({pos})\n\n"
            f"<b>Maʼnosi:</b> {meaning}\n"
            f"<b>Misol:</b> <i>{example}</i>")


def search_words(query):
    q = norm(query)
    if not q:
        return []
    exact = [w for w in WORDS if norm(w[0]) == q]
    if exact:
        return exact
    starts = [w for w in WORDS if norm(w[0]).startswith(q)]
    if starts:
        return starts
    return [w for w in WORDS if q in norm(w[0])]


# ------------------------------------------------------------------ Quiz
def start_quiz(uid, chat_id, level):
    pool = LEVELS[level]["questions"]
    qs = [fresh(q) for q in random.sample(pool, min(QUIZ_SIZE, len(pool)))]
    STATE[uid] = {"level": level, "qs": qs, "i": 0, "score": 0,
                  "chat_id": chat_id, "poll_id": None}
    LAST[uid] = level
    send(chat_id, f"{LEVELS[level]['title']}\n\n{len(qs)} ta savol. Javobni bosing — "
                  "toʻgʻri javob darhol koʻrinadi. Omad! 🍀", quiz_kb())
    send_next(uid)


def send_next(uid):
    st = STATE.get(uid)
    if not st:
        return
    qs, i = st["qs"], st["i"]
    if i >= len(qs):
        finish(uid)
        return
    q = qs[i]
    right = q["o"][q["a"]]
    res = safe_api(
        "sendPoll",
        chat_id=st["chat_id"],
        question=f"{i + 1}/{len(qs)}. {q['q']}"[:300],
        options=[o[:100] for o in q["o"]],
        type="quiz",
        correct_option_id=q["a"],
        is_anonymous=False,
        explanation=("Toʻgʻri javob: " + right)[:200],
    )
    if not res or not res.get("ok"):
        send(st["chat_id"], "Savolni yuborib boʻlmadi 😔", main_kb())
        STATE.pop(uid, None)
        return
    st["poll_id"] = res["result"]["poll"]["id"]


def finish(uid):
    st = STATE.pop(uid, None)
    if not st:
        return
    score, total, level = st["score"], len(st["qs"]), st["level"]
    if score == total:
        comment = "Ajoyib! Hammasi toʻgʻri 🎉"
    elif score >= total * 0.8:
        comment = "Juda yaxshi! Keyingi darajaga oʻtishingiz mumkin 🚀"
    elif score >= total * 0.6:
        comment = "Yaxshi natija! Yana mashq qiling 👍"
    else:
        comment = "Hechqisi yoʻq, qayta urinib koʻring 💪"
    send(st["chat_id"],
         f"{LEVELS[level]['title']}\n\nNatija: <b>{score}/{total}</b>\n{comment}",
         result_kb(), "HTML")


def handle_poll_answer(pa):
    uid = pa["user"]["id"]
    st = STATE.get(uid)
    if not st or st.get("poll_id") != pa["poll_id"]:
        return
    q = st["qs"][st["i"]]
    if pa.get("option_ids") and pa["option_ids"][0] == q["a"]:
        st["score"] += 1
    st["i"] += 1
    st["poll_id"] = None
    time.sleep(1.2)  # to'g'ri javobni ko'rishga ulgursin
    send_next(uid)


# ------------------------------------------------------------------ Xabarlar
def total_questions():
    return sum(len(v["questions"]) for v in LEVELS.values())


def handle_message(msg):
    chat_id = msg["chat"]["id"]
    uid = msg.get("from", {}).get("id", chat_id)
    text = (msg.get("text") or "").strip()
    if not text:
        return

    # --- Asosiy menyu
    if text.startswith("/start"):
        STATE.pop(uid, None)
        send(chat_id,
             "Assalomu alaykum! 👋\n\n"
             "Men ona tilini 0 dan oʻrganishda yordam beraman:\n"
             f"📝 4 darajali quiz-testlar ({total_questions()} ta savol)\n"
             "📖 lugʻat — soʻz yozing, maʼnosini topaman\n\n"
             "Quyidagi tugmalardan birini tanlang 👇", main_kb())
    elif text.startswith("/menu") or text in (B_MENU, B_BACK):
        STATE.pop(uid, None)
        send(chat_id, "Asosiy menyu 👇", main_kb())
    elif text == B_STOP:
        STATE.pop(uid, None)
        send(chat_id, "Test toʻxtatildi.", main_kb())
    elif text in (B_TESTS, B_OTHER):
        STATE.pop(uid, None)
        send(chat_id, levels_text(), levels_kb())
    elif text in TITLE2KEY:
        STATE.pop(uid, None)
        start_quiz(uid, chat_id, TITLE2KEY[text])
    elif text == B_AGAIN:
        STATE.pop(uid, None)
        level = LAST.get(uid)
        if level in LEVELS:
            start_quiz(uid, chat_id, level)
        else:
            send(chat_id, levels_text(), levels_kb())
    elif text == B_DICT:
        STATE.pop(uid, None)
        send(chat_id, "📖 Lugʻat\n\nQidirish uchun soʻzni yozib yuboring (masalan: ona).\n"
                      "Yoki «🎲 Tasodifiy soʻz» tugmasini bosing.", dict_kb())
    elif text == B_RANDOM:
        send(chat_id, format_word(random.choice(WORDS)), dict_kb(), "HTML")
    elif text == B_ABOUT:
        send(chat_id,
             "ℹ️ Bu bot ona tilini 0 dan oʻrganishga yordam beradi.\n\n"
             f"📝 4 daraja, jami {total_questions()} ta savol\n"
             f"📖 lugʻatda {len(WORDS)} ta soʻz\n\n"
             "Boshlash uchun «📝 Testlar» ni bosing.", main_kb())
    elif text.startswith("/"):
        send(chat_id, "Bunday buyruq yoʻq. /menu ni bosing.", main_kb())
    elif uid in STATE:
        send(chat_id, "Test davom etmoqda 🙂 Savolga javob bering yoki "
                      "«⛔ Testni to'xtatish» tugmasini bosing.")
    else:
        results = search_words(text)
        if not results:
            send(chat_id, "Bu soʻz lugʻatda topilmadi 😔\nBoshqa soʻz yozing.", main_kb())
        else:
            send(chat_id, "\n\n".join(format_word(w) for w in results[:5]),
                 main_kb(), "HTML")


def handle(update):
    if "message" in update:
        handle_message(update["message"])
    elif "poll_answer" in update:
        handle_poll_answer(update["poll_answer"])


def main():
    try:
        me = api("getMe")
    except urllib.error.HTTPError as e:
        if e.code in (401, 404):
            sys.exit("Token notoʻgʻri. BotFatherdan BUTUN tokenni nusxalang.")
        raise
    print("Bot ishga tushdi: @" + me["result"]["username"])
    offset = None
    while True:
        try:
            params = {"timeout": 30, "allowed_updates": ["message", "poll_answer"]}
            if offset:
                params["offset"] = offset
            res = api("getUpdates", **params)
            for u in res["result"]:
                offset = u["update_id"] + 1
                try:
                    handle(u)
                except Exception as e:
                    print("Xato:", repr(e))
        except KeyboardInterrupt:
            print("To'xtatildi.")
            return
        except Exception as e:
            print("Ulanish xatosi, qayta urinaman:", e)
            time.sleep(3)


if __name__ == "__main__":
    main()
