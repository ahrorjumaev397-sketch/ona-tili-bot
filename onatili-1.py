"""Ona tili boti — BITTA FAYL: testlar + lug'at + bot. Qo'shimcha kutubxona kerak emas."""
import html
import json
import os
import random
import re
import sys
import time
import urllib.error
import urllib.request


# ================= TESTLAR =================
# Ona tili testlari: 4 ta daraja


def _q(text, right, *wrong):
    """Savol yaratadi; variantlar aralashtiriladi."""
    opts = [right, *wrong]
    random.shuffle(opts)
    return {"q": text, "o": opts, "a": opts.index(right)}


# ---------------------------------------------------------------- 1-daraja
BOSHLANGICH = [
    _q("Oʻzbek alifbosida nechta harf bor?", "29", "26", "32", "35"),
    _q("Oʻzbek tilida nechta unli harf bor?", "6", "5", "7", "8"),
    _q("Quyidagilardan qaysi biri unli harf?", "u", "k", "m", "s"),
    _q("Quyidagilardan qaysi biri undosh harf?", "b", "a", "e", "o"),
    _q("Qaysi harf oʻzbek lotin alifbosida yoʻq?", "W", "Q", "X", "J"),
    _q("Oʻzbek alifbosining birinchi harfi qaysi?", "A", "B", "D", "E"),
    _q("«Ch» harflar birikmasi nechta tovushni bildiradi?", "1", "2", "3", "4"),
    _q("«Oʻzbekiston» soʻzida nechta unli harf bor?", "4", "3", "5", "6"),
    _q("«Kitob» soʻzida nechta undosh harf bor?", "3", "2", "4", "5"),
    _q("Qaysi harf undosh?", "q", "a", "i", "u"),
    _q("Qaysi harf unli?", "e", "d", "r", "t"),
    _q("«Gʻ» harfi qaysi guruhga kiradi?", "Undosh", "Unli", "Ikkalasi ham", "Hech qaysi"),
    _q("«Olma» soʻzida nechta boʻgʻin bor?", "2", "1", "3", "4"),
    _q("«Dars» soʻzida nechta boʻgʻin bor?", "1", "2", "3", "4"),
    _q("«Qalam» soʻzida nechta boʻgʻin bor?", "2", "1", "3", "4"),
    _q("«Oʻqituvchi» soʻzida nechta boʻgʻin bor?", "4", "2", "3", "5"),
    _q("«Maktab» soʻzi qanday boʻgʻinlanadi?", "mak-tab", "ma-ktab", "m-ak-tab", "maktab"),
    _q("«Ona» soʻzi qanday boʻgʻinlanadi?", "o-na", "on-a", "ona", "o-n-a"),
    _q("Boʻgʻin soni nimaga qarab aniqlanadi?", "Unlilar soniga", "Undoshlar soniga",
       "Harflar soniga", "Soʻz uzunligiga"),
    _q("«Kitob» qaysi soʻz turkumiga kiradi?", "Ot", "Sifat", "Feʼl", "Son"),
    _q("«Chiroyli» qaysi soʻz turkumiga kiradi?", "Sifat", "Ot", "Feʼl", "Olmosh"),
    _q("«Yozmoq» qaysi soʻz turkumiga kiradi?", "Feʼl", "Ot", "Sifat", "Son"),
    _q("«Uch» qaysi soʻz turkumiga kiradi?", "Son", "Ot", "Feʼl", "Sifat"),
    _q("«Men» qaysi soʻz turkumiga kiradi?", "Olmosh", "Son", "Sifat", "Feʼl"),
    _q("Ot qanday soʻroqqa javob boʻladi?", "Kim? Nima?", "Qanday?", "Nima qildi?", "Necha?"),
    _q("Sifat qanday soʻroqqa javob boʻladi?", "Qanday?", "Kim? Nima?", "Necha?", "Nima qildi?"),
    _q("Feʼl qanday soʻroqqa javob boʻladi?", "Nima qildi?", "Qanday?", "Necha?", "Kim?"),
    _q("Son qanday soʻroqqa javob boʻladi?", "Necha?", "Qanday?", "Kim?", "Nima qildi?"),
    _q("Quyidagilardan qaysi biri ot?", "Gul", "Oʻqidi", "Qizil", "Ikki"),
    _q("Quyidagilardan qaysi biri feʼl?", "Oʻqidi", "Gul", "Qizil", "Ikki"),
    _q("Darak gap oxiriga qaysi belgi qoʻyiladi?", "Nuqta", "Soʻroq belgisi", "Undov belgisi", "Ikki nuqta"),
    _q("Soʻroq gap oxiriga qaysi belgi qoʻyiladi?", "Soʻroq belgisi", "Nuqta", "Vergul", "Tire"),
    _q("Gap qanday harf bilan boshlanadi?", "Bosh harf", "Kichik harf", "Raqam", "Tinish belgisi"),
    _q("«!» belgisi qanday ataladi?", "Undov belgisi", "Soʻroq belgisi", "Ikki nuqta", "Tire"),
    _q("«,» belgisi qanday ataladi?", "Vergul", "Nuqta", "Ikki nuqta", "Tire"),
]

# ---------------------------------------------------------------- 2-daraja
OZROQ = [
    _q("Maʼnosi bir-biriga yaqin soʻzlar nima deyiladi?", "Sinonim", "Antonim", "Omonim", "Paronim"),
    _q("Maʼnosi qarama-qarshi soʻzlar nima deyiladi?", "Antonim", "Sinonim", "Omonim", "Paronim"),
    _q("«Katta» soʻzining antonimi qaysi?", "Kichik", "Baland", "Yirik", "Ulkan"),
    _q("«Yaxshi» soʻzining antonimi qaysi?", "Yomon", "Chiroyli", "Zoʻr", "Aʼlo"),
    _q("«Issiq» soʻzining antonimi qaysi?", "Sovuq", "Qaynoq", "Iliq", "Dim"),
    _q("«Kun» soʻzining antonimi qaysi?", "Tun", "Tong", "Kech", "Oqshom"),
    _q("«Baland» soʻzining antonimi qaysi?", "Past", "Uzun", "Keng", "Katta"),
    _q("«Ochiq» soʻzining antonimi qaysi?", "Yopiq", "Keng", "Yorugʻ", "Aniq"),
    _q("«Yangi» soʻzining antonimi qaysi?", "Eski", "Toza", "Zamonaviy", "Yosh"),
    _q("«Sekin» soʻzining antonimi qaysi?", "Tez", "Past", "Yengil", "Kuchli"),
    _q("«Goʻzal» soʻzining sinonimi qaysi?", "Chiroyli", "Xunuk", "Katta", "Qimmat"),
    _q("«Oʻqituvchi» soʻzining sinonimi qaysi?", "Muallim", "Oʻquvchi", "Talaba", "Shogird"),
    _q("«Quvonch» soʻzining sinonimi qaysi?", "Shodlik", "Gʻam", "Qoʻrquv", "Xafalik"),
    _q("«Ali kitob oʻqidi.» gapida ega qaysi?", "Ali", "kitob", "oʻqidi", "Gapda ega yoʻq"),
    _q("«Ali kitob oʻqidi.» gapida kesim qaysi?", "oʻqidi", "Ali", "kitob", "Gapda kesim yoʻq"),
    _q("«Bahor keldi.» gapida ega qaysi?", "Bahor", "keldi", "Ikkalasi ham", "Hech qaysi"),
    _q("«Quyosh chiqdi.» gapida kesim qaysi?", "chiqdi", "Quyosh", "Ikkalasi ham", "Hech qaysi"),
    _q("Gapning eng muhim ikki boʻlagi qaysilar?", "Ega va kesim", "Aniqlovchi va hol",
       "Toʻldiruvchi va hol", "Ega va aniqlovchi"),
    _q("«Bolalar maktabga bordi.» gapida nechta soʻz bor?", "3", "2", "4", "5"),
    _q("Oʻzbek tilida nechta kelishik bor?", "6", "4", "5", "7"),
    _q("«Kitobni» soʻzi qaysi kelishikda?", "Tushum", "Bosh", "Qaratqich", "Chiqish"),
    _q("«Maktabga» soʻzi qaysi kelishikda?", "Joʻnalish", "Oʻrin-payt", "Tushum", "Bosh"),
    _q("«Uyda» soʻzi qaysi kelishikda?", "Oʻrin-payt", "Joʻnalish", "Chiqish", "Qaratqich"),
    _q("«Shahardan» soʻzi qaysi kelishikda?", "Chiqish", "Oʻrin-payt", "Tushum", "Bosh"),
    _q("«Onamning» soʻzi qaysi kelishikda?", "Qaratqich", "Tushum", "Joʻnalish", "Bosh"),
    _q("Bosh kelishik qaysi soʻroqlarga javob beradi?", "Kim? Nima?", "Kimni? Nimani?",
       "Kimga? Nimaga?", "Kimning? Nimaning?"),
    _q("Qaysi soʻz toʻgʻri yozilgan?", "Moʻjiza", "Mojiza", "Mojzia", "Moʻziza"),
    _q("Qaysi soʻz toʻgʻri yozilgan?", "Toʻgʻri", "Togri", "Toʻgri", "Tugʻri"),
    _q("Qaysi soʻz toʻgʻri yozilgan?", "Gʻalaba", "Galaba", "Ghalaba", "Gʻalabba"),
    _q("Qaysi soʻz toʻgʻri yozilgan?", "Shahar", "Shaxar", "Shehar", "Shahhar"),
    _q("Qaysi soʻz toʻgʻri yozilgan?", "Hayot", "Xayot", "Hayyot", "Hayoot"),
    _q("Qaysi soʻz toʻgʻri yozilgan?", "Eʼlon", "Elon", "Eelon", "Eʼlonn"),
    _q("«Bola» soʻzining koʻplik shakli qaysi?", "Bolalar", "Bolalarlar", "Bolatar", "Bolaler"),
    _q("«Daftar» soʻzining koʻplik shakli qaysi?", "Daftarlar", "Daftarlarlar", "Daftarler", "Daftartar"),
    _q("Bir xil boʻlaklar (sanash) orasiga qaysi belgi qoʻyiladi?", "Vergul", "Nuqta", "Tire", "Undov belgisi"),
    _q("«:» belgisi qanday ataladi?", "Ikki nuqta", "Nuqta", "Vergul", "Undov belgisi"),
]

# ---------------------------------------------------------------- 3-daraja
ORTACHA = [
    _q("Joʻnalish kelishigining qoʻshimchasi qaysi?", "-ga", "-ni", "-da", "-dan"),
    _q("Chiqish kelishigining qoʻshimchasi qaysi?", "-dan", "-ga", "-ni", "-ning"),
    _q("Oʻrin-payt kelishigining qoʻshimchasi qaysi?", "-da", "-dan", "-ga", "-ning"),
    _q("Tushum kelishigining qoʻshimchasi qaysi?", "-ni", "-ning", "-da", "-ga"),
    _q("Qaratqich kelishigining qoʻshimchasi qaysi?", "-ning", "-ni", "-dan", "-ga"),
    _q("«Kitobim» soʻzidagi -im qoʻshimchasi kimga qarashlilikni bildiradi?",
       "Menga (I shaxs)", "Senga (II shaxs)", "Unga (III shaxs)", "Bizga (I shaxs koʻplik)"),
    _q("«Kitobing» soʻzidagi -ing qoʻshimchasi kimga qarashlilikni bildiradi?",
       "Senga (II shaxs)", "Menga (I shaxs)", "Unga (III shaxs)", "Bizga (I shaxs koʻplik)"),
    _q("«Kitobi» soʻzidagi -i qoʻshimchasi kimga qarashlilikni bildiradi?",
       "Unga (III shaxs)", "Menga (I shaxs)", "Senga (II shaxs)", "Bizga (I shaxs koʻplik)"),
    _q("«Kelyapti» feʼli qaysi zamonda?", "Hozirgi zamon", "Oʻtgan zamon", "Hozirgi-kelasi zamon", "Buyruq shakli"),
    _q("«Keldi» feʼli qaysi zamonda?", "Oʻtgan zamon", "Hozirgi zamon", "Hozirgi-kelasi zamon", "Buyruq shakli"),
    _q("«Keladi» feʼli qaysi zamonda?", "Hozirgi-kelasi zamon", "Oʻtgan zamon", "Hozirgi zamon (-yap-)", "Buyruq shakli"),
    _q("-chi qoʻshimchasi (ishchi, oʻqituvchi) qaysi turkumdagi soʻz yasaydi?", "Ot", "Sifat", "Feʼl", "Son"),
    _q("«Aqlli» soʻzi qaysi soʻz turkumiga kiradi?", "Sifat", "Ot", "Feʼl", "Son"),
    _q("«Suvsiz» soʻzidagi -siz qoʻshimchasi qanday maʼno bildiradi?",
       "Yoʻqlik", "Koʻplik", "Qarashlilik", "Harakat"),
    _q("«Doʻstlik» soʻzi qaysi soʻz turkumiga kiradi?", "Ot", "Sifat", "Feʼl", "Ravish"),
    _q("«Maktabga» soʻzining oʻzagi qaysi?", "maktab", "maktabg", "mak", "ga"),
    _q("«Kitoblarim» soʻzining oʻzagi qaysi?", "kitob", "kitobl", "kit", "lar"),
    _q("Oʻzak nima?", "Soʻzning qoʻshimchasiz, asosiy maʼnoli qismi", "Soʻzning oxirgi qismi",
       "Soʻzning birinchi harfi", "Gapning bosh boʻlagi"),
    _q("«Bolalar» soʻzida nechta qoʻshimcha bor?", "1", "0", "2", "3"),
    _q("Qaysi soʻz toʻgʻri yozilgan?", "Aʼlo", "Alʼo", "Aalo", "Aloʼ"),
    _q("Shakli bir xil, lekin maʼnosi har xil soʻzlar nima deyiladi?", "Omonim", "Sinonim", "Antonim", "Frazeologizm"),
    _q("«Ot» (hayvon) va «ot» (ism) soʻzlari qanday soʻzlar?", "Omonim", "Sinonim", "Antonim", "Paronim"),
    _q("«Ali kitobni oʻqidi.» gapida toʻldiruvchi qaysi?", "kitobni", "Ali", "oʻqidi", "Hech qaysi"),
    _q("«Chiroyli gul ochildi.» gapida aniqlovchi qaysi?", "chiroyli", "gul", "ochildi", "Hammasi"),
    _q("«Ali tez yugurdi.» gapida hol qaysi?", "tez", "Ali", "yugurdi", "Hammasi"),
    _q("Kimni? Nimani? soʻroqlariga javob boʻlgan gap boʻlagi qaysi?", "Toʻldiruvchi", "Ega", "Kesim", "Hol"),
    _q("Qachon? Qayerda? soʻroqlariga javob boʻlgan gap boʻlagi qaysi?", "Hol", "Ega", "Kesim", "Toʻldiruvchi"),
    _q("«Quyosh chiqdi.» qanday gap?", "Sodda gap", "Qoʻshma gap", "Soʻz birikmasi", "Hech qaysi"),
    _q("«Men kitob oʻqiyman, u esa rasm chizadi.» qanday gap?", "Qoʻshma gap", "Sodda gap", "Soʻz birikmasi", "Undalma"),
    _q("Toʻgʻridan-toʻgʻri nutq qaysi belgilar ichida yoziladi?", "Qoʻshtirnoq", "Qavs", "Tire", "Vergul"),
]

