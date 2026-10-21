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


ORTACHA += [
    _q("«Oʻqiyotgan» soʻzida nechta boʻgʻin bor?", "4 ta", "3 ta", "5 ta", "2 ta"),
    _q("«Qalam» soʻzida nechta unli tovush bor?", "2 ta", "1 ta", "3 ta", "4 ta"),
    _q("«Tez yugurgan bola charchadi.» gapida ega qaysi soʻz?", "bola", "tez", "yugurgan", "charchadi"),
    _q("«Men kitobni oʻqidim.» gapida «kitobni» qaysi gap boʻlagi?", "Toʻldiruvchi", "Ega", "Kesim", "Hol"),
    _q("«Kecha biz bogʻga bordik.» gapida «kecha» qaysi gap boʻlagi?", "Hol", "Ega", "Toʻldiruvchi", "Aniqlovchi"),
    _q("Quyidagilardan qaysi biri gapning bosh boʻlagi?", "Ega", "Aniqlovchi", "Toʻldiruvchi", "Hol"),
    _q("Qaysi qatorda barcha soʻzlar sifat?", "chiroyli, baland, yashil", "chiroyli, kitob, yashil",
       "baland, yugurmoq, yashil", "chiroyli, baland, uchinchi"),
    _q("«Kitoblarimizdan» soʻzida nechta qoʻshimcha bor?", "3 ta", "2 ta", "4 ta", "1 ta"),
    _q("«Oʻqituvchi» soʻzi qanday yoʻl bilan yasalgan?", "Qoʻshimcha qoʻshish orqali",
       "Soʻzlarni qoʻshish orqali", "Soʻzni takrorlash orqali", "Soʻzni qisqartirish orqali"),
    _q("Feʼlning bosh shakli (harakat nomi) qaysi qoʻshimcha bilan tugaydi?", "-moq", "-gan", "-ib", "-di"),
    _q("«Chiroyli» soʻziga maʼnodosh (sinonim) qaysi?", "goʻzal", "xunuk", "yomon", "kichik"),
    _q("«Baland» soʻziga zid maʼnoli (antonim) soʻz qaysi?", "past", "uzun", "katta", "keng"),
]


YUQORI += [
    _q("«Ali keldi va Vali ketdi.» gapi qaysi turga kiradi?", "Bogʻlangan qoʻshma gap",
       "Ergash gapli qoʻshma gap", "Sodda yigʻiq gap", "Sodda yoyiq gap"),
    _q("«Agar yomgʻir yogʻsa, biz bormaymiz.» gapida ergash gap qaysi turga kiradi?", "Shart ergash gap",
       "Sabab ergash gap", "Maqsad ergash gap", "Payt ergash gap"),
    _q("«Kitob oʻqigan odam donishmand boʻladi.» gapida «kitob oʻqigan» qanday birikma?", "Sifatdosh oboroti",
       "Ravishdosh oboroti", "Harakat nomi oboroti", "Undalma"),
    _q("Rasmiy uslub qayerda qoʻllanadi?", "Ish qogʻozlari va hujjatlarda", "Doʻstlar suhbatida",
       "Sheʼriy asarlarda", "Oilaviy suhbatda"),
    _q("Quyidagilardan qaysi birida «yurak» soʻzi koʻchma maʼnoda ishlatilgan?", "U juda yuragi keng odam.",
       "Uning yuragi tez urayapti.", "Yurak qonni haydaydi.", "Yurak koʻkrak qafasida joylashgan."),
    _q("Omonim juftligini toping.", "yoz (fasl) — yoz (yozmoq)", "katta — kichik", "chiroyli — goʻzal", "oq — qora"),
    _q("«Bilimli odam kitobsevar boʻladi.» gapi nechta soʻzdan iborat?", "4 ta", "3 ta", "5 ta", "6 ta"),
    _q("«Gulning hidi» birikmasida «gulning» qaysi soʻroqqa javob beradi?", "Kimning? Nimaning?",
       "Kimni? Nimani?", "Kimga? Nimaga?", "Kimdan? Nimadan?"),
    _q("«U kitobni stol ustiga qoʻydi.» gapida «stol ustiga» qaysi gap boʻlagi?", "Oʻrin holi",
       "Toʻldiruvchi", "Aniqlovchi", "Kesim"),
    _q("«Yomgʻir yogʻayotgan edi.» gapidagi kesim qaysi zamonda?", "Oʻtgan zamon", "Hozirgi zamon",
       "Kelasi zamon", "Buyruq mayli"),
    _q("Quyidagilardan qaysi biri soʻz yasovchi qoʻshimcha emas?", "-lar", "-chi", "-kor", "-gar"),
    _q("«Ota-ona» soʻzi qanday soʻz?", "Juft soʻz", "Takroriy soʻz", "Qoʻshma soʻz", "Sodda soʻz"),
]


