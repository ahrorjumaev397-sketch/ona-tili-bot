"""Ona tili boti — BITTA FAYL: testlar + lug'at + bot. Qo'shimcha kutubxona kerak emas."""
import html
import json
import os
import random
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

# ================= LUG'AT =================
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
]

RAVISH = [
    ("tez", "Harakat tarzi: tezlik bilan.", "U tez yugurdi."),
    ("sekin", "Harakat tarzi: oʻrtacha tezlikdan past.", "Mashina sekin yurdi."),
    ("asta", "Harakat tarzi: shoshmasdan, yumshoq.", "Asta gapiring."),
    ("juda", "Daraja-miqdor: kuchli darajada.", "Bugun juda issiq."),
    ("ancha", "Daraja-miqdor: kam emas, bir muncha.", "Ancha uzoq yoʻl yurdik."),
    ("ozgina", "Miqdor: kam miqdorda.", "Menga ozgina suv bering."),
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
    ("yaqin", "Oʻrin: masofasi kam holda.", "U maktab yaqinida yashaydi."),
    ("uzoq", "Payt yoki oʻrin: choʻzilgan, anchagacha.", "Uzoq kutdik."),
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
    ("na... na", "Inkor bildiruvchi biriktiruvchi bogʻlovchi.", "Na yomgʻir, na shamol toʻsa oldi."),
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
    ("deb", "Maqsad yoki sabab maʼnosidagi bogʻlovchi.", "U yaxshi oʻqiyman deb harakat qildi."),
    ("shunday ekan", "Xulosa bogʻlovchisi: xulosani bildiradi.", "Vaqt koʻp, shunday ekan, shoshmaymiz."),
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
    ("hali", "Davom etayotgan holatni bildiruvchi yuklama.", "U hali kelmadi."),
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
CAT2OBJ = {c["title"]: c for c in CATEGORIES}


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
    print(f"Ona tili boti | savollar: {sum(len(v['questions']) for v in LEVELS.values())}, lugʻat: {len(WORDS)} ta soʻz")
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