# ---------------------------------------------------------------- 4-daraja
YUQORI = [
    _q("«Lekin» soʻzi qaysi soʻz turkumiga kiradi?", "Bogʻlovchi", "Yuklama", "Koʻmakchi", "Undov"),
    _q("«Hamda» soʻzi qaysi soʻz turkumiga kiradi?", "Bogʻlovchi", "Yuklama", "Koʻmakchi", "Ravish"),
    _q("«Uchun» soʻzi qaysi soʻz turkumiga kiradi?", "Koʻmakchi", "Bogʻlovchi", "Yuklama", "Olmosh"),
    _q("«Faqat» soʻzi qaysi soʻz turkumiga kiradi?", "Yuklama", "Bogʻlovchi", "Koʻmakchi", "Sifat"),
    _q("«Oh!» soʻzi qaysi soʻz turkumiga kiradi?", "Undov soʻz", "Yuklama", "Bogʻlovchi", "Ravish"),
    _q("«Ertaga» soʻzi qaysi soʻz turkumiga kiradi?", "Ravish", "Ot", "Sifat", "Olmosh"),
    _q("Harakatning belgisini bildiruvchi soʻz turkumi qaysi?", "Ravish", "Sifat", "Son", "Olmosh"),
    _q("«Balandroq» soʻzi sifatning qaysi darajasida?", "Qiyosiy daraja", "Oddiy daraja", "Orttirma daraja", "Hech qaysi"),
    _q("«Eng yaxshi» birikmasi sifatning qaysi darajasida?", "Orttirma daraja", "Oddiy daraja", "Qiyosiy daraja", "Hech qaysi"),
    _q("«Katta» soʻzi sifatning qaysi darajasida?", "Oddiy daraja", "Qiyosiy daraja", "Orttirma daraja", "Hech qaysi"),
    _q("«Boraman» soʻzidagi -man qaysi shaxs-sonni bildiradi?",
       "I shaxs birlik", "II shaxs birlik", "III shaxs birlik", "I shaxs koʻplik"),
    _q("«Yozasan» soʻzidagi -san qaysi shaxs-sonni bildiradi?",
       "II shaxs birlik", "I shaxs birlik", "III shaxs birlik", "II shaxs koʻplik"),
    _q("«Kitobimiz» soʻzidagi -imiz qaysi shaxs-sonni bildiradi?",
       "I shaxs koʻplik", "I shaxs birlik", "II shaxs koʻplik", "III shaxs birlik"),
    _q("«Yozmoq» feʼlning qaysi shakli?", "Harakat nomi", "Oʻtgan zamon shakli", "Buyruq shakli", "Hozirgi zamon shakli"),
    _q("Maʼnosi koʻchma, bir butun holda ishlatiladigan turgʻun birikmalar nima deyiladi?",
       "Frazeologizm", "Omonim", "Sinonim", "Paronim"),
    _q("«Qoʻli gul» iborasining maʼnosi qaysi?", "Mohir, usta", "Qoʻli yaralangan", "Gul sotuvchi", "Qoʻli kasal"),
    _q("Aytilishi oʻxshash, lekin maʼnosi har xil soʻzlar nima deyiladi?", "Paronim", "Omonim", "Sinonim", "Antonim"),
    _q("Bitta soʻzning bir necha maʼnoga ega boʻlishi nima deyiladi?",
       "Koʻp maʼnolilik", "Omonimiya", "Sinonimiya", "Antonimiya"),
    _q("«Katta uy» nima?", "Soʻz birikmasi", "Gap", "Yagona soʻz", "Undalma"),
    _q("«Katta uy qurildi.» nima?", "Gap", "Soʻz birikmasi", "Yagona soʻz", "Hech qaysi"),
    _q("«Kitobni oʻqing!» qanday gap?", "Buyruq gap", "Darak gap", "Soʻroq gap", "Qoʻshma gap"),
    _q("«Ertaga maktabga borasanmi?» qanday gap?", "Soʻroq gap", "Darak gap", "Buyruq gap", "Qoʻshma gap"),
    _q("«Biz ertaga sayohatga boramiz.» qanday gap?", "Darak gap", "Soʻroq gap", "Buyruq gap", "Qoʻshma gap"),
    _q("«Ali kecha keldi.» gapida «kecha» qaysi hol?", "Payt holi", "Oʻrin holi", "Tarz holi", "Sabab holi"),
    _q("«Ali maktabda oʻqiydi.» gapida «maktabda» qaysi hol?", "Oʻrin holi", "Payt holi", "Tarz holi", "Sabab holi"),
    _q("Bir xil soʻroqqa javob boʻlib, oʻzaro teng bogʻlangan gap boʻlaklari nima deyiladi?",
       "Uyushiq boʻlaklar", "Undalma", "Kirish soʻz", "Ajratilgan boʻlak"),
    _q("«Ali, bu yoqqa kel!» gapida «Ali» qanday vazifada?", "Undalma", "Ega", "Toʻldiruvchi", "Hol"),
    _q("«Ali, bu yoqqa kel!» gapida vergul nima uchun qoʻyilgan?",
       "Undalmani ajratish uchun", "Gapni tugatish uchun", "Savol bildirish uchun", "Hayajon bildirish uchun"),
    _q("«Albatta, men sizga yordam beraman.» gapida «albatta» qanday vazifada?",
       "Kirish soʻz", "Ega", "Kesim", "Toʻldiruvchi"),
    _q("Ariza, buyruq, eʼlon qaysi nutq uslubiga xos?", "Rasmiy uslub", "Badiiy uslub", "Ilmiy uslub", "Soʻzlashuv uslubi"),
    _q("«Tong» soʻzida nechta tovush bor?", "3", "2", "4", "5"),
    _q("Qaysi biri shakl yasovchi qoʻshimcha?", "-lar", "-chi", "-lik", "-li"),
    _q("Qaysi biri soʻz yasovchi qoʻshimcha?", "-chi", "-lar", "-ni", "-ning"),
    _q("Ikki yoki undan ortiq sodda gapning birikuvidan hosil boʻlgan gap nima deyiladi?",
       "Qoʻshma gap", "Sodda gap", "Soʻz birikmasi", "Undalma"),
    _q("Maqol nima?", "Xalq donoligini ifodalovchi ixcham, ibratli gap",
       "Uzun hikoya", "Ilmiy atama", "Rasmiy hujjat"),
]

LEVELS = {
    "d1": {
        "title": "🌱 1-daraja: Boshlangʻich",
        "desc": "Alifbo, unli va undosh, boʻgʻin, soʻz turkumlari, tinish belgilari",
        "questions": BOSHLANGICH,
    },
    "d2": {
        "title": "🌿 2-daraja: Ozroq biladiganlar",
        "desc": "Sinonim-antonim, ega-kesim, kelishiklar, imlo, koʻplik",
        "questions": OZROQ,
    },
    "d3": {
        "title": "🌳 3-daraja: Oʻrtacha",
        "desc": "Qoʻshimchalar, zamonlar, soʻz yasalishi, gap boʻlaklari",
        "questions": ORTACHA,
    },
    "d4": {
        "title": "🏆 4-daraja: Yuqori",
        "desc": "Soʻz turkumlari, gap turlari, hol, uslub, frazeologiya",
        "questions": YUQORI,
    },
}


# ================= LUGʻAT =================
# Ona tili lugʻati: boʻlimlar boʻyicha (soʻz, izoh, misol)
# Yangi soʻz qoʻshish uchun tegishli roʻyxatga bitta qator qoʻshing.

ATAMALAR = [
    ("harf", "Yozuvda tovushni ifodalovchi belgi.", "A — alifboning birinchi harfi."),
    ("alifbo", "Tilning yozuvdagi harflar tizimi.", "Oʻzbek alifbosi 29 harfdan iborat."),
    ("unli", "Havo toʻsiqsiz chiqib aytiladigan tovush.", "A, e, i, o, u, oʻ — unlilar."),
    ("undosh", "Havo toʻsiqqa uchrab aytiladigan tovush.", "B, d, k, m — undoshlar."),
    ("boʻgʻin", "Soʻzning bir ovoz bilan aytiladigan boʻlagi.", "Ona soʻzi ikki boʻgʻinli: o-na."),
    ("urgʻu", "Soʻzdagi boʻgʻinlardan birining kuchliroq aytilishi.", "«Kitob» soʻzida urgʻu oxirgi boʻgʻinga tushadi."),
    ("soʻz", "Biror narsa yoki tushunchani bildiruvchi til birligi.", "«Daraxt» — bir soʻz."),
    ("gap", "Tugal fikr bildiruvchi soʻz yoki soʻzlar birikmasi.", "Bahor keldi."),
    ("soʻz birikmasi", "Ikki yoki undan ortiq mustaqil soʻzning maʼno va grammatik jihatdan bogʻlanishi.", "Katta uy."),
    ("ega", "Gapda harakat egasini bildirib, kim? nima? soʻrogʻiga javob beruvchi boʻlak.", "Ali keldi. (ega — Ali)"),
    ("kesim", "Ega haqida xabar beruvchi, ish-harakat yoki holatni bildiruvchi boʻlak.", "Ali keldi. (kesim — keldi)"),
    ("toʻldiruvchi", "Kimni? nimani? kimga? kimdan? kabi soʻroqlarga javob boʻluvchi gap boʻlagi.", "Men kitobni oʻqidim."),
    ("aniqlovchi", "Otning belgisi yoki qarashliligini bildiruvchi gap boʻlagi (qanday? qaysi? kimning?).", "Chiroyli gul ochildi."),
    ("hol", "Harakatning payt, oʻrin, tarz, sabab kabi belgisini bildiruvchi gap boʻlagi.", "U ertalab keldi."),
    ("undalma", "Gapda kimgadir yoki nimagadir murojaatni bildiruvchi soʻz.", "Ali, bu yoqqa kel!"),
    ("kirish soʻz", "Gapdagi fikrga munosabat bildiruvchi, gap boʻlagi boʻlmagan soʻz.", "Albatta, men boraman."),
    ("uyushiq boʻlaklar", "Bir xil soʻroqqa javob boʻlib, oʻzaro teng bogʻlangan gap boʻlaklari.", "Bogʻda olma, nok, uzum bor."),
    ("sodda gap", "Bitta mazmun markaziga ega boʻlgan gap.", "Quyosh chiqdi."),
    ("qoʻshma gap", "Ikki yoki undan ortiq sodda gapdan tuzilgan gap.", "Yomgʻir yogʻdi, lekin biz yoʻlga chiqdik."),
    ("oʻzak", "Soʻzning qoʻshimchasiz, asosiy maʼnoli qismi.", "«Kitoblar» soʻzining oʻzagi — kitob."),
    ("qoʻshimcha", "Soʻzga qoʻshilib, maʼno yoki shakl hosil qiluvchi qism.", "«Maktabga» — -ga qoʻshimchasi."),
    ("soʻz yasovchi qoʻshimcha", "Yangi soʻz hosil qiluvchi qoʻshimcha.", "-chi: ish + chi = ishchi."),
    ("shakl yasovchi qoʻshimcha", "Soʻzning shaklini oʻzgartiradi, yangi soʻz yasamaydi.", "-lar: kitob + lar = kitoblar."),
    ("qoʻshma soʻz", "Ikki soʻzning qoʻshilishidan hosil boʻlgan, bitta maʼno bildiruvchi soʻz.", "Gulkaram — gul va karam soʻzlaridan."),
    ("juft soʻz", "Ikki soʻzning juft holda ishlatilishidan hosil boʻlgan soʻz.", "Ota-ona, katta-kichik."),
    ("takroriy soʻz", "Soʻzning takrorlanishidan hosil boʻlgan soʻz.", "Uy-uyga tarqaldilar."),
    ("sinonim", "Maʼnosi bir-biriga yaqin soʻzlar.", "Chiroyli va goʻzal — sinonimlar."),
    ("antonim", "Maʼnosi qarama-qarshi soʻzlar.", "Katta va kichik — antonimlar."),
    ("omonim", "Shakli bir xil, lekin maʼnosi har xil soʻzlar.", "Ot (hayvon) va ot (ism)."),
    ("paronim", "Aytilishi oʻxshash, lekin maʼnosi har xil soʻzlar.", "Tarif va taʼrif."),
    ("frazeologizm", "Maʼnosi koʻchma, bir butun holda ishlatiladigan turgʻun birikma.", "«Qoʻli gul» — mohir, usta."),
    ("maqol", "Xalq donoligini ifodalovchi ixcham, ibratli gap.", "Ilm — hayot chirogʻi."),
    ("kelishik", "Otning gapdagi boshqa soʻzlarga munosabatini bildiruvchi shakl.", "Oʻzbek tilida 6 ta kelishik bor."),
    ("egalik qoʻshimchasi", "Narsa-buyumning kimgadir qarashliligini bildiruvchi qoʻshimcha.", "Kitobim, kitobing, kitobi."),
    ("koʻplik qoʻshimchasi", "Narsaning koʻpligini bildiruvchi -lar qoʻshimchasi.", "Bola + lar = bolalar."),
    ("zamon", "Ish-harakatning vaqtga munosabatini bildiruvchi feʼl shakli.", "Oʻtgan, hozirgi, kelasi zamon."),
    ("shaxs-son qoʻshimchasi", "Feʼlning kim tomonidan bajarilishini bildiruvchi qoʻshimcha.", "Boraman, borasan, boradi."),
    ("harakat nomi", "Feʼlning -moq bilan tugagan shakli.", "Yozmoq, oʻqimoq."),
    ("sifatdosh", "Harakat belgisini bildirib, sifat vazifasini bajaruvchi feʼl shakli.", "Oʻqigan bola."),
    ("ravishdosh", "Harakatning belgisini bildiruvchi feʼl shakli (-b, -ib, -gach).", "U kulib gapirdi."),
    ("daraja", "Sifat belgisining darajasi: oddiy, qiyosiy, orttirma.", "Baland, balandroq, eng baland."),
    ("mayl", "Feʼlning harakatga munosabatini bildiruvchi shakli.", "Buyruq mayli: oʻqi!"),
    ("soʻz turkumi", "Soʻzlarning maʼno, soʻroq va vazifasiga koʻra guruhi.", "Ot, sifat, son, olmosh, feʼl, ravish..."),
    ("mustaqil soʻz", "Mustaqil maʼnoga ega, gap boʻlagi boʻla oladigan soʻz.", "Ot, sifat, son, olmosh, feʼl, ravish."),
    ("yordamchi soʻz", "Mustaqil maʼnosiz, soʻzlar yoki gaplarni bogʻlashga xizmat qiluvchi soʻz.", "Koʻmakchi, bogʻlovchi, yuklama."),
    ("imlo", "Soʻzlarni toʻgʻri yozish qoidalari.", "Imlo qoidalarini bilish kerak."),
    ("talaffuz", "Soʻzlarni toʻgʻri aytish qoidalari.", "Toʻgʻri talaffuz — tushunarli nutq."),
    ("tutuq belgisi", "Soʻz ichida unlilarni ajratib, maxsus tovushni bildiruvchi belgi (ʼ).", "Maʼno, eʼlon, aʼlo."),
    ("tinish belgilari", "Yozuvda gap boʻlaklarini ajratib, maʼnoni aniqlashtiruvchi belgilar.", "Nuqta, vergul, soʻroq belgisi, undov belgisi."),
    ("ot", "Kim? nima? soʻroqlariga javob beruvchi, narsa-buyumni bildiruvchi soʻz turkumi.", "Kitob, maktab, ona — otlar."),
    ("sifat", "Narsaning belgisini bildiruvchi, qanday? qaysi? soʻroqlariga javob beruvchi soʻz turkumi.", "Chiroyli, katta — sifatlar."),
    ("son", "Narsaning miqdori yoki tartibini bildiruvchi, nechta? nechanchi? soʻroqlariga javob beruvchi soʻz turkumi.", "Uch, besh, oʻninchi — sonlar."),
    ("olmosh", "Ot, sifat, son oʻrnida ishlatiladigan soʻz turkumi.", "Men, sen, u — olmoshlar."),
    ("feʼl", "Ish-harakat yoki holatni bildiruvchi, nima qildi? nima qilyapti? soʻroqlariga javob beruvchi soʻz turkumi.", "Yozmoq, oʻqimoq — feʼllar."),
    ("ravish", "Harakatning belgisini (payt, tarz, miqdor, oʻrin) bildiruvchi soʻz turkumi.", "Tez, ertaga, juda — ravishlar."),
    ("koʻmakchi", "Soʻzlar orasidagi munosabatni bildiruvchi yordamchi soʻz turkumi.", "Bilan, uchun, kabi — koʻmakchilar."),
    ("bogʻlovchi", "Soʻz va gaplarni bir-biriga bogʻlovchi yordamchi soʻz turkumi. Turlari: biriktiruvchi, ayiruvchi, zid, sabab, natija, shart, qarshilik, maqsad, izohlovchi.", "Va, lekin, chunki — bogʻlovchilar."),
    ("yuklama", "Soʻz yoki gapga qoʻshimcha maʼno beruvchi yordamchi soʻz turkumi.", "Faqat, hatto, -mi — yuklamalar."),
    ("undov soʻz", "His-hayajon, chaqiriq bildiruvchi soʻz turkumi.", "Oh, ey, barakalla — undov soʻzlar."),
    ("modal soʻz", "Soʻzlovchining aytilgan fikrga munosabatini bildiruvchi soʻz turkumi.", "Albatta, ehtimol, afsuski — modal soʻzlar."),
    ("taqlid soʻz", "Tovush yoki holatga taqlid qiluvchi soʻz turkumi.", "Taq-taq, shildir-shildir — taqlid soʻzlar."),
]