LEVELS = {
    "d1": {
        "title": "🌱 B — umumiy test",
        "desc": "Alifbo, unli va undosh, boʻgʻin, soʻz turkumlari, tinish belgilari",
        "questions": BOSHLANGICH,
    },
    "d2": {
        "title": "🌿 B+ — umumiy test",
        "desc": "Sinonim-antonim, ega-kesim, kelishiklar, imlo, koʻplik",
        "questions": OZROQ,
    },
    "d3": {
        "title": "🌳 A — umumiy test",
        "desc": "Qoʻshimchalar, zamonlar, soʻz yasalishi, gap boʻlaklari",
        "questions": ORTACHA,
    },
    "d4": {
        "title": "🏆 A+ — umumiy test",
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
    ("d1", "🌱 B darajasi"),
    ("d2", "🌿 B+ darajasi"),
    ("d3", "🌳 A darajasi"),
    ("d4", "🏆 A+ darajasi"),
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
# ---- chuqur (A / A+) savollar
DEEP = {
    "ot": {
        "d3": [
            ("«Kitoblarimizdan» soʻzida nechta qoʻshimcha bor?", "3 ta", "2 ta", "4 ta", "1 ta"),
            ("«Oʻqituvchi» soʻzi qanday yoʻl bilan yasalgan?", "Qoʻshimcha qoʻshish orqali",
             "Soʻzlarni qoʻshish orqali", "Soʻzni takrorlash orqali", "Soʻzni qisqartirish orqali"),
            ("Quyidagilardan qaysi birida egalik qoʻshimchasi bor?", "kitobing", "kitobda", "kitoblar", "kitobni"),
        ],
        "d4": [
            ("«Bolalarning» soʻzidagi -ning qaysi kelishik qoʻshimchasi?", "Qaratqich kelishigi",
             "Tushum kelishigi", "Joʻnalish kelishigi", "Chiqish kelishigi"),
            ("«Uyimdan» soʻzidagi qoʻshimchalar qaysi tartibda?", "Egalik, keyin kelishik",
             "Kelishik, keyin egalik", "Koʻplik, keyin egalik", "Egalik, keyin koʻplik"),
            ("Quyidagilardan qaysi biri qoʻshma ot?", "boshogʻriq", "daftar", "maktab", "oʻqituvchi"),
            ("«Tinchlik» soʻzi qanday ot?", "Mavhum ot", "Moddiy ot", "Atoqli ot", "Jamlovchi ot"),
        ],
    },
    "sifat": {
        "d3": [
            ("«Qizil» sifati qanday sifat?", "Asliy sifat", "Nisbiy sifat", "Qiyosiy sifat", "Orttirma sifat"),
            ("«Kitobiy» sifati qanday sifat?", "Nisbiy sifat", "Asliy sifat", "Qiyosiy sifat", "Orttirma sifat"),
            ("«Yaxshigina» soʻzidagi -gina qoʻshimchasi nimani bildiradi?", "Kichraytirish-erkalash maʼnosini",
             "Qiyoslashni", "Orttirishni", "Mansublikni"),
        ],
        "d4": [
            ("«Oppoq» soʻzi sifatning qaysi darajasida?", "Orttirma daraja", "Oddiy daraja",
             "Qiyosiy daraja", "Hech qaysi darajada emas"),
            ("«Juda baland» birikmasi sifatning qaysi darajasida?", "Orttirma daraja", "Oddiy daraja",
             "Qiyosiy daraja", "Hech qaysi darajada emas"),
            ("«Qizgʻish» soʻzidagi -gʻish qoʻshimchasi qanday maʼno beradi?", "Belgining kamligini (ozligini)",
             "Belgining koʻpligini", "Belgini qiyoslashni", "Harakat nomini"),
            ("Sifat gapda koʻpincha qaysi gap boʻlagi vazifasida keladi?", "Aniqlovchi", "Ega", "Hol", "Toʻldiruvchi"),
        ],
    },
    "son": {
        "d3": [
            ("«Oʻnlab» soʻzi sonning qaysi turi?", "Chama son", "Sanoq son", "Tartib son", "Kasr son"),
            ("«Ikkovimiz» soʻzi sonning qaysi turi?", "Jamlovchi son", "Dona son", "Chama son", "Tartib son"),
            ("«Uch yarim» soni qaysi turga kiradi?", "Kasr son", "Tartib son", "Dona son", "Jamlovchi son"),
        ],
        "d4": [
            ("«Uchinchi qavat» birikmasida «uchinchi» qaysi gap boʻlagi?", "Aniqlovchi", "Ega", "Kesim", "Hol"),
            ("«Yigirma ikki» soni tuzilishiga koʻra qanday son?", "Qoʻshma son", "Sodda son", "Juft son", "Takroriy son"),
            ("«Yuzlab» soʻzidagi -lab qoʻshimchasi nimani bildiradi?", "Taxminiy miqdorni", "Tartibni",
             "Aniq sonni", "Kasrni"),
        ],
    },
    "olmosh": {
        "d3": [
            ("«Oʻzim» olmoshi qaysi turga kiradi?", "Oʻzlik olmoshi", "Kishilik olmoshi", "Belgilash olmoshi", "Gumon olmoshi"),
            ("«Hech kim» olmoshi qaysi turga kiradi?", "Inkor olmoshi", "Gumon olmoshi", "Soʻroq olmoshi", "Belgilash olmoshi"),
            ("«Har kim» olmoshi qaysi turga kiradi?", "Belgilash olmoshi", "Inkor olmoshi", "Soʻroq olmoshi", "Oʻzlik olmoshi"),
            ("«Kimdir» olmoshi qaysi turga kiradi?", "Gumon olmoshi", "Inkor olmoshi", "Soʻroq olmoshi", "Koʻrsatish olmoshi"),
        ],
        "d4": [
            ("«Bu kitob menga yoqdi.» gapida «bu» qaysi turdagi olmosh?", "Koʻrsatish olmoshi",
             "Kishilik olmoshi", "Soʻroq olmoshi", "Gumon olmoshi"),
            ("«Men seni tanimayman.» gapida «seni» qaysi kelishikda?", "Tushum kelishigi", "Bosh kelishik",
             "Qaratqich kelishigi", "Joʻnalish kelishigi"),
            ("«Mening kitobim» birikmasida «mening» qaysi kelishikda?", "Qaratqich kelishigi", "Tushum kelishigi",
             "Bosh kelishik", "Chiqish kelishigi"),
        ],
    },
    "feil": {
        "d3": [
            ("«Oʻqiyapman» feʼli qaysi zamonda?", "Hozirgi zamon", "Oʻtgan zamon", "Kelasi zamon", "Buyruq mayli"),
            ("«Bor!» shakli qaysi mayl?", "Buyruq mayli", "Shart mayli", "Aniqlik mayli", "Istak mayli"),
            ("«Bersa» shakli qaysi mayl?", "Shart mayli", "Buyruq mayli", "Aniqlik mayli", "Istak mayli"),
        ],
        "d4": [
            ("«Yozdirdi» feʼli qaysi nisbatda?", "Orttirma nisbat", "Majhul nisbat", "Oʻzlik nisbat", "Birgalik nisbat"),
            ("«Yozildi» feʼli qaysi nisbatda?", "Majhul nisbat", "Orttirma nisbat", "Oʻzlik nisbat", "Birgalik nisbat"),
            ("«Yuvindi» feʼli qaysi nisbatda?", "Oʻzlik nisbat", "Majhul nisbat", "Orttirma nisbat", "Birgalik nisbat"),
            ("«Kelishdi» feʼli qaysi nisbatda?", "Birgalik nisbat", "Majhul nisbat", "Orttirma nisbat", "Oʻzlik nisbat"),
        ],
    },
    "ravish": {
        "d3": [
            ("«Oldinga» soʻzi ravishning qaysi turi?", "Oʻrin ravishi", "Payt ravishi", "Tarz ravishi", "Miqdor-daraja ravishi"),
            ("«Juda» soʻzi ravishning qaysi turi?", "Miqdor-daraja ravishi", "Payt ravishi", "Oʻrin ravishi", "Tarz ravishi"),
            ("Quyidagilarning qaysi birida «koʻp» ravish?", "U koʻp oʻqidi.", "Bogʻda koʻp daraxt bor.",
             "Qutida koʻp qalam bor.", "Koʻp kitob oʻqidim."),
        ],
        "d4": [
            ("Quyidagilarning qaysi birida «yaxshi» ravish?", "U yaxshi gapiradi.", "U yaxshi bola.",
             "Yaxshi kitob oldim.", "Bu yaxshi fikr."),
            ("Quyidagilarning qaysi birida «tez» ravish?", "Tez yur.", "Tez poyezd keldi.",
             "U tez yigit.", "Tez mashina oldim."),
            ("Ravish gapda koʻpincha qaysi gap boʻlagi boʻladi?", "Hol", "Ega", "Toʻldiruvchi", "Aniqlovchi"),
        ],
    },
    "komakchi": {
        "d3": [
            ("Chiqish kelishigidagi soʻz bilan ishlatiladigan koʻmakchi qaysi?", "keyin", "uchun", "bilan", "kabi"),
            ("«Kabi» koʻmakchisi nimani bildiradi?", "Oʻxshatish", "Sabab", "Maqsad", "Payt"),
        ],
        "d4": [
            ("Quyidagilarning qaysi birida «bilan» koʻmakchi emas?", "Ota bilan ona keldi.",
             "Men doʻstim bilan keldim.", "U qalam bilan yozdi.", "Biz poyezd bilan bordik."),
            ("«Dars tugagandan keyin uyga bordik.» gapida «keyin» qaysi soʻz turkumi?", "koʻmakchi",
             "ravish", "bogʻlovchi", "yuklama"),
        ],
    },
    "boglovchi": {
        "d3": [
            ("Quyidagilardan qaysi biri ergashtiruvchi bogʻlovchi?", "chunki", "va", "hamda", "lekin"),
            ("«Lekin» qaysi turdagi bogʻlovchi?", "Zidlovchi", "Biriktiruvchi", "Ayiruvchi", "Shart"),
            ("«Yoki» qaysi turdagi bogʻlovchi?", "Ayiruvchi", "Biriktiruvchi", "Zidlovchi", "Sabab"),
        ],
        "d4": [
            ("«Garchi yomgʻir yogʻsa-da, biz bordik.» gapida «garchi» qaysi bogʻlovchi?",
             "Ergashtiruvchi bogʻlovchi", "Biriktiruvchi bogʻlovchi", "Ayiruvchi bogʻlovchi", "Zidlovchi bogʻlovchi"),
            ("Teng bogʻlovchilar nimani bogʻlaydi?", "Teng aloqadagi soʻz va sodda gaplarni",
             "Faqat ergash gapni bosh gapga", "Faqat undovlarni", "Tovushlarni"),
            ("«Ali keldi, lekin Vali kelmadi.» gapida «lekin» qaysi bogʻlovchi?", "Zidlovchi bogʻlovchi",
             "Biriktiruvchi bogʻlovchi", "Ayiruvchi bogʻlovchi", "Sabab bogʻlovchisi"),
        ],
    },
    "yuklama": {
        "d3": [
            ("«Hatto» yuklamasi qaysi turga kiradi?", "Kuchaytirish yuklamasi", "Inkor yuklamasi",
             "Soʻroq yuklamasi", "Cheklash yuklamasi"),
            ("«Emas» soʻzi qaysi yuklama turiga kiradi?", "Inkor yuklamasi", "Kuchaytirish yuklamasi",
             "Soʻroq yuklamasi", "Cheklash yuklamasi"),
        ],
        "d4": [
            ("Yuklamalar gapda qanday vazifa bajaradi?", "Gap boʻlagi boʻlmaydi, qoʻshimcha maʼno beradi",
             "Ega boʻladi", "Kesim boʻladi", "Hol boʻladi"),
            ("«Bilasan-ku.» gapidagi «-ku» yuklamasi nimani bildiradi?", "Taʼkid, eslatish",
             "Inkor", "Maqsad", "Oʻxshatish"),
        ],
    },
    "undov": {
        "d3": [
            ("«Attang» undov soʻzi qaysi hissiyotni bildiradi?", "Afsus", "Quvonch", "Qoʻrquv", "Buyruq"),
            ("«Hoy» undov soʻzi nima uchun ishlatiladi?", "Chaqirish uchun", "Rahmat aytish uchun",
             "Sanash uchun", "Qiyoslash uchun"),
        ],
        "d4": [
            ("«Ey, bola, bu yoqqa kel!» gapida «bola» qaysi gap boʻlagi?", "Undalma", "Ega", "Toʻldiruvchi", "Hol"),
            ("Undov soʻzlar qaysi gaplarda koʻproq ishlatiladi?", "His-hayajonli gaplarda", "Ilmiy taʼriflarda",
             "Rasmiy hujjatlarda", "Sanoq ifodalarida"),
        ],
    },
    "modal": {
        "d3": [
            ("«Ehtimol» modal soʻzi qanday maʼno bildiradi?", "Gumon, taxmin", "Ishonch", "Inkor", "Buyruq"),
            ("«Shubhasiz» modal soʻzi qanday maʼno bildiradi?", "Ishonch", "Gumon, taxmin", "Inkor", "Soʻroq"),
        ],
        "d4": [
            ("Modal soʻzlar gapda qanday vazifa bajaradi?", "Gap boʻlagi boʻlmaydi, kirish soʻz boʻlib keladi",
             "Ega boʻladi", "Kesim boʻladi", "Hol boʻladi"),
            ("«Demak, siz haqsiz.» gapida «demak» nimani bildiradi?", "Xulosani", "Soʻroqni", "Inkorni", "Buyruqni"),
        ],
    },
    "taqlid": {
        "d3": [
            ("«Taq-taq» taqlid soʻzi nimaga taqlid?", "Tovushga", "Holat va koʻrinishga", "Rangga", "Maʼnoga"),
            ("«Yarqir-yurqir» taqlid soʻzi nimaga taqlid?", "Holat va koʻrinishga", "Tovushga", "Hidga", "Maza-ta'mga"),
        ],
        "d4": [
            ("Taqlid soʻzlar gapda koʻpincha qaysi gap boʻlagi vazifasida keladi?", "Hol", "Ega", "Toʻldiruvchi", "Aniqlovchi"),
            ("«Shildir-shildir» taqlid soʻzi nimaga taqlid?", "Suv oqishi tovushiga", "Qush ovoziga", "Yurak urishiga", "Qor yogʻishiga"),
        ],
    },
}


for _k, _d in DEEP.items():
    for _lv, _qs in _d.items():
        EXTRA.setdefault(_k, {}).setdefault(_lv, [])
        EXTRA[_k][_lv] = list(_qs) + EXTRA[_k][_lv]

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

    def f_row(rng, k, near=False, rounds=120):
        lab = LABEL[k]
        cls = STRICT[k]
        if len(cls) < 5:
            return
        negpool = others(k, near)
        for _ in range(rounds):
            good = rng.sample(cls, 3)
            right = ", ".join(e["w"] for e in good)
            wrongs = []
            for _j in range(3):
                two = rng.sample(cls, 2)
                out = rng.choice(negpool)
                row = [two[0]["w"], two[1]["w"], out["w"]]
                rng.shuffle(row)
                wrongs.append(", ".join(row))
            yield make(rng, f"Quyidagi qatorlardan qaysi birida barcha soʻzlar {lab} turkumiga kiradi?",
                       right, wrongs)

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

    def near_labels(rng, k, n=3):
        same = [x for x in TURKUM_KEYS if x != k and GROUP[x] == GROUP[k]]
        rest = [x for x in TURKUM_KEYS if x != k and x not in same]
        rng.shuffle(same); rng.shuffle(rest)
        return [LABEL[x] for x in (same + rest)[:n]]

    def f_context_near(rng, k):
        for e in rng.sample(PLAIN[k], len(PLAIN[k])):
            tok = _find_token(e["ex"], e["w"], k)
            if not tok:
                continue
            yield make(rng, f"«{e['ex']}»\n\nShu gapdagi «{tok}» soʻzi qaysi soʻz turkumiga kiradi?",
                       LABEL[k], near_labels(rng, k))

    def deepen(gen, limit=999):
        n = 0
        for q in gen:
            if q:
                q["deep"] = True
                yield q
                n += 1
                if n >= limit:
                    return

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
            f_not_is(rg, k, False, 80), f_row(rg, k, False, 80)])
        rg = r("d2")
        result[k]["d2"] = collect(rg, [
            f_extra(rg, k, "d2"),
            f_context(rg, k), f_meaning_same(rg, k), f_not_is(rg, k, False, 80), f_row(rg, k, False, 80)])
        rg = r("d3")
        result[k]["d3"] = collect(rg, [
            deepen(f_extra(rg, k, "d3")), deepen(f_context_near(rg, k), 22),
            f_meaning_of(rg, k), f_type(rg, k), f_row(rg, k, False, 120), f_not_is(rg, k, True, 80)])
        rg = r("d4")
        result[k]["d4"] = collect(rg, [
            deepen(f_extra(rg, k, "d4")), deepen(f_context_near(rg, k), 22),
            f_composite(rg, k), f_row(rg, k, True, 160), f_not_is(rg, k, True, 80)])
    meta = {"keys": TURKUM_KEYS, "title": TITLE, "label": LABEL}
    return result, meta


