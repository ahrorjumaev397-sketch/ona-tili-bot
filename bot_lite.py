"""Ona tili boti — hech qanday qo'shimcha kutubxonasiz (faqat Python)."""
import html
import json
import os
import random
import sys
import time
import urllib.error
import urllib.request

from data import LEVELS, WORDS

TOKEN = os.getenv("BOT_TOKEN", "").strip()
if ":" not in TOKEN:
    sys.exit("BOT_TOKEN noto'g'ri yoki yo'q. U shunday ko'rinadi: 123456789:AAH...\n"
             "Yozing: export BOT_TOKEN=\"butun_token\"")

URL = f"https://api.telegram.org/bot{TOKEN}/"
STATE = {}  # {user_id: {"level":..., "score":..., "answered":...}}


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
        # masalan "message is not modified" — jiddiy emas
        print("API xato:", method, e.code, e.read().decode("utf-8", "ignore")[:200])
    except Exception as e:
        print("Tarmoq xatosi:", e)
    return None


def kb(rows):
    return {"inline_keyboard": [[{"text": t, "callback_data": d} for t, d in row] for row in rows]}


def norm(text):
    for ch in ("ʻ", "ʼ", "’", "‘", "`", "'"):
        text = text.replace(ch, "'")
    return text.lower().strip()


def main_menu():
    return kb([[("📝 Testlar", "menu:tests")], [("📖 Lug'at", "menu:dict")]])


def levels_menu():
    rows = [[(v["title"], f"lvl:{k}")] for k, v in LEVELS.items()]
    rows.append([("⬅️ Orqaga", "menu:main")])
    return kb(rows)


def question_kb(level, qi):
    q = LEVELS[level]["questions"][qi]
    return kb([[(opt, f"ans:{level}:{qi}:{oi}")] for oi, opt in enumerate(q["o"])])


def question_text(level, qi):
    total = len(LEVELS[level]["questions"])
    q = LEVELS[level]["questions"][qi]
    return f"{LEVELS[level]['title']}\n\nSavol {qi + 1}/{total}\n\n{q['q']}"


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


def send(chat_id, text, markup=None, parse_mode=None):
    p = {"chat_id": chat_id, "text": text}
    if markup:
        p["reply_markup"] = markup
    if parse_mode:
        p["parse_mode"] = parse_mode
    safe_api("sendMessage", **p)


def edit(cb, text, markup=None, parse_mode=None):
    m = cb["message"]
    p = {"chat_id": m["chat"]["id"], "message_id": m["message_id"], "text": text}
    if markup:
        p["reply_markup"] = markup
    if parse_mode:
        p["parse_mode"] = parse_mode
    safe_api("editMessageText", **p)


def answer(cb, text=None, alert=False):
    p = {"callback_query_id": cb["id"]}
    if text:
        p["text"] = text
        p["show_alert"] = alert
    safe_api("answerCallbackQuery", **p)


def handle_message(msg):
    chat_id = msg["chat"]["id"]
    text = (msg.get("text") or "").strip()
    if not text:
        return
    if text.startswith("/start"):
        send(chat_id,
             "Assalomu alaykum! 👋\n\n"
             "Men ona tilini 0 dan oʻrganishda yordam beraman:\n"
             "📝 daraja-daraja testlar\n"
             "📖 lugʻat — soʻz yozing, maʼnosini topaman\n\n"
             "Nimadan boshlaymiz?", main_menu())
    elif text.startswith("/menu"):
        send(chat_id, "Asosiy menyu:", main_menu())
    elif text.startswith("/"):
        send(chat_id, "Bunday buyruq yoʻq. /menu ni bosing.")
    else:
        results = search_words(text)
        if not results:
            send(chat_id, "Bu soʻz lugʻatda topilmadi 😔\nBoshqa soʻz yozing yoki /menu ni bosing.")
        else:
            send(chat_id, "\n\n".join(format_word(w) for w in results[:5]), parse_mode="HTML")


def handle_callback(cb):
    data = cb.get("data", "")
    uid = cb["from"]["id"]

    if data == "menu:main":
        edit(cb, "Asosiy menyu:", main_menu())
        answer(cb)
    elif data == "menu:tests":
        edit(cb, "Darajani tanlang:", levels_menu())
        answer(cb)
    elif data == "menu:dict":
        edit(cb, "📖 Lugʻat\n\nQidirish uchun soʻzni yozib yuboring (masalan: <b>ona</b>).",
             kb([[("🎲 Tasodifiy soʻz", "dict:random")], [("⬅️ Orqaga", "menu:main")]]), "HTML")
        answer(cb)
    elif data == "dict:random":
        edit(cb, format_word(random.choice(WORDS)),
             kb([[("🎲 Yana", "dict:random")], [("⬅️ Orqaga", "menu:dict")]]), "HTML")
        answer(cb)
    elif data.startswith("lvl:"):
        level = data.split(":")[1]
        if level not in LEVELS:
            answer(cb, "Daraja topilmadi", True)
            return
        STATE[uid] = {"level": level, "score": 0}
        edit(cb, question_text(level, 0), question_kb(level, 0))
        answer(cb)
    elif data.startswith("ans:"):
        _, level, qi_s, oi_s = data.split(":")
        qi, oi = int(qi_s), int(oi_s)
        st = STATE.get(uid)
        if not st or st["level"] != level or st.get("answered") == qi:
            answer(cb, "Bu savol allaqachon javoblangan.")
            return
        questions = LEVELS[level]["questions"]
        q = questions[qi]
        st["answered"] = qi
        if oi == q["a"]:
            st["score"] += 1
            answer(cb, "✅ Toʻgʻri!")
        else:
            answer(cb, f"❌ Notoʻgʻri. Javob: {q['o'][q['a']]}", True)
        nxt = qi + 1
        if nxt < len(questions):
            edit(cb, question_text(level, nxt), question_kb(level, nxt))
            return
        score, total = st["score"], len(questions)
        STATE.pop(uid, None)
        if score == total:
            comment = "Ajoyib! Hammasi toʻgʻri 🎉"
        elif score >= total * 0.6:
            comment = "Yaxshi natija! Yana mashq qiling 👍"
        else:
            comment = "Hechqisi yoʻq, qayta urinib koʻring 💪"
        edit(cb, f"{LEVELS[level]['title']}\n\nNatija: <b>{score}/{total}</b>\n{comment}",
             kb([[("🔁 Qayta yechish", f"lvl:{level}")],
                 [("📝 Boshqa daraja", "menu:tests")],
                 [("🏠 Menyu", "menu:main")]]), "HTML")
    else:
        answer(cb)


def handle(update):
    if "message" in update:
        handle_message(update["message"])
    elif "callback_query" in update:
        handle_callback(update["callback_query"])


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
            params = {"timeout": 30}
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