OT = [
    ("ona", "Farzandni dunyoga keltirgan ayol.", "Onam menga ertak aytib berdi."),
    ("ota", "Farzandning erkak ota-onasi.", "Otam dalada ishlaydi."),
    ("bola", "Yosh, voyaga yetmagan inson.", "Bola bogʻda oʻynayapti."),
    ("oʻqituvchi", "Bilim beruvchi kasb egasi.", "Oʻqituvchi darsni tushuntirdi."),
    ("oʻquvchi", "Maktabda taʼlim oluvchi bola.", "Oʻquvchilar sinfga kirishdi."),
    ("kitob", "Bosilgan, varaqlardan iborat oʻqiladigan asar.", "Men yangi kitob oʻqiyapman."),
    ("daftar", "Yozish uchun varaqlardan tikilgan buyum.", "Daftarga uy vazifasini yozdim."),
    ("qalam", "Yozish va chizish uchun asbob.", "Qalamim sinib qoldi."),
    ("maktab", "Bolalar taʼlim oladigan joy.", "Ertalab maktabga boraman."),
    ("uy", "Odamlar yashaydigan bino.", "Bizning uyimiz katta."),
    ("shahar", "Aholisi koʻp, yirik aholi punkti.", "Toshkent — katta shahar."),
    ("qishloq", "Aholisi asosan dehqonchilik bilan shugʻullanadigan joy.", "Bobom qishloqda yashaydi."),
    ("daryo", "Katta oqar suv.", "Daryo togʻdan boshlanadi."),
    ("togʻ", "Yer yuzining baland qismi.", "Togʻ choʻqqisida qor bor."),
    ("daraxt", "Tanasi yogʻochlashgan oʻsimlik.", "Bogʻda baland daraxtlar oʻsadi."),
    ("gul", "Oʻsimlikning chiroyli, xushboʻy qismi.", "Bahorda gullar ochiladi."),
    ("bahor", "Qish bilan yoz oralagʻidagi fasl.", "Bahor kelishi bilan dalalar yashillandi."),
    ("quyosh", "Yerga yorugʻlik va issiqlik beruvchi yulduz.", "Quyosh sharqdan chiqadi."),
    ("oy", "Yerning tabiiy yoʻldoshi.", "Tunda oy porladi."),
    ("yulduz", "Osmonda yorugʻ nuqta boʻlib koʻrinadigan samoviy jism.", "Osmon yulduzlarga toʻla."),
    ("osmon", "Yer ustidagi bepoyon fazo.", "Osmon musaffo edi."),
    ("suv", "Rangsiz, mazasiz suyuqlik.", "Men suv ichdim."),
    ("non", "Undan pishirilgan asosiy oziq-ovqat.", "Issiq non juda mazali."),
    ("olma", "Mevali daraxt va uning mevasi.", "Olma shirin ekan."),
    ("mehr", "Yaqin kishilarga boʻlgan iliq tuygʻu.", "Onasi unga mehr bilan qaradi."),
    ("doʻst", "Samimiy, ishonchli yaqin kishi.", "Doʻstim menga yordam berdi."),
    ("vatan", "Kishi tugʻilib oʻsgan, xalqning ona yurti.", "Vatan har kimga aziz."),
    ("til", "Odamlarning fikr almashish vositasi.", "Ona tilimizni sevamiz."),
    ("xalq", "Bir yurtda yashovchi, umumiy tarixga ega odamlar.", "Xalq mehnatsevar."),
    ("hayot", "Tirik mavjudotning yashash jarayoni.", "Hayot goʻzal."),
    ("bilim", "Oʻrganish orqali olingan maʼlumot va tushuncha.", "Bilim — kuch."),
    ("ish", "Mehnat, faoliyat.", "Ota ishdan qaytdi."),
    ("kun", "Ikki tun oralagʻidagi vaqt.", "Bugun issiq kun."),
    ("tun", "Quyosh botgandan keyingi qorongʻi vaqt.", "Tun sokin edi."),
    ("yoʻl", "Yurish uchun moʻljallangan joy.", "Yoʻl uzoq edi."),
    ("kuch", "Harakat qilish, ish bajarish qobiliyati.", "Birlikda kuch bor."),
    ("orzu", "Amalga oshishi istalgan niyat.", "Mening orzuim — shifokor boʻlish."),
    ("dala", "Ekin ekiladigan keng yer.", "Dehqonlar dalada ishlaydi."),
    ("bogʻ", "Meva daraxtlari oʻsadigan yer.", "Bogʻda qushlar sayradi."),
    ("qush", "Qanotli, patli hayvon.", "Qush daraxtda oʻtirdi."),
    ("bozor", "Savdo-sotiq qilinadigan joy.", "Bozorda meva sotildi."),
    ("kutubxona", "Kitoblar saqlanadigan va oʻqiladigan joy.", "Kutubxonada kitob oldim."),
    ("shifokor", "Kasallarni davolovchi kasb egasi.", "Shifokor bemorni koʻrdi."),
    ("dehqon", "Yer ekib, ekin yetishtiruvchi kishi.", "Dehqon dalada ishlayapti."),
    ("ustoz", "Bilim va hunar oʻrgatuvchi kishi.", "Ustoz shogirdiga maslahat berdi."),
    ("talaba", "Oliy oʻquv yurtida taʼlim oluvchi.", "Talaba maʼruzani tingladi."),
    ("mashina", "Yoʻlda yuradigan transport vositasi.", "Mashina tez yurdi."),
    ("stol", "Ustida yozadigan yoki ovqatlanadigan mebel.", "Stol ustida kitob yotibdi."),
    ("eshik", "Xonaga kirish-chiqish uchun moʻljallangan qurilma.", "Eshik ochiq edi."),
    ("deraza", "Xonaga yorugʻlik tushadigan oynali joy.", "Deraza ochiq qoldi."),
    ("qor", "Qishda yogʻadigan oq muz zarralari.", "Qor yogʻdi."),
    ("yomgʻir", "Osmondan tomchi boʻlib yogʻadigan suv.", "Yomgʻir yogʻmoqda."),
    ("shamol", "Havoning harakati.", "Shamol kuchaydi."),
    ("tosh", "Qattiq, yirik moddadan iborat jism.", "Tosh juda ogʻir."),
    ("dengiz", "Katta shoʻr suv havzasi.", "Dengiz tinch edi."),
    ("oila", "Birga yashaydigan qarindoshlar guruhi.", "Oila — jamiyat poydevori."),
]

SIFAT = [
    ("chiroyli", "Koʻrinishi yoqimli, goʻzal.", "Chiroyli gul ochildi."),
    ("katta", "Hajmi yoki yoshi jihatidan yirik.", "Biz katta uyda yashaymiz."),
    ("kichik", "Hajmi yoki yoshi jihatidan mayda.", "Mening kichik ukam bor."),
    ("baland", "Yer yuzasidan yuqoriga choʻzilgan.", "Baland togʻ koʻrindi."),
    ("past", "Balandligi kam.", "Past devor ustidan oshdi."),
    ("uzun", "Uzunligi katta.", "Uzun yoʻl bosib keldik."),
    ("qisqa", "Uzunligi kam.", "Qisqa hikoya oʻqidim."),
    ("yaxshi", "Foydali, ijobiy sifatli.", "U yaxshi talaba."),
    ("yomon", "Salbiy, noxush sifatli.", "Yomon odat zararli."),
    ("yangi", "Yaqinda paydo boʻlgan.", "Menga yangi kitob olib berishdi."),
    ("eski", "Anchadan beri mavjud, yangi emas.", "Eski uy buzildi."),
    ("toza", "Ifloslanmagan, pokiza.", "Xonamiz toza."),
    ("iflos", "Kirlangan, toza emas.", "Iflos qoʻlni yuvdim."),
    ("issiq", "Harorati yuqori.", "Bugun havo issiq."),
    ("sovuq", "Harorati past.", "Qishda havo sovuq boʻladi."),
    ("shirin", "Shakar kabi mazali.", "Shirin uzum yedik."),
    ("nordon", "Limon kabi nordon mazali.", "Nordon olma yoqmadi."),
    ("achchiq", "Garmdori kabi achchiq mazali.", "Achchiq qalampir yedim."),
    ("qizil", "Qon rangidagi.", "Qizil gul sotib oldim."),
    ("oq", "Qor rangidagi.", "Oq koʻylak kiydi."),
    ("qora", "Koʻmir rangidagi.", "Qora mushuk yugurdi."),
    ("yashil", "Oʻt rangidagi.", "Yashil daraxtlar oʻsdi."),
    ("sariq", "Limon rangidagi.", "Kuzda barglar sariq tusga kiradi."),
    ("koʻk", "Osmon rangidagi.", "Koʻk dengiz yaltirab turardi."),
    ("mehribon", "Boshqalarga mehr bilan munosabatda boʻladigan.", "Mehribon oʻqituvchi."),
    ("dono", "Aqlli, hayotiy tajribali.", "Dono kishi maslahat berdi."),
    ("botir", "Qoʻrqmas, jasur.", "Botir yigit xavfdan qochmadi."),
    ("tinch", "Shovqin-suronsiz, xotirjam.", "Tinch qishloq."),
    ("quvnoq", "Shod-xurram, kayfiyati yaxshi.", "Bolalar quvnoq oʻynashdi."),
    ("mehnatsevar", "Mehnat qilishni yaxshi koʻradigan.", "Mehnatsevar dehqon."),
    ("keng", "Eni katta.", "Keng koʻcha."),
    ("tor", "Eni kichik.", "Tor yoʻlak."),
    ("ogʻir", "Vazni katta.", "Ogʻir yuk."),
    ("yengil", "Vazni kam.", "Yengil sumka."),
    ("yumshoq", "Qattiq emas.", "Yumshoq non."),
    ("qattiq", "Yumshoq emas.", "Qattiq tosh."),
    ("yosh", "Yoshi kichik.", "Yosh yigit."),
    ("qari", "Yoshi katta.", "Qari daraxt."),
    ("boy", "Mol-mulki koʻp.", "Boy oila."),
    ("sodiq", "Vafodor, ishonchli.", "Sodiq doʻst."),
]