# ================= BOT =================
QUIZ_SIZE = 10  # har urinishda nechta savol
TIME_LIMIT = 30  # har bir savolga soniya

TOKEN = os.getenv("BOT_TOKEN", "").strip()
if ":" not in TOKEN:
    sys.exit("BOT_TOKEN noto'g'ri yoki yo'q. U shunday ko'rinadi: 123456789:AAH...\n"
             "Yozing: export BOT_TOKEN=\"butun_token\"")

URL = f"https://api.telegram.org/bot{TOKEN}/"

# --- Admin va roʻyxatdan oʻtish ---
try:
    ADMIN_ID = int(os.getenv("ADMIN_ID", "0").strip() or 0)
except ValueError:
    sys.exit("ADMIN_ID raqam boʻlishi kerak. Masalan: export ADMIN_ID=123456789")
DATA_DIR = os.path.dirname(os.path.abspath(__file__))
USERS_FILE = os.path.join(DATA_DIR, "users.json")
RESULTS_FILE = os.path.join(DATA_DIR, "natijalar.jsonl")


def load_users():
    try:
        with open(USERS_FILE, encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}


USERS = load_users()   # {"user_id": {"name","phone","username","joined"}}
REG = {}               # {user_id: "name" | "phone"}  — roʻyxatdan oʻtish bosqichi