SON = [
    ("bir", "Sanoq son: 1.", "Menda bir qalam bor."),
    ("ikki", "Sanoq son: 2.", "Ikki doʻstim keldi."),
    ("uch", "Sanoq son: 3.", "Uch kun oʻtdi."),
    ("toʻrt", "Sanoq son: 4.", "Yilning toʻrt fasli bor."),
    ("besh", "Sanoq son: 5.", "Qoʻlimda besh barmoq bor."),
    ("oʻn", "Sanoq son: 10.", "Oʻn kishi qatnashdi."),
    ("yigirma", "Sanoq son: 20.", "Yigirma soʻm."),
    ("yuz", "Sanoq son: 100.", "Yuz yil oʻtdi."),
    ("ming", "Sanoq son: 1000.", "Ming rahmat."),
    ("million", "Sanoq son: 1 000 000.", "Shaharda bir million aholi bor."),
    ("birinchi", "Tartib son: sanoqda 1-oʻrindagi.", "Birinchi sinfga bordim."),
    ("ikkinchi", "Tartib son: sanoqda 2-oʻrindagi.", "Ikkinchi qavatda yashaymiz."),
    ("uchta", "Dona son: narsalarning uch dona ekanini bildiradi.", "Uchta olma yedim."),
    ("beshta", "Dona son: narsalarning besh dona ekanini bildiradi.", "Beshta daftar oldim."),
    ("yarim", "Kasr son: butunning ikkidan bir qismi.", "Yarim non."),
    ("oʻnlab", "Taxminiy son: oʻnga yaqin yoki oʻn marta koʻp.", "Oʻnlab odam keldi."),
    ("olti", "Sanoq son: 6.", "Olti kishi keldi."),
    ("yetti", "Sanoq son: 7.", "Haftada yetti kun bor."),
    ("sakkiz", "Sanoq son: 8.", "Sakkiz soat uxladim."),
    ("toʻqqiz", "Sanoq son: 9.", "Toʻqqiz yoshga toʻldi."),
    ("oʻttiz", "Sanoq son: 30.", "Oʻttiz kun oʻtdi."),
    ("qirq", "Sanoq son: 40.", "Qirq bola qatnashdi."),
    ("ellik", "Sanoq son: 50.", "Ellik soʻm."),
    ("oltmish", "Sanoq son: 60.", "Oltmish daqiqa — bir soat."),
    ("yetmish", "Sanoq son: 70.", "Yetmish yosh."),
    ("sakson", "Sanoq son: 80.", "Sakson kishi yigʻildi."),
    ("toʻqson", "Sanoq son: 90.", "Toʻqson sahifa oʻqidim."),
    ("uchinchi", "Tartib son: sanoqda 3-oʻrindagi.", "Uchinchi sinfda oʻqiyman."),
    ("toʻrtinchi", "Tartib son: sanoqda 4-oʻrindagi.", "Toʻrtinchi qavatda yashayman."),
    ("beshinchi", "Tartib son: sanoqda 5-oʻrindagi.", "Beshinchi dars boshlandi."),
    ("ikkita", "Dona son: narsalarning ikki dona ekanini bildiradi.", "Ikkita qalam oldim."),
    ("toʻrtta", "Dona son: narsalarning toʻrt dona ekanini bildiradi.", "Toʻrtta kitob oldim."),
    ("chorak", "Kasr son: butunning toʻrtdan bir qismi.", "Bir chorak non yedim."),
]

OLMOSH = [
    ("men", "Kishilik olmoshi: gapiruvchining oʻzi (I shaxs, birlik).", "Men kitob oʻqiyman."),
    ("sen", "Kishilik olmoshi: suhbatdosh (II shaxs, birlik).", "Sen qayerga borasan?"),
    ("u", "Kishilik olmoshi: uchinchi shaxs (III shaxs, birlik).", "U maktabga ketdi."),
    ("biz", "Kishilik olmoshi: gapiruvchi va boshqalar (I shaxs, koʻplik).", "Biz birga oʻqiymiz."),
    ("siz", "Kishilik olmoshi: hurmat bilan murojaat (II shaxs).", "Siz bilan tanishganimdan xursandman."),
    ("ular", "Kishilik olmoshi: uchinchi shaxs koʻplik.", "Ular bogʻga ketishdi."),
    ("bu", "Koʻrsatish olmoshi: yaqindagi narsani koʻrsatadi.", "Bu mening kitobim."),
    ("shu", "Koʻrsatish olmoshi: aniq koʻrsatilgan narsani bildiradi.", "Shu uyda yashayman."),
    ("oʻsha", "Koʻrsatish olmoshi: uzoqdagi yoki oldin aytilgan narsani koʻrsatadi.", "Oʻsha bola menga qaradi."),
    ("kim", "Soʻroq olmoshi: shaxsni soʻraydi.", "Kim keldi?"),
    ("nima", "Soʻroq olmoshi: narsa yoki hodisani soʻraydi.", "Bu nima?"),
    ("qaysi", "Soʻroq olmoshi: bir necha narsadan birini soʻraydi.", "Qaysi kitobni oldingiz?"),
    ("qanday", "Soʻroq olmoshi: belgi-xususiyatni soʻraydi.", "U qanday odam?"),
    ("qancha", "Soʻroq olmoshi: miqdorni soʻraydi.", "Qancha pul kerak?"),
    ("hamma", "Belgilash olmoshi: barcha shaxslarni qamrab oladi.", "Hamma darsga keldi."),
    ("barcha", "Belgilash olmoshi: toʻliq qamrab oladi.", "Barcha oʻquvchilar qatnashdi."),
    ("har", "Belgilash olmoshi: har bir shaxs yoki narsa.", "Har kuni kitob oʻqiyman."),
    ("butun", "Belgilash olmoshi: hech biri qolmasdan, toʻliq.", "Butun qishloq yigʻildi."),
    ("hech kim", "Boʻlishsizlik olmoshi: birorta ham shaxs yoʻqligini bildiradi.", "Hech kim kelmadi."),
    ("hech narsa", "Boʻlishsizlik olmoshi: birorta ham narsa yoʻqligini bildiradi.", "Men hech narsa bilmayman."),
    ("kimdir", "Gumon olmoshi: nomaʼlum shaxsni bildiradi.", "Eshik oldida kimdir turibdi."),
    ("nimadir", "Gumon olmoshi: nomaʼlum narsani bildiradi.", "U nimadir dedi."),
    ("oʻz", "Oʻzlik olmoshi: ish-harakat egasining oʻziga qarashliligini bildiradi.", "U oʻz ishini bajardi."),
    ("oʻzim", "Oʻzlik olmoshi: I shaxsning oʻzi.", "Buni oʻzim qildim."),
    ("har kim", "Belgilash olmoshi: har bir shaxsni bildiradi.", "Har kim oʻz ishini qiladi."),
    ("biror", "Gumon olmoshi: noaniq shaxs yoki narsani bildiradi.", "Biror kitob oʻqidingmi?"),
    ("shunday", "Koʻrsatish olmoshi: belgi-xususiyatni koʻrsatadi.", "Shunday gap boʻlmaydi."),
    ("bunday", "Koʻrsatish olmoshi: belgi-xususiyatni koʻrsatadi.", "Bunday ish yoʻq."),
]

FEIL = [
    ("oʻqimoq", "Yozilganni anglab aytmoq yoki mutolaa qilmoq; taʼlim olmoq.", "U kitob oʻqiyapti."),
    ("yozmoq", "Qalam yoki klaviatura bilan harf va soʻzlarni tushirmoq.", "Men xat yozaman."),
    ("kelmoq", "Biror joyga yetib, yaqinlashmoq.", "Doʻstim bugun keldi."),
    ("bormoq", "Boshqa joyga qarab yoʻl olmoq.", "Ertaga maktabga boraman."),
    ("ketmoq", "Turgan joydan boshqa joyga yoʻl olmoq.", "U uydan ketdi."),
    ("aytmoq", "Soʻz bilan bildirmoq.", "Oʻqituvchi qoida aytdi."),
    ("gapirmoq", "Soʻzlamoq, nutq aytmoq.", "U ravon gapiradi."),
    ("koʻrmoq", "Koʻz bilan qaramoq, ilgʻamoq.", "Men togʻni koʻrdim."),
    ("eshitmoq", "Quloq bilan qabul qilmoq.", "Qushlar sayrashini eshitdim."),
    ("bilmoq", "Maʼlumotga ega boʻlmoq.", "Men javobni bilaman."),
    ("oʻylamoq", "Fikr yuritmoq.", "U masala ustida oʻyladi."),
    ("yugurmoq", "Tez yurmoq.", "Bola maydonda yugurdi."),
    ("yurmoq", "Oyoqda harakatlanmoq.", "Biz bogʻda yurdik."),
    ("turmoq", "Tik holda boʻlmoq; uygʻonib oʻrnidan turmoq.", "Ertalab erta turaman."),
    ("oʻtirmoq", "Joyga choʻkib tanani qoʻymoq.", "U stulga oʻtirdi."),
    ("yotmoq", "Tanani yer yoki oʻrinda choʻzilgan holatda tutmoq.", "Mushuk divanda yotibdi."),
    ("uxlamoq", "Uyquga ketmoq.", "Bola uxlayapti."),
    ("yemoq", "Ovqatni ogʻiz orqali qabul qilmoq.", "Biz non yedik."),
    ("ichmoq", "Suyuqlikni ogʻiz orqali qabul qilmoq.", "Men choy ichdim."),
    ("kulmoq", "Shodlik bilan ovoz chiqarmoq.", "Bolalar kulishdi."),
    ("yigʻlamoq", "Koʻz yoshi toʻkmoq.", "Chaqaloq yigʻladi."),
    ("sevmoq", "Mehr-muhabbat qoʻymoq.", "Men ona tilimni sevaman."),
    ("qurmoq", "Imorat yoki narsa yasamoq.", "Ular yangi uy qurdi."),
    ("ochmoq", "Yopiq narsani ochiq holga keltirmoq.", "Eshikni ochdim."),
    ("yopmoq", "Ochiq narsani berkitmoq.", "Derazani yoping."),
    ("boshlamoq", "Biror ishni dastlab qilmoq.", "Dars boshlandi."),
    ("tugatmoq", "Ishni oxiriga yetkazmoq.", "Vazifani tugatdim."),
    ("oʻrganmoq", "Bilim yoki malaka egallamoq.", "Men ingliz tilini oʻrganyapman."),
    ("oʻrgatmoq", "Boshqaga bilim yoki malaka bermoq.", "Ustoz bizga yozishni oʻrgatdi."),
    ("soʻramoq", "Savol bermoq; iltimos qilmoq.", "U yoʻlni soʻradi."),
    ("olmoq", "Biror narsani qoʻlga kiritmoq.", "Doʻkondan non oldim."),
    ("bermoq", "Biror narsani boshqaga uzatmoq.", "U menga kitob berdi."),
    ("qaramoq", "Nigohni biror tomonga yoʻnaltirmoq.", "U osmonga qaradi."),
    ("kutmoq", "Biror kishi yoki voqeaning kelishini intizor boʻlib turmoq.", "Doʻstimni kutyapman."),
    ("ishlamoq", "Mehnat qilmoq.", "Dada zavodda ishlaydi."),
    ("chizmoq", "Qalam yoki boʻr bilan chiziq tortmoq.", "U rasm chizdi."),
    ("yuvmoq", "Suv bilan tozalamoq.", "Men qoʻlimni yuvdim."),
    ("pishirmoq", "Ovqatni issiqlik bilan tayyorlamoq.", "Onam osh pishirdi."),
    ("ekmoq", "Urugʻ yoki koʻchatni oʻstirish uchun yerga solmoq.", "Dehqon bugʻdoy ekdi."),
    ("terimoq", "Meva yoki paxtani yigʻmoq.", "Biz olma terdik."),
    ("sotmoq", "Pulga almashtirmoq.", "U bozorda uzum sotdi."),
    ("uchmoq", "Havoda harakatlanmoq.", "Qush osmonda uchdi."),
    ("suzmoq", "Suvda harakatlanmoq.", "Baliqlar suzdi."),
    ("topmoq", "Izlangan yoki yoʻqolgan narsani qoʻlga kiritmoq.", "U yoʻqolgan kalitni topdi."),
    ("qidirmoq", "Topish uchun izlamoq.", "Men kitobni qidirdim."),
]

RAVISH = [
    ("tez", "Harakat tarzi: tezlik bilan.", "U tez yugurdi."),
    ("sekin", "Harakat tarzi: oʻrtacha tezlikdan past.", "Mashina sekin yurdi."),
    ("asta", "Harakat tarzi: shoshmasdan, yumshoq.", "Asta gapiring."),
    ("juda", "Daraja-miqdor: kuchli darajada.", "Bugun juda issiq."),
    ("ancha", "Daraja-miqdor: kam emas, bir muncha.", "Ancha uzoq yoʻl yurdik."),
    ("ozgina", "Miqdor: kam darajada.", "U ozgina dam oldi."),
    ("koʻp", "Miqdor: kam emas, ortiq darajada.", "U koʻp oʻqiydi."),
    ("kam", "Miqdor: oz, yetarli emas.", "U kam gapiradi."),
    ("bugun", "Payt: hozirgi kunda.", "Bugun dars yoʻq."),
    ("ertaga", "Payt: keyingi kunda.", "Ertaga uchrashamiz."),
    ("kecha", "Payt: oʻtgan kunda.", "Kecha yomgʻir yogʻdi."),
    ("hozir", "Payt: shu paytda.", "Men hozir ishlayapman."),
    ("avval", "Payt: oldin, birinchi navbatda.", "Avval dars tayyorla."),
    ("keyin", "Payt: biror ishdan soʻng.", "Keyin dam olamiz."),
    ("doim", "Payt: har vaqt, uzluksiz.", "U doim kitob oʻqiydi."),
    ("hamisha", "Payt: har doim.", "Hamisha rostgoʻy boʻling."),
    ("baʼzan", "Payt: ora-sira, vaqti-vaqti bilan.", "Baʼzan sayrga chiqamiz."),
    ("tez-tez", "Payt: koʻp marta takrorlanib.", "U bizga tez-tez keladi."),
    ("yana", "Takror: yana bir marta.", "Yana urinib koʻraylik."),
    ("hali", "Payt: hozirgacha, hanuz.", "Hali vaqt bor."),
    ("darhol", "Payt: kechiktirmasdan.", "Darhol javob bering."),
    ("birga", "Tarz: hamkorlikda.", "Biz birga bordik."),
    ("yaqin", "Oʻrin: masofasi kam holda.", "U maktabga yaqin yashaydi."),
    ("uzoq", "Payt: uzoq vaqt davomida.", "Uzoq kutdik."),
    ("qayta", "Takror: yana bir bor.", "Qayta urinib koʻring."),
    ("birdan", "Payt: kutilmaganda.", "U birdan toʻxtadi."),
    ("sekin-asta", "Tarz: ohista, shoshmasdan.", "Sekin-asta yuring."),
    ("deyarli", "Daraja: ozgina yetmay.", "U deyarli yetib keldi."),
    ("tamomila", "Daraja: butunlay.", "U tamomila oʻzgardi."),
    ("odatda", "Payt: koʻpincha.", "Odatda erta turaman."),
]

KOMAKCHI = [
    ("bilan", "Birgalik yoki vosita maʼnosini bildiradi.", "Doʻstim bilan keldim."),
    ("uchun", "Maqsad yoki sabab maʼnosini bildiradi.", "Bilim uchun oʻqiyman."),
    ("kabi", "Oʻxshashlikni bildiradi.", "U togʻ kabi mustahkam."),
    ("singari", "Oʻxshashlikni bildiradi.", "U ona singari mehribon."),
    ("sari", "Harakat yoʻnalishini bildiradi.", "Uy sari yurdim."),
    ("tomon", "Yoʻnalishni bildiradi.", "U shahar tomon ketdi."),
    ("qadar", "Chegara (vaqt, oʻrin, miqdor) maʼnosini bildiradi.", "Kechga qadar kutdim."),
    ("koʻra", "Asos yoki taqqoslash maʼnosini bildiradi.", "Rejaga koʻra ish bajarildi."),
    ("orqali", "Vosita yoki yoʻl maʼnosini bildiradi.", "Telefon orqali gaplashdik."),
    ("haqida", "Mavzuni bildiradi.", "U kitob haqida gapirdi."),
    ("toʻgʻrisida", "Mavzuni bildiradi.", "Sayohat toʻgʻrisida hikoya qildi."),
    ("boshqa", "Chiqarib tashlash (tashqari) maʼnosini bildiradi.", "Mendan boshqa hamma keldi."),
    ("beri", "Vaqt boshlanishini bildiradi.", "Kechadan beri yomgʻir yogʻyapti."),
    ("buyon", "Vaqt boshlanishini bildiradi.", "Bahordan buyon kutyapman."),
    ("boʻylab", "Harakat yoʻnalishi boʻyicha ketma-ketlikni bildiradi.", "Daryo boʻylab yurdik."),
    ("sayin", "Takror va ortib borishni bildiradi.", "Kun sayin kuchaymoqda."),
    ("tashqari", "Chiqarib tashlashni bildiradi.", "Mendan tashqari hamma bor."),
    ("qaramay", "Qarshilik maʼnosini bildiradi.", "Yomgʻirga qaramay chiqdik."),
    ("binoan", "Asos maʼnosini bildiradi.", "Qonunga binoan ish koʻrildi."),
    ("tomonidan", "Ish bajaruvchini bildiradi.", "Asar yozuvchi tomonidan yozilgan."),
    ("sababli", "Sabab maʼnosini bildiradi.", "Yomgʻir sababli kechikdik."),
]

BOGLOVCHI = [
    ("va", "Biriktiruvchi bogʻlovchi: teng boʻlaklarni bogʻlaydi.", "Ali va Vali keldi."),
    ("hamda", "Biriktiruvchi bogʻlovchi: teng boʻlaklarni bogʻlaydi.", "Kitob hamda daftar sotib oldim."),
    ("bilan", "Biriktiruvchi bogʻlovchi: «va» maʼnosida ishlatiladi.", "Ota bilan ona keldi."),
    ("yoki", "Ayiruvchi bogʻlovchi: tanlovni bildiradi.", "Choy yoki qahva ichasizmi?"),
    ("yoxud", "Ayiruvchi bogʻlovchi: tanlovni bildiradi.", "Bugun yoxud ertaga boraman."),
    ("yo", "Ayiruvchi bogʻlovchi (yo... yo): variantlardan birini bildiradi.", "Yo oʻqi, yo uxla."),
    ("goh... goh", "Ayiruvchi bogʻlovchi: navbatma-navbat takrorlanishni bildiradi.", "Goh yomgʻir yogʻdi, goh qor."),
    ("xoh... xoh", "Ayiruvchi bogʻlovchi: farqsizlikni bildiradi.", "Xoh sen kel, xoh u kelsin."),
    ("ham... ham", "Biriktiruvchi bogʻlovchi: ikki holatning birgaligini bildiradi.", "U ham oʻqiydi, ham ishlaydi."),
    ("na... na", "Biriktiruvchi bogʻlovchi (inkor shaklida): ikkala holatni inkor qiladi.", "Na yomgʻir, na shamol toʻsa oldi."),
    ("ammo", "Zid bogʻlovchi: qarama-qarshilikni bildiradi.", "Urindi, ammo eplay olmadi."),
    ("lekin", "Zid bogʻlovchi: qarama-qarshilikni bildiradi.", "Havo sovuq, lekin quyoshli."),
    ("biroq", "Zid bogʻlovchi: qarama-qarshilikni bildiradi.", "Kutdik, biroq u kelmadi."),
    ("balki", "Zid bogʻlovchi: inkordan keyin boshqa fikrni bildiradi.", "Bu kitob emas, balki daftar."),
    ("chunki", "Sabab bogʻlovchisi: sababni bildiradi.", "U kelmadi, chunki kasal edi."),
    ("negaki", "Sabab bogʻlovchisi: sababni bildiradi.", "Kechikdim, negaki yomgʻir yogʻdi."),
    ("sababki", "Sabab bogʻlovchisi: sababni bildiradi.", "Uyda qoldim, sababki ish koʻp edi."),
    ("shuning uchun", "Natija bogʻlovchisi: natijani bildiradi.", "Yomgʻir yogʻdi, shuning uchun uyda qoldik."),
    ("shu sababli", "Natija bogʻlovchisi: natijani bildiradi.", "U kasal edi, shu sababli kelmadi."),
    ("agar", "Shart bogʻlovchisi: shartni bildiradi.", "Agar yaxshi oʻqisang, qabul qilinasan."),
    ("basharti", "Shart bogʻlovchisi: shartni bildiradi.", "Basharti kelsangiz, xursand boʻlamiz."),
    ("mabodo", "Shart bogʻlovchisi: kam ehtimolli shartni bildiradi.", "Mabodo yomgʻir yogʻsa, uyda qolamiz."),
    ("garchi", "Qarshilik bogʻlovchisi: toʻsiq boʻlsa-da, harakat amalga oshishini bildiradi.", "Garchi charchagan boʻlsa-da, ishladi."),
    ("toki", "Maqsad bogʻlovchisi: maqsadni bildiradi.", "Yaxshi oʻqi, toki orzuingga yet."),
    ("yaʼni", "Izohlovchi bogʻlovchi: oldingi fikrni izohlaydi.", "U uch kundan keyin, yaʼni dushanba kuni keladi."),
]

YUKLAMA = [
    ("faqat", "Cheklash yuklamasi: boshqa narsani istisno qiladi.", "Menda faqat bitta qalam bor."),
    ("hatto", "Kuchaytirish yuklamasi: kutilmagan holatni bildiradi.", "Hatto bolalar ham bu masalani tushundi."),
    ("ham", "Kuchaytirish yuklamasi: qoʻshimcha maʼno beradi.", "Men ham boraman."),
    ("axir", "Kuchaytirish yuklamasi: tasdiqlash yoki eslatish.", "Axir, men senga aytgan edim."),
    ("nahotki", "Soʻroq-taʼkid yuklamasi: ajablanishni bildiradi.", "Nahotki u kelmasa?"),
    ("xuddi", "Qiyoslash yuklamasi: oʻxshashlikni bildiradi.", "Xuddi bahordek issiq."),
    ("goʻyo", "Qiyoslash yuklamasi: taxminiy oʻxshashlikni bildiradi.", "Goʻyo hech narsa boʻlmagandek turdi."),
    ("-mi", "Soʻroq yuklamasi: savol hosil qiladi.", "Siz keldingizmi?"),
    ("-chi", "Soʻroq-taʼkid yuklamasi: iltimos yoki taʼkidni bildiradi.", "Sen-chi?"),
    ("-ku", "Taʼkid yuklamasi: ajablanish va tasdiqni bildiradi.", "Kelding-ku!"),
    ("-oq", "Kuchaytirish yuklamasi: aniqlik yoki taʼkidni bildiradi.", "Bugunoq boraman."),
    ("-gina", "Kichraytirish yuklamasi: kamlik yoki erkalash maʼnosini beradi.", "Kichkinagina bola."),
    ("faqatgina", "Cheklash yuklamasi: «faqat» maʼnosini kuchaytiradi.", "Faqatgina bitta imkoniyat qoldi."),
    ("ayniqsa", "Ajratib koʻrsatish yuklamasi: alohida urgʻu beradi.", "Ayniqsa, bahor goʻzal."),
    ("xolos", "Cheklash yuklamasi: «faqat» maʼnosida.", "Bor-yoʻgʻi bir daqiqa xolos."),
]

UNDOV = [
    ("oh", "Hayajon, zavq yoki afsusni bildiradi.", "Oh, naqadar goʻzal!"),
    ("voy", "Ogʻriq, qoʻrquv yoki ajablanishni bildiradi.", "Voy, qoʻlim ogʻridi!"),
    ("uf", "Charchoq yoki norozilikni bildiradi.", "Uf, juda charchadim."),
    ("eh", "Afsus yoki armonni bildiradi.", "Eh, vaqt tez oʻtdi."),
    ("hoy", "Birovni chaqirish uchun ishlatiladi.", "Hoy, toʻxta!"),
    ("ey", "Murojaat yoki chaqiriq uchun ishlatiladi.", "Ey, doʻstlar, yigʻilinglar!"),
    ("ofarin", "Maqtov va tahsinni bildiradi.", "Ofarin, yaxshi bajarding!"),
    ("barakalla", "Maqtov va tahsinni bildiradi.", "Barakalla, yigit!"),
    ("attang", "Afsus va pushaymonni bildiradi.", "Attang, kechikib qoldim."),
    ("afsus", "Afsus-nadomat bildiradi.", "Afsus, imkoniyat qoʻldan ketdi."),
    ("tavba", "Ajablanish yoki hayratni bildiradi.", "Tavba, bu qanday gap?"),
    ("balli", "Maqtov, tahsinni bildiradi.", "Balli, aʼlo bajarding!"),
    ("ura", "Shodlik va gʻalabani bildiradi.", "Ura, gʻalaba qozondik!"),
    ("obbo", "Hayrat va ajablanishni bildiradi.", "Obbo, qanday chiroyli!"),
    ("iye", "Ajablanishni bildiradi.", "Iye, sen qachon kelding?"),
    ("tuf", "Nafrat va jirkanishni bildiradi.", "Tuf, qanday yomon hid!"),
    ("dod", "Yordamga chaqirish faryodini bildiradi.", "Dod, yordam bering!"),
    ("ayyo", "Afsus va hayratni bildiradi.", "Ayyo, nima boʻlib qoldi?"),
    ("essiz", "Afsus va kuyinishni bildiradi.", "Essiz, vaqt yetmadi."),
    ("qani", "Ragʻbatlantirish yoki chaqiruvni bildiradi.", "Qani, boshlaylik!"),
]

MODAL = [
    ("albatta", "Ishonch, aniqlikni bildiradi.", "Albatta, men yordam beraman."),
    ("shubhasiz", "Gumonsiz ishonchni bildiradi.", "Shubhasiz, u gʻolib boʻladi."),
    ("ehtimol", "Taxmin va ehtimolni bildiradi.", "Ehtimol, u bugun kelar."),
    ("balki", "Taxmin, ehtimol maʼnosini bildiradi.", "Balki, yomgʻir yogʻar."),
    ("aftidan", "Koʻrinishga qarab fikr bildiradi.", "Aftidan, u charchagan."),
    ("afsuski", "Afsus va noxushlik bildiradi.", "Afsuski, vaqt yetmadi."),
    ("xayriyat", "Yengillik, yaxshi tomonga ishora bildiradi.", "Xayriyat, hammasi yaxshi tugadi."),
    ("darhaqiqat", "Haqiqatan, tasdiq maʼnosini bildiradi.", "Darhaqiqat, u haq ekan."),
    ("mumkin", "Imkoniyat, ruxsat bildiradi.", "Bu yerda oʻtirish mumkin."),
    ("kerak", "Zarurlik bildiradi.", "Dars tayyorlash kerak."),
    ("zarur", "Muhim ehtiyoj bildiradi.", "Ushbu hujjat zarur."),
    ("lozim", "Lozimlik, tavsiya bildiradi.", "Vaqtida kelish lozim."),
    ("shekilli", "Taxmin, gumon bildiradi.", "U kasal shekilli."),
    ("chamasi", "Taxmin bildiradi.", "Chamasi, u kelmaydi."),
    ("xullas", "Xulosa bildiradi.", "Xullas, ish tugadi."),
    ("demak", "Xulosa, natija bildiradi.", "Demak, u kelmabdi."),
    ("darvoqe", "Gap orasida eslatma, qoʻshimcha fikr bildiradi.", "Darvoqe, uchrashuv ertaga."),
]

TAQLID = [
    ("taq-taq", "Taqillagan ovozga taqlid.", "Eshik taq-taq qilib taqillatildi."),
    ("tiq-tiq", "Soat yoki mayda zarbalar ovoziga taqlid.", "Soat tiq-tiq qilardi."),
    ("shildir-shildir", "Suvning sekin oqish ovoziga taqlid.", "Ariqda suv shildir-shildir oqardi."),
    ("gʻijir-gʻijir", "Gʻijirlash ovoziga taqlid.", "Eshik gʻijir-gʻijir qildi."),
    ("vov-vov", "Itning akillash ovoziga taqlid.", "It vov-vov deb akilladi."),
    ("miyov-miyov", "Mushukning ovoziga taqlid.", "Mushuk miyov-miyov qildi."),
    ("qagʻ-qagʻ", "Qargʻaning ovoziga taqlid.", "Qargʻalar qagʻ-qagʻ qilishdi."),
    ("yaltir-yultur", "Yaltirab koʻrinishga taqlid.", "Yulduzlar yaltir-yultur qilardi."),
    ("taraq-turuq", "Qattiq narsalar urilganda chiqadigan shovqinga taqlid.", "Tashqarida taraq-turuq ovoz eshitildi."),
    ("shitir-shitir", "Quruq barg yoki qogʻoz shitirlashiga taqlid.", "Quruq barglar shitir-shitir qilardi."),
    ("gʻarch-gʻarch", "Qor yoki qum ustida yurganda chiqadigan tovushga taqlid.", "Qorda gʻarch-gʻarch qilib yurdik."),
    ("ku-ku", "Kakkuning ovoziga taqlid.", "Oʻrmonda ku-ku sadosi yangradi."),
    ("pitir-pitir", "Tez-tez, chaqqon harakatga taqlid.", "Bola pitir-pitir yugurib ketdi."),
    ("yarq-yurq", "Yarqirab porlashga taqlid.", "Quyoshda muz yarq-yurq qilardi."),
    ("jimir-jimir", "Miltillab yonishga taqlid.", "Yulduzlar jimir-jimir qilib turardi."),
    ("shivir-shivir", "Past ovozda, ohista gapirishga taqlid.", "Ular shivir-shivir gaplashdi."),
]