def save_users():
    tmp = USERS_FILE + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(USERS, f, ensure_ascii=False, indent=1)
    os.replace(tmp, USERS_FILE)


def log_result(rec):
    try:
        with open(RESULTS_FILE, "a", encoding="utf-8") as f:
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")
    except Exception as e:
        print("Natijani saqlab boʻlmadi:", e)


def read_results():
    out = []
    try:
        with open(RESULTS_FILE, encoding="utf-8") as f:
            for line in f:
                try:
                    out.append(json.loads(line))
                except Exception:
                    pass
    except FileNotFoundError:
        pass
    return out
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
B_SKIP = "⏭ Oʻtkazib yuborish"
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
    lines = ["Darajani tanlang (milliy sertifikat darajalari):\n"]
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
    deep = [q for q in pool if q.get("deep")]
    rest = [q for q in pool if not q.get("deep")]
    nd = min(len(deep), QUIZ_SIZE // 2)
    chosen = random.sample(deep, nd) + random.sample(rest, min(QUIZ_SIZE - nd, len(rest)))
    random.shuffle(chosen)
    qs = [fresh(q) for q in chosen]
    STATE[uid] = {"title": title, "qs": qs, "i": 0, "score": 0,
                  "chat_id": chat_id, "poll_id": None}
    LAST[uid] = last
    send(chat_id, f"{title}\n\n{len(qs)} ta savol. Har bir savolga {TIME_LIMIT} soniya beriladi ⏱ "
                  "(vaqt tugasa, savol oʻtkazib yuboriladi). Omad! 🍀", quiz_kb())
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
        open_period=TIME_LIMIT,
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
    report_result(uid, title, score, total)


def who(uid):
    u = USERS.get(str(uid), {})
    name = u.get("name") or str(uid)
    extra = []
    if u.get("username"):
        extra.append("@" + u["username"])
    if u.get("phone"):
        extra.append(u["phone"])
    return name + (" (" + ", ".join(extra) + ")" if extra else "")


def report_result(uid, title, score, total):
    log_result({"t": time.strftime("%Y-%m-%d %H:%M:%S"), "uid": uid,
                "name": USERS.get(str(uid), {}).get("name", ""),
                "test": title, "score": score, "total": total})
    if ADMIN_ID and uid != ADMIN_ID:
        send(ADMIN_ID, f"📊 Yangi natija\n👤 {who(uid)}\n📝 {title}\n✅ {score}/{total}")


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


def handle_poll_closed(poll):
    """Savol vaqti tugadi (javob berilmagan) — keyingisiga oʻtamiz."""
    if not poll.get("is_closed"):
        return
    for uid, st in list(STATE.items()):
        if st.get("poll_id") == poll["id"]:
            q = st["qs"][st["i"]]
            st["i"] += 1
            st["poll_id"] = None
            send(st["chat_id"], "⏰ Vaqt tugadi. Toʻgʻri javob: " + q["o"][q["a"]])
            time.sleep(1)
            send_next(uid)
            return


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


def finish_registration(uid, chat_id):
    REG.pop(uid, None)
    save_users()
    send(chat_id, "✅ Roʻyxatdan oʻtdingiz! Endi testlarni boshlashingiz mumkin.", main_kb())
    if ADMIN_ID:
        send(ADMIN_ID, f"🆕 Yangi foydalanuvchi: {who(uid)}\nJami: {len(USERS)} ta")


def registration(msg, uid, chat_id, text, frm):
    step = REG.get(uid)
    if step == "phone":
        phone = ""
        c = msg.get("contact")
        if c and c.get("user_id") == uid:
            phone = c.get("phone_number", "")
            if phone and not phone.startswith("+"):
                phone = "+" + phone
        elif text != B_SKIP:
            send(chat_id, "Pastdagi «📱 Raqamni yuborish» tugmasini bosing yoki oʻtkazib yuboring.")
            return
        USERS[str(uid)]["phone"] = phone
        finish_registration(uid, chat_id)
        return
    if step == "name" and text and not text.startswith("/"):
        if not (2 <= len(text) <= 60) or not text[0].isalpha():
            send(chat_id, "Iltimos, ism-familiyangizni harflar bilan yozing (masalan: Ali Valiyev).")
            return
        USERS[str(uid)] = {"name": text, "phone": "", "username": frm.get("username", ""),
                           "joined": time.strftime("%Y-%m-%d %H:%M")}
        REG[uid] = "phone"
        send(chat_id, "Telefon raqamingizni yuborasizmi? (ixtiyoriy)",
             {"keyboard": [[{"text": "📱 Raqamni yuborish", "request_contact": True}], [{"text": B_SKIP}]],
              "resize_keyboard": True, "one_time_keyboard": True})
        return
    REG[uid] = "name"
    send(chat_id, "Assalomu alaykum! 👋 Ona tili botiga xush kelibsiz.\n\n"
                  "Boshlashdan oldin roʻyxatdan oʻting.\nIsmingiz va familiyangizni yozing:",
         {"remove_keyboard": True})


def send_chunks(chat_id, head, lines, limit=3800):
    cur = head + "\n\n"
    for ln in lines:
        if len(cur) + len(ln) + 1 > limit:
            send(chat_id, cur)
            cur = ""
        cur += ln + "\n"
    send(chat_id, cur if cur.strip() else head)


def send_document(chat_id, path, filename, caption=""):
    """Faylni Telegramga yuboradi (qoʻshimcha kutubxonasiz)."""
    boundary = "----ona" + str(int(time.time() * 1000))
    with open(path, "rb") as f:
        content = f.read()
    parts = []
    for name, val in (("chat_id", str(chat_id)), ("caption", caption)):
        parts.append(f'--{boundary}\r\nContent-Disposition: form-data; name="{name}"\r\n\r\n{val}\r\n'.encode("utf-8"))
    parts.append((f'--{boundary}\r\nContent-Disposition: form-data; name="document"; filename="{filename}"\r\n'
                  'Content-Type: text/csv\r\n\r\n').encode("utf-8") + content + b"\r\n")
    parts.append(f"--{boundary}--\r\n".encode())
    req = urllib.request.Request(URL + "sendDocument", data=b"".join(parts),
                                 headers={"Content-Type": f"multipart/form-data; boundary={boundary}"})
    try:
        urllib.request.urlopen(req, timeout=60).read()
    except Exception as e:
        print("Fayl yuborib boʻlmadi:", e)
        send(chat_id, "Faylni yuborib boʻlmadi 😔")


def export_csv(res):
    import csv
    path = os.path.join(DATA_DIR, "natijalar.csv")
    with open(path, "w", encoding="utf-8-sig", newline="") as f:
        w = csv.writer(f)
        w.writerow(["Sana", "ID", "Ism", "Username", "Telefon", "Test", "Toʻgʻri", "Jami", "Foiz"])
        for r in res:
            u = USERS.get(str(r["uid"]), {})
            pct = round(r["score"] / r["total"] * 100) if r["total"] else 0
            w.writerow([r["t"], r["uid"], r.get("name", ""), u.get("username", ""), u.get("phone", ""),
                        r["test"], r["score"], r["total"], pct])
    return path


def admin_command(chat_id, text):
    res = read_results()
    cmd = text.split()[0].split("@")[0]
    if cmd == "/stats":
        avg = (sum(r["score"] / r["total"] for r in res if r["total"]) / len(res) * 100) if res else 0
        active = len({r["uid"] for r in res})
        send(chat_id, f"📈 Statistika\n👥 Roʻyxatdan oʻtganlar: {len(USERS)}\n"
                      f"🏃 Test yechganlar: {active}\n📝 Yechilgan testlar: {len(res)}\n"
                      f"🎯 Oʻrtacha natija: {avg:.0f}%")
    elif cmd == "/users":
        lines = [f"{i}. {who(u)} — {d.get('joined', '')}" for i, (u, d) in enumerate(USERS.items(), 1)]
        send_chunks(chat_id, f"👥 Barcha foydalanuvchilar ({len(USERS)}):", lines or ["Hozircha yoʻq"])
    elif cmd == "/natijalar":
        by = {}
        for r in res:
            by.setdefault(str(r["uid"]), []).append(r)
        rows = []
        for u in USERS:
            rs = by.get(u, [])
            if rs:
                avg = sum(x["score"] / x["total"] for x in rs if x["total"]) / len(rs) * 100
                l = rs[-1]
                rows.append((avg, f"{who(u)}\n   {len(rs)} ta test, oʻrtacha {avg:.0f}%\n"
                                  f"   Oxirgi: {l['test']} — {l['score']}/{l['total']}"))
            else:
                rows.append((-1, f"{who(u)}\n   hali test yechmagan"))
        for u, rs in by.items():  # roʻyxatda yoʻq (masalan, admin oʻzi)
            if u not in USERS:
                avg = sum(x["score"] / x["total"] for x in rs if x["total"]) / len(rs) * 100
                rows.append((avg, f"{rs[0].get('name') or u}\n   {len(rs)} ta test, oʻrtacha {avg:.0f}%"))
        rows.sort(key=lambda x: -x[0])
        lines = [f"{i}. {t}" for i, (_, t) in enumerate(rows, 1)]
        send_chunks(chat_id, f"🏆 Barcha ishtirokchilar natijasi ({len(rows)} kishi, yaxshisidan boshlab):",
                    lines or ["Hozircha yoʻq"])
    elif cmd == "/oxirgi":
        lines = [f"{r['t'][5:16]} {r['name'] or r['uid']} — {r['test']}: {r['score']}/{r['total']}"
                 for r in res[-30:]]
        send_chunks(chat_id, "🕒 Oxirgi natijalar:", lines or ["Hozircha yoʻq"])
    elif cmd == "/eksport":
        if not res:
            send(chat_id, "Hozircha natija yoʻq.")
        else:
            send_document(chat_id, export_csv(res), "natijalar.csv",
                          f"Barcha natijalar: {len(res)} ta (Excelda ochiladi)")


A_RES, A_STAT, A_USERS, A_LAST, A_EXP = ("📊 Natijalar", "📈 Statistika", "👥 Foydalanuvchilar",
                                         "🕒 Oxirgi natijalar", "📤 Eksport (CSV)")
ADMIN_MAP = {A_RES: "/natijalar", A_STAT: "/stats", A_USERS: "/users", A_LAST: "/oxirgi", A_EXP: "/eksport"}


def admin_kb():
    return rk([[A_RES, A_STAT], [A_USERS, A_LAST], [A_EXP]])


def admin_entry(chat_id, text):
    """Admin rejimi: faqat natijalar, test va lugʻat yoʻq."""
    cmd = ADMIN_MAP.get(text) or (text.split()[0].split("@")[0] if text.startswith("/") else None)
    if cmd in ADMIN_MAP.values():
        admin_command(chat_id, cmd)
    else:
        send(chat_id, "👑 Admin rejimi — faqat natijalarni koʻrasiz.\n"
                      "Quyidagi tugmalardan birini tanlang 👇", admin_kb())


def handle_message(msg):
    chat_id = msg["chat"]["id"]
    uid = msg.get("from", {}).get("id", chat_id)
    text = (msg.get("text") or "").strip()
    frm = msg.get("from", {})

    if text.startswith("/id"):
        send(chat_id, f"Sizning Telegram ID raqamingiz: {uid}")
        return
    if uid == ADMIN_ID:
        admin_entry(chat_id, text)
        return
    if uid != ADMIN_ID and (str(uid) not in USERS or uid in REG):
        registration(msg, uid, chat_id, text, frm)
        return
    if not text:
        return

    # --- Asosiy menyu
    if text.startswith("/start"):
        STATE.pop(uid, None)
        send(chat_id,
             "Assalomu alaykum! 👋\n\n"
             "Men ona tilini 0 dan oʻrganishda yordam beraman:\n"
             f"📝 Quiz-testlar ({total_questions()} ta savol): har bir soʻz turkumi uchun B, B+, A, A+ darajalarida\n"
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
                      "uchun B, B+, A, A+ darajalarida 50 tadan savol; har safar 10 tasi tasodifiy beriladi. Har bir savolga 30 soniya beriladi.\n"
                      "📊 Umumiy testlar — butun ona tili boʻyicha B, B+, A, A+ darajalari.", tests_kb())
    elif text == B_GEN:
        STATE.pop(uid, None)
        send(chat_id, levels_text(), levels_kb())
    elif text == B_TUR:
        STATE.pop(uid, None)
        send(chat_id, "Soʻz turkumini tanlang 👇", tur_kb())
    elif text in TUR_BTN:
        STATE.pop(uid, None)
        PICK[uid] = TUR_BTN[text]
        send(chat_id, f"{TUR_META['title'][PICK[uid]]}\n\nDarajani tanlang 👇 (B, B+, A, A+)\n"
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
             f"📝 Testlar: jami {total_questions()} ta savol (12 soʻz turkumi × B, B+, A, A+ × 50 + umumiy)\n"
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
    elif "poll" in update:
        handle_poll_closed(update["poll"])


def main():
    try:
        me = api("getMe")
    except urllib.error.HTTPError as e:
        if e.code in (401, 404):
            sys.exit("Token notoʻgʻri. BotFatherdan BUTUN tokenni nusxalang.")
        raise
    print("Bot ishga tushdi: @" + me["result"]["username"])
    print("Admin ID:", ADMIN_ID or "BELGILANMAGAN (export ADMIN_ID=... qiling)", "| roʻyxatdagilar:", len(USERS))
    print(f"Ona tili boti | savollar: {total_questions()}, lugʻat: {len(WORDS)} ta soʻz")
    offset = None
    while True:
        try:
            params = {"timeout": 30, "allowed_updates": ["message", "poll_answer", "poll"]}
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