BADIIY = [
    ("koʻngil", "Qalb, his-tuygʻular markazi.", "Koʻngli toʻldi."),
    ("dil", "Qalb, yurak (sheʼriy nutqda).", "Dilimdagi gaplar koʻp."),
    ("nigoh", "Qarash, nazar.", "Nigohi mehr bilan lim-lim edi."),
    ("yor", "Sevgan inson, suyukli yoki yaqin doʻst.", "Yorining yoʻliga qaradi."),
    ("ishq", "Qattiq, kuchli muhabbat.", "Ishq — qalbning olovi."),
    ("vafo", "Sadoqat, ahdga amal qilish.", "Vafo — insoniylik belgisi."),
    ("jafo", "Azob-uqubat, zulm.", "Jafo chekdi, lekin sabr qildi."),
    ("hijron", "Ayriliq, judolik.", "Hijron azobi ogʻir."),
    ("visol", "Uchrashuv, birlashish.", "Visol onlari shirin."),
    ("armon", "Ushalmagan orzu, afsus.", "Armonda qoldi."),
    ("sabr", "Chidam, bardosh.", "Sabr — oltin."),
    ("dilbar", "Dilni oluvchi, suyukli.", "Dilbar qiz."),
    ("sarvqomat", "Sarv daraxtidek tik qaddi-qomatli.", "Sarvqomat yigit."),
    ("mahzun", "Gʻamgin, xafa.", "U mahzun boʻlib oʻtirdi."),
    ("shabnam", "Erta tongda oʻsimliklar ustiga tushgan nam tomchilari.", "Gul ustida shabnam yaltirardi."),
    ("gulshan", "Gullar bogʻi.", "Gulshanda bulbul sayradi."),
    ("sahar", "Erta tong, tong payti.", "Sahar chogʻida turdik."),
    ("falak", "Osmon, koʻk gumbazi.", "Falakka nazar soldi."),
    ("samo", "Osmon, bepoyon fazo.", "Samoda qushlar uchdi."),
    ("fido", "Qurbon; yoʻlida jonini bagʻishlagan.", "Vatan yoʻlida jon fido."),
]

ADABIY = [
    ("sheʼr", "Misralardan tuzilgan, ohangdor badiiy asar.", ""),
    ("nasr", "Sheʼriy shaklda boʻlmagan, oddiy yozma badiiy nutq.", "Hikoya va roman — nasr janrlari."),
    ("doston", "Katta hajmli, sheʼriy shakldagi epik asar.", ""),
    ("ruboiy", "Toʻrt misradan iborat sheʼriy shakl.", ""),
    ("gʻazal", "Baytlardan tuzilgan, qofiyali lirik sheʼriy janr.", ""),
    ("hikoya", "Hajmi kichik nasriy asar.", ""),
    ("qissa", "Hajmi hikoyadan katta, romandan kichik nasriy asar.", ""),
    ("roman", "Katta hajmli, murakkab voqealarni qamrab olgan nasriy asar.", ""),
    ("obraz", "Asarda tasvirlangan inson yoki hodisa timsoli.", "Asar qahramonining obrazi."),
    ("syujet", "Asardagi voqealar tizimi, ularning ketma-ketligi.", ""),
    ("qahramon", "Badiiy asarda tasvirlanuvchi bosh shaxs.", ""),
    ("muallif", "Asarni yaratgan kishi.", ""),
    ("mavzu", "Asarda yoritiladigan hayot hodisalari doirasi.", "Asar mavzusi — Vatan."),
    ("gʻoya", "Asarning asosiy fikri, mazmuni.", ""),
    ("janr", "Adabiy asarning turi.", "Hikoya, doston — janrlar."),
    ("misra", "Sheʼriy matndagi alohida qator.", ""),
    ("bayt", "Ikki misradan iborat sheʼriy qator.", ""),
    ("band", "Bir necha misradan iborat sheʼr boʻlagi.", ""),
    ("qofiya", "Misralar oxiridagi uygʻun tovushlar.", "Koʻz — soʻz."),
    ("vazn", "Sheʼrda boʻgʻinlarning maʼlum tartibda takrorlanishi, ohang.", ""),
    ("radif", "Qofiyadan keyin takrorlanadigan soʻz yoki soʻzlar guruhi.", ""),
    ("epitet", "Narsa belgisini tasviriy boʻyoq bilan beruvchi sifatlash.", "Oltin kuz."),
    ("metafora", "Soʻzni oʻxshashlik asosida koʻchma maʼnoda ishlatish.", "Quyosh — osmon chirogʻi."),
    ("oʻxshatish", "Bir narsani boshqasiga qiyoslash.", "Yuzi oydek yorugʻ."),
    ("jonlantirish", "Jonsiz narsaga jon belgisi berish.", "Tong kulib boqdi."),
    ("mubolagʻa", "Narsa yoki hodisani boʻrttirib tasvirlash.", "Koʻz yoshlari daryo boʻldi."),
    ("ramz", "Biror tushunchani ifodalovchi belgi.", "Oq kaptar — tinchlik ramzi."),
    ("dialog", "Ikki yoki undan ortiq kishining suhbati.", ""),
    ("monolog", "Bir kishining nutqi.", ""),
]

CATEGORIES = [
    {"key": "atama", "title": "📘 Ona tili atamalari", "label": "ona tili atamasi",
     "desc": "Grammatika va tilshunoslik atamalari", "entries": ATAMALAR},
    {"key": "ot", "title": "🏷️ Ot", "label": "ot",
     "desc": "Kim? nima? soʻroqlariga javob beruvchi soʻzlar", "entries": OT},
    {"key": "sifat", "title": "🎨 Sifat", "label": "sifat",
     "desc": "Qanday? qaysi? soʻroqlariga javob beruvchi, belgi bildiruvchi soʻzlar", "entries": SIFAT},
    {"key": "son", "title": "🔢 Son", "label": "son",
     "desc": "Necha? nechanchi? soʻroqlariga javob beruvchi soʻzlar", "entries": SON},
    {"key": "olmosh", "title": "👤 Olmosh", "label": "olmosh",
     "desc": "Ot, sifat, son oʻrnida ishlatiladigan soʻzlar", "entries": OLMOSH},
    {"key": "feil", "title": "🏃 Feʼl", "label": "feʼl",
     "desc": "Ish-harakat va holatni bildiruvchi soʻzlar", "entries": FEIL},
    {"key": "ravish", "title": "⚡ Ravish", "label": "ravish",
     "desc": "Harakat belgisini (payt, tarz, miqdor, oʻrin) bildiruvchi soʻzlar", "entries": RAVISH},
    {"key": "komakchi", "title": "🔗 Koʻmakchi", "label": "koʻmakchi",
     "desc": "Soʻzlar orasidagi munosabatni bildiruvchi yordamchi soʻzlar", "entries": KOMAKCHI},
    {"key": "boglovchi", "title": "🧩 Bogʻlovchi", "label": "bogʻlovchi",
     "desc": "Soʻz va gaplarni bogʻlovchi yordamchi soʻzlar (turlari bilan)", "entries": BOGLOVCHI},
    {"key": "yuklama", "title": "✨ Yuklama", "label": "yuklama",
     "desc": "Soʻz yoki gapga qoʻshimcha maʼno beruvchi yordamchi soʻzlar", "entries": YUKLAMA},
    {"key": "undov", "title": "❗ Undov soʻz", "label": "undov soʻz",
     "desc": "His-hayajon, chaqiriq bildiruvchi soʻzlar", "entries": UNDOV},
    {"key": "modal", "title": "💭 Modal soʻz", "label": "modal soʻz",
     "desc": "Soʻzlovchining fikrga munosabatini bildiruvchi soʻzlar", "entries": MODAL},
    {"key": "taqlid", "title": "🔊 Taqlid soʻz", "label": "taqlid soʻz",
     "desc": "Tovush yoki holatga taqlid qiluvchi soʻzlar", "entries": TAQLID},
    {"key": "badiiy", "title": "🌸 Badiiy soʻzlar", "label": "badiiy soʻz",
     "desc": "Sheʼriyat va badiiy nutqda keng qoʻllanadigan soʻzlar", "entries": BADIIY},
    {"key": "adabiy", "title": "🎭 Adabiy atamalar", "label": "adabiy atama",
     "desc": "Adabiyotshunoslik atamalari", "entries": ADABIY},
]

# Qidiruv uchun tekis roʻyxat: (soʻz, boʻlim nomi, izoh, misol)
WORDS = [(w, c["label"], meaning, example)
         for c in CATEGORIES for (w, meaning, example) in c["entries"]]


# ================= SOʻZ TURKUMLARI TESTLARI =================
# So'z turkumlari bo'yicha testlar: har bir turkum x 4 daraja x (eng ko'pi bilan) 50 savol.
# Savollar lug'atdagi (lugat.py) so'zlardan avtomatik tuziladi (har safar bir xil natija beradi).

TURKUM_KEYS = ["ot", "sifat", "son", "olmosh", "feil", "ravish",
               "komakchi", "boglovchi", "yuklama", "undov", "modal", "taqlid"]
GROUP = {"ot": "m", "sifat": "m", "son": "m", "olmosh": "m", "feil": "m", "ravish": "m",
         "komakchi": "y", "boglovchi": "y", "yuklama": "y",
         "undov": "a", "modal": "a", "taqlid": "a"}
TYPED = {"son", "olmosh", "boglovchi", "yuklama", "ravish"}
SEM_OK = {"ot", "sifat", "feil", "son", "olmosh"}  # izohlari bir-biridan aniq farq qiladigan turkumlar

POOL_SIZE = 50
QUIZ_LEVELS = [
    ("d1", "🌱 Boshlangʻich daraja"),
    ("d2", "🌿 Ozroq biladiganlar"),
    ("d3", "🌳 Oʻrtacha daraja"),
    ("d4", "🏆 Yuqori daraja"),
]

# Bir necha turkumda (yoki gapda har xil vazifada) kela oladigan so'zlar:
# ularni "noto'g'ri variant" sifatida ishlatmaymiz.
AMB = set("""tez yaxshi yomon koʻp kam yaqin uzoq baland past hozir bugun ertaga kecha avval keyin hali yana birga
bir yarim chorak oʻnlab kun tun ish yoʻl kuch orzu mehr bilim hamma barcha butun har oʻz oʻzim afsus tavba xayriyat balki ham
kerak mumkin zarur lozim tinch boy yosh qari sodiq qattiq shunday bunday boshqa tashqari tomon koʻra sababli qani
""".split())


# ------------------------------------------------------------------ yordamchilar
def _norm(t):
    for ch in ("ʻ", "ʼ", "’", "‘", "`", "'"):
        t = t.replace(ch, "'")
    return t.lower().strip()


_TOKEN_RE = re.compile(r"[\w'ʻʼ’-]+", re.U)


def _find_token(example, w, key):
    """Misol gapidan shu so'zning gapdagi shaklini topadi (aniq bitta bo'lsa)."""
    toks = _TOKEN_RE.findall(example)
    nw = _norm(w)
    if key == "feil" and nw.endswith("moq"):
        stem = nw[:-3]
        c = [t for t in toks if _norm(t).startswith(stem) and len(_norm(t)) > len(stem)]
        return c[0] if len(c) == 1 else None
    if " " in w or "." in w or w.startswith("-"):
        return None
    c = [t for t in toks if _norm(t) == nw]
    return c[0] if len(c) == 1 else None


def _content_words(text):
    return {x for x in re.findall(r"\w+", _norm(text)) if len(x) >= 5}


def _type_of(e):
    """Izoh boshidagi tur nomi (olmosh, son, bog'lovchi, yuklama, ravish uchun)."""
    if e["T"] not in TYPED or ":" not in e["m"]:
        return None
    pre = e["m"].split(":")[0].strip()
    if len(pre) > 45:
        return None
    T = e["T"]
    if T == "son":
        return pre
    first = pre.split()[0]
    if T == "olmosh":
        return f"{first} olmoshi"
    if T == "boglovchi":
        return f"{first} bogʻlovchi"
    if T == "yuklama":
        x = pre.replace(" yuklamasi", "")
        x = {"Soʻroq-taʼkid": "Soʻroq", "Taʼkid": "Kuchaytirish"}.get(x, x)
        return f"{x} yuklamasi"
    if T == "ravish":
        x = {"Daraja-miqdor": "Miqdor-daraja", "Miqdor": "Miqdor-daraja",
             "Daraja": "Miqdor-daraja"}.get(pre, pre)
        return f"{x} ravishi"
    return None


# ------------------------------------------------------------------ qo'lda yozilgan savollar
# (savol, toʻgʻri, xato1, xato2, xato3)
EXTRA = {
    "ot": {
        "d3": [
            ("Ot qaysi soʻroqlarga javob beradi?", "Kim? Nima?", "Qanday? Qaysi?", "Nima qildi?", "Necha? Nechanchi?"),
            ("Otning koʻplik qoʻshimchasi qaysi?", "-lar", "-ni", "-ga", "-dan"),
            ("«Maktab» soʻziga -da qoʻshimchasi qoʻshilsa, qaysi kelishik hosil boʻladi?", "Oʻrin-payt kelishigi",
             "Tushum kelishigi", "Qaratqich kelishigi", "Joʻnalish kelishigi"),
        ],
        "d4": [
            ("«Kitob» soʻziga -ni qoʻshimchasi qoʻshilsa, qaysi kelishik hosil boʻladi?", "Tushum kelishigi",
             "Bosh kelishik", "Qaratqich kelishigi", "Chiqish kelishigi"),
            ("Otlar maʼnosiga koʻra qaysi guruhlarga boʻlinadi?", "Atoqli va turdosh otlar",
             "Oddiy va orttirma otlar", "Oʻtgan va kelasi otlar", "Sanoq va tartib otlar"),
            ("«Toshkent» qanday ot?", "Atoqli ot", "Turdosh ot", "Sifat", "Olmosh"),
        ],
    },
    "sifat": {
        "d3": [
            ("Sifat qaysi soʻroqlarga javob beradi?", "Qanday? Qaysi?", "Kim? Nima?", "Nima qildi?", "Necha?"),
            ("Sifat darajalari nechta?", "3 ta", "2 ta", "4 ta", "5 ta"),
        ],
        "d4": [
            ("«Balandroq» soʻzi sifatning qaysi darajasida?", "Qiyosiy daraja", "Oddiy daraja", "Orttirma daraja", "Hech qaysi"),
            ("«Eng yaxshi» birikmasi sifatning qaysi darajasida?", "Orttirma daraja", "Oddiy daraja", "Qiyosiy daraja", "Hech qaysi"),
            ("Qiyosiy daraja qaysi qoʻshimcha bilan yasaladi?", "-roq", "-chi", "-lik", "-siz"),
            ("«U yaxshi talaba.» gapida «yaxshi» qaysi soʻz turkumi?", "sifat", "ravish", "ot", "olmosh"),
            ("«Tez poyezd keldi.» gapida «tez» qaysi soʻz turkumi?", "sifat", "ravish", "ot", "feʼl"),
        ],
    },
    "son": {
        "d3": [
            ("Son qaysi soʻroqlarga javob beradi?", "Necha? Nechanchi?", "Kim? Nima?", "Qanday?", "Nima qildi?"),
            ("«Uch» soʻzi sonning qaysi turiga kiradi?", "Sanoq son", "Tartib son", "Dona son", "Kasr son"),
        ],
        "d4": [
            ("«Uchinchi» soʻzi sonning qaysi turiga kiradi?", "Tartib son", "Sanoq son", "Dona son", "Kasr son"),
            ("«Beshta» soʻzidagi -ta qoʻshimchasi qaysi son turini yasaydi?", "Dona son", "Tartib son", "Kasr son", "Taxminiy son"),
            ("«Menda bir qalam bor.» gapida «bir» qaysi soʻz turkumi?", "son", "sifat", "olmosh", "ravish"),
        ],
    },
    "olmosh": {
        "d3": [
            ("Olmosh qaysi soʻz turkumlari oʻrnida ishlatiladi?", "Ot, sifat, son", "Feʼl, ravish, undov",
             "Bogʻlovchi, yuklama", "Faqat feʼl"),
            ("Quyidagilardan qaysi biri kishilik olmoshi?", "men", "kim", "hamma", "shu"),
        ],
        "d4": [
            ("Olmoshlar nechta turga boʻlinadi?", "7 ta", "5 ta", "6 ta", "9 ta"),
            ("«Kim?» olmoshi qaysi turga kiradi?", "Soʻroq olmoshi", "Kishilik olmoshi", "Gumon olmoshi", "Oʻzlik olmoshi"),
        ],
    },
    "feil": {
        "d3": [
            ("Feʼl qaysi soʻroqlarga javob beradi?", "Nima qildi? Nima qilyapti?", "Kim? Nima?", "Qanday?", "Necha?"),
            ("Feʼlning -moq bilan tugagan shakli nima deyiladi?", "Harakat nomi", "Sifatdosh", "Ravishdosh", "Buyruq shakli"),
        ],
        "d4": [
            ("Feʼlning asosiy zamonlari qaysilar?", "Oʻtgan, hozirgi, kelasi zamon", "Oddiy, qiyosiy, orttirma",
             "Bosh, qaratqich, tushum", "Sanoq, tartib, dona"),
            ("«Oʻqigan bola» birikmasidagi «oʻqigan» feʼlning qaysi shakli?", "Sifatdosh", "Harakat nomi", "Ravishdosh", "Buyruq shakli"),
            ("«Kulib gapirdi» birikmasidagi «kulib» feʼlning qaysi shakli?", "Ravishdosh", "Sifatdosh", "Harakat nomi", "Buyruq shakli"),
        ],
    },
    "ravish": {
        "d3": [
            ("Ravish nimani bildiradi?", "Harakatning belgisini", "Narsaning nomini", "Narsaning miqdorini sanashni", "His-hayajonni"),
            ("«Ertaga» soʻzi ravishning qaysi turiga kiradi?", "Payt ravishi", "Tarz ravishi", "Oʻrin ravishi", "Miqdor-daraja ravishi"),
        ],
        "d4": [
            ("«U tez yugurdi.» gapida «tez» qaysi soʻz turkumi?", "ravish", "sifat", "ot", "olmosh"),
            ("«U yaxshi oʻqiydi.» gapida «yaxshi» qaysi soʻz turkumi?", "ravish", "sifat", "ot", "olmosh"),
            ("Ravishning maʼno turlari qaysilar?", "Payt, tarz, oʻrin, miqdor-daraja", "Sanoq, tartib, dona, kasr",
             "Kishilik, soʻroq, gumon, oʻzlik", "Oddiy, qiyosiy, orttirma"),
        ],
    },
    "komakchi": {
        "d3": [
            ("Koʻmakchi qanday soʻz turkumiga kiradi?", "Yordamchi soʻz", "Mustaqil soʻz", "Taqlid soʻz", "Undov soʻz"),
            ("Koʻmakchi gap boʻlagi boʻla oladimi?", "Yoʻq, u yordamchi soʻz", "Ha, ega boʻladi", "Ha, kesim boʻladi", "Ha, hol boʻladi"),
        ],
        "d4": [
            ("«Doʻstim bilan keldim.» gapida «bilan» qaysi soʻz turkumi?", "koʻmakchi", "bogʻlovchi", "yuklama", "olmosh"),
            ("Quyidagi gaplardan qaysi birida «bilan» koʻmakchi?", "Men doʻstim bilan keldim.",
             "Ota bilan ona keldi.", "Ali bilan Vali oʻqiydi.", "Non bilan choy ichdik."),
        ],
    },
    "boglovchi": {
        "d3": [
            ("Bogʻlovchi nimani bogʻlaydi?", "Soʻz va gaplarni", "Faqat otlarni", "Faqat feʼllarni", "Tovushlarni"),
            ("Bogʻlovchilar mustaqil soʻzmi?", "Yoʻq, yordamchi soʻz", "Ha, mustaqil soʻz", "Ha, gap boʻlagi", "Faqat baʼzilari"),
        ],
        "d4": [
            ("«Ota bilan ona keldi.» gapida «bilan» qaysi soʻz turkumi?", "bogʻlovchi", "koʻmakchi", "yuklama", "ravish"),
            ("«Bu kitob emas, balki daftar.» gapida «balki» qaysi soʻz turkumi?", "bogʻlovchi", "modal soʻz", "yuklama", "ravish"),
            ("Bogʻlovchilar gap boʻlagi boʻla oladimi?", "Yoʻq", "Ha, ega boʻladi", "Ha, kesim boʻladi", "Ha, hol boʻladi"),
        ],
    },
    "yuklama": {
        "d3": [
            ("Yuklama qanday vazifa bajaradi?", "Soʻz yoki gapga qoʻshimcha maʼno beradi", "Ish-harakatni bildiradi",
             "Narsa nomini bildiradi", "Tovushga taqlid qiladi"),
            ("«-mi» yuklamasi qaysi gapni hosil qiladi?", "Soʻroq gapni", "Buyruq gapni", "Darak gapni", "Undov gapni"),
        ],
        "d4": [
            ("«Men ham boraman.» gapida «ham» qaysi soʻz turkumi?", "yuklama", "ravish", "olmosh", "koʻmakchi"),
            ("«Faqat» soʻzi qaysi yuklama turiga kiradi?", "Cheklash yuklamasi", "Soʻroq yuklamasi",
             "Qiyoslash yuklamasi", "Kichraytirish yuklamasi"),
        ],
    },
    "undov": {
        "d3": [
            ("Undov soʻzlar nimani bildiradi?", "His-hayajon, chaqiriqni", "Narsa nomini", "Ish-harakatni", "Miqdorni"),
            ("Quyidagilardan qaysi biri undov soʻz?", "Oh", "Kitob", "Yozmoq", "Uch"),
        ],
        "d4": [
            ("Undov soʻzlar gap boʻlagi boʻla oladimi?", "Yoʻq, gap boʻlagi boʻlmaydi", "Ha, ega boʻladi",
             "Ha, kesim boʻladi", "Faqat hol boʻladi"),
            ("Undov soʻzdan keyin odatda qaysi belgi qoʻyiladi?", "Undov belgisi yoki vergul", "Faqat nuqta", "Tire", "Qavs"),
        ],
    },
    "modal": {
        "d3": [
            ("Modal soʻzlar nimani bildiradi?", "Soʻzlovchining fikrga munosabatini", "Narsa nomini", "Tovushga taqlidni", "Sonni"),
            ("Quyidagilardan qaysi biri modal soʻz?", "albatta", "kitob", "oʻqimoq", "beshta"),
        ],
        "d4": [
            ("«Balki, yomgʻir yogʻar.» gapida «balki» qaysi soʻz turkumi?", "modal soʻz", "bogʻlovchi", "yuklama", "ravish"),
            ("«Albatta, men boraman.» gapida «albatta» qanday vazifada?", "Kirish soʻz", "Ega", "Kesim", "Toʻldiruvchi"),
        ],
    },
    "taqlid": {
        "d3": [
            ("Taqlid soʻzlar nimaga taqlid qiladi?", "Tovush yoki holatga", "Faqat sonlarga", "Faqat ranglarga", "Faqat nomlarga"),
            ("Quyidagilardan qaysi biri taqlid soʻz?", "taq-taq", "kitob", "chiroyli", "uchun"),
        ],
        "d4": [
            ("Taqlid soʻzlar koʻpincha qanday shaklda boʻladi?", "Juft yoki takroriy", "Faqat bitta boʻgʻinli",
             "Faqat sonlar bilan", "Faqat qoʻshimcha bilan"),
            ("«Vov-vov» taqlid soʻzi nimaning ovoziga taqlid?", "Itning", "Mushukning", "Qargʻaning", "Soatning"),
        ],
    },
}


# ------------------------------------------------------------------ asosiy qism
def build_turkum_tests(categories):
    """categories: lug'atdagi CATEGORIES. Natija: {turkum_kaliti: {daraja_kaliti: [savollar]}}"""
    cats = {c["key"]: c for c in categories if c["key"] in TURKUM_KEYS}
    LABEL = {k: cats[k]["label"] for k in TURKUM_KEYS}
    TITLE = {k: cats[k]["title"] for k in TURKUM_KEYS}

    ENT = {}
    for k in TURKUM_KEYS:
        ENT[k] = [{"w": w, "m": m, "ex": ex, "T": k} for (w, m, ex) in cats[k]["entries"]]

    # bir necha turkumda uchraydigan so'zlar
    count = {}
    for k in TURKUM_KEYS:
        for e in ENT[k]:
            count[_norm(e["w"])] = count.get(_norm(e["w"]), 0) + 1

    def plain(e):  # variant sifatida yaroqli (qo'shimcha emas, ko'p bo'lakli emas)
        w = e["w"]
        return not (w.startswith("-") or "..." in w)

    def strict(e):
        return plain(e) and count[_norm(e["w"])] == 1 and e["w"] not in AMB

    STRICT = {k: [e for e in ENT[k] if strict(e)] for k in TURKUM_KEYS}
    PLAIN = {k: [e for e in ENT[k] if plain(e)] for k in TURKUM_KEYS}

    def uniq_meaning(k):
        from collections import Counter
        cnt = Counter(e["m"] for e in ENT[k])
        return [e for e in PLAIN[k] if cnt[e["m"]] == 1]

    UM = {k: uniq_meaning(k) for k in TURKUM_KEYS}

    def others(k, near=False):
        keys = [x for x in TURKUM_KEYS if x != k]
        if near:
            g = [x for x in keys if GROUP[x] == GROUP[k]]
            pool = [e for x in g for e in STRICT[x]]
            if len(pool) >= 6:
                return pool
        return [e for x in keys for e in STRICT[x]]

    def ok_len(q, opts):
        return (len(q) <= 270 and all(len(o) <= 95 for o in opts)
                and len(set(opts)) == len(opts))

    def make(rng, q, right, wrongs, shuffle=True):
        opts = [right] + list(wrongs)
        if len(set(opts)) != len(opts) or not ok_len(q, opts):
            return None
        if shuffle:
            rng.shuffle(opts)
        return {"q": q, "o": opts, "a": opts.index(right)}

    def pick_other_words(rng, k, right_w, n=3, near=False):
        pool = [e for e in others(k, near) if _norm(e["w"]) != _norm(right_w)]
        if len(pool) < n:
            return None
        seen, res = set(), []
        for e in rng.sample(pool, len(pool)):
            if e["w"] not in seen:
                seen.add(e["w"]); res.append(e["w"])
            if len(res) == n:
                return res
        return None

    def other_labels(rng, k, n=3):
        return rng.sample([LABEL[x] for x in TURKUM_KEYS if x != k], n)

    def low_overlap(m1, m2):
        return not (_content_words(m1) & _content_words(m2))

    # ---------------- oilalar (har biri nomzod savollar generatori)
    def f_which_is(rng, k, rounds=1, near=False):
        lab = LABEL[k]
        for _ in range(rounds):
            for e in rng.sample(PLAIN[k], len(PLAIN[k])):
                wr = pick_other_words(rng, k, e["w"], 3, near)
                if wr:
                    yield make(rng, f"Quyidagilardan qaysi biri {lab}?", e["w"], wr)

    def f_meaning_far(rng, k):
        for e in rng.sample(UM[k], len(UM[k])):
            wr = pick_other_words(rng, k, e["w"], 3)
            if wr:
                yield make(rng, f"Quyidagi izohga mos soʻzni toping:\n«{e['m']}»", e["w"], wr)

    def f_word_to_label(rng, k):
        for e in rng.sample(STRICT[k], len(STRICT[k])):
            yield make(rng, f"«{e['w']}» soʻzi qaysi soʻz turkumiga kiradi?", LABEL[k], other_labels(rng, k))

    def f_yes_no(rng, k):
        lab = LABEL[k]
        pos = [e for e in PLAIN[k]]
        negpool = others(k)
        rng.shuffle(pos)
        i = 0
        while True:
            if i % 2 == 0 and pos:
                e = pos[(i // 2) % len(pos)]
                yield make(rng, f"«{e['w']}» soʻzi {lab} turkumiga kiradimi?", "Ha", ["Yoʻq"], shuffle=False)
            else:
                e = rng.choice(negpool)
                yield make(rng, f"«{e['w']}» soʻzi {lab} turkumiga kiradimi?", "Yoʻq", ["Ha"], shuffle=False)
            i += 1
            if i > 400:
                return

    def f_context(rng, k):
        for e in rng.sample(PLAIN[k], len(PLAIN[k])):
            tok = _find_token(e["ex"], e["w"], k)
            if not tok:
                continue
            yield make(rng, f"«{e['ex']}»\n\nShu gapdagi «{tok}» soʻzi qaysi soʻz turkumiga kiradi?",
                       LABEL[k], other_labels(rng, k))

    def f_meaning_same(rng, k):
        if k not in SEM_OK:
            return
        pool = UM[k]
        for e in rng.sample(pool, len(pool)):
            cands = [x for x in pool if x["w"] != e["w"] and low_overlap(e["m"], x["m"])]
            if len(cands) < 3:
                continue
            wr = [x["w"] for x in rng.sample(cands, 3)]
            yield make(rng, f"Quyidagi izohga mos soʻzni toping:\n«{e['m']}»", e["w"], wr)

    def f_not_is(rng, k, near=False, rounds=40):
        lab = LABEL[k]
        pool = PLAIN[k]
        if len(pool) < 3:
            return
        for _ in range(rounds):
            odd = rng.choice(others(k, near))
            three = [e["w"] for e in rng.sample(pool, 3)]
            yield make(rng, f"Quyidagilardan qaysi biri {lab} emas?", odd["w"], three)

    def f_meaning_of(rng, k):
        if k not in SEM_OK:
            return
        pool = UM[k]
        for e in rng.sample(pool, len(pool)):
            cands = [x for x in pool if x["w"] != e["w"] and low_overlap(e["m"], x["m"])]
            if len(cands) < 3:
                continue
            wr = [x["m"] for x in rng.sample(cands, 3)]
            yield make(rng, f"«{e['w']}» soʻzining izohi qaysi?", e["m"], wr)

    def f_type(rng, k):
        if k not in TYPED:
            return
        typed = [(e, _type_of(e)) for e in PLAIN[k]]
        typed = [(e, t) for e, t in typed if t]
        types = sorted({t for _, t in typed})
        if len(types) < 3:
            return
        for e, t in rng.sample(typed, len(typed)):
            wr = rng.sample([x for x in types if x != t], min(3, len(types) - 1))
            yield make(rng, f"«{e['w']}» soʻzi qaysi turga kiradi?", t, wr)

    def f_pair(rng, k, near=False, rounds=60):
        lab_pool = STRICT[k]
        negpool = others(k, near)
        for i in range(rounds):
            if i % 2 == 0 and len(lab_pool) >= 2:
                a, b = rng.sample(lab_pool, 2)
                yield make(rng, f"«{a['w']}» va «{b['w']}» soʻzlari bir soʻz turkumiga kiradimi?",
                           "Ha", ["Yoʻq"], shuffle=False)
            elif lab_pool:
                a = rng.choice(lab_pool); b = rng.choice(negpool)
                yield make(rng, f"«{a['w']}» va «{b['w']}» soʻzlari bir soʻz turkumiga kiradimi?",
                           "Yoʻq", ["Ha"], shuffle=False)

    def f_composite(rng, k):
        lab = LABEL[k]
        pool = UM[k]
        for e in rng.sample(pool, len(pool)):
            if len(e["m"]) > 80:
                continue
            ol = other_labels(rng, k, 2)
            diff = [x for x in pool if x["w"] != e["w"] and low_overlap(e["m"], x["m"]) and len(x["m"]) <= 80]
            if len(diff) < 2:
                continue
            m2 = rng.choice(diff)["m"]
            # boshqa turkumdan izoh
            oe = rng.choice([x for kk in TURKUM_KEYS if kk != k for x in UM[kk] if len(x["m"]) <= 80])
            right = f"{lab} — {e['m']}"
            wrongs = [f"{ol[0]} — {e['m']}", f"{lab} — {m2}", f"{ol[1]} — {oe['m']}"]
            yield make(rng, f"«{e['w']}» soʻzining turkumi va izohi toʻgʻri berilgan qatorni toping.", right, wrongs)

    def f_extra(rng, k, lvl):
        for (q, right, *wrongs) in EXTRA.get(k, {}).get(lvl, []):
            yield make(rng, q, right, wrongs)

    # ---------------- havzalarni yig'ish
    def collect(rng, gens, size=POOL_SIZE):
        pool, seen = [], set()
        for g in gens:
            for q in g:
                if not q:
                    continue
                key = (q["q"], q["o"][q["a"]])
                if key in seen:
                    continue
                seen.add(key); pool.append(q)
                if len(pool) >= size:
                    return pool
        return pool

    result = {}
    for k in TURKUM_KEYS:
        result[k] = {}
        r = lambda lv: random.Random(f"{k}-{lv}")
        rg = r("d1")
        result[k]["d1"] = collect(rg, [
            f_extra(rg, k, "d1"),
            f_which_is(rg, k, 1), f_meaning_far(rg, k), f_word_to_label(rg, k),
            f_yes_no(rg, k), f_which_is(rg, k, 3)])
        rg = r("d2")
        result[k]["d2"] = collect(rg, [
            f_extra(rg, k, "d2"),
            f_context(rg, k), f_meaning_same(rg, k), f_not_is(rg, k, False, 80)])
        rg = r("d3")
        result[k]["d3"] = collect(rg, [
            f_extra(rg, k, "d3"),
            f_meaning_of(rg, k), f_type(rg, k), f_pair(rg, k, False, 120), f_not_is(rg, k, True, 80)])
        rg = r("d4")
        result[k]["d4"] = collect(rg, [
            f_extra(rg, k, "d4"),
            f_composite(rg, k), f_not_is(rg, k, True, 80), f_pair(rg, k, True, 160)])
    meta = {"keys": TURKUM_KEYS, "title": TITLE, "label": LABEL}
    return result, meta


# ================= BOT =================
QUIZ_SIZE = 10  # har urinishda nechta savol

TOKEN = os.getenv("BOT_TOKEN", "").strip()
if ":" not in TOKEN:
    sys.exit("BOT_TOKEN noto'g'ri yoki yo'q. U shunday ko'rinadi: 123456789:AAH...\n"
             "Yozing: export BOT_TOKEN=\"butun_token\"")

URL = f"https://api.telegram.org/bot{TOKEN}/"
STATE = {}  # {user_id: {"level","qs","i","score","chat_id","poll_id"}}
LAST = {}   # {user_id: oxirgi test: ("gen", daraja) yoki ("tur", turkum, daraja)}
PICK = {}   # {user_id: tanlangan soʻz turkumi}

# Tugma matnlari
B_TESTS = "📝 Testlar"
B_DICT = "📖 Lug'at"
B_ABOUT = "ℹ️ Bot haqida"
B_MENU = "🏠 Menyu"
B_BACK = "⬅️ Orqaga"
B_RANDOM = "🎲 Tasodifiy so'z"
B_STOP = "⛔ Testni to'xtatish"
B_AGAIN = "🔁 Qayta yechish"
B_OTHER = "📝 Boshqa test"
B_GEN = "📊 Umumiy testlar"
B_TUR = "🧩 Soʻz turkumlari testi"

TITLE2KEY = {v["title"]: k for k, v in LEVELS.items()}
CAT2OBJ = {c["title"]: c for c in CATEGORIES}

TUR_TESTS, TUR_META = build_turkum_tests(CATEGORIES)
TUR_BTN = {"🧪 " + TUR_META["title"][k].split(" ", 1)[1]: k for k in TUR_META["keys"]}
TUR_BTN_REV = {v: k for k, v in TUR_BTN.items()}
LVL_BTN = {t: k for k, t in QUIZ_LEVELS}
LVL_TITLE = dict(QUIZ_LEVELS)


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


def tests_kb():
    return rk([[B_TUR], [B_GEN], [B_BACK]])


def levels_kb():
    rows = [[v["title"]] for v in LEVELS.values()]
    rows.append([B_OTHER, B_MENU])
    return rk(rows)


def tur_kb():
    items = list(TUR_BTN)
    rows = [items[i:i + 2] for i in range(0, len(items), 2)]
    rows.append([B_OTHER, B_MENU])
    return rk(rows)


def tur_levels_kb():
    rows = [[t] for _, t in QUIZ_LEVELS]
    rows.append([B_TUR, B_MENU])
    return rk(rows)


def dict_kb():
    rows, cur = [], []
    for c in CATEGORIES:
        cur.append(c["title"])
        if len(cur) == 2:
            rows.append(cur)
            cur = []
    if cur:
        rows.append(cur)
    rows.append([B_RANDOM, B_BACK])
    return rk(rows)


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
    text = (f"📖 <b>{word}</b> ({pos})\n\n"
            f"<b>Maʼnosi:</b> {meaning}")
    if example:
        text += f"\n<b>Misol:</b> <i>{example}</i>"
    return text


def send_category(chat_id, cat):
    """Bo'limdagi barcha so'zlarni izohi bilan yuboradi (uzun bo'lsa, bo'laklab)."""
    head = html.escape(f"{cat['title']} — {len(cat['entries'])} ta\n{cat['desc']}") + "\n\n"
    chunks, cur = [], head
    for w, meaning, _ in cat["entries"]:
        line = f"• <b>{html.escape(w)}</b> — {html.escape(meaning)}\n"
        if len(cur) + len(line) > 3800:
            chunks.append(cur)
            cur = ""
        cur += line
    cur += "\nMisolini koʻrish uchun soʻzni yozing."
    chunks.append(cur)
    for i, ch in enumerate(chunks):
        send(chat_id, ch, dict_kb() if i == len(chunks) - 1 else None, "HTML")


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
def start_quiz(uid, chat_id, title, pool, last):
    qs = [fresh(q) for q in random.sample(pool, min(QUIZ_SIZE, len(pool)))]
    STATE[uid] = {"title": title, "qs": qs, "i": 0, "score": 0,
                  "chat_id": chat_id, "poll_id": None}
    LAST[uid] = last
    send(chat_id, f"{title}\n\n{len(qs)} ta savol. Javobni bosing — "
                  "toʻgʻri javob darhol koʻrinadi. Omad! 🍀", quiz_kb())
    send_next(uid)


def start_general(uid, chat_id, level):
    start_quiz(uid, chat_id, LEVELS[level]["title"], LEVELS[level]["questions"], ("gen", level))


def start_turkum(uid, chat_id, tk, lv):
    title = f"{TUR_META['title'][tk]} — {LVL_TITLE[lv]}"
    start_quiz(uid, chat_id, title, TUR_TESTS[tk][lv], ("tur", tk, lv))


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
    score, total, title = st["score"], len(st["qs"]), st["title"]
    if score == total:
        comment = "Ajoyib! Hammasi toʻgʻri 🎉"
    elif score >= total * 0.8:
        comment = "Juda yaxshi! Keyingi darajaga oʻtishingiz mumkin 🚀"
    elif score >= total * 0.6:
        comment = "Yaxshi natija! Yana mashq qiling 👍"
    else:
        comment = "Hechqisi yoʻq, qayta urinib koʻring 💪"
    send(st["chat_id"],
         f"{html.escape(title)}\n\nNatija: <b>{score}/{total}</b>\n{comment}",
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
    return (sum(len(v["questions"]) for v in LEVELS.values())
            + sum(len(q) for d in TUR_TESTS.values() for q in d.values()))


def restart_last(uid, chat_id):
    last = LAST.get(uid)
    if last and last[0] == "gen":
        start_general(uid, chat_id, last[1])
    elif last and last[0] == "tur":
        start_turkum(uid, chat_id, last[1], last[2])
    else:
        send(chat_id, "Qaysi testni yechamiz? 👇", tests_kb())


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
             f"📝 Quiz-testlar ({total_questions()} ta savol): har bir soʻz turkumi uchun 4 darajada\n"
             "📖 lugʻat — soʻz yozing, maʼnosini topaman\n\n"
             "Quyidagi tugmalardan birini tanlang 👇", main_kb())
    elif text.startswith("/menu") or text in (B_MENU, B_BACK):
        STATE.pop(uid, None)
        PICK.pop(uid, None)
        send(chat_id, "Asosiy menyu 👇", main_kb())
    elif text == B_STOP:
        STATE.pop(uid, None)
        send(chat_id, "Test toʻxtatildi.", main_kb())
    elif text in (B_TESTS, B_OTHER):
        STATE.pop(uid, None)
        send(chat_id, "📝 Testlar\n\n🧩 Soʻz turkumlari testi — har bir turkum (ot, sifat, feʼl...) "
                      "uchun 4 darajada 50 tadan savol; har safar 10 tasi tasodifiy beriladi.\n"
                      "📊 Umumiy testlar — butun ona tili boʻyicha 4 daraja.", tests_kb())
    elif text == B_GEN:
        STATE.pop(uid, None)
        send(chat_id, levels_text(), levels_kb())
    elif text == B_TUR:
        STATE.pop(uid, None)
        send(chat_id, "Soʻz turkumini tanlang 👇", tur_kb())
    elif text in TUR_BTN:
        STATE.pop(uid, None)
        PICK[uid] = TUR_BTN[text]
        send(chat_id, f"{TUR_META['title'][PICK[uid]]}\n\nDarajani tanlang 👇\n"
                      "Har bir darajada 50 ta savol bor, 10 tasi tasodifiy beriladi.", tur_levels_kb())
    elif text in LVL_BTN:
        STATE.pop(uid, None)
        if PICK.get(uid) in TUR_TESTS:
            start_turkum(uid, chat_id, PICK[uid], LVL_BTN[text])
        else:
            send(chat_id, "Avval soʻz turkumini tanlang 👇", tur_kb())
    elif text in TITLE2KEY:
        STATE.pop(uid, None)
        start_general(uid, chat_id, TITLE2KEY[text])
    elif text == B_AGAIN:
        STATE.pop(uid, None)
        restart_last(uid, chat_id)
    elif text in CAT2OBJ:
        STATE.pop(uid, None)
        send_category(chat_id, CAT2OBJ[text])
    elif text == B_DICT:
        STATE.pop(uid, None)
        send(chat_id, f"📖 Lugʻat — {len(WORDS)} ta soʻz, {len(CATEGORIES)} ta boʻlim.\n\n"
                      "Boʻlimni tanlang yoki izohini bilmoqchi boʻlgan soʻzni yozing "
                      "(masalan: bilan, ona, sifat).", dict_kb())
    elif text == B_RANDOM:
        send(chat_id, format_word(random.choice(WORDS)), dict_kb(), "HTML")
    elif text == B_ABOUT:
        send(chat_id,
             "ℹ️ Bu bot ona tilini 0 dan oʻrganishga yordam beradi.\n\n"
             f"📝 Testlar: jami {total_questions()} ta savol (12 soʻz turkumi × 4 daraja × 50 + umumiy)\n"
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
            shown = "\n\n".join(format_word(w) for w in results[:5])
            if len(results) > 5:
                shown += f"\n\n… va yana {len(results) - 5} ta natija. Soʻzni aniqroq yozing."
            send(chat_id, shown, main_kb(), "HTML")


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
    print(f"Ona tili boti | savollar: {total_questions()}, lugʻat: {len(WORDS)} ta soʻz")
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
