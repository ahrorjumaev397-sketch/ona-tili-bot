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
    _q("«Yoz» (fasl) va «yoz» (yozmoq) soʻzlari qanday soʻzlar?", "Omonim", "Sinonim", "Antonim", "Paronim"),
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
    ("omonim", "Shakli bir xil, lekin maʼnosi har xil soʻzlar.", "Yoz (fasl) va yoz (yozmoq)."),
    ("paronim", "Aytilishi oʻxshash, lekin maʼnosi har xil soʻzlar.", "Tavsiya va tavsif."),
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
    ("ota", "Farzandi bor erkak; oilaning erkak ota-onasi.", "Otam dalada ishlaydi."),
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
    ("oʻnlab", "Taxminiy son: oʻn va undan ortiq, aniq boʻlmagan miqdor.", "Oʻnlab odam keldi."),
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
    ("tez", "Tarz: tezlik bilan.", "U tez yugurdi."),
    ("sekin", "Tarz: oʻrtacha tezlikdan past.", "Mashina sekin yurdi."),
    ("asta", "Tarz: shoshmasdan, yumshoq.", "Asta gapiring."),
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

OT_NEW = [
    ("aka", "Oʻzidan katta erkak qarindosh yoki katta yoshdagi erkakka hurmat bilan aytiladigan soʻz.", "Mening akam shifokor, aka juda mehribon."),
    ("uka", "Oʻzidan kichik erkak qarindosh.", "Uka akasining ortidan ergashdi."),
    ("opa", "Oʻzidan katta ayol qarindosh.", "Opa menga dars tayyorlashda yordam berdi."),
    ("singil", "Oʻzidan kichik ayol qarindosh.", "Singil bogʻda gul terdi."),
    ("buva", "Otaning yoki onaning otasi.", "Buva nevaralariga ertak aytib berdi."),
    ("buvi", "Otaning yoki onaning onasi.", "Buvi non yopdi."),
    ("amaki", "Otaning ukasi yoki akasi.", "Amaki mehmonga keldi."),
    ("togʻa", "Onaning akasi yoki ukasi.", "Togʻa bizga sovgʻa olib keldi."),
    ("qoʻshni", "Yonma-yon turar joyda yashovchi kishi.", "Qoʻshni bizga yordam berdi."),
    ("mehmon", "Uyga taklif bilan yoki tasodifan kelgan kishi.", "Mehmon eshikdan kirdi."),
    ("odam", "Aql va nutqqa ega jonzot, inson.", "Bu odam juda xushmuomala."),
    ("qiz", "Ayol jinsidagi yosh inson.", "Qiz kitob oʻqiyapti."),
    ("yigit", "Voyaga yetgan yosh erkak.", "Yigit ishga ketdi."),
    ("kampir", "Keksa ayol.", "Kampir ertak aytdi."),
    ("chol", "Keksa erkak.", "Chol hovlida oʻtirardi."),
    ("muallim", "Taʼlim beruvchi kasb egasi, oʻqituvchi.", "Muallim sinfga kirdi."),
    ("shogird", "Ustozdan hunar yoki ilm oʻrganuvchi kishi.", "Shogird ustoziga hurmat koʻrsatdi."),
    ("haydovchi", "Transport vositasini boshqaruvchi kishi.", "Haydovchi mashinani toʻxtatdi."),
    ("quruvchi", "Bino va inshootlar quruvchi kasb egasi.", "Quruvchi uy qurmoqda."),
    ("oshpaz", "Ovqat tayyorlovchi kasb egasi.", "Oshpaz mazali osh pishirdi."),
    ("novvoy", "Non yopuvchi kasb egasi.", "Novvoy tandirdan non uzdi."),
    ("temirchi", "Temirdan buyum yasovchi usta.", "Temirchi bolgʻa bilan temirni urdi."),
    ("hamshira", "Shifokorga yordam beruvchi, bemorlarga qarovchi tibbiyot xodimi.", "Hamshira bemorga dori berdi."),
    ("muhandis", "Texnika va qurilish ishlarini loyihalovchi mutaxassis.", "Muhandis loyihani tekshirdi."),
    ("yozuvchi", "Badiiy asarlar yaratuvchi shaxs.", "Yozuvchi yangi roman yozdi."),
    ("shoir", "Sheʼr yozuvchi ijodkor.", "Shoir vatan haqida sheʼr yozdi."),
    ("rassom", "Rasm chizuvchi ijodkor.", "Rassom tabiat manzarasini chizdi."),
    ("askar", "Harbiy xizmatchi.", "Askar Vatanni qoʻriqladi."),
    ("savdogar", "Savdo-sotiq bilan shugʻullanuvchi kishi.", "Savdogar bozorga mol olib keldi."),
    ("bogʻbon", "Bogʻda daraxt va gullarni parvarish qiluvchi kishi.", "Bogʻbon daraxtlarni sugʻordi."),
    ("chorvador", "Chorva mollarini boqib parvarish qiluvchi kishi.", "Chorvador qoʻylarni yaylovga haydadi."),
    ("paxtakor", "Paxta yetishtiruvchi dehqon.", "Paxtakor dalada ishladi."),
    ("jamoa", "Birgalikda ish bajaruvchi yoki oʻynovchi kishilar guruhi.", "Jamoa gʻalaba qozondi."),
    ("sinf", "Bir xil bosqichda taʼlim oluvchi oʻquvchilar guruhi yoki ularning xonasi.", "Sinf toza va yorugʻ edi."),
    ("dars", "Oʻqituvchi tomonidan oʻtiladigan mashgʻulot.", "Dars soat sakkizda boshlandi."),
    ("imtihon", "Bilimni sinash maqsadida oʻtkaziladigan tekshiruv.", "Imtihon muvaffaqiyatli oʻtdi."),
    ("baho", "Bilim yoki ish natijasiga berilgan qiymat.", "Oʻquvchi aʼlo baho oldi."),
    ("darslik", "Oʻquv fani boʻyicha asosiy kitob.", "Darslik sumkamda turibdi."),
    ("sumka", "Narsalarni solib olib yurish uchun buyum.", "Sumka kitobga toʻla edi."),
    ("ruchka", "Siyoh bilan yozish uchun asbob.", "Ruchka yozmay qoldi."),
    ("oʻchirgʻich", "Yozilgan yoki chizilgan narsani oʻchirish uchun buyum.", "Oʻchirgʻich stol ustida yotibdi."),
    ("lugʻat", "Soʻzlar va ularning izohi jamlangan kitob.", "Lugʻat yangi soʻzlarni oʻrganishga yordam beradi."),
    ("xat", "Qogʻozga yozilgan murojaat yoki yozishma.", "Xat ertalab yetib keldi."),
    ("gazeta", "Yangiliklar bosiladigan nashr.", "Gazeta har kuni chiqadi."),
    ("jurnal", "Davriy nashr, maqola va rasmlar toʻplami.", "Jurnal yangi sonini chiqardi."),
    ("telefon", "Masofadan gaplashish uchun qurilma.", "Telefon jiringladi."),
    ("kompyuter", "Maʼlumotlarni qayta ishlovchi elektron qurilma.", "Kompyuter stolda turibdi."),
    ("soat", "Vaqtni koʻrsatuvchi asbob; vaqt oʻlchovi.", "Soat toʻqqizni koʻrsatdi."),
    ("oyna", "Shaffof shishadan yasalgan yuza.", "Oyna tiniq edi."),
    ("kalit", "Qulfni ochish va yopish uchun buyum.", "Kalit choʻntakda edi."),
    ("qulf", "Eshik yoki sandiqni berkitish uchun moslama.", "Qulf zang bosib ketgan."),
    ("devor", "Bino yoki hovlini toʻsib turuvchi tik inshoot.", "Devor boʻyalgan edi."),
    ("tom", "Binoning yuqori yopilgan qismi.", "Tom qor bilan qoplandi."),
    ("hovli", "Uy atrofidagi toʻsilgan ochiq maydon.", "Hovli supurilgan edi."),
    ("koʻcha", "Shahar yoki qishloqdagi yoʻl.", "Koʻcha odamlarga toʻla."),
    ("koʻprik", "Daryo yoki jarlikdan oʻtish uchun qurilgan inshoot.", "Koʻprik daryo ustidan oʻtadi."),
    ("bekat", "Transport toʻxtaydigan joy.", "Bekat maktab yonida."),
    ("poyezd", "Temir yoʻldan yuruvchi transport.", "Poyezd vaqtida keldi."),
    ("samolyot", "Havoda uchuvchi transport vositasi.", "Samolyot osmonga koʻtarildi."),
    ("velosiped", "Oyoq bilan pedal bosib yuriladigan ikki gʻildirakli transport.", "Velosiped bogʻ yoʻlidan oʻtdi."),
    ("avtobus", "Koʻp yoʻlovchi tashiydigan transport vositasi.", "Avtobus bekatga keldi."),
    ("doʻkon", "Mahsulot sotiladigan joy.", "Doʻkon ertalab ochiladi."),
    ("dorixona", "Dori-darmon sotiladigan joy.", "Dorixona yaqin joyda."),
    ("kasalxona", "Kasallar davolanadigan muassasa.", "Kasalxona shahar markazida."),
    ("stadion", "Sport musobaqalari oʻtkaziladigan maydon.", "Stadion tomoshabinlarga toʻla edi."),
    ("muzey", "Tarixiy va nodir buyumlar saqlanadigan va koʻrsatiladigan joy.", "Muzey juda boy ekspozitsiyaga ega."),
    ("teatr", "Sahna asarlari koʻrsatiladigan joy.", "Teatr kechqurun ochiladi."),
    ("paxta", "Tolasidan mato ishlanadigan oʻsimlik.", "Paxta oq oltin deyiladi."),
    ("bugʻdoy", "Undan non uni olinadigan boshoqli oʻsimlik.", "Bugʻdoy pishdi."),
    ("guruch", "Palov va boshqa ovqatlar pishiriladigan don.", "Guruch yuvildi."),
    ("un", "Donni tuyib olinadigan kukun.", "Un elandi."),
    ("sut", "Sigir, echki kabi hayvonlardan olinadigan oq ichimlik.", "Sut yangi edi."),
    ("goʻsht", "Hayvon tanasining yeyiladigan qismi.", "Goʻsht pishib qoldi."),
    ("tuxum", "Qush yoki hasharot qoʻygan, ichidan bola chiqadigan urugʻ.", "Tuxum qaynatildi."),
    ("tuz", "Ovqatga solinadigan shoʻr kristall.", "Tuz kam ekan."),
    ("shakar", "Shirin taʼm beruvchi oq kristall modda.", "Shakar choyga solindi."),
    ("choy", "Barglaridan damlanadigan ichimlik.", "Choy issiq edi."),
    ("palov", "Guruch, goʻsht va sabzidan pishiriladigan milliy taom.", "Palov dasturxonga tortildi."),
    ("shoʻrva", "Goʻsht va sabzavotdan qaynatilgan suyuq taom.", "Shoʻrva issiq edi."),
    ("meva", "Daraxt yoki oʻsimlikda pishadigan yeyiladigan qism.", "Meva pishib yetildi."),
    ("sabzavot", "Dalada yetishtiriladigan yeyiladigan oʻsimlik.", "Sabzavot bozorda arzon."),
    ("uzum", "Tok mevasi, shirin va sersuv.", "Uzum pishdi."),
    ("anor", "Doʻlsimon qizil donali meva.", "Anor shirin ekan."),
    ("sabzi", "Sariq-qizil ildizmeva.", "Sabzi toʻgʻraldi."),
    ("piyoz", "Qatlamli, oʻtkir hidli sabzavot.", "Piyoz aʼlo sifatli edi."),
    ("kartoshka", "Ildizpoyasidan oziq-ovqat sifatida foydalaniladigan oʻsimlik.", "Kartoshka qovurildi."),
    ("pomidor", "Qizil, sersuv sabzavot.", "Pomidor pishgan edi."),
    ("buzoq", "Sigirning bolasi.", "Buzoq oʻtlab yurdi."),
    ("qoʻy", "Juni va goʻshti uchun boqiladigan uy hayvoni.", "Qoʻy yaylovda oʻtlayapti."),
    ("sigir", "Sut beradigan uy hayvoni.", "Sigir sut berdi."),
    ("mushuk", "Sichqon tutadigan, mayin juni bor uy hayvoni.", "Mushuk derazada yotibdi."),
    ("it", "Uyni qoʻriqlaydigan sodiq uy hayvoni.", "It darvoza oldida yotardi."),
    ("baliq", "Suvda yashaydigan, qanoti va tangachasi bor jonzot.", "Baliq suvda suzdi."),
    ("kapalak", "Rangdor qanotli hasharot.", "Kapalak gulga qoʻndi."),
    ("asalari", "Asal yigʻuvchi hasharot.", "Asalari gulda uchib yurdi."),
    ("chumoli", "Mehnatsevarligi bilan mashhur mayda hasharot.", "Chumoli donni uyasiga olib ketdi."),
    ("burgut", "Kuchli, yirik yirtqich qush.", "Burgut baland uchdi."),
    ("bulbul", "Chiroyli sayraydigan qush.", "Bulbul bogʻda sayradi."),
    ("kaptar", "Tinchlik ramzi hisoblangan qush.", "Kaptar tomga qoʻndi."),
    ("bulut", "Osmonda suv bugʻidan hosil boʻlgan quyuq parcha.", "Bulut quyoshni toʻsdi."),
    ("chaqmoq", "Osmondagi elektr razryadi tufayli paydo boʻladigan yorugʻlik.", "Chaqmoq yaltirab oʻtdi."),
    ("daryocha", "Kichik daryo.", "Daryocha boʻylab yurdik."),
    ("koʻl", "Quruqlik bilan oʻralgan katta suv havzasi.", "Koʻl tiniq edi."),
    ("jilgʻa", "Togʻdan oqib tushadigan kichik suv oqimi.", "Jilgʻa shildirab oqdi."),
    ("choʻl", "Suvi kam, qumloq keng yer.", "Choʻl jaziramada qizidi."),
    ("oʻrmon", "Daraxtlar koʻp oʻsadigan katta yer.", "Oʻrmon sokin edi."),
    ("vodiy", "Togʻlar orasidagi keng pasttekislik.", "Vodiy yashil libosga burkandi."),
    ("yaylov", "Chorva mollari oʻtlaydigan yer.", "Yaylov yam-yashil edi."),
]

SIFAT_NEW = [
    ("goʻzal", "Husni-jamoli yoqimli, ajoyib koʻrinishli.", "Goʻzal bogʻ koʻz oldimizda yastandi."),
    ("xunuk", "Koʻrinishi yoqimsiz, xushsiz.", "Xunuk hid anqidi."),
    ("ulkan", "Juda katta, ulugʻvor.", "Ulkan togʻ osmonga bosh urdi."),
    ("mayda", "Hajmi juda kichik.", "Mayda toshlar yoʻlga toʻshaldi."),
    ("yirik", "Hajmi katta, ulgʻaygan.", "Yirik olma savatga solindi."),
    ("keksa", "Yoshi ulgʻaygan, yoshi katta.", "Keksa dehqon dalaga chiqdi."),
    ("navqiron", "Yosh, kuch-quvvatga toʻlgan.", "Navqiron yigit sportni yaxshi koʻradi."),
    ("semiz", "Tanasi yogʻ bosgan, toʻladan kelgan.", "Semiz qoʻy boqildi."),
    ("ozgʻin", "Tanasi ingichka, oriq.", "Ozgʻin bola tez yugurdi."),
    ("baquvvat", "Kuchli, jismonan baquvvat.", "Baquvvat yigit yukni koʻtardi."),
    ("zaif", "Kuchi kam, nimjon.", "Zaif shamol yengil esdi."),
    ("charchagan", "Holdan toygan, toliqqan.", "Charchagan sayyoh dam oldi."),
    ("sogʻlom", "Kasalligi yoʻq, tani-joni baquvvat.", "Sogʻlom bola quvnoq oʻynadi."),
    ("kasal", "Salomatligi buzilgan, betob.", "Kasal bola yotib dam oldi."),
    ("toʻq", "Qorni ochmagan; rangi quyuq.", "Toʻq qizil gul koʻzga tashlandi."),
    ("och", "Qorni ochgan; rangi yorqin emas.", "Och bola non soʻradi."),
    ("quruq", "Namligi yoʻq, hoʻl emas.", "Quruq barg shitirladi."),
    ("nam", "Ozgina suv shimgan, hoʻl.", "Nam yerda oʻt unib chiqdi."),
    ("yumaloq", "Shakli doira yoki shar kabi.", "Yumaloq olma yerga tushdi."),
    ("kvadrat", "Toʻrt tomoni teng, toʻgʻri burchakli.", "Kvadrat stol xonaning oʻrtasida turardi."),
    ("tekis", "Notekisligi yoʻq, silliq.", "Tekis yoʻl uzoqqa choʻzildi."),
    ("silliq", "Yuzasi tekis, gʻadir-budir emas.", "Silliq tosh qirgʻoqda yotardi."),
    ("pandir", "", ""),
    ("notekis", "Yuzasi yoki shakli tekis boʻlmagan.", "Notekis yoʻl mashinani silkitdi."),
    ("chuqur", "Pastga yoki ichkariga ancha oʻyilgan.", "Chuqur quduq qazildi."),
    ("sayoz", "Chuqurligi kam.", "Sayoz ariqdan oʻtdik."),
    ("keng", "", ""),
    ("ingichka", "Yoʻgʻonligi kam, ozgʻin.", "Ingichka ip uzildi."),
    ("yoʻgʻon", "Yoʻgʻonligi katta, qalin.", "Yoʻgʻon daraxt tanasi qulab tushdi."),
    ("qalin", "Qatlami yoki qalinligi katta.", "Qalin kitob javonda turardi."),
    ("yupqa", "Qalinligi kam, nozik.", "Yupqa non pishirildi."),
    ("ogʻir-vazmin", "", ""),
    ("sokin", "Tinch, shovqinsiz.", "Sokin kecha hammani uyquga chorladi."),
    ("shovqinli", "Shovqin-suroni koʻp.", "Shovqinli koʻchadan chetlandik."),
    ("yorugʻ", "Nuri koʻp, ravshan.", "Yorugʻ xonada kitob oʻqidik."),
    ("qorongʻi", "Nur yoʻq, zulmat.", "Qorongʻi tunda yulduzlar yaqqol koʻrindi."),
    ("iliq", "Harorati meʼyorida, issiq ham, sovuq ham emas.", "Iliq suvda choʻmildik."),
    ("salqin", "Biroz sovuq, orom beruvchi.", "Salqin shabada esdi."),
    ("qaynoq", "Juda issiq, qaynagan.", "Qaynoq choy ichdik."),
    ("muzdek", "Juda sovuq, muz kabi.", "Muzdek suv ichdim."),
    ("shoʻr", "Tuz kabi mazali.", "Shoʻr osh ichishga qiyin edi."),
    ("totli", "Mazasi yoqimli, shirin.", "Totli taom dasturxonni bezadi."),
    ("mazali", "Taʼmi yaxshi, yoqimli.", "Mazali palov pishirildi."),
    ("xushboʻy", "Hidi yoqimli.", "Xushboʻy gul hidladim."),
    ("badbo'y", "", ""),
    ("pushti", "Och qizil rang tusidagi.", "Pushti gul ochildi."),
    ("binafsha", "Ko'k va qizil oralig'idagi rang tusidagi.", ""),
    ("jigarrang", "Jigar rangidagi, qoʻngʻir.", "Jigarrang ot yoʻlda yurdi."),
    ("kulrang", "Kul rangidagi, och qora.", "Kulrang bulut osmonni qopladi."),
    ("moviy", "Och koʻk rangdagi.", "Moviy osmon musaffo edi."),
    ("zarrin", "Oltin rangli, oltindek yaltiragan.", "Zarrin barglar toʻkildi."),
    ("kumush", "", ""),
    ("jonli", "Harakatchan, tirik-tirik.", "Jonli suhbat davom etdi."),
    ("jasur", "Qoʻrqmas, dadil.", "Jasur askar xavfdan qaytmadi."),
    ("qoʻrqoq", "Tezda qoʻrqadigan, dovyuraklik yoʻq.", "Qoʻrqoq bola orqaga tisarildi."),
    ("dovyurak", "Qoʻrqmaydigan, bahodir.", "Dovyurak oʻgʻlon yordamga shoshildi."),
    ("ochiqkoʻngil", "Samimiy, dilidagini yashirmaydigan.", "Ochiqkoʻngil kishi hammaga yoqadi."),
    ("kamtar", "Oʻzini yuqori tutmaydigan, ortiqcha maqtanmaydigan.", "Kamtar inson hurmatga sazovor."),
    ("maqtanchoq", "Oʻzini maqtashni yaxshi koʻradigan.", "Maqtanchoq bola hammaga oʻz yutugʻini aytdi."),
    ("ochkoʻz", "Haddan ziyod tamagir, hirsli.", "Ochkoʻz savdogar narxni oshirdi."),
    ("saxiy", "Qoʻli ochiq, berishdan toʻrmaydigan.", "Saxiy odam mehmonlarni kutib oldi."),
    ("xasis", "Pul yoki mol berishni istamaydigan, qizgʻanchiq.", "Xasis kishi hech kimga yordam bermadi."),
    ("odobli", "Axloq-odobi yaxshi, xushmuomala.", "Odobli bola kattalarga salom berdi."),
    ("befarq", "Hech narsaga qiziqmaydigan, loqayd.", "Befarq kishi eshitmadi."),
    ("tirishqoq", "Mehnatda qunt va gʻayrat koʻrsatadigan.", "Tirishqoq oʻquvchi darslarini oʻz vaqtida tayyorladi."),
    ("dangasa", "Mehnat qilishni yoqtirmaydigan, ishyoqmas.", "Dangasa bola yotib oldi."),
    ("aqlli", "Zehni oʻtkir, fikrlash qobiliyati yuqori.", "Aqlli bola masalani tez yechdi."),
    ("zehnli", "Zehni oʻtkir, tez tushunadigan.", "Zehnli shogird ustozini mamnun qildi."),
    ("nodon", "Bilimsiz, oʻqimagan.", "Nodon kishi xato qildi."),
    ("tajribali", "Koʻp ishni boshidan kechirgan, mahoratli.", "Tajribali usta ishni tez bitirdi."),
    ("mohir", "Ishning pishiq-puxta ustasi.", "Mohir hunarmand koʻp asar yaratdi."),
    ("foydali", "Naf keltiradigan, manfaatli.", "Foydali maslahat berdi."),
    ("zararli", "Ziyon keltiradigan, foydasiz.", "Zararli odat sogʻliqqa ziyon."),
    ("qimmat", "Narxi baland, arzon emas.", "Qimmat kitob doʻkon peshtaxtasida turardi."),
    ("arzon", "Narxi past, qimmat emas.", "Arzon olma bozorda sotildi."),
    ("muhim", "Ahamiyati katta, zarur.", "Muhim uchrashuv ertaga boʻladi."),
    ("oddiy", "Sodda, maxsus xususiyati yoʻq.", "Oddiy savol berdi."),
    ("murakkab", "Tuzilishi yoki mazmuni qiyin, chigal.", "Murakkab masala yechildi."),
    ("oson", "Qiyinchiligi yoʻq, yengil.", "Oson topshiriq bajarildi."),
    ("qiyin", "Bajarilishi mashaqqatli.", "Qiyin yoʻl bosib oʻtdik."),
    ("toʻgʻri", "Egri emas; rost, xato emas.", "Toʻgʻri yoʻl topildi."),
    ("egri", "Toʻgʻri emas, qiyshiq.", "Egri novda sindi."),
    ("haqiqiy", "Soxta emas, chin.", "Haqiqiy oltin yaltirardi."),
    ("soxta", "Asl emas, yasama.", "Soxta pul topildi."),
    ("ajoyib", "Hayratga soladigan darajada yaxshi.", "Ajoyib manzara koʻz oldimizda namoyon boʻldi."),
    ("mashhur", "Hammaga taniqli, nomi chiqqan.", "Mashhur shoir xalq orasida hurmatga ega."),
    ("noyob", "Kam uchraydigan, tengi yoʻq.", "Noyob qoʻlyozma muzeyda saqlanadi."),
    ("qadimiy", "Juda qadim zamonlarga oid.", "Qadimiy shahar harobalari topildi."),
    ("zamonaviy", "Hozirgi zamonga mos, yangi.", "Zamonaviy bino qurildi."),
    ("milliy", "Xalq yoki millatga xos.", "Milliy libos kiydik."),
    ("ilmiy", "Fanga oid, ilmga asoslangan.", "Ilmiy maqola chop etildi."),
    ("badiiy", "", ""),
]
SIFAT_NEW = [x for x in SIFAT_NEW if x[1] and x[2]]

FEIL_NEW = [
    ("koʻtarmoq", "Pastdagi narsani yuqoriga olmoq.", "Yigit ogʻir yukni koʻtardi."),
    ("tushmoq", "Yuqoridan pastga qarab harakatlanmoq.", "Yomgʻir tomchilari tushdi."),
    ("chiqmoq", "Ichkaridan tashqariga yoʻnalmoq.", "Quyosh sharqdan chiqdi."),
    ("kirmoq", "Tashqaridan ichkariga yoʻnalmoq.", "Mehmon uyga kirdi."),
    ("qaytmoq", "Ketgan joyidan orqaga burilmoq.", "Ota ishdan qaytdi."),
    ("yetmoq", "Biror joyga yoki maqsadga erishmoq.", "Poyezd manzilga yetdi."),
    ("toʻxtamoq", "Harakatdan tinmoq, qolmoq.", "Mashina chorrahada toʻxtadi."),
    ("chaqirmoq", "Birovni oʻz oldiga kelishga undamoq.", "Oʻqituvchi oʻquvchini chaqirdi."),
    ("tushunmoq", "Mazmun va mohiyatni anglab yetmoq.", "Men qoidani tushundim."),
    ("eslamoq", "Esga olmoq, yodga keltirmoq.", "U bolalik kunlarini esladi."),
    ("unutmoq", "Yodidan chiqarmoq.", "Men soʻzni unutdim."),
    ("xohlamoq", "Biror narsani istamoq.", "U sayohatga chiqishni xohladi."),
    ("yoqtirmoq", "Biror narsani yaxshi koʻrmoq.", "Bola mevani yoqtirdi."),
    ("kuzatmoq", "Diqqat bilan qarab turmoq.", "Talaba tajribani kuzatdi."),
    ("tinglamoq", "Diqqat bilan eshitmoq.", "Biz ustozni tingladik."),
    ("yasamoq", "Biror narsani tayyorlab chiqarmoq.", "Usta stol yasadi."),
    ("tikmoq", "Ignaga ip solib toʻqimoq yoki birlashtirmoq.", "Onam koʻylak tikdi."),
    ("yirtmoq", "Qogʻoz yoki matoni boʻlaklarga ajratmoq.", "Bola qogʻozni yirtdi."),
    ("sindirmoq", "Qattiq narsani boʻlaklarga ajratmoq.", "U stakanni sindirdi."),
    ("tozalamoq", "Kir va chiqindidan xoli qilmoq.", "Biz sinfni tozaladik."),
    ("supurmoq", "Supurgi bilan changni yigʻmoq.", "Hovlini supurdim."),
    ("sugʻormoq", "Yerga yoki oʻsimlikka suv bermoq.", "Bogʻbon daraxtlarni sugʻordi."),
    ("haydamoq", "Hayvon yoki transportni harakatlantirmoq.", "Chorvador qoʻylarni haydadi."),
    ("boqmoq", "Hayvon yoki bolaga oziq berib parvarish qilmoq.", "U sigirni boqdi."),
    ("tortmoq", "Oʻzi tomonga yoki oʻz ketidan sudramoq.", "Ular arqonni tortdi."),
    ("itarmoq", "Kuch bilan oldinga surmoq.", "Yigitlar mashinani itardi."),
    ("tashimoq", "Yukni bir joydan boshqa joyga olib bormoq.", "Haydovchi yuk tashidi."),
    ("yigʻmoq", "Narsalarni bir joyga toʻplamoq.", "Dehqon hosilni yigʻdi."),
    ("toʻldirmoq", "Boʻsh joyni biror narsa bilan egallamoq.", "Ona stakanni suv bilan toʻldirdi."),
    ("qaynamoq", "Suyuqlik qizib, pufak hosil qilmoq.", "Choynak qaynadi."),
    ("qovurmoq", "Yogʻda pishirmoq.", "Onam kartoshka qovurdi."),
    ("tashlamoq", "Qoʻldagi narsani qoʻyib yubormoq yoki otmoq.", "U toshni suvga tashladi."),
    ("tutmoq", "Qoʻl bilan ushlamoq.", "Bola kapalakni tutdi."),
    ("saqlamoq", "Narsani yoʻqotmay asramoq.", "U kitoblarni javonda saqladi."),
    ("qoʻriqlamoq", "Biror joy yoki narsani himoya qilib turmoq.", "Askar chegarani qoʻriqladi."),
    ("yutmoq", "Gʻalaba qozonmoq; ovqatni halqumdan oʻtkazmoq.", "Jamoamiz musobaqada yutdi."),
    ("hisoblamoq", "Sonlarni sanab natija chiqarmoq.", "Oʻquvchi misolni hisobladi."),
    ("oʻlchamoq", "Uzunlik, vazn kabi miqdorni aniqlamoq.", "Usta gazni oʻlchadi."),
    ("tayyorlamoq", "Biror ish uchun hozirlamoq.", "U ertangi darsni tayyorladi."),
    ("bajarmoq", "Topshiriq yoki ishni amalga oshirmoq.", "Oʻquvchi vazifani bajardi."),
    ("kechikmoq", "Belgilangan vaqtdan keyin kelmoq.", "Avtobus kechikdi."),
    ("shoshilmoq", "Tez harakat qilmoq, ulgurishga intilmoq.", "Odamlar ishga shoshildi."),
    ("charchamoq", "Holdan toymoq.", "Yoʻlovchi charchadi."),
    ("kuylamoq", "Ohang bilan ashula aytmoq.", "Xonanda yoqimli kuyladi."),
    ("chalmoq", "Sozni ijro etmoq; urmoq.", "U dutor chaldi."),
    ("oʻynamoq", "Vaqt oʻtkazmoq uchun mashgʻul boʻlmoq.", "Bolalar maydonda oʻynadi."),
    ("sakramoq", "Oyoqlarini yerdan uzib, yuqoriga irgʻimoq.", "Ot toʻsiqdan sakradi."),
    ("emaklamoq", "Qoʻl va tizza ustida yurmoq.", "Chaqaloq emakladi."),
    ("chopmoq", "Oʻtkir narsa bilan boʻlmoq; tez yugurmoq.", "Dehqon oʻtinni chopdi."),
    ("urmoq", "Zarba bermoq.", "Usta bolgʻa bilan mixni urdi."),
    ("silkitmoq", "Tez-tez harakatga keltirmoq.", "Shamol novdani silkitdi."),
    ("esmoq", "Shamol yoki yel harakatlanmoq.", "Shamol sekin esdi."),
    ("porlamoq", "Nur sochmoq, yaltiramoq.", "Quyosh porladi."),
    ("yonmoq", "Olov chiqarib kuymoq.", "Gulxan yondi."),
    ("oʻchmoq", "Olov yoki nur yoʻqolmoq.", "Chiroq oʻchdi."),
    ("erimoq", "Qattiq narsa suyuqlikka aylanmoq.", "Qor eridi."),
    ("muzlamoq", "Suv qotib muzga aylanmoq.", "Koʻl muzladi."),
    ("oʻsmoq", "Ulgʻaymoq, kattalashmoq.", "Daraxt oʻsdi."),
    ("gullamoq", "Gul ochmoq.", "Bogʻ bahorda gulladi."),
    ("soʻlmoq", "Namini yoʻqotib toʻkilmoq, quvvatdan ketmoq.", "Gul soʻldi."),
    ("pishmoq", "Mevaning yetilishi yoki ovqatning tayyor boʻlishi.", "Uzum pishdi."),
    ("tugʻilmoq", "Dunyoga kelmoq.", "U Toshkentda tugʻildi."),
    ("yashamoq", "Hayot kechirmoq.", "Ular qishloqda yashadi."),
    ("oʻzgarmoq", "Boshqacha holga kelmoq.", "Havo oʻzgardi."),
    ("rivojlanmoq", "Oldinga siljib takomillashmoq.", "Shahar tez rivojlandi."),
    ("quvonmoq", "Xursand boʻlmoq.", "Bolalar sovgʻaga quvondi."),
    ("ranjimoq", "Xafa boʻlmoq, ozor chekmoq.", "U gapdan ranjidi."),
    ("qoʻrqmoq", "Xavfdan choʻchimoq.", "Bola qorongʻidan qoʻrqdi."),
    ("ishonmoq", "Biror kishi yoki narsaga ishonch bildirmoq.", "Men doʻstimga ishondim."),
    ("ajablanmoq", "Hayron boʻlmoq.", "Hamma bu xabardan ajablandi."),
    ("achinmoq", "Rahm qilmoq, afsuslanmoq.", "U yiqilgan bolaga achindi."),
    ("kechirmoq", "Aybini yuziga solmay afv etmoq.", "Ustoz xatoni kechirdi."),
    ("tabriklamoq", "Bayram yoki yutuq bilan muborakbod qilmoq.", "Biz doʻstimizni tabrikladik."),
    ("uchrashmoq", "Bir-biri bilan yuzma-yuz kelmoq.", "Doʻstlar bogʻda uchrashdi."),
    ("xayrlashmoq", "Ayrilishda vidolashmoq.", "Ular bekatda xayrlashdi."),
    ("salomlashmoq", "Bir-biri bilan salom bermoq.", "Qoʻshnilar salomlashdi."),
    ("maslahatlashmoq", "Bir-biri bilan fikr almashib kengashmoq.", "Ustoz va shogird maslahatlashdi."),
    ("tinchimoq", "Tinch holga kelmoq.", "Dengiz tinchidi."),
    ("ulgʻaymoq", "Yoshi yoki hajmi kattalashmoq.", "Bola tez ulgʻaydi."),
    ("yaxshilamoq", "Yaxshi holga keltirmoq.", "U oʻz yozuvini yaxshiladi."),
    ("mustahkamlamoq", "Puxta qilmoq, barqaror etmoq.", "Quruvchilar poydevorni mustahkamladi."),
    ("tekshirmoq", "Toʻgʻriligini aniqlash uchun koʻzdan kechirmoq.", "Oʻqituvchi daftarni tekshirdi."),
    ("tahlil qilmoq", "", ""),
    ("taqqoslamoq", "Ikki narsani solishtirmoq.", "Oʻquvchi ikki gapni taqqosladi."),
    ("yodlamoq", "Esda saqlash uchun takrorlab oʻrganmoq.", "Oʻquvchi sheʼrni yodladi."),
    ("takrorlamoq", "Bir ishni qayta bajarmoq.", "Biz darsni takrorladik."),
    ("izlamoq", "Topish maqsadida qidirmoq.", "Ular yoʻqolgan qoʻzichoqni izladi."),
]
FEIL_NEW = [x for x in FEIL_NEW if x[1]]

SON_NEW = [
    ("nol", "Sanoq son: 0, hech narsa yoʻqligini bildiradi.", "Harorat nol darajaga tushdi."),
    ("milliard", "Sanoq son: 1 000 000 000.", "Respublikada bir milliard soʻm sarflandi."),
    ("yuzlab", "Taxminiy son: yuzga yaqin yoki yuz marta koʻp.", "Yuzlab odam yigʻildi."),
    ("minglab", "Taxminiy son: mingga yaqin yoki ming marta koʻp.", "Minglab tomoshabin kelgan edi."),
    ("beshtacha", "Taxminiy son: taxminan besh dona.", "Beshtacha olma qoldi."),
    ("oltinchi", "Tartib son: sanoqda 6-oʻrindagi.", "Oltinchi sinfda oʻqiyman."),
    ("yettinchi", "Tartib son: sanoqda 7-oʻrindagi.", "Yettinchi kun dam olish kuni edi."),
    ("sakkizinchi", "Tartib son: sanoqda 8-oʻrindagi.", "Sakkizinchi mart bayram."),
    ("toʻqqizinchi", "Tartib son: sanoqda 9-oʻrindagi.", "Toʻqqizinchi sinf oʻquvchisi."),
    ("oʻninchi", "Tartib son: sanoqda 10-oʻrindagi.", "Oʻninchi dars boshlandi."),
    ("yigirmanchi", "Tartib son: sanoqda 20-oʻrindagi.", "Yigirmanchi asr tugadi."),
    ("yuzinchi", "Tartib son: sanoqda 100-oʻrindagi.", "Yuzinchi sahifani ochdim."),
    ("oltita", "Dona son: narsalarning olti dona ekanini bildiradi.", "Oltita kitob oldim."),
    ("yettita", "Dona son: narsalarning yetti dona ekanini bildiradi.", "Yettita qalam sotib oldim."),
    ("sakkizta", "Dona son: narsalarning sakkiz dona ekanini bildiradi.", "Sakkizta olma yedim."),
    ("toʻqqizta", "Dona son: narsalarning toʻqqiz dona ekanini bildiradi.", "Toʻqqizta stul keltirdik."),
    ("oʻnta", "Dona son: narsalarning oʻn dona ekanini bildiradi.", "Oʻnta daftar sotib oldim."),
    ("bitta", "Dona son: narsaning bir dona ekanini bildiradi.", "Menda bitta qalam bor."),
    ("yigirmata", "Dona son: narsalarning yigirma dona ekanini bildiradi.", "Yigirmata bola keldi."),
    ("ikkov", "Jamlovchi son: ikki kishining birgalikda ekanini bildiradi.", "Ikkov birga keldi."),
    ("uchov", "Jamlovchi son: uch kishining birgalikda ekanini bildiradi.", "Uchov bogʻga bordi."),
    ("toʻrtov", "Jamlovchi son: toʻrt kishining birgalikda ekanini bildiradi.", "Toʻrtov birga oʻqidi."),
    ("beshov", "Jamlovchi son: besh kishining birgalikda ekanini bildiradi.", "Beshov yigʻildi."),
    ("oltov", "Jamlovchi son: olti kishining birgalikda ekanini bildiradi.", "Oltov safga turdi."),
    ("yettov", "Jamlovchi son: yetti kishining birgalikda ekanini bildiradi.", "Yettov sayohatga chiqdi."),
    ("yuz yigirma", "", ""),
    ("choragi", "", ""),
    ("uchdan", "", ""),
]
SON_NEW = [x for x in SON_NEW if x[1]]

OLMOSH_NEW = [
    ("mening", "Kishilik olmoshi: «men» olmoshining qaratqich shakli.", "Mening kitobim yangi."),
    ("sening", "Kishilik olmoshi: «sen» olmoshining qaratqich shakli.", "Sening doʻsting kim?"),
    ("bizning", "Kishilik olmoshi: «biz» olmoshining qaratqich shakli.", "Bizning uyimiz katta."),
    ("sizning", "Kishilik olmoshi: «siz» olmoshining qaratqich shakli.", "Sizning fikringiz muhim."),
    ("uning", "Kishilik olmoshi: «u» olmoshining qaratqich shakli.", "Uning ismi Aziz."),
    ("oʻzing", "Oʻzlik olmoshi: II shaxsning oʻzi.", "Buni oʻzing qilding."),
    ("oʻzi", "Oʻzlik olmoshi: III shaxsning oʻzi.", "U oʻzi keldi."),
    ("oʻzimiz", "Oʻzlik olmoshi: I shaxs koʻplikning oʻzi.", "Biz uni oʻzimiz yasadik."),
    ("oʻzingiz", "Oʻzlik olmoshi: hurmat bilan II shaxsning oʻzi.", "Buni oʻzingiz tuzatdingizmi?"),
    ("mana", "Koʻrsatish olmoshi: yaqindagi narsani aniq koʻrsatadi.", "Mana, kitob shu yerda."),
    ("ana", "Koʻrsatish olmoshi: uzoqroqdagi narsani koʻrsatadi.", "Ana, bola kelyapti."),
    ("bular", "Koʻrsatish olmoshi: yaqindagi bir necha narsani koʻrsatadi.", "Bular mening kitoblarim."),
    ("shular", "Koʻrsatish olmoshi: aniq koʻrsatilgan bir necha narsani bildiradi.", "Shular menga yoqdi."),
    ("ushbu", "Koʻrsatish olmoshi: rasmiy uslubda yaqindagi narsani koʻrsatadi.", "Ushbu hujjat tasdiqlandi."),
    ("unday", "Koʻrsatish olmoshi: belgi-xususiyatni koʻrsatadi.", "Unday gap yoʻq."),
    ("shunaqa", "Koʻrsatish olmoshi: belgi-xususiyatni koʻrsatadi.", "Shunaqa chiroyli gul koʻrmaganman."),
    ("bunaqa", "Koʻrsatish olmoshi: belgi-xususiyatni koʻrsatadi.", "Bunaqa kitob menda yoʻq."),
    ("qachon", "Soʻroq olmoshi: payt-vaqtni soʻraydi.", "Qachon qaytasan?"),
    ("nega", "Soʻroq olmoshi: sababni soʻraydi.", "Nega kechikding?"),
    ("qandaydir", "Gumon olmoshi: noaniq belgini bildiradi.", "Qandaydir ovoz eshitildi."),
    ("qaysidir", "Gumon olmoshi: nomaʼlum bir narsani bildiradi.", "Qaysidir kitobni oʻqidim."),
    ("birov", "Gumon olmoshi: nomaʼlum shaxsni bildiradi.", "Birov eshikni taqillatdi."),
    ("bironta", "Gumon olmoshi: noaniq bir donani bildiradi.", "Bironta olma bering."),
    ("qachondir", "Gumon olmoshi: nomaʼlum vaqtni bildiradi.", "Qachondir uchrashamiz."),
    ("hammasi", "Belgilash olmoshi: barcha narsani qamrab oladi.", "Hammasi joyida."),
    ("barchasi", "Belgilash olmoshi: toʻliq qamrab oladi.", "Barchasi yaxshi tugadi."),
    ("hechkim", "", ""),
]
OLMOSH_NEW = [x for x in OLMOSH_NEW if x[1]]

RAVISH_NEW = [
    ("ohista", "Tarz: shoshmasdan, sekin va yumshoq.", "U eshikni ohista ochdi."),
    ("bemalol", "Tarz: qiynalmasdan, erkin.", "Bemalol oʻtiring."),
    ("ketma-ket", "Tarz: birin-ketin, uzilishsiz.", "Mashinalar ketma-ket oʻtdi."),
    ("yonma-yon", "Tarz: bir-biriga yaqin, bir qatorda.", "Ular yonma-yon yurdi."),
    ("ataylab", "Maqsad: oldindan niyat qilib.", "U ataylab kechikdi."),
    ("allaqachon", "Payt: ancha avval.", "U allaqachon ketgan."),
    ("endi", "Payt: shu paytdan boshlab.", "Endi dars boshlanadi."),
    ("hanuz", "Payt: hozirgacha, hali ham.", "U hanuz kelmadi."),
    ("darrov", "Payt: kechiktirmasdan.", "U darrov javob berdi."),
    ("tezda", "Payt: qisqa vaqt ichida.", "Ishni tezda tugatdik."),
    ("ertalab", "Payt: kunning boshlanish vaqtida.", "Ertalab shabnam tushdi."),
    ("kechqurun", "Payt: kunning oxirida, quyosh botgach.", "Kechqurun oila yigʻildi."),
    ("kunduz", "Payt: kunning yorugʻ vaqtida.", "Kunduz havo issiq boʻldi."),
    ("hozircha", "Payt: hozirgi paytda, hozir uchun.", "Hozircha hech kim kelmadi."),
    ("qayta-qayta", "Takror: koʻp marta, takrorlab.", "U qayta-qayta urindi."),
    ("birin-ketin", "Takror: bir-biridan keyin navbat bilan.", "Mehmonlar birin-ketin kirdi."),
    ("yana-yana", "", ""),
    ("biroz", "Miqdor: ozgina, kam miqdorda.", "U biroz kutdi."),
    ("nihoyatda", "Daraja: juda yuqori darajada.", "Havo nihoyatda sovuq edi."),
    ("behad", "Daraja: haddan tashqari.", "U behad xursand boʻldi."),
    ("gʻoyat", "Daraja: juda, nihoyatda.", "Manzara gʻoyat goʻzal edi."),
    ("kamroq", "Miqdor: oʻrtachadan past.", "U kamroq gapirdi."),
    ("koʻproq", "Miqdor: oʻrtachadan yuqori.", "Koʻproq oʻqish kerak."),
    ("tepada", "Oʻrin: yuqori joyda.", "Tepada qush uchdi."),
    ("pastda", "Oʻrin: past joyda.", "Pastda daryo oqardi."),
    ("ichkarida", "Oʻrin: ichki qismda.", "Ichkarida chiroq yondi."),
    ("tashqarida", "Oʻrin: tashqi qismda.", "Tashqarida qor yogʻdi."),
    ("oldinda", "Oʻrin: old tomonda.", "Oldinda yoʻl choʻzildi."),
    ("orqada", "Oʻrin: orqa tomonda.", "Orqada bola yugurib keldi."),
    ("shundoq", "Tarz: shu tarzda, shunday.", "U shundoq javob berdi."),
    ("birdaniga", "Payt: bir zumda, kutilmaganda.", "Shamol birdaniga kuchaydi."),
    ("boshqacha", "Tarz: boshqa usulda.", "U boshqacha fikrladi."),
    ("jimgina", "Tarz: ovoz chiqarmasdan.", "U jimgina oʻtirdi."),
    ("shoshib", "", ""),
    ("oʻz-oʻzidan", "Tarz: tashqi taʼsirsiz, avtomatik.", "Eshik oʻz-oʻzidan ochildi."),
    ("xotirjam", "", ""),
    ("kam-kam", "Miqdor: oz-oz, oz miqdorda.", "U kam-kam gapirdi."),
]
RAVISH_NEW = [x for x in RAVISH_NEW if x[1]]

KOMAKCHI_NEW = [
    ("tufayli", "Sabab maʼnosini bildiradi.", "Yomgʻir tufayli yoʻl buzildi."),
    ("natijasida", "Sabab-oqibat maʼnosini bildiradi.", "Mehnat natijasida muvaffaqiyatga erishdi."),
    ("yuzasidan", "Mavzu yoki sababni bildiradi.", "Masala yuzasidan suhbatlashdik."),
    ("nisbatan", "Taqqoslash maʼnosini bildiradi.", "Kechagiga nisbatan bugun issiq."),
    ("qaraganda", "Taqqoslash maʼnosini bildiradi.", "Akamdan qaraganda ukam balandroq."),
    ("oʻrniga", "Almashtirish maʼnosini bildiradi.", "Choy oʻrniga sut ichdim."),
    ("boʻyicha", "Soha yoki asosni bildiradi.", "Fan boʻyicha imtihon oʻtdi."),
    ("doir", "Aloqadorlikni bildiradi.", "Tarixga doir kitob oʻqidim."),
    ("oid", "Aloqadorlikni bildiradi.", "Madaniyatga oid maqola chiqdi."),
    ("xususida", "Mavzuni bildiradi.", "U sayohat xususida gapirdi."),
    ("ila", "Vosita yoki birgalikni bildiradi (adabiy uslubda).", "Mehr ila qaradi."),
    ("yanglig", "Oʻxshashlikni bildiradi (adabiy uslubda).", "Oy yanglig porladi."),
    ("uzra", "Oʻrinni bildiradi (adabiy uslubda).", "Togʻ uzra bulut suzdi."),
    ("soʻng", "Vaqt maʼnosini bildiradi.", "Darsdan soʻng uyga qaytdim."),
]
BOGLOVCHI_NEW = [
    ("holbuki", "Zid bogʻlovchi: qarama-qarshilikni bildiradi.", "U bilaman dedi, holbuki bilmas edi."),
    ("vaholanki", "Zid bogʻlovchi: qarama-qarshilikni kuchaytiradi.", "U kelmadi, vaholanki vaʼda bergan edi."),
    ("agarda", "Shart bogʻlovchisi: shartni bildiradi.", "Agarda vaqt boʻlsa, uchrashamiz."),
    ("modomiki", "Sabab bogʻlovchisi: sababni bildiradi.", "Modomiki rozisan, boshlaymiz."),
    ("zero", "Sabab bogʻlovchisi: sababni izohlaydi.", "Shoshilma, zero hali vaqt bor."),
    ("chunonchi", "Izohlovchi bogʻlovchi: misol bilan izohlaydi.", "Meva, chunonchi olma, mazali."),
    ("yoinki", "Ayiruvchi bogʻlovchi: tanlovni bildiradi.", "Choy yoinki qahva ichamiz."),
    ("lek", "Zid bogʻlovchi: qarama-qarshilikni bildiradi (adabiy uslubda).", "Urindi, lek eplay olmadi."),
    ("bordi-yu", "Shart bogʻlovchisi: kam ehtimolli shartni bildiradi.", "Bordi-yu yomgʻir yogʻsa, qolamiz."),
    ("hamki", "", ""),
]
BOGLOVCHI_NEW = [x for x in BOGLOVCHI_NEW if x[1]]
YUKLAMA_NEW = [
    ("aynan", "Ajratib koʻrsatish yuklamasi: aniqlikni taʼkidlaydi.", "Aynan shu gap meni oʻylantirdi."),
    ("goʻyoki", "Qiyoslash yuklamasi: taxminiy oʻxshashlikni bildiradi.", "Goʻyoki hech narsa boʻlmaganday turdi."),
    ("nahot", "Soʻroq-taʼkid yuklamasi: ajablanishni bildiradi.", "Nahot sen buni bilmasang?"),
    ("-da", "Kuchaytirish yuklamasi: taʼkid yoki kuchaytirish maʼnosini beradi.", "Bor-da, koʻrib kel."),
    ("-u", "Kuchaytirish yuklamasi: aniqlik yoki taʼkid beradi.", "Bordi-yu, kelmadi."),
    ("-a", "Taʼkid yuklamasi: his-tuygʻu va taʼkidni bildiradi.", "Qanday yaxshi-a!"),
    ("-dir", "Taxmin yuklamasi: taxmin va gumonni bildiradi.", "Ehtimol, u ketgandir."),
]
UNDOV_NEW = [
    ("oho", "Hayrat va tahsinni bildiradi.", "Oho, qanday chiroyli!"),
    ("ehe", "Ajablanish yoki kinoyani bildiradi.", "Ehe, bu yerda kimlar yoʻq!"),
    ("vah", "Hayrat va zavqni bildiradi.", "Vah, naqadar goʻzal manzara!"),
    ("vay", "Qoʻrquv yoki ajablanishni bildiradi.", "Vay, tushib ketdim!"),
    ("bay-bay", "Hayrat va tahsinni bildiradi.", "Bay-bay, qanday katta uy!"),
    ("voy-voy", "Qoʻrquv va ajablanishni bildiradi.", "Voy-voy, nima qilib qoʻydim!"),
    ("hay-hay", "Qarshilik, norozilikni bildiradi.", "Hay-hay, boʻldi qil!"),
    ("ayvoh", "Afsus, nadomatni bildiradi.", "Ayvoh, kech qoldik!"),
    ("pisht", "Hayvonni haydash uchun ishlatiladi.", "Pisht, ket bu yerdan!"),
    ("kisht", "Qushni haydash uchun ishlatiladi.", "Kisht, qush uchib ket!"),
    ("xoʻsh", "Soʻroq yoki qiziqishni bildiradi.", "Xoʻsh, nima gap?"),
    ("hayhot", "Afsus va armonni bildiradi.", "Hayhot, vaqt oʻtdi."),
    ("mashallo", "Maqtov, tahsin bildiradi.", "Mashallo, bola katta boʻptibdi!"),
    ("subhonalloh", "Hayrat va tahsin bildiradi.", "Subhonalloh, naqadar buyuk!"),
    ("marhamat", "Taklif va xushmuomalalikni bildiradi.", "Marhamat, kiring!"),
]
MODAL_NEW = [
    ("masalan", "Misol keltirishni bildiradi.", "Masalan, men kitob oʻqishni yaxshi koʻraman."),
    ("jumladan", "Ajratib misol keltirishni bildiradi.", "Jumladan, u ham qatnashdi."),
    ("xususan", "Alohida ajratib koʻrsatishni bildiradi.", "Xususan, ona tili darsi qiziqarli."),
    ("birinchidan", "Fikrlar tartibini bildiradi.", "Birinchidan, vaqt yoʻq."),
    ("ikkinchidan", "Fikrlar tartibini bildiradi.", "Ikkinchidan, bu qimmat."),
    ("nihoyat", "Uzoq kutilgan natijani bildiradi.", "Nihoyat, ish tugadi."),
    ("haqiqatan", "Tasdiq va ishonchni bildiradi.", "Haqiqatan, u haq ekan."),
    ("rostdan", "Ishonch va tasdiqni bildiradi.", "Rostdan, men xato qilibman."),
    ("aslida", "Asl holatni bildiradi.", "Aslida, hammasi boshqacha edi."),
    ("qisqasi", "Xulosa bildiradi.", "Qisqasi, ish bitdi."),
    ("umuman", "Umumiy xulosani bildiradi.", "Umuman, hammasi yaxshi."),
    ("oxir-oqibat", "Natijani bildiradi.", "Oxir-oqibat, u gʻalaba qozondi."),
    ("yaxshiyamki", "Baxtli tasodifni bildiradi.", "Yaxshiyamki, oʻz vaqtida keldik."),
    ("tabiiyki", "Tabiiylik, qonuniyatni bildiradi.", "Tabiiyki, bu qiyin boʻlgan."),
]
TAQLID_NEW = [
    ("tap-tap", "Oyoq tovushiga taqlid.", "Bola tap-tap qilib yugurdi."),
    ("tuk-tuk", "Mayda taqillashga taqlid.", "Eshik tuk-tuk qilib taqillatildi."),
    ("taraq-taraq", "Qattiq narsalar urilishiga taqlid.", "Gʻildirak taraq-taraq qilib yurdi."),
    ("gumbur-gumbur", "Momaqaldiroq yoki dumbira tovushiga taqlid.", "Osmonda gumbur-gumbur ovoz eshitildi."),
    ("dukur-dukur", "Otning dukurlab yurishiga taqlid.", "Ot dukur-dukur qilib chopdi."),
    ("qoʻq-qoʻq", "Tovuqning ovoziga taqlid.", "Tovuq qoʻq-qoʻq qildi."),
    ("maa-maa", "Qoʻyning ovoziga taqlid.", "Qoʻy maa-maa deb chaqirdi."),
    ("chuvur-chuvur", "Chumchuqlarning sayrashiga taqlid.", "Chumchuqlar chuvur-chuvur qilishdi."),
    ("bijir-bijir", "Tez va toʻxtovsiz gapirishga taqlid.", "Qiz bijir-bijir gapirdi."),
    ("pichir-pichir", "Past ovozda shivirlashga taqlid.", "Ular pichir-pichir qilib gaplashdi."),
    ("sharq-sharq", "Suv oqishi yoki tushishi tovushiga taqlid.", "Sharshara sharq-sharq tushdi."),
    ("lip-lip", "Miltillab porlashga taqlid.", "Chiroq lip-lip yondi."),
    ("yalt-yalt", "Yaltirashga taqlid.", "Yulduzlar yalt-yalt qilardi."),
    ("lov-lov", "Alanganing lovullashiga taqlid.", "Olov lov-lov yondi."),
    ("dir-dir", "Titrash holatiga taqlid.", "U sovuqdan dir-dir titradi."),
    ("gup-gup", "Yurak urishiga taqlid.", "Yuragi gup-gup urdi."),
    ("qars-qars", "Quruq narsa sinishiga taqlid.", "Novda qars-qars sindi."),
    ("shuv-shuv", "", ""),
]
TAQLID_NEW = [x for x in TAQLID_NEW if x[1]]

ATAMA_NEW = [
    ("fonetika", "Tilning tovush tizimini oʻrganuvchi boʻlim.", "Fonetika tovush va boʻgʻinlarni oʻrganadi."),
    ("leksikologiya", "Tilning lugʻat tarkibini oʻrganuvchi boʻlim.", "Leksikologiya soʻzlarning maʼnosini tekshiradi."),
    ("morfologiya", "Soʻz turkumlari va soʻz shakllarini oʻrganuvchi boʻlim.", "Morfologiya soʻz yasalishini ham oʻrganadi."),
    ("sintaksis", "Soʻz birikmasi va gaplarni oʻrganuvchi boʻlim.", "Sintaksis gap boʻlaklarini tahlil qiladi."),
    ("grammatika", "Til qurilishi va uning qonun-qoidalari tizimi.", "Grammatika qoidalarini bilish nutqni boyitadi."),
    ("tovush", "Nutqda aytiladigan eng kichik birlik.", "Har bir tovush maʼlum harf bilan ifodalanadi."),
    ("intonatsiya", "Nutqdagi ohang, ovoz koʻtarilishi va pasayishi.", "Intonatsiya gapning maʼnosini oʻzgartiradi."),
    ("pauza", "Nutqdagi qisqa toʻxtash.", "Gap oʻrtasida pauza qilib oʻqing."),
    ("fonema", "Tilning maʼno farqlovchi eng kichik tovush birligi.", "Fonema soʻz maʼnosini ajratishga yordam beradi."),
    ("transkripsiya", "Soʻzning aytilishini maxsus belgilarda yozish.", "Transkripsiya talaffuzni koʻrsatadi."),
    ("jarangli undosh", "Ovoz ishtirokida aytiladigan undosh.", "B, d, g — jarangli undoshlar."),
    ("jarangsiz undosh", "Faqat shovqin bilan aytiladigan undosh.", "P, t, k — jarangsiz undoshlar."),
    ("sinharmonizm", "Unlilarning bir-biriga uygʻun moslashuvi.", "Oʻzbek adabiy tilida sinharmonizm yoʻq."),
    ("affiks", "Soʻzning oʻzak va qoʻshimcha qismi.", "Qoʻshimchalar affikslar deyiladi."),
    ("leksema", "Lugʻatdagi soʻz birligi.", "Leksema maʼnoga ega boʻladi."),
    ("neologizm", "Yangi paydo boʻlgan soʻz.", "«Internet» — neologizm sifatida kirib kelgan."),
    ("arxaizm", "Eskirgan, hozir kam ishlatiladigan soʻz.", "«Maktub» — arxaizm."),
    ("dialekt", "Til yoki shevaning hududiy koʻrinishi.", "Dialekt oʻziga xos talaffuz va soʻzlarga ega."),
    ("sheva", "Xalq tilining hududiy xususiyatli turi.", "Sheva soʻzlari adabiy tilga taʼsir qiladi."),
    ("adabiy til", "Umumxalq tilining meʼyorlashtirilgan, ishlov berilgan shakli.", "Adabiy tilda yozuv va rasmiy nutq yaratiladi."),
    ("termin", "Fan yoki kasb sohasiga oid aniq tushuncha bildiruvchi soʻz.", "«Fonema» — tilshunoslik termini."),
    ("jargon", "Muayyan guruh doirasida ishlatiladigan soʻz yoki ibora.", "Jargon adabiy tilga kirmaydi."),
    ("kasbiy soʻz", "Muayyan kasb egalari qoʻllaydigan soʻz.", "«Tandir» — novvoylarning kasbiy soʻzi."),
    ("oʻzlashma soʻz", "Boshqa tildan kirib kelgan soʻz.", "«Kitob» — arabchadan oʻzlashgan soʻz."),
    ("turgʻun birikma", "Maʼnosi bir butun boʻlgan, oʻzgarmas birikma.", "Turgʻun birikmalar frazeologizmlardir."),
    ("ajratilgan boʻlak", "Gapda alohida urgʻu va ohang bilan ajratilgan boʻlak.", "Ajratilgan boʻlak vergul bilan ajratiladi."),
    ("ergash gap", "Bosh gapga bogʻlanib, uning boʻlagini izohlaydigan gap.", "Ergash gap bosh gapga tobe boʻladi."),
    ("bosh gap", "Ergash gap tobe boʻladigan asosiy gap.", "Bosh gap ergash gapga maʼno beradi."),
    ("bogʻlangan qoʻshma gap", "Teng huquqli sodda gaplardan tuzilgan qoʻshma gap.", "Yomgʻir yogʻdi va shamol esdi."),
    ("ergash gapli qoʻshma gap", "Bosh va ergash gapdan tuzilgan qoʻshma gap.", "Agar yomgʻir yogʻsa, uyda qolamiz."),
    ("bogʻlovchisiz qoʻshma gap", "Qismlari bogʻlovchisiz, ohang bilan bogʻlangan qoʻshma gap.", "Kuz keldi, barglar soʻlib tushdi."),
    ("yigʻiq gap", "Faqat bosh boʻlaklardan iborat sodda gap.", "Bahor keldi."),
    ("yoyiq gap", "Bosh va ikkinchi darajali boʻlaklardan iborat sodda gap.", "Chiroyli bahor keldi."),
    ("darak gap", "Biror voqea yoki holat haqida xabar beruvchi gap.", "Quyosh chiqdi."),
    ("soʻroq gap", "Savol bildiruvchi gap.", "Qayerga ketyapsiz?"),
    ("buyruq gap", "Amr, iltimos yoki taklif bildiruvchi gap.", "Kitobni oching!"),
    ("undov gap", "Kuchli his-tuygʻu bildiruvchi gap.", "Naqadar goʻzal!"),
    ("buyruq mayli", "Buyruq, iltimos maʼnosini bildiruvchi feʼl shakli.", "Oʻqing, yozing."),
    ("shart mayli", "Shart bildiruvchi feʼl shakli.", "Kelsang, birga boramiz."),
    ("istak mayli", "Istak, xohish bildiruvchi feʼl shakli.", "Kelgim keldi."),
    ("aniqlik mayli", "Ish-harakatning aniq bajarilishini bildiruvchi feʼl shakli.", "U kitob oʻqidi."),
    ("nisbat", "Feʼlning ish-harakat bajaruvchisi va obyektiga munosabatini bildiruvchi shakli.", "Nisbat feʼlning shaklini oʻzgartiradi."),
    ("orttirma nisbat", "Ish-harakatni boshqa kishiga bajartirishni bildiruvchi nisbat.", "Yozdirdi, oʻqitdi."),
    ("oʻzlik nisbat", "Ish-harakat egasining oʻzida kechishini bildiruvchi nisbat.", "Yuvindi, kiyindi."),
    ("majhul nisbat", "Ish-harakat bajaruvchisi nomaʼlum boʻlgan nisbat.", "Kitob yozildi."),
    ("birgalik nisbat", "Ish-harakatning birgalikda bajarilishini bildiruvchi nisbat.", "Suhbatlashdi, kurashdi."),
    ("bosh kelishik", "Kim? nima? soʻroqlariga javob beruvchi kelishik.", "Kitob stolda turibdi."),
    ("tushum kelishigi", "Kimni? nimani? soʻroqlariga javob beruvchi kelishik.", "Men kitobni oʻqidim."),
    ("joʻnalish kelishigi", "Kimga? nimaga? qayerga? soʻroqlariga javob beruvchi kelishik.", "Maktabga bordim."),
    ("oʻrin-payt kelishigi", "Kimda? nimada? qayerda? soʻroqlariga javob beruvchi kelishik.", "Uyda oʻtirdim."),
    ("chiqish kelishigi", "Kimdan? nimadan? qayerdan? soʻroqlariga javob beruvchi kelishik.", "Shahardan keldik."),
    ("qaratqich kelishigi", "Kimning? nimaning? soʻroqlariga javob beruvchi kelishik.", "Onamning kitobi."),
    ("otlashish", "Boshqa turkum soʻzining ot vazifasida kelishi.", "Yaxshilar koʻp boʻlsin — «yaxshilar» otlashgan."),
    ("sifatlanish", "Ot yoki boshqa turkum soʻzining sifat vazifasida kelishi.", "Oltin soat — «oltin» sifatlangan."),
    ("yordamchi feʼl", "Asosiy feʼlga qoʻshilib, qoʻshimcha maʼno beruvchi feʼl.", "Oʻqib chiqdi — «chiqdi» yordamchi feʼl."),
    ("oʻtgan zamon", "Ish-harakatning gapirishdan oldin boʻlganini bildiruvchi shakl.", "U kecha keldi."),
    ("hozirgi zamon", "Ish-harakatning hozir boʻlayotganini bildiruvchi shakl.", "U kitob oʻqiyapti."),
    ("kelasi zamon", "Ish-harakatning keyin boʻlishini bildiruvchi shakl.", "U ertaga keladi."),
    ("nutq", "Odamlarning til vositasida fikr almashish jarayoni.", "Nutq ogʻzaki va yozma boʻladi."),
    ("ogʻzaki nutq", "Tovushlar vositasida amalga oshadigan nutq.", "Suhbat — ogʻzaki nutq."),
    ("yozma nutq", "Harflar vositasida ifodalangan nutq.", "Xat — yozma nutq."),
    ("nutq uslubi", "Til vositalarining maʼlum maqsadda tanlab qoʻllanishi.", "Ilmiy, rasmiy, badiiy — nutq uslublari."),
    ("ilmiy uslub", "Fan va taʼlimda ishlatiladigan aniq va izchil uslub.", "Darslik ilmiy uslubda yozilgan."),
    ("rasmiy uslub", "Hujjat va murojaatlarda ishlatiladigan uslub.", "Ariza — rasmiy uslubga misol."),
    ("badiiy uslub", "Obrazli, hissiy taʼsirchan uslub.", "Sheʼr badiiy uslubda yoziladi."),
    ("soʻzlashuv uslubi", "Kundalik suhbatda qoʻllanadigan uslub.", "Oʻrtoqlar orasida soʻzlashuv uslubi ishlatiladi."),
    ("publitsistik uslub", "Gazeta va jurnallarda ommaviy axborot uchun ishlatiladigan uslub.", "Maqola publitsistik uslubda yozildi."),
    ("matn", "Maʼlum fikrni ifodalovchi, bir-biriga bogʻliq gaplar yigʻindisi.", "Matn mavzuga mos boʻlishi kerak."),
    ("bayon", "Voqea yoki fikrni izchil aytib berish.", "Bayon yozish uchun reja tuzing."),
    ("ariza", "Biror iltimos bilan yoziladigan rasmiy hujjat.", "Ariza rahbarga topshirildi."),
    ("tarjimai hol", "Shaxsning hayot yoʻli haqidagi qisqa maʼlumot.", "Tarjimai hol qisqa yozildi."),
    ("ikki tomonlama bogʻlanish", "", ""),
]
ATAMA_NEW = [x for x in ATAMA_NEW if x[1]]

ADABIY_NEW = [
    ("lirika", "Shoir tuygʻu va kechinmalarini ifodalovchi adabiy tur.", "Lirika shoir qalbini aks ettiradi."),
    ("epos", "Voqealarni hikoya qilib tasvirlovchi adabiy tur.", "Epos katta voqealarni qamrab oladi."),
    ("drama", "Sahnada ijro etish uchun yozilgan adabiy tur.", "Drama personajlar suhbati asosida quriladi."),
    ("komediya", "Kulgili voqealar tasvirlangan sahna asari.", "Komediya tomoshabinni kuldiradi."),
    ("fojea", "Qahramon fojiasini tasvirlovchi dramatik asar.", "Fojea oxirida qahramon halok boʻladi."),
    ("ertak", "Xalq ogʻzaki ijodidagi xayoliy voqealar hikoyasi.", "Ertak odatda yaxshilik gʻalabasi bilan tugaydi."),
    ("afsona", "Qadimiy voqea va qahramonlar haqidagi xalq rivoyati.", "Afsona xalq orasida ogʻizdan ogʻizga oʻtadi."),
    ("rivoyat", "Xalq orasida aytiladigan, haqiqatga yaqin hikoya.", "Rivoyat tarixiy shaxs haqida."),
    ("masal", "Hayvonlar va narsalar tilidan ibrat beruvchi qisqa hikoya.", "Masal oxirida xulosa keltiriladi."),
    ("latifa", "Qisqa, kulgili va oʻtkir fikrli hikoya.", "Latifa kulgi uygʻotadi."),
    ("topishmoq", "Narsa yoki hodisani bilvosita tasvirlovchi xalq ijodi namunasi.", "Topishmoq oʻylashga undaydi."),
    ("qasida", "Maqtov mazmunidagi sheʼriy janr.", "Qasida shoh yoki ulugʻ zotni maqtaydi."),
    ("masnaviy", "Har bayti oʻz qofiyasiga ega boʻlgan sheʼriy shakl.", "Doston masnaviy shaklda yozilgan."),
    ("tuyuq", "Soʻzlarning shakldosh qofiyasiga asoslangan toʻrtlik.", "Tuyuq soʻz oʻyiniga boy."),
    ("muxammas", "Besh misrali band shaklidagi sheʼr.", "Muxammas bandlari bir xil tuzilgan."),
    ("hajviya", "Kamchilikni kulgi orqali fosh etuvchi asar.", "Hajviya kinoya bilan boyitilgan."),
    ("satira", "Illat va kamchiliklarni oʻtkir kulgi bilan fosh etish.", "Satira jamiyat kamchiligini tanqid qiladi."),
    ("prolog", "Asarning kirish qismi.", "Prolog voqealarni tanishtiradi."),
    ("epilog", "Asarning yakunlovchi qismi.", "Epilog voqealar oqibatini koʻrsatadi."),
    ("epigraf", "Asar yoki bob boshiga qoʻyilgan qisqa soʻz.", "Epigraf asarning gʻoyasini ochib beradi."),
    ("ekspozitsiya", "Voqealar boshlanishidan oldingi tanishtiruv qismi.", "Ekspozitsiya qahramonlarni tanishtiradi."),
    ("tugun", "Asardagi voqealar boshlanib, ziddiyat paydo boʻlgan nuqta.", "Tugun asar voqealarini boshlab beradi."),
    ("avj", "Asarda ziddiyat eng yuqori nuqtaga yetgan qism.", "Avj nuqtasi oʻquvchini hayajonga soladi."),
    ("yechim", "Asarda ziddiyatning hal boʻlish qismi.", "Yechim asarni yakunlaydi."),
    ("kompozitsiya", "Asar qismlarining tartibli joylashuvi.", "Kompozitsiya asarning tuzilishidir."),
    ("personaj", "Asarda ishtirok etuvchi shaxs.", "Personaj xarakteri voqealarda ochiladi."),
    ("lirik qahramon", "Sheʼrda shoir tuygʻularini ifodalovchi obraz.", "Lirik qahramon qalbini ochadi."),
    ("peyzaj", "Asarda tabiat tasviri.", "Peyzaj kayfiyatni kuchaytiradi."),
    ("portret", "Asarda qahramonning tashqi koʻrinishi tasviri.", "Portret qahramonni yaqqol koʻrsatadi."),
    ("kinoya", "Maqtov shaklida yashirin tanqid bildirish.", "Kinoya orqali kamchilik fosh etildi."),
    ("tashbeh", "Oʻxshatish sanʼati.", "Tashbeh narsalarni bir-biriga oʻxshatadi."),
    ("folklor", "Xalq ogʻzaki ijodi.", "Folklor xalq ruhini aks ettiradi."),
    ("taxallus", "Ijodkorning asarlarida qoʻllaydigan nomi.", "«Navoiy» — Alisher Navoiyning taxalluslaridan biri."),
    ("mumtoz adabiyot", "Qadimiy va klassik adabiyot.", "Mumtoz adabiyot bebaho meros."),
    ("tanqid", "Asarning yutuq va kamchiligini baholash.", "Tanqid asarni yaxshilashga xizmat qiladi."),
    ("ritm", "Sheʼrda ohang va boʻgʻinlarning muntazam almashinuvi.", "Ritm sheʼrga ohang beradi."),
]
BADIIY_NEW = [
    ("zulf", "Sochning uzun, jingalak tolasi (sheʼriy nutqda).", "Zulfi shamolda hilpiradi."),
    ("qomat", "Odam gavdasi, qad-qomati.", "Sarv kabi qomati koʻrinardi."),
    ("qosh", "Koʻz ustidagi tuk chizigʻi (sheʼriy nutqda).", "Qoshi kamon kabi."),
    ("ohu", "Kiyik; nafis, jozibali koʻzga ishora (sheʼriy nutqda).", "Koʻzlari ohu kabi."),
    ("jonon", "Suyukli, sevgan kishi.", "Jonon yoʻliga intizor qoldi."),
    ("navo", "Kuy, ohang.", "Navo qalbni tebratdi."),
    ("sado", "Aks-sado, ovoz.", "Togʻlardan sado keldi."),
    ("nola", "Dard bilan yigʻlab aytilgan faryod.", "Nola chekib yigʻladi."),
    ("faryod", "Ogʻir dard bilan baland ovozda yigʻlash.", "Faryod osmonga koʻtarildi."),
    ("sarob", "Choʻlda yaqinda suv borday koʻrinadigan aldamchi manzara.", "Sarob ortidan quvdi."),
    ("qismat", "Insonning boshiga tushgan hayot yoʻli, taqdir.", "Qismat uni yangi yoʻlga boshladi."),
    ("taqdir", "Insonning hayotda yozilgan yoʻli.", "Taqdir sinoviga bardosh berdi."),
    ("nasib", "Taqdirda kimga nima tegishi.", "Yutuq unga nasib etdi."),
    ("xayol", "Ongda paydo boʻladigan tasavvur.", "Xayol uni uzoqlarga olib ketdi."),
    ("hayrat", "Ajablanish bilan aralash taʼsir.", "Hayrat koʻzlarida yarqiradi."),
    ("hasrat", "Ushalmagan orzu uchun chekilgan armon.", "Hasrat uning qalbini kuydirdi."),
    ("iztirob", "Ruhiy qiynalish, bezovtalik.", "Iztirob uni tark etmadi."),
    ("iltijo", "Mehr bilan yalinib soʻrash.", "Iltijo bilan yolvordi."),
    ("intizor", "Kimdir yoki nimadir uchun sabrsizlik bilan kutuvchi.", "Intizor boʻlib yoʻl qaradi."),
    ("muhabbat", "Qattiq mehr, yaxshi koʻrish tuygʻusi.", "Muhabbat yurakni oʻstiradi."),
    ("nafosat", "Goʻzallik, nazokat.", "Nafosat uning ijodida yaqqol sezildi."),
    ("latofat", "Nafislik, yoqimlilik.", "Latofat uning yuzida porladi."),
    ("noz", "Erkalanib oʻzini tutish.", "Nozli qiz oʻzini toʻxtatdi."),
    ("gʻamza", "Mayin, oʻynoqi qarash.", "Gʻamza bilan qaradi."),
    ("fugʻon", "Dard va afsusdan chiqadigan ohu-nola.", "Fugʻon osmonni titratdi."),
    ("vujud", "Odam tanasi, butun borligʻi.", "Vujudi titrab ketdi."),
    ("nasim", "Mayin tong shabadasi.", "Nasim gullarni silab oʻtdi."),
    ("sabo", "Yengil, oʻzgacha xushboʻy shabada.", "Sabo xushboʻy hid taratdi."),
    ("gulzor", "Gullar koʻp oʻsgan joy.", "Gulzor yam-yashil edi."),
    ("chaman", "Gulzor, bogʻ-rogʻ.", "Chamanda bulbul sayradi."),
    ("boʻstan", "Gul va mevali daraxtlar bogʻi.", "Boʻstonda tong otdi."),
    ("lola", "Bahorda ochiladigan qizil gul.", "Lola togʻ yonbagʻrini bezadi."),
    ("nargis", "Oq, xushboʻy bahor guli.", "Nargis bahor kelganini bildirdi."),
    ("sahro", "Cheksiz, odamsiz keng yer.", "Sahroda karvon yurdi."),
    ("jilva", "Nurning yaltirab, goʻzal tovlanishi.", "Quyosh jilvasi suvda oʻynadi."),
]


OT += OT_NEW
SIFAT += SIFAT_NEW
FEIL += FEIL_NEW
SON += SON_NEW
OLMOSH += OLMOSH_NEW
RAVISH += RAVISH_NEW
KOMAKCHI += KOMAKCHI_NEW
BOGLOVCHI += BOGLOVCHI_NEW
YUKLAMA += YUKLAMA_NEW
UNDOV += UNDOV_NEW
MODAL += MODAL_NEW
TAQLID += TAQLID_NEW
ATAMALAR += ATAMA_NEW
ADABIY += ADABIY_NEW
BADIIY += BADIIY_NEW


OT_2 = [('farzand', 'Ota-onaning bolasi, oʻgʻil yoki qiz.', 'Farzand ota-onaning quvonchi.'), ('oʻgʻil', 'Ota-onaning erkak jinsidagi bolasi.', 'Oʻgʻil otasiga yordam berdi.'), ('nevara', 'Oʻgʻil yoki qizning bolasi.', 'Nevara buvisiga gul olib keldi.'), ('kelin', 'Yangi turmush qurgan ayol; oʻgʻilning xotini.', 'Kelin yangi uyga kirdi.'), ('kuyov', 'Qizning eri.', 'Kuyov qaynotasiga salom berdi.'), ('er', 'Turmush qurgan ayolning juftiga aytiladi.', 'Er xotiniga yordam berdi.'), ('xotin', 'Turmush qurgan erkakning juftiga aytiladi.', 'Xotin choy damladi.'), ('qarindosh', 'Tugʻishgan yoki nasabdosh kishi.', 'Qarindosh bayramga keldi.'), ('mahalla', 'Shahar yoki qishloqdagi aholi turar joyi, jamoat birligi.', 'Mahalla keng hovlili edi.'), ('fuqaro', 'Davlatga mansub kishi.', 'Fuqaro qonunga amal qiladi.'), ('jamiyat', 'Birgalikda yashovchi odamlar majmuasi.', 'Jamiyat ilm bilan rivojlanadi.'), ('davlat', 'Mamlakatni boshqaruvchi tashkilot va uning hududi.', 'Davlat fuqarolarini himoya qiladi.'), ('mamlakat', 'Chegarasi aniq, mustaqil hudud.', 'Mamlakat tez rivojlanmoqda.'), ('poytaxt', 'Davlatning bosh shahri.', 'Poytaxt gavjum edi.'), ('viloyat', 'Mamlakatning maʼmuriy qismi.', 'Viloyat markazi chiroyli.'), ('tuman', 'Viloyatning maʼmuriy boʻlimi.', 'Tuman aholisi dehqonchilik qiladi.'), ('chegara', 'Ikki hudud yoki davlat orasidagi chiziq.', 'Chegara qoʻriqlanadi.'), ('bayroq', 'Davlat yoki tashkilot ramzi boʻlgan mato.', 'Bayroq baland koʻtarildi.'), ('qonun', 'Davlat tomonidan belgilangan majburiy qoida.', 'Qonun hammaga barobar.'), ('huquq', 'Qonun bilan berilgan imkoniyat.', 'Huquq har bir kishiga tegishli.'), ('burch', 'Bajarilishi shart boʻlgan majburiyat.', 'Burch Vatan oldida ado etiladi.'), ('rahbar', 'Jamoani boshqaruvchi shaxs.', 'Rahbar yigʻilishni boshladi.'), ('elchi', 'Davlatni xorijda vakil qilib turuvchi shaxs.', 'Elchi hujjat topshirdi.'), ('sudya', 'Sud ishlarini koʻruvchi shaxs.', 'Sudya hukmni oʻqidi.'), ('politsiyachi', 'Tartibni saqlovchi huquq xodimi.', 'Politsiyachi yoʻlni tartibga soldi.'), ('oʻqish', 'Taʼlim olish jarayoni.', 'Oʻqish yosh kishiga bilim beradi.'), ('fan', 'Bilimlarning tizimlashgan sohasi.', 'Fan yangi kashfiyotlarga yoʻl ochadi.'), ('kashfiyot', 'Yangi, oldin maʼlum boʻlmagan narsani topish.', 'Kashfiyot dunyoni oʻzgartirdi.'), ('tajriba', 'Sinov asosida hosil qilingan bilim yoki malaka.', 'Tajriba ish usulini oʻrgatadi.'), ('olim', 'Ilm bilan shugʻullanuvchi mutaxassis.', 'Olim yangi nazariyani yaratdi.'), ('kutubxonachi', 'Kutubxonada ishlovchi xodim.', 'Kutubxonachi kitob berdi.'), ('maqola', 'Gazeta yoki jurnalda bosilgan yozma ish.', 'Maqola qiziqarli edi.'), ('hikmat', 'Chuqur maʼnoli donishmandlik fikri.', 'Hikmat insonni oʻylantiradi.'), ('fikr', 'Ongda tugʻilgan qarash yoki tushuncha.', 'Fikr ravshan boʻlishi kerak.'), ('maqsad', 'Erishmoqchi boʻlgan natija.', 'Maqsad yuksak boʻlsa, yoʻl topiladi.'), ('reja', 'Ishning oldindan belgilangan tartibi.', 'Reja tuzildi.'), ('natija', 'Ish yoki jarayon oqibati.', 'Natija quvonarli boʻldi.'), ('muammo', 'Hal etilishi lozim boʻlgan masala.', 'Muammo birgalikda yechildi.'), ('savol', 'Javob talab qiladigan gap yoki soʻrov.', 'Savol aniq berildi.'), ('javob', 'Savolga berilgan fikr.', 'Javob toʻgʻri chiqdi.'), ('masala', 'Yechilishi kerak boʻlgan topshiriq.', 'Masala murakkab edi.'), ('misol', 'Fikrni tushuntirish uchun keltirilgan holat.', 'Misol fikrni ochib berdi.'), ('qoida', 'Bajarilishi lozim boʻlgan tartib.', 'Qoida hammaga tushunarli boʻlishi kerak.'), ('xato', 'Notoʻgʻri bajarilgan ish yoki fikr.', 'Xato oʻz vaqtida tuzatildi.'), ('sabab', 'Voqeaning kelib chiqish asosi.', 'Sabab hali aniq emas.'), ('oqibat', 'Voqeadan keyin chiqqan natija.', 'Oqibat ogʻir boʻldi.'), ('salomatlik', 'Tananing sogʻlom holati.', 'Salomatlik eng katta boylik.'), ('kasallik', 'Salomatlikning buzilgan holati.', 'Kasallik tez tarqaldi.'), ('dori', 'Kasallikni davolash uchun moʻljallangan modda.', 'Dori ichildi.'), ('tabib', 'Anʼanaviy usulda davolovchi kishi.', 'Tabib giyoh bilan davoladi.'), ('bemor', 'Kasal kishi.', 'Bemor shifokor qabuliga keldi.'), ('yurak', 'Qonni haydovchi ichki aʼzo.', 'Yurak tinmay uradi.'), ('qoʻl', 'Odam tanasining yelkadan pastga qarab choʻzilgan aʼzosi.', 'Qoʻl bilan yozdim.'), ('oyoq', 'Odam tanasining yurish uchun xizmat qiladigan aʼzosi.', 'Oyoq charchadi.'), ('koʻz', 'Koʻrish aʼzosi.', 'Koʻz yorugʻlikni sezadi.'), ('quloq', 'Eshitish aʼzosi.', 'Quloq tovushni qabul qiladi.'), ('burun', 'Hid bilish aʼzosi.', 'Burun sovuqdan qizardi.'), ('ogʻiz', 'Ovqat qabul qilish va gapirish aʼzosi.', 'Ogʻiz ochilib qoldi.'), ('soch', 'Boshda oʻsadigan tuk.', 'Soch taralgan edi.'), ('bosh', 'Tananing yuqori qismi, kalla.', 'Bosh ogʻridi.'), ('barmoq', 'Qoʻl yoki oyoqning uchidagi uzun qism.', 'Barmoq yaralangan edi.'), ('tirnoq', 'Barmoq uchidagi shoxsimon qatlam.', 'Tirnoq oʻsib ketdi.'), ('tish', 'Ogʻizdagi ovqatni chaynaydigan qattiq aʼzo.', 'Tish ogʻrib qoldi.'), ('kiyim', 'Tanani oʻrab turuvchi liboslar.', 'Kiyim toza edi.'), ('koʻylak', 'Ustki kiyim turi.', 'Koʻylak oq rangda edi.'), ('shim', 'Beldan pastga kiyiladigan kiyim.', 'Shim yangi edi.'), ('etik', 'Oyoqni qoplab turuvchi poyabzal.', 'Etik quruq edi.'), ('doʻppi', 'Boshga kiyiladigan milliy kiyim.', 'Doʻppi naqshli edi.'), ('roʻmol', 'Boshga yoki boʻyinga oʻraladigan mato.', 'Roʻmol qizil rangda edi.'), ('chopon', 'Ustidan kiyiladigan milliy kiyim.', 'Chopon issiq edi.'), ('kamar', 'Belga bogʻlanadigan bogʻich.', 'Kamar mahkam bogʻlandi.'), ('qoʻlqop', 'Qoʻlga kiyiladigan buyum.', 'Qoʻlqop sovuqdan saqladi.'), ('paypoq', 'Oyoq kiyimi ostidan kiyiladigan buyum.', 'Paypoq yumshoq edi.'), ('karavot', 'Uxlash uchun moʻljallangan mebel.', 'Karavot xonaning burchagida turardi.'), ('yostiq', 'Uxlaganda bosh qoʻyiladigan yumshoq buyum.', 'Yostiq yumshoq edi.'), ('dasturxon', 'Ovqat yoyiladigan mato.', 'Dasturxon rang-barang taomlarga toʻldi.'), ('lagan', 'Ovqat solinadigan yirik idish.', 'Lagan palovga toʻla edi.'), ('piyola', 'Choy ichiladigan kichik idish.', 'Piyola issiq edi.'), ('qoshiq', 'Ovqat yeyishda ishlatiladigan asbob.', 'Qoshiq stol ustida turardi.'), ('pichoq', 'Kesish uchun moʻljallangan asbob.', 'Pichoq oʻtkir edi.'), ('choynak', 'Choy damlanadigan idish.', 'Choynak qaynab turardi.'), ('qozon', 'Katta ovqat pishirish idishi.', 'Qozon olovda turardi.'), ('tandir', 'Non yopiladigan loy oʻchoq.', 'Tandir qizib ketdi.')]
SIFAT_2 = [('yoqimli', 'Koʻngilga xush yoqadigan.', 'Yoqimli ovoz eshitildi.'), ('yoqimsiz', 'Koʻngilga yoqmaydigan.', 'Yoqimsiz hid taraldi.'), ('rangli', 'Turli ranglardan iborat.', 'Rangli gilam toʻshaldi.'), ('bejirim', 'Chiroyli va ozoda.', 'Bejirim hovli koʻzni quvontirdi.'), ('ozoda', 'Toza va saranjom.', 'Ozoda xona ochiq edi.'), ('pokiza', 'Ifloslanmagan, toza.', 'Pokiza suv ichdik.'), ('sermahsul', 'Mahsuli koʻp beradigan.', 'Sermahsul dala quvontirdi.'), ('unumdor', 'Hosil beradigan, samarali.', 'Unumdor yer yaxshi hosil berdi.'), ('serhosil', 'Hosili koʻp.', 'Serhosil bogʻ meva berdi.'), ('serquyosh', 'Quyoshi koʻp.', 'Serquyosh yurt mashhur.'), ('sersuv', 'Suvi koʻp, sersuv.', 'Sersuv meva yeyildi.'), ('kamsuv', 'Suvi kam.', 'Kamsuv yerda dehqonchilik qiyin.'), ('tiniq', 'Loyqasi yoʻq, shaffof.', 'Tiniq suv koʻrindi.'), ('loyqa', 'Tindirilmagan, tiniq emas.', 'Loyqa suv ichishga yaroqsiz.'), ('shaffof', 'Ichidan koʻrinib turadigan.', 'Shaffof shisha oldik.'), ('yaltiroq', 'Yaltirab turadigan.', 'Yaltiroq toshlar koʻzni oladi.'), ('xira', 'Nuri oʻchgan, tiniq emas.', 'Xira chiroq yonib turardi.'), ('sertuk', 'Tuki koʻp.', 'Sertuk mushuk yotibdi.'), ('shirali', 'Sersuv, mazali.', 'Shirali uzum pishdi.'), ('rostgoʻy', 'Haqiqatni gapiradigan.', 'Rostgoʻy bola hammaga yoqdi.'), ('yolgʻonchi', 'Yolgʻon gapirishga odatlangan.', 'Yolgʻonchi odam hurmat topmaydi.'), ('vafodor', 'Ahdiga sodiq, sadoqatli.', 'Vafodor doʻst hech qachon tashlab ketmaydi.'), ('xudbin', 'Faqat oʻzini oʻylaydigan.', 'Xudbin kishi boshqalarni hisobga olmaydi.'), ('ochiq', 'Yopilmagan; samimiy.', 'Ochiq deraza ostida oʻtirdik.'), ('yopiq', 'Berkitilgan, ochilmagan.', 'Yopiq eshik oldida kutdik.'), ('bekor', 'Foydasiz, ishsiz.', 'Bekor vaqt oʻtdi.'), ('tayyor', 'Ishga yoki harakatga shay.', 'Tayyor ovqat dasturxonga qoʻyildi.'), ('bexavotir', 'Xavfdan holi, xotirjam.', 'Bexavotir yoʻl bilan ketdik.'), ('xavfli', 'Zarar yetkazishi mumkin boʻlgan.', 'Xavfli yoʻldan yurmang.'), ('xotirjam', 'Tinch, bezovtalanmaydigan.', 'Xotirjam kayfiyat ishga yordam beradi.'), ('bezovta', 'Tinchligini yoʻqotgan, notinch.', 'Bezovta bola uxlolmadi.'), ('hayajonli', 'Hayajon uygʻotadigan.', 'Hayajonli daqiqalar boshlandi.'), ('qiziqarli', 'Qiziqish uygʻotadigan.', 'Qiziqarli kitob oʻqidim.'), ('zerikarli', 'Zerikish uygʻotadigan.', 'Zerikarli dars choʻzildi.'), ('fidoyi', 'Oʻz manfaatini oʻylamay xizmat qiladigan.', 'Fidoyi shifokor bemorlarni davoladi.'), ('vijdonli', 'Vijdoni toza, halol.', 'Vijdonli kishi aldamaydi.'), ('halol', 'Poklik bilan topilgan; poʻrtahol emas.', 'Halol mehnat shirin boʻladi.'), ('adolatli', 'Haqqoniy, toʻgʻri qaror qiladigan.', 'Adolatli sudya hukm chiqardi.'), ('shijoatli', 'Dadil, gʻayratli.', 'Shijoatli yigit oldinga intildi.'), ('gʻayratli', 'Ishga ishtiyoqli, shijoatli.', 'Gʻayratli talaba tez oʻrgandi.'), ('sabrli', 'Chidamli, sabr qiladigan.', 'Sabrli odam maqsadiga yetadi.'), ('chidamli', 'Qiyinchilikka bardosh beradigan.', 'Chidamli ot uzoq yoʻl bosdi.'), ('mustahkam', 'Puxta, qattiq turadigan.', 'Mustahkam devor qurildi.'), ('nozik', 'Yupqa, mayin; ehtiyot bilan muomala talab qiladigan.', 'Nozik shisha idish sinishi mumkin.'), ('pishiq', 'Chidamli, puxta.', 'Pishiq mato yirtilmadi.'), ('puxta', 'Mustahkam, har tomonlama oʻylangan.', 'Puxta reja tuzildi.'), ('sifatli', 'Sifati yuqori.', 'Sifatli mahsulot sotildi.'), ('arzimas', 'Ahamiyatsiz, juda kichik.', 'Arzimas gap uchun xafa boʻldi.'), ('ahamiyatli', 'Ahamiyati katta.', 'Ahamiyatli ish bajarildi.'), ('shoshqaloq', 'Tez shoshiladigan.', 'Shoshqaloq bola xato qildi.'), ('serharakat', 'Harakati koʻp, tinim bilmaydigan.', 'Serharakat bola bir joyda turmaydi.'), ('tinimsiz', 'Toʻxtovsiz, uzluksiz.', 'Tinimsiz mehnat meva beradi.'), ('abadiy', 'Hech qachon tugamaydigan.', 'Abadiy dostlik qoldi.'), ('vaqtinchalik', 'Qisqa muddatga moʻljallangan.', 'Vaqtinchalik yoʻl ochildi.'), ('doimiy', 'Uzluksiz, oʻzgarmas.', 'Doimiy ish topdi.'), ('tabiiy', 'Tabiatga xos, sunʼiy emas.', 'Tabiiy sharbat ichdik.'), ('sunʼiy', 'Inson yaratgan, tabiiy emas.', 'Sunʼiy gul stolda turardi.'), ('shaxsiy', 'Oʻziga tegishli.', 'Shaxsiy kitobxonamni koʻrsatdim.'), ('umumiy', 'Hammaga tegishli.', 'Umumiy maʼlumot berildi.'), ('alohida', 'Boshqalardan ajralgan.', 'Alohida xona ajratildi.')]
FEIL_2 = [('anglamoq', 'Mohiyatini fahmlab yetmoq.', 'U gapning maʼnosini angladi.'), ('fahmlamoq', 'Chuqur tushunmoq.', 'Ustoz shogirdning niyatini fahmladi.'), ('oʻqitmoq', 'Taʼlim bermoq, oʻrgatmoq.', 'Ustoz bolalarni oʻqitdi.'), ('tarbiyalamoq', 'Odob va xulq oʻrgatib voyaga yetkazmoq.', 'Ota-ona bolani tarbiyaladi.'), ('yaratmoq', 'Yangi narsani vujudga keltirmoq.', 'Shoir yangi dostonni yaratdi.'), ('rejalashtirmoq', 'Ishni oldindan tartibga solmoq.', 'Biz sayohatni rejalashtirdik.'), ('yakunlamoq', 'Ishni oxiriga yetkazmoq.', 'Ular loyihani yakunladi.'), ('jamlamoq', 'Bir joyga toʻplamoq.', 'Oʻquvchi maʼlumotlarni jamladi.'), ('saralamoq', 'Yaxshisini tanlab olmoq.', 'Dehqon uzumni saraladi.'), ('ajratmoq', 'Bir butundan alohida qilmoq.', 'U gapni boʻlaklarga ajratdi.'), ('birlashtirmoq', 'Bir necha narsani bir qilmoq.', 'Ular ikki jamoani birlashtirdi.'), ('bogʻlamoq', 'Ip yoki boshqa narsa bilan mahkamlamoq.', 'U arqonni daraxtga bogʻladi.'), ('yechmoq', 'Bogʻlangan narsani ochmoq; masalani hal etmoq.', 'Oʻquvchi masalani yechdi.'), ('burmoq', 'Yoʻnalishni oʻzgartirmoq; buramoq.', 'Haydovchi chapga burdi.'), ('aylanmoq', 'Doira boʻylab harakatlanmoq.', 'Yer Quyosh atrofida aylanadi.'), ('siljimoq', 'Joyidan sekin qoʻzgʻalmoq.', 'Mashina sekin siljidi.'), ('qoʻzgʻalmoq', 'Joyidan turmoq, harakatga kelmoq.', 'Karvon sahar vaqti qoʻzgʻaldi.'), ('yaqinlashmoq', 'Yaqinroq kelmoq.', 'Poyezd bekatga yaqinlashdi.'), ('uzoqlashmoq', 'Uzoqroq ketmoq.', 'Kema qirgʻoqdan uzoqlashdi.'), ('toʻplamoq', 'Bir joyga yigʻmoq.', 'Bolalar gul toʻpladi.'), ('tarqalmoq', 'Har tomonga yoyilib ketmoq.', 'Xabar tez tarqaldi.'), ('yoyilmoq', 'Keng sathga yastanmoq.', 'Dasturxon yoyildi.'), ('qichqirmoq', 'Baland ovozda baqirmoq.', 'Bola qichqirdi.'), ('baqirmoq', 'Qattiq ovoz chiqarmoq.', 'Odamlar baqirdi.'), ('shivirlamoq', 'Past ovozda gapirmoq.', 'U qulogʻiga shivirladi.'), ('pichirlamoq', 'Past tovushda soʻzlamoq.', 'Ular pichirlashdi.'), ('soʻzlamoq', 'Nutq aytmoq, gapirmoq.', 'Rais majlisda soʻzladi.'), ('tushuntirmoq', 'Mazmunini anglatmoq.', 'Ustoz qoidani tushuntirdi.'), ('izohlamoq', 'Maʼnosini tushuntirmoq.', 'U soʻzni izohladi.'), ('maqtamoq', 'Yaxshi tomonini aytib ulugʻlamoq.', 'Ustoz shogirdni maqtadi.'), ('koʻndirmoq', 'Rozi qilmoq.', 'U otasini koʻndirdi.'), ('ishontirmoq', 'Ishonch hosil qildirmoq.', 'U doʻstini ishontirdi.'), ('ogohlantirmoq', 'Xavfdan oldindan xabar bermoq.', 'Haydovchi yoʻlovchini ogohlantirdi.'), ('yordamlashmoq', 'Bir-biriga koʻmak bermoq.', 'Qoʻshnilar yordamlashdi.'), ('qoʻllamoq', 'Foydalanmoq, ishlatmoq.', 'U yangi usulni qoʻlladi.'), ('ishlatmoq', 'Biror ish uchun foydalanmoq.', 'Usta bolgʻani ishlatdi.'), ('foydalanmoq', 'Biror narsadan naf koʻrmoq.', 'Talaba kutubxonadan foydalandi.'), ('sarflamoq', 'Pul yoki vaqtni ishlatib tugatmoq.', 'U vaqtini behuda sarfladi.'), ('tejamoq', 'Ehtiyotkorlik bilan sarflamoq.', 'Oila mablagʻni tejadi.'), ('toʻlamoq', 'Qarz yoki xizmat haqini bermoq.', 'U qarzni toʻladi.'), ('ayirboshlamoq', 'Bir narsani boshqasiga almashtirmoq.', 'Bolalar kartochka ayirboshladi.'), ('almashtirmoq', 'Birini oʻrniga boshqasini qoʻymoq.', 'U eski kitobni yangisiga almashtirdi.'), ('yangilamoq', 'Yangi holga keltirmoq.', 'Ustalar binoni yangiladi.'), ('taʼmirlamoq', 'Buzilgan narsani tuzatmoq.', 'Usta soatni taʼmirladi.'), ('tuzatmoq', 'Xatoni toʻgʻrilamoq.', 'U yozuvdagi xatoni tuzatdi.'), ('buzmoq', 'Yaroqsiz holga keltirmoq.', 'Bola oʻyinchoqni buzdi.'), ('qazimoq', 'Yerni kovlab chuqur hosil qilmoq.', 'Ular quduq qazidi.'), ('kovlamoq', 'Yerni agʻdarmoq.', 'Dehqon yerni kovladi.'), ('oʻrmoq', 'Oʻroq bilan kesib yigʻmoq.', 'Dehqonlar bugʻdoyni oʻrdi.'), ('yanchmoq', 'Mayda qilib maydalamoq.', 'Ayol donni yanchdi.'), ('yopishmoq', 'Bir narsaga yopishib qolmoq.', 'Gilam polga yopishdi.'), ('osmoq', 'Biror narsaga ilib qoʻymoq.', 'U kiyimni ilgakka osdi.'), ('ilmoq', 'Ilgakka tushirmoq.', 'Soatni devorga ildi.'), ('silamoq', 'Yengil qoʻl tekkizib erkalamoq.', 'Ona bolaning sochini siladi.'), ('quchmoq', 'Qoʻllari bilan oʻramoq.', 'Ota bolani quchdi.'), ('oʻpmoq', 'Lab bilan mehr bildirmoq.', 'Ona farzandining peshonasidan oʻpdi.'), ('sevindirmoq', 'Quvontirmoq.', 'Sovgʻa bolalarni sevindirdi.'), ('gʻazablanmoq', 'Qattiq jahli chiqmoq.', 'Kishi gʻazablandi.'), ('jahllanmoq', 'Jahli chiqmoq.', 'U jahllandi.'), ('tinchlanmoq', 'Xotirjam boʻlmoq.', 'Bola tinchlandi.'), ('hayajonlanmoq', 'Qattiq his qilmoq.', 'Toʻy kuni kelin hayajonlandi.'), ('intilmoq', 'Biror narsaga erishishga harakat qilmoq.', 'U yuksak maqsadga intildi.'), ('erishmoq', 'Maqsadga yetmoq.', 'U gʻalabaga erishdi.')]
SON_2 = [('yarimta', 'Kasr son: butunning yarmi.', 'Yarimta non qoldi.'), ('ikkitacha', 'Taxminiy son: taxminan ikki dona.', 'Ikkitacha olma qoldi.'), ('uchtacha', 'Taxminiy son: taxminan uch dona.', 'Uchtacha qalam yetadi.'), ('oʻntacha', 'Taxminiy son: taxminan oʻn dona.', 'Oʻntacha kitob oldim.'), ('yigirmatacha', 'Taxminiy son: taxminan yigirma dona.', 'Yigirmatacha bola keldi.'), ('sakkizov', 'Jamlovchi son: sakkiz kishining birgalikda ekanini bildiradi.', 'Sakkizov yoʻlga chiqdi.'), ('toʻqqizov', 'Jamlovchi son: toʻqqiz kishining birgalikda ekanini bildiradi.', 'Toʻqqizov uyga qaytdi.'), ('oʻnov', 'Jamlovchi son: oʻn kishining birgalikda ekanini bildiradi.', 'Oʻnov safga turdi.'), ('oʻttizinchi', 'Tartib son: sanoqda 30-oʻrindagi.', 'Oʻttizinchi kun yetib keldi.'), ('ellikinchi', 'Tartib son: sanoqda 50-oʻrindagi.', 'Ellikinchi sahifani oʻqidim.'), ('mingta', 'Dona son: narsalarning ming dona ekanini bildiradi.', 'Mingta kitob sotildi.'), ('yuzta', 'Dona son: narsalarning yuz dona ekanini bildiradi.', 'Yuzta daraxt ekildi.'), ('ellikta', 'Dona son: narsalarning ellik dona ekanini bildiradi.', 'Ellikta bola qatnashdi.'), ('oʻttizta', 'Dona son: narsalarning oʻttiz dona ekanini bildiradi.', 'Oʻttizta stul keltirildi.')]
OLMOSH_2 = [('kimlar', 'Soʻroq olmoshi: bir necha shaxsni soʻraydi.', 'Kimlar keldi?'), ('nimalar', 'Soʻroq olmoshi: bir necha narsani soʻraydi.', 'Nimalar sotib oldingiz?'), ('qaysilar', 'Soʻroq olmoshi: bir necha narsadan koʻpini soʻraydi.', 'Qaysilar kelishdi?'), ('qanaqa', 'Soʻroq olmoshi: belgi-xususiyatni soʻraydi.', 'Qanaqa kitob olding?'), ('necha', 'Soʻroq olmoshi: miqdorni soʻraydi.', 'Necha kishi keldi?'), ('nechanchi', 'Soʻroq olmoshi: tartibni soʻraydi.', 'Nechanchi sinfda oʻqiysan?'), ('hech qaysi', 'Boʻlishsizlik olmoshi: birorta ham narsani bildirmaydi.', 'Hech qaysi kitob menga yoqmadi.'), ('har qaysi', 'Belgilash olmoshi: har bir narsani bildiradi.', 'Har qaysi bola oʻz ishini bildi.'), ('hech qanday', 'Boʻlishsizlik olmoshi: belgisi yoʻqligini bildiradi.', 'Hech qanday gap yoʻq.'), ('falon', 'Gumon olmoshi: nomaʼlum shaxs yoki narsani bildiradi.', 'Falon kishi keldi.'), ('fulon', 'Gumon olmoshi: nomaʼlum shaxsni bildiradi.', 'Fulon joyga bordim.')]
RAVISH_2 = [('sekingina', 'Tarz: juda sekin, ohista.', 'U sekingina yurib ketdi.'), ('keskin', 'Tarz: tez va qatʼiy.', 'U keskin burildi.'), ('toʻsatdan', 'Payt: kutilmaganda.', 'Toʻsatdan yomgʻir yogʻdi.'), ('barvaqt', 'Payt: erta, vaqtidan oldin.', 'U barvaqt turdi.'), ('kechroq', 'Payt: odatdagidan kech.', 'Kechroq keling.'), ('oldinroq', 'Payt: oldinroq.', 'Oldinroq chiqdim.'), ('tezroq', 'Tarz: tezlikni oshirib.', 'Tezroq yuring.'), ('sekinroq', 'Tarz: tezlikni kamaytirib.', 'Sekinroq gapiring.'), ('benihoya', 'Daraja: juda, haddan ortiq.', 'U benihoya xursand edi.'), ('anchagina', 'Miqdor: ancha koʻp.', 'Anchagina vaqt oʻtdi.'), ('jiqqa', 'Miqdor: toʻla, toʻlib-toshgan.', 'Zal jiqqa odamga toʻldi.'), ('rosa', 'Daraja: yaxshigina, ancha.', 'U rosa charchadi.'), ('birgalashib', 'Tarz: hamkorlikda.', 'Biz birgalashib ishladik.'), ('ochiqchasiga', 'Tarz: yashirmasdan.', 'U ochiqchasiga gapirdi.'), ('beixtiyor', 'Tarz: ixtiyorsiz.', 'U beixtiyor kulib yubordi.'), ('istar-istamas', 'Tarz: ixtiyoriy emas, noxohish bilan.', 'U istar-istamas rozi boʻldi.'), ('shosha-pisha', 'Tarz: ayrim shoshilib.', 'U shosha-pisha kiyindi.'), ('hozirgina', 'Payt: shu zahotiyoq.', 'U hozirgina ketdi.'), ('yaqinda', 'Payt: oz vaqt avval yoki keyin.', 'Yaqinda yangi kitob chiqadi.'), ('ilgari', 'Payt: avvalroq, oldin.', 'Ilgari bu yerda bogʻ bor edi.'), ('keyinroq', 'Payt: kechroq.', 'Keyinroq gaplashamiz.'), ('nari', 'Oʻrin: uzoqroq tomonda.', 'Nari turing.'), ('hamon', 'Payt: hali ham, hanuz.', 'U hamon kutmoqda.'), ('hanuzgacha', 'Payt: hozirgacha.', 'Hanuzgacha xabar kelmadi.')]
KOMAKCHI_2 = [('yoʻsinida', 'Usul, yoʻsin maʼnosini bildiradi.', 'Eski odat yoʻsinida ish koʻrildi.'), ('jihatidan', 'Nuqtai nazarni bildiradi.', 'Sifat jihatidan bu yaxshi.'), ('barobar', 'Birgalik yoki bir vaqtlilikni bildiradi.', 'Quyosh chiqishi barobar yoʻlga chiqdik.'), ('qarshi', 'Qarama-qarshilik maʼnosini bildiradi.', 'Shamolga qarshi yurdik.'), ('muvofiq', 'Moslik maʼnosini bildiradi.', 'Reja muvofiq bajarildi.'), ('qaramasdan', 'Qarshilik maʼnosini bildiradi.', 'Yomgʻirga qaramasdan chiqdik.')]
BOGLOVCHI_2 = [('shu bois', 'Natija bogʻlovchisi: natijani bildiradi.', 'U kasal edi, shu bois kelmadi.'), ('shunday boʻlsa-da', 'Qarshilik bogʻlovchisi: qarama-qarshilikka qaramay.', 'Havo sovuq, shunday boʻlsa-da biz chiqdik.'), ('bordiyu', 'Shart bogʻlovchisi: kam ehtimolli shartni bildiradi.', 'Bordiyu kelmasangiz, xabar bering.'), ('shuningdek', 'Biriktiruvchi bogʻlovchi: qoʻshimcha maʼno beradi.', 'Kitob, shuningdek daftar ham oldim.')]
YUKLAMA_2 = [('hech boʻlmasa', 'Cheklash yuklamasi: eng kamini bildiradi.', 'Hech boʻlmasa, bir daqiqa tinglang.'), ('hattoki', 'Kuchaytirish yuklamasi: kutilmagan holatni bildiradi.', 'Hattoki bolalar ham bildi.'), ('-ov', 'Kuchaytirish yuklamasi: taʼkid bildiradi.', 'Kelasan-ov, kelmasan.'), ('-yu', 'Kuchaytirish yuklamasi: taʼkid beradi.', 'U keldi-yu, hammasi oʻzgardi.'), ('-ya', 'Soʻroq-taʼkid yuklamasi: tasdiq soʻraydi.', 'Oʻzing-ya?')]
UNDOV_2 = [('ehh', 'Charchoq yoki norozilikni bildiradi.', 'Ehh, yana kech qoldim.'), ('hoy-hoy', 'Birovni toʻxtatish uchun ishlatiladi.', 'Hoy-hoy, toʻxtang!'), ('hayda', 'Hayvonni yoki odamni yurishga undaydi.', 'Hayda, tezroq yur!'), ('chuh', 'Otni yurishga undaydi.', 'Chuh, ot yur!'), ('yasha', 'Maqtov yoki tantana bildiradi.', 'Yasha, gʻalaba bizniki!'), ('rahmat', 'Minnatdorchilik bildiradi.', 'Rahmat, yordamingiz uchun.'), ('xayr', 'Vidolashuvni bildiradi.', 'Xayr, ertagacha!'), ('salom', 'Salomlashishni bildiradi.', 'Salom, qalaysiz?'), ('kechirasiz', 'Uzr soʻrashni bildiradi.', 'Kechirasiz, bu joy bandmi?'), ('assalom', 'Salomlashishni bildiradi.', 'Assalom, aziz mehmonlar!'), ('vovey', 'Qoʻrquv yoki ajablanishni bildiradi.', 'Vovey, nima boʻldi bu?'), ('boh-boh', 'Hayrat va zavqni bildiradi.', 'Boh-boh, naqadar mazali!'), ('xoʻp', 'Rozilikni bildiradi.', 'Xoʻp, boraman.')]
MODAL_2 = [('aniqki', 'Ishonch bildiradi.', 'Aniqki, u kelmaydi.'), ('ochigʻi', 'Samimiylikni bildiradi.', 'Ochigʻi, men bilmayman.'), ('toʻgʻrisi', 'Samimiy fikr bildiradi.', 'Toʻgʻrisi, u menga yoqmadi.'), ('ehtimolki', 'Taxmin bildiradi.', 'Ehtimolki, u kech qoladi.'), ('maʼlumki', 'Hammaga maʼlum fikrni bildiradi.', 'Maʼlumki, Vatan hammaga aziz.'), ('yoʻq', 'Inkorni bildiradi.', 'Yoʻq, men bormayman.'), ('ha', 'Tasdiqni bildiradi.', 'Ha, men boraman.')]
TAQLID_2 = [('shivir', 'Past ovozli shivirlashga taqlid.', 'Shamol shivir ovoz bilan esdi.'), ('gʻurr-gʻurr', 'Uchib ketayotgan parrandalar qanotiga taqlid.', 'Kaptarlar gʻurr-gʻurr uchib ketdi.'), ('shaqir-shuqur', 'Mayda narsalar bir-biriga urilishiga taqlid.', 'Qoʻngʻiroq shaqir-shuqur jiringladi.'), ('jiring-jiring', 'Qoʻngʻiroq tovushiga taqlid.', 'Qoʻngʻiroq jiring-jiring qildi.'), ('dangʻir-dungʻur', 'Gʻildirak yoki bochka shovqiniga taqlid.', 'Aravada dangʻir-dungʻur ovoz eshitildi.'), ('shaldir-shuldir', 'Suvning tez oqishiga taqlid.', 'Daryo shaldir-shuldir oqardi.'), ('charaq-charaq', 'Chaqmoq yoki yonayotgan quruq oʻt tovushiga taqlid.', 'Olov charaq-charaq yonardi.'), ('hapir-hapir', 'Tez-tez nafas olishga taqlid.', 'Bola hapir-hapir nafas oldi.'), ('gur-gur', 'Qaynayotgan suv yoki uzoq gumburlashga taqlid.', 'Choynak gur-gur qaynadi.'), ('vijir-vijir', 'Hasharotlarning shovqiniga taqlid.', 'Kechasi vijir-vijir ovozi eshitildi.'), ('chirq-chirq', 'Chirqillab qichqirgan qush ovoziga taqlid.', 'Chumchuq chirq-chirq qildi.'), ('chirt-chirt', 'Qaychi yoki mayda zarbaga taqlid.', 'Qaychi chirt-chirt kesdi.'), ('lapang-lapang', 'Yengil, sekin yurishga taqlid.', 'Ot lapang-lapang kela boshladi.')]
ATAMALAR_2 = [('tovush oʻzgarishi', 'Soʻz tarkibida tovushlarning bir-biriga taʼsiri bilan oʻzgarishi.', 'Tovush oʻzgarishi nutqda kuzatiladi.'), ('unli tovush tushishi', 'Soʻzga qoʻshimcha qoʻshilganda unlining tushib qolishi.', 'Oʻgʻil — oʻgʻlim: unli tushishi.'), ('tovush ortishi', 'Soʻzga qoʻshimcha qoʻshilganda yangi tovush paydo boʻlishi.', 'Tovush ortishi koʻp uchraydi.'), ('bosh harf', 'Gapning boshida va atoqli otlarda yoziladigan katta harf.', 'Toshkent — bosh harf bilan yoziladi.'), ('apostrof', 'Tutuq belgisi sifatida ishlatiladigan yozuv belgisi.', 'Apostrof soʻzda tutuqni bildiradi.'), ('yozuv', 'Tilni harf belgilari orqali ifodalash tizimi.', 'Yozuv til tarixida muhim oʻrin tutadi.'), ('kirill yozuvi', 'Rus alifbosiga asoslangan yozuv tizimi.', 'Kirill yozuvi bir davr ishlatilgan.'), ('lotin yozuvi', 'Lotin alifbosiga asoslangan yozuv tizimi.', 'Hozirgi oʻzbek yozuvi lotin yozuvida.'), ('soʻz boʻgʻini', 'Soʻzning bir nafasda aytiladigan qismi.', 'Soʻz boʻgʻini unli atrofida tuziladi.'), ('koʻchirish', 'Soʻzni qatordan qatorga boʻgʻin boʻyicha oʻtkazish qoidasi.', 'Koʻchirishda boʻgʻin buzilmasligi kerak.'), ('oʻzak soʻz', 'Qoʻshimcha olmagan, bir oʻzakdan iborat soʻz.', 'Kitob — oʻzak soʻz.'), ('yasama soʻz', 'Soʻz yasovchi qoʻshimcha bilan hosil qilingan soʻz.', 'Ishchi — yasama soʻz.'), ('qoʻshma otlar', 'Ikki soʻzdan tuzilgan yangi ot.', 'Gulkaram — qoʻshma ot.'), ('juft otlar', 'Ikki ot juftlanib bitta tushunchani bildiradi.', 'Ota-ona — juft ot.'), ('takroriy otlar', 'Soʻzning takrorlanishi bilan hosil boʻlgan ot.', 'Uy-uy takroriy ot.'), ('atoqli ot', 'Yakka narsa yoki shaxsning nomini bildiruvchi ot.', 'Alisher, Toshkent — atoqli otlar.'), ('turdosh ot', 'Bir turdagi narsalarning umumiy nomini bildiruvchi ot.', 'Kitob, shahar — turdosh otlar.'), ('shaxs', 'Gapda kim tomonidan ish bajarilishini koʻrsatuvchi grammatik shakl.', 'Shaxs I, II, III boʻladi.'), ('birlik va koʻplik', 'Narsa yoki shaxsning bitta yoki bir nechta ekanini bildiruvchi grammatik shakl.', 'Kitob — birlik, kitoblar — koʻplik.'), ('sifat darajasi', 'Belgining kuchi yoki zaifligini bildiruvchi shakl.', 'Sifat darajasi uchta boʻladi.'), ('oddiy daraja', 'Belgi qiyoslanmay, oʻz holicha berilgan sifat darajasi.', 'Katta — oddiy daraja.'), ('qiyosiy daraja', 'Belgi boshqasidan koʻproq yoki kamroq ekanini bildiruvchi daraja.', 'Kattaroq — qiyosiy daraja.'), ('orttirma daraja', 'Belgi eng yuqori ekanini bildiruvchi daraja.', 'Eng katta — orttirma daraja.'), ('sanoq son', 'Narsaning miqdorini bildiruvchi son.', 'Uch, besh — sanoq sonlar.'), ('tartib son', 'Narsaning tartibini bildiruvchi son.', 'Uchinchi — tartib son.'), ('dona son', 'Narsaning dona ekanini bildiruvchi son.', 'Beshta — dona son.'), ('kasr son', 'Butunning qismini bildiruvchi son.', 'Yarim — kasr son.'), ('taxminiy son', 'Aniq boʻlmagan miqdorni bildiruvchi son.', 'Oʻnlab — taxminiy son.'), ('jamlovchi son', 'Kishilar jamlanganini bildiruvchi son.', 'Ikkov — jamlovchi son.'), ('kishilik olmoshi', 'Shaxs oʻrnida qoʻllanuvchi olmosh.', 'Men, sen, u — kishilik olmoshlari.'), ('koʻrsatish olmoshi', 'Narsani koʻrsatuvchi olmosh.', 'Bu, shu — koʻrsatish olmoshlari.'), ('soʻroq olmoshi', 'Savol bildiruvchi olmosh.', 'Kim, nima — soʻroq olmoshlari.'), ('belgilash olmoshi', 'Narsani qamrab olish yoki ajratib koʻrsatish maʼnosini bildiruvchi olmosh.', 'Hamma, barcha — belgilash olmoshlari.'), ('oʻzlik olmoshi', 'Oʻzini bildiruvchi olmosh.', 'Oʻzim, oʻzing — oʻzlik olmoshlari.'), ('gumon olmoshi', 'Noaniqlik bildiruvchi olmosh.', 'Kimdir, nimadir — gumon olmoshlari.'), ('boʻlishsizlik olmoshi', 'Inkor maʼnosini bildiruvchi olmosh.', 'Hech kim, hech narsa — boʻlishsizlik olmoshlari.'), ('sifatdosh shakli', 'Feʼlning sifat vazifasini bajaruvchi shakli.', 'Kelgan odam — sifatdosh shakli.'), ('ravishdosh shakli', 'Feʼlning ravish vazifasini bajaruvchi shakli.', 'Kulib gapirdi — ravishdosh shakli.'), ('harakat nomi shakli', 'Feʼlning ot vazifasidagi shakli.', 'Yozmoq — harakat nomi.'), ('ravish turlari', 'Ravishlarning maʼnosiga koʻra guruhlari.', 'Payt, tarz, oʻrin, miqdor ravishlari mavjud.'), ('payt ravishi', 'Harakatning vaqtini bildiruvchi ravish.', 'Bugun, ertaga — payt ravishlari.'), ('tarz ravishi', 'Harakatning qanday bajarilishini bildiruvchi ravish.', 'Tez, sekin — tarz ravishlari.'), ('oʻrin ravishi', 'Harakatning joyini bildiruvchi ravish.', 'Yuqorida, pastda — oʻrin ravishlari.'), ('miqdor ravishi', 'Harakatning miqdor yoki darajasini bildiruvchi ravish.', 'Juda, ancha — miqdor ravishlari.'), ('ega ifodalanishi', 'Gapda eganing qaysi soʻz turkumi bilan ifodalanishi.', 'Ega ot yoki olmosh bilan ifodalanadi.'), ('kesim ifodalanishi', 'Gapda kesimning qaysi soʻz turkumi bilan ifodalanishi.', 'Kesim koʻpincha feʼl bilan ifodalanadi.'), ('toʻldiruvchi turlari', 'Vositasiz va vositali toʻldiruvchilar.', 'Kitobni oʻqidi — vositasiz toʻldiruvchi.'), ('hol turlari', 'Payt, oʻrin, tarz, sabab, maqsad, miqdor-daraja holi.', 'Hol turlari soʻroqlariga koʻra farqlanadi.'), ('aniqlovchi turlari', 'Sifatlovchi va qaratqich aniqlovchilar.', 'Chiroyli gul — sifatlovchi aniqlovchi.'), ('sifatlovchi aniqlovchi', 'Narsaning belgisini bildiruvchi aniqlovchi.', 'Katta uy — sifatlovchi aniqlovchi.'), ('qaratqich aniqlovchi', 'Narsaning kimga tegishli ekanini bildiruvchi aniqlovchi.', 'Onamning kitobi — qaratqich aniqlovchi.'), ('tenglanuvchi qoʻshma gap', 'Qismlari teng huquqli boʻlgan qoʻshma gap.', 'Yomgʻir yogʻdi va shamol esdi.'), ('shart ergash gap', 'Bosh gapning bajarilish shartini bildiruvchi ergash gap.', 'Agar oʻqisang, bilasan.'), ('sabab ergash gap', 'Bosh gapning sababini bildiruvchi ergash gap.', 'U kelmadi, chunki kasal edi.'), ('payt ergash gap', 'Bosh gapning vaqtini bildiruvchi ergash gap.', 'Men kelganda, u ketgan edi.'), ('maqsad ergash gap', 'Bosh gapning maqsadini bildiruvchi ergash gap.', 'Oʻqidim, toki bilim olay.'), ('toʻgʻri nutq', 'Birovning gapi aynan keltirilgan nutq.', 'U: «Men boraman», — dedi.'), ('koʻchirma gap', 'Muallif gapi va koʻchirilgan gapdan tuzilgan gap.', 'Ali: «Men boraman», — dedi.'), ('muallif gapi', 'Koʻchirma gapda gapni keltiruvchi qism.', 'Ali dedi: «Boraman».'), ('ajratilgan oʻzlashtirma', 'Gapda soʻz birikmasi shaklida ajratilgan boʻlak.', 'Ajratilgan boʻlak vergul bilan ajratiladi.'), ('tinish belgisi turlari', 'Nuqta, vergul, undov, soʻroq va boshqa belgilar.', 'Tinish belgilari yozuvda zarur.'), ('tire', 'Ega va kesim orasida yoki juft soʻzlarda qoʻyiladigan belgi.', 'Tire gapda muhim belgi.'), ('ikki nuqta', 'Sanash yoki izohlashdan oldin qoʻyiladigan belgi.', 'Ikki nuqta sanoqdan oldin yoziladi.'), ('qavs', 'Izoh yoki qoʻshimcha fikrni ajratib koʻrsatuvchi belgi.', 'Qavs ichida izoh beriladi.')]
ADABIY_2 = [('ballada', 'Sheʼriy shakldagi hikoyali asar.', 'Ballada tarixiy voqeani aytib beradi.'), ('poema', 'Katta hajmli lirik-epik sheʼriy asar.', 'Poema Vatan haqida yozilgan.'), ('sonet', 'Oʻn toʻrt qatordan iborat sheʼriy shakl.', 'Sonet shoir mahoratini koʻrsatadi.'), ('elegiya', 'Gʻamgin kechinmalar ifodalangan sheʼriy asar.', 'Elegiya ayriliq haqida.'), ('ode', 'Ulugʻlash, maqtov mazmunidagi sheʼriy asar.', 'Ode Vatan ulugʻlanadi.'), ('epigramma', 'Qisqa, oʻtkir kinoyali sheʼriy asar.', 'Epigramma bir necha misra.'), ('remarka', 'Pesada muallifning izohi.', 'Remarka sahna harakatini bildiradi.'), ('sahna', 'Spektakl koʻrsatiladigan joy.', 'Sahna yoritildi.'), ('pesa', 'Sahna uchun yozilgan dramatik asar.', 'Pesa uch pardadan iborat.'), ('parda', 'Spektaklning boʻlimi.', 'Parda yopildi.'), ('rejissyor', 'Spektakl yoki filmni sahnalashtiruvchi shaxs.', 'Rejissyor aktyorlarga yoʻnalish berdi.'), ('aktyor', 'Sahna yoki kinoda rol ijro etuvchi shaxs.', 'Aktyor rolni mahorat bilan ijro etdi.'), ('tomoshabin', 'Spektakl yoki filmni koʻruvchi shaxs.', 'Tomoshabin qarsak chaldi.'), ('ssenariy', 'Film yoki sahna asarining yozma matni.', 'Ssenariy tayyor boʻldi.'), ('adabiy qahramon', 'Asardagi asosiy ishtirokchi obraz.', 'Adabiy qahramon oʻquvchi qalbida qoladi.'), ('ijobiy qahramon', 'Asarda yaxshi sifatlar bilan tasvirlangan obraz.', 'Ijobiy qahramon adolat uchun kurashadi.'), ('salbiy qahramon', 'Asarda yomon xislatlar bilan tasvirlangan obraz.', 'Salbiy qahramon jazolanadi.'), ('xarakter', 'Qahramonning ichki fazilatlari majmuasi.', 'Xarakter harakatlarida koʻrinadi.'), ('konflikt', 'Asarda qarama-qarshi kuchlarning toʻqnashuvi.', 'Konflikt voqealarni harakatga keltiradi.'), ('ziddiyat', 'Qarama-qarshi fikr yoki manfaatlarning toʻqnashuvi.', 'Ziddiyat avjiga chiqdi.'), ('voqea', 'Asarda yuz bergan hodisa.', 'Voqea qishloqda boʻlib oʻtdi.'), ('xotima', 'Asarning yakuniy qismi.', 'Xotima oʻquvchini oʻylantirdi.'), ('sarlavha', 'Asarning nomi.', 'Sarlavha mavzuni anglatadi.'), ('annotatsiya', 'Asarning qisqa mazmuni.', 'Annotatsiya kitob orqasida yozilgan.'), ('taqriz', 'Asar haqida yozilgan baho.', 'Taqriz asarning kuchli tomonlarini koʻrsatdi.'), ('adabiyotshunos', 'Adabiyotni ilmiy oʻrganuvchi mutaxassis.', 'Adabiyotshunos asarni tahlil qildi.'), ('nashr', 'Bosilib chiqarilgan kitob yoki jurnal.', 'Nashr katta tirajda chiqdi.')]
BADIIY_2 = [('anbar', 'Xushboʻy modda; sochning hidiga ishora (sheʼriy nutqda).', 'Anbar hidi taraldi.'), ('anjuman', 'Yigʻin, davra.', 'Anjuman shoirlar bilan boy edi.'), ('ashk', 'Koʻz yoshi.', 'Ashk tomchiladi.'), ('ayriliq', 'Sevgan inson bilan judo boʻlish.', 'Ayriliq dard keltirdi.'), ('bedor', 'Uygʻoq.', 'Bedor tun dardga toʻla edi.'), ('bevafo', 'Sadoqatsiz.', 'Bevafo yor yuz oʻgirdi.'), ('bexabar', 'Xabarsiz, bilmaydigan.', 'Bexabar odam hech narsani bilmasdi.'), ('diydor', 'Koʻrishuv, uchrashuv.', 'Diydor lazzatini totdi.'), ('dard', 'Ruhiy yoki jismoniy azob.', 'Dard yuragini ezdi.'), ('farishta', 'Nur va yaxshilik timsoli boʻlgan goʻzal obraz.', 'Farishta kabi qiz edi.'), ('gardish', 'Hayotdagi oʻzgarish, aylanish.', 'Gardish zamona gʻalayoni.'), ('gulchehra', 'Yuzi gul kabi goʻzal.', 'Gulchehra qiz bogʻda yurdi.'), ('huzur', 'Orom, farogʻat.', 'Huzur qilib dam oldi.'), ('kamolot', 'Yetuklik, mukammallik.', 'Kamolot yoʻli uzoq.'), ('lahza', 'Qisqa vaqt, damlar.', 'Lahza ichida hammasi oʻzgardi.'), ('lavha', 'Manzara, qisqa tasvir.', 'Lavha esdan chiqmaydi.'), ('mayin', 'Yumshoq, yoqimli.', 'Mayin shabada esdi.'), ('mehrob', 'Masjid yoki bino devoridagi egilgan nish.', 'Mehrob naqshlar bilan bezatilgan.'), ('mubtalo', 'Biror narsaga yoʻliqqan, ishqida oʻrtangan.', 'Mubtalo boʻlib qoldi.'), ('nigor', 'Goʻzal, suyukli.', 'Nigor sevgisi yuragida edi.'), ('nur', 'Yorugʻlik.', 'Nur xonaga toʻldi.'), ('oromijon', 'Orom beruvchi, jon orom.', 'Oromijon farzand.'), ('parvona', 'Shamga oʻzini urib oʻladigan kapalak; sodiq oshiq timsoli.', 'Parvona shamga intildi.'), ('pari', 'Ertaklardagi goʻzal xayoliy mavjudot.', 'Pari qanotlari yaltirardi.'), ('rashk', 'Rashkchilik, kuyish tuygʻusi.', 'Rashk qalbini kuydirdi.'), ('sabohat', 'Goʻzallik, porloqlik.', 'Sabohat uning yuzida.'), ('sarxush', 'Oʻziga kelmagan, mast.', 'Sarxush holda yurdi.'), ('sayqal', 'Silliqlash, jilo berish.', 'Sayqal soʻzga jilo berdi.'), ('tabassum', 'Mayin kulgi.', 'Tabassum yuziga yoyildi.'), ('tafakkur', 'Chuqur oʻylash.', 'Tafakkur odamni ulugʻlaydi.'), ('zavq', 'Quvonch, huzur.', 'Zavq bilan kuyladi.'), ('zamona', 'Zamon, davr.', 'Zamona sinovlari qiyin edi.'), ('zarra', 'Eng mayda zarrachasi.', 'Zarra toʻpiq bilan quyoshni koʻrdi.'), ('ziyo', 'Nur, yorugʻlik, maʼrifat.', 'Ziyo bilim bilan keladi.')]
FRAZEO_2 = [('qoʻli gul', 'Mohir, usta.', 'Bizning ustoz qoʻli gul inson.'), ('koʻngli ochiq', 'Samimiy, ochiq kishi.', 'Koʻngli ochiq inson hammaga yoqadi.'), ('koʻzi ochiq', 'Bilimli, hushyor.', 'Koʻzi ochiq yigit tezda tushundi.'), ('koʻzi toʻq', 'Ochkoʻz emas, qanoatli.', 'Koʻzi toʻq odam boshqa narsaga intilmaydi.'), ('burni baland', 'Oʻzini baland tutadigan, kibrli.', 'U burni baland, hammani mensimaydi.'), ('tili uzun', 'Koʻp gapiradigan, ortiqcha gapga usta.', 'Tili uzun odam sirni saqlamaydi.'), ('tili chiqmoq', 'Gapirishga boshlamoq (bolalar haqida).', 'Chaqaloqning tili chiqdi.'), ('tili boʻgʻilmoq', 'Gapirolmay qolmoq.', 'Hayajondan tili boʻgʻildi.'), ('ogʻzi quloqda', 'Juda xursand.', 'Sovgʻani olib ogʻzi quloqda boʻldi.'), ('yuragi qinidan chiqmoq', 'Qattiq qoʻrqmoq.', 'Dahshatdan yuragi qinidan chiqayozdi.'), ('yuragi toʻlmoq', 'Hayajonlanmoq, yigʻlamsiramoq.', 'Soʻzlaganda yuragi toʻldi.'), ('dili siyoh', 'Xafa, ranjigan.', 'Gapdan dili siyoh boʻldi.'), ('bagʻri kuymoq', 'Juda achinmoq.', 'Farzandi uchun bagʻri kuydi.'), ('boshi osmonga yetmoq', 'Juda xursand boʻlmoq.', 'Gʻalabadan boshi osmonga yetdi.'), ('boshi qotmoq', 'Chigal masalaga duch kelmoq.', 'Masaladan boshi qotdi.'), ('boshini egmoq', 'Hurmat yoki uyat bilan taʼzim qilmoq.', 'Ustoz oldida boshini egdi.'), ('qoʻl uzatmoq', 'Yordam bermoq.', 'Ahvoli ogʻir kishiga qoʻl uzatdi.'), ('qoʻl qovushtirmoq', 'Hech ish qilmay turmoq.', 'U qoʻl qovushtirib oʻtirmadi.'), ('qoʻl koʻtarmoq', 'Rozilik bildirmoq; urishga chogʻlanmoq.', 'Hamma qoʻl koʻtardi.'), ('etak yoymoq', 'Yolvorib iltijo qilmoq.', 'U etak yoyib soʻradi.'), ('etagidan tutmoq', 'Himoya qilmoq, yordam bermoq.', 'Doʻstining etagidan tutdi.'), ('oyoq osti qilmoq', 'Qadrsizlantirmoq, mensimaslik bilan munosabatda boʻlmoq.', 'Haqini oyoq osti qilib tashladi.'), ('yer bilan yakson qilmoq', 'Butunlay vayron etmoq.', 'Dushman shaharni yer bilan yakson qildi.'), ('suv quyganday jim', 'Juda jim.', 'Zal suv quyganday jim edi.'), ('ot oʻynatmoq', 'Dadil harakat qilmoq, hukmronlik qilmoq.', 'U bu yerda ot oʻynatdi.'), ('ishi yurishmoq', 'Ishi oʻngidan kelmoq.', 'Ishi yurishgan odam tinch yashaydi.'), ('hafsalasi pir boʻlmoq', 'Orzusi ushalmay, ruhi tushmoq.', 'Natijadan hafsalasi pir boʻldi.'), ('jon kuydirmoq', 'Fidokorlik bilan ishlamoq.', 'Ustoz shogirdi uchun jon kuydirdi.'), ('jon bermoq', 'Vafot etmoq; juda ishtiyoq bilan bajarmoq.', 'Ish uchun jon berdi.'), ('jonini hovuchlab', 'Qoʻrqib, xavf ostida.', 'U jonini hovuchlab qochdi.'), ('koʻz qorachigʻi', 'Eng aziz, qadrli inson yoki narsa.', 'Kitoblar uning koʻz qorachigʻi edi.'), ('koʻz yummoq', 'Eʼtibor bermaslikka olmoq; vafot etmoq.', 'U xatoga koʻz yumdi.'), ('koʻz tikmoq', 'Intizor boʻlib qaramoq.', 'Ona yoʻlga koʻz tikdi.'), ('quloq solmoq', 'Diqqat bilan tinglamoq.', 'U ustozning gapiga quloq soldi.'), ('quloq osmoq', 'Eshitmoqchi boʻlib diqqat qilmoq.', 'Hammasi gapga quloq osdi.'), ('labini tishlamoq', 'Afsuslanmoq, ichida yutmoq.', 'U xatosidan labini tishladi.'), ('lab burmoq', 'Norozilik bildirmoq.', 'U taklifga lab burdi.'), ('yoqa ushlamoq', 'Taajjub yoki afsuslanmoq.', 'Hodisadan yoqa ushladi.'), ('bel bogʻlamoq', 'Biror ishga qatʼiy kirishmoq.', 'U oʻqishga bel bogʻladi.'), ('belini mahkam bogʻlamoq', 'Ishga qatʼiy kirishmoq.', 'Belini mahkam bogʻlab ishga tushdi.')]
MAQOL_2 = [('Ilm — hayot chirogʻi', 'Bilim insonning yoʻlini yoritadi.', 'Ilm — hayot chirogʻi, uni qadrlang.'), ('Bilim — kuch', 'Bilim insonga qudrat beradi.', ''), ('Oʻqigan — oʻzar', 'Oʻqigan kishi oldinga siljiydi.', ''), ('Birlik bor joyda — tirilik bor', 'Hamjihatlik hayot va taraqqiyot keltiradi.', ''), ('Birlashgan — oʻzar, birlashmagan — toʻzar', 'Ahillik yutuqqa, nizo parokandalikka olib boradi.', ''), ('Mehnat — mehnatning tagi rohat', 'Mehnat qilgan kishi rohat topadi.', ''), ('Hunar — hunardan unar', 'Mahorat oʻrganilgan sari oʻsadi.', ''), ('Yaxshi soʻz — jon ozigʻi', 'Yaxshi soʻz kishiga kuch beradi.', ''), ('Bir qoʻlda ikki tarvuz turmas', 'Bir vaqtda ikki ishni yaxshi bajarish qiyin.', ''), ('Oz-oz oʻrganib dono boʻlur', 'Asta-sekin bilim orttirib, donishmand boʻlinadi.', ''), ('Birovga choh qazima, oʻzing tushasan', 'Boshqaga yomonlik qilsang, oʻzingga qaytadi.', ''), ('Yaxshining nomi oʻchmas', 'Yaxshi insonning nomi hech qachon unutilmaydi.', ''), ('Dono dushman — nodon doʻstdan yaxshi', 'Oqil dushman ham johil doʻstdan afzal.', ''), ('Sabr tagi — sariq oltin', 'Sabr qilgan kishi katta ajr topadi.', ''), ('Koʻrpangga qarab oyoq uzat', 'Imkoniyatingga qarab ish tut.', ''), ('Ekkaningni oʻrasan', 'Qilgan ishing natijasini koʻrasan.', ''), ('Vaqt — oltin', 'Vaqtning qadriga yetish kerak.', ''), ('Mehmon — otangdek ulugʻ', 'Mehmonga hurmat bilan munosabatda boʻl.', ''), ('Yoshlikda olgan bilim — toshga oʻyilgan naqsh', 'Yoshlikdagi bilim umrbod saqlanadi.', ''), ('Ilmsiz kishi — qanotsiz qush', 'Bilimsiz odam rivojlana olmaydi.', '')]

OT += OT_2
SIFAT += SIFAT_2
FEIL += FEIL_2
SON += SON_2
OLMOSH += OLMOSH_2
RAVISH += RAVISH_2
KOMAKCHI += KOMAKCHI_2
BOGLOVCHI += BOGLOVCHI_2
YUKLAMA += YUKLAMA_2
UNDOV += UNDOV_2
MODAL += MODAL_2
TAQLID += TAQLID_2
ATAMALAR += ATAMALAR_2
ADABIY += ADABIY_2
BADIIY += BADIIY_2

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
    {"key": "frazeo", "title": "🧵 Frazeologizmlar", "label": "frazeologizm",
     "desc": "Maʼnosi koʻchma, turgʻun iboralar", "entries": FRAZEO_2},
    {"key": "maqol", "title": "📜 Maqollar", "label": "maqol",
     "desc": "Xalq donoligi — maqollar va ularning maʼnosi", "entries": MAQOL_2},
]

# Lugʻat kengaytirilgan: maqol, frazeologizm, adabiy va badiiy soʻzlar, atamalar
LEX_EXTRA = {'adabiy': [('qofiya',
             'Misralar oxiridagi tovush jihatidan uygʻun soʻzlar.',
             '«Bahor» va «ruxsor» — qofiyadosh.'),
            ('radif',
             'Qofiyadan keyin takrorlanuvchi soʻz yoki ibora.',
             'Gʻazalda radif har baytda takrorlanadi.'),
            ('vazn',
             'Sheʼrning ohangdorligini belgilovchi oʻlchov tizimi.',
             'Navoiy gʻazallari aruz vaznida yozilgan.'),
            ('aruz',
             'Boʻgʻinlarning uzun va qisqa boʻlishiga asoslangan sheʼr vazni.',
             'Aruz vaznida gʻazal va ruboiy yoziladi.'),
            ('barmoq vazni',
             'Misralardagi boʻgʻinlar soni teng boʻladigan sheʼr vazni.',
             'Xalq qoʻshiqlari barmoq vaznida.'),
            ('bayt', 'Ikki misradan iborat sheʼriy birlik.', 'Gʻazal baytlardan tuziladi.'),
            ('band', 'Bir necha misradan tuzilgan sheʼriy parcha.', 'Sheʼr toʻrt bandli.'),
            ('misra', 'Sheʼrning bir qatori.', 'Baytda ikkita misra bor.'),
            ('mavzu', 'Asarda tasvirlangan voqelik doirasi.', 'Asarning mavzusi — Vatan.'),
            ('gʻoya',
             'Asarda muallif aytmoqchi boʻlgan asosiy fikr.',
             'Romanning gʻoyasi — adolat gʻalabasi.'),
            ('obraz', 'Badiiy asardagi shaxs yoki tasvir.', 'Otabek — «Oʻtkan kunlar» romanidagi obraz.'),
            ('syujet', 'Asarda voqealarning rivojlanish tartibi.', 'Syujet voqealar zanjiriga asoslanadi.'),
            ('kompozitsiya',
             'Asar qismlarining tuzilishi va joylashuvi.',
             'Kompozitsiya asarning butunligini taʼminlaydi.'),
            ('konflikt',
             'Asarda qahramonlar yoki gʻoyalar oʻrtasidagi toʻqnashuv.',
             'Konflikt asar rivojini belgilaydi.'),
            ('monolog',
             'Qahramonning yolgʻiz oʻz-oʻzi bilan yoki tinglovchiga qaratilgan nutqi.',
             'Hamlet monologi mashhur.'),
            ('dialog', 'Ikki yoki undan ortiq personaj oʻrtasidagi suhbat.', 'Asarda dialoglar jonli.'),
            ('ekspozitsiya',
             'Asarda voqealarning boshlanishi oldidagi tanishtiruv qismi.',
             'Ekspozitsiyada qahramonlar tanishtiriladi.'),
            ('kulminatsiya',
             'Asarda voqealar eng keskin choʻqqisiga yetgan nuqta.',
             'Kulminatsiyada qahramon qaror qabul qiladi.'),
            ('yechim', 'Asardagi voqealar yakuniy hal boʻlgan qism.', 'Asar yechimida haqiqat ochildi.'),
            ('metafora',
             'Soʻzni koʻchma maʼnoda qoʻllab, oʻxshatish yaratish.',
             '«Vaqt — oltin» — metafora.'),
            ('tashbeh', 'Biror narsani boshqasiga oʻxshatish (oʻxshatish).', '«Yuzi oydek» — tashbeh.'),
            ('epitet', 'Narsani aniqlab, obrazli taʼriflovchi sifatlash.', '«Oltin kuz» — epitet.'),
            ('mubolagʻa',
             "Narsa yoki belgini haddan ortiq bo'rttirib tasvirlash.",
             '«Dengizdek koʻz yosh» — mubolagʻa.'),
            ('tajassum',
             'Jonsiz narsani jonli mavjudot sifatida tasvirlash.',
             '«Shamol pichirladi» — tajassum.'),
            ('ramz',
             'Biror tushuncha yoki gʻoyani ifodalovchi belgi (simvol).',
             'Oq kaptar — tinchlik ramzi.'),
            ('ironiya',
             'Aytilgan gapning aksi nazarda tutiladigan kinoyali ifoda.',
             '«Qoyil, juda aqlli ish qilibsan» — ironiya.'),
            ('satira',
             'Kamchiliklarni kuchli kulgi bilan fosh qiluvchi asar turi.',
             'Satirada illatlar tanqid qilinadi.'),
            ('komediya',
             'Kulgili voqealar bilan yakunlanuvchi sahna asari.',
             'Komediya tomoshabinni kuldiradi.'),
            ('tragediya',
             'Qahramonning fojiali halokati tasvirlangan sahna asari.',
             'Tragediya tomoshabinni larzaga soladi.'),
            ('lirik qahramon',
             'Sheʼrda shoirning his-tuygʻularini bildiruvchi obraz.',
             'Lirik qahramon vatanga muhabbat izhor qiladi.'),
            ('peyzaj', 'Asarda tabiat manzarasining tasviri.', 'Peyzaj kayfiyatni kuchaytiradi.'),
            ('portret',
             'Asarda qahramon tashqi qiyofasining tasviri.',
             'Portret qahramonni koʻz oldimizga keltiradi.'),
            ('badiiy detal',
             'Tasvirda muhim ahamiyatga ega kichik tafsilot.',
             'Badiiy detal obrazni jonlantiradi.'),
            ('hajviya',
             'Kulgi orqali kamchiliklarni tanqid qiluvchi asar.',
             'Hajviya jamiyat illatlarini fosh qiladi.'),
            ('rivoyat',
             'Xalq orasida aytiladigan, tarixiy voqelikka asoslangan hikoya.',
             'Rivoyatda Navoiyning hayoti tasvirlanadi.'),
            ('afsona',
             'Xayoliy voqealar bilan qorishgan qadimiy xalq hikoyasi.',
             'Afsonada ajdarho haqida soʻzlanadi.'),
            ('ertak',
             'Xayoliy voqealarga asoslangan xalq yoki adabiy hikoya.',
             'Ertakda yaxshilik yomonlik ustidan gʻalaba qiladi.'),
            ('qasida',
             'Biror shaxs yoki voqeani madh etuvchi sheʼriy asar.',
             'Qasida podshoh sharafiga yozildi.'),
            ('marsiya',
             'Vafot etgan kishi yoki fojea haqida qayigʻu bilan yozilgan sheʼr.',
             'Marsiyada kuchli iztirob bor.'),
            ('masnaviy',
             'Har bayti oʻz ichida qofiyalanadigan yirik sheʼriy shakl.',
             'Navoiy «Xamsa»si masnaviy shaklida.'),
            ('tuyuq', 'Toʻrt misradan iborat, jinsli qofiyali sheʼriy janr.', 'Tuyuq soʻz oʻyiniga boy.')],
 'atama': [('morfema',
            'Soʻzning maʼnoli eng kichik boʻlagi.',
            '«Kitoblar» soʻzi ikki morfemadan iborat: kitob + lar.'),
           ('etimologiya',
            'Soʻzlarning kelib chiqishini oʻrganuvchi boʻlim.',
            'Etimologiya «maktab» soʻzining arabchadan kelganini koʻrsatadi.'),
           ('semantika',
            'Soʻz va gaplarning maʼnosini oʻrganuvchi boʻlim.',
            'Semantika maʼno munosabatlarini tahlil qiladi.'),
           ('polisemiya', 'Bir soʻzning bir necha maʼnoga ega boʻlishi.', '«Koʻz» soʻzi polisemiyaga misol.'),
           ('orfografiya', 'Toʻgʻri yozish qoidalari tizimi.', 'Orfografiya imlo qoidalarini belgilaydi.'),
           ('orfoepiya',
            'Toʻgʻri talaffuz qoidalari tizimi.',
            'Orfoepiya adabiy talaffuz meʼyorini koʻrsatadi.'),
           ('punktuatsiya',
            'Tinish belgilari qoʻyish qoidalari.',
            'Punktuatsiya gapda vergul qoʻyishni oʻrgatadi.'),
           ('stilistika',
            'Nutq uslublari va ifoda vositalarini oʻrganuvchi boʻlim.',
            'Stilistika nutqni boyitadi.'),
           ('leksikografiya', 'Lugʻat tuzish ilmi.', 'Leksikografiya izohli lugʻatlarni yaratadi.'),
           ('terminologiya',
            'Atamalar tizimini oʻrganuvchi boʻlim.',
            'Terminologiya fan atamalarini tartibga soladi.'),
           ('toponim', 'Joy nomi.', '«Samarqand» — toponim.'),
           ('antroponim', 'Kishi nomi.', '«Dilnoza» — antroponim.'),
           ('polisemantik soʻz', 'Bir necha maʼnoli soʻz.', '«Tish» soʻzi polisemantik soʻz.'),
           ('maʼnodosh qator', 'Maʼnosi yaqin soʻzlar guruhi.', 'Chiroyli, goʻzal, suluv — maʼnodosh qator.'),
           ('tarixiy soʻz',
            "Tarixiy davr bilan bogʻliq, hozir iste'moldan chiqqan narsani bildiruvchi soʻz.",
            '«Amir» — tarixiy soʻz.'),
           ('soʻz yasalishi',
            'Yangi soʻzlar hosil qilish usullari.',
            'Soʻz yasalishi qoʻshimcha va qoʻshish usullarini oʻrganadi.'),
           ('affiksatsiya',
            'Qoʻshimcha qoʻshish yoʻli bilan soʻz yasash.',
            'Ish + chi = ishchi — affiksatsiya.'),
           ('kompozitsiya usuli', 'Soʻzlarni qoʻshish orqali yangi soʻz yasash.', 'Gul + karam = gulkaram.'),
           ('abbreviatura', 'Soʻz yoki iboralarning qisqartirilgan shakli.', '«BMT» — abbreviatura.'),
           ('urgʻu turlari', 'Soʻz urgʻusi va mantiqiy urgʻu.', 'Urgʻu maʼnoni oʻzgartirishi mumkin.'),
           ('transliteratsiya',
            'Bir yozuvdagi matnni boshqa yozuvga harfma-harf oʻtkazish.',
            'Kirilldan lotinga transliteratsiya qilindi.'),
           ('tavtologiya', 'Bir fikrning ortiqcha takrorlanishi.', '«Yana qaytadan» — tavtologiya.'),
           ('pleonazm', 'Maʼnoni ortiqcha soʻzlar bilan ifodalash.', '«Eng eng yaxshi» — pleonazm.')],
 'badiiy': [('sabo', 'Mayin, sokin esuvchi shamol.', 'Sabo gullarni siypadi.'),
            ('shabnam',
             'Tongda oʻsimliklar ustida paydo boʻlgan suv tomchilari.',
             'Shabnam barglarda yaltiradi.'),
            ('gulshan', 'Gullar oʻsgan chiroyli bogʻ.', 'Gulshanda bulbullar sayraydi.'),
            ('navo', 'Kuy, ovoz, nola.', 'Dutor navosi koʻngilga yoqdi.'),
            ('armon', 'Roʻyobga chiqmagan orzu, afsus.', 'U armon bilan yurtini tark etdi.'),
            ('intizor', 'Zoriqib kutuvchi.', 'Ona intizor koʻz bilan farzandini kutdi.'),
            ('hijron', 'Ayriliq, sevganidan judolik.', 'Hijron dardi uni toliqtirdi.'),
            ('visol', 'Uchrashuv, sevganiga yetishish.', 'Visol onlari baxtli edi.'),
            ('sarv', 'Boʻyi nozik va baland daraxt; goʻzal qomatga oʻxshatiladi.', 'Uning qomati sarvdek.'),
            ('nozanin', 'Nozik va goʻzal qiz.', 'Nozanin qiz bogʻda sayr qildi.'),
            ('dilbar', 'Koʻngilga yoqadigan, goʻzal.', 'Dilbar chehra hammani oʻziga tortdi.'),
            ('jonon', 'Sevimli, aziz inson.', 'Jononni koʻrib dili yayradi.'),
            ('maftun',
             'Biror narsaga mahliyo boʻlgan, oʻziga tortilgan.',
             'U goʻzal manzaraga maftun boʻldi.'),
            ('shaydo', 'Qattiq sevgan, telbalarcha oshiq.', 'Shaydo oshiq yorini izladi.'),
            ('sogʻinch', 'Uzoqdagi yaqinini koʻrishga boʻlgan ishtiyoq.', 'Sogʻinch uni uyga qaytardi.'),
            ('oʻy', 'Fikr, xayol.', 'U chuqur oʻylarga choʻmdi.'),
            ('hayrat', 'Taʼajjub, qoyil qolish.', 'Manzaraga hayrat bilan boqdi.'),
            ('sukunat', 'Jimjitlik, tinchlik.', 'Kechasi sukunat choʻkdi.'),
            ('zavq', 'Rohat, lazzat his etish.', 'Musiqadan zavq oldi.'),
            ('nafis', 'Nozik, goʻzal va oʻzgacha.', 'Nafis naqshlar koʻzni quvontirdi.'),
            ('lola', 'Bahorda ochiladigan qizil gul.', 'Dalada lolalar ochildi.'),
            ('bulbul', "Chiroyli sayraydigan qush; she'riyatda gulga oshiq.", 'Bulbul bogʻda kuyladi.'),
            ('sahar', 'Tong, erta tong.', 'Sahar chogʻida yoʻlga chiqdi.'),
            ('shafaq',
             'Quyosh chiqishi yoki botishidagi qizil-sariq yorugʻlik.',
             'Osmonda shafaq yonib turardi.'),
            ('hasrat', 'Armon, afsus-nadomat bilan sogʻinish.', 'Uning koʻzlarida hasrat bor edi.'),
            ('huzur', 'Roʻshnolik, aʼlo xotirjamlik.', 'Bogʻda huzur qildi.')],
 'frazeo': [('koʻngli boʻsh',
             'Tez taʼsirlanadigan, yumshoq tabiatli.',
             'U koʻngli boʻsh kishi, bolaning yigʻisiga chiday olmadi.'),
            ('koʻngli qora',
             'Niyati yomon, nopok maqsadli.',
             'Koʻngli qora kishi boshqalarga yomonlik tilaydi.'),
            ('koʻngli tosh', 'Berahm, mehrsiz.', 'Koʻngli tosh odam ham bu manzaradan taʼsirlandi.'),
            ('koʻngli keng', 'Saxiy, kechirimli, bagʻrikeng.', 'Koʻngli keng ustoz xatoimni kechirdi.'),
            ('qoʻli ochiq', 'Saxiy, bermaydigan emas.', 'Qoʻli ochiq kishi hammaga yordam beradi.'),
            ('qoʻli qisqa', 'Imkoniyati kam, kambagʻal.', 'Qoʻli qisqa boʻlgani uchun sayohatga bormadi.'),
            ('qoʻli engil', 'Ishi baroridan keladigan, omadli.', 'Qoʻli engil tabib bemorni tezda tuzatdi.'),
            ('qoʻli egri', 'Oʻgʻirlik qilishga moyil.', 'Qoʻli egri kishiga hech kim ishonmaydi.'),
            ('koʻzi qizigan', 'Ochkoʻz, nimadir ustida ishtahasi qoʻzigan.', 'Pulni koʻrib koʻzi qizidi.'),
            ('koʻzi oʻtkir',
             'Sezgir, zehnli, tez payqaydigan.',
             'Koʻzi oʻtkir oʻquvchi xatoni darhol topdi.'),
            ('quloq solmoq', 'Diqqat bilan tinglamoq.', 'Oʻquvchilar ustozning gapiga quloq soldi.'),
            ('til biriktirmoq',
             'Kelishib olib, birgalikda harakat qilmoq (koʻpincha yomon ish uchun).',
             'Ular til biriktirib, rejani buzdi.'),
            ('tili chiqmoq', 'Bola gapira boshlamoq.', 'Chaqaloqning tili chiqdi.'),
            ('tili achchiq',
             'Ozor beradigan, qattiq gapiradigan.',
             'Tili achchiq kishining gapi koʻnglimga tegdi.'),
            ('tili shirin',
             'Muloyim, yoqimli gapiradigan.',
             'Tili shirin sotuvchi mijozlarni oʻziga tortdi.'),
            ('yuragi yorilmoq',
             'Qattiq qoʻrqmoq yoki xavotirlanmoq.',
             'Imtihonni kutib yuragi yorilay dedi.'),
            ('boshi osmonga yetmoq', 'Juda xursand boʻlmoq.', 'Gʻalabadan boshi osmonga yetdi.'),
            ('boshi qotmoq', 'Hal qilolmay, oʻylanib qolmoq.', 'Masalani yechishda boshi qotdi.'),
            ('boshini egmoq', 'Boʻysunmoq yoki hurmat bildirmoq.', 'Hamma ulugʻ shoir oldida boshini egdi.'),
            ('oyogʻi yerga tegmaslik',
             'Juda shoshilib yoki quvonib yurmoq.',
             'Mehmon kelayotganda oyogʻi yerga tegmadi.'),
            ('yer bilan yakson qilmoq',
             'Butunlay yoʻq qilib tashlamoq.',
             'Dushman qalʼani yer bilan yakson qildi.'),
            ('oq yoʻl', 'Safarda omad tilash soʻzi.', 'Oq yoʻl, yoʻlingiz bexatar boʻlsin!'),
            ('yuzi yorugʻ',
             'Obroʻli, hech kimdan uyalmaydigan.',
             'U halol mehnati bilan yuzi yorugʻ boʻldi.'),
            ('yuzi qora', 'Sharmanda, uyatga qolgan.', 'Yolgʻon gapirib yuzi qora boʻldi.'),
            ('yuz oʻgirmoq', 'Eʼtibor bermay qoʻymoq, tark etmoq.', 'Doʻstlari undan yuz oʻgirdi.'),
            ('koʻz tikmoq', 'Umid bilan intizor boʻlib qaramoq.', 'Ona yoʻlga koʻz tikib oʻtirdi.'),
            ('gap tashimoq',
             'Boshqalar haqida yomon gaplarni yetkazib yurmoq.',
             'Gap tashiydigan odam jamiyatda hurmat topmaydi.'),
            ('gapga kirmoq', 'Aytganiga amal qilmoq.', 'Farzand ota gapiga kirdi.'),
            ('burnini koʻtarmoq',
             'Kibrlanib, oʻzini yuqori tutmoq.',
             'Yutuqdan keyin burnini koʻtarib yurdi.'),
            ('burun suqmoq', 'Boshqaning ishiga aralashmoq.', 'Oʻzgalar ishiga burun suqma.'),
            ('qoʻl uzatmoq', 'Yordam bermoq.', 'Kambagʻalga qoʻl uzatish savobdir.'),
            ('qoʻl siltamoq',
             'Umidni uzmoq, eʼtiborsiz qoldirmoq.',
             'Ishlar chatoq boʻlgach, qoʻl siltab ketdi.'),
            ('qoʻl qovushtirmoq',
             'Hech narsa qilmay, ishsiz turmoq.',
             'Hamma ishlayotganda u qoʻl qovushtirib oʻtirdi.'),
            ('tishi oʻtmaslik',
             'Hech qanday taʼsir qila olmaslik.',
             'Qarshiliklar oldida uning tishi oʻtmadi.'),
            ('ogʻzi qulogʻida',
             'Juda xursand, doim tabassum qilib turgan.',
             'Sovrinni olib, ogʻzi qulogʻida yurdi.'),
            ('ogʻzini yummoq', 'Jim boʻlmoq, gap aytmaslik.', 'Savol berilganda u ogʻzini yumdi.'),
            ('labini tishlamoq', 'Afsuslanmoq, pushaymon boʻlmoq.', 'Xatosini anglab, labini tishladi.'),
            ('bel bogʻlamoq', 'Biror ishga astoydil kirishmoq.', 'Ular dalaga bel bogʻlab chiqdi.'),
            ('yoqa ushlamoq', 'Hayratlanmoq, taʼajjublanmoq.', 'Uning jasoratiga hamma yoqa ushladi.'),
            ('yuragini ochmoq', 'Sirini ishonib aytmoq.', 'Doʻstiga yuragini ochdi.'),
            ('koʻz yummoq', 'Eʼtibor bermay qoʻymoq (yoki oʻlmoq).', 'Kamchilikka koʻz yumma.'),
            ('koʻz oldiga keltirmoq', 'Xayolida tasavvur qilmoq.', 'Bolalik yillarini koʻz oldiga keltirdi.'),
            ('dili ogʻrimoq', 'Xafa boʻlmoq, koʻngli qolmoq.', 'Uning gapidan dilim ogʻridi.'),
            ('oʻzini oʻtga-choʻgʻga urmoq',
             'Maqsad yoʻlida har qanday xavfdan qaytmaslik.',
             'Ona farzandi uchun oʻzini oʻtga-choʻgʻga urdi.'),
            ('qulogʻi dikkaymoq',
             'Diqqat bilan tinglay boshlamoq.',
             'Ismi tilga olinganda qulogʻi dikkaydi.'),
            ('koʻngil qoʻymoq', 'Biror ishga astoydil berilmoq.', 'U ilmga koʻngil qoʻydi.')],
 'maqol': [('Ona rozi — Xudo rozi',
            'Ona rozi boʻlsa, Alloh ham rozi boʻladi; onani rozi qilish muhim.',
            'Onasining duosini olgan kishi omadli boʻladi.'),
           ('Yaxshi soʻz — jon ozigʻi',
            'Yaxshi gap insonga madad va quvvat beradi.',
            'Ustozning yaxshi soʻzi unga qanot boʻldi.'),
           ('Oz-oz oʻrganib dono boʻlur, qatra-qatra yigʻilib daryo boʻlur',
            'Oz-ozdan bilim yigʻilib, katta ilm boʻladi.',
            'Har kuni bir sahifa oʻqigan kishi bilimdon boʻladi.'),
           ('Yetti oʻlchab, bir kes',
            'Har ishni puxta oʻylab, keyin qilish kerak.',
            'Qaror qabul qilishdan oldin yetti oʻlchab, bir kes.'),
           ('Vatansiz odam — nolasiz bulbul',
            'Vatani yoʻq kishi baxtsiz va qadrsiz boʻladi.',
            'Vatanning qadriga yetgan kishi uni asraydi.'),
           ('Yaxshi bilan yursang, yetarsan murodga, yomon bilan yursang, qolarsan uyatga',
            'Doʻstni toʻgʻri tanlash hayotda muhim.',
            'Yaxshi doʻst tanlagan oʻquvchi yoʻldan adashmaydi.'),
           ('Sabr tagi — sariq oltin',
            'Sabrli kishi oxir-oqibat maqsadiga yetadi.',
            'Sabr qilgan talaba imtihonni topshirdi.'),
           ('Qush uyasida koʻrganini qiladi',
            'Bola oilada koʻrgan odatlarini takrorlaydi.',
            'Farzandga yaxshi ibrat koʻrsatish kerak.'),
           ('Ona yurting — oltin beshiging',
            'Vatan insonning eng aziz, tinch makonidir.',
            'Chet elda yurganda ona yurt yanada qadrli boʻladi.'),
           ('Hunarmand xor boʻlmas',
            'Kasb-hunar bilgan kishi hech qachon muhtoj boʻlmaydi.',
            'Usta oyda ham ishsiz qolmaydi.'),
           ('Bir bolaga yetti mahalla ota-ona',
            'Bolaga butun mahalla gʻamxoʻrlik qiladi.',
            "Mahallamizda har bir bola hammaning e'tiborida."),
           ('Bir yigitga qirq hunar oz',
            'Inson koʻp kasb-hunar egallashi kerak.',
            'U haydovchi, usta va dasturchi ham boʻlmoqchi.'),
           ('Oʻz uying — oʻlan toʻshaging',
            'Oʻz uyida inson eng erkin va xotirjam boʻladi.',
            'Mehmonchilikdan keyin uy tinchligi yaxshi.'),
           ('Birovga choh qazima, oʻzing tushasan',
            'Boshqaga yomonlik qilsang, oʻzing zarar koʻrasan.',
            'Hasadgoʻy kishi oxiri oʻzi yutqazdi.'),
           ('Yaxshi gap bilan ilon inidan chiqar',
            'Muloyim soʻz bilan hamma ishga erishish mumkin.',
            'Xushmuomala kishi qiyin ishni ham hal qildi.'),
           ('Qoʻl qoʻlni yuvar, ikkalasi yuzni yuvar',
            'Oʻzaro yordam hammaga foyda beradi.',
            'Qoʻshnilar bir-biriga yordam berib, ishni tezda bitirdi.'),
           ('Yurt tinch — el farovon',
            'Yurtda tinchlik boʻlsa, xalq yaxshi yashaydi.',
            'Tinchlik tufayli bogʻlar gullab-yashnadi.'),
           ('Mehnatning noni shirin',
            'Halol mehnat bilan topilgan non zavq bagʻishlaydi.',
            'Oʻz kuchi bilan topgan pul uni xursand qildi.'),
           ('Koʻp oʻyla, oz soʻzla',
            'Gapirishdan oldin yaxshilab oʻylash kerak.',
            'Muhim yigʻilishda koʻp oʻyla, oz soʻzla.'),
           ('Til — dilning tarjimoni',
            'Soʻz kishining koʻngildagi fikrini bildiradi.',
            'Uning soʻzlaridan koʻngli ochiq ekanini bildim.'),
           ('Doʻst achitib gapirar, dushman — kuldirib',
            'Haqiqiy doʻst chin gapni aytadi, dushman esa maqtab aldaydi.',
            'Doʻstining tanqidi unga foyda berdi.'),
           ('Odob — insonning ziynati',
            'Odob kishining eng yaxshi bezagidir.',
            'Odobli bola hammaning hurmatiga sazovor.'),
           ('Birlik bor joyda — tirilik bor',
            'Jamiyat ittifoq boʻlsa, hayot obod boʻladi.',
            'Mahalla birlashib, koʻcha obod qildi.'),
           ('Vaqt — oltin',
            'Vaqt juda qimmatli, uni behuda sarflamaslik kerak.',
            'Dars tayyorlashda vaqt — oltin.'),
           ('Ishlagan tishlaydi',
            'Mehnat qilgan kishi natija koʻradi.',
            'Kuni bilan ishlagan dehqon hosilni yigʻdi.')]}
for _c in CATEGORIES:
    _have = {e[0].lower() for e in _c["entries"]}
    for _e in LEX_EXTRA.get(_c["key"], []):
        if _e[0].lower() not in _have:
            _c["entries"].append(_e)
            _have.add(_e[0].lower())

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

POOL_SIZE = 220
# Qiyin darajalarda savollar koʻproq (jami ~20 000 ta)
POOL_BY = {"d1": 420, "d2": 520, "d3": 760, "d4": 900}
_LV = ["d1"]
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
keskin nari ha yoʻq rahmat salom kerak mumkin zarur lozim tinch boy yosh qari sodiq qattiq shunday bunday boshqa tashqari tomon koʻra sababli qani
oq qora qizil yashil sariq koʻk pushti moviy kulrang jigarrang zarrin yuz ertalab kechqurun kunduz nihoyat haqiqatan
rostdan aslida umuman qisqasi hozircha tepada pastda ichkarida tashqarida oldinda orqada kech erta tong ming oʻn soʻng
oʻzi oʻzing oʻzimiz oʻzingiz birov hammasi barchasi mana ana yoʻl
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

PRO_DATA = {'boglovchi': {'d3': [('Bogʻlovchilar qanday guruhlarga boʻlinadi?',
                       'Teng bogʻlovchilar va ergashtiruvchi bogʻlovchilar',
                       'Asliy va nisbiy bogʻlovchilar',
                       'Oʻtimli va oʻtimsiz bogʻlovchilar',
                       'Sodda va qoʻshma bogʻlovchilar'),
                      ('«Va» bogʻlovchisi qaysi turga kiradi?',
                       'Biriktiruvchi (teng) bogʻlovchi',
                       'Ayiruvchi bogʻlovchi',
                       'Zid bogʻlovchi',
                       'Shart bogʻlovchisi'),
                      ('«Lekin» bogʻlovchisi qaysi turga kiradi?',
                       'Zid (teng) bogʻlovchi',
                       'Biriktiruvchi bogʻlovchi',
                       'Shart bogʻlovchisi',
                       'Sabab bogʻlovchisi'),
                      ('«Agar» bogʻlovchisi qaysi turga kiradi?',
                       'Shart (ergashtiruvchi) bogʻlovchi',
                       'Zid bogʻlovchi',
                       'Ayiruvchi bogʻlovchi',
                       'Biriktiruvchi bogʻlovchi'),
                      ('«Chunki» bogʻlovchisi qaysi turga kiradi?',
                       'Sabab (ergashtiruvchi) bogʻlovchi',
                       'Zid bogʻlovchi',
                       'Shart bogʻlovchisi',
                       'Maqsad bogʻlovchisi'),
                      ('«Yoki» bogʻlovchisi qaysi turga kiradi?',
                       'Ayiruvchi bogʻlovchi',
                       'Biriktiruvchi bogʻlovchi',
                       'Zid bogʻlovchi',
                       'Sabab bogʻlovchisi'),
                      ('Uyushiq boʻlaklar orasidagi «va» dan oldin odatda vergul qoʻyiladimi?',
                       'Yoʻq, qoʻyilmaydi',
                       'Ha, har doim qoʻyiladi',
                       'Faqat savol gapda',
                       'Faqat undov gapda'),
                      ('«Urindi, ammo eplay olmadi.» gapida «ammo» dan oldin qaysi belgi '
                       'qoʻyilgan?',
                       'Vergul',
                       'Nuqta',
                       'Ikki nuqta',
                       'Tire')],
               'd4': [('«Ham... ham» takrorlanuvchi bogʻlovchisi qaysi turga kiradi?',
                       'Biriktiruvchi bogʻlovchi',
                       'Ayiruvchi bogʻlovchi',
                       'Zid bogʻlovchi',
                       'Shart bogʻlovchisi'),
                      ('«Goh... goh» takrorlanuvchi bogʻlovchisi qaysi turga kiradi?',
                       'Ayiruvchi bogʻlovchi',
                       'Biriktiruvchi bogʻlovchi',
                       'Zid bogʻlovchi',
                       'Natija bogʻlovchisi'),
                      ('Bogʻlovchi gapda qanday vazifa bajaradi?',
                       'Soʻz yoki gap boʻlaklarini, gaplarni bogʻlaydi, oʻzi gap boʻlagi boʻlmaydi',
                       'Gap boʻlagi boʻladi',
                       'His-hayajon bildiradi',
                       'Soʻroq maʼnosini beradi'),
                      ('«Garchi... boʻlsa-da» konstruksiyasi qaysi ergash gapni hosil qiladi?',
                       'Toʻsiqsiz (qarshilik) ergash gap',
                       'Shart ergash gap',
                       'Sabab ergash gap',
                       'Payt ergash gap'),
                      ('«Yomgʻir yogʻdi, shuning uchun uyda qoldik.» gapida «shuning uchun» qanday '
                       'vazifada?',
                       'Natija bildiruvchi bogʻlovchi vazifasida',
                       'Sabab bildiruvchi koʻmakchi vazifasida',
                       'Hol vazifasida',
                       'Ega vazifasida'),
                      ('«Yaʼni» soʻzi qanday bogʻlovchi?',
                       'Izohlovchi bogʻlovchi',
                       'Zid bogʻlovchi',
                       'Shart bogʻlovchisi',
                       'Maqsad bogʻlovchisi'),
                      ('«Toki» bogʻlovchisi qaysi ergash gapni bogʻlaydi?',
                       'Maqsad ergash gapni',
                       'Sabab ergash gapni',
                       'Shart ergash gapni',
                       'Payt ergash gapni')]},
 'feil': {'d3': [('«Yordam bermoq» birikmasi tuzilishiga koʻra qanday feʼl?',
                  'Qoʻshma feʼl',
                  'Sodda feʼl',
                  'Juft feʼl',
                  'Takroriy feʼl'),
                 ('«Oʻqimoq» feʼli qanday feʼl?',
                  'Oʻtimli feʼl',
                  'Oʻtimsiz feʼl',
                  'Yordamchi feʼl',
                  'Nisbat feʼli'),
                 ('«Yugurmoq» feʼli qanday feʼl?',
                  'Oʻtimsiz feʼl',
                  'Oʻtimli feʼl',
                  'Yordamchi feʼl',
                  'Qoʻshma feʼl'),
                 ('Oʻtimli feʼl qanday gap boʻlagini talab qiladi?',
                  'Vositasiz toʻldiruvchini (tushum kelishigida)',
                  'Payt holini',
                  'Qaratqich aniqlovchini',
                  'Undalmani'),
                 ('Feʼlning shaxs-son qoʻshimchalari bilan oʻzgarishi nima deyiladi?',
                  'Tuslanish',
                  'Turlanish',
                  'Darajalanish',
                  'Qoʻshilish'),
                 ('Feʼlning boʻlishsiz shakli qaysi qoʻshimcha bilan yasaladi?',
                  '-ma',
                  '-mi',
                  '-siz',
                  '-ga'),
                 ('«Yozmoqchi» soʻzidagi -moqchi qoʻshimchasi qanday maʼno bildiradi?',
                  'Niyat, maqsad',
                  'Boʻlishsizlik',
                  'Tugallanganlik',
                  'Orttirma'),
                 ('Qaysi qatorda ravishdosh qoʻshimchalari berilgan?',
                  '-ib, -gach, -guncha',
                  '-gan, -ar, -yotgan',
                  '-moq, -ish, -v',
                  '-ma, -mi, -siz'),
                 ('Qaysi qatorda sifatdosh qoʻshimchalari berilgan?',
                  '-gan, -ar, -yotgan',
                  '-ib, -gach, -guncha',
                  '-moq, -ish, -v',
                  '-di, -yapti, -adi'),
                 ('Qaysi qatorda harakat nomi qoʻshimchalari berilgan?',
                  '-moq, -ish, -v',
                  '-ib, -gach, -guncha',
                  '-gan, -ar, -yotgan',
                  '-man, -san, -miz'),
                 ('«Oʻqimoq» feʼlining «savod chiqarmoq» va «taʼlim olmoq» maʼnolari qanday '
                  'hodisaga misol?',
                  'Koʻp maʼnolilik',
                  'Omonimiya',
                  'Sinonimiya',
                  'Antonimiya'),
                 ('«Kelsa» shakli feʼlning qaysi mayliga kiradi?',
                  'Shart mayli',
                  'Buyruq mayli',
                  'Aniqlik mayli',
                  'Istak mayli'),
                 ('«Boramiz» soʻzidagi -miz qoʻshimchasi qaysi shaxs-sonni bildiradi?',
                  'I shaxs koʻplik',
                  'II shaxs koʻplik',
                  'I shaxs birlik',
                  'III shaxs koʻplik')],
          'd4': [('«Oʻqib chiqdi» birikmasida «chiqdi» yordamchi feʼli qanday maʼno qoʻshadi?',
                  'Harakatning tugallanganlik maʼnosini',
                  'Boʻlishsizlik maʼnosini',
                  'Orttirma maʼnosini',
                  'Majhullik maʼnosini'),
                 ('Feʼlning qaysi shakli gapda sifat vazifasini bajaradi?',
                  'Sifatdosh',
                  'Ravishdosh',
                  'Harakat nomi',
                  'Buyruq mayli'),
                 ('Feʼlning qaysi shakli gapda ravish vazifasini bajaradi?',
                  'Ravishdosh',
                  'Sifatdosh',
                  'Harakat nomi',
                  'Shart mayli'),
                 ('Feʼlning qaysi shakli gapda ot vazifasini bajara oladi?',
                  'Harakat nomi',
                  'Ravishdosh',
                  'Sifatdosh',
                  'Buyruq mayli'),
                 ('«Oʻqiyotgan bola» birikmasida «oʻqiyotgan» qaysi shaklda?',
                  'Hozirgi zamon sifatdoshi',
                  'Oʻtgan zamon ravishdoshi',
                  'Harakat nomi',
                  'Shart mayli'),
                 ('«Yozdirdi» va «yozildi» shakllari qaysi nisbatlarga mansub?',
                  'Orttirma va majhul nisbat',
                  'Majhul va orttirma nisbat',
                  'Oʻzlik va birgalik nisbat',
                  'Birgalik va oʻzlik nisbat'),
                 ('«Keldi» soʻzida III shaxs birlik qoʻshimchasi qanday ifodalangan?',
                  'Nol (koʻrinmaydigan) qoʻshimcha bilan',
                  '-i bilan',
                  '-di bilan shaxs ham ifodalangan',
                  '-man bilan'),
                 ('«Kitob oʻqigan odam» birikmasida «oʻqigan» qanday sintaktik vazifada?',
                  'Aniqlovchi',
                  'Kesim',
                  'Ega',
                  'Payt holi'),
                 ('«Kulib gapirdi» gapida «kulib» qaysi shakl va qaysi vazifada?',
                  'Ravishdosh, tarz holi',
                  'Sifatdosh, aniqlovchi',
                  'Harakat nomi, ega',
                  'Aniqlik mayli, kesim'),
                 ('«Yozish foydali.» gapida «yozish» qanday vazifada?',
                  'Ega (harakat nomi)',
                  'Kesim',
                  'Aniqlovchi',
                  'Hol'),
                 ('«Bor!» shakli feʼlning qaysi mayliga kiradi?',
                  'Buyruq mayli',
                  'Shart mayli',
                  'Aniqlik mayli',
                  'Istak mayli'),
                 ('«Borgim keldi» shakli qaysi mayl?',
                  'Istak mayli',
                  'Buyruq mayli',
                  'Shart mayli',
                  'Aniqlik mayli'),
                 ('«Bormoq» va «borish» shakllari qanday umumiy xususiyatga ega?',
                  'Ikkalasi ham harakat nomi',
                  'Ikkalasi ham sifatdosh',
                  'Ikkalasi ham ravishdosh',
                  'Ikkalasi ham buyruq mayli')]},
 'komakchi': {'d3': [('«Uchun» koʻmakchisi qanday maʼnoni bildiradi?',
                      'Maqsad yoki sabab',
                      'Oʻxshatish',
                      'Yoʻnalish',
                      'Chegara'),
                     ('«Kabi» koʻmakchisi qanday maʼnoni bildiradi?',
                      'Oʻxshatish',
                      'Maqsad',
                      'Chegara',
                      'Yoʻnalish'),
                     ('«Qadar» koʻmakchisi qanday maʼnoni bildiradi?',
                      'Chegara (vaqt, oʻrin, miqdor)',
                      'Oʻxshatish',
                      'Vosita',
                      'Sabab'),
                     ('Koʻmakchi gap boʻlagi boʻla oladimi?',
                      'Yoʻq, u mustaqil gap boʻlagi boʻlmaydi',
                      'Ha, har doim ega boʻladi',
                      'Ha, har doim kesim boʻladi',
                      'Ha, hol boʻladi'),
                     ('«Doʻstim bilan keldim» gapida «doʻstim bilan» qaysi gap boʻlagi?',
                      'Toʻldiruvchi',
                      'Ega',
                      'Kesim',
                      'Payt holi'),
                     ('«Mendan boshqa hamma keldi» gapida «boshqa» koʻmakchisi qaysi kelishikdagi '
                      'soʻz bilan keldi?',
                      'Chiqish kelishigi',
                      'Tushum kelishigi',
                      'Joʻnalish kelishigi',
                      'Qaratqich kelishigi'),
                     ('«Kechadan beri yomgʻir yogʻyapti» gapida «beri» koʻmakchisi qaysi '
                      'kelishikdagi soʻz bilan keldi?',
                      'Chiqish kelishigi',
                      'Joʻnalish kelishigi',
                      'Tushum kelishigi',
                      'Oʻrin-payt kelishigi'),
                     ('«Ali bilan Vali keldi.» gapida «bilan» qaysi soʻz turkumi?',
                      'Bogʻlovchi',
                      'Koʻmakchi',
                      'Yuklama',
                      'Ravish'),
                     ('«Qalam bilan yozdim.» gapida «bilan» qaysi soʻz turkumi?',
                      'Koʻmakchi',
                      'Bogʻlovchi',
                      'Yuklama',
                      'Undov')],
              'd4': [('Koʻmakchilar boshqa yordamchi soʻzlardan qaysi belgisi bilan farqlanadi?',
                      'Soʻzlarning grammatik bogʻlanishini kelishik bilan birgalikda ifodalashi',
                      'Gapni gapga bogʻlashi',
                      'Soʻroq maʼnosini berishi',
                      'Hissiyotni bildirishi'),
                     ('«Yomgʻirga qaramay chiqdik» gapida «qaramay» qanday maʼno bildiradi?',
                      'Qarshilik',
                      'Sabab',
                      'Maqsad',
                      'Oʻxshatish'),
                     ('«Reja asosida ish olib borildi» gapidagi «asosida» soʻzi qanday vazifada?',
                      'Asos bildiruvchi koʻmakchi vazifasida',
                      'Ega',
                      'Kesim',
                      'Undalma'),
                     ('Koʻmakchili birikma gapda koʻpincha qanday vazifada keladi?',
                      'Toʻldiruvchi yoki hol',
                      'Faqat ega',
                      'Faqat kesim',
                      'Faqat undalma'),
                     ('«Sari» va «tomon» koʻmakchilari qanday maʼno bildiradi?',
                      'Yoʻnalish',
                      'Chegara',
                      'Sabab',
                      'Oʻxshatish'),
                     ('«Boʻyicha» koʻmakchisi qanday maʼno bildiradi?',
                      'Soha yoki asos',
                      'Qarshilik',
                      'Oʻxshatish',
                      'Chegara')]},
 'modal': {'d3': [('Modal soʻzlar gapda qanday vazifa bajaradi?',
                   'Kirish soʻz vazifasini bajaradi',
                   'Ega vazifasini bajaradi',
                   'Kesim vazifasini bajaradi',
                   'Aniqlovchi vazifasini bajaradi'),
                  ('«Albatta» modal soʻzi qanday maʼno bildiradi?',
                   'Ishonch, aniqlik',
                   'Gumon, taxmin',
                   'Afsus',
                   'Tartib'),
                  ('«Ehtimol» modal soʻzi qanday maʼno bildiradi?',
                   'Gumon, taxmin',
                   'Ishonch',
                   'Afsus',
                   'Tartib'),
                  ('«Afsuski» modal soʻzi qanday maʼno bildiradi?',
                   'Afsus, noxushlik',
                   'Ishonch',
                   'Gumon',
                   'Tartib'),
                  ('«Birinchidan» modal soʻzi qanday maʼno bildiradi?',
                   'Fikrlar tartibi, ketma-ketligi',
                   'Ishonch',
                   'Afsus',
                   'Gumon'),
                  ('Kirish soʻzlar gapdan qaysi tinish belgisi bilan ajratiladi?',
                   'Vergul bilan',
                   'Nuqta bilan',
                   'Ikki nuqta bilan',
                   'Qavs bilan')],
           'd4': [('«Masalan» soʻzi qanday maʼno bildiradi?',
                   'Misol keltirish',
                   'Ishonch',
                   'Afsus',
                   'Taxmin'),
                  ('«Xullas» modal soʻzi qanday maʼno bildiradi?',
                   'Xulosa',
                   'Gumon',
                   'Afsus',
                   'Misol'),
                  ('Modal soʻz bilan ravish farqi qaysi?',
                   'Modal soʻz gap mazmuniga munosabat bildiradi, ravish harakat belgisini '
                   'bildiradi',
                   'Ular bir xil',
                   'Ravish munosabat bildiradi, modal soʻz harakat belgisini',
                   'Ikkalasi ham otni aniqlaydi'),
                  ('«Haqiqatan, u haq ekan.» gapida «haqiqatan» qanday vazifada?',
                   'Kirish soʻz',
                   'Ega',
                   'Kesim',
                   'Hol'),
                  ('«Balki» soʻzining qaysi turkumlarga mansubligi mumkin?',
                   'Modal soʻz va bogʻlovchi',
                   'Faqat ot',
                   'Faqat feʼl',
                   'Faqat son'),
                  ('«Mumkin», «kerak», «zarur» soʻzlari qaysi maʼnoni bildiradi?',
                   'Imkoniyat yoki zarurlik (modallik)',
                   'Tasdiq',
                   'Qoʻrquv',
                   'Tartib')]},
 'olmosh': {'d3': [('Olmoshlar qaysi soʻz turkumlari oʻrnida ishlatiladi?',
                    'Ot, sifat, son (va ravish) oʻrnida',
                    'Faqat feʼl oʻrnida',
                    'Faqat undov soʻz oʻrnida',
                    'Faqat bogʻlovchi oʻrnida'),
                   ('«U» olmoshiga -ga qoʻshilganda «unga» boʻladi. Qaysi hodisa yuz beradi?',
                    'n tovushining ortishi',
                    'Unli tovush tushishi',
                    'Undoshning almashishi',
                    'Boʻgʻin tushishi'),
                   ('«Bu kitob qiziq.» gapida «bu» qaysi gap boʻlagi?',
                    'Aniqlovchi',
                    'Ega',
                    'Kesim',
                    'Hol'),
                   ('«Hamma keldi.» gapida «hamma» qaysi gap boʻlagi?',
                    'Ega',
                    'Kesim',
                    'Aniqlovchi',
                    'Hol'),
                   ('«Hech kim kelmadi.» gapida inkor maʼnosi qanday ifodalangan?',
                    'Boʻlishsizlik olmoshi va boʻlishsiz shakldagi kesim bilan',
                    'Faqat olmosh bilan',
                    'Faqat yuklama bilan',
                    'Faqat ravish bilan'),
                   ('«Mening kitobim» birikmasida «mening» qanday vazifada?',
                    'Qaratqich aniqlovchi',
                    'Sifatlovchi aniqlovchi',
                    'Ega',
                    'Toʻldiruvchi'),
                   ('«Siz» va «sen» olmoshlari oʻrtasidagi asosiy uslubiy farq qaysi?',
                    '«Siz» hurmat, «sen» yaqinlik bildiradi',
                    '«Siz» koʻplik, «sen» birlik, farqi faqat sonda',
                    'Farq yoʻq',
                    '«Sen» rasmiy, «siz» norasmiy'),
                   ('Qaysi qatorda faqat soʻroq olmoshlari bor?',
                    'kim, nima, qaysi, qancha',
                    'men, sen, u, biz',
                    'bu, shu, oʻsha',
                    'hamma, barcha, har'),
                   ('Qaysi qatorda faqat belgilash olmoshlari bor?',
                    'hamma, barcha, har, butun',
                    'kim, nima, qaysi',
                    'bu, shu, oʻsha',
                    'kimdir, nimadir, biror'),
                   ('Qaysi qatorda faqat gumon olmoshlari bor?',
                    'kimdir, nimadir, biror',
                    'men, sen, u',
                    'hech kim, hech narsa',
                    'oʻzim, oʻzing, oʻzi')],
            'd4': [('Oʻzlik olmoshi «oʻz» qaysi qoʻshimchalarni qabul qiladi?',
                    'Egalik qoʻshimchalarini',
                    'Faqat tuslovchi qoʻshimchalarni',
                    'Faqat -lar ni',
                    'Hech qanday qoʻshimchani'),
                   ('Olmosh bilan ot orasidagi asosiy farq qaysi?',
                    'Olmosh narsani nomlamaydi, balki unga ishora qiladi yoki uni almashtiradi',
                    'Olmosh narsani aniq nomlaydi',
                    'Olmosh harakatni bildiradi',
                    'Olmosh faqat sonni bildiradi'),
                   ('Ilmiy maqolada muallif «Biz bu masalani tahlil qildik» deganda «biz» qanday '
                    'maʼnoda?',
                    'Muallifning oʻzi (kamtarlik maʼnosida)',
                    'Koʻp odam',
                    'Oʻquvchilar',
                    'Hurmat bilan murojaat'),
                   ('«Shunday kitob qiziq.» gapida «shunday» qaysi gap boʻlagi?',
                    'Aniqlovchi',
                    'Ega',
                    'Kesim',
                    'Hol'),
                   ('«U kelganda uyda edim.» gapida «u» olmoshi qaysi shaxsni bildiradi?',
                    'III shaxs birlik',
                    'I shaxs birlik',
                    'II shaxs birlik',
                    'III shaxs koʻplik'),
                   ('«Men» olmoshining tushum kelishigi shakli qaysi?',
                    'meni',
                    'mening',
                    'menga',
                    'mendan'),
                   ('«Ular» olmoshining joʻnalish kelishigi shakli qaysi?',
                    'ularga',
                    'ularni',
                    'ularning',
                    'ulardan'),
                   ('«Kimning?» soʻrogʻiga javob boʻlgan olmosh shakli qaysi?',
                    'mening, sening, uning',
                    'meni, seni, uni',
                    'menga, senga, unga',
                    'mendan, sendan, undan'),
                   ('Gumon olmoshlari qaysi qoʻshimcha yordamida yasaladi?',
                    '-dir (kimdir, nimadir) va bir (birov, bironta)',
                    '-lik',
                    '-chi',
                    '-siz'),
                   ('«Har kim oʻz ishini qiladi» gapida «har kim» qanday olmosh?',
                    'Belgilash olmoshi',
                    'Soʻroq olmoshi',
                    'Gumon olmoshi',
                    'Kishilik olmoshi')]},
 'ot': {'d3': [('«Kitoblarimizdan» soʻzida qoʻshimchalar qaysi tartibda joylashgan?',
                'koʻplik + egalik + kelishik',
                'egalik + koʻplik + kelishik',
                'kelishik + egalik + koʻplik',
                'kelishik + koʻplik + egalik'),
               ('Otlarning kelishik qoʻshimchalari bilan oʻzgarishi nima deyiladi?',
                'Turlanish',
                'Tuslanish',
                'Darajalanish',
                'Boʻgʻinlanish'),
               ('Quyidagi qatorlardan qaysi birida faqat atoqli otlar berilgan?',
                'Navoiy, Samarqand, Amudaryo',
                'shoir, shahar, daryo',
                'Navoiy, shahar, Amudaryo',
                'kitob, Samarqand, daryo'),
               ('Quyidagi qatorlardan qaysi birida mavhum otlar berilgan?',
                'mehr, adolat, baxt',
                'kitob, stol, qalam',
                'Toshkent, Navoiy, Sirdaryo',
                'bola, ona, oʻquvchi'),
               ('«Gulzor» soʻzi qanday yoʻl bilan yasalgan?',
                'Qoʻshimcha qoʻshish (affiksatsiya) yoʻli bilan',
                'Soʻzlarni qoʻshish (kompozitsiya) yoʻli bilan',
                'Soʻzni takrorlash yoʻli bilan',
                'Soʻzni qisqartirish yoʻli bilan'),
               ('«Ota-ona» soʻzi tuzilishiga koʻra qanday ot?',
                'Juft ot',
                'Takroriy ot',
                'Qoʻshma ot',
                'Qisqartma ot'),
               ('«Maktabning hovlisi» birikmasida «maktabning» qanday vazifada keladi?',
                'Qaratqich aniqlovchi',
                'Sifatlovchi aniqlovchi',
                'Vositali toʻldiruvchi',
                'Payt holi'),
               ('Qaratqich kelishigidagi ot odatda qaysi shakldagi ot bilan birikadi?',
                'Egalik qoʻshimchasini olgan ot bilan',
                'Feʼl bilan',
                'Ravish bilan',
                'Undov soʻz bilan'),
               ('«Bolani maktabga olib bordim.» gapida «bolani» qaysi gap boʻlagi?',
                'Vositasiz toʻldiruvchi',
                'Vositali toʻldiruvchi',
                'Ega',
                'Payt holi'),
               ('«Qalam» soʻzi qaysi tildan oʻzlashgan?',
                'Arab tilidan',
                'Fors tilidan',
                'Rus tilidan',
                'Yunon tilidan'),
               ('«Stol» soʻzi qaysi tildan oʻzlashgan?',
                'Rus tilidan',
                'Arab tilidan',
                'Fors tilidan',
                'Mongol tilidan'),
               ('Ot III shaxs egalik qoʻshimchasini qabul qilganda qaysi qoida amal qiladi?',
                'Undoshdan keyin -i, unlidan keyin -si',
                'Undoshdan keyin -si, unlidan keyin -i',
                'Har doim -i',
                'Har doim -si')],
        'd4': [('«Tilak» soʻziga -im qoʻshilganda «tilagim» boʻladi. Bu qanday tovush hodisasi?',
                'k tovushining g ga almashishi (jaranglilashuv)',
                'Unli tovush tushishi',
                'Unli tovush ortishi',
                'Boʻgʻin tushishi'),
               ('«Singil» soʻzidan «singlim» hosil boʻlishida qanday hodisa yuz beradi?',
                'Unli tovush (i) tushishi',
                'Undosh tovush ortishi',
                'Unli tovush ortishi',
                'Undoshning almashishi'),
               ('«Toshkent — Oʻzbekistonning poytaxti.» gapida kesim qanday ifodalangan?',
                'Ot bilan',
                'Feʼl bilan',
                'Sifat bilan',
                'Son bilan'),
               ('«Yosh» soʻzi «yosh bola» va «yoshi katta» birikmalarida qanday xususiyat '
                'koʻrsatadi?',
                'Sifat va ot sifatida qoʻllanadi (turkumdan turkumga oʻtish)',
                'Faqat sifat sifatida qoʻllanadi',
                'Faqat ot sifatida qoʻllanadi',
                'Ravish sifatida qoʻllanadi'),
               ('Otlar maʼnosiga koʻra qaysi juft guruhlarga boʻlinadi?',
                'Atoqli va turdosh; moddiy va mavhum',
                'Oʻtimli va oʻtimsiz; sodda va qoʻshma',
                'Asliy va nisbiy; oddiy va qiyosiy',
                'Sanoq va tartib; dona va kasr'),
               ('«Qirollik» soʻzida -lik qoʻshimchasi qanday maʼno qoʻshgan?',
                'Mavhum tushuncha (holat) nomini yasagan',
                'Kichraytirish maʼnosini bergan',
                'Koʻplik maʼnosini bergan',
                'Oʻrin-joy nomini yasagan'),
               ('«Maktab» soʻzining «bino» va «taʼlim tizimi» maʼnolarida qoʻllanishi qanday '
                'hodisa?',
                'Koʻp maʼnolilik (polisemiya)',
                'Omonimiya',
                'Sinonimiya',
                'Paronimiya'),
               ('«Qoʻl» soʻzining «aʼzo» va «yordam» (qoʻl uzatmoq) maʼnolarida qoʻllanishi qaysi '
                'hodisaga misol?',
                'Koʻchma maʼno',
                'Omonimiya',
                'Antonimiya',
                'Paronimiya'),
               ('Qaysi gapda ot ega vazifasida kelgan?',
                'Yomgʻir yogʻdi.',
                'U yomgʻirda ketdi.',
                'Yomgʻirni kutdik.',
                'Yomgʻirdan keyin chiqdik.'),
               ('Qaysi gapda ot hol vazifasida kelgan?',
                'Biz maktabda oʻqiymiz.',
                'Maktab katta.',
                'Maktabni koʻrdim.',
                'Maktab bogʻi chiroyli.'),
               ('«Uyga keldim» gapida «uyga» soʻzi qaysi kelishikda va qanday vazifada?',
                'Joʻnalish kelishigida, oʻrin holi',
                'Tushum kelishigida, toʻldiruvchi',
                'Chiqish kelishigida, oʻrin holi',
                'Qaratqich kelishigida, aniqlovchi'),
               ('«Olma» soʻzining «meva» va «daraxt» maʼnolarida qoʻllanishi qanday hodisa?',
                'Koʻp maʼnolilik',
                'Omonimiya',
                'Antonimiya',
                'Paronimiya'),
               ('«Yoz» (fasl) va «yoz» (yozmoq) soʻzlari oʻzaro qanday munosabatda?',
                'Omonim',
                'Sinonim',
                'Antonim',
                'Paronim')]},
 'ravish': {'d3': [('Ravish qaysi turkumlarni aniqlab keladi?',
                    'Feʼl, sifat va boshqa ravishni',
                    'Faqat otni',
                    'Faqat sonni',
                    'Faqat olmoshni'),
                   ('«Juda chiroyli» birikmasida «juda» qaysi soʻz turkumi?',
                    'Ravish',
                    'Sifat',
                    'Olmosh',
                    'Yuklama'),
                   ('Ravishlar maʼnosiga koʻra qaysi guruhlarga boʻlinadi?',
                    'Payt, oʻrin, tarz, miqdor-daraja, maqsad, sabab',
                    'Asliy, nisbiy, qiyosiy',
                    'Sanoq, tartib, dona',
                    'Oʻtimli, oʻtimsiz'),
                   ('«Tez-tez» soʻzi tuzilishiga koʻra qanday ravish?',
                    'Takroriy ravish',
                    'Juft ravish',
                    'Qoʻshma ravish',
                    'Sodda ravish'),
                   ('Qaysi qoʻshimcha ravish yasaydi?', '-lab (kunlab)', '-chi', '-lik', '-li'),
                   ('«Oʻzbekcha gapirdi» soʻzida «oʻzbekcha» qaysi soʻz turkumi va vazifada?',
                    'Ravish, tarz holi',
                    'Sifat, aniqlovchi',
                    'Ot, ega',
                    'Olmosh, toʻldiruvchi'),
                   ('«Bugun dars bor.» gapida «bugun» qaysi gap boʻlagi?',
                    'Payt holi',
                    'Ega',
                    'Kesim',
                    'Aniqlovchi'),
                   ('«Pastda daryo oqdi.» gapida «pastda» qaysi gap boʻlagi?',
                    'Oʻrin holi',
                    'Payt holi',
                    'Tarz holi',
                    'Ega'),
                   ('«Ancha uzoq yoʻl yurdik.» gapida «ancha» qaysi soʻz turkumi?',
                    'Ravish (miqdor-daraja)',
                    'Sifat',
                    'Son',
                    'Olmosh')],
            'd4': [('«Yaxshi» soʻzining «yaxshi odam» va «yaxshi yozdi» birikmalarida qoʻllanishi '
                    'qanday hodisa?',
                    'Konversiya (turkumdan turkumga oʻtish)',
                    'Omonimiya',
                    'Antonimiya',
                    'Paronimiya'),
                   ('Konversiya nima?',
                    'Soʻzning shaklini oʻzgartirmay boshqa turkumga oʻtishi',
                    'Soʻzning qisqarishi',
                    'Soʻzga yasovchi qoʻshimcha qoʻshilishi',
                    'Soʻz maʼnosining koʻchishi'),
                   ('Qaysi gapda «kech» ravish vazifasida kelgan?',
                    'U bugun kech qaytdi.',
                    'Kech tushdi.',
                    'Kechni tinch oʻtkazdik.',
                    'Kechning sovugʻi yoqdi.'),
                   ('«Kam-kam gapirdi» gapida «kam-kam» soʻzi tuzilishiga koʻra qanday?',
                    'Takroriy ravish',
                    'Qoʻshma ravish',
                    'Juft ravish',
                    'Sodda ravish'),
                   ('«Juda yaxshi, juda tez» birikmalarida «juda» ravishining vazifasi qanday?',
                    'Sifat va ravishning belgisini kuchaytiradi',
                    'Otni aniqlaydi',
                    'Feʼlni boʻlishsiz qiladi',
                    'Gap boʻlagini bogʻlaydi'),
                   ('«Hozirgina ketdi» soʻzidagi -gina qoʻshimchasi qanday maʼno beradi?',
                    'Taʼkid (shu zahotiyoq maʼnosini kuchaytiradi)',
                    'Kichraytirish (hajm)',
                    'Koʻplik',
                    'Inkor'),
                   ('Ravish gapda koʻpincha qaysi gap boʻlagi vazifasida keladi?',
                    'Hol',
                    'Ega',
                    'Kesim',
                    'Undalma'),
                   ('«Oʻzbekcha», «ruscha» soʻzlaridagi -cha qoʻshimchasi qanday maʼno beradi?',
                    'Tarz (til yoki uslub boʻyicha)',
                    'Oʻrin',
                    'Payt',
                    'Miqdor')]},
 'sifat': {'d3': [('«Shirin» sifati belgining qaysi turini bildiradi?',
                   'Taʼm-maza belgisini',
                   'Rang-tus belgisini',
                   'Shakl belgisini',
                   'Hajm-oʻlchov belgisini'),
                  ('«Yumaloq» sifati belgining qaysi turini bildiradi?',
                   'Shakl belgisini',
                   'Taʼm belgisini',
                   'Rang belgisini',
                   'Harorat belgisini'),
                  ('«Baland» sifati belgining qaysi turini bildiradi?',
                   'Hajm-oʻlchov belgisini',
                   'Rang belgisini',
                   'Taʼm belgisini',
                   'Xarakter belgisini'),
                  ('«Ilmiy» soʻzi sifatning qaysi turiga kiradi?',
                   'Nisbiy sifat',
                   'Asliy sifat',
                   'Qiyosiy sifat',
                   'Orttirma sifat'),
                  ('«Yoʻgʻon» soʻzi sifatning qaysi turiga kiradi?',
                   'Asliy sifat',
                   'Nisbiy sifat',
                   'Qiyosiy sifat',
                   'Kamaytirma sifat'),
                  ('«Xushmuomala» soʻzi tuzilishiga koʻra qanday sifat?',
                   'Qoʻshma sifat',
                   'Sodda sifat',
                   'Juft sifat',
                   'Takroriy sifat'),
                  ('«Oq-sariq» soʻzi tuzilishiga koʻra qanday sifat?',
                   'Juft sifat',
                   'Qoʻshma sifat',
                   'Takroriy sifat',
                   'Sodda sifat'),
                  ('«Katta-katta» soʻzi tuzilishiga koʻra qanday sifat?',
                   'Takroriy sifat',
                   'Juft sifat',
                   'Qoʻshma sifat',
                   'Sodda sifat'),
                  ('«Bu gul juda chiroyli.» gapida «chiroyli» qaysi gap boʻlagi?',
                   'Kesim',
                   'Aniqlovchi',
                   'Ega',
                   'Hol'),
                  ('«Chiroyli bogʻ koʻrindi.» gapida «chiroyli» qaysi gap boʻlagi?',
                   'Sifatlovchi aniqlovchi',
                   'Kesim',
                   'Ega',
                   'Oʻrin holi'),
                  ('«Yaxshilar koʻp boʻlsin.» gapida «yaxshilar» soʻzida qanday hodisa yuz bergan?',
                   'Sifatning otlashishi',
                   'Otning sifatlanishi',
                   'Sifatning ravishlanishi',
                   'Feʼlning otlashishi'),
                  ('«Qizgʻish» soʻzidagi -ish qoʻshimchasi qanday maʼno beradi?',
                   'Belgining kamligini (kamaytirma)',
                   'Belgining kuchliligini',
                   'Joy nomini',
                   'Kasb-hunar nomini')],
           'd4': [('«Yengil» soʻzining «vazni kam» va «oson» maʼnolarida qoʻllanishi qanday '
                   'hodisa?',
                   'Koʻp maʼnolilik (polisemiya)',
                   'Omonimiya',
                   'Sinonimiya',
                   'Paronimiya'),
                  ('«Achchiq soʻz» birikmasida «achchiq» qanday maʼnoda?',
                   'Koʻchma maʼnoda',
                   'Toʻgʻri (asosiy) maʼnoda',
                   'Antonim maʼnoda',
                   'Termin maʼnoda'),
                  ('«Tez poyezd keldi.» gapida «tez» qaysi soʻz turkumiga kiradi?',
                   'Sifat',
                   'Ravish',
                   'Ot',
                   'Olmosh'),
                  ('«U tez yurdi.» gapida «tez» qaysi soʻz turkumiga kiradi?',
                   'Ravish',
                   'Sifat',
                   'Ot',
                   'Son'),
                  ('«Yaxshi yozdi.» gapida «yaxshi» qaysi soʻz turkumiga kiradi?',
                   'Ravish',
                   'Sifat',
                   'Ot',
                   'Olmosh'),
                  ('Soʻzning shaklini oʻzgartirmasdan boshqa turkumga oʻtishi nima deyiladi?',
                   'Konversiya',
                   'Affiksatsiya',
                   'Kompozitsiya',
                   'Abbreviatsiya'),
                  ('«Kattagina» soʻzidagi -gina qoʻshimchasi qanday maʼno beradi?',
                   'Kichraytirish-erkalash',
                   'Kuchaytirish',
                   'Qiyoslash',
                   'Inkor'),
                  ('«Qip-qizil» soʻzidagi «qip-» qismi qanday vazifa bajaradi?',
                   'Belgini kuchaytiradi',
                   'Belgini kamaytiradi',
                   'Ot yasaydi',
                   'Koʻplik bildiradi'),
                  ('«Chiroylilik» soʻzi qanday yoʻl bilan va qaysi turkumdan yasalgan?',
                   'Sifatdan ot (affiksatsiya)',
                   'Otdan sifat (affiksatsiya)',
                   'Feʼldan ot (konversiya)',
                   'Sifatdan feʼl (affiksatsiya)'),
                  ('«Oltin soch» birikmasida «oltin» soʻzi qanday vazifada qoʻllangan?',
                   'Koʻchma maʼnoli sifatlash (epitet)',
                   'Nisbiy sifat sifatida, toʻgʻri maʼnoda',
                   'Qiyosiy daraja shaklida',
                   'Ravish sifatida'),
                  ('Sifatning orttirma darajasi qaysi usulda hosil qilinadi?',
                   '«eng», «juda» kabi soʻzlar yoki takror orqali',
                   '-roq qoʻshimchasi orqali',
                   '-lik qoʻshimchasi orqali',
                   '-la qoʻshimchasi orqali'),
                  ('«Yaxshi» va «yomon» soʻzlari oʻzaro qanday munosabatda?',
                   'Antonim',
                   'Sinonim',
                   'Omonim',
                   'Paronim'),
                  ('«Goʻzal» va «chiroyli» soʻzlari oʻzaro qanday munosabatda?',
                   'Sinonim',
                   'Antonim',
                   'Omonim',
                   'Paronim')]},
 'son': {'d3': [('Quyidagi qatorlardan qaysi birida sonlarning maʼno turlari toʻgʻri sanalgan?',
                 'sanoq, tartib, dona, kasr, jamlovchi, taxminiy',
                 'sanoq, tartib, atoqli, turdosh',
                 'asliy, nisbiy, oddiy, qiyosiy',
                 'sodda, qoʻshma, juft, takroriy'),
                ('«Yigirma» soniga tartib son qoʻshimchasi qoʻshilsa, qaysi shakl toʻgʻri?',
                 'yigirmanchi',
                 'yigirmainchi',
                 'yigirmachi',
                 'yigirmaninchi'),
                ('«Besh» soniga tartib son qoʻshimchasi qoʻshilsa, qaysi shakl toʻgʻri?',
                 'beshinchi',
                 'beshnchi',
                 'beshchi',
                 'beshanchi'),
                ('Son ot bilan birikkanda ot qanday shaklda keladi?',
                 'Birlikda: «uch kitob»',
                 'Koʻplikda: «uch kitoblar»',
                 'Qaratqich kelishigida',
                 'Faqat egalik shaklida'),
                ('«Beshta» soʻzidagi -ta qoʻshimchasi qanday son yasaydi?',
                 'Dona son',
                 'Tartib son',
                 'Jamlovchi son',
                 'Kasr son'),
                ('«Oʻnlab» soʻzidagi -lab qoʻshimchasi qanday maʼno beradi?',
                 'Taxminiy, noaniq koʻp miqdor',
                 'Tartib',
                 'Jamlovchi maʼno',
                 'Kasr maʼno'),
                ('«Besh kishi keldi.» gapida «besh» qaysi gap boʻlagi?',
                 'Aniqlovchi',
                 'Ega',
                 'Kesim',
                 'Hol'),
                ('Quyidagi qatorlardan qaysi birida faqat kasr sonlar bor?',
                 'yarim, chorak, uchdan bir',
                 'ikkita, beshinchi, oʻnlab',
                 'uch, besh, yetti',
                 'birinchi, ikkinchi, uchinchi'),
                ('«Bir kishi keldi.» gapida «bir» soni qanday maʼnoda qoʻllangan?',
                 'Noaniqlik maʼnosida',
                 'Sanoq maʼnosida (1 ta)',
                 'Tartib maʼnosida',
                 'Kasr maʼnosida'),
                ('«Beshni uchga qoʻshdim.» gapida «beshni» soʻzida qanday hodisa yuz bergan?',
                 'Sonning otlashishi',
                 'Otning sonlashishi',
                 'Sifatning otlashishi',
                 'Feʼlning otlashishi')],
         'd4': [('«Ikki» va «ikkita» soʻzlari oʻrtasidagi farq qaysi?',
                 'Ikki — sanoq son, ikkita — dona son',
                 'Ikki — dona son, ikkita — sanoq son',
                 'Ikkisi ham tartib son',
                 'Farq yoʻq, bir xil son turi'),
                ('«Yuz» soʻzining «100» va «betning old qismi» maʼnolarida qoʻllanishi qanday '
                 'hodisa?',
                 'Omonimiya',
                 'Koʻp maʼnolilik',
                 'Sinonimiya',
                 'Antonimiya'),
                ('Qaysi qatorda tartib sonlar toʻgʻri yozilgan?',
                 'oltinchi, yettinchi, sakkizinchi',
                 'oltiinchi, yettinchi, sakkizinchi',
                 'oltinchi, yettiinchi, sakkizinchi',
                 'oltinchi, yettinchi, sakkiznchi'),
                ('«Beshta olma yedi.» gapida «beshta» qaysi gap boʻlagi?',
                 'Aniqlovchi',
                 'Toʻldiruvchi',
                 'Hol',
                 'Kesim'),
                ('Sonlar boshqa turkumlardan qaysi belgisi bilan ajraladi?',
                 'Miqdor yoki tartibni bildirishi va necha? nechanchi? soʻroqlariga javob berishi',
                 'Harakat bildirishi',
                 'Narsa belgisini rang bilan bildirishi',
                 'Shaxs oʻrnida ishlatilishi'),
                ('Tartib sonlar sifatga qaysi jihatdan oʻxshaydi?',
                 'Otni aniqlashi va aniqlovchi vazifasida kelishi',
                 'Daraja shakllariga ega boʻlishi',
                 'Qiyoslanishi',
                 'Harakat bildirishi'),
                ('«Oʻninchi dars» birikmasida bosh soʻz qaysi?',
                 'dars',
                 'oʻninchi',
                 'Ikkalasi teng',
                 'Bosh soʻz yoʻq')]},
 'taqlid': {'d3': [('Taqlid soʻzlar maʼnosiga koʻra qaysi ikki guruhga boʻlinadi?',
                    'Tovushga va holat (obraz)ga taqlid',
                    'Asliy va nisbiy',
                    'Oʻtimli va oʻtimsiz',
                    'Sanoq va tartib'),
                   ('«Taq-taq» qaysi taqlid soʻz guruhiga kiradi?',
                    'Tovushga taqlid',
                    'Holat (obraz)ga taqlid',
                    'Rangga taqlid',
                    'Maʼnoga taqlid'),
                   ('«Yaltir-yultur» qaysi taqlid soʻz guruhiga kiradi?',
                    'Holat (obraz)ga taqlid',
                    'Tovushga taqlid',
                    'Hidga taqlid',
                    'Mazaga taqlid'),
                   ('«Shitir-shitir» qaysi taqlid soʻz guruhiga kiradi?',
                    'Tovushga taqlid',
                    'Holat (obraz)ga taqlid',
                    'Harakat nomi',
                    'Sifat'),
                   ('Taqlid soʻzlar gapda koʻpincha qanday vazifa bajaradi?',
                    'Hol (tarz holi) yoki kesim boʻlib keladi',
                    'Faqat ega',
                    'Faqat aniqlovchi',
                    'Faqat undalma')],
            'd4': [('Taqlid soʻzdan feʼl yasovchi qoʻshimcha qaysi?',
                    '-la (shitirlamoq)',
                    '-chi',
                    '-lik',
                    '-siz'),
                   ('«Gʻijirlamoq» feʼli qanday yoʻl bilan yasalgan?',
                    'Taqlid soʻzdan -la qoʻshimchasi bilan',
                    'Sifatdan -la bilan',
                    'Otdan -chi bilan',
                    'Sondan -ta bilan'),
                   ('Badiiy matnda taqlid soʻzlar nima uchun qoʻllanadi?',
                    'Tasvirni jonli va taʼsirchan qilish uchun',
                    'Qoidalarni belgilash uchun',
                    'Hisob-kitob uchun',
                    'Rasmiy hujjat yozish uchun'),
                   ('«Miyov-miyov» taqlid soʻzi nimaga taqlid?',
                    'Mushukning ovoziga',
                    'Itning ovoziga',
                    'Qargʻaning ovoziga',
                    'Suv oqishiga'),
                   ('«Vov-vov» taqlid soʻzi nimaga taqlid?',
                    'Itning ovoziga',
                    'Mushukning ovoziga',
                    'Qargʻaning ovoziga',
                    'Eshik gʻijirlashiga')]},
 'undov': {'d3': [('Undov soʻzlar gap boʻlagi boʻladimi?',
                   'Yoʻq, gap boʻlagi boʻlmaydi',
                   'Ha, ega boʻladi',
                   'Ha, kesim boʻladi',
                   'Ha, aniqlovchi boʻladi'),
                  ('«Oh, naqadar goʻzal!» gapida «oh» qanday undov soʻz?',
                   'His-hayajon undovi',
                   'Buyruq-xitob undovi',
                   'Nutq odobi undovi',
                   'Taqlid undovi'),
                  ('«Hoy, toʻxta!» gapida «hoy» qanday undov soʻz?',
                   'Buyruq-xitob undovi',
                   'His-hayajon undovi',
                   'Nutq odobi undovi',
                   'Taqlid undovi'),
                  ('«Rahmat» soʻzi qanday undov soʻz?',
                   'Nutq odobi undovi',
                   'His-hayajon undovi',
                   'Buyruq-xitob undovi',
                   'Taqlid undovi'),
                  ('Undov soʻzdan keyin odatda qaysi tinish belgisi qoʻyiladi?',
                   'Undov belgisi yoki vergul',
                   'Nuqta',
                   'Ikki nuqta',
                   'Tire'),
                  ('«Voy, qoʻlim ogʻridi!» gapida «voy» qanday maʼno bildiradi?',
                   'Ogʻriq, qoʻrquv',
                   'Maqtov',
                   'Rozilik',
                   'Chaqiriq')],
           'd4': [('«Ali, bu yoqqa kel!» gapida «Ali» qaysi vazifada?',
                   'Undalma',
                   'Undov soʻz',
                   'Ega',
                   'Kirish soʻz'),
                  ('Undov soʻz bilan undalma farqi qaysi?',
                   'Undov soʻz his-hayajon bildiradi, undalma murojaat qilinayotgan shaxsni '
                   'bildiradi',
                   'Ular bir xil',
                   'Undalma his-hayajon bildiradi, undov soʻz shaxsni bildiradi',
                   'Ikkalasi ham gap boʻlagi'),
                  ('«Barakalla, yigit!» gapida «barakalla» qanday maʼno bildiradi?',
                   'Maqtov, tahsin',
                   'Afsus',
                   'Qoʻrquv',
                   'Ogʻriq'),
                  ('«Attang, kechikib qoldim!» gapida «attang» qanday maʼno bildiradi?',
                   'Afsus, pushaymon',
                   'Quvonch',
                   'Maqtov',
                   'Chaqiriq'),
                  ('Undov soʻzlar gapda qanday sintaktik xususiyatga ega?',
                   'Gapning boshqa boʻlaklari bilan grammatik bogʻlanmaydi',
                   'Kesimga tobe boʻladi',
                   'Egaga tobe boʻladi',
                   'Aniqlovchi boʻladi')]},
 'yuklama': {'d3': [('Yuklama gapda gap boʻlagi boʻladimi?',
                     'Yoʻq, qoʻshimcha maʼno beradi',
                     'Ha, ega boʻladi',
                     'Ha, kesim boʻladi',
                     'Ha, hol boʻladi'),
                    ('«Siz keldingizmi?» gapidagi -mi yuklamasi qanday maʼno beradi?',
                     'Soʻroq maʼnosi',
                     'Cheklash maʼnosi',
                     'Inkor maʼnosi',
                     'Kichraytirish maʼnosi'),
                    ('«Kichkinagina bola» birikmasidagi -gina yuklamasi qanday maʼno beradi?',
                     'Kichraytirish-erkalash',
                     'Soʻroq',
                     'Taʼkid',
                     'Inkor'),
                    ('«Menda faqat bitta qalam bor.» gapida «faqat» yuklamasi qanday maʼno beradi?',
                     'Cheklash',
                     'Kuchaytirish',
                     'Soʻroq',
                     'Qiyoslash'),
                    ('«Hatto bolalar ham tushundi.» gapida «hatto» yuklamasi qanday maʼno beradi?',
                     'Kuchaytirish',
                     'Cheklash',
                     'Inkor',
                     'Soʻroq'),
                    ('«Xuddi bahordek issiq.» gapida «xuddi» yuklamasi qanday maʼno beradi?',
                     'Qiyoslash',
                     'Cheklash',
                     'Soʻroq',
                     'Inkor')],
             'd4': [('«Kelding-ku!» gapidagi -ku yuklamasi qanday maʼno beradi?',
                     'Taʼkid, ajablanish',
                     'Cheklash',
                     'Soʻroq',
                     'Kichraytirish'),
                    ('«-mi» yuklamasi gapda qayerga qoʻshiladi?',
                     'Soʻroq qaratilgan soʻzga, odatda kesimga',
                     'Faqat gap boshiga',
                     'Faqat gap oxiriga',
                     'Faqat egaga'),
                    ('«Nahotki u kelmasa?» gapidagi «nahotki» qanday maʼno beradi?',
                     'Soʻroq-taʼkid (ajablanish)',
                     'Cheklash',
                     'Qiyoslash',
                     'Kichraytirish'),
                    ('«Ham» soʻzi qaysi turkumlarda uchrashi mumkin?',
                     'Yuklama va bogʻlovchi',
                     'Faqat ot',
                     'Faqat feʼl',
                     'Faqat son'),
                    ('Yuklamalar qaysi vazifani bajaradi?',
                     'Soʻz yoki gapga qoʻshimcha maʼno qoʻshadi',
                     'Soʻzlarni kelishik bilan bogʻlaydi',
                     'Gaplarni teng bogʻlaydi',
                     'Tovushga taqlid qiladi'),
                    ('«Bugunoq boraman» soʻzidagi -oq yuklamasi qanday maʼno beradi?',
                     'Kuchaytirish, aniqlik',
                     'Cheklash',
                     'Soʻroq',
                     'Kichraytirish')]}}
PRO_GEN = {'d3': [('«Ogʻiz — ogʻzi», «oʻgʻil — oʻgʻli» juftliklarida qanday fonetik hodisa roʻy bergan?',
         'Unli tovush tushishi',
         'Unli tovush ortishi',
         'Undosh tovush almashishi',
         'Boʻgʻin qoʻshilishi'),
        ('«Qishloq — qishlogʻim», «ketmoq — ketgan» juftliklaridan birinchisida qanday fonetik '
         'hodisa kuzatiladi?',
         'Undosh almashishi (q — gʻ)',
         'Unli tushishi',
         'Undosh ortishi',
         'Boʻgʻin tushishi'),
        ('«Oʻqituvchilarimizga» soʻzi nechta boʻgʻindan iborat?', '8', '6', '7', '9'),
        ('Lablangan unlilar qatorini toping.', 'u, o, oʻ', 'i, e, a', 'i, u, e', 'a, i, oʻ'),
        ('Faqat jarangsiz undoshlardan iborat qatorni toping.',
         'p, t, q, sh',
         'b, t, q, sh',
         'p, d, q, sh',
         'p, t, g, sh'),
        ('Sonor undoshlar qatorini toping.',
         'm, n, l, r',
         'p, t, k, q',
         'b, d, g, z',
         's, sh, f, x'),
        ('Shakl yasovchi qoʻshimchani toping.', '-ning', '-chi', '-lik', '-kor'),
        ('«Kitoblarimizdan» soʻzida qoʻshimchalar qanday tartibda kelgan?',
         'Koʻplik — egalik — kelishik',
         'Egalik — koʻplik — kelishik',
         'Kelishik — koʻplik — egalik',
         'Koʻplik — kelishik — egalik'),
        ('Quyidagilardan qaysi biri tub soʻz?', 'Qalam', 'Yozuvchi', 'Gulzor', 'Oqqush'),
        ('«OʻzMU», «BMT» kabi soʻzlar qaysi usulda hosil boʻlgan?',
         'Abbreviatsiya (qisqartma)',
         'Qoʻshish',
         'Juftlash',
         'Takrorlash'),
        ('«Qop-qora», «yam-yashil» shakllari sifatning qaysi darajasiga kiradi?',
         'Orttirma daraja',
         'Qiyosiy daraja',
         'Ozaytirma daraja',
         'Oddiy daraja'),
        ('Quyidagilardan qaysi biri ravishdosh qoʻshimchasi?', '-ib', '-gan', '-ayotgan', '-di'),
        ('Quyidagi shakllardan qaysi biri kelasi zamon sifatdoshi qoʻshimchasi?',
         '-ajak',
         '-gan',
         '-ayotgan',
         '-moqda'),
        ('«Yozdirdi» feʼli qaysi nisbatda?',
         'Orttirma nisbat',
         'Oʻzlik nisbat',
         'Majhul nisbat',
         'Birgalik nisbat'),
        ('«Yuvindi» feʼli qaysi nisbatda?',
         'Oʻzlik nisbat',
         'Orttirma nisbat',
         'Majhul nisbat',
         'Birgalik nisbat'),
        ('«Tanishdi» feʼli qaysi nisbatga kiradi?',
         'Birgalik nisbat',
         'Oʻzlik nisbat',
         'Orttirma nisbat',
         'Majhul nisbat'),
        ('«Xat yozildi» gapida «yozildi» feʼli qaysi nisbatda?',
         'Majhul nisbat',
         'Orttirma nisbat',
         'Oʻzlik nisbat',
         'Birgalik nisbat'),
        ('Umumlashtiruvchi soʻz uyushiq boʻlaklardan oldin kelsa, undan keyin qaysi tinish belgisi '
         'qoʻyiladi?',
         'Ikki nuqta',
         'Nuqtali vergul',
         'Tire',
         'Vergul'),
        ('«Men kitobni oʻqidim.» gapida «kitobni» qaysi gap boʻlagi?',
         'Vositasiz toʻldiruvchi',
         'Vositali toʻldiruvchi',
         'Aniqlovchi',
         'Hol'),
        ('«Alining kitobi» birikmasida «Alining» soʻzi qaysi gap boʻlagi vazifasida?',
         'Qaratqich aniqlovchi',
         'Sifatlovchi aniqlovchi',
         'Izohlovchi',
         'Hol'),
        ('«Shoir Navoiy» birikmasida «shoir» soʻzi qaysi boʻlak vazifasida kelgan?',
         'Izohlovchi',
         'Sifatlovchi',
         'Qaratqich aniqlovchi',
         'Toʻldiruvchi'),
        ('«Bu uy goʻzal.» gapida kesim qanday turga kiradi?',
         'Otli kesim',
         'Feʼlli kesim',
         'Sodda ega',
         'Aniqlovchi'),
        ('«Yurish — sogʻliq garovi.» gapida ega qaysi shakldagi soʻz bilan ifodalangan?',
         'Harakat nomi',
         'Sifatdosh',
         'Ravishdosh',
         'Buyruq mayli'),
        ('Koʻchirma gap muallif gapidan oldin kelganda, qoʻshtirnoqdan keyin qanday tinish '
         'belgilari qoʻyiladi?',
         'Vergul va tire',
         'Ikki nuqta',
         'Faqat nuqta',
         'Nuqtali vergul'),
        ('«Men shuni bilamanki, u kelmaydi.» gapida ergash gap qaysi turga kiradi?',
         'Toʻldiruvchi ergash gap',
         'Ega ergash gap',
         'Aniqlovchi ergash gap',
         'Kesim ergash gap')],
 'd4': [('«Oltin kuz» birikmasida «oltin» soʻzining koʻchma maʼnosi qaysi hodisaga asoslangan?',
         'Metafora (oʻxshashlik)',
         'Metonimiya (bogʻliqlik)',
         'Evfemizm',
         'Litota'),
        ('«Butun auditoriya qarsak chaldi» gapida «auditoriya» soʻzi qanday koʻchgan?',
         'Metonimiya (joy — odamlar)',
         'Metafora',
         'Gradatsiya',
         'Inversiya'),
        ('«Dunyodan oʻtdi» ifodasi qanday uslubiy hodisa?',
         'Evfemizm',
         'Disfemizm',
         'Arxaizm',
         'Neologizm'),
        ('Quyidagi juftliklardan qaysi biri omonim?',
         'oʻt (alanga) — oʻt (oʻtmoq)',
         'bosh (aʼzo) — bosh (rahbar)',
         'koʻz (aʼzo) — koʻz (ignaning koʻzi)',
         'oyoq (aʼzo) — oyoq (stol oyogʻi)'),
        ('«Tarif» va «taʼrif» soʻzlari qaysi lugʻaviy munosabatda?',
         'Paronim',
         'Omonim',
         'Sinonim',
         'Antonim'),
        ('Isteʼmoldan chiqqan, chunki ifodalagan narsasi yoʻqolgan soʻzlar qanday ataladi?',
         'Historizm',
         'Arxaizm',
         'Neologizm',
         'Dialektizm'),
        ('Narsa saqlanib qolgan, lekin uni bildiruvchi soʻz eskirgan boʻlsa, bunday soʻz nima '
         'deyiladi?',
         'Arxaizm',
         'Historizm',
         'Neologizm',
         'Jargon'),
        ('Yangi paydo boʻlgan narsa-hodisani ifodalovchi soʻz qanday ataladi?',
         'Neologizm',
         'Arxaizm',
         'Historizm',
         'Dialektizm'),
        ('Faqat muayyan hududda ishlatiladigan soʻz qanday ataladi?',
         'Dialektizm',
         'Jargon',
         'Termin',
         'Professionalizm'),
        ('Qaysi soʻz fors-tojik tilidan oʻzlashgan?', 'Dehqon', 'Kitob', 'Samolyot', 'Pichoq'),
        ('«Qoʻli egri» frazeologizmining maʼnosi qaysi?',
         'Oʻgʻrilik qiladigan',
         'Ishyoqmas',
         'Gap tashuvchi',
         'Baxil'),
        ('«Bahor dalalarni uygʻotdi» jumlasidagi badiiy vosita nima?',
         'Jonlantirish (shaxslantirish)',
         'Muboʻlagʻa',
         'Kinoya',
         'Oʻxshatish'),
        ('«Chumoli fil boʻlib koʻrindi» ifodasi qaysi badiiy vositaga misol?',
         'Muboʻlagʻa',
         'Litota',
         'Jonlantirish',
         'Antiteza'),
        ('«Barakalla, ishyoqmas!» deganda hajviy maʼno qaysi vosita orqali ifodalangan?',
         'Kinoya',
         'Oʻxshatish',
         'Sifatlash',
         'Inversiya'),
        ('«Keldi bahor.» gapida qaysi uslubiy hodisa kuzatiladi?',
         'Inversiya',
         'Gradatsiya',
         'Antiteza',
         'Anafora'),
        ('Ilmiy uslubning asosiy belgisi qaysi?',
         'Terminlarga boyligi va aniqligi',
         'Sheʼriy obrazlilik',
         'Soʻzlashuv unsurlarining koʻpligi',
         'Hissiy boʻyoqdorlikning kuchliligi'),
        ('Ijtimoiy-siyosiy mavzularni ommaga yetkazuvchi, taʼsirchan uslub qaysi?',
         'Publitsistik uslub',
         'Ilmiy uslub',
         'Rasmiy uslub',
         'Soʻzlashuv uslubi'),
        ('Ish qogʻozlari, buyruq va arizalar qaysi uslubga xos?',
         'Rasmiy uslub',
         'Badiiy uslub',
         'Publitsistik uslub',
         'Ilmiy-ommabop uslub'),
        ('Gap ichida sinonim soʻzlarning oʻrinsiz takrorlanishi qanday nuqson sanaladi?',
         'Tavtologiya',
         'Inversiya',
         'Gradatsiya',
         'Antiteza'),
        ('«Yurak» soʻzining «jasur odam» maʼnosida qoʻllanishi qanday maʼno turiga kiradi?',
         'Koʻchma maʼno',
         'Bevosita maʼno',
         'Terminologik maʼno',
         'Lugʻaviy omonimlik'),
        ('Soʻzning bevosita predmetga bogʻlanib, birinchi navbatda eslanadigan maʼnosi nima '
         'deyiladi?',
         'Asosiy (toʻgʻri) maʼno',
         'Koʻchma maʼno',
         'Frazeologik maʼno',
         'Qoʻshimcha maʼno'),
        ('Soʻz maʼnosining kengayishi, torayishi va koʻchishi qaysi tilshunoslik boʻlimida '
         'oʻrganiladi?',
         'Semasiologiya (soʻz maʼnosi haqidagi taʼlimot)',
         'Fonetika',
         'Grafika',
         'Orfografiya'),
        ('Soʻzlarning tarkibiy qismlarini oʻrganuvchi boʻlim qaysi?',
         'Morfemika',
         'Sintaksis',
         'Leksikografiya',
         'Orfoepiya'),
        ('Toʻgʻri talaffuz qoidalarini oʻrganuvchi boʻlim qaysi?',
         'Orfoepiya',
         'Orfografiya',
         'Grafika',
         'Leksikologiya'),
        ('Soʻzlarning yozilish qoidalarini oʻrganuvchi boʻlim qaysi?',
         'Orfografiya',
         'Orfoepiya',
         'Fonetika',
         'Morfologiya'),
        ('Lugʻat tuzish nazariyasi va amaliyoti qaysi boʻlimda oʻrganiladi?',
         'Leksikografiya',
         'Etimologiya',
         'Frazeologiya',
         'Dialektologiya'),
        ('Soʻzlarning kelib chiqishini oʻrganuvchi boʻlim qaysi?',
         'Etimologiya',
         'Leksikografiya',
         'Semasiologiya',
         'Morfemika'),
        ('Gap boʻlaklari oʻrtasidagi grammatik munosabat va soʻzlarning bogʻlanish usullarini '
         'oʻrganuvchi boʻlim qaysi?',
         'Sintaksis',
         'Morfologiya',
         'Fonetika',
         'Leksikologiya')]}
PRO_TEXT = {t[0] for d in PRO_DATA.values() for l in d.values() for t in l}
for _k, _d in PRO_DATA.items():
    for _lv, _qs in _d.items():
        EXTRA.setdefault(_k, {}).setdefault(_lv, [])
        EXTRA[_k][_lv] = list(_qs) + EXTRA[_k][_lv]
for _lv, _qs in PRO_GEN.items():
    for (_t, _r, *_w) in _qs:
        _x = _q(_t, _r, *_w); _x['pro'] = True
        (ORTACHA if _lv == 'd3' else YUQORI).append(_x)

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
            x = make(rng, q, right, wrongs)
            if x and q in PRO_TEXT:
                x["pro"] = True
            yield x

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


    # ---------------- yangi, chuqur generatorlar
    VOW = "aeiou"

    def vend(w):
        return w[-1] in VOW or w.endswith("oʻ")

    def safe_noun(w):
        if " " in w or "-" in w or w.startswith("-") or len(w) < 3:
            return False
        if w[-1] in "kq":
            return False
        if not vend(w):
            if w[-2] in "aiu" and w[-3] not in VOW and sum(1 for c in w if c in VOW) >= 2:
                return False
        return True

    def ego_forms(w):
        v = vend(w)
        return {"I": w + ("m" if v else "im"), "II": w + ("ng" if v else "ing"),
                "III": w + ("si" if v else "i"), "Ip": w + ("miz" if v else "imiz")}

    PERSON = {"I": "I shaxs birlik (mening)", "II": "II shaxs birlik (sening)",
              "III": "III shaxs birlik (uning)", "Ip": "I shaxs koʻplik (bizning)"}

    def verb_forms(w):
        stem = w[:-3]
        if len(stem) < 2 or stem.endswith("y"):
            return None
        v = stem[-1] in VOW or stem.endswith("oʻ")
        return {"Oʻtgan zamon": stem + "di", "Hozirgi zamon (-yap-)": stem + "yapti",
                "Hozirgi-kelasi zamon": stem + ("ydi" if v else "adi"),
                "Buyruq mayli (III shaxs)": stem + "sin"}

    def f_form(rng, k):
        if k == "ot":
            pool = [e for e in STRICT["ot"] if safe_noun(e["w"])]
            for e in rng.sample(pool, len(pool)):
                f = ego_forms(e["w"])
                p = rng.choice(list(PERSON))
                if rng.random() < 0.5:
                    yield make(rng, f"«{e['w']}» soʻziga {PERSON[p]} egalik qoʻshimchasi qoʻshilsa, qaysi shakl hosil boʻladi?",
                               f[p], [f[x] for x in PERSON if x != p])
                else:
                    yield make(rng, f"«{f[p]}» soʻzidagi egalik qoʻshimchasi kimga qarashlilikni bildiradi?",
                               PERSON[p], [PERSON[x] for x in PERSON if x != p])
        elif k == "feil":
            pool = [e for e in STRICT["feil"] if e["w"].endswith("moq") and " " not in e["w"]]
            for e in rng.sample(pool, len(pool)):
                f = verb_forms(e["w"])
                if not f:
                    continue
                name = rng.choice(list(f))
                if rng.random() < 0.5:
                    yield make(rng, f"«{e['w']}» feʼlining {name} shakli qaysi?", f[name],
                               [f[x] for x in f if x != name])
                else:
                    yield make(rng, f"«{f[name]}» feʼli qaysi zamon yoki mayl shaklida?", name,
                               [x for x in f if x != name])
        elif k == "sifat":
            pool = [e for e in STRICT["sifat"] if " " not in e["w"] and "-" not in e["w"]]
            for e in rng.sample(pool, len(pool)):
                w = e["w"]
                forms = {"Oddiy daraja": w, "Qiyosiy daraja": w + "roq", "Orttirma daraja": "eng " + w}
                name = rng.choice(list(forms))
                if rng.random() < 0.5:
                    yield make(rng, f"«{forms[name]}» sifatning qaysi darajasida?", name,
                               [x for x in list(forms) if x != name] + ["Kamaytirma daraja"])
                else:
                    wr = [forms[x] for x in forms if x != name] + [w + "gina"]
                    yield make(rng, f"«{w}» sifatining {name.lower()} shakli qaysi?", forms[name], wr)

    def f_count(rng, k, near=False, rounds=60):
        cls = STRICT[k]
        if len(cls) < 6:
            return
        lab = LABEL[k]
        neg = others(k, near)
        for _ in range(rounds):
            n = rng.choice([1, 2, 3])
            good = [e["w"] for e in rng.sample(cls, n)]
            bad, seen = [], set(good)
            for e in rng.sample(neg, len(neg)):
                if e["w"] not in seen and _norm(e["w"]) not in {_norm(x) for x in seen}:
                    seen.add(e["w"]); bad.append(e["w"])
                if len(bad) == 5 - n:
                    break
            if len(bad) < 5 - n:
                continue
            row = good + bad
            rng.shuffle(row)
            nums = [x for x in range(0, 5) if x != n]
            yield make(rng, f"Quyidagi qatorda nechta {lab} bor?\n" + ", ".join(row),
                       str(n), [str(x) for x in rng.sample(nums, 3)])

    def f_type_ctx(rng, k):
        if k not in TYPED:
            return
        typed = [(e, _type_of(e)) for e in PLAIN[k]]
        typed = [(e, t) for e, t in typed if t]
        types = sorted({t for _, t in typed})
        if len(types) < 4:
            return
        for e, t in rng.sample(typed, len(typed)):
            tok = _find_token(e["ex"], e["w"], k)
            if not tok:
                continue
            wr = rng.sample([x for x in types if x != t], 3)
            yield make(rng, f"«{e['ex']}»\n\nShu gapdagi «{tok}» soʻzi qaysi turga kiradi?", t, wr)

    def f_def_label(rng, k):
        if k not in ("ot", "sifat", "feil"):
            return
        for e in rng.sample(UM[k], len(UM[k])):
            yield make(rng, f"Quyidagi izoh qaysi turkumdagi soʻzga tegishli?\n«{e['m']}»",
                       LABEL[k], near_labels(rng, k))


    # ---------------- 3-bosqich: murakkab generatorlar
    SON_BASE = {"ikki": "ikk", "uch": "uch", "toʻrt": "toʻrt", "besh": "besh", "olti": "olti", "yetti": "yetti",
                "sakkiz": "sakkiz", "toʻqqiz": "toʻqqiz"}
    SON_KIND = {"Tartib son": lambda b: {"ikki": "ikkinchi", "uch": "uchinchi", "toʻrt": "toʻrtinchi", "besh": "beshinchi",
                                         "olti": "oltinchi", "yetti": "yettinchi", "sakkiz": "sakkizinchi",
                                         "toʻqqiz": "toʻqqizinchi"}[b],
                "Dona son": lambda b: {"ikki": "ikkita", "uch": "uchta", "toʻrt": "toʻrtta", "besh": "beshta",
                                       "olti": "oltita", "yetti": "yettita", "sakkiz": "sakkizta",
                                       "toʻqqiz": "toʻqqizta"}[b],
                "Jamlovchi son": lambda b: {"ikki": "ikkov", "uch": "uchov", "toʻrt": "toʻrtov", "besh": "beshov",
                                            "olti": "oltov", "yetti": "yettov", "sakkiz": "sakkizov",
                                            "toʻqqiz": "toʻqqizov"}[b],
                "Taxminiy son": lambda b: {"ikki": "ikkitacha", "uch": "uchtacha", "toʻrt": "toʻrttacha",
                                           "besh": "beshtacha", "olti": "oltitacha", "yetti": "yettitacha",
                                           "sakkiz": "sakkiztacha", "toʻqqiz": "toʻqqiztacha"}[b]}

    def f_son_form(rng, k):
        if k != "son":
            return
        bases = list(SON_BASE)
        for _ in range(60):
            b = rng.choice(bases)
            kind = rng.choice(list(SON_KIND))
            forms = {x: SON_KIND[x](b) for x in SON_KIND}
            if rng.random() < 0.5:
                yield make(rng, f"«{b}» sanoq sonidan {kind.lower()} yasalsa, qaysi shakl hosil boʻladi?",
                           forms[kind], [forms[x] for x in forms if x != kind])
            else:
                yield make(rng, f"«{forms[kind]}» soni qaysi son turiga kiradi?", kind,
                           [x for x in forms if x != kind])

    PRON = ["men", "sen", "u", "biz", "siz", "ular"]
    CASEF = {
        "Qaratqich kelishigi": ["mening", "sening", "uning", "bizning", "sizning", "ularning"],
        "Tushum kelishigi": ["meni", "seni", "uni", "bizni", "sizni", "ularni"],
        "Joʻnalish kelishigi": ["menga", "senga", "unga", "bizga", "sizga", "ularga"],
        "Oʻrin-payt kelishigi": ["menda", "senda", "unda", "bizda", "sizda", "ularda"],
        "Chiqish kelishigi": ["mendan", "sendan", "undan", "bizdan", "sizdan", "ulardan"],
    }

    def f_olmosh_form(rng, k):
        if k != "olmosh":
            return
        for _ in range(60):
            i = rng.randrange(6)
            case = rng.choice(list(CASEF))
            if rng.random() < 0.5:
                wr = [CASEF[c][i] for c in CASEF if c != case]
                yield make(rng, f"«{PRON[i]}» olmoshining {case.lower()} shakli qaysi?", CASEF[case][i],
                           rng.sample(wr, 3))
            else:
                cs = [c for c in CASEF if c != case]
                yield make(rng, f"«{CASEF[case][i]}» olmoshi qaysi kelishik shaklida?", case, rng.sample(cs, 3))

    NISBAT = {
        "Orttirma nisbat": ["yozdirmoq", "oʻqitmoq", "kuldirmoq", "yuvdirmoq", "kiydirmoq", "bildirmoq",
                            "koʻrsatmoq", "pishirmoq", "uxlatmoq", "yigʻlatmoq", "tushirmoq", "uchirmoq"],
        "Majhul nisbat": ["yozilmoq", "oʻqilmoq", "yuvilmoq", "qurilmoq", "yopilmoq", "aytilmoq", "koʻrilmoq",
                          "topilmoq", "sotilmoq", "berilmoq"],
        "Oʻzlik nisbat": ["yuvinmoq", "kiyinmoq", "toʻplanmoq", "oʻylanmoq", "oʻranmoq", "taranmoq"],
        "Birgalik nisbat": ["yozishmoq", "oʻqishmoq", "kurashmoq", "suhbatlashmoq", "uchrashmoq", "xayrlashmoq",
                            "maslahatlashmoq", "bahslashmoq", "salomlashmoq", "kelishmoq"],
    }

    def f_nisbat(rng, k):
        if k != "feil":
            return
        names = list(NISBAT)
        for _ in range(70):
            nm = rng.choice(names)
            if rng.random() < 0.5:
                w = rng.choice(NISBAT[nm])
                yield make(rng, f"«{w}» feʼli qaysi nisbatda?", nm, [x for x in names if x != nm])
            else:
                right = rng.choice(NISBAT[nm])
                wr = [rng.choice(NISBAT[x]) for x in names if x != nm]
                yield make(rng, f"Quyidagi feʼllardan qaysi biri {nm.lower()} shaklida?", right, wr)

    DERIV = [
        ("ishchi", "ot", "-chi"), ("baliqchi", "ot", "-chi"), ("bogʻchi", "ot", "-chi"), ("yoʻlchi", "ot", "-chi"),
        ("doʻstlik", "ot", "-lik"), ("bolalik", "ot", "-lik"), ("oʻquvchilik", "ot", "-lik"),
        ("gulzor", "ot", "-zor"), ("paxtazor", "ot", "-zor"), ("lolazor", "ot", "-zor"),
        ("oshxona", "ot", "-xona"), ("dorixona", "ot", "-xona"), ("kutubxona", "ot", "-xona"),
        ("kitobxon", "ot", "-xon"), ("yurtdosh", "ot", "-dosh"), ("sinfdosh", "ot", "-dosh"),
        ("qalamdon", "ot", "-don"), ("kulgidon", "ot", "-don"),
        ("aqlli", "sifat", "-li"), ("kuchli", "sifat", "-li"), ("mehrli", "sifat", "-li"), ("ilmli", "sifat", "-li"),
        ("suvsiz", "sifat", "-siz"), ("mehrsiz", "sifat", "-siz"), ("kuchsiz", "sifat", "-siz"),
        ("ilmiy", "sifat", "-iy"), ("tarixiy", "sifat", "-iy"), ("badiiy", "sifat", "-iy"),
        ("doʻstona", "sifat", "-ona"), ("dehqonona", "sifat", "-ona"), ("ustozona", "sifat", "-ona"),
        ("ishlamoq", "feil", "-la"), ("boshlamoq", "feil", "-la"), ("tozalamoq", "feil", "-la"),
        ("yaxshilamoq", "feil", "-la"), ("toʻgʻrilamoq", "feil", "-la"),
    ]

    def f_derive(rng, k):
        if k not in ("ot", "sifat", "feil"):
            return
        mine = [d for d in DERIV if d[1] == k]
        sufs = sorted({d[2] for d in DERIV})
        for d in rng.sample(mine, len(mine)):
            wr = rng.sample([s for s in sufs if s != d[2]], 3)
            yield make(rng, f"«{d[0]}» soʻzi qaysi qoʻshimcha yordamida yasalgan?", d[2], wr)
        for d in rng.sample(mine, len(mine)):
            yield make(rng, f"«{d[0]}» yasama soʻzi qaysi soʻz turkumiga kiradi?", LABEL[k], near_labels(rng, k))

    def f_pair(rng, k, near=False, rounds=60):
        s1 = STRICT[k]
        if len(s1) < 2:
            return
        for _ in range(rounds):
            k2 = rng.choice([x for x in TURKUM_KEYS if x != k and (not near or GROUP[x] == GROUP[k] or rng.random() < 0.3)])
            if not STRICT[k2]:
                continue
            a = rng.choice(s1)
            b = rng.choice(STRICT[k2])
            if _norm(a["w"]) == _norm(b["w"]):
                continue
            rest = [x for x in TURKUM_KEYS if x not in (k, k2)]
            k3 = rng.choice(rest)
            L1, L2, L3 = LABEL[k], LABEL[k2], LABEL[k3]
            right = f"1) {L1}, 2) {L2}"
            wr = [f"1) {L2}, 2) {L1}", f"1) {L1}, 2) {L3}", f"1) {L3}, 2) {L2}"]
            yield make(rng, f"«{a['w']}» (1) va «{b['w']}» (2) soʻzlari qaysi turkumlarga mansub?", right, wr)

    # ---------------- havzalarni yig'ish
    def collect(rng, gens, size=None):
        if size is None:
            size = POOL_BY[_LV[0]]
        pool, seen = [], set()
        its = [iter(g) for g in gens]
        alive = list(range(len(its)))
        while alive and len(pool) < size:
            for i in list(alive):
                while True:
                    try:
                        q = next(its[i])
                    except StopIteration:
                        alive.remove(i)
                        break
                    if not q:
                        continue
                    key = (q["q"], q["o"][q["a"]])
                    if key in seen:
                        continue
                    seen.add(key)
                    q["kind"] = i
                    pool.append(q)
                    break
                if len(pool) >= size:
                    break
        return pool

    result = {}
    for k in TURKUM_KEYS:
        result[k] = {}
        r = lambda lv: random.Random(f"{k}-{lv}")
        rg = r("d1")
        _LV[0] = "d1"
        result[k]["d1"] = collect(rg, [
            f_extra(rg, k, "d1"),
            f_which_is(rg, k, 1), f_word_to_label(rg, k), f_meaning_far(rg, k),
            f_not_is(rg, k, False, 80)])
        rg = r("d2")
        _LV[0] = "d2"
        result[k]["d2"] = collect(rg, [
            f_extra(rg, k, "d2"),
            f_context(rg, k), f_meaning_same(rg, k), f_def_label(rg, k), f_count(rg, k, False),
            f_which_is(rg, k, 2, True), f_not_is(rg, k, False, 80), f_row(rg, k, False, 80)])
        rg = r("d3")
        _LV[0] = "d3"
        result[k]["d3"] = collect(rg, [
            deepen(f_extra(rg, k, "d3")), deepen(f_context_near(rg, k), 40),
            f_meaning_of(rg, k), f_type(rg, k), f_type_ctx(rg, k), deepen(f_form(rg, k)),
            f_count(rg, k, True), f_row(rg, k, False, 160), f_not_is(rg, k, True, 100),
            deepen(f_son_form(rg, k)), deepen(f_olmosh_form(rg, k)), deepen(f_derive(rg, k)),
            f_pair(rg, k, False)])
        rg = r("d4")
        _LV[0] = "d4"
        result[k]["d4"] = collect(rg, [
            deepen(f_extra(rg, k, "d4")), deepen(f_context_near(rg, k), 40),
            f_composite(rg, k), deepen(f_form(rg, k)), f_type_ctx(rg, k), f_meaning_of(rg, k),
            f_count(rg, k, True), f_row(rg, k, True, 200), f_not_is(rg, k, True, 100),
            deepen(f_nisbat(rg, k)), deepen(f_son_form(rg, k)), deepen(f_olmosh_form(rg, k)),
            deepen(f_derive(rg, k)), f_pair(rg, k, True)])
    meta = {"keys": TURKUM_KEYS, "title": TITLE, "label": LABEL}
    return result, meta


# ================= BOT =================
QUIZ_SIZE = 10  # har urinishda nechta savol
TIME_LIMIT = 30  # har bir savolga soniya

TOKEN = (os.getenv("TELEGRAM_BOT_TOKEN") or os.getenv("BOT_TOKEN") or "").strip()
if ":" not in TOKEN:
    sys.exit("TELEGRAM_BOT_TOKEN topilmadi. Hosting panelida Environment boʻlimiga yozing:\n"
             "TELEGRAM_BOT_TOKEN=123456789:AAH...")

URL = f"https://api.telegram.org/bot{TOKEN}/"

# --- Admin va roʻyxatdan oʻtish ---
try:
    ADMIN_ID = int((os.getenv("ADMIN_ID") or "7617175325").strip() or 0)
except ValueError:
    sys.exit("ADMIN_ID raqam boʻlishi kerak. Masalan: export ADMIN_ID=123456789")
CODE_DIR = os.path.dirname(os.path.abspath(__file__))


def _pick_data_dir():
    """Ma'lumotlar doimiy papkada (/data) saqlanadi; boʻlmasa kod papkasida."""
    d = (os.getenv("DATA_DIR") or "").strip()
    for cand in ([d] if d else []) + ["/data"]:
        try:
            if os.path.isdir(cand) and os.access(cand, os.W_OK):
                return cand
        except Exception:
            pass
    return CODE_DIR


DATA_DIR = _pick_data_dir()
if DATA_DIR != CODE_DIR:   # birinchi ishga tushishda eski maʼlumotlarni koʻchirib olamiz
    import shutil, hashlib

    def _merge_seed(_n):
        """Repodagi eski maʼlumotni /data dagi fayl bilan BIR MARTA qoʻshib yuboradi (hech narsa oʻchmaydi)."""
        _src, _dst = os.path.join(CODE_DIR, _n), os.path.join(DATA_DIR, _n)
        if not os.path.exists(_src):
            return
        if not os.path.exists(_dst):
            shutil.copyfile(_src, _dst)
            return
        _raw = open(_src, "rb").read()
        _h = hashlib.md5(_raw).hexdigest()
        _mark = _dst + ".seed"
        try:
            if open(_mark).read().strip() == _h:
                return
        except Exception:
            pass
        if _n.endswith(".jsonl"):
            _have = set(open(_dst, encoding="utf-8").read().splitlines())
            _add = [x for x in _raw.decode("utf-8", "ignore").splitlines() if x.strip() and x not in _have]
            if _add:
                with open(_dst, "a", encoding="utf-8") as _f:
                    _f.write(("\n" if _have and not open(_dst, encoding="utf-8").read().endswith("\n") else "") + "\n".join(_add) + "\n")
        elif _n == "users.json":
            _a = json.load(open(_dst, encoding="utf-8"))
            _b = json.loads(_raw.decode("utf-8"))
            for _k, _v in _b.items():
                _a.setdefault(_k, _v)
            json.dump(_a, open(_dst, "w", encoding="utf-8"), ensure_ascii=False)
        elif _n == "admins.json":
            _a = set(json.load(open(_dst, encoding="utf-8")))
            _a |= set(json.loads(_raw.decode("utf-8")))
            json.dump(sorted(_a), open(_dst, "w", encoding="utf-8"))
        open(_mark, "w").write(_h)

    for _n in ("users.json", "natijalar.jsonl", "esse_natijalar.jsonl", "admins.json"):
        try:
            _merge_seed(_n)
        except Exception as _e:
            print("seed merge xato:", _n, _e)
USERS_FILE = os.path.join(DATA_DIR, "users.json")
RESULTS_FILE = os.path.join(DATA_DIR, "natijalar.jsonl")


def load_users():
    try:
        with open(USERS_FILE, encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}


ADMINS_FILE = os.path.join(DATA_DIR, "admins.json")


def load_admins():
    try:
        with open(ADMINS_FILE, encoding="utf-8") as f:
            return {int(x) for x in json.load(f)}
    except Exception:
        return set()


ADMINS = load_admins()   # bosh admin qoʻshgan qoʻshimcha adminlar


def save_admins():
    tmp = ADMINS_FILE + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(sorted(ADMINS), f)
    os.replace(tmp, ADMINS_FILE)


def is_main(uid):
    return bool(ADMIN_ID) and uid == ADMIN_ID


def is_admin(uid):
    return is_main(uid) or uid in ADMINS


def all_admin_ids():
    ids = set(ADMINS)
    if ADMIN_ID:
        ids.add(ADMIN_ID)
    return sorted(ids)


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
LAST_N = {}   # {user_id: oxirgi test savollar soni}
PENDING = {}  # {user_id: savollar sonini kutayotgan test}
SIZES = list(range(10, 101, 10))
SIZE_BTN = {f"{n} talik": n for n in SIZES}
PICK = {}   # {user_id: tanlangan soʻz turkumi}

# Tugma matnlari
B_TESTS = "📝 Testlar"
B_DICT = "📖 Lug'at"
B_ABOUT = "ℹ️ Bot haqida"
B_ESSE = "✍️ Esse yozish"
def _esse_url():
    u = (os.getenv("ESSE_URL") or "").strip()
    if not u:
        try:
            with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "esse_url.txt"), encoding="utf-8") as f:
                u = f.read().strip()
        except Exception:
            u = ""
    return u or "https://ahrorjumaev397-sketch.github.io/esse/esse11.html"


ESSE_URL = _esse_url()
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

# ------------------------------------------------------------------ Qoʻshimcha professor savollari (PRO4)
PRO4 = {'boglovchi': {'d3': [('«Va, hamda» bogʻlovchilari qaysi turga kiradi?',
                       'Biriktiruvchi',
                       'Zidlovchi',
                       'Ayiruvchi',
                       'Sabab'),
                      ('«Lekin, ammo, biroq» bogʻlovchilari qaysi turga kiradi?',
                       'Zidlovchi',
                       'Biriktiruvchi',
                       'Ayiruvchi',
                       'Shart'),
                      ('«Yoki, yo» bogʻlovchilari qaysi turga kiradi?',
                       'Ayiruvchi',
                       'Biriktiruvchi',
                       'Zidlovchi',
                       'Maqsad'),
                      ('«Chunki» bogʻlovchisi qaysi maʼnoni bildiradi?',
                       'Sabab',
                       'Shart',
                       'Maqsad',
                       'Toʻsiqsizlik')],
               'd4': [('«Agar... boʻlsa» tuzilmasida «agar» qaysi maʼnodagi bogʻlovchi?',
                       'Shart',
                       'Sabab',
                       'Maqsad',
                       'Zidlik'),
                      ('«Garchi... biroq» juftligi qaysi maʼnoni bildiradi?',
                       'Toʻsiqsizlik',
                       'Shart',
                       'Sabab',
                       'Maqsad'),
                      ('Bogʻlovchi gapda qanday vazifa bajaradi?',
                       'Soʻz, birikma yoki gaplarni bogʻlaydi, gap boʻlagi boʻlmaydi',
                       'Ega boʻladi',
                       'Kesim boʻladi',
                       'Toʻldiruvchi boʻladi'),
                      ('«Shuning uchun» birikmasi gapda qanday maʼnoda keladi?',
                       'Natija (oqibat)',
                       'Shart',
                       'Zidlik',
                       'Toʻsiqsizlik')]},
 'feil': {'d3': [('Feʼlning noaniq (harakat nomi) shakli qaysi qoʻshimcha bilan yasaladi?',
                  '-moq',
                  '-gan',
                  '-ib',
                  '-ar'),
                 ('«Kelgan» soʻzi feʼlning qaysi shakli?',
                  'Sifatdosh',
                  'Ravishdosh',
                  'Harakat nomi',
                  'Buyruq mayli'),
                 ('«Kelib» soʻzi feʼlning qaysi shakli?',
                  'Ravishdosh',
                  'Sifatdosh',
                  'Harakat nomi',
                  'Shart mayli'),
                 ('«Oʻqish foydali» gapida «oʻqish» soʻzi feʼlning qaysi shakli?',
                  'Harakat nomi',
                  'Sifatdosh',
                  'Ravishdosh',
                  'Buyruq mayli')],
          'd4': [('«Yozdirdi» feʼli qaysi nisbatda?',
                  'Orttirma nisbat',
                  'Oʻzlik nisbat',
                  'Majhul nisbat',
                  'Birgalik nisbat'),
                 ('«Yuvindi» feʼli qaysi nisbatda?',
                  'Oʻzlik nisbat',
                  'Orttirma nisbat',
                  'Majhul nisbat',
                  'Birgalik nisbat'),
                 ('«Yozildi» feʼli qaysi nisbatda?',
                  'Majhul nisbat',
                  'Oʻzlik nisbat',
                  'Orttirma nisbat',
                  'Birgalik nisbat'),
                 ('«Gaplashdi» feʼlidagi «-sh» qoʻshimchasi qaysi nisbatni yasagan?',
                  'Birgalik nisbat',
                  'Orttirma nisbat',
                  'Majhul nisbat',
                  'Oʻzlik nisbat')]},
 'komakchi': {'d3': [('Quyidagilardan qaysi biri koʻmakchi?', 'uchun', 'va', 'ham', 'hay'),
                     ('«Aka kabi» birikmasida «kabi» qanday maʼno bildiradi?',
                      'Oʻxshatish',
                      'Maqsad',
                      'Sabab',
                      'Vosita'),
                     ('«Kasallik sababli» birikmasida «sababli» qanday maʼno bildiradi?',
                      'Sabab',
                      'Maqsad',
                      'Oʻxshatish',
                      'Vosita')],
              'd4': [('«Kitob oʻqish uchun» birikmasida «uchun» qanday maʼno bildiradi?',
                      'Maqsad',
                      'Sabab',
                      'Oʻxshatish',
                      'Vosita'),
                     ('Koʻmakchi gapda qanday xususiyatga ega?',
                      'Mustaqil gap boʻlagi boʻlmaydi, boshqa soʻz bilan birga keladi',
                      'Ega boʻladi',
                      'Kesim boʻladi',
                      'Aniqlovchi boʻladi'),
                     ('«Uyga qadar» birikmasida «qadar» qanday maʼno bildiradi?',
                      'Chegara',
                      'Vosita',
                      'Sabab',
                      'Oʻxshatish'),
                     ('Yordamchi soʻz turkumlari qaysi qatorda toʻgʻri berilgan?',
                      'Koʻmakchi, bogʻlovchi, yuklama',
                      'Ot, sifat, son',
                      'Modal, undov, taqlid',
                      'Ravish, olmosh, feʼl')]},
 'modal': {'d3': [('«Balki, ehtimol» modal soʻzlari qanday maʼno bildiradi?',
                   'Taxmin (gumon)',
                   'Ishonch',
                   'Buyruq',
                   'Afsus'),
                  ('«Albatta, shubhasiz» modal soʻzlari qanday maʼno bildiradi?',
                   'Ishonch (tasdiq)',
                   'Taxmin',
                   'Inkor',
                   'Maqsad'),
                  ('Modal soʻzlar nimani bildiradi?',
                   'Soʻzlovchining fikrga munosabatini',
                   'Predmetni',
                   'Harakatni',
                   'Belgini')],
           'd4': [('«Ehtimol, men kelaman» gapida «ehtimol» qaysi turkumga kiradi?',
                   'Modal soʻz',
                   'Ravish',
                   'Yuklama',
                   'Bogʻlovchi'),
                  ('Gap boshidagi modal soʻzdan keyin qanday tinish belgisi qoʻyiladi?',
                   'Vergul',
                   'Nuqta',
                   'Tire',
                   'Ikki nuqta'),
                  ('Modal soʻz gap boʻlagi boʻladimi?',
                   'Yoʻq, gap boʻlagi boʻlmaydi',
                   'Ha, ega boʻladi',
                   'Ha, kesim boʻladi',
                   'Ha, holat boʻladi')]},
 'olmosh': {'d3': [('«Men, sen, u» olmoshlari qaysi turga kiradi?',
                    'Kishilik olmoshlari',
                    'Koʻrsatish olmoshlari',
                    'Soʻroq olmoshlari',
                    'Oʻzlik olmoshlari'),
                   ('«Hech kim» olmoshi qaysi turga kiradi?',
                    'Inkor olmoshi',
                    'Belgilash olmoshi',
                    'Gumon olmoshi',
                    'Soʻroq olmoshi'),
                   ('«Biror» olmoshi qaysi turga kiradi?',
                    'Gumon olmoshi',
                    'Inkor olmoshi',
                    'Belgilash olmoshi',
                    'Koʻrsatish olmoshi'),
                   ('«Oʻz» olmoshi qaysi turga kiradi?',
                    'Oʻzlik olmoshi',
                    'Kishilik olmoshi',
                    'Belgilash olmoshi',
                    'Soʻroq olmoshi')],
            'd4': [('«Men» olmoshi tushum kelishigida qanday shaklda keladi?',
                    'meni',
                    'menni',
                    'menga',
                    'mendan'),
                   ('«U» olmoshi joʻnalish kelishigida qanday shaklda keladi?',
                    'unga',
                    'uga',
                    'unda',
                    'undan'),
                   ('«Mening» soʻzi qaysi kelishik shaklidagi olmosh?',
                    'Qaratqich kelishigi',
                    'Tushum kelishigi',
                    'Joʻnalish kelishigi',
                    'Oʻrin-payt kelishigi'),
                   ('«Hamma» olmoshi qaysi turga kiradi?',
                    'Belgilash olmoshi',
                    'Gumon olmoshi',
                    'Inkor olmoshi',
                    'Soʻroq olmoshi')]},
 'ot': {'d3': [('«Oʻquvchilarning» soʻzidagi «-ning» qoʻshimchasi qaysi kelishik shakli?',
                'Qaratqich kelishigi',
                'Tushum kelishigi',
                'Joʻnalish kelishigi',
                'Chiqish kelishigi'),
               ('Quyidagilardan qaysi biri yigʻma ot?', 'xalq', 'tosh', 'gul', 'kitob'),
               ('«Adolat» soʻzi qanday otlar guruhiga kiradi?',
                'Mavhum ot',
                'Aniq ot',
                'Atoqli ot',
                'Yigʻma ot'),
               ('«Kitobim» soʻzidagi «-im» qoʻshimchasi qanday qoʻshimcha?',
                'Egalik qoʻshimchasi (1-shaxs, birlik)',
                'Kelishik qoʻshimchasi',
                'Soʻz yasovchi qoʻshimcha',
                'Shaxs-son qoʻshimchasi')],
        'd4': [('«Ish» oʻzagidan yasalgan «ishchi» va «ishchan» soʻzlari qaysi turkumlarga kiradi?',
                'Ishchi — ot, ishchan — sifat',
                'Ikkalasi ham ot',
                'Ishchi — sifat, ishchan — ot',
                'Ikkalasi ham sifat'),
               ('Oʻzbek tilidagi otlarda qaysi grammatik kategoriya mavjud emas?',
                'Grammatik jins',
                'Son (birlik-koʻplik)',
                'Egalik',
                'Kelishik'),
               ('«Ona tilimiz» birikmasida «tilimiz» soʻzi qaysi shaxs va sonda egalik qoʻshimchasini olgan?',
                '1-shaxs, koʻplik',
                '1-shaxs, birlik',
                '2-shaxs, koʻplik',
                '3-shaxs, birlik'),
               ('«Toshkentlik» soʻzidagi «-lik» qoʻshimchasi qanday vazifa bajargan?',
                'Joy nomidan kishi otini yasagan (soʻz yasagan)',
                'Kelishik shaklini yasagan',
                'Egalik maʼnosini bildirgan',
                'Koʻplik maʼnosini bildirgan')]},
 'ravish': {'d3': [('Qaysi qatorda faqat payt ravishlari berilgan?',
                    'bugun, ertaga, hozir',
                    'tez, sekin, asta',
                    'yuqori, past, ichkari',
                    'juda, nihoyatda, ancha'),
                   ('«Juda, nihoyatda, ancha» ravishlari qaysi turga kiradi?',
                    'Daraja-miqdor ravishi',
                    'Payt ravishi',
                    'Oʻrin ravishi',
                    'Holat ravishi'),
                   ('Ravish qaysi turkumlarga bogʻlanib keladi?',
                    'Feʼl, sifat va boshqa ravishga',
                    'Faqat otga',
                    'Faqat olmoshga',
                    'Faqat sonlarga'),
                   ('«Doim, hamisha» ravishlari qaysi turga kiradi?',
                    'Payt ravishi',
                    'Oʻrin ravishi',
                    'Daraja ravishi',
                    'Maqsad ravishi')],
            'd4': [('«Sekin yurdi» birikmasida «sekin» qaysi gap boʻlagi?',
                    'Holat holi',
                    'Aniqlovchi',
                    'Vositali toʻldiruvchi',
                    'Ega'),
                   ('Ravishlarning qaysi xususiyati toʻgʻri?',
                    'Kelishik va egalik qoʻshimchalarini olmaydi',
                    'Koʻplik qoʻshimchasini oladi',
                    'Shaxs-son bilan tuslanadi',
                    'Kelishik bilan turlanadi'),
                   ('«Ertalab maktabga bordim» gapida «ertalab» soʻzi qaysi gap boʻlagi?',
                    'Payt holi',
                    'Oʻrin holi',
                    'Aniqlovchi',
                    'Ega'),
                   ('Ravishning qiyosiy daraja shakli qaysi qatorda berilgan?',
                    'tezroq',
                    'tezlik',
                    'tezkor',
                    'tezli')]},
 'sifat': {'d3': [('«Qizil» soʻzi sifatning qaysi turiga kiradi?',
                   'Asliy sifat',
                   'Nisbiy sifat',
                   'Ravish',
                   'Ot'),
                  ('«Maktabdagi» soʻzi sifatning qaysi turiga mansub?',
                   'Nisbiy sifat',
                   'Asliy sifat',
                   'Ravish',
                   'Olmosh'),
                  ('Sifatning orttirma daraja shakli qaysi qatorda berilgan?',
                   'qip-qizil',
                   'qizil',
                   'qizilroq',
                   'qizillik'),
                  ('Sifatning qiyosiy daraja shakli qaysi qatorda berilgan?',
                   'chiroyliroq',
                   'juda chiroyli',
                   'chip-chiroyli',
                   'chiroyli')],
           'd4': [('«U chiroyli yozadi» gapida «chiroyli» soʻzi qaysi turkum vazifasida kelgan?',
                   'Ravish vazifasida (holat holi)',
                   'Sifatlovchi aniqlovchi vazifasida',
                   'Kesim vazifasida',
                   'Ega vazifasida'),
                  ('Sifat gapda koʻproq qaysi vazifani bajaradi?',
                   'Sifatlovchi aniqlovchi',
                   'Vositasiz toʻldiruvchi',
                   'Ega',
                   'Payt holi'),
                  ('«Sovuq — issiq» juftligi leksik jihatdan nima?',
                   'Antonimlar',
                   'Sinonimlar',
                   'Omonimlar',
                   'Paronimlar'),
                  ('«Oqish» soʻzidagi «-ish» qoʻshimchasi sifatda qanday maʼno bildiradi?',
                   'Belgining kuchsizligini (ozroqligini)',
                   'Belgining kuchliligini',
                   'Mansublikni',
                   'Maqsadni')]},
 'son': {'d3': [('«Beshinchi» soʻzi qaysi son turiga kiradi?',
                 'Tartib son',
                 'Sanoq son',
                 'Dona son',
                 'Chama son'),
                ('«Uchov» soʻzi qaysi son turiga kiradi?',
                 'Jamlovchi son',
                 'Tartib son',
                 'Kasr son',
                 'Chama son'),
                ('«Oʻnlab» soʻzi qaysi son turiga kiradi?',
                 'Chama son',
                 'Sanoq son',
                 'Tartib son',
                 'Jamlovchi son'),
                ('«Ikkita» soʻzidagi «-ta» qoʻshimchasi qanday maʼno beradi?',
                 'Dona (hisob) maʼnosi',
                 'Tartib maʼnosi',
                 'Taxmin maʼnosi',
                 'Kasr maʼnosi')],
         'd4': [('«Yarim» soʻzi qaysi son turiga kiradi?',
                 'Kasr son',
                 'Tartib son',
                 'Jamlovchi son',
                 'Dona son'),
                ('Son otdan oldin kelganda ot qaysi shaklda boʻladi?',
                 'Birlikda (koʻplik qoʻshimchasisiz)',
                 'Koʻplikda',
                 'Qaratqich kelishigida',
                 'Egalik shaklida'),
                ('«Uchinchi qavatda» birikmasida son qaysi gap boʻlagi vazifasida keladi?',
                 'Aniqlovchi',
                 'Ega',
                 'Kesim',
                 'Holat'),
                ('Tartib sonning raqamli yozilishi toʻgʻri qatorni toping.',
                 '5-sinf',
                 '5sinf',
                 '5 sinf',
                 '5chi sinf')]},
 'taqlid': {'d3': [('«Taq-tuq» soʻzi nimaga taqlid?', 'Tovushga', 'Harakatga', 'Holatga', 'Rangga'),
                   ('«Yalt-yalt» soʻzi nimaga taqlid?', 'Harakat va holatga', 'Tovushga', 'Rangga', 'Hidga'),
                   ('Taqlid soʻzlar koʻproq qanday yoziladi?',
                    'Takroriy shaklda, chiziqcha bilan',
                    'Qoʻshib',
                    'Alohida',
                    'Qisqartirib')],
            'd4': [('«Taqillamoq» feʼli qaysi soʻzdan yasalgan?',
                    'Taqlid soʻz «taq»dan',
                    'Otdan',
                    'Sifatdan',
                    'Sondan'),
                   ('Taqlid soʻzlar qaysi guruhga kiradi?',
                    'Mustaqil ham, yordamchi ham boʻlmagan guruh',
                    'Faqat mustaqil soʻzlar',
                    'Faqat yordamchi soʻzlar',
                    'Faqat shakldosh soʻzlar')]},
 'undov': {'d3': [('«Oh, voy, afsus» undovlari qaysi maʼnoni bildiradi?',
                   'His-hayajon (afsus, alam)',
                   'Buyruq',
                   'Chaqiriq',
                   'Taqlid'),
                  ('«Hoy, ey» undovlari qaysi turga kiradi?',
                   'Murojaat (chaqiriq) undovlari',
                   'Afsus undovlari',
                   'Taqlid soʻzlar',
                   'Modal soʻzlar'),
                  ('Undov soʻzdan keyin qanday tinish belgisi qoʻyiladi?',
                   'Vergul yoki undov belgisi',
                   'Nuqta-vergul',
                   'Qoʻshtirnoq',
                   'Qavs')],
           'd4': [('Undov soʻzlar gap boʻlagi boʻladimi?',
                   'Yoʻq, gap boʻlagi boʻlmaydi, hissiyotni ifodalaydi',
                   'Ha, ega boʻladi',
                   'Ha, kesim boʻladi',
                   'Ha, toʻldiruvchi boʻladi'),
                  ('Modal, undov va taqlid soʻzlar qanday guruhga kiradi?',
                   'Mustaqil ham, yordamchi ham boʻlmagan guruh',
                   'Mustaqil soʻzlar',
                   'Yordamchi soʻzlar',
                   'Shakldosh soʻzlar'),
                  ('«Barakalla!» undovi qanday maʼnoni bildiradi?',
                   'Maqtov (tahsin)',
                   'Afsus',
                   'Qoʻrquv',
                   'Nafrat')]},
 'yuklama': {'d3': [('«Faqat, xolos, -gina» yuklamalari qaysi turga kiradi?',
                     'Cheklov yuklamasi',
                     'Kuchaytiruv yuklamasi',
                     'Soʻroq yuklamasi',
                     'Inkor yuklamasi'),
                    ('«-mi» yuklamasi qaysi turga kiradi?',
                     'Soʻroq yuklamasi',
                     'Cheklov yuklamasi',
                     'Kuchaytiruv yuklamasi',
                     'Inkor yuklamasi'),
                    ('«Hatto, axir, -ku» yuklamalari qaysi turga kiradi?',
                     'Kuchaytiruv yuklamasi',
                     'Cheklov yuklamasi',
                     'Soʻroq yuklamasi',
                     'Inkor yuklamasi')],
             'd4': [('Yuklama gapda qanday xususiyatga ega?',
                     'Mustaqil gap boʻlagi boʻlmaydi',
                     'Ega boʻladi',
                     'Kesim boʻladi',
                     'Aniqlovchi boʻladi'),
                    ('«Kitobni emas, daftarni oldim» gapida «emas» qaysi yuklama turiga mansub?',
                     'Inkor yuklamasi',
                     'Soʻroq yuklamasi',
                     'Cheklov yuklamasi',
                     'Kuchaytiruv yuklamasi'),
                    ('«Kelsa-ku, bilib olarmiz» gapida «-ku» yuklamasi qaysi turga kiradi?',
                     'Kuchaytiruv yuklamasi',
                     'Soʻroq yuklamasi',
                     'Cheklov yuklamasi',
                     'Inkor yuklamasi')]}}


def _add_pro4():
    seen = set()
    for _k, _d in PRO4.items():
        for _lv, _qs in _d.items():
            pool = TUR_TESTS.get(_k, {}).get(_lv)
            if pool is None:
                continue
            seen.update(q["q"] for q in pool)
            for (_t, _r, *_w) in _qs:
                if _t in seen:
                    continue
                seen.add(_t)
                _o = [_r] + list(_w)
                random.shuffle(_o)
                pool.append({"q": _t, "o": _o, "a": _o.index(_r), "kind": 99, "pro": True})


_add_pro4()

GEN5 = {'d3': [('Gapda ega va kesim orasida tire qachon qoʻyiladi?',
         'Ega va kesim ot, son yoki olmosh bilan ifodalanganda',
         'Kesim feʼl bilan ifodalanganda',
         'Ega va kesim orasida ravish kelganda',
         'Tire hech qachon qoʻyilmaydi'),
        ('Uyushiq boʻlaklar orasida «va» bogʻlovchisi kelsa, undan oldin vergul qoʻyiladimi?',
         'Qoʻyilmaydi',
         'Har doim qoʻyiladi',
         'Faqat gap oxirida qoʻyiladi',
         'Faqat ega boʻlsa qoʻyiladi'),
        ('«Lekin, ammo, biroq» bogʻlovchilaridan oldin qanday tinish belgisi qoʻyiladi?',
         'Vergul',
         'Nuqta',
         'Tire',
         'Ikki nuqta'),
        ('Qaysi gapda undalma bor?',
         'Ali, bu yoqqa kel!',
         'Ali keldi.',
         'U kitob oʻqidi.',
         'Bugun havo issiq.'),
        ('Qaysi qatorda soʻzlar toʻgʻri yozilgan?',
         'mahalla, hozir, hayot',
         'maxalla, hozir, hayot',
         'mahalla, xozir, hayot',
         'mahalla, hozir, xayot'),
        ('Qaysi qatorda tutuq belgisi toʻgʻri qoʻllangan?',
         'maʼno, eʼlon, aʼlo',
         'maʻno, eʻlon, aʻlo',
         'mano, elon, alo',
         'ma-no, e-lon, a-lo'),
        ('Bogʻlovchisiz qoʻshma gap qismlari orasida qanday tinish belgisi qoʻyiladi?',
         'Vergul yoki nuqtali vergul',
         'Faqat tire',
         'Faqat nuqta',
         'Qavs'),
        ('«Men kelganimda, u ketgan edi.» gapida ergash gap qaysi turga kiradi?',
         'Payt ergash gap',
         'Shart ergash gap',
         'Sabab ergash gap',
         'Maqsad ergash gap'),
        ('«Agar yomgʻir yogʻsa, uyda qolamiz.» gapi qanday qoʻshma gap?',
         'Ergash gapli qoʻshma gap',
         'Bogʻlovchisiz qoʻshma gap',
         'Tenglanuvchi qoʻshma gap',
         'Sodda yoyiq gap'),
        ('Qaysi gap yigʻiq gap?',
         'Bahor keldi.',
         'Chiroyli bahor keldi.',
         'Bugun bahor keldi.',
         'Dalada bahor keldi.'),
        ('Gapning bosh boʻlaklari qaysilar?',
         'Ega va kesim',
         'Aniqlovchi va hol',
         'Toʻldiruvchi va hol',
         'Ega va toʻldiruvchi'),
        ('«Ketdi — ketmadi» juftligida «-ma» qoʻshimchasi nimani bildiradi?',
         'Feʼlning boʻlishsiz shaklini',
         'Nisbatni',
         'Zamonni',
         'Maylni'),
        ('Oʻzbek adabiy tilida nechta kelishik bor?', '6', '5', '7', '4'),
        ('Qaysi qatorda faqat jarangli undoshlar berilgan?',
         'b, d, g, z',
         'p, t, k, s',
         'p, d, g, z',
         'b, t, g, z'),
        ('Quyidagilardan qaysi biri qoʻshma soʻz va birga yoziladi?',
         'gulkaram',
         'gul karam',
         'gul-karam',
         'gul — karam')],
 'd4': [('Ajratilgan boʻlak gapda qanday ajratiladi?',
         'Odatda vergul bilan, ayrim hollarda tire bilan',
         'Faqat nuqta bilan',
         'Faqat qavs bilan',
         'Hech qanday belgisiz'),
        ('«U, kitobni oʻqib boʻlgach, uxlab qoldi.» gapida ajratilgan qism nima?',
         'Ravishdosh oborot',
         'Sifatdosh oborot',
         'Uyushiq boʻlak',
         'Undalma'),
        ('Qaysi gapda «bilan» biriktiruvchi bogʻlovchi vazifasida kelgan?',
         'Ali bilan Vali keldi.',
         'Qalam bilan yozdim.',
         'Doʻsti bilan bordi.',
         'Ota bilan gaplashdim.'),
        ('«Navoiy mening ustozim.» gapida kesim qanday ifodalangan?',
         'Ot bilan',
         'Feʼl bilan',
         'Son bilan',
         'Ravish bilan'),
        ('Tilshunoslikda «leksema» nima?',
         'Lugʻaviy birlik, soʻzning maʼnoviy asosi',
         'Eng kichik tovush birligi',
         'Gap boʻlagi',
         'Qoʻshimcha'),
        ('«Qoʻl» soʻzining «aʼzo» va «boshqaruv» maʼnolari qanday hodisa?',
         'Polisemiya (koʻp maʼnolilik)',
         'Omonimiya',
         'Sinonimiya',
         'Antonimiya'),
        ('«Tuz» (ovqat uchun) va «tuz» (tuzmoq feʼli) qanday hodisaga misol?',
         'Omonimiya',
         'Polisemiya',
         'Sinonimiya',
         'Paronimiya'),
        ('«Tavsiya — tavsif» juftligi nima deyiladi?', 'Paronimlar', 'Omonimlar', 'Sinonimlar', 'Antonimlar'),
        ('Qaysi soʻz fors-tojik tilidan oʻzlashgan?', 'daftar', 'kitob', 'qalam', 'maktab'),
        ('Oʻzbek tilida urgʻu odatda qaysi boʻgʻinga tushadi?',
         'Oxirgi boʻgʻinga',
         'Birinchi boʻgʻinga',
         'Ikkinchi boʻgʻinga',
         'Har qanday boʻgʻinga'),
        ('«Dars tayyorladim, chunki imtihon yaqin edi.» gapida ergash gap turi qaysi?',
         'Sabab ergash gap',
         'Shart ergash gap',
         'Payt ergash gap',
         'Maqsad ergash gap'),
        ('«Garchi yomgʻir yogʻayotgan boʻlsa-da, biz yoʻlga chiqdik.» gapida ergash gap turi qaysi?',
         'Toʻsiqsiz ergash gap',
         'Shart ergash gap',
         'Sabab ergash gap',
         'Payt ergash gap'),
        ('Koʻchirma gapda muallif gapi keyin kelsa, qaysi variant toʻgʻri?',
         '«Men boraman», — dedi Ali.',
         '«Men boraman» — dedi Ali.',
         '«Men boraman» dedi Ali.',
         '«Men boraman». — dedi Ali.'),
        ('Fikrning ortiqcha takrorlanishi nima deyiladi?', 'Tavtologiya', 'Metafora', 'Epitet', 'Mubolagʻa'),
        ('Ilmiy uslubning asosiy xususiyati qaysi?',
         'Aniqlik, mantiqiy izchillik, atamalarga tayanish',
         'Obrazlilik va sheʼriylik',
         'Soʻzlashuv iboralari',
         'Kinoya va hajv'),
        ('Qaysi matn rasmiy uslubga mansub?', 'Ariza', 'Ertak', 'Gʻazal', 'Doʻstlar suhbati'),
        ('Gʻazalning birinchi bayti nima deyiladi?', 'Matla', 'Maqta', 'Radif', 'Qofiya'),
        ('Gʻazalning oxirgi bayti nima deyiladi?', 'Maqta', 'Matla', 'Band', 'Misra'),
        ('Ruboiy nechta misradan iborat?', '4', '2', '6', '8')]}


GEN6 = {
"d3": [
("«Kitobxon» soʻzi qanday yasalgan?", "Qoʻshimcha qoʻshish yoʻli bilan (kitob + xon)", "Juft soʻz", "Takroriy soʻz", "Qisqartma soʻz"),
("«-gan, -uvchi, -ajak» qoʻshimchalari qaysi shaklni yasaydi?", "Sifatdosh", "Ravishdosh", "Harakat nomi", "Mayl shakli"),
("«-ib, -gach, -guncha» qoʻshimchalari qaysi shaklni yasaydi?", "Ravishdosh", "Sifatdosh", "Harakat nomi", "Nisbat"),
("«-ish, -uv, -moq» qoʻshimchalari qaysi shaklni yasaydi?", "Harakat nomi (masdar)", "Sifatdosh", "Ravishdosh", "Buyruq mayli"),
("Fe'lning tuslanmaydigan shakllari qaysi qatorda berilgan?", "Sifatdosh, ravishdosh, harakat nomi", "Buyruq, shart, istak mayli", "Oʻtgan, hozirgi, kelasi zamon", "Aniq, majhul, orttirma nisbat"),
("Oʻzbek tilida qoʻshimchalar qaysi tartibda qoʻshiladi?", "Koʻplik – egalik – kelishik", "Egalik – koʻplik – kelishik", "Kelishik – egalik – koʻplik", "Koʻplik – kelishik – egalik"),
("Umumlashtiruvchi soʻz uyushiq boʻlaklardan oldin kelsa, undan keyin qanday belgi qoʻyiladi?", "Ikki nuqta", "Vergul", "Nuqta", "Qavs"),
("Umumlashtiruvchi soʻz uyushiq boʻlaklardan keyin kelsa, undan oldin qanday belgi qoʻyiladi?", "Tire", "Ikki nuqta", "Nuqtali vergul", "Qoʻshtirnoq"),
("Kirish soʻzlar gapda qanday ajratiladi?", "Vergul bilan", "Nuqta bilan", "Ajratilmaydi", "Faqat qavs bilan"),
("Gap oʻrtasida kelgan undalma qanday ajratiladi?", "Ikki tomondan vergul bilan", "Faqat tire bilan", "Faqat oldidan nuqta bilan", "Ajratilmaydi"),
("«Kimdir» soʻzi qaysi olmosh turiga kiradi?", "Gumon olmoshi", "Soʻroq olmoshi", "Inkor olmoshi", "Belgilash olmoshi"),
("«Hech kim» birikmasi qaysi olmosh turiga kiradi?", "Inkor olmoshi", "Gumon olmoshi", "Koʻrsatish olmoshi", "Oʻzlik olmoshi"),
("«Har kim» birikmasi qaysi olmosh turiga kiradi?", "Belgilash-jamlash olmoshi", "Inkor olmoshi", "Gumon olmoshi", "Shaxs olmoshi"),
("«Yozishdi» feʼli qaysi nisbatda?", "Birgalik nisbati", "Oʻzlik nisbati", "Majhul nisbat", "Orttirma nisbat"),
("«Yuvindi» feʼli qaysi nisbatda?", "Oʻzlik nisbati", "Birgalik nisbati", "Majhul nisbat", "Aniq nisbat"),
("«Yozdirdi» feʼli qaysi nisbatda?", "Orttirma nisbat", "Oʻzlik nisbati", "Birgalik nisbati", "Aniq nisbat"),
("Qaysi qatordagi bogʻlovchilar ergashtiruvchi bogʻlovchilardir?", "agar, chunki, garchi", "va, hamda, yoki", "lekin, ammo, biroq", "goh–goh, dam–dam"),
("«-zor» qoʻshimchasi qanday maʼno beradi?", "Oʻrin-joy (gulzor, paxtazor)", "Kasb-hunar egasi", "Kichraytirish", "Mansublik"),
("«-chi» qoʻshimchasi (ishchi, baliqchi) qanday maʼno beradi?", "Kasb-kor egasi", "Oʻrin-joy", "Oʻxshatish", "Kamlik"),
("Oʻzbek tilida nechta unli tovush bor?", "6", "5", "7", "8"),
("Oʻzbek tilida soʻz urgʻusi odatda qaysi boʻgʻinga tushadi?", "Oxirgi boʻgʻinga", "Birinchi boʻgʻinga", "Ikkinchi boʻgʻinga", "Har bir boʻgʻinga"),
("«Oʻqituvchilar» soʻzi nechta boʻgʻindan iborat?", "5", "4", "6", "3"),
("Qaysi qatorda faqat jarangli undoshlar berilgan?", "b, d, g, z, v", "p, t, k, s", "ch, f, h, q", "sh, x, s, t"),
("Paronimlar nima?", "Shakli yaqin, maʼnosi har xil soʻzlar", "Maʼnosi yaqin, shakli har xil soʻzlar", "Shakli bir xil, maʼnosi har xil soʻzlar", "Maʼnosi qarama-qarshi soʻzlar"),
("Qaysi juftlik omonimlardan iborat?", "tuz (ovqatga solinadigan) — tuz (feʼl: tuzmoq)", "chiroyli — goʻzal", "katta — kichik", "oq — qora"),
("«Zal qarsak chaldi» gapida qaysi maʼno koʻchish turi bor?", "Metonimiya", "Metafora", "Epitet", "Mubolagʻa"),
("Qaratqich aniqlovchi qaysi qoʻshimcha bilan keladi?", "-ning", "-ni", "-ga", "-da"),
("Qoʻshma gap necha turga boʻlinadi?", "Tenglanuvchi, ergashtiruvchi, bogʻlovchisiz", "Darak, soʻroq, buyruq", "Sodda, yoyiq, yigʻiq", "Ega, kesim, hol"),
("Qaysi gap oʻzlashtirma gap?", "Ali ertaga kelishini aytdi.", "«Men ertaga kelaman», — dedi Ali.", "Ali: «Ertaga kelaman», — dedi.", "Ali ertaga keladi."),
("Qaysi uslubda ariza, buyruq, bayonnoma yoziladi?", "Rasmiy uslub", "Badiiy uslub", "Soʻzlashuv uslubi", "Publitsistik uslub"),
("«Boburnoma» qaysi janrga mansub?", "Memuar (xotira) asar", "Doston", "Gʻazal", "Drama"),
("«Kecha va kunduz» romani muallifi kim?", "Choʻlpon", "Abdulla Qodiriy", "Oybek", "Gʻafur Gʻulom"),
("«Mehrobdan chayon» romani muallifi kim?", "Abdulla Qodiriy", "Choʻlpon", "Fitrat", "Oybek"),
("«Sarob» romani muallifi kim?", "Abdulla Qahhor", "Oybek", "Odil Yoqubov", "Pirimqul Qodirov"),
],
"d4": [
("Navoiy «Xamsa»siga kirmaydigan asar qaysi?", "Mahbub ul-qulub", "Hayrat ul-abror", "Sabʼai sayyor", "Saddi Iskandariy"),
("«Qutadgʻu bilig» muallifi kim?", "Yusuf Xos Hojib", "Mahmud Koshgʻariy", "Ahmad Yugnakiy", "Ahmad Yassaviy"),
("«Devonu lugʻotit turk» muallifi kim?", "Mahmud Koshgʻariy", "Yusuf Xos Hojib", "Ahmad Yugnakiy", "Alisher Navoiy"),
("«Hibatul haqoyiq» asari muallifi kim?", "Ahmad Yugnakiy", "Yusuf Xos Hojib", "Mahmud Koshgʻariy", "Sakkokiy"),
("«Muhokamat ul-lugʻatayn» asari nima haqida?", "Turkiy va fors tillarini taqqoslash", "Arab tili grammatikasi", "Hind adabiyoti tarixi", "Tarixiy voqealar bayoni"),
("«Zafarnoma» asarining muallifi kim?", "Sharafuddin Ali Yazdiy", "Zahiriddin Bobur", "Mirzo Ulugʻbek", "Abulgʻozi Bahodirxon"),
("«Qobusnoma» qanday asar?", "Pand-nasihat xarakteridagi asar", "Tarixiy doston", "Lugʻat", "Sheʼriy devon"),
("«Sinchalak» asarining muallifi kim?", "Abdulla Qahhor", "Abdulla Qodiriy", "Gʻafur Gʻulom", "Said Ahmad"),
("«Qutlugʻ qon» romani muallifi kim?", "Oybek", "Choʻlpon", "Abdulla Qahhor", "Mirzakalon Ismoiliy"),
("«Ruhlar isyoni» dostoni muallifi kim?", "Erkin Vohidov", "Abdulla Oripov", "Muhammad Yusuf", "Rauf Parfi"),
("Ruboiyning qofiyalanish sxemasi qanday boʻladi?", "a-a-b-a yoki a-a-a-a", "a-b-a-b", "a-b-b-a", "a-a-b-b"),
("Tazod nima?", "Qarama-qarshi tushunchalarni yonma-yon qoʻyish", "Jonsiz narsani jonli qilib tasvirlash", "Voqea-hodisani boʻrttirib tasvirlash", "Soʻz oxiridagi tovushlar uygʻunligi"),
("Tashxis (jonlantirish) qaysi gapda qoʻllangan?", "Quyosh kulib boqdi.", "Quyosh chiqdi.", "Quyosh olovdek issiq.", "Quyosh — osmon oʻrtasida."),
("Radif nima?", "She'r misralari oxirida takrorlanuvchi soʻz yoki birikma", "Misralardagi unli tovushlar takrori", "Sheʼrning birinchi bayti", "Misra ichidagi tinish belgilari"),
("Epitet nima?", "Badiiy aniqlovchi", "Qarama-qarshi qoʻyish", "Takroriy soʻz", "Soʻz oʻyini"),
("Mubolagʻa nima?", "Voqea-hodisani boʻrttirib tasvirlash", "Narsalarni kichraytirib tasvirlash", "Jonlantirib tasvirlash", "Qarama-qarshi qoʻyish"),
("«Ega va kesim moslashuvi»da shaxs-son jihatdan mosliq qaysi gapda buzilgan?", "Biz maktabga bordi.", "Biz maktabga bordik.", "U maktabga bordi.", "Siz maktabga bordingiz."),
("Qaysi gapda ortiqcha soʻz (pleonazm) bor?", "Mening shaxsiy fikrim shundan iborat.", "Mening fikrim shundan iborat.", "Fikrim shunday.", "Men shunday oʻylayman."),
("Qaysi qatorda soʻzlar tutuq belgisi bilan toʻgʻri yozilgan?", "maʼrifat, saʼy, jurʼat", "marifat, say, jurat", "maʼrifat, say, jurat", "maʻrifat, saʻy, jurʻat"),
("Sinonimik qatorda dominanta (asosiy soʻz) qanday boʻladi?", "Maʼnosi umumiy, uslubiy betaraf soʻz", "Eng kam ishlatiladigan soʻz", "Faqat eskirgan soʻz", "Faqat badiiy soʻz"),
("Eskirgan soʻzlarning predmeti yoʻqolgan turi qanday ataladi?", "Tarixiy soʻzlar (istorizm)", "Neologizm", "Arxaizm", "Dialektizm"),
("Hozirgi kunda boshqa soʻz bilan almashtirilgan eskirgan soʻz qanday ataladi?", "Arxaizm", "Istorizm", "Neologizm", "Jargon"),
("Yangi paydo boʻlgan soʻzlar qanday ataladi?", "Neologizm", "Arxaizm", "Istorizm", "Varvarizm"),
("Faqat muayyan hudud aholisiga xos soʻzlar qanday ataladi?", "Dialektizm (shevaga xos soʻz)", "Termin", "Arxaizm", "Neologizm"),
],
}


GEN7 = {
"d1": [
    ('«Oʻqituvchi» soʻzi nechta boʻgʻindan iborat?', '4 ta', '3 ta', '5 ta', '6 ta'),
    ('«Kitobxonlik» soʻzi nechta boʻgʻindan iborat?', '4 ta', '3 ta', '5 ta', '6 ta'),
    ('«Mehribonlik» soʻzida nechta boʻgʻin bor?', '4 ta', '3 ta', '5 ta', '2 ta'),
    ('«Maktab» soʻzi qaysi qatorda toʻgʻri boʻgʻinlangan?', 'mak-tab', 'ma-ktab', 'makt-ab', 'm-ak-tab'),
    ('«Qishloq» soʻzi qaysi qatorda toʻgʻri boʻgʻinlangan?', 'qish-loq', 'qi-shloq', 'qishl-oq', 'qis-hloq'),
    ('«Daryo» soʻzi qaysi qatorda toʻgʻri boʻgʻinlangan?', 'dar-yo', 'da-ryo', 'day-ro', 'd-aryo'),
    ('Oʻzbek tilida nechta unli tovush bor?', '6 ta', '5 ta', '8 ta', '9 ta'),
    ('Quyidagi harflardan qaysi biri unli emas?', 'y', 'a', 'oʻ', 'e'),
    ('Qaysi qatordagi barcha harflar undosh tovushni bildiradi?', 'b, d, q, r', 'a, b, d, q', 'e, k, l, m', 'i, t, s, n'),
    ('Qaysi soʻzda tutuq belgisi (ʼ) ishlatiladi?', 'maʼno', 'maktab', 'daryo', 'kitob'),
    ('«Kim?» soʻrogʻiga qaysi soʻz javob boʻladi?', 'Shifokor', 'Daftar', 'Daraxt', 'Kitob'),
    ('«Nima?» soʻrogʻiga qaysi soʻz javob boʻladi?', 'Deraza', 'Hamshira', 'Talaba', 'Sartarosh'),
    ('«Qanday?» soʻrogʻiga qaysi soʻz javob boʻladi?', 'mehribon', 'mehr', 'mehribonlik', 'mehrdan'),
    ('«Nima qildi?» soʻrogʻiga qaysi soʻz javob boʻladi?', 'yozdi', 'yozuv', 'yozuvchi', 'yozma'),
    ('«Oʻqidi» soʻzi qaysi soʻz turkumiga kiradi?', 'Feʼl', 'Ot', 'Sifat', 'Son'),
    ('«Beshta olma» birikmasidagi «beshta» qaysi soʻz turkumi?', 'Son', 'Ot', 'Sifat', 'Olmosh'),
    ('«Men, sen, u» soʻzlari qaysi soʻz turkumiga kiradi?', 'Olmosh', 'Ot', 'Son', 'Ravish'),
    ('«Juda chiroyli» birikmasidagi «juda» qaysi soʻz turkumi?', 'Ravish', 'Sifat', 'Ot', 'Feʼl'),
    ('Darak gap oxirida qaysi tinish belgisi qoʻyiladi?', 'Nuqta', 'Soʻroq belgisi', 'Vergul', 'Ikki nuqta'),
    ('Qaysi gap darak gap hisoblanadi?', 'Bahor keldi.', 'Bahor keldimi?', 'Bahor kelsin!', 'Voy, bahor keldi-ya!'),
    ('Ega qaysi soʻroqlarga javob boʻladi?', 'Kim? Nima?', 'Qayerda? Qachon?', 'Qanday? Qaysi?', 'Nima qildi?'),
    ('«Uka kitob oʻqidi.» gapida ega qaysi?', 'Uka', 'kitob', 'oʻqidi', 'Ega yoʻq'),
    ('«Qush uchib ketdi.» gapida kesim qaysi?', 'uchib ketdi', 'Qush', 'uchib', 'ketdi'),
    ('Quyidagilardan qaysi biri koʻplik qoʻshimchasi?', '-lar', '-ni', '-ga', '-chi'),
    ('Qaysi soʻzda egalik qoʻshimchasi bor?', 'kitobim', 'kitoblar', 'kitobga', 'kitobchi'),
    ('Qaysi soʻzda kelishik qoʻshimchasi bor?', 'uyga', 'uychi', 'uylar', 'uyim'),
    ('«Chiroyli» soʻzining sinonimi qaysi?', 'goʻzal', 'xunuk', 'yomon', 'past'),
    ('«Yorugʻ» soʻzining antonimi qaysi?', 'qorongʻi', 'ravshan', 'nurli', 'porloq'),
    ('Shakli bir xil, maʼnosi har xil soʻzlar qanday ataladi?', 'Omonim', 'Sinonim', 'Antonim', 'Paronim'),
    ('Maʼnosi bir-biriga yaqin soʻzlar qanday ataladi?', 'Sinonim', 'Omonim', 'Antonim', 'Termin'),
    ('Qarama-qarshi maʼnoli soʻzlar qanday ataladi?', 'Antonim', 'Sinonim', 'Omonim', 'Paronim'),
    ('Qaysi qatorda faqat otlar berilgan?', 'daftar, qalam, maktab', 'yugurdi, oʻqidi, yozdi', 'katta, kichik, yaxshi', 'men, sen, u'),
    ('Qaysi qatorda faqat sifatlar berilgan?', 'katta, shirin, yorugʻ', 'kitob, daftar, qalam', 'yozdi, oʻqidi, keldi', 'bir, ikki, uch'),
    ('Qaysi qatorda faqat feʼllar berilgan?', 'yozdi, keldi, oʻqidi', 'yozuv, kelish, oʻqish', 'yozuvchi, kelgan, oʻqigan', 'yoz, sen, u'),
    ('«Bolalar bogʻda oʻynashdi.» gapida nechta soʻz bor?', '3 ta', '2 ta', '4 ta', '5 ta'),
    ('«Mening kitobim» birikmasida «mening» qaysi olmosh?', 'Kishilik olmoshi', 'Koʻrsatish olmoshi', 'Soʻroq olmoshi', 'Oʻzlik olmoshi'),
    ('«Bu kitob qiziq.» gapida «bu» qaysi turkumga kiradi?', 'Olmosh', 'Ot', 'Sifat', 'Ravish'),
    ('«Soat» soʻzi nechta boʻgʻindan iborat?', '2 ta', '1 ta', '3 ta', '4 ta'),
    ('«Muallim» soʻzi nechta boʻgʻindan iborat?', '3 ta', '2 ta', '4 ta', '5 ta'),
    ('«Oʻzbekiston» soʻzi nechta boʻgʻindan iborat?', '4 ta', '3 ta', '5 ta', '6 ta'),
    ('«Yoʻlovchi» soʻzi nechta boʻgʻindan iborat?', '3 ta', '2 ta', '4 ta', '5 ta'),
    ('«Gʻoya» soʻzi nechta boʻgʻindan iborat?', '2 ta', '3 ta', '4 ta', '1 ta'),
    ('«Shahar» soʻzida nechta tovush bor (sh — bitta tovush)?', '5 ta', '6 ta', '4 ta', '7 ta'),
    ('«Choy» soʻzida nechta tovush bor (ch — bitta tovush)?', '3 ta', '4 ta', '2 ta', '5 ta'),
    ('«Maktab» soʻzida nechta tovush bor?', '6 ta', '5 ta', '7 ta', '4 ta'),
    ('Qaysi soʻz ot?', 'ona', 'mehribon', 'oʻqidi', 'yaxshi'),
    ('Qaysi soʻz sifat?', 'yumshoq', 'daftar', 'yozdi', 'men'),
    ('Qaysi soʻz feʼl?', 'sakradi', 'sakrash joyi', 'sakragan bola', 'baland'),
    ('Qaysi soʻz son?', 'oʻn', 'bola', 'katta', 'yozdi'),
    ('Qaysi soʻz olmosh?', 'ular', 'olma', 'oʻqidi', 'chiroyli'),
    ('Qaysi soʻz ravish?', 'hozir', 'uy', 'chiroyli', 'yozdi'),
    ('«Necha?» soʻrogʻiga qaysi soʻz javob boʻladi?', 'besh', 'beshinchi', 'bola', 'katta'),
    ('«Nechanchi?» soʻrogʻiga qaysi soʻz javob boʻladi?', 'beshinchi', 'besh', 'beshta', 'olti'),
    ('«Qachon?» soʻrogʻiga qaysi soʻz javob boʻladi?', 'bugun', 'uyda', 'kitob', 'chiroyli'),
    ('«Qayerda?» soʻrogʻiga qaysi soʻz javob boʻladi?', 'uyda', 'uydan', 'uyga', 'uyning'),
    ('«Gul ochildi.» gapida kesim qaysi soʻz?', 'ochildi', 'Gul', 'Ikkalasi ham', 'Hech qaysi'),
    ('«Oʻquvchilar yozmoqda.» gapida ega qaysi soʻz?', 'Oʻquvchilar', 'yozmoqda', 'Ikkalasi ham', 'Ega yoʻq'),
    ('Quyidagilardan qaysi biri eng qisqa toʻliq gap boʻla oladi?', 'Tong otdi.', 'Tong.', 'Otdi.', 'Erta tong.'),
    ('Qaysi gap toʻgʻri yozilgan?', 'Bahor keldi.', 'bahor keldi.', 'Bahor keldi', 'bahor Keldi.'),
    ('Qaysi gap soʻroq gap?', 'Sen qayerdasan?', 'Sen uydasan.', 'Sen uyda boʻl.', 'Sen uydasan!'),
    ('«Olma, nok, uzum sotildi.» gapida vergul nima uchun qoʻyilgan?', 'Bir xil boʻlaklarni ajratish uchun', 'Gap tugaganini bildirish uchun', 'Soʻroq uchun', 'Koʻchirma uchun'),
    ('Kitob nomi imloda qanday belgi bilan yoziladi?', 'Qoʻshtirnoq ichida', 'Qavs ichida', 'Tire bilan', 'Hech qanday belgisiz'),
    ('«Yosh» soʻzining antonimi «qari». Qaysi juftlik ham antonim?', 'yangi — eski', 'uy — xona', 'katta — ulkan', 'chiroyli — goʻzal'),
    ('«Baxtli» soʻzining antonimi qaysi?', 'baxtsiz', 'xursand', 'shod', 'omadli'),
    ('«Ochiq» soʻzining antonimi qaysi?', 'yopiq', 'keng', 'toza', 'ravshan'),
    ('«Xursand» soʻzining sinonimi qaysi?', 'shod', 'xafa', 'gʻamgin', 'mahzun'),
    ('«Jasur» soʻzining sinonimi qaysi?', 'dovyurak', 'qoʻrqoq', 'bezovta', 'lanj'),
    ('«Dushman» soʻzining antonimi qaysi?', 'doʻst', 'raqib', 'yov', 'begona'),
    ('«Kitob» soʻzining I shaxs birlikdagi egalik shakli qaysi?', 'kitobim', 'kitobing', 'kitobi', 'kitobimiz'),
    ('«Uy» soʻzining III shaxs egalik shakli qaysi?', 'uyi', 'uyim', 'uying', 'uyimiz'),
    ('«Qalam» soʻziga tushum kelishigi qoʻshilsa, qaysi shakl hosil boʻladi?', 'qalamni', 'qalamga', 'qalamda', 'qalamning'),
    ('Qaysi soʻz toʻgʻri yozilgan?', 'oʻrdak', 'ordak', 'oʻrtak', 'oʻrdok'),
    ('«Gʻalaba» soʻzining toʻgʻri imlosi qaysi?', 'gʻalaba', 'galaba', 'gʻalabo', 'kʻalaba'),
    ('«Tuxum» soʻzining toʻgʻri imlosi qaysi?', 'tuxum', 'tuhum', 'tuxim', 'tuhim'),
    ('«Xalq» soʻzining toʻgʻri imlosi qaysi?', 'xalq', 'halq', 'xaliq', 'halk'),
    ('«Hovli» soʻzining toʻgʻri imlosi qaysi?', 'hovli', 'xovli', 'hovly', 'xovely'),
    ('«Mehnat» soʻzining toʻgʻri imlosi qaysi?', 'mehnat', 'mexnat', 'mehnaat', 'menhat'),
    ('«Baxt» soʻzining toʻgʻri imlosi qaysi?', 'baxt', 'baht', 'bakht', 'baxd'),
    ('Sifat qanday soʻroqqa javob beradi?', 'Qanday? Qaysi?', 'Kim? Nima?', 'Nima qildi?', 'Necha?'),
    ('Ot qanday soʻroqlarga javob beradi?', 'Kim? Nima?', 'Qanday? Qaysi?', 'Nima qildi?', 'Qachon?'),
    ('«Katta uyda yashayman» gapida «katta» qaysi soʻz turkumi?', 'Sifat', 'Ot', 'Feʼl', 'Ravish'),
],
"d2": [
    ('«Maktabdan» soʻzi qaysi kelishikda?', 'Chiqish kelishigi', 'Oʻrin-payt kelishigi', 'Joʻnalish kelishigi', 'Tushum kelishigi'),
    ('«Uyning» soʻzi qaysi kelishikda?', 'Qaratqich kelishigi', 'Tushum kelishigi', 'Bosh kelishik', 'Chiqish kelishigi'),
    ('«Bogʻda» soʻzi qaysi kelishikda?', 'Oʻrin-payt kelishigi', 'Chiqish kelishigi', 'Joʻnalish kelishigi', 'Qaratqich kelishigi'),
    ('«Shaharga» soʻzi qaysi kelishikda?', 'Joʻnalish kelishigi', 'Oʻrin-payt kelishigi', 'Tushum kelishigi', 'Bosh kelishik'),
    ('Qaysi kelishikning maxsus qoʻshimchasi yoʻq?', 'Bosh kelishik', 'Tushum kelishigi', 'Joʻnalish kelishigi', 'Chiqish kelishigi'),
    ('«-da» qoʻshimchasi qaysi soʻroqqa javob beradi?', 'Qayerda? Qachon?', 'Qayerga? Kimga?', 'Qayerdan? Kimdan?', 'Kimning? Nimaning?'),
    ('Qaratqich kelishigi qaysi soʻroqlarga javob beradi?', 'Kimning? Nimaning?', 'Kimni? Nimani?', 'Kimga? Nimaga?', 'Kimda? Nimada?'),
    ('Qaysi soʻzda joʻnalish kelishigi qoʻshimchasi toʻgʻri yozilgan?', 'qishloqqa', 'qishloqga', 'qishloqka', 'qishloqgʻa'),
    ('«Tok» soʻziga joʻnalish kelishigi qoʻshilganda qaysi imlo toʻgʻri?', 'tokka', 'tokga', 'tokqa', 'tokgʻa'),
    ('Sanoq soʻzi bilan kelgan otning qaysi shakli toʻgʻri? (besh ...)', 'besh kitob', 'besh kitoblar', 'beshta kitoblar', 'besh ta kitoblar'),
    ('Sanoq soʻzi bilan kelgan otning qaysi shakli toʻgʻri? (yigirma ...)', 'yigirma talaba', 'yigirma talabalar', 'yigirma ta talabalar', 'yigirmata talabalar'),
    ('«Kitobim» soʻzidagi egalik qoʻshimchasi qaysi shaxs va sonda?', 'I shaxs, birlik', 'II shaxs, birlik', 'I shaxs, koʻplik', 'III shaxs, birlik'),
    ('«Kitobingiz» soʻzidagi egalik qoʻshimchasi qaysi shaxsni bildiradi?', 'II shaxs (hurmat)', 'I shaxs, birlik', 'III shaxs, koʻplik', 'I shaxs, koʻplik'),
    ('«Kitobimiz» soʻzidagi egalik qoʻshimchasi qaysi shaxs va sonda?', 'I shaxs, koʻplik', 'I shaxs, birlik', 'II shaxs, koʻplik', 'III shaxs, birlik'),
    ('Qaysi yozuv «shahar» soʻzining toʻgʻri imlosi?', 'shahar', 'shaxar', 'sahar', 'shaxr'),
    ('Qaysi yozuv «hayot» soʻzining toʻgʻri imlosi?', 'hayot', 'xayot', 'hayat', 'xayat'),
    ('Qaysi yozuv «maʼruza» soʻzining toʻgʻri imlosi?', 'maʼruza', 'maruza', 'maʼruzza', 'mauruza'),
    ('Qaysi yozuv «oʻqituvchi» soʻzining toʻgʻri imlosi?', 'oʻqituvchi', 'oqituvchi', 'oʻkituvchi', 'oʻqitubchi'),
    ('Gapda kesim odatda qaysi soʻz turkumi bilan ifodalanadi?', 'Feʼl', 'Ravish', 'Koʻmakchi', 'Yuklama'),
    ('Gapda ega koʻpincha qaysi soʻz turkumi bilan ifodalanadi?', 'Ot', 'Feʼl', 'Ravish', 'Yuklama'),
    ('«Oʻtkir qalam» birikmasida «oʻtkir» qaysi gap boʻlagi?', 'Aniqlovchi', 'Hol', 'Toʻldiruvchi', 'Kesim'),
    ('«U tez yugurdi.» gapida «tez» qaysi gap boʻlagi?', 'Hol', 'Aniqlovchi', 'Toʻldiruvchi', 'Ega'),
    ('«U kitobni oʻqidi.» gapida «kitobni» qaysi gap boʻlagi?', 'Toʻldiruvchi', 'Hol', 'Ega', 'Kesim'),
    ('Gapning bosh boʻlaklari qaysilar?', 'Ega va kesim', 'Aniqlovchi va hol', 'Toʻldiruvchi va hol', 'Ega va toʻldiruvchi'),
    ('Gapning ikkinchi darajali boʻlaklari qaysilar?', 'Aniqlovchi, toʻldiruvchi, hol', 'Ega, kesim', 'Ega, aniqlovchi', 'Kesim, hol'),
    ('Gap boʻlaklari nechta turga boʻlinadi (ega, kesim, aniqlovchi, toʻldiruvchi, hol)?', '5 ta', '4 ta', '6 ta', '3 ta'),
    ('Qaysi juftlik sinonim?', 'oʻqituvchi — muallim', 'issiq — sovuq', 'katta — kichik', 'kun — tun'),
    ('Qaysi juftlik antonim?', 'issiq — sovuq', 'vatan — yurt', 'chiroyli — goʻzal', 'mard — jasur'),
    ('«Tez» soʻzining antonimi qaysi?', 'sekin', 'chaqqon', 'darrov', 'ildam'),
    ('«Shirin» soʻzining antonimi qaysi?', 'achchiq', 'mazali', 'totli', 'yoqimli'),
    ('«Keng» soʻzining antonimi qaysi?', 'tor', 'ulkan', 'yirik', 'uzun'),
    ('«Boy» soʻzining antonimi qaysi?', 'kambagʻal', 'badavlat', 'davlatmand', 'tuqqan'),
    ('«Dono» soʻzining sinonimi qaysi?', 'aqlli', 'ahmoq', 'nodon', 'johil'),
    ('Bir turdagi sanalayotgan gap boʻlaklari orasida qaysi tinish belgisi qoʻyiladi?', 'Vergul', 'Ikki nuqta', 'Nuqtali vergul', 'Qoʻshtirnoq'),
    ('Qaysi gapda ega soʻz bilan ifodalangan emas, balki yashirin (ifodalanmagan)?', 'Maktabga bordim.', 'Men maktabga bordim.', 'Ali maktabga bordi.', 'U maktabga bordi.'),
    ('«U kitobdan oʻqidi.» gapida «kitobdan» qaysi kelishikda?', 'Chiqish kelishigi', 'Oʻrin-payt kelishigi', 'Joʻnalish kelishigi', 'Tushum kelishigi'),
    ('«Men kitobni oldim.» gapida tushum kelishigidagi soʻz qaysi?', 'kitobni', 'Men', 'oldim', 'Hech qaysi'),
    ('«Bolalarning» soʻzida qoʻshimchalar tartibi qanday?', '-lar (koʻplik) + -ning (kelishik)', '-ning + -lar', '-lar + -ni', '-ni + -lar'),
    ('«Kitobimdan» soʻzida qanday qoʻshimchalar bor?', 'I shaxs egalik + chiqish kelishigi', 'II shaxs egalik + tushum kelishigi', 'Koʻplik + joʻnalish kelishigi', 'I shaxs egalik + oʻrin-payt kelishigi'),
    ('«Daftaringga» soʻzida qanday qoʻshimchalar bor?', 'II shaxs egalik + joʻnalish kelishigi', 'I shaxs egalik + tushum kelishigi', 'III shaxs egalik + chiqish kelishigi', 'Koʻplik + qaratqich kelishigi'),
    ('«Uyimizda» soʻzida qanday qoʻshimchalar bor?', 'I shaxs koʻplik egalik + oʻrin-payt kelishigi', 'I shaxs birlik egalik + oʻrin-payt kelishigi', 'II shaxs egalik + joʻnalish kelishigi', 'Koʻplik + tushum kelishigi'),
    ('Qaysi birikmada xato bor?', 'ikki bolalar', 'ikki bola', 'ikkita bola', 'bolalar'),
    ('«Ona» soʻzining sinonimi qaysi?', 'oyi', 'ota', 'opa', 'bola'),
    ('«Mehnatkash» soʻzining sinonimi qaysi?', 'tirishqoq', 'dangasa', 'boʻsh', 'yalqov'),
    ('«Qoʻrqoq» soʻzining antonimi qaysi?', 'jasur', 'ojiz', 'tortinchoq', 'bezovta'),
    ('«Past» soʻzining antonimi qaysi?', 'baland', 'chuqur', 'tor', 'kichik'),
    ('«Ochlik» soʻzining antonimi qaysi?', 'toʻqlik', 'ishtaha', 'chanqoqlik', 'tashnalik'),
    ('«Kelmoq» feʼlining antonimi qaysi?', 'ketmoq', 'kirmoq', 'yetmoq', 'tushmoq'),
    ('«Kulmoq» feʼlining antonimi qaysi?', 'yigʻlamoq', 'shodlanmoq', 'tabassum qilmoq', 'yayramoq'),
    ('«Qoʻshmoq» feʼlining antonimi qaysi?', 'ayirmoq', 'birlashtirmoq', 'yigʻmoq', 'boʻlmoq'),
    ('«Anvar va Salim maktabga bordi.» gapida ega qaysi?', 'Anvar va Salim', 'maktabga', 'bordi', 'Salim'),
    ('«Maktabda darslar boshlandi.» gapida ega qaysi?', 'darslar', 'Maktabda', 'boshlandi', 'Maktabda darslar'),
    ('«Osmonda yulduzlar charaqlaydi.» gapida kesim qaysi?', 'charaqlaydi', 'yulduzlar', 'Osmonda', 'Osmonda yulduzlar'),
    ('«Havo ochiq.» gapida kesim qaysi soʻz turkumi bilan ifodalangan?', 'Sifat', 'Ot', 'Feʼl', 'Son'),
    ('«Bahor — yilning eng goʻzal fasli.» gapida tire nima uchun qoʻyilgan?', 'Ega va kesim ot bilan ifodalangan', 'Gap soʻroq', 'Koʻchirma gap', 'Uyushiq boʻlaklar bor'),
    ('«Darsni tez tugat!» gapi maqsadiga koʻra qaysi turga kiradi?', 'Buyruq gap', 'Darak gap', 'Soʻroq gap', 'Shart gap'),
    ('«Qanday goʻzal!» gapi qaysi turga kiradi?', 'Undov gap', 'Soʻroq gap', 'Buyruq gap', 'Shart gap'),
    ('Qaysi soʻz toʻgʻri yozilgan?', 'meʼyor', 'meyor', 'meʼor', 'meʼyyor'),
    ('«Ehtiyot» soʻzining toʻgʻri imlosi qaysi?', 'ehtiyot', 'extiyot', 'ehtiyod', 'extiyod'),
    ('«Hamkor» soʻzining toʻgʻri imlosi qaysi?', 'hamkor', 'xamkor', 'hamqor', 'xamqor'),
    ('«Xabar» soʻzining toʻgʻri imlosi qaysi?', 'xabar', 'habar', 'xabbar', 'habbar'),
    ('«Hukumat» soʻzining toʻgʻri imlosi qaysi?', 'hukumat', 'xukumat', 'hukimat', 'xukimat'),
    ('«Xizmat» soʻzining toʻgʻri imlosi qaysi?', 'xizmat', 'hizmat', 'xizmet', 'hizmet'),
    ('«Hurmat» soʻzining toʻgʻri imlosi qaysi?', 'hurmat', 'xurmat', 'hurmet', 'xurmet'),
    ('«Gʻazal» soʻzining toʻgʻri imlosi qaysi?', 'gʻazal', 'gazal', 'gʻazel', 'kʻazal'),
    ('Qaysi soʻz doim bosh harf bilan yoziladi?', 'Samarqand', 'daryo', 'shahar', 'togʻ'),
    ('Til nomi qaysi yozuvda toʻgʻri berilgan?', 'oʻzbek tili', 'Oʻzbek Tili', 'OʻZBEK tili', 'oʻzbek Tili'),
    ('Qaysi soʻz bir boʻgʻinli?', 'ot', 'kitob', 'maktab', 'daftar'),
    ('«Kitob» soʻzi qanday boʻgʻinlanadi?', 'ki-tob', 'kit-ob', 'k-itob', 'kito-b'),
    ('Qaysi birikmada egalik qoʻshimchasi III shaxsni bildiradi?', 'uning uyi', 'mening uyim', 'sening uying', 'bizning uyimiz'),
    ('«Bola oʻynadi.» gapida nechta soʻz turkumi bor (soʻzlar turkumi)?', '2 ta: ot va feʼl', '1 ta', '3 ta', '4 ta'),
    ('«Kitob» soʻziga «-lar» va «-im» qoʻshilsa, qaysi tartib toʻgʻri?', 'kitoblarim', 'kitobimlar', 'kitoblarmi', 'kitobmlar'),
    ('«Sinfdosh» soʻzi qanday soʻz?', 'Yasama soʻz', 'Sodda soʻz', 'Juft soʻz', 'Takroriy soʻz'),
    ('«Yaxshi» soʻzi qaysi turkumga kiradi?', 'Sifat', 'Ot', 'Feʼl', 'Son'),
    ('Gapda ikkinchi darajali boʻlak qaysi?', 'Aniqlovchi', 'Ega', 'Kesim', 'Bosh boʻlak'),
    ('«Qalam» soʻzida nechta boʻgʻin bor?', '2 ta', '1 ta', '3 ta', '4 ta'),
    ('«Ota-ona» soʻzining yozilishi qanday?', 'Chiziqcha bilan', 'Qoʻshib', 'Ajratib', 'Qavs bilan'),
    ('«Katta bola» birikmasi qaysi turkumlardan tuzilgan?', 'Sifat + ot', 'Ot + feʼl', 'Ravish + feʼl', 'Son + ot'),
],
"d3": [
    ('«Ishchi» soʻzidagi «-chi» qoʻshimchasi qanday vazifa bajaradi?', 'Ot yasaydi', 'Sifat yasaydi', 'Feʼl yasaydi', 'Shakl yasaydi'),
    ('«Kuchli» soʻzidagi «-li» qoʻshimchasi qaysi turkumni yasagan?', 'Sifat', 'Ot', 'Feʼl', 'Ravish'),
    ('«Kuchsiz» soʻzidagi «-siz» qoʻshimchasi qaysi turkumni yasagan?', 'Sifat', 'Ot', 'Feʼl', 'Son'),
    ('«Sinfdosh» soʻzidagi «-dosh» qoʻshimchasi qaysi turkumni yasagan?', 'Ot', 'Sifat', 'Feʼl', 'Ravish'),
    ('«Ijodkor» soʻzidagi «-kor» qoʻshimchasi qaysi turkumni yasagan?', 'Ot', 'Sifat', 'Feʼl', 'Olmosh'),
    ('«Doʻstlik» soʻzidagi «-lik» qoʻshimchasi qaysi turkumni yasagan?', 'Ot', 'Sifat', 'Feʼl', 'Ravish'),
    ('«Ishla» soʻzidagi «-la» qoʻshimchasi qaysi turkumni yasagan?', 'Feʼl', 'Ot', 'Sifat', 'Son'),
    ('Qaysi soʻz yasama soʻz hisoblanadi?', 'kitobxon', 'kitob', 'qalam', 'daryo'),
    ('Qaysi soʻz sodda (yasalmagan) soʻz?', 'tosh', 'toshloq', 'toshli', 'toshchi'),
    ('Qaysi soʻz qoʻshma soʻz hisoblanadi?', 'temiryoʻl', 'ota-ona', 'qator-qator', 'OʻzMU'),
    ('Qaysi soʻz juft soʻz hisoblanadi?', 'ota-ona', 'temiryoʻl', 'qator-qator', 'BMT'),
    ('Qaysi soʻz takroriy soʻz hisoblanadi?', 'qator-qator', 'ota-ona', 'kitobxon', 'koʻzoynak'),
    ('Qaysi soʻz qisqartma soʻz hisoblanadi?', 'BMT', 'ota-ona', 'qator-qator', 'boshqaruv'),
    ('Soʻzning qoʻshimchalarsiz, asosiy maʼno bildiruvchi qismi nima deb ataladi?', 'Oʻzak', 'Qoʻshimcha', 'Negiz', 'Qoʻshma'),
    ('«Yozuvchi» soʻzining tarkibi qaysi javobda toʻgʻri koʻrsatilgan?', 'yoz + uv + chi', 'yozuv + ch + i', 'yo + zuvchi', 'yozu + vchi'),
    ('«Kitoblarimizdan» soʻzida qoʻshimchalar tartibi qaysi?', 'koʻplik + egalik + kelishik', 'kelishik + egalik + koʻplik', 'egalik + koʻplik + kelishik', 'koʻplik + kelishik + egalik'),
    ('«Daftarlarimda» soʻzidagi qoʻshimchalar qaysi tartibda?', '-lar, -im, -da', '-im, -lar, -da', '-da, -lar, -im', '-lar, -da, -im'),
    ('Qaysi soʻzda qoʻshimchalar tartibi buzilgan?', 'kitobdanlarim', 'kitoblarimdan', 'kitobimdan', 'kitoblardan'),
    ('«Oʻqidi» feʼli qaysi zamonda?', 'Aniq oʻtgan zamon', 'Hozirgi zamon', 'Kelasi zamon', 'Shart mayli'),
    ('«Oʻqiyapti» feʼli qaysi zamonda?', 'Hozirgi zamon (davomiy)', 'Oʻtgan zamon', 'Kelasi zamon', 'Buyruq mayli'),
    ('«Oʻqiydi» feʼli qaysi zamon shaklida?', 'Hozirgi-kelasi zamon', 'Oʻtgan zamon', 'Shart mayli', 'Buyruq mayli'),
    ('«Oʻqimoqchi» shakli qaysi zamon maʼnosini bildiradi?', 'Kelasi zamon (maqsad)', 'Oʻtgan zamon', 'Hozirgi zamon', 'Buyruq'),
    ('«Oʻqisa» shakli qaysi maylga kiradi?', 'Shart mayli', 'Buyruq-istak mayli', 'Aniqlik mayli', 'Sifatdosh'),
    ('«Oʻqisin» shakli qaysi maylga kiradi?', 'Buyruq-istak mayli', 'Shart mayli', 'Aniqlik mayli', 'Sifatdosh'),
    ('«Yozildi» feʼli qaysi nisbatda?', 'Majhul nisbat', 'Oʻzlik nisbati', 'Orttirma nisbat', 'Birgalik nisbati'),
    ('«Yozishdi» feʼli qaysi nisbatda?', 'Birgalik nisbati', 'Orttirma nisbat', 'Majhul nisbat', 'Oʻzlik nisbati'),
    ('«Biz oʻqidik» gapida kesim qaysi shaxs va sonda?', 'I shaxs, koʻplik', 'I shaxs, birlik', 'II shaxs, koʻplik', 'III shaxs, koʻplik'),
    ('«Siz keldingiz» gapida kesim qaysi shaxsda?', 'II shaxs', 'I shaxs', 'III shaxs', 'Shaxssiz'),
    ('Quyidagilardan qaysi biri harakat nomi?', 'oʻqish', 'oʻqigan', 'oʻqib', 'oʻqidi'),
    ('«-gan» qoʻshimchali shakl qaysi feʼl shakliga kiradi?', 'Sifatdosh', 'Ravishdosh', 'Harakat nomi', 'Shart mayli'),
    ('«Kelib» shakli qaysi feʼl shakliga kiradi?', 'Ravishdosh', 'Sifatdosh', 'Harakat nomi', 'Buyruq mayli'),
    ('«Oʻqigach» shakli qaysi feʼl shakliga kiradi?', 'Ravishdosh', 'Sifatdosh', 'Harakat nomi', 'Aniqlik mayli'),
    ('«Oʻqiydigan bola» birikmasidagi «oʻqiydigan» qaysi feʼl shakli?', 'Sifatdosh', 'Ravishdosh', 'Harakat nomi', 'Buyruq mayli'),
    ('«Bu yil bahor erta keldi.» gapida «bu yil» qaysi gap boʻlagi?', 'Payt holi', 'Oʻrin holi', 'Aniqlovchi', 'Ega'),
    ('«U maktabda oʻqiydi.» gapida «maktabda» qaysi hol?', 'Oʻrin holi', 'Payt holi', 'Sabab holi', 'Holat holi'),
    ('«Yomgʻir tufayli yoʻl buzildi.» gapida «yomgʻir tufayli» qaysi hol?', 'Sabab holi', 'Payt holi', 'Oʻrin holi', 'Maqsad holi'),
    ('«Bilim olish uchun maktabga boramiz.» gapida «bilim olish uchun» qaysi hol?', 'Maqsad holi', 'Sabab holi', 'Payt holi', 'Oʻrin holi'),
    ('«Mening kitobim» birikmasida «mening» qaysi gap boʻlagi?', 'Qaratqich aniqlovchi', 'Sifatlovchi aniqlovchi', 'Toʻldiruvchi', 'Hol'),
    ('«Oʻtkir qalam» birikmasidagi «oʻtkir» qaysi aniqlovchi?', 'Sifatlovchi aniqlovchi', 'Qaratqich aniqlovchi', 'Izohlovchi', 'Toʻldiruvchi'),
    ('«Shoir Alisher Navoiy» birikmasida «shoir» qaysi gap boʻlagi?', 'Izohlovchi', 'Qaratqich aniqlovchi', 'Hol', 'Toʻldiruvchi'),
    ('«Bu — kitob.» gapida kesim qaysi turga kiradi?', 'Ot kesim', 'Feʼl kesim', 'Sifat kesim', 'Ravish kesim'),
    ('«Dilnoza oʻqituvchi.» gapida kesim qanday ifodalangan?', 'Ot bilan', 'Feʼl bilan', 'Ravish bilan', 'Olmosh bilan'),
    ('«Katta uy» birikmasi qaysi turga kiradi?', 'Ot birikma (otli birikma)', 'Feʼl birikma', 'Ravish birikma', 'Qoʻshma gap'),
    ('«Kitob oʻqimoq» birikmasi qaysi turga kiradi?', 'Feʼl birikma (feʼlli birikma)', 'Ot birikma', 'Sifat birikma', 'Sodda gap'),
    ('Oʻzbek tilidagi gapda kesim odatda qayerda keladi?', 'Gap oxirida', 'Gap boshida', 'Gap oʻrtasida', 'Ega oldida'),
    ('Soʻz birikmasida asosiy maʼnoni ifodalovchi soʻz qanday ataladi?', 'Hokim soʻz', 'Tobe soʻz', 'Qoʻshma soʻz', 'Yasama soʻz'),
    ('Hokim soʻzga tobelanib, uni toʻldirib keluvchi soʻz qanday ataladi?', 'Tobe soʻz', 'Hokim soʻz', 'Yasovchi soʻz', 'Oʻzak soʻz'),
    ('«Olma» soʻzida «-ni» qoʻshimchasi qoʻshilsa, qaysi shakl hosil boʻladi?', 'Tushum kelishigi', 'Qaratqich kelishigi', 'Chiqish kelishigi', 'Joʻnalish kelishigi'),
    ('«U kitob oʻqidi.» gapida nechta gap boʻlagi bor?', '3 ta', '2 ta', '4 ta', '5 ta'),
    ('«Anvar yangi kitobni diqqat bilan oʻqidi.» gapida nechta gap boʻlagi bor?', '5 ta', '4 ta', '6 ta', '3 ta'),
    ('«Anvar yangi kitobni diqqat bilan oʻqidi.» gapida «diqqat bilan» qaysi hol?', 'Holat holi', 'Payt holi', 'Oʻrin holi', 'Sabab holi'),
    ('«Ertaga imtihon boʻladi.» gapida «ertaga» qaysi gap boʻlagi?', 'Payt holi', 'Ega', 'Toʻldiruvchi', 'Aniqlovchi'),
    ('«Qizil olma» birikmasida «qizil» qaysi soʻz turkumi?', 'Sifat', 'Ot', 'Feʼl', 'Ravish'),
    ('Qaysi gapda toʻldiruvchi bor?', 'Ali xatni yozdi.', 'Ali keldi.', 'Ali kasal.', 'Ali tez keldi.'),
    ('Qaysi gapda hol bor?', 'Ali tez keldi.', 'Ali xatni yozdi.', 'Ali kasal.', 'Ali kitobni oldi.'),
    ('Qaysi gapda aniqlovchi bor?', 'Yangi kitob keldi.', 'Kitob keldi.', 'Ali keldi.', 'U keldi.'),
    ('Qaysi gap faqat ega va kesimdan iborat?', 'Bahor keldi.', 'Erta bahor keldi.', 'Bahor erta keldi.', 'Bahor shahrimizga keldi.'),
    ('Ega va kesim orasida tire qachon qoʻyiladi?', 'Ikkalasi ham ot yoki sonlar bilan ifodalanganda: Ona — Vatan.', 'Ega feʼl bilan ifodalanganda', 'Kesim feʼl bilan ifodalanganda', 'Hamma gaplarda'),
    ('Qaysi gapda ega va kesim orasiga tire qoʻyiladi?', 'Toshkent — Oʻzbekistonning poytaxti.', 'U kitob oʻqiyapti.', 'Bahor keldi.', 'Ali tez yuguradi.'),
    ('«Gulzor» soʻzidagi «-zor» qoʻshimchasi qanday maʼno bildiradi?', 'Oʻsimlik koʻp joy nomini', 'Kasb-hunar egasini', 'Belgi-xususiyatni', 'Harakat nomini'),
    ('«Kitobxona» soʻzidagi «-xona» qoʻshimchasi qanday maʼno bildiradi?', 'Joy nomini', 'Kasb egasini', 'Belgi-xususiyatni', 'Harakat nomini'),
    ('Feʼlning inkor (boʻlishsiz) shaklini yasovchi qoʻshimcha qaysi?', '-ma', '-la', '-lan', '-ish'),
    ('«Gapchan» soʻzidagi «-chan» qoʻshimchasi qaysi turkumni yasagan?', 'Sifat', 'Ot', 'Feʼl', 'Ravish'),
    ('«Oʻqish — foydali.» gapida ega qaysi feʼl shakli bilan ifodalangan?', 'Harakat nomi', 'Sifatdosh', 'Ravishdosh', 'Shart mayli'),
    ('«Yaxshilar topishar.» gapida ega qaysi soʻz turkumidan otlashgan?', 'Sifat', 'Feʼl', 'Ravish', 'Son'),
    ('«Yoz» feʼli qaysi shaxs va sondagi buyruq shaklini bildiradi?', 'II shaxs, birlik', 'I shaxs, birlik', 'III shaxs, birlik', 'II shaxs, koʻplik'),
    ('«Kelmadi» soʻzida «-ma» qoʻshimchasi qanday vazifa bajaradi?', 'Inkor (boʻlishsizlik) bildiradi', 'Nisbat yasaydi', 'Zamon bildiradi', 'Shaxs bildiradi'),
    ('«Kitobingni» soʻzida nechta qoʻshimcha bor?', '2 ta', '1 ta', '3 ta', '4 ta'),
    ('«Anvarning» soʻzidagi «-ning» qoʻshimchasi qaysi kelishik qoʻshimchasi?', 'Qaratqich kelishigi', 'Tushum kelishigi', 'Joʻnalish kelishigi', 'Chiqish kelishigi'),
    ('«-roq» qoʻshimchasi (kattaroq) nimani bildiradi?', 'Qiyosiy darajani', 'Kamaytirma darajani', 'Koʻplikni', 'Egalikni'),
    ('«Qizgina» soʻzidagi «-gina» qoʻshimchasi qanday maʼno beradi?', 'Kichraytirish-erkalash', 'Koʻplik', 'Inkor', 'Oʻxshatish'),
    ('«Kitobcha» soʻzidagi «-cha» qoʻshimchasi qanday maʼno beradi?', 'Kichraytirish', 'Kattalashtirish', 'Inkor', 'Zamon'),
    ('«Gulday» soʻzidagi «-day» qoʻshimchasi qanday maʼno beradi?', 'Oʻxshatish', 'Koʻplik', 'Inkor', 'Kichraytirish'),
    ('«Beshta» soʻzidagi «-ta» qoʻshimchasi qanday maʼno beradi?', 'Dona (sanoq) maʼnosini', 'Tartib maʼnosini', 'Chama maʼnosini', 'Inkor maʼnosini'),
    ('«Oltinchi» soʻzidagi «-nchi» (-inchi) qoʻshimchasi qaysi turkum shaklini yasaydi?', 'Tartib son', 'Sanoq son', 'Chama son', 'Sifatdosh'),
    ('«Maktabdagi bolalar» birikmasida «maktabdagi» qaysi gap boʻlagi?', 'Aniqlovchi', 'Hol', 'Toʻldiruvchi', 'Ega'),
    ('«Keling» shakli qaysi maylga kiradi?', 'Buyruq-istak mayli', 'Shart mayli', 'Aniqlik mayli', 'Sifatdosh'),
    ('«Oʻqiyman» shakli qaysi shaxs va son hamda zamonda?', 'I shaxs, birlik, hozirgi-kelasi zamon', 'II shaxs, birlik, oʻtgan zamon', 'III shaxs, birlik, kelasi zamon', 'I shaxs, koʻplik, oʻtgan zamon'),
    ('Quyidagilardan qaysi biri harakat nomi yasovchi qoʻshimcha emas?', '-gan', '-ish', '-moq', '-v'),
    ('Quyidagi qoʻshimchalardan qaysi biri sifatdosh yasamaydi?', '-ib', '-gan', '-uvchi', '-adigan'),
    ('Quyidagi qoʻshimchalardan qaysi biri ravishdosh yasamaydi?', '-uvchi', '-ib', '-gach', '-guncha'),
    ('Aniqlovchi qaysi soʻroqlarga javob beradi?', 'Qanday? Qaysi? Kimning?', 'Kimni? Nimani?', 'Qachon? Qayerda?', 'Nima qildi?'),
    ('Toʻldiruvchi qaysi soʻroqlarga javob beradi?', 'Kimni? Nimani? Kimga? Nimaga?', 'Qanday? Qaysi?', 'Qachon? Qayerda?', 'Kim? Nima?'),
    ('«Kitobni oʻqimoq» birikmasida tobe soʻz hokim soʻzga qaysi usul bilan bogʻlangan?', 'Boshqaruv', 'Moslashuv', 'Bitishuv', 'Qoʻshma'),
    ('«Katta uy» birikmasida tobe soʻz hokim soʻzga qaysi usul bilan bogʻlangan?', 'Bitishuv', 'Boshqaruv', 'Moslashuv', 'Takror'),
    ('«Mening uyim» birikmasida tobe soʻz hokim soʻzga qaysi usul bilan bogʻlangan?', 'Moslashuv', 'Boshqaruv', 'Bitishuv', 'Takror'),
    ('Oʻzbek tilida aniqlovchi aniqlanmishga nisbatan qayerda keladi?', 'Oldida', 'Orqasida', 'Gap oxirida', 'Gap boshida'),
    ('«Biz keldik.» gapida ega qaysi soʻz turkumi bilan ifodalangan?', 'Olmosh', 'Ot', 'Son', 'Sifat'),
    ('«Ishlay boshladi» kesimi qaysi turga kiradi?', 'Murakkab feʼl kesim', 'Sodda feʼl kesim', 'Ot kesim', 'Sifat kesim'),
    ('«Xabar bermoq» birikmasi qaysi turdagi feʼl?', 'Qoʻshma feʼl', 'Juft feʼl', 'Sodda feʼl', 'Takroriy feʼl'),
    ('Bir xil soʻroqqa javob beradigan va bir boʻlakka tobelanuvchi boʻlaklar qanday ataladi?', 'Uyushiq boʻlaklar', 'Ajratilgan boʻlaklar', 'Izohlovchi boʻlaklar', 'Bosh boʻlaklar'),
    ('«Anvar, Salim va Karim keldi.» gapida nechta ega bor?', '3 ta (uyushiq ega)', '1 ta', '2 ta', 'Ega yoʻq'),
    ('Uyushiq boʻlaklar orasida «va» bogʻlovchisi kelsa, undan oldin qanday tinish belgisi qoʻyilmaydi?', 'Vergul', 'Nuqta', 'Undov belgisi', 'Soʻroq belgisi'),
    ('«Oʻzbekiston» soʻzidagi «-iston» qoʻshimchasi qanday maʼno beradi?', 'Joy, mamlakat nomi', 'Kasb nomi', 'Belgi', 'Harakat'),
    ('«Yaxshilik» soʻzi qaysi turkumdan qaysi turkum yasalgan?', 'Sifatdan ot', 'Otdan sifat', 'Feʼldan ot', 'Otdan feʼl'),
    ('«Yozuv» soʻzi qaysi turkumdan qaysi turkum yasalgan?', 'Feʼldan ot', 'Sifatdan ot', 'Otdan feʼl', 'Otdan sifat'),
    ('«Ishchan» soʻzi qaysi turkumdan qaysi turkum yasalgan?', 'Otdan sifat', 'Feʼldan ot', 'Sifatdan ot', 'Otdan ravish'),
    ('«Tinchlik» soʻzi qaysi turkumdan qaysi turkum yasalgan?', 'Sifatdan ot', 'Otdan sifat', 'Feʼldan sifat', 'Otdan feʼl'),
    ('«Bilim» soʻzi qaysi turkumdan qaysi turkum yasalgan?', 'Feʼldan ot', 'Otdan feʼl', 'Sifatdan ot', 'Otdan sifat'),
    ('Qaysi gapda feʼl kesim sodda shaklda?', 'Quyosh chiqdi.', 'U ishlay boshladi.', 'U oʻqituvchi.', 'Bu — kitob.'),
    ('«Kitob — bilim manbai.» gapida kesim qaysi turga kiradi?', 'Ot kesim', 'Sodda feʼl kesim', 'Murakkab feʼl kesim', 'Ravish kesim'),
    ('«Uyga keldim.» gapida «uyga» qaysi gap boʻlagi?', 'Oʻrin holi', 'Toʻldiruvchi', 'Aniqlovchi', 'Ega'),
    ('«Men senga kitob berdim.» gapida «senga» qaysi gap boʻlagi?', 'Toʻldiruvchi', 'Hol', 'Aniqlovchi', 'Ega'),
    ('«Bola kitob oʻqiyapti.» gapida nechta gap boʻlagi bor?', '3 ta', '2 ta', '4 ta', '5 ta'),
    ('«Katta bola yangi kitobni oʻqidi.» gapida nechta gap boʻlagi bor?', '5 ta', '3 ta', '4 ta', '6 ta'),
    ('Toʻldiruvchi qaysi kelishiklar bilan koʻp ifodalanadi?', 'Tushum, joʻnalish, oʻrin-payt, chiqish', 'Faqat bosh kelishik', 'Faqat qaratqich kelishigi', 'Kelishik qoʻshimchasiz'),
    ('Quyidagi birikmalardan qaysi biri toʻgʻri tuzilgan?', 'uch kitob', 'uch kitoblar', 'uchlar kitob', 'uchta kitoblar'),
    ('«Bogʻbon» soʻzidagi «-bon» qoʻshimchasi qanday maʼno beradi?', 'Kasb-hunar egasini', 'Joy nomini', 'Belgi-xususiyatni', 'Harakat nomini'),
    ('«Aqlli» soʻzi qaysi turkumdan qaysi turkum yasalgan?', 'Otdan sifat', 'Sifatdan ot', 'Feʼldan sifat', 'Otdan feʼl'),
    ('«Qoʻl-oyoq» soʻzi tuzilishiga koʻra qaysi turga kiradi?', 'Juft soʻz', 'Qoʻshma soʻz', 'Takroriy soʻz', 'Sodda soʻz'),
    ('«Toʻp-toʻp» soʻzi tuzilishiga koʻra qaysi turga kiradi?', 'Takroriy soʻz', 'Juft soʻz', 'Qoʻshma soʻz', 'Qisqartma soʻz'),
    ('«Oʻqituvchi» soʻzidagi «-t» qoʻshimchasi qaysi nisbat belgisi?', 'Orttirma nisbat', 'Majhul nisbat', 'Oʻzlik nisbati', 'Birgalik nisbati'),
    ('«Yozilgan» soʻzida qanday qoʻshimchalar bor?', '-il (majhul nisbat) + -gan (sifatdosh)', '-ish (birgalik) + -gan', '-t (orttirma) + -ib', '-in (oʻzlik) + -adi'),
    ('«Uy qurildi.» gapida «qurildi» qaysi nisbatda?', 'Majhul nisbat', 'Aniq nisbat', 'Oʻzlik nisbati', 'Birgalik nisbati'),
    ('«U shoshib kiyindi.» gapida «kiyindi» qaysi nisbatda?', 'Oʻzlik nisbati', 'Majhul nisbat', 'Orttirma nisbat', 'Birgalik nisbati'),
    ('«Ustoz shogirdni oʻqitdi.» gapida «oʻqitdi» qaysi nisbatda?', 'Orttirma nisbat', 'Majhul nisbat', 'Oʻzlik nisbati', 'Birgalik nisbati'),
    ('«Bolalar gaplashdi.» gapida «gaplashdi» qaysi nisbatda?', 'Birgalik nisbati', 'Orttirma nisbat', 'Majhul nisbat', 'Oʻzlik nisbati'),
    ('«Keldi» feʼlidagi «-di» qoʻshimchasi qaysi zamonni bildiradi?', 'Aniq oʻtgan zamon', 'Hozirgi zamon', 'Kelasi zamon', 'Shart maylini'),
    ('«Oʻqimoqda» feʼli qaysi zamonda?', 'Hozirgi zamon (davomiy)', 'Oʻtgan zamon', 'Kelasi zamon', 'Buyruq mayli'),
    ('«Oʻqing» shakli qaysi maylga kiradi?', 'Buyruq-istak mayli', 'Shart mayli', 'Aniqlik mayli', 'Sifatdosh'),
    ('«Agar yomgʻir yogʻsa» birikmasida «yogʻsa» qaysi maylda?', 'Shart mayli', 'Buyruq mayli', 'Aniqlik mayli', 'Istak mayli'),
    ('«Oʻqima!» shakli qaysi shaklga kiradi?', 'Buyruq maylining inkor shakli', 'Shart maylining inkor shakli', 'Sifatdosh', 'Harakat nomi'),
    ('«Ishlovchi» soʻzidagi «-uvchi» qaysi feʼl shaklini yasaydi?', 'Sifatdosh', 'Ravishdosh', 'Harakat nomi', 'Shart mayli'),
    ('«Oʻqiguncha» shakli qaysi feʼl shakliga kiradi?', 'Ravishdosh', 'Sifatdosh', 'Harakat nomi', 'Buyruq mayli'),
    ('«Oʻqimoq» shakli qaysi feʼl shakliga kiradi?', 'Harakat nomi', 'Sifatdosh', 'Ravishdosh', 'Shart mayli'),
    ('Qaysi feʼl oʻtimli feʼl hisoblanadi?', 'yozmoq', 'yugurmoq', 'uxlamoq', 'kulmoq'),
    ('Qaysi feʼl oʻtimsiz feʼl hisoblanadi?', 'uxlamoq', 'yozmoq', 'oʻqimoq', 'koʻrmoq'),
    ('«Ishlay boshladi» birikmasida yordamchi feʼl qaysi?', 'boshladi', 'ishlay', 'Ikkalasi ham', 'Hech qaysi'),
    ('«Alining kitobi» birikmasida «Alining» qaysi aniqlovchi?', 'Qaratqich aniqlovchi', 'Sifatlovchi aniqlovchi', 'Izohlovchi', 'Toʻldiruvchi'),
    ('«Ikki bola keldi.» gapida «ikki» qaysi gap boʻlagi?', 'Aniqlovchi', 'Hol', 'Toʻldiruvchi', 'Ega'),
    ('«U shoshib keldi.» gapida «shoshib» qaysi hol?', 'Holat holi', 'Payt holi', 'Oʻrin holi', 'Sabab holi'),
    ('«U ertalab turdi.» gapida «ertalab» qaysi hol?', 'Payt holi', 'Holat holi', 'Oʻrin holi', 'Maqsad holi'),
    ('«U juda yaxshi koʻrdi.» gapida «juda» qaysi hol?', 'Miqdor-daraja holi', 'Payt holi', 'Oʻrin holi', 'Holat holi'),
    ('«U doʻsti bilan bordi.» gapida «doʻsti bilan» qaysi gap boʻlagi?', 'Toʻldiruvchi', 'Aniqlovchi', 'Ega', 'Kesim'),
    ('«Beshtasi keldi.» gapida ega qaysi soʻz turkumi bilan ifodalangan?', 'Son', 'Ot', 'Olmosh', 'Sifat'),
    ('«Bola ziyrak.» gapida kesim qaysi soʻz turkumi bilan ifodalangan?', 'Sifat', 'Ot', 'Feʼl', 'Son'),
    ('«Ular beshta.» gapida kesim qaysi soʻz turkumi bilan ifodalangan?', 'Son', 'Ot', 'Feʼl', 'Sifat'),
    ('Faqat bosh boʻlaklardan iborat gap qanday ataladi?', 'Yigʻiq gap', 'Yoyiq gap', 'Toʻliqsiz gap', 'Qoʻshma gap'),
    ('Ikkinchi darajali boʻlaklari ham bor gap qanday ataladi?', 'Yoyiq gap', 'Yigʻiq gap', 'Nomli gap', 'Qoʻshma gap'),
    ('«Men kitob oʻqidim, u esa — gazeta.» gapida qaysi boʻlak tushib qolgan?', 'Kesim (oʻqidi)', 'Ega', 'Hol', 'Aniqlovchi'),
    ('«Eshikni taqillatishdi.» gapi qaysi turga kiradi?', 'Noaniq shaxsli gap', 'Aniq shaxsli gap', 'Umumiy shaxsli gap', 'Nomli gap'),
    ('«Maktabga boryapman.» gapi qaysi turga kiradi?', 'Aniq shaxsli gap', 'Noaniq shaxsli gap', 'Shaxssiz gap', 'Nomli gap'),
    ('«Tun. Sukunat. Oy nuri.» gaplari qaysi turga kiradi?', 'Nomli gap', 'Aniq shaxsli gap', 'Umumiy shaxsli gap', 'Toʻliqsiz gap'),
    ('«Kitob — bilim chashmasi.» gapida tire nima uchun qoʻyilgan?', 'Ega va kesim ot bilan ifodalangan', 'Uyushiq boʻlaklar bor', 'Koʻchirma gap', 'Qoʻshma gap'),
    ('Gapning soʻz tartibi: kesim odatda qayerda keladi?', 'Ega va boshqa boʻlaklardan keyin, gap oxirida', 'Gap boshida', 'Ega oldida', 'Hol oldida'),
    ('«Maktabdan qaytdim» gapida «maktabdan» qaysi hol?', 'Oʻrin holi', 'Payt holi', 'Maqsad holi', 'Sabab holi'),
    ('«Kasalligi tufayli kela olmadi.» gapida «kasalligi tufayli» qaysi hol?', 'Sabab holi', 'Maqsad holi', 'Payt holi', 'Oʻrin holi'),
    ('«Dars tayyorlash uchun kutubxonaga bordi.» gapida «dars tayyorlash uchun» qaysi hol?', 'Maqsad holi', 'Sabab holi', 'Payt holi', 'Holat holi'),
    ('«Gapchan» soʻzida nechta qoʻshimcha bor?', '1 ta (-chan)', '2 ta', '3 ta', 'Yoʻq'),
    ('«Daraxtlarimizning» soʻzida nechta qoʻshimcha bor?', '3 ta', '2 ta', '4 ta', '1 ta'),
    ('«Kitoblarimiz» soʻzidagi egalik qoʻshimchasi qaysi?', '-imiz', '-lar', '-ing', '-ni'),
    ('«Ota-onamiz» soʻzi qanday soʻz?', 'Juft soʻzga egalik qoʻshilgan shakl', 'Takroriy soʻz', 'Qisqartma soʻz', 'Sodda soʻz'),
    ('«Yuzta» soʻzida «-ta» qanday vazifa bajaradi?', 'Dona maʼnosini bildiradi', 'Tartib maʼnosini bildiradi', 'Chama bildiradi', 'Koʻplik yasaydi'),
    ('«Oʻnlab» soʻzi sonning qaysi turi?', 'Chama son', 'Sanoq son', 'Tartib son', 'Dona son'),
    ('«Qizil olma» birikmasida bogʻlanish usuli qaysi?', 'Bitishuv', 'Boshqaruv', 'Moslashuv', 'Qoʻshma'),
    ('«Kitobni oʻqidi» birikmasida «kitobni» qaysi gap boʻlagi?', 'Vositasiz toʻldiruvchi', 'Vositali toʻldiruvchi', 'Hol', 'Aniqlovchi'),
    ('«Maktabga bordi» birikmasida «maktabga» soʻzi nimaga bogʻlangan?', 'Feʼlga (boshqaruv)', 'Otga (moslashuv)', 'Sifatga (bitishuv)', 'Hech narsaga'),
    ('Quyidagi qoʻshimchalardan qaysi biri kelishik qoʻshimchasi emas?', '-lar', '-ning', '-ni', '-dan'),
    ('Quyidagi qoʻshimchalardan qaysi biri egalik qoʻshimchasi emas?', '-ni', '-im', '-ing', '-imiz'),
    ('Quyidagi qoʻshimchalardan qaysi biri ot yasovchi emas?', '-la', '-chi', '-lik', '-dosh'),
    ('Quyidagi qoʻshimchalardan qaysi biri sifat yasovchi emas?', '-lar', '-li', '-siz', '-chan'),
    ('«Katta» soʻzi qaysi gapda ot vazifasida kelgan?', 'Kattalar keldi.', 'Katta uy qurildi.', 'Katta bola keldi.', 'U kattaroq edi.'),
    ('«Yaxshi» soʻzi qaysi gapda ravish vazifasida kelgan?', 'U yaxshi oʻqiydi.', 'U yaxshi bola.', 'Yaxshilar koʻp.', 'Yaxshi kun.'),
    ('«Oq» soʻzi qaysi birikmada ot vazifasida?', 'oq va qora', 'oq uy', 'oq qogʻoz', 'oq qor'),
    ('«Qora» soʻzi qaysi gapda sifat vazifasida kelgan?', 'Qora mushuk keldi.', 'Qoralar koʻpaydi.', 'Qora bilan oq', 'Qoraning rangi'),
    ('Tarkibida «-gan» qoʻshimchasi bor soʻz qaysi?', 'yozgan', 'yozuv', 'yozish', 'yozing'),
    ('Tarkibida «-ish» qoʻshimchasi harakat nomi yasagan soʻz qaysi?', 'yozish', 'yozgan', 'yozdi', 'yozib'),
    ('«Yozib» shakli qaysi feʼl shakliga kiradi?', 'Ravishdosh', 'Sifatdosh', 'Harakat nomi', 'Buyruq mayli'),
    ('«Yozgan xat» birikmasida «yozgan» qaysi gap boʻlagi?', 'Aniqlovchi', 'Hol', 'Kesim', 'Ega'),
    ('«Kelgach, dam oldi.» gapida «kelgach» qaysi shakl va gap boʻlagi?', 'Ravishdosh, hol', 'Sifatdosh, aniqlovchi', 'Harakat nomi, ega', 'Shart mayli, kesim'),
    ('«Kitob oʻqish foydali.» gapida ega qaysi?', 'Kitob oʻqish', 'foydali', 'Kitob', 'oʻqish'),
],
"d4": [
    ('Mustaqil soʻz turkumlari qaysi qatorda toʻgʻri sanalgan?', 'ot, sifat, son, olmosh, feʼl, ravish', 'ot, sifat, son, yuklama, feʼl, ravish', 'ot, bogʻlovchi, son, olmosh, feʼl, ravish', 'ot, sifat, koʻmakchi, olmosh, feʼl, ravish'),
    ('Yordamchi soʻz turkumlari qaysi qatorda toʻgʻri sanalgan?', 'koʻmakchi, bogʻlovchi, yuklama', 'ravish, bogʻlovchi, yuklama', 'olmosh, koʻmakchi, yuklama', 'son, bogʻlovchi, undov'),
    ('«Uchun» soʻzi qaysi turkumga kiradi?', 'Koʻmakchi', 'Bogʻlovchi', 'Yuklama', 'Ravish'),
    ('«Va, hamda» soʻzlari qaysi turkumga kiradi?', 'Bogʻlovchi', 'Koʻmakchi', 'Yuklama', 'Olmosh'),
    ('«-mi» qoʻshimchasi (Keldimi?) qaysi turkumga mansub?', 'Yuklama', 'Koʻmakchi', 'Bogʻlovchi', 'Undov'),
    ('«Chunki» soʻzi qaysi bogʻlovchiga kiradi?', 'Ergashtiruvchi bogʻlovchi', 'Teng bogʻlovchi', 'Ayiruv bogʻlovchisi', 'Biriktiruv bogʻlovchisi'),
    ('«Ammo, lekin, biroq» soʻzlari qaysi bogʻlovchi turiga kiradi?', 'Qarshilov bogʻlovchisi', 'Biriktiruv bogʻlovchisi', 'Ayiruv bogʻlovchisi', 'Ergashtiruvchi bogʻlovchi'),
    ('«Yoki, goh» soʻzlari qaysi bogʻlovchi turiga kiradi?', 'Ayiruv bogʻlovchisi', 'Biriktiruv bogʻlovchisi', 'Qarshilov bogʻlovchisi', 'Ergashtiruvchi bogʻlovchi'),
    ('«Uy tomon yurdi.» gapida «tomon» qaysi turkumga kiradi?', 'Koʻmakchi', 'Ravish', 'Bogʻlovchi', 'Ot'),
    ('«Ehtimol, albatta, shubhasiz» soʻzlari qaysi turkumga kiradi?', 'Modal soʻz', 'Ravish', 'Undov', 'Yuklama'),
    ('«Oh! Bahor keldi!» gapida «oh» qaysi turkumga kiradi?', 'Undov', 'Modal soʻz', 'Yuklama', 'Taqlid'),
    ('«Shaldir-shuldur, taraq-turuq» soʻzlari qaysi turkumga kiradi?', 'Taqlid soʻz', 'Undov', 'Ravish', 'Modal soʻz'),
    ('«Oqish» soʻzi sifatning qaysi darajasida?', 'Kamaytirma daraja', 'Qiyosiy daraja', 'Orttirma daraja', 'Oddiy daraja'),
    ('«Oqroq» soʻzi sifatning qaysi darajasida?', 'Qiyosiy daraja', 'Kamaytirma daraja', 'Orttirma daraja', 'Oddiy daraja'),
    ('«Eng goʻzal» birikmasi sifatning qaysi darajasida?', 'Orttirma daraja', 'Qiyosiy daraja', 'Kamaytirma daraja', 'Oddiy daraja'),
    ('«Qip-qizil» soʻzi sifatning qaysi darajasida?', 'Orttirma daraja', 'Kamaytirma daraja', 'Qiyosiy daraja', 'Oddiy daraja'),
    ('«Beshinchi» soʻzi sonning qaysi turiga kiradi?', 'Tartib son', 'Sanoq son', 'Chama son', 'Kasr son'),
    ('«Besh» soʻzi sonning qaysi turiga kiradi?', 'Sanoq son', 'Tartib son', 'Chama son', 'Jamlovchi son'),
    ('«Oʻnlab, yigirmaga yaqin» soʻzlari sonning qaysi turiga kiradi?', 'Chama son', 'Sanoq son', 'Tartib son', 'Taqsim son'),
    ('«Beshta-beshta» soʻzi sonning qaysi turiga kiradi?', 'Taqsim son', 'Chama son', 'Tartib son', 'Sanoq son'),
    ('«Hech kim» olmoshi qaysi turga kiradi?', 'Boʻlishsizlik olmoshi', 'Gumon olmoshi', 'Soʻroq olmoshi', 'Belgilash olmoshi'),
    ('«Kimdir» olmoshi qaysi turga kiradi?', 'Gumon olmoshi', 'Boʻlishsizlik olmoshi', 'Soʻroq olmoshi', 'Koʻrsatish olmoshi'),
    ('«Bu, shu, oʻsha» olmoshlari qaysi turga kiradi?', 'Koʻrsatish olmoshi', 'Kishilik olmoshi', 'Soʻroq olmoshi', 'Oʻzlik olmoshi'),
    ('«Kim, nima, qachon» olmoshlari qaysi turga kiradi?', 'Soʻroq olmoshi', 'Kishilik olmoshi', 'Gumon olmoshi', 'Belgilash olmoshi'),
    ('«Hamma, har kim» olmoshlari qaysi turga kiradi?', 'Belgilash-jamlash olmoshi', 'Boʻlishsizlik olmoshi', 'Gumon olmoshi', 'Koʻrsatish olmoshi'),
    ('«Tez yugurdi» birikmasidagi «tez» qaysi ravish turiga kiradi?', 'Holat ravishi', 'Payt ravishi', 'Oʻrin ravishi', 'Miqdor-daraja ravishi'),
    ('«Ertaga keladi» birikmasidagi «ertaga» qaysi ravish turiga kiradi?', 'Payt ravishi', 'Holat ravishi', 'Oʻrin ravishi', 'Sabab ravishi'),
    ('«Yuqorida turibdi» birikmasidagi «yuqorida» qaysi ravish turiga kiradi?', 'Oʻrin ravishi', 'Payt ravishi', 'Holat ravishi', 'Maqsad ravishi'),
    ('«Juda yaxshi» birikmasidagi «juda» qaysi ravish turiga kiradi?', 'Miqdor-daraja ravishi', 'Holat ravishi', 'Payt ravishi', 'Oʻrin ravishi'),
    ('«Men kitob oʻqidim, u esa rasm chizdi.» gap qaysi turga kiradi?', 'Bogʻlangan qoʻshma gap', 'Ergashgan qoʻshma gap', 'Sodda yigʻiq gap', 'Bogʻlovchisiz qoʻshma gap'),
    ('«Agar yomgʻir yogʻsa, biz chiqmaymiz.» gap qaysi turga kiradi?', 'Ergashgan qoʻshma gap', 'Bogʻlangan qoʻshma gap', 'Bogʻlovchisiz qoʻshma gap', 'Sodda gap'),
    ('«Kun isidi, qor erib ketdi.» gap qaysi turga kiradi?', 'Bogʻlovchisiz qoʻshma gap', 'Ergashgan qoʻshma gap', 'Bogʻlangan qoʻshma gap', 'Sodda yigʻiq gap'),
    ('«Agar mehnat qilsang, natija boʻladi.» gapda ergash gap qaysi turga kiradi?', 'Shart ergash gap', 'Payt ergash gap', 'Sabab ergash gap', 'Maqsad ergash gap'),
    ('«Garchi charchagan boʻlsa-da, ishlayverdi.» gapda ergash gap qaysi turga kiradi?', 'Toʻsiqsiz ergash gap', 'Shart ergash gap', 'Sabab ergash gap', 'Payt ergash gap'),
    ('«U kelmadi, chunki kasal edi.» gapda ergash gap qaysi turga kiradi?', 'Sabab ergash gap', 'Shart ergash gap', 'Maqsad ergash gap', 'Toʻsiqsiz ergash gap'),
    ('«Oʻqish uchun shaharga bordi.» gapida «oʻqish uchun» qaysi hol?', 'Maqsad holi', 'Sabab holi', 'Payt holi', 'Oʻrin holi'),
    ('Gap maqsadiga koʻra qaysi turlarga boʻlinadi?', 'Darak, soʻroq, buyruq gap', 'Sodda, qoʻshma gap', 'Yigʻiq, yoyiq gap', 'Toʻliq, toʻliqsiz gap'),
    ('Gap tuzilishiga koʻra qaysi turlarga boʻlinadi?', 'Sodda va qoʻshma gap', 'Darak va soʻroq gap', 'Buyruq va undov gap', 'Ega va kesimli gap'),
    ('Faqat bitta ega-kesim juftligidan tuzilgan gap qanday ataladi?', 'Sodda gap', 'Qoʻshma gap', 'Koʻchirma gap', 'Ergash gap'),
    ('Ikki va undan ortiq ega-kesim juftligidan tuzilgan gap qanday ataladi?', 'Qoʻshma gap', 'Sodda gap', 'Yigʻiq gap', 'Toʻliqsiz gap'),
    ('Birovning gapi aynan keltirilgan gap qanday ataladi?', 'Koʻchirma gap', 'Oʻzlashtirma gap', 'Ergash gap', 'Yigʻiq gap'),
    ('Koʻchirma gap qaysi tinish belgilari bilan ajratiladi?', 'Qoʻshtirnoq va tire', 'Qavs va vergul', 'Faqat nuqta', 'Ikki nuqta va nuqtali vergul'),
    ('«Ustoz, savolim bor.» gapida «ustoz» qanday ajratiladi?', 'Vergul bilan (murojaat)', 'Tire bilan', 'Qavs bilan', 'Ikki nuqta bilan'),
    ('«Albatta, men boraman.» gapida «albatta» qanday ajratiladi?', 'Vergul bilan (kirish soʻz)', 'Tire bilan', 'Qavs bilan', 'Ikki nuqta bilan'),
    ('Umumlashtiruvchi soʻzdan keyin sanalayotgan boʻlaklar oldidan qaysi tinish belgisi qoʻyiladi?', 'Ikki nuqta', 'Vergul', 'Nuqta', 'Qoʻshtirnoq'),
    ('Qaysi gapda tinish belgilari toʻgʻri qoʻyilgan?', 'Hamma kelgan edi: ota-onalar, oʻqituvchilar, oʻquvchilar.', 'Hamma kelgan edi, ota-onalar: oʻqituvchilar, oʻquvchilar.', 'Hamma kelgan edi; ota-onalar. oʻqituvchilar, oʻquvchilar.', 'Hamma kelgan edi ota-onalar, oʻqituvchilar: oʻquvchilar.'),
    ('Ariza, buyruq, bayonnoma qaysi uslubga xos?', 'Rasmiy (idoraviy) uslub', 'Badiiy uslub', 'Soʻzlashuv uslubi', 'Publitsistik uslub'),
    ('Ilmiy maqola, darslik, risola qaysi uslubga xos?', 'Ilmiy uslub', 'Badiiy uslub', 'Soʻzlashuv uslubi', 'Rasmiy uslub'),
    ('Gazeta va jurnal maqolalari, ommaviy chiqishlar qaysi uslubga xos?', 'Publitsistik uslub', 'Ilmiy uslub', 'Rasmiy uslub', 'Soʻzlashuv uslubi'),
    ('Tasviriy vositalar (oʻxshatish, mubolagʻa) koʻp ishlatiladigan uslub qaysi?', 'Badiiy uslub', 'Rasmiy uslub', 'Ilmiy uslub', 'Idoraviy uslub'),
    ('Kundalik erkin muloqotda ishlatiladigan uslub qaysi?', 'Soʻzlashuv uslubi', 'Ilmiy uslub', 'Rasmiy uslub', 'Badiiy uslub'),
    ('«Amir, xon, mingboshi» kabi soʻzlar qaysi guruhga kiradi?', 'Istorizm', 'Neologizm', 'Dialektizm', 'Varvarizm'),
    ('Hozirgi tilda boshqa soʻz bilan almashgan eskirgan soʻz qanday ataladi?', 'Arxaizm', 'Istorizm', 'Neologizm', 'Jargon'),
    ('Fan va texnika sohasidagi aniq tushunchani bildiruvchi soʻz qanday ataladi?', 'Termin', 'Jargon', 'Dialektizm', 'Arxaizm'),
    ('«Shoʻx» soʻzining sinonimi qaysi?', 'oʻynoqi', 'mahzun', 'jiddiy', 'vazmin'),
    ('«Qoʻli ochiq» iborasi qanday maʼnoni bildiradi?', 'Saxiy', 'Ishyoqmas', 'Oʻgʻri', 'Bekorchi'),
    ('«Koʻzi toʻrt boʻlmoq» iborasi qanday maʼnoni bildiradi?', 'Intizor boʻlib kutmoq', 'Yaxshi koʻrmoq', 'Ogʻir uxlamoq', 'Koʻp oʻqimoq'),
    ('«Boshi osmonga yetdi» iborasi qanday maʼnoni bildiradi?', 'Juda xursand boʻldi', 'Juda charchadi', 'Juda xafa boʻldi', 'Juda qoʻrqdi'),
    ('«Ichi qora» iborasi qanday maʼnoni bildiradi?', 'Yomon niyatli, hasadgoʻy', 'Kasal', 'Och', 'Mehribon'),
    ('«Qoʻl qovushtirib oʻtirmoq» iborasi qanday maʼnoni bildiradi?', 'Hech narsa qilmay, ishsiz oʻtirmoq', 'Duo qilmoq', 'Hurmat bildirmoq', 'Dam olmoq'),
    ('Maʼnosi tarkibidagi soʻzlar maʼnosidan kelib chiqmaydigan turgʻun birikma nima deb ataladi?', 'Frazeologizm (ibora)', 'Oddiy birikma', 'Qoʻshma soʻz', 'Gap'),
    ('Juft soʻzlar qanday yoziladi?', 'Chiziqcha bilan: ota-ona', 'Qoʻshib: otaona', 'Ajratib: ota ona', 'Qavs ichida'),
    ('Takroriy soʻzlar qanday yoziladi?', 'Chiziqcha bilan: qator-qator', 'Qoʻshib: qatorqator', 'Ajratib: qator qator', 'Tire bilan: qator — qator'),
    ('«-mi» yuklamasi qanday yoziladi?', 'Oldingi soʻzga qoʻshib: keldimi', 'Chiziqcha bilan: keldi-mi', 'Ajratib: keldi mi', 'Tire bilan: keldi — mi'),
    ('Davlat nomi qaysi yozuvda toʻgʻri bosh harf bilan berilgan?', 'Oʻzbekiston Respublikasi', 'oʻzbekiston respublikasi', 'Oʻzbekiston respublikasi', 'oʻzbekiston Respublikasi'),
    ('Viloyat nomi qaysi yozuvda toʻgʻri bosh harf bilan berilgan?', 'Sirdaryo viloyati', 'Sirdaryo Viloyati', 'sirdaryo viloyati', 'SIRDARYO viloyati'),
    ('«Qop-qora» soʻzi qanday yoziladi?', 'Chiziqcha bilan', 'Qoʻshib', 'Ajratib', 'Qavs ichida'),
    ('«Nahotki u kelmagan boʻlsa?» gapida «nahotki» qaysi turkumga kiradi?', 'Yuklama', 'Bogʻlovchi', 'Koʻmakchi', 'Ravish'),
    ('«Agar» soʻzi qaysi turkumga kiradi?', 'Ergashtiruvchi bogʻlovchi', 'Qarshilov bogʻlovchisi', 'Yuklama', 'Koʻmakchi'),
    ('«Alisher Navoiy, buyuk shoir, ijod qildi.» gapida «buyuk shoir» qanday ajratilgan?', 'Vergul bilan (izohlovchi)', 'Qavs bilan', 'Ikki nuqta bilan', 'Ajratilmagan'),
    ('Undov gap oxirida qaysi tinish belgisi qoʻyiladi?', 'Undov belgisi', 'Nuqta', 'Vergul', 'Ikki nuqta'),
    ('Ergashgan qoʻshma gapning ergash gapga tayanadigan asosiy qismi nima deb ataladi?', 'Bosh gap', 'Ergash gap', 'Koʻchirma gap', 'Yigʻiq gap'),
    ('Shakli oʻxshash, ammo maʼnosi har xil soʻzlar qanday ataladi?', 'Paronim', 'Omonim', 'Sinonim', 'Antonim'),
    ('Bir necha maʼnoga ega boʻlgan soʻz qanday ataladi?', 'Koʻp maʼnoli soʻz', 'Omonim', 'Termin', 'Arxaizm'),
    ('Soʻzning oʻxshashlik asosida boshqa narsaga koʻchishi qanday ataladi?', 'Koʻchma maʼno', 'Asl maʼno', 'Termin maʼnosi', 'Lugʻaviy maʼno'),
    ('Narsa-hodisani ataylab oshirib tasvirlash qanday ataladi?', 'Mubolagʻa', 'Oʻxshatish', 'Jonlantirish', 'Sifatlash'),
    ('«Daraxtlar shivirlashdi.» jumlada qanday tasviriy vosita bor?', 'Jonlantirish', 'Mubolagʻa', 'Antiteza', 'Inkor'),
    ('«Yuzi oydek» birikmasida qanday tasviriy vosita bor?', 'Oʻxshatish', 'Jonlantirish', 'Mubolagʻa', 'Takror'),
    ('«Oʻzim ishladim.» gapida «oʻzim» qaysi olmosh?', 'Oʻzlik olmoshi', 'Kishilik olmoshi', 'Koʻrsatish olmoshi', 'Soʻroq olmoshi'),
    ('Kishilik olmoshlari nechta (men, sen, u, biz, siz, ular)?', '6 ta', '4 ta', '5 ta', '8 ta'),
    ('«Faqat» soʻzi qaysi turkumga kiradi?', 'Yuklama (cheklov-ajratuv)', 'Bogʻlovchi', 'Koʻmakchi', 'Ravish'),
    ('«Hatto» soʻzi qaysi turkumga kiradi?', 'Yuklama (kuchaytiruv)', 'Bogʻlovchi', 'Koʻmakchi', 'Undov'),
    ('Quyidagilardan qaysi biri ergashtiruvchi bogʻlovchi emas?', 'va', 'agar', 'chunki', 'garchi'),
    ('Quyidagilardan qaysi biri koʻmakchi emas?', 'garchi', 'bilan', 'uchun', 'kabi'),
    ('Bogʻlangan qoʻshma gap qismlari qaysi vosita bilan bogʻlanadi?', 'Teng bogʻlovchilar (va, ammo, lekin...)', 'Ergashtiruvchi bogʻlovchilar', 'Faqat qoʻshtirnoq', 'Faqat soʻroq olmoshi'),
    ('«Kim ishlasa, shu yeydi.» gapda ergash gap qaysi turga kiradi?', 'Ega ergash gap', 'Kesim ergash gap', 'Payt ergash gap', 'Sabab ergash gap'),
    ('«Quyosh chiqqanda, biz yoʻlga chiqdik.» gapda ergash gap qaysi turga kiradi?', 'Payt ergash gap', 'Shart ergash gap', 'Oʻrin ergash gap', 'Sabab ergash gap'),
    ('«Shu qadar charchadiki, oyoqda turolmadi.» gapda ergash gap qaysi turga kiradi?', 'Natija ergash gap', 'Maqsad ergash gap', 'Shart ergash gap', 'Payt ergash gap'),
    ('«Men bilamanki, u keladi.» gapda ergash gap qaysi turga kiradi?', 'Toʻldiruvchi ergash gap', 'Payt ergash gap', 'Shart ergash gap', 'Oʻrin ergash gap'),
    ('Nuqtali vergul koʻpincha qachon qoʻyiladi?', 'Ichida vergul bor qoʻshma gap qismlari orasida', 'Har bir gap oxirida', 'Koʻchirma gap boshida', 'Murojaatdan keyin'),
    ('Gapga qoʻshimcha izoh beruvchi qism qaysi belgilar ichida yoziladi?', 'Qavs', 'Qoʻshtirnoq', 'Vergul', 'Faqat tire'),
    ('Fikr tugallanmay qolganini koʻrsatish uchun qaysi belgi qoʻyiladi?', 'Uch nuqta', 'Nuqta', 'Qoʻshtirnoq', 'Qavs'),
    ('«Kitob, maktab, qalam» soʻzlari qaysi tildan oʻzlashgan?', 'Arab tilidan', 'Rus tilidan', 'Xitoy tilidan', 'Ingliz tilidan'),
    ('«Dehqon, daryo, shahar» soʻzlari qaysi tildan oʻzlashgan?', 'Fors-tojik tilidan', 'Arab tilidan', 'Rus tilidan', 'Nemis tilidan'),
    ('Qaysi soʻz oʻzbek tilining asl (turkiy) soʻzi?', 'koʻz', 'kitob', 'daryo', 'stansiya'),
    ('«Yosh» (qari emas) va «yosh» (koʻz yoshi) soʻzlari oʻzaro qanday munosabatda?', 'Omonim', 'Sinonim', 'Antonim', 'Paronim'),
    ('«Kirmoq — chiqmoq» juftligi qanday munosabatda?', 'Antonim', 'Sinonim', 'Omonim', 'Paronim'),
    ('Qaysi juftlik antonim emas?', 'chiroyli — goʻzal', 'baland — past', 'keng — tor', 'yorugʻ — qorongʻi'),
    ('Qaysi soʻz qoʻshib yoziladi?', 'koʻzoynak', 'ota-ona', 'qator-qator', 'oq-qora'),
    ('Soʻzni boʻgʻin koʻchirishda qaysi qoida toʻgʻri?', 'Boʻgʻin chegarasidan koʻchiriladi', 'Bitta harf qatorda qoldiriladi', 'Bitta harf yangi qatorga koʻchiriladi', 'Istalgan joydan boʻlinadi'),
    ('«Jargon» nima?', 'Muayyan ijtimoiy guruhga xos soʻz', 'Fan atamasi', 'Eskirgan soʻz', 'Shevaga xos soʻz'),
    ('Qaysi gapda murojaat bor?', 'Doʻstlar, birga boramiz.', 'Doʻstlar birga bordi.', 'Doʻstlarimiz keldi.', 'Doʻstlik — baxt.'),
    ('Qaysi gapda kirish soʻz bor?', 'Afsuski, u kelmadi.', 'U kelmadi.', 'U tez kelmadi.', 'U kecha kelmadi.'),
    ('«Ammo» bogʻlovchisi qaysi tinish belgisi bilan ajratiladi (gap boshida emas)?', 'Oldidan vergul', 'Oldidan nuqta', 'Oldidan ikki nuqta', 'Hech narsa qoʻyilmaydi'),
    ('Qaysi gap soʻroq gap?', 'Siz qayerga ketyapsiz?', 'Siz bugun ketyapsiz.', 'Siz ketdingiz!', 'Siz keting.'),
    ('Qaysi gap buyruq gap?', 'Darsni oʻqi.', 'Darsni oʻqidi.', 'Darsni oʻqiydimi?', 'Darsni oʻqiyapti.'),
    ('«Hay, nima qilyapsan!» gapida «hay» qaysi turkumga kiradi?', 'Undov', 'Yuklama', 'Modal soʻz', 'Ravish'),
    ('«Balki» soʻzi ehtimollik maʼnosida kelsa, qaysi turkumga kiradi?', 'Modal soʻz', 'Undov', 'Taqlid soʻz', 'Koʻmakchi'),
    ('«Chiyq-chiyq, vizz» kabi soʻzlar nimaga taqlid?', 'Tovushga', 'Harakatga', 'Rangga', 'Hidga'),
    ('Sifatning orttirma darajasini hosil qilish usuliga qaysi biri kiradi?', '«juda, eng» soʻzlarini qoʻllash', '«-lar» qoʻshimchasi', '«-ni» qoʻshimchasi', '«-da» qoʻshimchasi'),
    ('Quyidagilardan qaysi biri sifat darajasi emas?', 'Qoʻshma daraja', 'Oddiy daraja', 'Qiyosiy daraja', 'Orttirma daraja'),
    ('Soʻz yasalishining qaysi usulida yangi soʻz qoʻshimcha yordamida hosil qilinadi?', 'Affiksatsiya', 'Kompozitsiya', 'Abbreviatsiya', 'Konversiya'),
    ('«Temiryoʻl» soʻzi qaysi usul bilan yasalgan?', 'Kompozitsiya (soʻz qoʻshish)', 'Affiksatsiya', 'Abbreviatsiya', 'Konversiya'),
    ('«OʻzMU» soʻzi qaysi usul bilan yasalgan?', 'Abbreviatsiya (qisqartirish)', 'Affiksatsiya', 'Kompozitsiya', 'Konversiya'),
    ('Soʻzning shaklini oʻzgartirmay, boshqa turkumga oʻtishi qanday ataladi?', 'Konversiya', 'Affiksatsiya', 'Kompozitsiya', 'Abbreviatsiya'),
    ('Qaysi qatordagi undoshlar jarangsiz?', 'p, t, k, s', 'b, d, g, z', 'b, t, g, s', 'd, p, z, k'),
    ('Qaysi qatordagi undoshlar jarangli?', 'b, d, g, z', 'p, t, k, s', 'p, d, k, z', 't, b, s, g'),
    ('Qaysi unlilar lablangan unlilar hisoblanadi?', 'u, oʻ, o', 'a, e, i', 'a, i, u', 'e, oʻ, i'),
    ('Qaysi unlilar lablanmagan unlilar hisoblanadi?', 'a, e, i', 'u, oʻ, o', 'a, u, oʻ', 'e, o, i'),
    ('«Kitob» soʻzining birinchi boʻgʻini qanday boʻgʻin?', 'Ochiq boʻgʻin (ki)', 'Yopiq boʻgʻin (kit)', 'Qoʻshma boʻgʻin', 'Boʻgʻin emas'),
    ('«Daryo» soʻzining birinchi boʻgʻini qanday boʻgʻin?', 'Yopiq boʻgʻin (dar)', 'Ochiq boʻgʻin (da)', 'Qoʻshma boʻgʻin', 'Boʻgʻin emas'),
    ('Oʻzbek tilida urgʻu odatda qaysi boʻgʻinga tushadi?', 'Oxirgi boʻgʻinga', 'Birinchi boʻgʻinga', 'Ikkinchi boʻgʻinga', 'Faqat toq boʻgʻinga'),
    ('Soʻzning oʻxshashlik asosida boshqa maʼnoga koʻchishi natijasida hosil boʻlgan maʼno qanday ataladi?', 'Koʻchma maʼno', 'Toʻgʻri maʼno', 'Termin maʼnosi', 'Asl maʼno'),
    ('«Yoz» (fasl) va «yoz» (buyruq) soʻzlari oʻzaro qanday munosabatda?', 'Omonim', 'Sinonim', 'Antonim', 'Paronim'),
    ('«Ertalab — kechqurun» juftligi qanday munosabatda?', 'Antonim', 'Sinonim', 'Omonim', 'Paronim'),
    ('«Yigirma besh» soʻzi tuzilishiga koʻra qanday son?', 'Qoʻshma son', 'Sodda son', 'Juft son', 'Takroriy son'),
    ('«Yetti-sakkiz» soʻzi tuzilishiga koʻra qanday son?', 'Juft son', 'Qoʻshma son', 'Sodda son', 'Takroriy son'),
    ('«Ikkita-ikkita» soʻzi qaysi son turiga kiradi?', 'Taqsim son (takroriy shaklda)', 'Tartib son', 'Kasr son', 'Chama son'),
    ('«Yarim» soʻzi qaysi son turiga kiradi?', 'Kasr son', 'Tartib son', 'Taqsim son', 'Jamlovchi son'),
    ('«Bu kitob» birikmasida «bu» qaysi soʻz turkumi?', 'Koʻrsatish olmoshi (aniqlovchi vazifasida)', 'Ot', 'Sifat', 'Ravish'),
    ('«Shirin, achchiq, nordon» sifatlari qaysi maʼnoviy guruhga kiradi?', 'Taʼm bildiruvchi sifatlar', 'Rang bildiruvchi sifatlar', 'Shakl bildiruvchi sifatlar', 'Hajm bildiruvchi sifatlar'),
    ('«Qizil, yashil, koʻk» sifatlari qaysi maʼnoviy guruhga kiradi?', 'Rang bildiruvchi sifatlar', 'Taʼm bildiruvchi sifatlar', 'Hajm bildiruvchi sifatlar', 'Hid bildiruvchi sifatlar'),
    ('«Xalq, poda, qoʻshin» otlari qaysi guruhga kiradi?', 'Jamlovchi otlar', 'Mavhum otlar', 'Atoqli otlar', 'Yakka otlar'),
    ('«Adolat, quvonch, sadoqat» otlari qaysi guruhga kiradi?', 'Mavhum otlar', 'Aniq otlar', 'Atoqli otlar', 'Jamlovchi otlar'),
    ('«Kerak, lozim, zarur» soʻzlari qaysi turkumga kiradi?', 'Modal soʻz', 'Undov', 'Koʻmakchi', 'Yuklama'),
    ('«Aftidan» soʻzi kirish soʻz sifatida qanday maʼno bildiradi?', 'Taxmin', 'Ishonch', 'Afsus', 'Tartib'),
    ('«Afsuski» soʻzi kirish soʻz sifatida qanday maʼno bildiradi?', 'His-tuygʻu (afsus)', 'Taxmin', 'Tartib', 'Ishonch'),
    ('«Birinchidan» soʻzi kirish soʻz sifatida qanday maʼno bildiradi?', 'Fikrlar tartibi', 'Afsus', 'Taxmin', 'Ishonch'),
    ('«Qayerda ish boʻlsa, oʻsha yerda odam boʻladi.» gapda ergash gap qaysi turga kiradi?', 'Oʻrin ergash gap', 'Payt ergash gap', 'Shart ergash gap', 'Sabab ergash gap'),
    ('«Yaxshi oʻqisin deb, uni ragʻbatlantirdik.» gapda ergash gap qaysi turga kiradi?', 'Maqsad ergash gap', 'Sabab ergash gap', 'Shart ergash gap', 'Natija ergash gap'),
    ('Shart ergash gapni bosh gapga bogʻlovchi vosita qaysi?', 'agar', 'chunki', 'toki', 'garchi'),
    ('Toʻsiqsiz ergash gapni bosh gapga bogʻlovchi vosita qaysi?', 'garchi', 'agar', 'chunki', 'toki'),
    ('«Men bilaman: u kelmaydi.» gapida ikki nuqta nima uchun qoʻyilgan?', 'Ikkinchi qism birinchisini izohlaydi', 'Koʻchirma gap bor', 'Uyushiq boʻlaklar bor', 'Murojaat bor'),
    ('«Ali: «Kelaman», — dedi.» koʻchirma gapini oʻzlashtirma gapga aylantiring.', 'Ali kelishini aytdi.', 'Ali: kelaman dedi.', 'Ali «kelaman» dedi.', 'Ali kelaman, dedi.'),
    ('Qaysi yozuv toʻgʻri?', 'hech kim', 'hechkim', 'hech-kim', 'hech.kim'),
    ('«Ham» yuklamasi qanday yoziladi?', 'Alohida: men ham keldim', 'Qoʻshib: menham keldim', 'Chiziqcha bilan: men-ham', 'Qavs ichida'),
    ('Obrazlilik, tasviriy vositalar boyligi qaysi uslubning belgisi?', 'Badiiy uslub', 'Rasmiy uslub', 'Ilmiy uslub', 'Soʻzlashuv uslubi'),
    ('Termin, aniqlik va mantiqiylik qaysi uslubning belgisi?', 'Ilmiy uslub', 'Badiiy uslub', 'Soʻzlashuv uslubi', 'Publitsistik uslub'),
    ('Shablonlilik, aniq qolip qaysi uslubning belgisi?', 'Rasmiy (idoraviy) uslub', 'Badiiy uslub', 'Ilmiy uslub', 'Soʻzlashuv uslubi'),
    ('Ommabop va taʼsirchan til, siyosiy-ijtimoiy mavzular qaysi uslubning belgisi?', 'Publitsistik uslub', 'Rasmiy uslub', 'Ilmiy uslub', 'Badiiy uslub'),
    ('Ergashgan qoʻshma gapning qismlari qanday ataladi?', 'Bosh gap va ergash gap', 'Ega va kesim', 'Aniqlovchi va hol', 'Toʻliq va toʻliqsiz gap'),
    ('Fan yoki kasb sohasida maxsus tushunchani bildiruvchi soʻz qanday ataladi?', 'Termin', 'Jargon', 'Sheva soʻzi', 'Arxaizm'),
    ('Qaysi soʻz istorizm hisoblanadi?', 'mingboshi', 'kompyuter', 'telefon', 'kitob'),
    ('Hozirgi paytda qoʻllanmaydigan, boshqa soʻz bilan almashgan eskirgan soʻz qaysi guruhga kiradi?', 'Arxaizm', 'Neologizm', 'Termin', 'Dialektizm'),
    ('Qaysi birikma erkin birikma, frazeologizm emas?', 'yangi kitob', 'qoʻli ochiq', 'koʻzi toʻrt boʻlmoq', 'ichi qora'),
    ('«Kecha kutubxonada yangi kitobni diqqat bilan oʻqidim.» gapida nechta hol bor?', '3 ta', '2 ta', '4 ta', '1 ta'),
    ('«Kecha kutubxonada yangi kitobni diqqat bilan oʻqidim.» gapida nechta ikkinchi darajali boʻlak bor?', '5 ta', '4 ta', '6 ta', '3 ta'),
    ('«Kecha kutubxonada yangi kitobni diqqat bilan oʻqidim.» gapida «kutubxonada» qaysi gap boʻlagi?', 'Oʻrin holi', 'Payt holi', 'Toʻldiruvchi', 'Aniqlovchi'),
    ('«Kecha kutubxonada yangi kitobni diqqat bilan oʻqidim.» gapida «diqqat bilan» qaysi gap boʻlagi?', 'Holat holi', 'Toʻldiruvchi', 'Payt holi', 'Aniqlovchi'),
    ('«Kecha kutubxonada yangi kitobni diqqat bilan oʻqidim.» gapida ega qanday ifodalangan?', 'Ifodalanmagan (kesimdagi shaxs qoʻshimchasidan maʼlum: men)', 'kitobni', 'kecha', 'oʻqidim'),
    ('«Kuchli shamol esib, daraxtlarni egdi.» gapida «esib» qaysi gap boʻlagi?', 'Hol', 'Aniqlovchi', 'Toʻldiruvchi', 'Ega'),
    ('«Oʻqigan odam donishmand boʻladi.» gapida «oʻqigan» qaysi gap boʻlagi?', 'Aniqlovchi', 'Hol', 'Kesim', 'Toʻldiruvchi'),
    ('«Dehqonlar ekin ekish uchun dalaga chiqdi.» gapida «ekin ekish uchun» qaysi hol?', 'Maqsad holi', 'Sabab holi', 'Payt holi', 'Holat holi'),
    ('«Yomgʻir yogʻayotgani sababli, yigʻilish kechikdi.» gapida «yomgʻir yogʻayotgani sababli» qaysi hol?', 'Sabab holi', 'Maqsad holi', 'Payt holi', 'Oʻrin holi'),
    ('«Aka-ukalar bir-biriga yordam berdi.» gapida «bir-biriga» qaysi gap boʻlagi?', 'Toʻldiruvchi', 'Hol', 'Aniqlovchi', 'Ega'),
    ('«U kasal edi.» gapida «edi» qanday vazifa bajargan?', 'Bogʻlama (kesimning tarkibiy qismi)', 'Ega', 'Hol', 'Toʻldiruvchi'),
    ('«Kitobni oʻqib chiqdi.» gapida kesim qaysi turga kiradi?', 'Murakkab feʼl kesim', 'Sodda feʼl kesim', 'Ot kesim', 'Sifat kesim'),
    ('«Oʻqish va yozish zarur.» gapida ega qanday ifodalangan?', 'Harakat nomlari bilan (uyushiq ega)', 'Otlar bilan', 'Olmoshlar bilan', 'Sifatdoshlar bilan'),
    ('«Bir-biriga» soʻzining toʻgʻri imlosi qaysi?', 'bir-biriga', 'birbiriga', 'bir biriga', 'bir_biriga'),
    ('Raqam bilan yozilgan sinf nomi qaysi yozuvda toʻgʻri?', '5-sinf', '5sinf', '5 - sinf', '5nchi sinf'),
    ('«Ketma-ket» soʻzining toʻgʻri imlosi qaysi?', 'ketma-ket', 'ketmaket', 'ketma ket', 'ketma_ket'),
    ('Uyushiq boʻlakli gapda tinish belgilari qaysi yozuvda toʻgʻri?', 'Olma, nok va uzum pishdi.', 'Olma, nok, va uzum pishdi.', 'Olma nok, va uzum pishdi.', 'Olma: nok va uzum, pishdi.'),
    ('Qoʻshma gapda tinish belgilari qaysi yozuvda toʻgʻri?', 'Bahor keldi, daraxtlar gullay boshladi.', 'Bahor keldi daraxtlar, gullay boshladi.', 'Bahor keldi: daraxtlar, gullay boshladi.', 'Bahor, keldi daraxtlar gullay boshladi.'),
],
}


def _add_gen5():
    for _lv, _qs in list(GEN5.items()) + list(GEN6.items()) + list(GEN7.items()):
        _pool = LEVELS[_lv]["questions"]
        _seen = {q["q"] for q in _pool}
        for (_t, _r, *_w) in _qs:
            if _t in _seen:
                continue
            _o = [_r] + list(_w)
            random.shuffle(_o)
            _pool.append({"q": _t, "o": _o, "a": _o.index(_r), "kind": 99, "pro": True})


_add_gen5()


# ------------------------------------------------------------------ Oʻrganish boʻlimi
# Telegram HTML: faqat <b>, <i> ishlatilgan; < & > belgilari yoʻq.
TUR = {}
TUR["ot"] = """🏷️ <b>OT</b>

<b>Nima?</b> Predmetni bildirib, <i>kim? nima? qayer?</i> soʻroqlariga javob boʻladigan soʻz turkumi. <i>Kim?</i> odamga, <i>nima?</i> qolgan hamma narsaga beriladi.

<b>📌 Maʼnoviy tuzilishi (guruhlari)</b>
• <b>Atoqli</b> (Anvar, Samarqand, Zarafshon) va <b>turdosh</b> (kitob, daryo, shahar)
• <b>Yakka</b> (daraxt, uy) va <b>jamlovchi</b> (xalq, qoʻshin, poda, olomon)
• <b>Aniq</b> (stol, qalam) va <b>mavhum</b> (adolat, quvonch, vatanparvarlik)
• <b>Sanaladigan</b> (kitob) va <b>sanalmaydigan</b> (suv, sut, havo)

<b>🧱 Shakl jihatdan tuzilishi</b>
• sodda: <i>gul, tosh</i> • yasama: <i>kitobxon, ishchi, gulzor, bilimdon</i>
• qoʻshma: <i>temiryoʻl, koʻzoynak, boshqaruv</i> • juft: <i>ota-ona, qoʻl-oyoq</i>
• takroriy: <i>qator-qator</i> • qisqartma: <i>BMT, OTM</i>

<b>⚙️ Grammatik shakllari</b>
• Son: <i>-lar</i> (kitoblar) • Egalik: <i>-im, -ing, -i, -imiz, -ingiz, -i</i>
• Kelishik (6 ta): bosh (—), qaratqich <i>-ning</i>, tushum <i>-ni</i>, joʻnalish <i>-ga</i>, oʻrin-payt <i>-da</i>, chiqish <i>-dan</i>
• Qoʻshimchalar tartibi: <b>koʻplik → egalik → kelishik</b>: <i>kitob-lar-im-dan</i>
• Joʻnalish: <i>kitobga, uyga</i>; <b>k</b> va <b>q</b> dan keyin <i>-ka, -qa</i> yoziladi: <i>tokka, ariqqa, qishloqqa</i>

<b>🧩 Gapdagi vazifasi</b>
Ega (<i>Kitob stolda.</i>), toʻldiruvchi (<i>kitobni oʻqidi</i>), aniqlovchi (<i>maktab hovlisi</i>), hol (<i>uyda oʻtirdi</i>), kesim (<i>U — oʻqituvchi.</i>).

<b>⚠️ Eslatma:</b> Son bilan kelganda ot koʻplikda boʻlmaydi: <i>uch kitob</i> (uchta kitoblar — xato)."""

TUR["sifat"] = """🎨 <b>SIFAT</b>

<b>Nima?</b> Predmet belgisini bildirib, <i>qanday? qanaqa? qaysi?</i> soʻroqlariga javob boʻladigan soʻz turkumi.

<b>📌 Maʼnoviy tuzilishi</b>
Belgisiga koʻra:
• rang-tus: <i>oq, qizil, moviy</i> • shakl: <i>yumaloq, tekis, egri</i>
• oʻlcham-hajm: <i>katta, uzun, keng</i> • maza-taʼm: <i>shirin, achchiq, nordon</i>
• hid: <i>xushboʻy, sassiq</i> • xususiyat: <i>mehribon, dono, tirishqoq</i>
• vaqt-oʻrin: <i>kechki, ertangi, tashqi</i>

<b>Asliy va nisbiy sifat:</b>
• <b>Asliy</b> — oʻzi belgi bildiradi, daraja shakllari boʻladi: <i>oq, katta, yaxshi</i>
• <b>Nisbiy</b> — otdan yasaladi, belgi boshqa narsaga nisbatan: <i>temirdek, suvli, kuzgi, ilmiy, vatanparvar</i>

<b>📈 Sifat darajalari</b>
• oddiy: <i>chiroyli</i> • qiyosiy: <i>chiroyliroq</i> (-roq)
• orttirma: <i>eng chiroyli, juda chiroyli, qip-qizil, yam-yashil, sap-sariq, oppoq</i>
• kamaytirma: <i>oqish, qoramtir, koʻkimtir</i>

<b>🧱 Tuzilishi:</b> sodda (<i>yaxshi</i>), yasama (<i>-li, -siz, -iy, -dor, -kor, -chan: bilimli, aqlsiz, ilmiy, ishchan</i>), qoʻshma (<i>ochiqkoʻngil</i>), juft (<i>yaxshi-yomon</i>), takroriy (<i>katta-katta</i>).

<b>🧩 Gapdagi vazifasi:</b> aniqlovchi (<i>baland bino</i>), kesim (<i>Havo sovuq.</i>), hol (<i>chiroyli yozdi</i>); otlashsa — ega yoki toʻldiruvchi (<i>Yaxshilar koʻp.</i>).

<b>⚠️ Eslatma:</b> Sifat aniqlovchi boʻlganda koʻplik qoʻshimchasini olmaydi: <i>katta uylar</i> (kattalar uylar — xato)."""

TUR["son"] = """🔢 <b>SON</b>

<b>Nima?</b> Predmetning sanogʻi, miqdori va tartibini bildirib, <i>nechta? qancha? nechanchi?</i> soʻroqlariga javob beradi.

<b>📌 Maʼnoviy tuzilishi</b>
• <b>Sanoq</b>: bir, yigirma, yuz, ming • <b>Dona</b>: ikkita, beshta, oʻnta
• <b>Tartib</b> (-inchi, -nchi): birinchi, yigirmanchi • <b>Taqsim</b> (-tadan, -ar): beshtadan, ikkitadan, uchtadan
• <b>Chama</b>: oʻnlab, yigirmaga yaqin, ellikcha, oʻn besh chogʻli
• <b>Jamlovchi</b> (-ov, -ala, -ovlon): ikkov, uchala, toʻrtovlon
• <b>Kasr</b>: uchdan bir, ikki butun oʻndan besh

<b>🧱 Tuzilishi</b>
• sodda: <i>bir, oʻn, yuz</i> • qoʻshma: <i>yigirma besh, bir yuz</i>
• juft: <i>bir-ikki, uch-toʻrt</i> • takroriy: <i>bir-bir, ikkitadan-ikkitadan</i>

<b>✍️ Imlo</b>
• Raqam bilan yozilgan tartib son va yil chiziqcha bilan yoziladi: <i>5-sinf, 3-qavat, 1990-yil</i>
• Sonli ot koʻplikda boʻlmaydi: <i>beshta kitob</i>
• Sonlar aniqlovchi: <i>uch oʻquvchi</i>, oʻzi ham otlashadi: <i>Ikkisi keldi.</i>

<b>🧩 Gapdagi vazifasi:</b> aniqlovchi (<i>ikki kitob</i>), ega/toʻldiruvchi (otlashganda), kesim (<i>Ularning soni — beshta.</i>)."""

TUR["olmosh"] = """👤 <b>OLMOSH</b>

<b>Nima?</b> Ot, sifat, son oʻrnida qoʻllanib, ularni atamasdan, ularga <i>ishora qiladi</i>.

<b>📌 Maʼnoviy tuzilishi (7 tur)</b>
• <b>Kishilik</b>: men, sen, u, biz, siz, ular
• <b>Koʻrsatish</b>: bu, shu, u, oʻsha, mana bu, ana u, shunday, bunday
• <b>Soʻroq</b>: kim, nima, qanday, qaysi, qancha, nechta, qachon, qayerda
• <b>Belgilash-jamlash</b>: har, hamma, barcha, butun, har kim, hamma narsa
• <b>Oʻzlik</b>: oʻz, oʻzim, oʻzing, oʻzi
• <b>Gumon</b>: kimdir, nimadir, kimdur, biror, birov
• <b>Boʻlishsizlik (inkor)</b>: hech kim, hech nima, hech qachon, hech narsa, hech qayer

<b>⚙️ Grammatik xususiyatlari</b>
Kelishik oladi, lekin oʻziga xos shakllarda: <i>men → mening, meni, menga, mendan; sen → sening, seni; u → uning, uni, unga; bu → buning, buni, bunga</i>.

<b>🧩 Gapdagi vazifasi:</b> ega (<i>U keldi.</i>), toʻldiruvchi (<i>Meni chaqirdi.</i>), aniqlovchi (<i>mening kitobim</i>), hol (<i>shunday yozdi</i>).

<b>⚠️ Eslatma:</b> «sen» — yaqinlar, «siz» — hurmat bilan murojaat. Uslub: rasmiy nutqda «siz» ishlatiladi."""

TUR["feil"] = """🏃 <b>FEʼL</b>

<b>Nima?</b> Predmetning harakati yoki holatini bildirib, <i>nima qildi? nima qilyapti? nima qiladi?</i> soʻroqlariga javob beradi.

<b>📌 Maʼnoviy tuzilishi</b>
• <b>Harakat</b>: yozmoq, bormoq • <b>Holat</b>: yotmoq, uxlamoq, quvonmoq
• <b>Oʻtimli</b> (tushum kelishigi bilan: <i>kitobni oʻqidi</i>) va <b>oʻtimsiz</b> (<i>bordi, uxladi</i>)
• <b>Boʻlishli</b> va <b>boʻlishsiz</b> (-ma): <i>keldi — kelmadi</i>

<b>🔄 Nisbat (5 ta)</b>
aniq (<i>yozdi</i>), oʻzlik (<i>yuvindi</i>, -n, -in), majhul (<i>yozildi</i>, -l, -il), birgalik (<i>yozishdi</i>, -sh, -ish), orttirma (<i>yozdirdi</i>, -dir, -t, -tir)

<b>🎯 Mayl:</b> aniqlik (<i>keldi</i>), buyruq-istak (<i>kel, kelsin, kelaylik</i>), shart (<i>kelsa</i>)

<b>⏱ Zamon</b>
• oʻtgan: <i>-di, -gan, -ib: keldi</i> • hozirgi: <i>-yapti, -moqda, -yotir: kelyapti</i> • kelasi: <i>-adi, -ar, -moqchi, -ajak: keladi</i>

<b>👥 Shaxs-son:</b> men -man, sen -san, u (—), biz -miz, siz -siz, ular -lar

<b>🌿 Tuslanmaydigan shakllar</b>
• <b>Sifatdosh</b>: -gan, -uvchi, -ajak, -yotgan, -adigan (<i>oʻqigan bola</i>)
• <b>Ravishdosh</b>: -ib, -a/-y, -gach, -guncha, -gani, -may (<i>kulib gapirdi</i>)
• <b>Harakat nomi</b>: -ish, -uv, -moq (<i>oʻqish, yozuv</i>)

<b>🧱 Tuzilishi:</b> sodda (<i>yoz</i>), yasama (<i>ishla, oʻrgan</i>), qoʻshma (<i>xursand boʻl, sotib ol</i>), juft (<i>oldi-berdi qil</i>), takroriy.

<b>🧩 Gapdagi vazifasi:</b> asosan kesim."""

TUR["ravish"] = """⚡ <b>RAVISH</b>

<b>Nima?</b> Harakat yoki belgining belgisini bildiradi, <i>qanday? qachon? qayerda? qancha?</i> soʻroqlariga javob beradi.

<b>📌 Maʼnoviy tuzilishi</b>
• <b>Holat (tarz)</b>: tez, sekin, asta, birga, ochiq
• <b>Payt</b>: bugun, kecha, hozir, erta, ertalab, kech
• <b>Oʻrin</b>: yuqori, past, ichkari, tashqari, uzoq, yaqin
• <b>Miqdor-daraja</b>: juda, ancha, koʻp, kam, nihoyatda, biroz
• <b>Maqsad-sabab</b>: ataylab, noiloj, chorasiz

<b>🧱 Tuzilishi va yasalishi</b>
• sodda: <i>tez, kecha</i> • yasama: <i>-cha (oʻzbekcha), -ona (mardona), -lab (soatlab, kunlab), -dan (boshdan)</i>
• qoʻshma: <i>hech qachon, har doim</i> • juft: <i>asta-sekin, erta-kech</i>
• takroriy: <i>tez-tez, sekin-sekin</i>

<b>🧩 Gapdagi vazifasi:</b> hol (<i>Bugun keldi. Tez yozdi.</i>); kelishik va egalik qoʻshimchalarini olmaydi.

<b>⚠️ Eslatma:</b> Ravish feʼlga bogʻlanadi: <i>tez yuguradi</i>; sifat otga bogʻlanadi: <i>tez poyezd</i>."""

TUR["komakchi"] = """🔗 <b>KOʻMAKCHI</b>

<b>Nima?</b> Oʻzi mustaqil maʼno bildirmay, kelishikdagi soʻzlarga qoʻshilib, ular orasidagi munosabatni bildiradigan yordamchi soʻz.

<b>📌 Maʼnoviy tuzilishi (turlari)</b>
• <b>Sof koʻmakchilar</b>: bilan, uchun, kabi, singari, sari, sayin, qadar, boshqa
• <b>Otdan oʻtgan koʻmakchilar</b>: ustida, ostida, ichida, orqasida, haqida, toʻgʻrisida, orqali, oldida

<b>🔗 Qaysi kelishik bilan keladi?</b>
• bosh kelishik: <i>kitob bilan, ish uchun, gul kabi</i>
• qaratqich: <i>uyning oldida, daraxtning ostida</i>
• joʻnalish: <i>shaharga qadar, qoidaga koʻra, ishga nisbatan</i>
• chiqish: <i>soʻzdan keyin, kechadan beri, ishdan oldin</i>

<b>🧩 Maʼnolari:</b> vosita (<i>qalam bilan</i>), maqsad (<i>vatan uchun</i>), oʻxshatish (<i>quyoshday, gul kabi</i>), chegara (<i>kechgacha</i>), yoʻnalish (<i>shu tomon</i>).

<b>✍️ Imlo:</b> koʻmakchilar oʻzidan oldingi soʻzdan alohida yoziladi: <i>maktab uchun, doʻst bilan</i>.

<b>🧩 Gapdagi vazifasi:</b> mustaqil gap boʻlagi emas; oʻzi bogʻlangan soʻz bilan birga hol yoki toʻldiruvchi boʻladi."""

TUR["boglovchi"] = """🧩 <b>BOGʻLOVCHI</b>

<b>Nima?</b> Soʻzlarni, soʻz birikmalarini, gap boʻlaklarini va gaplarni bir-biriga bogʻlovchi yordamchi soʻz.

<b>📌 Maʼnoviy tuzilishi</b>
<b>A) Teng bogʻlovchilar (teng huquqli qismlarni bogʻlaydi)</b>
• <b>Biriktiruvchi</b>: va, hamda, ham, -u (-yu), na…na
• <b>Zidlovchi</b>: lekin, ammo, biroq, balki, holbuki
• <b>Ayiruvchi</b>: yoki, yo, goh…goh, dam…dam, bir…bir, yo…yo

<b>B) Ergashtiruvchi bogʻlovchilar (ergash gapni bosh gapga bogʻlaydi)</b>
• <b>Sabab</b>: chunki, negaki, zeroki • <b>Shart</b>: agar, basharti, mabodo
• <b>Toʻsiqsizlik</b>: garchi, garchand • <b>Maqsad</b>: toki, deb
• <b>Izohlash</b>: ki • <b>Qiyoslash</b>: goʻyo, xuddi

<b>🧱 Tuzilishi:</b> sodda (<i>va, ammo</i>), qoʻshma (<i>shuning uchun, hamda, nima uchun</i>), juft (<i>goh-goh</i>).

<b>✍️ Tinish belgisi</b>
• <i>lekin, ammo, biroq</i> oldidan vergul qoʻyiladi.
• Uyushiq boʻlaklarni bogʻlovchi <i>va</i> oldidan vergul <b>qoʻyilmaydi</b>.

<b>🧩 Gapdagi vazifasi:</b> gap boʻlagi emas, faqat bogʻlaydi."""

TUR["yuklama"] = """✨ <b>YUKLAMA</b>

<b>Nima?</b> Soʻzga, birikmaga yoki gapga qoʻshimcha maʼno va his-tuygʻu yuklaydigan yordamchi soʻz.

<b>📌 Maʼnoviy tuzilishi</b>
• <b>Soʻroq</b>: -mi, -chi (<i>Keldingmi? Sen-chi?</i>)
• <b>Koʻrsatish-ajratish</b>: faqat, hatto, aynan, xuddi, xolos (<i>Hatto u keldi.</i>)
• <b>Kuchaytiruv</b>: -ku, -da, -u (-yu), -oq, -ey, -a (<i>Keldi-ku! Oʻzi-oq!</i>)
• <b>Chegaralash</b>: faqat, -gina, xolos, bor-yoʻgʻi (<i>Faqat bitta.</i>)
• <b>Gumon</b>: -dir, shekilli, chamasi, ehtimol
• <b>Inkor</b>: emas
• <b>His-hayajon</b>: naqadar (<i>Naqadar goʻzal!</i>)

<b>✍️ Imlo</b>
• <i>-mi</i> va <i>-gina</i> qoʻshib yoziladi: <i>keldimi, yaxshigina</i>.
• <i>-chi, -ku</i> chiziqcha bilan: <i>Sen-chi? Keldi-ku!</i>
• <i>faqat, hatto, xolos</i> — alohida yoziladi.

<b>🧩 Gapdagi vazifasi:</b> gap boʻlagi emas; qaysi soʻzga taalluqli boʻlsa, oʻsha soʻzga maʼno beradi.

<b>⚠️ Eslatma:</b> Yuklamani koʻmakchi va bogʻlovchidan farqlash uchun: u soʻzlarni bogʻlamaydi, balki maʼno qoʻshadi."""

TUR["undov"] = """❗ <b>UNDOV SOʻZ</b>

<b>Nima?</b> His-tuygʻu, hayajon, buyruq yoki nutq odobini bildiradigan, lekin ularni atamaydigan soʻz.

<b>📌 Maʼnoviy tuzilishi</b>
• <b>His-hayajon</b>: oh, voy, uf, eh, bay-bay, ofarin, attang, dod
• <b>Buyruq-chaqiriq</b>: hoy, hey, ey, hay
• <b>Nutq odobi</b>: rahmat, marhamat, xayr, kechirasiz, tashakkur, salom

<b>🧱 Tuzilishi:</b> sodda (<i>oh, voy</i>), qoʻshma (<i>yo tavba</i>), juft (<i>bay-bay</i>).

<b>🧩 Gapdagi vazifasi:</b> gap boʻlagi emas, gapning boshqa boʻlaklari bilan grammatik aloqaga kirishmaydi.

<b>✍️ Tinish belgisi</b>
• Undov soʻzdan keyin <b>undov belgisi</b> yoki <b>vergul</b> qoʻyiladi: <i>Oh, qanday goʻzal! Voy! Nega keldi?</i>

<b>⚠️ Undov va undalma farqi</b>
• <b>Undov</b> — his-tuygʻuni bildiradi: <i>Voy, qanday goʻzal!</i>
• <b>Undalma</b> — kimgadir murojaat: <i>Ali, bu yoqqa kel!</i> Undalma gap boʻlagi emas: u kimgadir murojaat qilinayotganini koʻrsatadi va vergul bilan ajratiladi."""

TUR["modal"] = """💭 <b>MODAL SOʻZ</b>

<b>Nima?</b> Soʻzlovchining gapdagi fikrga munosabatini (ishonch, gumon, taxmin, tasdiq va hokazo) bildiradigan soʻz.

<b>📌 Maʼnoviy tuzilishi</b>
• <b>Ishonch</b>: albatta, shubhasiz, haqiqatan, darhaqiqat, tabiiyki, shak-shubhasiz
• <b>Gumon-taxmin</b>: ehtimol, balki, shekilli, chamasi
• <b>Tasdiq</b>: ha, xoʻp, toʻgʻri, mayli
• <b>Xursandchilik / afsus</b>: xayriyat, afsuski, taassuf, baxtimizga

<b>🧱 Tuzilishi:</b> sodda (<i>balki</i>), qoʻshma (<i>shubhasiz</i>), juft (<i>shak-shubhasiz</i>).

<b>🧩 Gapdagi vazifasi:</b> kirish soʻz sifatida gap boʻlagi emas; vergul bilan ajratiladi: <i>Albatta, boraman.</i>

<b>⚠️ Eslatma:</b> Modal soʻz gap boshida, oʻrtasida va oxirida kelishi mumkin. Esse yozganda ularni qoʻllash fikrni aniq ifodalaydi, lekin haddan oshirmang: har gapda <i>albatta</i> deyilsa, nutq zerikarli boʻladi."""

TUR["taqlid"] = """🔊 <b>TAQLID SOʻZ</b>

<b>Nima?</b> Tabiatdagi, hayvonlar va narsalardagi tovushga yoki harakat-holatga taqlid qilib yasalgan soʻz.

<b>📌 Maʼnoviy tuzilishi</b>
• <b>Tovushga taqlid</b>: gup-gup, gumbur-gumbur, taq-tuq, shitir-shitir, qars-qurs, tars-turs
• <b>Holat, harakatga taqlid</b>: yaltir-yultur, jimir-jimir, apil-tapil, dir-dir, lip-lip

<b>🧱 Tuzilishi:</b> asosan takroriy yoki juft shaklida: <i>taq-taq, shitir-shitir, apil-tapil</i>.

<b>🔁 Yasalishi:</b> taqlid soʻzlardan feʼl yasaladi: <i>shitirla, gʻijirla, taqilla, yaltilla</i>; ot ham yasaladi: <i>shitirlash, chirqillash</i>.

<b>🧩 Gapdagi vazifasi:</b> hol (<i>Qor gʻijir-gʻijir qilib yogʻdi.</i>), aniqlovchi, kesim (<i>Eshik gʻijir etdi.</i>).

<b>⚠️ Eslatma:</b> Taqlid soʻz badiiy nutqni jonli qiladi: <i>Yomgʻir shitirlab yogʻdi</i> — oddiy <i>yogʻdi</i> dan koʻra boy."""

SEC = {}
SEC["fonetika"] = """🔤 <b>FONETIKA VA ORFOEPIYA</b>

<b>Tovush va harf.</b> Tovush — talaffuz, harf — yozuv belgisi. Oʻzbek lotin alifbosida <b>29 harf</b> va tutuq belgisi (ʼ) bor: a, b, d, e, f, g, h, i, j, k, l, m, n, o, p, q, r, s, t, u, v, x, y, z, oʻ, gʻ, sh, ch, ng.

<b>🔴 Unlilar (6 ta):</b> a, e, i, o, u, oʻ
• Lab ishtirokiga koʻra: <b>lablangan</b> (u, oʻ, o), <b>lablanmagan</b> (i, e, a)
• Tilning vertikal holati: <b>yuqori</b> (i, u), <b>oʻrta</b> (e, oʻ), <b>quyi</b> (a, o)
• Tilning gorizontal holati: <b>old qator</b> (i, e, a), <b>orqa qator</b> (u, oʻ, o)

<b>🔵 Undoshlar (23 ta)</b>
• Jarangli: b, v, g, d, z, j, gʻ • Jarangsiz: p, f, k, q, t, s, sh, x, h, ch
• Sonor: m, n, ng, l, r, y

<b>✂️ Boʻgʻin.</b> Boʻgʻinlar soni unlilar soniga teng: <i>oʻ-qi-tuv-chi-lar</i> (5 boʻgʻin). Boʻgʻin ochiq (unli bilan tugaydi: <i>ma-na</i>) va yopiq (undosh bilan: <i>kitob</i>) boʻladi. <i>sh, ch, ng, oʻ, gʻ</i> bir tovushni bildiradi, koʻchirishda ajratilmaydi.

<b>🎵 Urgʻu.</b> Odatda oxirgi boʻgʻinga tushadi: <i>kitób, maktáb</i>. Ravish, bogʻlovchi va undov soʻzlarda oldingi boʻgʻinga ham tushishi mumkin.

<b>🔄 Tovush oʻzgarishlari</b>
• Almashinish: <i>yurak → yuragi, qishloq → qishlogʻi</i> (k→g, q→gʻ)
• Unli tushishi: <i>oʻrin → oʻrni, burun → burni, ogʻiz → ogʻzi</i>
• Unli tushishi: <i>singil → singlim</i>
• Qoʻshimchada: <i>-ga → -ka, -qa</i> (<i>tokka, ariqqa</i>)

<b>📣 Orfoepiya</b> — adabiy talaffuz qoidalari. Toʻgʻri talaffuz imloni ham yaxshilaydi."""

SEC["imlo"] = """✍️ <b>IMLO QOIDALARI</b>

<b>🔹 Tutuq belgisi (ʼ)</b> unli va undosh orasida yoziladi: <i>maʼno, eʼlon, aʼlo, taʼlim, sheʼr, jurʼat, saʼy, iʼtiqod</i>.
<b>oʻ, gʻ</b> harflari: <i>oʻzbek, gʻoya</i>. Tutuq (ʼ) bilan oʻ/gʻ ni aralashtirmang.

<b>🔹 Koʻp xato qilinadigan soʻzlar</b>
kutubxona (qutubxona emas), imtihon, mahalla, hayot, ehtiyot, mehnat, mamlakat, sanʼat, iqtisodiyot, madaniyat, ijtimoiy, mustaqillik, ahamiyat, tarbiya, iltimos, tabiat, mavjud, shaxs, aqlli, uslub, mutaxassis, Oʻzbekiston.

<b>🔹 Qoʻshib yoziladigan soʻzlar:</b> temiryoʻl, kitobxon, boshqarma, nafaqat.
<b>🔹 Chiziqcha bilan:</b> juft (<i>ota-ona, katta-kichik</i>), takroriy (<i>tez-tez, uy-uy</i>), raqam bilan (<i>5-sinf, 1991-yil, 3-qavat</i>).
<b>🔹 Alohida yoziladigan soʻzlar:</b> koʻmakchilar (<i>maktab uchun</i>), <i>hech kim, har kim, shu yerda</i>.

<b>🔹 Bosh harf bilan:</b> gap boshi, atoqli otlar (<i>Anvar, Samarqand, Oʻzbekiston</i>), muassasa nomi (<i>Oʻzbekiston Respublikasi Prezidenti</i>), bayram (<i>Navroʻz, Mustaqillik kuni</i>).

<b>🔹 Boʻgʻin koʻchirish:</b> boʻgʻin boʻyicha: <i>ki-tob, mav-zu</i>; bitta harf oldingi qatorda qoldirilmaydi yoki keyingi qatorga koʻchirilmaydi.

<b>🔹 Qoʻshimchalar imlosi:</b> <i>-ga</i> emas, <i>-ka, -qa</i>: <i>tokka, qishloqqa</i>. Son bilan: <i>5 ta</i> (alohida), <i>5-sinf</i> (chiziqcha). Tartib: <i>3-oʻrin, ikkinchi</i>.

<b>💡 Imlo xatosini qanday kamaytirish:</b> esse yozgach, hamma soʻzni oʻqib chiqing, shubhali soʻzni lugʻatdan tekshiring. Sayt tekshiruvchisi koʻp xatoni oʻzi topadi."""

SEC["punkt"] = """❓ <b>TINISH BELGILARI</b>

<b>• Nuqta (.)</b> — darak gap oxirida. <b>Soʻroq (?)</b> — soʻroq gap oxirida. <b>Undov (!)</b> — his-hayajon, buyruq, murojaat.

<b>• Vergul (,) qoʻyiladi:</b>
1) uyushiq boʻlaklar orasida: <i>Olma, nok, uzum pishdi.</i> (<i>va, hamda</i> bilan bogʻlansa — qoʻyilmaydi)
2) undalma, kirish soʻzlar ajratilganda: <i>Ali, kel! Albatta, kelaman.</i>
3) ajratilgan boʻlaklar, izohlovchi: <i>Navoiy, buyuk shoir, 1441-yilda tugʻilgan.</i>
4) qoʻshma gap qismlari orasida: <i>Havo sovuq, lekin biz chiqdik.</i> (<i>lekin, ammo, biroq</i> dan oldin)
5) ergash gap bosh gapdan ajratilganda: <i>Agar yomgʻir yogʻsa, uyda qolamiz.</i>

<b>• Nuqtali vergul (;)</b> — ichida vergul boʻlgan uyushiq boʻlaklar yoki bogʻlovchisiz qoʻshma gap qismlarini ajratadi.

<b>• Ikki nuqta (:)</b> — umumlashtiruvchi soʻz uyushiq boʻlaklardan <b>oldin</b> kelsa: <i>U hamma narsani oldi: kitob, daftar, qalam.</i> Muallif gapi koʻchirma gapdan oldin kelganda: <i>U dedi: «Boraman».</i>

<b>• Tire (—)</b>
1) ega va kesim ot, son yoki olmosh boʻlsa: <i>Toshkent — Oʻzbekiston poytaxti.</i>
2) umumlashtiruvchi soʻz uyushiq boʻlaklardan <b>keyin</b> kelsa: <i>Olma, nok, uzum — hammasi pishdi.</i>
3) koʻchirma gapda: <i>«Boraman», — dedi u.</i>; dialogda har bir qator oldidan.

<b>• Koʻp nuqta (…)</b> — fikr tugallanmaganda yoki pauza.
<b>• Qoʻshtirnoq (« »)</b> — koʻchirma gap, nomlar (<i>«Oʻtkan kunlar»</i>), shartli soʻzlar.
<b>• Qavs ( )</b> — izoh, qoʻshimcha maʼlumot.

<b>⚠️ Eslatma:</b> Ega va kesim orasidagi tire feʼl kesimdan oldin qoʻyilmaydi: <i>Ali keldi.</i> (tiresiz)."""

SEC["leks"] = """📚 <b>LEKSIKOLOGIYA (SOʻZ MAʼNOSI)</b>

<b>1) Soʻzning maʼnosi</b>
• Bir maʼnoli: <i>kitob, daftar</i> • Koʻp maʼnoli (polisemiya): <i>koʻz (organ, teshik, koʻz yoshi)</i>
• Toʻgʻri va koʻchma maʼno. Koʻchish turlari: <b>metafora</b> (oʻxshashlik: <i>choynak tumshugʻi</i>), <b>metonimiya</b> (aloqadorlik: <i>Zal qarsak chaldi</i>), <b>sinekdoxa</b> (qism bilan butunni atash).

<b>2) Soʻzlarning maʼno munosabati</b>
• <b>Sinonim</b>: maʼnodosh — <i>chiroyli, goʻzal, latofatli</i>; birinchisi — <b>dominanta</b> (betaraf, asosiy soʻz).
• <b>Antonim</b>: qarama-qarshi maʼno — <i>katta — kichik, yaxshi — yomon</i>.
• <b>Omonim</b>: shakli bir xil, maʼnosi har xil — <i>tuz (ovqatga) — tuz (feʼl)</i>, <i>ot (hayvon) — ot (ism)</i>.
• <b>Paronim</b>: shakli yaqin, maʼnosi har xil — <i>soda — sodda</i>.

<b>3) Qoʻllanishiga koʻra</b>
• <b>Arxaizm</b> — eskirgan, oʻrniga yangi soʻz kelgan soʻz
• <b>Istorizm</b> — predmeti yoʻqolgan tarixiy soʻz (<i>amir, mingboshi</i>)
• <b>Neologizm</b> — yangi paydo boʻlgan soʻz (<i>internet, blog</i>)
• <b>Dialektizm</b> — shevaga xos soʻz, <b>Jargon</b> — kasb-hunar yoki guruh nutqi

<b>4) Kelib chiqishiga koʻra:</b> oʻzbekcha soʻzlar (<i>ota, koʻz</i>), arabcha (<i>kitob, ilm</i>), forscha-tojikcha (<i>zamin, gul</i>), rus-yevropa (<i>teatr, kompyuter</i>).

<b>5) Frazeologizm va maqol:</b> turgʻun birikma — <i>koʻz ochib yumguncha</i>, <i>tilni tishlamoq</i>. Maqol — hikmatli gap: <i>Oltin olma, bilim ol.</i>"""

SEC["morf"] = """🧩 <b>MORFEMIKA VA SOʻZ YASALISHI</b>

<b>Morfema</b> — soʻzning maʼnoli eng kichik boʻlagi.
• <b>Ildiz morfema</b>: <i>kitob, ish, yoz</i>
• <b>Qoʻshimcha</b> (affiks): lugʻaviy (soʻz yasovchi) va grammatik (shakl yasovchi)

<b>Soʻz yasash usullari</b>
1) <b>Qoʻshimcha bilan (affiksatsiya)</b>: <i>kitob + xon, ish + chi, gul + zor, aql + li</i>
2) <b>Qoʻshish (kompozitsiya)</b>: <i>temir + yoʻl → temiryoʻl, koʻz + oynak → koʻzoynak</i>
3) <b>Takrorlash</b>: <i>katta-katta, uy-uy</i>
4) <b>Qisqartirish</b>: <i>BMT, OTM, PTT</i>
5) <b>Oʻtish (konversiya)</b>: bir turkum boshqa turkumga oʻtadi — <i>yoshlar (sifat → ot), katta (sifat → ot)</i>.

<b>Soʻz yasovchi qoʻshimchalar</b>
• Ot: <i>-chi, -xon, -zor, -lik, -kor, -gar, -xona, -noma, -shunos, -iston</i> (<i>ishchi, tinchlik, kitobxona</i>)
• Sifat: <i>-li, -siz, -iy, -dor, -chan, -ona, -simon, -gi</i> (<i>bilimli, aqlsiz, ilmiy</i>)
• Feʼl: <i>-la, -lan, -lash, -sira</i> (<i>ishla, ishlan, kulimsira</i>)
• Ravish: <i>-cha, -ona, -lab, -dan</i> (<i>oʻzbekcha, soatlab</i>)
• Son: <i>-inchi, -ta, -ov</i> (<i>beshinchi, beshta</i>)

<b>Shakl yasovchilar:</b> koʻplik (-lar), egalik (-im, -ing), kelishik (-ning, -ni, -ga, -da, -dan), shaxs-son (-man, -san), zamon, nisbat.

<b>Asos va negiz:</b> shakl qoʻshimchasi qoʻshilishidan oldingi qism — <b>asos</b>: <i>kitoblarim → kitoblar+im → asos — kitoblar</i>.

<b>⚠️ Eslatma:</b> Yasama soʻz yangi maʼno, yangi turkum hosil qiladi (<i>ish → ishchi</i>), shakl yasovchi esa faqat shaklni oʻzgartiradi (<i>kitob → kitoblar</i>)."""

SEC["sintaksis"] = """📐 <b>SINTAKSIS</b>

<b>1) Soʻz birikmasi</b> — ikki va undan koʻp mustaqil soʻzning tobe aloqasi (<i>kitob oʻqimoq</i>). Aloqa usullari:
• <b>Moslashuv</b> (qaratqich + egalik): <i>maktabning hovlisi</i>
• <b>Boshqaruv</b> (kelishik bilan): <i>kitobni oʻqimoq, uyga bormoq</i>
• <b>Bitishuv</b> (qoʻshimchasiz): <i>baland bino, tez yurmoq</i>

<b>2) Gap boʻlaklari</b>
• Bosh: <b>ega</b> (<i>kim? nima?</i>), <b>kesim</b> (<i>nima qildi?</i>)
• Ikkinchi darajali: <b>toʻldiruvchi</b> (<i>kimni? nimani? kimga?...</i>), <b>aniqlovchi</b> (sifatlovchi, qaratqich, izohlovchi), <b>hol</b> (payt, oʻrin, sabab, maqsad, tarz, daraja, miqdor)

<b>3) Gap turlari</b>
• Maqsad: darak, soʻroq, buyruq • His-tuygʻu: undovli, undovsiz
• Tuzilishi: sodda / qoʻshma • Yoyiq / yigʻiq • Toʻliq / toʻliqsiz
• Bosh boʻlak soniga koʻra: <b>ikki tarkibli</b> (ega + kesim) va <b>bir tarkibli</b> (<i>Tun. Kechqurun boraman.</i>)

<b>4) Qoʻshma gap</b>
• <b>Bogʻlangan</b> (teng): <i>Havo sovuq, lekin biz chiqdik.</i>
• <b>Ergashgan</b>: <i>Agar yomgʻir yogʻsa, uyda qolamiz.</i> Ergash gap turlari: ega, kesim, toʻldiruvchi, aniqlovchi, payt, oʻrin, sabab, maqsad, shart, toʻsiqsizlik, natija, ravish, miqdor-daraja
• <b>Bogʻlovchisiz</b>: <i>Yoz keldi, kunlar isidi.</i>

<b>5) Boshqa hodisalar</b>
• Uyushiq boʻlaklar (<i>Olma, nok, uzum pishdi</i>)
• Ajratilgan boʻlaklar, undalma, kirish soʻz va kirish gap
• Koʻchirma gap (<i>«Boraman», — dedi Ali.</i>) va oʻzlashtirma gap (<i>Ali boraman, dedi.</i>)

<b>⚠️ Qoida:</b> kesim egaga shaxs-sonda mos keladi: <i>Biz keldik, Ular keldi.</i>"""

SEC["uslub"] = """🎭 <b>USLUBIYAT</b>

Nutq uslubi — til vositalaridan maqsadga muvofiq foydalanish.

<b>5 ta nutq uslubi</b>
1) <b>Soʻzlashuv</b> — kundalik muloqot. Soʻzlari: <i>qalay, yuring, bola-chaqa</i>.
2) <b>Ilmiy</b> — maqola, darslik. Terminlar, aniqlik, dalil: <i>Fotosintez — oʻsimliklarda organik moddalarning hosil boʻlishi.</i>
3) <b>Rasmiy (idoraviy)</b> — ariza, buyruq, bayonnoma, tavsifnoma: <i>Sizdan iltimos qilaman… Buyuraman…</i>
4) <b>Publitsistik</b> — gazeta, esse, nutq. Fikr va tuygʻu, ommaviy ruhi.
5) <b>Badiiy</b> — she'riyat, nasr. Obrazlilik, tasvir vositalari.

<b>Esse uslubi.</b> Esse — <b>publitsistik + badiiy</b> uslub. Shaxsiy fikr, dalil, obrazli til. Soʻzlashuv soʻzlaridan (<i>zoʻr, qalay, yuring</i>) qochish kerak.

<b>🏗 Esse tuzilishi</b>
1) <b>Kirish</b>: mavzuga qiziqtiruvchi boshlanma + tezis (asosiy fikr)
2) <b>Asosiy qism</b>: 2–3 xatboshi — dalil, misol, shaxsiy tajriba, qarshi fikr va unga javob
3) <b>Xulosa</b>: fikr yakuni, murojaat yoki umid

<b>⚠️ Uslubiy xatolar</b>
• Takror: <i>“Bu esseda men yozaman, men aytaman, men fikr qilaman”</i>
• Klishe: <i>“Bugungi kunda hammamizga ma’lumki…”</i> (haddan ortiq)
• Ortiqcha <i>juda</i>, undov, soʻzlashuv: <i>“zoʻr”, “qalay”</i>
• Ortiqcha soʻz (pleonazm): <i>“shaxsiy oʻz fikrim”</i>

<b>💡 Maslahat:</b> Gapni qisqa va aniq qiling. Har xatboshida bitta asosiy fikr boʻlsin."""

SEC["adabiyot"] = """🎨 <b>ADABIY NAZARIYA: TASVIR VOSITALARI</b>

<b>Tasvir vositalari</b>
• <b>Oʻxshatish</b>: <i>Yuzi oydek yorqin.</i>
• <b>Epitet</b> (sifatlash, badiiy aniqlovchi): <i>oltin kuz, mehribon quyosh</i>
• <b>Jonlantirish (tashxis)</b>: <i>Quyosh kulib boqdi.</i>
• <b>Mubolagʻa</b>: boʻrttirish — <i>Ming yillik gʻamga tushdi.</i>
• <b>Tazod</b>: qarama-qarshi qoʻyish — <i>Kecha va kunduz.</i>
• <b>Metafora</b>: koʻchma maʼnoda — <i>Vatan — ona.</i>
• <b>Kinoya</b>: yashirin kulgi, istehzo
• <b>Takrir, ritorik savol</b>: javob talab qilmaydigan savol — <i>Vatan nima?</i>

<b>Adabiy turlar va janrlar</b>
• <b>Epos</b>: roman, qissa, hikoya, doston, ertak
• <b>Lirika</b>: gʻazal, ruboiy, tuyuq, masnaviy, qasida, muxammas, murabbaʼ
• <b>Drama</b>: tragediya, komediya, drama

<b>Sheʼr tuzilishi</b>
• <b>Bayt</b> (ikki misra), <b>band</b>, <b>qofiya</b> (misralar oxirida), <b>radif</b> (qofiyadan keyin takrorlanuvchi soʻz), <b>matla</b> (gʻazalning birinchi bayti), <b>maqta</b> (oxirgi bayt — shoir taxallusi)
• <b>Vazn</b>: aruz, barmoq, erkin
• <b>Ruboiy</b> — 4 misra, a-a-b-a yoki a-a-a-a qofiyali

<b>Mashhur asarlar (testlar uchun)</b>
• Yusuf Xos Hojib — «Qutadgʻu bilig»
• Mahmud Koshgʻariy — «Devonu lugʻotit turk»
• Alisher Navoiy — «Xamsa» (5 doston: <i>Hayrat ul-abror, Farhod va Shirin, Layli va Majnun, Sabʼai sayyor, Saddi Iskandariy</i>)
• Zahiriddin Bobur — «Boburnoma»
• Abdulla Qodiriy — «Oʻtgan kunlar», «Mehrobdan chayon»
• Choʻlpon — «Kecha va kunduz»
• Abdulla Qahhor — «Sarob», «Sinchalak»
• Oybek — «Qutlugʻ qon», «Navoiy»
• Erkin Vohidov — «Ruhlar isyoni»"""

SEC["jadval"] = """📊 <b>QOʻSHIMCHALAR JADVALI</b>

<b>Kelishik qoʻshimchalari</b>
• Bosh: — (kim? nima?) → <i>Ali, kitob</i>
• Qaratqich: <b>-ning</b> (kimning? nimaning?) → <i>Alining, kitobning</i>
• Tushum: <b>-ni</b> (kimni? nimani?) → <i>Alini, kitobni</i>
• Joʻnalish: <b>-ga</b> (-ka, -qa) (kimga? nimaga? qayoqqa?) → <i>Aliga, tokka, ariqqa</i>
• Oʻrin-payt: <b>-da</b> (kimda? qayerda?) → <i>Alida, uyda</i>
• Chiqish: <b>-dan</b> (kimdan? qayerdan?) → <i>Alidan, uydan</i>

<b>Egalik qoʻshimchalari</b>
• 1-shaxs: -im, -m (<i>kitobim, onam</i>), -imiz, -miz
• 2-shaxs: -ing, -ng, -ingiz, -ngiz
• 3-shaxs: -i, -si (<i>kitobi, onasi</i>)

<b>Shaxs-son qoʻshimchalari</b>
• men -man, sen -san, u (—), biz -miz, siz -siz, ular -lar
• Oʻtgan zamonda: <i>bordim, bording, bordi, bordik, bordingiz, bordilar</i>

<b>Zamon qoʻshimchalari</b>
• Oʻtgan: <i>-di, -gan, -ib</i> • Hozirgi: <i>-yapti, -moqda, -yotir</i> • Kelasi: <i>-adi, -ar, -ajak, -moqchi</i>

<b>Tartib:</b> <b>asos + koʻplik + egalik + kelishik</b>
→ <i>kitob-lar-im-ning</i>

<b>Nisbat qoʻshimchalari:</b> oʻzlik <i>-n, -in</i>; majhul <i>-l, -il</i>; birgalik <i>-sh, -ish</i>; orttirma <i>-dir, -t, -tir, -giz</i>

<b>Fe'l shakllari:</b> sifatdosh <i>-gan, -uvchi, -ajak</i>; ravishdosh <i>-ib, -a, -gach, -guncha</i>; harakat nomi <i>-ish, -uv, -moq</i>"""

BTN_TUR = {k: v.split("\n", 1)[0] for k, v in TUR.items()}


# Har bir turkum uchun «Xatolar va mashq» sahifasi (javoblar <tg-spoiler> ichida: bosganda ochiladi)
PRAC = {}
PRAC["ot"] = """📌 <b>OT: xatolar va mashq</b>

<b>❌ Eng koʻp uchraydigan xatolar</b>
1) Son bilan ot koʻplikda: <s>beshta kitoblar</s> → <b>beshta kitob</b>
2) Joʻnalish imlosi: <s>qishloqga</s> → <b>qishloqqa</b>; <s>tokga</s> → <b>tokka</b>
3) Qoʻshimchalar tartibi: <s>kitobimlar</s> → <b>kitoblarim</b>
4) Ega-kesim orasida tire: <s>Ali talaba.</s> → <b>Ali — talaba.</b>
5) Atoqli ot kichik harf bilan: <s>toshkent</s> → <b>Toshkent</b>

<b>🔍 Tahlil namunasi:</b> <i>oʻquvchilarimizning</i> = oʻquvchi (ildiz) + <b>lar</b> (koʻplik) + <b>imiz</b> (1-shaxs koʻplik egalik) + <b>ning</b> (qaratqich kelishigi).

<b>📝 Oʻzingizni sinang</b> (javob yashirin, bosib oching)
1) «bolalarimdan» soʻzini qismlarga ajrating.
<tg-spoiler>bola + lar + im + dan (koʻplik, 1-shaxs egalik, chiqish kelishigi)</tg-spoiler>
2) «Alisher» — atoqli otmi yoki turdoshmi?
<tg-spoiler>Atoqli ot (odam ismi), bosh harf bilan yoziladi.</tg-spoiler>
3) «Xalq» qaysi ot: yakka yoki jamlovchi?
<tg-spoiler>Jamlovchi ot (koʻp kishini bir nom bilan ataydi).</tg-spoiler>

💡 <b>Maslahat:</b> otni topishning eng oson yoʻli — unga <i>kim? nima?</i> deb soʻrab, sonda va kelishikda oʻzgartirib koʻrish."""

PRAC["sifat"] = """📌 <b>SIFAT: xatolar va mashq</b>

<b>❌ Eng koʻp uchraydigan xatolar</b>
1) Sifatga koʻplik qoʻshish: <s>kattalar uylar</s> → <b>katta uylar</b>
2) Ikki daraja bir vaqtda: <s>eng chiroyliroq</s> → <b>eng chiroyli</b> yoki <b>chiroyliroq</b>
3) Ortiqcha qoʻshimcha: <s>juda yaxshiroq</s> → <b>juda yaxshi</b> yoki <b>ancha yaxshiroq</b>
4) Orttirma shakl imlosi: <s>qip qizil</s> → <b>qip-qizil</b>
5) Sifat va ravishni aralashtirish: <i>chiroyli yozdi</i> — «chiroyli» bu yerda ravish vazifasida (qanday yozdi?).

<b>📝 Oʻzingizni sinang</b>
1) «qip-qizil» qaysi daraja shakli?
<tg-spoiler>Orttirma daraja (belgini kuchaytiradi).</tg-spoiler>
2) «qoramtir» qaysi daraja?
<tg-spoiler>Kamaytirma daraja (-timtir/-imtir: belgi kuchsiz).</tg-spoiler>
3) «temirdek» asliy sifatmi yoki nisbiy?
<tg-spoiler>Nisbiy sifat: ot (temir) dan yasalgan, oʻxshatish bildiradi.</tg-spoiler>

💡 <b>Maslahat:</b> sifat ot oldida turadi va koʻplik, kelishik olmaydi. Agar olsa — u otlashgan: <i>yaxshilar</i> (ot)."""

PRAC["son"] = """📌 <b>SON: xatolar va mashq</b>

<b>❌ Eng koʻp uchraydigan xatolar</b>
1) <s>uchta kitoblar</s> → <b>uchta kitob</b> (son bilan ot koʻplikda boʻlmaydi)
2) <s>5ta daftar</s> → <b>5 ta daftar</b> (raqam va «ta» alohida)
3) <s>1990yilda</s> → <b>1990-yilda</b>
4) <s>5chi sinf</s> → <b>5-sinf</b>
5) <s>1-inchi sinf</s> → <b>1-sinf</b> yoki <b>birinchi sinf</b>

<b>📝 Oʻzingizni sinang</b>
1) «beshtadan» soni qaysi turga kiradi?
<tg-spoiler>Taqsim son (-tadan).</tg-spoiler>
2) «oʻnlab» qaysi turga kiradi?
<tg-spoiler>Chama son (taxminiy miqdor).</tg-spoiler>
3) «uchinchi» qaysi son?
<tg-spoiler>Tartib son (-inchi/-nchi): nechanchi?</tg-spoiler>

💡 <b>Maslahat:</b> «nechta?» — sanoq/dona son; «nechanchi?» — tartib son; «nechadan?» — taqsim son."""

PRAC["olmosh"] = """📌 <b>OLMOSH: xatolar va mashq</b>

<b>❌ Eng koʻp uchraydigan xatolar</b>
1) <s>meni kitobim</s> → <b>mening kitobim</b> (qaratqich kelishigi)
2) <s>uni uyi</s> → <b>uning uyi</b>
3) <s>ularni kitobi</s> → <b>ularning kitobi</b>
4) <s>senning</s> → <b>sening</b>
5) Oʻrin-payt: <s>menda kitob berdi</s> → <b>menga kitob berdi</b> (joʻnalish).

<b>📝 Oʻzingizni sinang</b>
1) «mening» qaysi kelishikda?
<tg-spoiler>Qaratqich kelishigi (men + -ning).</tg-spoiler>
2) «kimdir» qaysi olmosh?
<tg-spoiler>Gumon olmoshi.</tg-spoiler>
3) «hech narsa» qaysi olmosh?
<tg-spoiler>Boʻlishsizlik (inkor) olmoshi.</tg-spoiler>

💡 <b>Maslahat:</b> olmosh oʻzi ataydigan soʻzning oʻrnida keladi va xuddi shu soʻzdek gap boʻlagi boʻladi."""

PRAC["feil"] = """📌 <b>FEʼL: xatolar va mashq</b>

<b>❌ Eng koʻp uchraydigan xatolar</b>
1) Shaxs-son moslashuvi: <s>Biz keldi</s> → <b>Biz keldik</b>
2) Qoʻshma feʼl birga yozilgan: <s>sotibolmoq</s> → <b>sotib olmoq</b>
3) Koʻmakchi feʼl: <s>olibkeldi</s> → <b>olib keldi</b>
4) Bir gapda ikki marta inkor: <s>Hech kim kelmadi emas</s> — mantiqiy xato.
5) Zamon aralashishi: <s>Kecha u keladi</s> → <b>Kecha u keldi</b>

<b>📝 Oʻzingizni sinang</b>
1) «yozilgan» soʻzini tahlil qiling.
<tg-spoiler>yoz + il (majhul nisbat) + gan (sifatdosh)</tg-spoiler>
2) «-moqchi» qaysi zamon shaklini yasaydi?
<tg-spoiler>Kelasi zamon (kelmoqchi — keladi, niyat bilan).</tg-spoiler>
3) «Kelsa» qaysi maylda?
<tg-spoiler>Shart mayli (-sa).</tg-spoiler>

💡 <b>Maslahat:</b> feʼlni topish: <i>nima qildi?</i> — oʻtgan, <i>nima qiladi?</i> — kelasi, <i>nima qilyapti?</i> — hozirgi zamon."""

PRAC["ravish"] = """📌 <b>RAVISH: xatolar va mashq</b>

<b>❌ Eng koʻp uchraydigan xatolar</b>
1) <s>asta sekin</s> → <b>asta-sekin</b> (juft ravish — chiziqcha)
2) <s>tez tez</s> → <b>tez-tez</b>
3) <s>hechqachon</s> → <b>hech qachon</b> (alohida)
4) <s>juda yaxshiroq</s> → <b>juda yaxshi</b>
5) <s>oʻzbekchada gapirdi</s> → <b>oʻzbekcha gapirdi</b> (ravish kelishik olmaydi)

<b>📝 Oʻzingizni sinang</b>
1) «bugun» qaysi ravish?
<tg-spoiler>Payt ravishi (qachon?).</tg-spoiler>
2) «yuqorida» qaysi ravish?
<tg-spoiler>Oʻrin ravishi (qayerda?).</tg-spoiler>
3) «juda» qaysi ravish?
<tg-spoiler>Miqdor-daraja ravishi.</tg-spoiler>

💡 <b>Maslahat:</b> ravish feʼlga yoki sifatga bogʻlanadi va hol vazifasini bajaradi. <i>Tez yozdi</i> — ravish; <i>tez poyezd</i> — sifat."""

PRAC["komakchi"] = """📌 <b>KOʻMAKCHI: xatolar va mashq</b>

<b>❌ Eng koʻp uchraydigan xatolar</b>
1) Birga yozish: <s>Alibilan</s> → <b>Ali bilan</b>; <s>senuchun</s> → <b>sen uchun</b>
2) Notoʻgʻri kelishik: <s>kechani qadar</s> → <b>kechgacha</b> yoki <b>kechaga qadar</b>
3) «Kabi» oʻrniga ortiqcha: <s>xuddi gul kabidek</s> → <b>gul kabi</b>/<b>guldek</b>

<b>📝 Oʻzingizni sinang</b>
1) «qalam bilan yozdi» da «bilan» qanday maʼno beradi?
<tg-spoiler>Vosita (nima bilan?).</tg-spoiler>
2) «vatan uchun» da «uchun» qanday maʼno?
<tg-spoiler>Maqsad (nima uchun?).</tg-spoiler>
3) «gul kabi» da «kabi» qanday maʼno?
<tg-spoiler>Oʻxshatish.</tg-spoiler>

💡 <b>Maslahat:</b> koʻmakchini «bilan, uchun, kabi, singari, sari, qadar...» roʻyxatidan eslab qoling; ular hamma vaqt boshqa soʻz bilan birga keladi."""

PRAC["boglovchi"] = """📌 <b>BOGʻLOVCHI: xatolar va mashq</b>

<b>❌ Eng koʻp uchraydigan xatolar</b>
1) <s>U keldi lekin men yoʻq edim.</s> → <b>U keldi, lekin men yoʻq edim.</b> (zidlovchi oldidan vergul)
2) <s>U keldi, va ketdi.</s> → <b>U keldi va ketdi.</b> (uyushiq boʻlak — vergulsiz)
3) <s>Uyga ketdik. Chunki kech edi.</s> → <b>Uyga ketdik, chunki kech edi.</b>
4) <s>Agar kelsang boraman.</s> → <b>Agar kelsang, boraman.</b> (ergash gapdan keyin vergul)
5) <s>Shuning uchun</s> oldidan nuqta emas, vergul: <b>Yomgʻir yogʻdi, shuning uchun uyda qoldik.</b>

<b>📝 Oʻzingizni sinang</b>
1) «ammo» qaysi bogʻlovchi?
<tg-spoiler>Teng bogʻlovchi, zidlovchi.</tg-spoiler>
2) «chunki» qaysi bogʻlovchi?
<tg-spoiler>Ergashtiruvchi bogʻlovchi, sabab maʼnosida.</tg-spoiler>
3) «goh... goh» qaysi turga kiradi?
<tg-spoiler>Ayiruvchi bogʻlovchi (takroriy).</tg-spoiler>

💡 <b>Maslahat:</b> teng bogʻlovchi gaplarni teng huquqli bogʻlaydi, ergashtiruvchi esa ergash gapni bosh gapga tobe qiladi."""

PRAC["yuklama"] = """📌 <b>YUKLAMA: xatolar va mashq</b>

<b>❌ Eng koʻp uchraydigan xatolar</b>
1) <s>Keldi mi?</s> → <b>Keldimi?</b> (-mi qoʻshib yoziladi)
2) <s>Keldi ku</s> → <b>Keldi-ku!</b>
3) Yuklamani ortiqcha ishlatmang: <s>faqat va faqat</s> → <b>faqat</b>

<b>📝 Oʻzingizni sinang</b>
1) «Keldingmi?» da «-mi» qaysi yuklama?
<tg-spoiler>Soʻroq yuklamasi.</tg-spoiler>
2) «Faqat bitta» da «faqat»?
<tg-spoiler>Chegaralash (ajratish) yuklamasi.</tg-spoiler>
3) «Keldi-ku» da «-ku»?
<tg-spoiler>Kuchaytiruv yuklamasi.</tg-spoiler>

💡 <b>Maslahat:</b> yuklama soʻzni bogʻlamaydi, balki unga maʼno qoʻshadi. Bu uni bogʻlovchi va koʻmakchidan ajratadi."""

PRAC["undov"] = """📌 <b>UNDOV SOʻZ: xatolar va mashq</b>

<b>❌ Eng koʻp uchraydigan xatolar</b>
1) <s>Oh qanday goʻzal</s> → <b>Oh, qanday goʻzal!</b> (undovdan keyin vergul/undov)
2) Undov bilan undalmani aralashtirish: <i>Ey, Ali!</i> — «ey» undov, «Ali» undalma.
3) Undovdan keyin ham vergul, ham undov belgisi qoʻyish mumkin: <b>Oh!</b> / <b>Oh,</b>

<b>📝 Oʻzingizni sinang</b>
1) «hoy» qaysi turga kiradi?
<tg-spoiler>Buyruq-chaqiriq undovi.</tg-spoiler>
2) «ofarin» qaysi turga kiradi?
<tg-spoiler>His-hayajon undovi (maqtov).</tg-spoiler>
3) «marhamat» qaysi turga kiradi?
<tg-spoiler>Nutq odobi undovi.</tg-spoiler>

💡 <b>Maslahat:</b> undov soʻz gap boʻlagi boʻlmaydi; u his-tuygʻuni bildiradi, xolos."""

PRAC["modal"] = """📌 <b>MODAL SOʻZ: xatolar va mashq</b>

<b>❌ Eng koʻp uchraydigan xatolar</b>
1) <s>Albatta men boraman.</s> → <b>Albatta, men boraman.</b>
2) <s>Balki yomgʻir yogʻadi.</s> → <b>Balki, yomgʻir yogʻadi.</b> (kirish soʻz ajratiladi)
3) Haddan ortiq ishlatish: har gapda <i>albatta, shubhasiz</i> deyish nutqni zerikarli qiladi.

<b>📝 Oʻzingizni sinang</b>
1) «ehtimol» qaysi maʼnoni bildiradi?
<tg-spoiler>Gumon, taxmin.</tg-spoiler>
2) «shubhasiz» qaysi maʼno?
<tg-spoiler>Ishonch.</tg-spoiler>
3) «xayriyat» qaysi maʼno?
<tg-spoiler>Xursandchilik (yengil tortish).</tg-spoiler>

💡 <b>Maslahat:</b> modal soʻz gapning mazmuniga soʻzlovchi munosabatini qoʻshadi va vergul bilan ajratiladi."""

PRAC["taqlid"] = """📌 <b>TAQLID SOʻZ: xatolar va mashq</b>

<b>❌ Eng koʻp uchraydigan xatolar</b>
1) <s>gʻijir gʻijir</s> → <b>gʻijir-gʻijir</b> (juft/takror — chiziqcha)
2) <s>taqtaq</s> → <b>taq-taq</b>
3) Feʼl bilan: <s>gʻijirketdi</s> → <b>gʻijir etdi</b> (alohida)

<b>📝 Oʻzingizni sinang</b>
1) «gumbur-gumbur» nimaga taqlid?
<tg-spoiler>Tovushga taqlid.</tg-spoiler>
2) «yaltir-yultur» nimaga taqlid?
<tg-spoiler>Holat, harakatga taqlid (yaltirash).</tg-spoiler>
3) «shitir» dan feʼl yasang.
<tg-spoiler>shitirla (shitirlamoq).</tg-spoiler>

💡 <b>Maslahat:</b> esseda taqlid soʻz tasvirni jonlantiradi: <i>yomgʻir shitirlab yogʻdi</i>."""

# ---- Yangi mavzular
NEW = {}
NEW["xarita"] = """🗺 <b>SOʻZ TURKUMLARI XARITASI</b>

Oʻzbek tilida soʻzlar 3 guruhga boʻlinadi:

<b>1️⃣ Mustaqil soʻzlar (6 ta)</b> — oʻzi maʼno bildiradi, gap boʻlagi boʻladi
• <b>Ot</b> — kim? nima? (kitob, Ali)
• <b>Sifat</b> — qanday? (chiroyli, katta)
• <b>Son</b> — nechta? nechanchi? (besh, beshinchi)
• <b>Olmosh</b> — oʻrniga qoʻllanadi (men, bu, kim)
• <b>Feʼl</b> — nima qildi? (yozdi, boradi)
• <b>Ravish</b> — qanday? qachon? (tez, bugun)

<b>2️⃣ Yordamchi soʻzlar (3 ta)</b> — oʻzi maʼno bermaydi, bogʻlaydi yoki maʼno qoʻshadi
• <b>Koʻmakchi</b> — bilan, uchun, kabi
• <b>Bogʻlovchi</b> — va, lekin, agar
• <b>Yuklama</b> — faqat, hatto, -mi, -ku

<b>3️⃣ Alohida turkumlar (3 ta)</b> — mustaqil ham, yordamchi ham emas
• <b>Undov</b> — oh, voy, hoy
• <b>Modal soʻz</b> — albatta, balki
• <b>Taqlid soʻz</b> — shitir-shitir, gumbur

<b>🔎 Qaysi turkumligini qanday aniqlash?</b>
1) Soʻroq bering: <i>kim? nima?</i> — ot; <i>qanday?</i> — sifat; <i>nechta?</i> — son; <i>nima qildi?</i> — feʼl.
2) Soʻroq berib boʻlmasa, u yordamchi yoki alohida soʻz.
3) Gapdagi vazifasini koʻring: bogʻlayaptimi — bogʻlovchi; kishini ataydimi — ot.

⚠️ Bir soʻz gapga qarab turkum oʻzgartiradi: <i>tez</i> — ravish (<i>tez yuguradi</i>) va sifat (<i>tez poyezd</i>). Shuning uchun turkumni doim gapda aniqlang."""

NEW["boluk"] = """🧱 <b>GAP BOʻLAKLARI</b>

Gap boʻlaklari <b>bosh</b> va <b>ikkinchi darajali</b> boʻlaklarga boʻlinadi.

<b>1) Bosh boʻlaklar</b>
• <b>Ega</b> — gapda kim yoki nima haqida gap ketayotganini bildiradi. Soʻroq: <i>kim? nima?</i>
  <i>Oʻquvchi kitob oʻqidi.</i> — ega: oʻquvchi
• <b>Kesim</b> — ega haqida nima deyilganini bildiradi. Soʻroq: <i>nima qildi? kim? qanday?</i>
  <i>Oʻquvchi kitob oʻqidi.</i> — kesim: oʻqidi

<b>2) Ikkinchi darajali boʻlaklar</b>
• <b>Toʻldiruvchi</b> — predmetni bildiradi. Soʻroq: <i>kimni? nimani? kimga? nimaga? kimdan?...</i>
  <i>Kitobni oʻqidi.</i> / <i>Doʻstiga yozdi.</i>
• <b>Aniqlovchi</b> — otni aniqlaydi. Soʻroq: <i>qanday? qaysi? kimning? nechta?</i>
  – sifatlovchi: <i>baland bino</i> – qaratqich: <i>maktabning hovlisi</i> – izohlovchi: <i>shoir Navoiy</i>
• <b>Hol</b> — harakatning holatini bildiradi. Turlari:
  – payt (<i>qachon?</i>): <i>ertalab keldi</i>
  – oʻrin (<i>qayerda? qayerga?</i>): <i>uyda oʻtirdi</i>
  – sabab (<i>nega?</i>): <i>charchoqdan yiqildi</i>
  – maqsad (<i>nima uchun?</i>): <i>oʻqish uchun keldi</i>
  – tarz (<i>qanday?</i>): <i>tez yurdi</i>
  – daraja/miqdor (<i>qancha?</i>): <i>juda yaxshi</i>

<b>🧪 Gap tahlili namunasi</b>
<i>Bahorda bogʻimizdagi daraxtlar chiroyli gulladi.</i>
• <b>daraxtlar</b> — ega • <b>gulladi</b> — kesim
• <b>bogʻimizdagi</b> — aniqlovchi (qaysi daraxtlar?) • <b>Bahorda</b> — payt holi (qachon?) • <b>chiroyli</b> — tarz holi (qanday?)

💡 <b>Maslahat:</b> gapni tahlil qilishni kesimdan boshlang: kesimni toping, unga <i>kim? nima?</i> deb soʻrang — ega chiqadi. Keyin boshqa boʻlaklarni soʻroq bilan aniqlang."""

NEW["uyushiq"] = """🔗 <b>UYUSHIQ, AJRATILGAN BOʻLAKLAR, UNDALMA, KIRISH SOʻZ</b>

<b>1) Uyushiq boʻlaklar</b> — bir xil soʻroqqa javob beradigan, bir boʻlakka bogʻlangan boʻlaklar.
<i>Olma, nok, uzum pishdi.</i> (uchta ega)
• Bogʻlovchisiz — vergul: <i>keldi, oʻtirdi, ketdi</i>
• <i>va, hamda</i> bilan — vergulsiz: <i>Ali va Vali keldi.</i>
• <i>lekin, ammo</i> bilan — vergul: <i>Keldi, lekin ketdi.</i>

<b>Umumlashtiruvchi soʻz:</b>
• oldin kelsa — ikki nuqta: <i>U hamma narsani oldi: kitob, daftar, qalam.</i>
• keyin kelsa — tire: <i>Kitob, daftar, qalam — hammasi stolda.</i>

<b>2) Undalma</b> — kimgadir murojaat. Gap boʻlagi emas. Vergul bilan ajratiladi:
<i>Ali, bu yoqqa kel! / Siz, ustoz, toʻgʻri aytdingiz.</i>

<b>3) Kirish soʻz va kirish gap</b> — soʻzlovchining munosabati. Vergul bilan:
<i>Albatta, men kelaman. / Aytgancha, imtihon qachon?</i>
Kirish gap qavs yoki tire ichida: <i>Biz (hammamiz shunday oʻylaymiz) bunga qarshimiz.</i>

<b>4) Ajratilgan boʻlak</b> — maʼnoni aniqlashtiradi, vergul yoki tire bilan ajratiladi:
<i>Toshkent, Oʻzbekiston poytaxti, katta shahar.</i> (izohlovchi)
<i>Navoiy — buyuk shoir — 1441-yilda tugʻilgan.</i>


⚠️ <b>Eslatma:</b> uyushiq boʻlaklar bogʻlovchisiz va <i>va</i> bilan kelganda tinish farqini eslang: <i>Ali, Vali, Salim keldi</i> va <i>Ali, Vali va Salim keldi</i>."""

NEW["qoshma"] = """🧩 <b>QOʻSHMA GAP</b>

Ikki yoki undan koʻp sodda gapdan tuzilgan gap qoʻshma gap deyiladi. Uch xil:

<b>1) Bogʻlangan qoʻshma gap</b> — teng bogʻlovchilar bilan:
• biriktiruvchi: <i>Yomgʻir yogʻdi va yoʻllar loyga botdi.</i>
• zidlovchi: <i>Havo sovuq edi, lekin biz sayrga chiqdik.</i>
• ayiruvchi: <i>Yo kitob oʻqiyman, yo film koʻraman.</i>
Tinish: <i>lekin, ammo, biroq</i> dan oldin vergul.

<b>2) Ergashgan qoʻshma gap</b> — bosh gap + ergash gap:
<i>Agar yomgʻir yogʻsa, biz uyda qolamiz.</i>
• ergash gap «agar» bilan boshlanib shart bildiradi
• bosh gap — «biz uyda qolamiz»
Tinish: ergash gap va bosh gap orasida vergul.

<b>3) Bogʻlovchisiz qoʻshma gap</b> — qismlar bogʻlovchisiz, ohang bilan bogʻlanadi:
<i>Kun botdi, qorongʻi tushdi.</i> / <i>Bilib qoʻying: u kelmaydi.</i>
Tinish: vergul, nuqtali vergul, ikki nuqta yoki tire.

<b>📝 Oʻzingizni sinang</b>
1) <i>Men kelganimda, u ketgan edi.</i> qanday gap?
<tg-spoiler>Ergashgan qoʻshma gap (payt ergash gap).</tg-spoiler>
2) <i>Qish keldi, kunlar sovidi.</i> qanday gap?
<tg-spoiler>Bogʻlovchisiz qoʻshma gap.</tg-spoiler>
3) <i>U keldi, ammo men yoʻq edim.</i> qanday gap?
<tg-spoiler>Bogʻlangan qoʻshma gap (zidlovchi).</tg-spoiler>

💡 <b>Maslahat:</b> qoʻshma gapni topish uchun kesimlarni sanang: nechta kesim — shuncha sodda gap."""

NEW["ergash"] = """📚 <b>ERGASH GAP TURLARI</b>

Ergash gap bosh gapdagi biror boʻlakni yoki butun gapni izohlaydi.

<b>A) Gap boʻlagi ergash gaplar</b> (bosh gapning boʻlagi oʻrnida):
• <b>Ega ergash gap</b> (kim? nima?): <i>Kim ishlasa, shu yeydi.</i>
• <b>Kesim ergash gap</b> (qanday?): <i>Gap shundaki, u kelmadi.</i>
• <b>Toʻldiruvchi ergash gap</b> (nimani?): <i>Men bilamanki, u kelmaydi.</i>
• <b>Aniqlovchi ergash gap</b> (qanday? qaysi?): <i>Shunday kishilar bor-ki, ular mehnatdan qochmaydi.</i>

<b>B) Hol ergash gaplar</b>
• <b>Payt</b> (qachon?): <i>Men kelganimda, u ketgan edi.</i>
• <b>Oʻrin</b> (qayerda?): <i>Qayerda mehnat bor, oʻsha yerda barakat bor.</i>
• <b>Sabab</b> (nega?): <i>U kelmadi, chunki kasal edi.</i>
• <b>Maqsad</b> (nima uchun?): <i>U oʻqidi, toki imtihondan oʻtsin.</i>
• <b>Shart</b> (qanday shartda?): <i>Agar yomgʻir yogʻsa, uyda qolamiz.</i>
• <b>Toʻsiqsizlik</b> (qaramasdan): <i>Garchi charchagan edi, ishladi.</i>
• <b>Natija</b>: <i>U shunday charchadiki, joyidan turolmadi.</i>

<b>🔎 Ergash gapni qanday topish?</b>
1) Gapdagi bogʻlovchini toping: <i>agar, chunki, garchi, toki, ki</i>.
2) Ergash gapga soʻroq bering: <i>qachon? nega? qanday shartda?</i>
3) Bosh gap — soʻroq beriladigan gap.

⚠️ Ergash gap va bosh gap orasida <b>vergul</b> qoʻyiladi."""

NEW["kochirma"] = """💬 <b>KOʻCHIRMA VA OʻZLASHTIRMA GAP</b>

<b>1) Koʻchirma gap</b> — birovning gapi aynan keltiriladi. Ikki qism: <b>muallif gapi</b> va <b>koʻchirma</b>.

Shakllar:
• Muallif gapi oldin: <i>Ali dedi: «Men ertaga kelaman».</i> (ikki nuqta + qoʻshtirnoq)
• Muallif gapi keyin: <i>«Men ertaga kelaman», — dedi Ali.</i> (vergul + tire)
• Muallif gapi oʻrtada: <i>«Men, — dedi Ali, — ertaga kelaman».</i>
• Soʻroq yoki undovda: <i>«Qachon kelasan?» — deb soʻradi u.</i>

<b>2) Oʻzlashtirma gap</b> — birovning gapi mazmuni bilan, oʻz soʻzlarimiz bilan beriladi.
<i>Ali ertaga kelishini aytdi.</i> Qoʻshtirnoq va tire yoʻq.

<b>🔄 Aylantirish (koʻchirmadan oʻzlashtirmaga)</b>
• <i>Ali: «Men kelaman», — dedi.</i> → <i>Ali oʻzi kelishini aytdi.</i>
• Kishilik olmoshi oʻzgaradi: <i>men → u (oʻzi)</i>
• Fe'l shakli oʻzgaradi: <i>kelaman → kelishini</i>

<b>📝 Oʻzingizni sinang</b>
1) <i>«Bu kitob menga yoqdi», — dedi Vali.</i> Bu qanday gap?
<tg-spoiler>Koʻchirma gap (muallif gapi keyin).</tg-spoiler>
2) <i>Vali kitob unga yoqqanini aytdi.</i> Bu qanday gap?
<tg-spoiler>Oʻzlashtirma gap.</tg-spoiler>

💡 Dialogda har bir qator tire bilan boshlanadi: <i>— Qalaysan? — Yaxshi.</i>"""

NEW["birikma"] = """🔤 <b>SOʻZ BIRIKMASI</b>

Soʻz birikmasi — ikki yoki undan koʻp mustaqil soʻzning maʼno va grammatik jihatdan bogʻlanishi.

<b>Ikki tur:</b>
• <b>Tobe aloqali</b> — bir soʻz boshqasiga tobe: <i>baland bino, kitob oʻqimoq</i>
• <b>Teng aloqali</b> — soʻzlar teng: <i>ota va ona, kitob va daftar</i>

<b>Tobe aloqa usullari</b>
1) <b>Moslashuv</b> — tobe soʻz egalik qoʻshimchasi bilan keladi:
<i>maktabning hovlisi, Alining kitobi</i>
2) <b>Boshqaruv</b> — tobe soʻz kelishik qoʻshimchasini oladi:
<i>kitobni oʻqimoq, uyga bormoq, maktabdan kelmoq</i>
3) <b>Bitishuv</b> — qoʻshimchasiz, tartib va ohang bilan:
<i>chiroyli gul, tez yurmoq, bugungi kun</i>

<b>Bosh va tobe soʻz:</b> <i>baland bino</i> — «bino» bosh soʻz, «baland» tobe soʻz.

<b>Qanday farqlanadi?</b>
• Birikmada fikr tugallanmaydi: <i>kitob oʻqimoq</i>.
• Gapda fikr tugallanadi, ega-kesim aloqasi bor: <i>Ali kitob oʻqidi.</i>

<b>📝 Oʻzingizni sinang</b>
1) «maktabning hovlisi» qaysi aloqa?
<tg-spoiler>Moslashuv (qaratqich + egalik).</tg-spoiler>
2) «kitobni oʻqimoq» qaysi aloqa?
<tg-spoiler>Boshqaruv (tushum kelishigi).</tg-spoiler>
3) «baland bino» qaysi aloqa?
<tg-spoiler>Bitishuv.</tg-spoiler>"""

NEW["esse"] = """📝 <b>ESSE YOZISH BOSQICHLARI</b>

<b>1️⃣ Mavzuni tushuning (2 daqiqa)</b>
Mavzudagi asosiy soʻzlarni belgilang. Savol: <i>bu mavzuda men nimani isbotlayman?</i>

<b>2️⃣ Reja tuzing (3 daqiqa)</b>
• Tezis (asosiy fikr) — 1 gap
• 2–3 dalil
• Misol yoki shaxsiy tajriba
• Xulosa

<b>3️⃣ Yozing</b>
<b>Kirish</b> (3–5 gap): mavzuga qiziqtiruvchi boshlanma + <b>tezis</b>.
Namuna boshlanmalar: savol bilan (<i>Til nima?</i>), maqol bilan, qisqa voqea bilan, ziddiyat bilan.

<b>Asosiy qism</b> (2–3 xatboshi): har xatboshida bitta fikr:
fikr → dalil → misol → mini-xulosa.

<b>Xulosa</b> (3–4 gap): fikrni yakunlang, yangi dalil keltirmang, umid yoki murojaat bilan tugating.

<b>🧷 Foydali bogʻlovchi iboralar</b>
• Fikrni qoʻshish: <i>bundan tashqari, shu bilan birga, ayniqsa</i>
• Qarama-qarshilik: <i>ammo, biroq, aksincha</i>
• Sabab-natija: <i>shuning uchun, demak, natijada</i>
• Misol: <i>masalan, chunonchi, buning isboti</i>
• Xulosa: <i>xulosa qilib aytganda, shunday qilib</i>

<b>✅ Topshirishdan oldin tekshiring</b>
1) Soʻz soni yetarlimi (kamida 100)?
2) Har gap bosh harf bilan boshlanib, nuqta bilan tugadimi?
3) Uyushiq boʻlak, undalma, kirish soʻzlarda vergul bormi?
4) h/x, tutuq belgisi, oʻ/gʻ toʻgʻrimi?
5) Soʻzlashuv soʻzlari yoʻqmi (<i>zoʻr, qalay</i>)?
6) Fikr mavzuga mosmi? Takrorlar yoʻqmi?

💡 Saytdagi «Esse ustaxonasi» esseni shu mezonlar boʻyicha tekshiradi."""

NEW["xatolar"] = """⚠️ <b>ENG KOʻP UCHRAYDIGAN 20 XATO</b>

<b>Imlo</b>
1) <s>qutubxona</s> → <b>kutubxona</b>
2) <s>imtixon</s> → <b>imtihon</b>
3) <s>mexnat</s> → <b>mehnat</b>
4) <s>xayot</s> → <b>hayot</b>
5) <s>halq</s> → <b>xalq</b>
6) <s>mutaxasis</s> → <b>mutaxassis</b>
7) <s>mustaqilik</s> → <b>mustaqillik</b>
8) <s>sanat</s> → <b>sanʼat</b>, <s>mano</s> → <b>maʼno</b>
9) <s>qishloqga</s> → <b>qishloqqa</b>, <s>tokga</s> → <b>tokka</b>

<b>Raqam va chiziqcha</b>
10) <s>5ta</s> → <b>5 ta</b>
11) <s>1990yil</s> → <b>1990-yil</b>
12) <s>asta sekin</s> → <b>asta-sekin</b>
13) <s>hechqachon</s> → <b>hech qachon</b>

<b>Grammatika</b>
14) <s>uchta kitoblar</s> → <b>uchta kitob</b>
15) <s>Biz keldi</s> → <b>Biz keldik</b>
16) <s>eng chiroyliroq</s> → <b>eng chiroyli</b>
17) <s>meni kitobim</s> → <b>mening kitobim</b>
18) <s>kitobimlar</s> → <b>kitoblarim</b>

<b>Tinish</b>
19) <s>Lekin</s> oldidan vergul: <b>Keldi, lekin ketdi.</b>
20) Kirish soʻzdan keyin vergul: <b>Albatta, boraman.</b>

💡 Bu xatolarni yoddan bilsangiz, esseda koʻp ball yigʻasiz. Test bilan mustahkamlang: «Testlar → ✍️ Yozma test»."""

NEW["imtihon"] = """🎯 <b>IMTIHONGA TAYYORGARLIK MASLAHATLARI</b>

<b>📅 Tayyorgarlik rejasi</b>
• Har kuni 15–20 daqiqa: 10 talik test (turli turkum yoki umumiy).
• Haftada 1–2 ta esse: sayt orqali yozib, tekshiring, xatolarni tuzating.
• Har kuni 5 yangi soʻz: lugʻat boʻlimidan.

<b>🧠 Testlarda</b>
1) Savolni oxirigacha oʻqing: «xato», «istisno», «emas» soʻzlariga eʼtibor bering.
2) Avval oson savollarga javob bering.
3) Variantlarni bartaraf qiling: aniq notoʻgʻrisini chiqarib tashlang.
4) Imlo savollarida soʻzni boʻgʻinlab oʻqing.

<b>✍️ Esseda</b>
1) Reja tuzing, keyin yozing.
2) Kirishni qisqa, asosiy qismni boy, xulosani aniq qiling.
3) Murakkab gap qurishdan koʻra, oddiy va toʻgʻri gap afzal: xato kamayadi.
4) Tugatgach, kamida 3 daqiqa tekshirish uchun qoldiring.

<b>🔁 Xatolar ustida ishlang</b>
• Xato qilgan soʻz va qoidani daftarga yozing.
• Bir xil xatoni qayta qilmaslik uchun 3 marta yozing.
• Botda «🔁 Qayta yechish» tugmasi bilan shu mavzuni takrorlang.

<b>🚀 Daraja oshirish yoʻli</b>
B → B+: imlo va tinish xatolarini kamaytiring.
B+ → A: tuzilma (kirish, asosiy qism, xulosa) va dalil qoʻshing.
A → A+: uslub, boy soʻz zaxirasi, obrazli tasvir va qarshi fikrga javob.

💡 Eng muhimi — muntazamlik. Har kuni oz-ozdan shugʻullaning!"""

NEW["tahlil"] = """🧪 <b>GAP VA SOʻZ TAHLILI NAMUNALARI</b>

<b>1) Soʻz tarkibi tahlili</b>
<i>oʻquvchilarimizning</i>
• oʻqi — ildiz, -uvchi — soʻz yasovchi, -lar, -imiz, -ning — shakl yasovchilar
• -lar — koʻplik
• -imiz — egalik (1-shaxs koʻplik)
• -ning — qaratqich kelishigi

<b>2) Soʻz turkumi tahlili</b>
<i>Kecha biz kutubxonada kitob oʻqidik.</i>
• Kecha — ravish (payt) • biz — kishilik olmoshi • kutubxonada — ot (oʻrin-payt kelishigi)
• kitob — ot (bosh kelishik) • oʻqidik — feʼl (oʻtgan zamon, 1-shaxs koʻplik)

<b>3) Gap boʻlaklari tahlili</b>
<i>Kecha biz kutubxonada kitob oʻqidik.</i>
• biz — ega • oʻqidik — kesim • kitob — toʻldiruvchi • Kecha — payt holi • kutubxonada — oʻrin holi

<b>4) Gap turi tahlili</b>
• Maqsadiga koʻra: darak • His-tuygʻu: undovsiz • Tuzilishi: sodda, yoyiq, toʻliq, ikki tarkibli

<b>5) Qoʻshma gap tahlili</b>
<i>Agar vaqtim boʻlsa, men sizga yordam beraman.</i>
• Ergashgan qoʻshma gap • ergash gap: <i>Agar vaqtim boʻlsa</i> (shart) • bosh gap: <i>men sizga yordam beraman</i>
• Bogʻlovchi: <i>agar</i>, aloqa vositasi: <i>-sa</i> shakli

💡 <b>Tahlil tartibi:</b> kesimlarni toping → sodda yoki qoʻshma ekanini aniqlang → boʻlaklarni soʻroq bilan belgilang → turkumlarni aniqlang."""

NEW_BTN = {
 "🗺 Turkumlar xaritasi": "xarita", "🧱 Gap boʻlaklari": "boluk", "🔗 Uyushiq va ajratilgan": "uyushiq",
 "🧩 Qoʻshma gap": "qoshma", "📚 Ergash gap turlari": "ergash", "💬 Koʻchirma gap": "kochirma",
 "🔤 Soʻz birikmasi": "birikma", "🧪 Tahlil namunalari": "tahlil", "📝 Esse yozish bosqichlari": "esse",
 "⚠️ Eng koʻp 20 xato": "xatolar", "🎯 Imtihonga tayyorgarlik": "imtihon"}


LESSON = {}   # {uid: oxirgi koʻrilgan turkum}
B_PRAC = "📌 Xatolar va mashq"
B_LEARN = "📚 Oʻrganish"
B_LT = "🧩 Soʻz turkumlari (12 ta)"
SEC_BTN = {"🔤 Fonetika": "fonetika", "✍️ Imlo qoidalari": "imlo", "❓ Tinish belgilari": "punkt",
           "📚 Leksikologiya": "leks", "🧱 Soʻz yasalishi": "morf", "📐 Sintaksis": "sintaksis",
           "🎭 Uslubiyat va esse": "uslub", "🎨 Adabiy nazariya": "adabiyot", "📊 Qoʻshimchalar jadvali": "jadval"}
LT_BTN = {"📗 " + t.split(" ", 1)[1]: k for k, t in {
    "ot": "🏷️ Ot", "sifat": "🎨 Sifat", "son": "🔢 Son", "olmosh": "👤 Olmosh", "feil": "🏃 Feʼl",
    "ravish": "⚡ Ravish", "komakchi": "🔗 Koʻmakchi", "boglovchi": "🧩 Bogʻlovchi", "yuklama": "✨ Yuklama",
    "undov": "❗ Undov soʻz", "modal": "💭 Modal soʻz", "taqlid": "🔊 Taqlid soʻz"}.items()}


# ------------------------------------------------------------------ AI esse tekshiruvi (Groq)
B_AI = "🤖 AI esse tekshiruvi"
GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"
GROQ_MODELS = [m for m in [(os.getenv("GROQ_MODEL") or "").strip(), "llama-3.3-70b-versatile",
                           "llama-3.1-8b-instant"] if m]
AIST = {}        # {uid: True} — esse kutayotgan foydalanuvchilar
AI_LAST = {}     # {uid: oxirgi soʻrov vaqti}
AI_DAY = {}      # {uid: (sana, soni)}
AI_PER_DAY = 8
AI_MIN_WORDS = 40


def groq_key():
    k = (os.getenv("GROQ_API_KEY") or "").strip()
    if not k:
        try:
            with open(os.path.join(DATA_DIR, "groq_key.txt"), encoding="utf-8") as f:
                k = f.read().strip()
        except Exception:
            k = ""
    return k


AI_SYSTEM = (
    "Sen Oʻzbekiston milliy sertifikat (ona tili) yozma imtihonining tajribali ekspertisan. "
    "Talabaning esseini tekshirasan. Javobing FAQAT oʻzbek tilida (lotin yozuvi) boʻlsin. "
    "Oʻzing ham toʻgʻri imlo bilan yoz. Markdown belgilarini (**, #) ishlatma.\n\n"
    "Baholash mezonlari (jami 100 ball): mazmun va mavzuga mosligi 25, tuzilishi (kirish, asosiy qism, xulosa) 20, "
    "dalil va misollar 15, imlo 15, tinish belgilari 10, uslub va soʻz boyligi 15.\n"
    "Daraja: 90–100 A+, 80–89 A, 70–79 B+, 60–69 B, 60 dan past — talab darajasidan past.\n\n"
    "Javob shakli (aynan shu sarlavhalar bilan):\n"
    "📊 UMUMIY BALL: N/100 — daraja\n"
    "📌 Mezonlar boʻyicha: har bir mezon uchun ball va 1 gap izoh\n"
    "❌ XATOLAR: eng muhim 6–10 ta xatoni «xato → toʻgʻrisi — sababi» koʻrinishida (faqat matnda haqiqatan bor xatolarni yoz, oʻylab topma)\n"
    "✅ KUCHLI TOMONLARI: 2–3 ta\n"
    "💡 MASLAHATLAR: keyingi esse uchun 3–4 ta aniq maslahat\n\n"
    "Matnda xato boʻlmasa, xato oʻylab topma. Qatʼiy, lekin xolis va xayrixoh boʻl. Javob 3000 belgidan oshmasin."
)


def groq_review(text):
    key = groq_key()
    if not key:
        return None, "nokey"
    last_err = "xato"
    for model in GROQ_MODELS:
        body = {"model": model, "temperature": 0.3, "max_tokens": 1600,
                "messages": [{"role": "system", "content": AI_SYSTEM},
                             {"role": "user", "content": "Mana talabaning essesi:\n\n" + text}]}
        req = urllib.request.Request(GROQ_URL, data=json.dumps(body).encode("utf-8"),
                                     headers={"Content-Type": "application/json",
                                              "Authorization": "Bearer " + key,
                                              "User-Agent": "ona-tili-bot/1.0"})
        try:
            with urllib.request.urlopen(req, timeout=60) as r:
                data = json.loads(r.read().decode("utf-8"))
            out = data["choices"][0]["message"]["content"].strip()
            return out.replace("**", "").replace("##", "").replace("# ", ""), None
        except urllib.error.HTTPError as e:
            last_err = f"http{e.code}"
            if e.code in (401, 403):
                return None, "badkey"
            if e.code == 429:
                return None, "limit"
            continue  # model topilmadi va h.k. — keyingisini sinaymiz
        except Exception as e:
            last_err = repr(e)[:80]
            continue
    return None, last_err


def ai_allowed(uid):
    now = time.time()
    if now - AI_LAST.get(uid, 0) < 20:
        return "Bir oz kuting, oldingi tekshiruv endigina boʻldi (20 soniya)."
    day = time.strftime("%Y-%m-%d")
    d, n = AI_DAY.get(uid, (day, 0))
    if d != day:
        n = 0
    if n >= AI_PER_DAY:
        return f"Bugungi limit tugadi ({AI_PER_DAY} ta tekshiruv). Ertaga yana urinib koʻring."
    AI_DAY[uid] = (day, n + 1)
    AI_LAST[uid] = now
    return None


def send_long(chat_id, text, markup=None):
    parts, cur = [], ""
    for para in text.split("\n"):
        if len(cur) + len(para) + 1 > 3800:
            parts.append(cur)
            cur = ""
        cur += para + "\n"
    parts.append(cur)
    for i, p in enumerate([x for x in parts if x.strip()]):
        send(chat_id, p.strip(), markup if i == len(parts) - 1 else None)


def ai_check(uid, chat_id, text):
    words = len(text.split())
    if words < AI_MIN_WORDS:
        send(chat_id, f"Esse juda qisqa ({words} soʻz). Kamida {AI_MIN_WORDS} soʻz yozing, tavsiya — 100 soʻz va undan koʻp.")
        return
    if len(text) > 6000:
        send(chat_id, "Esse juda uzun. 6000 belgigacha yuboring (taxminan 800 soʻz).")
        return
    msg_ = ai_allowed(uid)
    if msg_:
        send(chat_id, msg_)
        return
    send(chat_id, f"⏳ Esseingiz ({words} soʻz) tekshirilyapti, bu 5–15 soniya oladi…")
    out, err = groq_review(text)
    if err == "nokey":
        AIST.pop(uid, None)
        send(chat_id, "AI tekshiruvi hali sozlanmagan. Admin Groq kalitini qoʻshgach ishlaydi.", main_kb())
        notify_admins("⚠️ AI tekshiruvi ishlamadi: Groq kaliti topilmadi (groq_key.txt yoki GROQ_API_KEY).")
        return
    if err:
        AI_DAY[uid] = (time.strftime("%Y-%m-%d"), max(0, AI_DAY.get(uid, ("", 1))[1] - 1))
        msgs = {"badkey": "AI xizmati kaliti notoʻgʻri. Admin bilan bogʻlaning.",
                "limit": "AI xizmati hozir band (limit). Bir daqiqadan keyin qayta yuboring."}
        send(chat_id, msgs.get(err, "AI javob bera olmadi. Birozdan keyin qayta urinib koʻring."))
        if err in ("badkey",) or err.startswith("http"):
            notify_admins(f"⚠️ Groq xatosi: {err}")
        return
    AIST.pop(uid, None)
    send_long(chat_id, "🤖 AI ekspert xulosasi\n\n" + out)
    send(chat_id, "Yana esse yuborish uchun «" + B_AI + "» ni bosing. Saytdagi tekshiruv bilan solishtirib koʻring 😉", main_kb())


# ------------------------------------------------------------------ Yozma test (javobni oʻzingiz yozasiz)
WTESTS = json.loads(r'''[{"k": "Imlo", "q": "Soʻzni toʻgʻri yozing: «xozir»", "a": ["hozir"], "e": "«hozir» — h harfi bilan yoziladi."}, {"k": "Imlo", "q": "Soʻzni toʻgʻri yozing: «dexqon»", "a": ["dehqon"], "e": "«dehqon» — h bilan: dehqon."}, {"k": "Imlo", "q": "Soʻzni toʻgʻri yozing: «maxalla»", "a": ["mahalla"], "e": "«mahalla» — h bilan yoziladi."}, {"k": "Imlo", "q": "Soʻzni toʻgʻri yozing: «taxlil»", "a": ["tahlil"], "e": "«tahlil» — arabcha oʻzlashma, h bilan."}, {"k": "Imlo", "q": "Soʻzni toʻgʻri yozing: «saxifa»", "a": ["sahifa"], "e": "«sahifa» — h bilan yoziladi."}, {"k": "Imlo", "q": "Soʻzni toʻgʻri yozing: «extiyoj»", "a": ["ehtiyoj"], "e": "«ehtiyoj» — h bilan: ehtiyoj."}, {"k": "Imlo", "q": "Soʻzni toʻgʻri yozing: «mexmon»", "a": ["mehmon"], "e": "«mehmon» — h bilan yoziladi."}, {"k": "Imlo", "q": "Soʻzni toʻgʻri yozing: «shaxar»", "a": ["shahar"], "e": "«shahar» — h bilan yoziladi."}, {"k": "Imlo", "q": "Soʻzni toʻgʻri yozing: «ruxiyat»", "a": ["ruhiyat"], "e": "«ruhiyat» — h bilan yoziladi."}, {"k": "Imlo", "q": "Soʻzni toʻgʻri yozing: «axamiyat»", "a": ["ahamiyat"], "e": "«ahamiyat» — h bilan yoziladi."}, {"k": "Imlo", "q": "Soʻzni toʻgʻri yozing: «halq»", "a": ["xalq"], "e": "«xalq» — x bilan yoziladi."}, {"k": "Imlo", "q": "Soʻzni toʻgʻri yozing: «tarih»", "a": ["tarix"], "e": "«tarix» — x bilan yoziladi."}, {"k": "Imlo", "q": "Soʻzni toʻgʻri yozing: «ahloq»", "a": ["axloq"], "e": "«axloq» — x bilan yoziladi."}, {"k": "Imlo", "q": "Soʻzni toʻgʻri yozing: «xaqiqat»", "a": ["haqiqat"], "e": "«haqiqat» — h bilan yoziladi."}, {"k": "Imlo", "q": "Soʻzni toʻgʻri yozing: «xamma»", "a": ["hamma"], "e": "«hamma» — h bilan yoziladi."}, {"k": "Imlo", "q": "Soʻzni toʻgʻri yozing: «xayot»", "a": ["hayot"], "e": "«hayot» — h bilan yoziladi."}, {"k": "Imlo", "q": "Soʻzni toʻgʻri yozing: «xalol»", "a": ["halol"], "e": "«halol» — h bilan yoziladi."}, {"k": "Imlo", "q": "Soʻzni toʻgʻri yozing: «xurmat»", "a": ["hurmat"], "e": "«hurmat» — h bilan yoziladi."}, {"k": "Imlo", "q": "Soʻzni toʻgʻri yozing: «hazina»", "a": ["xazina"], "e": "«xazina» — x bilan yoziladi."}, {"k": "Imlo", "q": "Soʻzni toʻgʻri yozing: «hotira»", "a": ["xotira"], "e": "«xotira» — x bilan yoziladi."}, {"k": "Gapdagi xato", "q": "Gapdagi xatoli soʻzni toping va toʻgʻri yozing:\\n«Biz xar kuni kutubxonaga boramiz.»", "a": ["har", "har"], "e": "«har» — h bilan yoziladi."}, {"k": "Gapdagi xato", "q": "Gapdagi xatoli soʻzni toping va toʻgʻri yozing:\\n«Mening opam shaxarda yashaydi.»", "a": ["shaharda", "shaharda"], "e": "«shahar» — h bilan: shaharda."}, {"k": "Gapdagi xato", "q": "Gapdagi xatoli soʻzni toping va toʻgʻri yozing:\\n«Xamma vaqtida halol boʻlish kerak.»", "a": ["hamma", "hamma"], "e": "«hamma» — h bilan."}, {"k": "Gapdagi xato", "q": "Gapdagi xatoli soʻzni toping va toʻgʻri yozing:\\n«Oʻzbek halqi mehmondoʻst.»", "a": ["xalqi", "xalqi"], "e": "«xalq» — x bilan: xalqi."}, {"k": "Gapdagi xato", "q": "Gapdagi xatoli soʻzni toping va toʻgʻri yozing:\\n«Bu kitob menga juda foydali boʻldi, lekin undagi tarih qisqa.»", "a": ["tarix", "tarix"], "e": "«tarix» — x bilan yoziladi."}, {"k": "Gapdagi xato", "q": "Gapdagi xatoli soʻzni toping va toʻgʻri yozing:\\n«Ona tilimiz xayotimizning ajralmas qismi.»", "a": ["hayotimizning", "hayotimizning"], "e": "«hayot» — h bilan: hayotimizning."}, {"k": "Qoʻshimcha", "q": "«shahar» soʻziga tushum kelishigi qoʻshimchasini qoʻshing.", "a": ["shaharni"], "e": "Tushum kelishigi: -ni."}, {"k": "Qoʻshimcha", "q": "«bola» soʻziga qaratqich kelishigi qoʻshimchasini qoʻshing.", "a": ["bolaning"], "e": "Qaratqich kelishigi: -ning."}, {"k": "Qoʻshimcha", "q": "«maktab» soʻziga joʻnalish kelishigi qoʻshimchasini qoʻshing.", "a": ["maktabga"], "e": "Joʻnalish kelishigi: -ga."}, {"k": "Qoʻshimcha", "q": "«qalam» soʻziga chiqish kelishigi qoʻshimchasini qoʻshing.", "a": ["qalamdan"], "e": "Chiqish kelishigi: -dan."}, {"k": "Qoʻshimcha", "q": "«kitob» soʻziga oʻrin-payt kelishigi qoʻshimchasini qoʻshing.", "a": ["kitobda"], "e": "Oʻrin-payt kelishigi: -da."}, {"k": "Qoʻshimcha", "q": "«men» olmoshini qaratqich kelishigida yozing.", "a": ["mening"], "e": "men → mening."}, {"k": "Qoʻshimcha", "q": "«u» olmoshini tushum kelishigida yozing.", "a": ["uni"], "e": "u → uni."}, {"k": "Qoʻshimcha", "q": "«sen» olmoshini joʻnalish kelishigida yozing.", "a": ["senga"], "e": "sen → senga."}, {"k": "Qoʻshimcha", "q": "«biz» olmoshini qaratqich kelishigida yozing.", "a": ["bizning"], "e": "biz → bizning."}, {"k": "Qoʻshimcha", "q": "«ona» soʻzini 1-shaxs egalik shaklida (mening ...) yozing.", "a": ["onam"], "e": "1-shaxs birlik egalik: -(i)m: onam."}, {"k": "Qoʻshimcha", "q": "«kitob» soʻzini 2-shaxs egalik shaklida (sening ...) yozing.", "a": ["kitobing"], "e": "2-shaxs birlik egalik: -ing."}, {"k": "Qoʻshimcha", "q": "«uy» soʻzini 3-shaxs egalik shaklida (uning ...) yozing.", "a": ["uyi"], "e": "3-shaxs egalik: -i."}, {"k": "Qoʻshimcha", "q": "«daftar» soʻzini koʻplik shaklida yozing.", "a": ["daftarlar"], "e": "Koʻplik: -lar."}, {"k": "Qoʻshimcha", "q": "«bola» soʻzini koʻplik va 1-shaxs egalik shaklida (mening ...) yozing.", "a": ["bolalarim"], "e": "bola + lar + im = bolalarim."}, {"k": "Antonim va sinonim", "q": "«keng» soʻzining antonimini yozing.", "a": ["tor"], "e": "keng — tor."}, {"k": "Antonim va sinonim", "q": "«yaxshi» soʻzining antonimini yozing.", "a": ["yomon"], "e": "yaxshi — yomon."}, {"k": "Antonim va sinonim", "q": "«katta» soʻzining antonimini yozing.", "a": ["kichik"], "e": "katta — kichik."}, {"k": "Antonim va sinonim", "q": "«baland» soʻzining antonimini yozing.", "a": ["past"], "e": "baland — past."}, {"k": "Antonim va sinonim", "q": "«doʻst» soʻzining antonimini yozing.", "a": ["dushman"], "e": "doʻst — dushman."}, {"k": "Antonim va sinonim", "q": "«haqiqat» soʻzining antonimini yozing.", "a": ["yolgʻon", "yolgʻonchilik"], "e": "haqiqat — yolgʻon."}, {"k": "Antonim va sinonim", "q": "«sovuq» soʻzining antonimini yozing.", "a": ["issiq"], "e": "sovuq — issiq."}, {"k": "Antonim va sinonim", "q": "«qoʻrqoq» soʻzining antonimini yozing.", "a": ["jasur", "botir", "qoʻrqmas"], "e": "qoʻrqoq — jasur."}, {"k": "Antonim va sinonim", "q": "«saxiy» soʻzining antonimini yozing.", "a": ["xasis", "baxil", "qizgʻanchoq"], "e": "saxiy — xasis."}, {"k": "Antonim va sinonim", "q": "«mehnatsevar» soʻzining antonimini yozing.", "a": ["dangasa", "ishyoqmas"], "e": "mehnatsevar — dangasa."}, {"k": "Antonim va sinonim", "q": "«goʻzal» soʻzining sinonimini yozing (bitta).", "a": ["chiroyli", "suluv", "nafis"], "e": "goʻzal — chiroyli."}, {"k": "Antonim va sinonim", "q": "«bilim» soʻzining sinonimini yozing (bitta).", "a": ["ilm"], "e": "bilim — ilm."}, {"k": "Antonim va sinonim", "q": "«vatan» soʻzining sinonimini yozing (bitta).", "a": ["yurt", "diyor", "ona yurt", "ona vatan"], "e": "vatan — yurt."}, {"k": "Antonim va sinonim", "q": "«shod» soʻzining sinonimini yozing (bitta).", "a": ["xursand", "mamnun", "quvnoq"], "e": "shod — xursand."}, {"k": "Atama", "q": "Harakat yoki holatni bildirib, nima qildi? soʻrogʻiga javob boʻladigan soʻz turkumi nima?", "a": ["fel"], "e": "Fel — harakat-holat bildiruvchi soʻz turkumi."}, {"k": "Atama", "q": "Predmetni bildirib, kim? nima? soʻroqlariga javob boʻladigan soʻz turkumi nima?", "a": ["ot"], "e": "Ot — predmet bildiradi."}, {"k": "Atama", "q": "Predmetning belgisini bildirib, qanday? soʻrogʻiga javob boʻladigan soʻz turkumi nima?", "a": ["sifat"], "e": "Sifat — belgi bildiradi."}, {"k": "Atama", "q": "Predmetning sanogʻini bildirib, nechta? soʻrogʻiga javob boʻladigan soʻz turkumi nima?", "a": ["son"], "e": "Son — miqdor va tartib bildiradi."}, {"k": "Atama", "q": "Ot, sifat yoki son oʻrnida qoʻllanadigan soʻz turkumi nima?", "a": ["olmosh"], "e": "Olmosh — shu turkumlar oʻrnida keladi."}, {"k": "Atama", "q": "Gapda «kim? nima?» soʻrogʻiga javob boʻlib, harakat egasini bildiruvchi boʻlak nima?", "a": ["ega"], "e": "Ega — gapning bosh boʻlagi."}, {"k": "Atama", "q": "Gapda ega haqida axborot beruvchi bosh boʻlak nima?", "a": ["kesim"], "e": "Kesim — gapning bosh boʻlagi."}, {"k": "Atama", "q": "Soʻz, gap boʻlaklarini yoki gaplarni bogʻlovchi yordamchi soʻz turkumi nima?", "a": ["bogʻlovchi", "boglovchi"], "e": "Bogʻlovchi — va, ammo, lekin kabilar."}, {"k": "Atama", "q": "Shakli bir xil, maʼnosi har xil soʻzlar (masalan, «qoʻy» — hayvon va feʼl) nima deyiladi?", "a": ["omonim", "omonimlar"], "e": "Shakldosh soʻzlar — omonimlar."}, {"k": "Atama", "q": "Maʼnosi yaqin soʻzlar nima deyiladi?", "a": ["sinonim", "sinonimlar"], "e": "Maʼnodosh soʻzlar — sinonimlar."}, {"k": "Atama", "q": "Soʻzning maʼnoli eng kichik boʻlagi nima?", "a": ["morfema"], "e": "Morfema — maʼnoli eng kichik boʻlak."}, {"k": "Atama", "q": "Gap boʻlaklarining toʻliq ifodalanishi uchun kelgan, ega va kesimdan boshqa boʻlaklar umumiy nomi? (ikkinchi darajali ...)", "a": ["boʻlaklar", "bolaklar", "ikkinchi darajali boʻlaklar"], "e": "Ikkinchi darajali boʻlaklar: aniqlovchi, toʻldiruvchi, holat."}, {"k": "Tinish belgilari", "q": "«Men oʻqiyman lekin u yozadi.» Gapda nechta vergul kerak? (raqam bilan)", "a": ["1"], "e": "«lekin» dan oldin vergul qoʻyiladi: 1 ta."}, {"k": "Tinish belgilari", "q": "«Kitob daftar qalam va ruchka stolda edi.» Gapda nechta vergul kerak? (raqam bilan)", "a": ["2"], "e": "Uyushiq boʻlaklar: Kitob, daftar, qalam va ruchka — 2 ta."}, {"k": "Tinish belgilari", "q": "«Hamma xursand edi chunki imtihon yaxshi oʻtdi.» Gapda nechta vergul kerak? (raqam bilan)", "a": ["1"], "e": "«chunki» dan oldin vergul: 1 ta."}, {"k": "Imlo", "q": "Soʻzni toʻgʻri yozing: «qutubxona»", "a": ["kutubxona"], "e": "«kutubxona» — k bilan: kitob + xona."}, {"k": "Imlo", "q": "Soʻzni toʻgʻri yozing: «imtixon»", "a": ["imtihon"], "e": "«imtihon» — h bilan yoziladi."}, {"k": "Imlo", "q": "Soʻzni toʻgʻri yozing: «ehtiyod»", "a": ["ehtiyot"], "e": "«ehtiyot» — oxiri t bilan."}, {"k": "Imlo", "q": "Soʻzni toʻgʻri yozing: «mexnat»", "a": ["mehnat"], "e": "«mehnat» — h bilan yoziladi."}, {"k": "Imlo", "q": "Soʻzni toʻgʻri yozing: «ijtimoy»", "a": ["ijtimoiy"], "e": "«ijtimoiy» — -iy qoʻshimchasi bilan."}, {"k": "Imlo", "q": "Soʻzni toʻgʻri yozing: «madaniyyat»", "a": ["madaniyat"], "e": "«madaniyat» — bitta y bilan."}, {"k": "Imlo", "q": "Soʻzni toʻgʻri yozing: «tabiyat»", "a": ["tabiat"], "e": "«tabiat» — i dan keyin y yoʻq."}, {"k": "Imlo", "q": "Soʻzni toʻgʻri yozing: «mustaqilik»", "a": ["mustaqillik"], "e": "«mustaqillik» — ikkita l: mustaqil + lik."}, {"k": "Imlo", "q": "Soʻzni toʻgʻri yozing: «iqtisodyot»", "a": ["iqtisodiyot"], "e": "«iqtisodiyot» — -iyot qoʻshimchasi."}, {"k": "Imlo", "q": "Soʻzni toʻgʻri yozing: «sanat»", "a": ["sanʼat"], "e": "«sanʼat» — tutuq belgisi bilan: sanʼat."}, {"k": "Imlo", "q": "Soʻzni toʻgʻri yozing: «tarbiyya»", "a": ["tarbiya"], "e": "«tarbiya» — bitta y."}, {"k": "Imlo", "q": "Soʻzni toʻgʻri yozing: «taxsil»", "a": ["tahsil"], "e": "«tahsil» — h bilan."}, {"k": "Imlo", "q": "Soʻzni toʻgʻri yozing: «soxil»", "a": ["sohil"], "e": "«sohil» — h bilan."}, {"k": "Imlo", "q": "Soʻzni toʻgʻri yozing: «mutaxasis»", "a": ["mutaxassis"], "e": "«mutaxassis» — ikkita s."}, {"k": "Imlo", "q": "Soʻzni toʻgʻri yozing: «jurat»", "a": ["jurʼat"], "e": "«jurʼat» — tutuq belgisi bilan."}, {"k": "Gapdagi xato", "q": "Gapdagi xatoli soʻzni toping va toʻgʻri yozing:\\n«Qutubxonada kitoblar koʻp.»", "a": ["kutubxonada"], "e": "«kutubxona» — k bilan."}, {"k": "Gapdagi xato", "q": "Gapdagi xatoli soʻzni toping va toʻgʻri yozing:\\n«Bugun imtixon boʻladi.»", "a": ["imtihon"], "e": "«imtihon» — h bilan."}, {"k": "Gapdagi xato", "q": "Gapdagi xatoli soʻzni toping va toʻgʻri yozing:\\n«Ota-onamning mexnati behisob.»", "a": ["mehnati"], "e": "«mehnat» — h bilan."}, {"k": "Gapdagi xato", "q": "Gapdagi xatoli soʻzni toping va toʻgʻri yozing:\\n«U yaxshi mutaxasis boʻldi.»", "a": ["mutaxassis"], "e": "«mutaxassis» — ikkita s."}, {"k": "Gapdagi xato", "q": "Gapdagi xatoli soʻzni toping va toʻgʻri yozing:\\n«Bizning mamlakat boy tabiyatga ega.»", "a": ["tabiatga"], "e": "«tabiat» — y yoʻq."}, {"k": "Gapdagi xato", "q": "Gapdagi xatoli soʻzni toping va toʻgʻri yozing:\\n«Mustaqilik bayrami keldi.»", "a": ["mustaqillik"], "e": "«mustaqillik» — ikkita l."}, {"k": "Gapdagi xato", "q": "Gapdagi xatoli soʻzni toping va toʻgʻri yozing:\\n«Ijtimoy hayot oʻzgarmoqda.»", "a": ["ijtimoiy"], "e": "«ijtimoiy» — -iy bilan."}, {"k": "Gapdagi xato", "q": "Gapdagi xatoli soʻzni toping va toʻgʻri yozing:\\n«Madaniyyatimiz boy.»", "a": ["madaniyatimiz"], "e": "«madaniyat» — bitta y."}, {"k": "Gapdagi xato", "q": "Gapdagi xatoli soʻzni toping va toʻgʻri yozing:\\n«Men xayotdan mamnunman.»", "a": ["hayotdan"], "e": "«hayot» — h bilan."}, {"k": "Qoʻshimcha", "q": "«kitob» soʻziga tushum kelishigi qoʻshimchasini qoʻshing.", "a": ["kitobni"], "e": "Tushum kelishigi: -ni"}, {"k": "Qoʻshimcha", "q": "«qalam» soʻziga joʻnalish kelishigi qoʻshimchasini qoʻshing.", "a": ["qalamga"], "e": "Joʻnalish kelishigi: -ga"}, {"k": "Qoʻshimcha", "q": "«uy» soʻziga oʻrin-payt kelishigi qoʻshimchasini qoʻshing.", "a": ["uyda"], "e": "Oʻrin-payt kelishigi: -da"}, {"k": "Qoʻshimcha", "q": "«daryo» soʻziga chiqish kelishigi qoʻshimchasini qoʻshing.", "a": ["daryodan"], "e": "Chiqish kelishigi: -dan"}, {"k": "Qoʻshimcha", "q": "«ona» soʻziga qaratqich kelishigi qoʻshimchasini qoʻshing.", "a": ["onaning"], "e": "Qaratqich kelishigi: -ning"}, {"k": "Qoʻshimcha", "q": "«maktab» soʻziga oʻrin-payt kelishigi qoʻshimchasini qoʻshing.", "a": ["maktabda"], "e": "Oʻrin-payt kelishigi: -da"}, {"k": "Qoʻshimcha", "q": "«shahar» soʻziga chiqish kelishigi qoʻshimchasini qoʻshing.", "a": ["shahardan"], "e": "Chiqish kelishigi: -dan"}, {"k": "Qoʻshimcha", "q": "«tok» soʻziga joʻnalish kelishigi qoʻshimchasini qoʻshing.", "a": ["tokka"], "e": "Joʻnalish kelishigi: k dan keyin -ka: tokka"}, {"k": "Qoʻshimcha", "q": "«ariq» soʻziga joʻnalish kelishigi qoʻshimchasini qoʻshing.", "a": ["ariqqa"], "e": "Joʻnalish kelishigi: q dan keyin -qa: ariqqa"}, {"k": "Qoʻshimcha", "q": "«qishloq» soʻziga joʻnalish kelishigi qoʻshimchasini qoʻshing.", "a": ["qishloqqa"], "e": "Joʻnalish kelishigi: q dan keyin -qa."}, {"k": "Qoʻshimcha", "q": "«bola» soʻziga koʻplik qoʻshimchasi qoʻshimchasini qoʻshing.", "a": ["bolalar"], "e": "Koʻplik qoʻshimchasi: -lar"}, {"k": "Qoʻshimcha", "q": "«oʻquvchi» soʻziga koʻplik qoʻshimchasi qoʻshimchasini qoʻshing.", "a": ["oʻquvchilar"], "e": "Koʻplik qoʻshimchasi: -lar"}, {"k": "Qoʻshimcha", "q": "«kitob» soʻziga 1-shaxs birlik egalik qoʻshimchasini qoʻshing (mening ...).", "a": ["kitobim"], "e": "-im: kitobim."}, {"k": "Qoʻshimcha", "q": "«ona» soʻziga 3-shaxs egalik qoʻshimchasini qoʻshing (uning ...).", "a": ["onasi"], "e": "Unli bilan tugasa -si: onasi."}, {"k": "Qoʻshimcha", "q": "«qalam» soʻziga 2-shaxs birlik egalik qoʻshimchasini qoʻshing (sening ...).", "a": ["qalaming"], "e": "-ing: qalaming."}, {"k": "Qoʻshimcha", "q": "«maktab» soʻzini koʻplikda, keyin chiqish kelishigida yozing.", "a": ["maktablardan"], "e": "Tartib: koʻplik + kelishik: maktab-lar-dan."}, {"k": "Qoʻshimcha", "q": "«kitob» soʻzini koʻplik, 1-shaxs egalik va tushum kelishigida yozing.", "a": ["kitoblarimni"], "e": "Tartib: koʻplik + egalik + kelishik: kitob-lar-im-ni."}, {"k": "Qoʻshimcha", "q": "«doʻst» soʻziga 1-shaxs koʻplik egalik qoʻshimchasini qoʻshing (bizning ...).", "a": ["doʻstimiz"], "e": "-imiz: doʻstimiz."}, {"k": "Soʻz yasalishi", "q": "«kitob» soʻziga «-xon» qoʻshimchasini qoʻshib, yangi soʻz yasang.", "a": ["kitobxon"], "e": "kitob + xon = kitobxon (ot)."}, {"k": "Soʻz yasalishi", "q": "«ish» soʻziga «-chi» qoʻshimchasini qoʻshib, yangi soʻz yasang.", "a": ["ishchi"], "e": "ish + chi = ishchi (kasb)."}, {"k": "Soʻz yasalishi", "q": "«gul» soʻziga «-zor» qoʻshimchasini qoʻshib, yangi soʻz yasang.", "a": ["gulzor"], "e": "gul + zor = gulzor (oʻrin-joy)."}, {"k": "Soʻz yasalishi", "q": "«aql» soʻziga «-li» qoʻshimchasini qoʻshib, yangi soʻz yasang.", "a": ["aqlli"], "e": "aql + li = aqlli (sifat)."}, {"k": "Soʻz yasalishi", "q": "«bilim» soʻziga «-siz» qoʻshimchasini qoʻshib, yangi soʻz yasang.", "a": ["bilimsiz"], "e": "bilim + siz = bilimsiz (sifat)."}, {"k": "Soʻz yasalishi", "q": "«vatan» soʻziga «-parvar» qoʻshimchasini qoʻshib, yangi soʻz yasang.", "a": ["vatanparvar"], "e": "vatan + parvar = vatanparvar."}, {"k": "Soʻz yasalishi", "q": "«tinch» soʻziga «-lik» qoʻshimchasini qoʻshib, yangi soʻz yasang.", "a": ["tinchlik"], "e": "tinch + lik = tinchlik (ot)."}, {"k": "Soʻz yasalishi", "q": "«mehnat» soʻziga «-kash» qoʻshimchasini qoʻshib, yangi soʻz yasang.", "a": ["mehnatkash"], "e": "mehnat + kash = mehnatkash."}, {"k": "Soʻz yasalishi", "q": "«ilm» soʻziga «-iy» qoʻshimchasini qoʻshib, yangi soʻz yasang.", "a": ["ilmiy"], "e": "ilm + iy = ilmiy (sifat)."}, {"k": "Soʻz yasalishi", "q": "«ish» soʻziga «-la» qoʻshimchasini qoʻshib, yangi soʻz yasang.", "a": ["ishla"], "e": "ish + la = ishla (feʼl)."}, {"k": "Soʻz yasalishi", "q": "«kitob» soʻziga «-xona» qoʻshimchasini qoʻshib, yangi soʻz yasang.", "a": ["kitobxona"], "e": "kitob + xona = kitobxona (ot)."}, {"k": "Soʻz turkumi", "q": "«Anvar kitob oʻqidi.» gapida «kitob» qaysi turkum? (bitta soʻz)", "a": ["ot", "ot", "ot"], "e": "Kitob — predmet nomi: ot."}, {"k": "Soʻz turkumi", "q": "«Chiroyli gul ochildi.» gapida «chiroyli» qaysi turkum?", "a": ["sifat", "sifat", "sifat"], "e": "Chiroyli — belgi bildiradi: sifat."}, {"k": "Soʻz turkumi", "q": "«U tez yuguradi.» gapida «tez» qaysi turkum?", "a": ["ravish", "ravish", "ravish"], "e": "Tez — harakat belgisi: ravish."}, {"k": "Soʻz turkumi", "q": "«Ular bugun keldi.» gapida «ular» qaysi turkum?", "a": ["olmosh", "olmosh", "olmosh"], "e": "Ular — kishilik olmoshi."}, {"k": "Soʻz turkumi", "q": "«Beshta olma» birikmasida «beshta» qaysi turkum?", "a": ["son", "son", "son"], "e": "Beshta — dona son."}, {"k": "Soʻz turkumi", "q": "«Qalam bilan yozdi.» gapida «bilan» qaysi turkum?", "a": ["koʻmakchi", "koʻmakchi", "koʻmakchi"], "e": "Bilan — koʻmakchi."}, {"k": "Soʻz turkumi", "q": "«Men keldim, lekin u yoʻq edi.» gapida «lekin» qaysi turkum?", "a": ["bogʻlovchi", "bogʻlovchi", "bogʻlovchi"], "e": "Lekin — zidlovchi bogʻlovchi."}, {"k": "Soʻz turkumi", "q": "«Faqat sen keldingmi?» gapida «faqat» qaysi turkum?", "a": ["yuklama", "yuklama", "yuklama"], "e": "Faqat — chegaralash yuklamasi."}, {"k": "Soʻz turkumi", "q": "«Oh, qanday goʻzal!» gapida «oh» qaysi turkum?", "a": ["undov", "undov", "undov"], "e": "Oh — undov soʻz."}, {"k": "Soʻz turkumi", "q": "«Albatta, boraman.» gapida «albatta» qaysi turkum?", "a": ["modal", "modal", "modal"], "e": "Albatta — modal soʻz (ishonch)."}, {"k": "Soʻz turkumi", "q": "«Shitir-shitir» soʻzi qaysi turkum?", "a": ["taqlid", "taqlid", "taqlid"], "e": "Taqlid soʻz (tovushga)."}, {"k": "Soʻz turkumi", "q": "«Yozmoq» soʻzi qaysi turkum?", "a": ["feʼl", "fe'l", "feʼl"], "e": "Harakat bildiradi: feʼl."}, {"k": "Feʼl shakllari", "q": "«yozdirdi» feʼli qaysi nisbatda? (bitta soʻz: aniq, oʻzlik, majhul, birgalik, orttirma)", "a": ["orttirma", "orttirma"], "e": "-dir — orttirma nisbat."}, {"k": "Feʼl shakllari", "q": "«yuvindi» feʼli qaysi nisbatda?", "a": ["oʻzlik", "oʻzlik"], "e": "-in — oʻzlik nisbat."}, {"k": "Feʼl shakllari", "q": "«yozildi» feʼli qaysi nisbatda?", "a": ["majhul", "majhul"], "e": "-il — majhul nisbat."}, {"k": "Feʼl shakllari", "q": "«yozishdi» feʼli qaysi nisbatda?", "a": ["birgalik", "birgalik"], "e": "-ish — birgalik nisbat."}, {"k": "Feʼl shakllari", "q": "«oʻqigan» shakli feʼlning qaysi shakli? (sifatdosh, ravishdosh, harakat nomi)", "a": ["sifatdosh", "sifatdosh"], "e": "-gan — sifatdosh."}, {"k": "Feʼl shakllari", "q": "«oʻqib» shakli feʼlning qaysi shakli? (sifatdosh, ravishdosh, harakat nomi)", "a": ["ravishdosh", "ravishdosh"], "e": "-ib — ravishdosh."}, {"k": "Feʼl shakllari", "q": "«oʻqish» shakli feʼlning qaysi shakli? (sifatdosh, ravishdosh, harakat nomi)", "a": ["harakat nomi", "harakat nomi"], "e": "-ish — harakat nomi."}, {"k": "Feʼl shakllari", "q": "«Kel!» feʼli qaysi maylda? (aniqlik, buyruq-istak, shart)", "a": ["buyruq-istak", "buyruq-istak"], "e": "Buyruq mayli."}, {"k": "Feʼl shakllari", "q": "«Kelsa» feʼli qaysi maylda? (aniqlik, buyruq-istak, shart)", "a": ["shart", "shart"], "e": "-sa — shart mayli."}, {"k": "Olmosh turlari", "q": "«kimdir» olmoshi qaysi turga kiradi? (kishilik, koʻrsatish, soʻroq, belgilash, oʻzlik, gumon, inkor)", "a": ["gumon", "gumon", "gumon"], "e": "Gumon olmoshi."}, {"k": "Olmosh turlari", "q": "«hech kim» olmoshi qaysi turga kiradi?", "a": ["inkor", "inkor", "boʻlishsizlik"], "e": "Boʻlishsizlik (inkor) olmoshi."}, {"k": "Olmosh turlari", "q": "«har kim» olmoshi qaysi turga kiradi?", "a": ["belgilash", "belgilash-jamlash", "belgilash"], "e": "Belgilash-jamlash olmoshi."}, {"k": "Olmosh turlari", "q": "«oʻzim» olmoshi qaysi turga kiradi?", "a": ["oʻzlik", "oʻzlik", "oʻzlik"], "e": "Oʻzlik olmoshi."}, {"k": "Olmosh turlari", "q": "«qaysi» olmoshi qaysi turga kiradi?", "a": ["soʻroq", "soʻroq", "soʻroq"], "e": "Soʻroq olmoshi."}, {"k": "Olmosh turlari", "q": "«shu» olmoshi qaysi turga kiradi?", "a": ["koʻrsatish", "koʻrsatish", "koʻrsatish"], "e": "Koʻrsatish olmoshi."}, {"k": "Olmosh turlari", "q": "«biz» olmoshi qaysi turga kiradi?", "a": ["kishilik", "kishilik", "kishilik"], "e": "Kishilik olmoshi."}, {"k": "Boʻgʻin", "q": "«maktab» soʻzida nechta boʻgʻin bor? (raqam bilan)", "a": ["2"], "e": "Boʻgʻinlar soni unlilar soniga teng: 2 ta unli — 2 boʻgʻin."}, {"k": "Boʻgʻin", "q": "«kitob» soʻzida nechta boʻgʻin bor? (raqam bilan)", "a": ["2"], "e": "Boʻgʻinlar soni unlilar soniga teng: 2 ta unli — 2 boʻgʻin."}, {"k": "Boʻgʻin", "q": "«oʻqituvchi» soʻzida nechta boʻgʻin bor? (raqam bilan)", "a": ["4"], "e": "Boʻgʻinlar soni unlilar soniga teng: 4 ta unli — 4 boʻgʻin."}, {"k": "Boʻgʻin", "q": "«Oʻzbekiston» soʻzida nechta boʻgʻin bor? (raqam bilan)", "a": ["4"], "e": "Boʻgʻinlar soni unlilar soniga teng: 4 ta unli — 4 boʻgʻin."}, {"k": "Boʻgʻin", "q": "«daryo» soʻzida nechta boʻgʻin bor? (raqam bilan)", "a": ["2"], "e": "Boʻgʻinlar soni unlilar soniga teng: 2 ta unli — 2 boʻgʻin."}, {"k": "Boʻgʻin", "q": "«mustaqillik» soʻzida nechta boʻgʻin bor? (raqam bilan)", "a": ["4"], "e": "Boʻgʻinlar soni unlilar soniga teng: 4 ta unli — 4 boʻgʻin."}, {"k": "Boʻgʻin", "q": "«ona» soʻzida nechta boʻgʻin bor? (raqam bilan)", "a": ["2"], "e": "Boʻgʻinlar soni unlilar soniga teng: 2 ta unli — 2 boʻgʻin."}, {"k": "Boʻgʻin", "q": "«tabiat» soʻzida nechta boʻgʻin bor? (raqam bilan)", "a": ["3"], "e": "Boʻgʻinlar soni unlilar soniga teng: 3 ta unli — 3 boʻgʻin."}, {"k": "Boʻgʻin", "q": "«hayot» soʻzida nechta boʻgʻin bor? (raqam bilan)", "a": ["2"], "e": "Boʻgʻinlar soni unlilar soniga teng: 2 ta unli — 2 boʻgʻin."}, {"k": "Boʻgʻin", "q": "«vatan» soʻzida nechta boʻgʻin bor? (raqam bilan)", "a": ["2"], "e": "Boʻgʻinlar soni unlilar soniga teng: 2 ta unli — 2 boʻgʻin."}, {"k": "Antonim va sinonim", "q": "«issiq» soʻzining antonimini yozing.", "a": ["sovuq"], "e": "issiq — sovuq."}, {"k": "Antonim va sinonim", "q": "«kecha» soʻzining antonimini yozing.", "a": ["kunduz"], "e": "kecha — kunduz."}, {"k": "Antonim va sinonim", "q": "«tez» soʻzining antonimini yozing.", "a": ["sekin"], "e": "tez — sekin."}, {"k": "Antonim va sinonim", "q": "«ochiq» soʻzining antonimini yozing.", "a": ["yopiq"], "e": "ochiq — yopiq."}, {"k": "Antonim va sinonim", "q": "«yangi» soʻzining antonimini yozing.", "a": ["eski"], "e": "yangi — eski."}, {"k": "Antonim va sinonim", "q": "«shirin» soʻzining antonimini yozing.", "a": ["achchiq"], "e": "shirin — achchiq."}, {"k": "Antonim va sinonim", "q": "«toza» soʻzining antonimini yozing.", "a": ["iflos"], "e": "toza — iflos."}, {"k": "Antonim va sinonim", "q": "«yaqin» soʻzining antonimini yozing.", "a": ["uzoq"], "e": "yaqin — uzoq."}, {"k": "Antonim va sinonim", "q": "«kuchli» soʻzining antonimini yozing.", "a": ["zaif"], "e": "kuchli — zaif."}, {"k": "Antonim va sinonim", "q": "«boy» soʻzining antonimini yozing.", "a": ["kambagʻal"], "e": "boy — kambagʻal."}, {"k": "Antonim va sinonim", "q": "«quvonch» soʻzining antonimini yozing.", "a": ["gʻam"], "e": "quvonch — gʻam."}, {"k": "Antonim va sinonim", "q": "«koʻp» soʻzining antonimini yozing.", "a": ["kam"], "e": "koʻp — kam."}, {"k": "Antonim va sinonim", "q": "«past» soʻzining antonimini yozing.", "a": ["baland"], "e": "past — baland."}, {"k": "Antonim va sinonim", "q": "«yosh» soʻzining antonimini yozing.", "a": ["qari"], "e": "yosh — qari."}, {"k": "Antonim va sinonim", "q": "«ertalab» soʻzining antonimini yozing.", "a": ["kechqurun"], "e": "ertalab — kechqurun."}, {"k": "Antonim va sinonim", "q": "«foyda» soʻzining antonimini yozing.", "a": ["zarar"], "e": "foyda — zarar."}, {"k": "Antonim va sinonim", "q": "«oson» soʻzining antonimini yozing.", "a": ["qiyin"], "e": "oson — qiyin."}, {"k": "Antonim va sinonim", "q": "«chiroyli» soʻzining sinonimini (maʼnodoshini) yozing.", "a": ["goʻzal", "kelishgan", "xushroʻy", "latofatli"], "e": "chiroyli — goʻzal."}, {"k": "Antonim va sinonim", "q": "«katta» soʻzining sinonimini (maʼnodoshini) yozing.", "a": ["ulkan", "yirik", "buyuk"], "e": "katta — yirik, ulkan."}, {"k": "Antonim va sinonim", "q": "«tez» soʻzining sinonimini (maʼnodoshini) yozing.", "a": ["chaqqon", "shoshilinch", "jadal"], "e": "tez — chaqqon, jadal."}, {"k": "Antonim va sinonim", "q": "«aqlli» soʻzining sinonimini (maʼnodoshini) yozing.", "a": ["dono", "zehnli", "farosatli", "oqil"], "e": "aqlli — dono, zehnli."}, {"k": "Antonim va sinonim", "q": "«mehnat» soʻzining sinonimini (maʼnodoshini) yozing.", "a": ["ish", "zahmat", "mashaqqat"], "e": "mehnat — zahmat, ish."}, {"k": "Atama va adabiyot", "q": "Qofiyadan keyin takrorlanuvchi soʻz yoki birikma nima deyiladi? (bitta soʻz)", "a": ["radif"], "e": "Radif."}, {"k": "Atama va adabiyot", "q": "Gʻazalning birinchi bayti nima deyiladi?", "a": ["matla", "matlaʼ", "matla'"], "e": "Matla — gʻazalning birinchi bayti."}, {"k": "Atama va adabiyot", "q": "Gʻazalning oxirgi bayti (shoir taxallusi bor) nima deyiladi?", "a": ["maqta", "maqtaʼ", "maqta'"], "e": "Maqta — oxirgi bayt."}, {"k": "Atama va adabiyot", "q": "Toʻrt misrali sheʼriy janr nima deyiladi?", "a": ["ruboiy"], "e": "Ruboiy — 4 misra."}, {"k": "Atama va adabiyot", "q": "Voqea-hodisani boʻrttirib tasvirlash nima deyiladi?", "a": ["mubolagʻa", "mubolaga"], "e": "Mubolagʻa."}, {"k": "Atama va adabiyot", "q": "Jonsiz narsani jonli qilib tasvirlash nima deyiladi?", "a": ["tashxis", "jonlantirish"], "e": "Tashxis (jonlantirish)."}, {"k": "Atama va adabiyot", "q": "Qarama-qarshi tushunchalarni yonma-yon qoʻyish nima deyiladi?", "a": ["tazod"], "e": "Tazod."}, {"k": "Atama va adabiyot", "q": "Badiiy aniqlovchi nima deyiladi?", "a": ["epitet", "sifatlash"], "e": "Epitet."}, {"k": "Atama va adabiyot", "q": "Oʻqishda ham, yozishda ham bir xil, maʼnosi har xil soʻzlar nima deyiladi?", "a": ["omonim", "omonimlar"], "e": "Omonim."}, {"k": "Atama va adabiyot", "q": "Maʼnosi qarama-qarshi soʻzlar nima deyiladi?", "a": ["antonim", "antonimlar", "zid maʼnoli", "qarama-qarshi"], "e": "Antonim."}, {"k": "Atama va adabiyot", "q": "Eskirgan, oʻrniga yangi soʻz kelgan soʻz nima deyiladi?", "a": ["arxaizm"], "e": "Arxaizm."}, {"k": "Atama va adabiyot", "q": "Predmeti yoʻqolgan tarixiy soʻz nima deyiladi?", "a": ["istorizm"], "e": "Istorizm."}, {"k": "Atama va adabiyot", "q": "Yangi paydo boʻlgan soʻz nima deyiladi?", "a": ["neologizm"], "e": "Neologizm."}, {"k": "Atama va adabiyot", "q": "«Boburnoma» muallifi kim? (familiyasi bilan)", "a": ["bobur", "zahiriddin bobur", "zahiriddin muhammad bobur"], "e": "Zahiriddin Muhammad Bobur."}, {"k": "Atama va adabiyot", "q": "«Oʻtgan kunlar» romani muallifi kim?", "a": ["qodiriy", "abdulla qodiriy"], "e": "Abdulla Qodiriy."}, {"k": "Atama va adabiyot", "q": "«Kecha va kunduz» romani muallifi kim?", "a": ["choʻlpon", "cholpon", "cho'lpon"], "e": "Choʻlpon."}, {"k": "Atama va adabiyot", "q": "«Sarob» romani muallifi kim?", "a": ["qahhor", "abdulla qahhor"], "e": "Abdulla Qahhor."}, {"k": "Atama va adabiyot", "q": "«Qutadgʻu bilig» muallifi kim?", "a": ["yusuf xos hojib", "xos hojib", "yusuf xoss hojib"], "e": "Yusuf Xos Hojib."}, {"k": "Atama va adabiyot", "q": "«Devonu lugʻotit turk» muallifi kim?", "a": ["mahmud koshgʻariy", "koshgʻariy", "mahmud qoshgʻariy"], "e": "Mahmud Koshgʻariy."}, {"k": "Atama va adabiyot", "q": "Navoiy «Xamsa»si nechta dostondan iborat? (raqam bilan)", "a": ["5", "besh"], "e": "Xamsa — 5 doston."}, {"k": "Atama va adabiyot", "q": "«Mehrobdan chayon» muallifi kim?", "a": ["qodiriy", "abdulla qodiriy"], "e": "Abdulla Qodiriy."}, {"k": "Tinish belgilari", "q": "«Bahor keldi va tabiat uygʻondi.» Gapda nechta vergul kerak? (raqam bilan)", "a": ["0"], "e": "«va» bogʻlovchisidan oldin vergul qoʻyilmaydi (qisqa gap)."}, {"k": "Tinish belgilari", "q": "«Olma nok uzum va anor pishdi.» Gapda nechta vergul kerak? (raqam bilan)", "a": ["2"], "e": "Uyushiq boʻlaklar: Olma, nok, uzum va anor — 2 ta."}, {"k": "Tinish belgilari", "q": "«Ali kel bu yoqqa.» Gapda nechta vergul kerak? (raqam bilan)", "a": ["1"], "e": "Undalmadan keyin vergul: Ali, kel bu yoqqa — 1 ta."}, {"k": "Tinish belgilari", "q": "«Albatta men kelaman.» Gapda nechta vergul kerak? (raqam bilan)", "a": ["1"], "e": "Kirish soʻzdan keyin vergul: 1 ta."}, {"k": "Tinish belgilari", "q": "«Agar yomgʻir yogʻsa uyda qolamiz.» Gapda nechta vergul kerak? (raqam bilan)", "a": ["1"], "e": "Ergash gapdan keyin vergul: 1 ta."}, {"k": "Tinish belgilari", "q": "«U charchagan edi ammo ishlashda davom etdi.» Gapda nechta vergul kerak? (raqam bilan)", "a": ["1"], "e": "«ammo» dan oldin vergul: 1 ta."}, {"k": "Tinish belgilari", "q": "«Kitob daftar qalam hammasi stolda.» Gapda nechta vergul kerak? (raqam bilan)", "a": ["2"], "e": "Uyushiq boʻlaklar: kitob, daftar, qalam — 2 ta (tire ham qoʻyiladi)."}, {"k": "Tinish belgilari", "q": "«Biz oʻqiymiz yozamiz va izlanamiz.» Gapda nechta vergul kerak? (raqam bilan)", "a": ["1"], "e": "Uyushiq: oʻqiymiz, yozamiz va izlanamiz — 1 ta."}, {"k": "Gap turlari", "q": "«Men ertaga kelaman», — dedi Ali. Bu qanday gap? (koʻchirma yoki oʻzlashtirma)", "a": ["koʻchirma", "kochirma", "ko'chirma"], "e": "Soʻz egasining gapi aynan keltirilgan: koʻchirma gap."}, {"k": "Gap turlari", "q": "«Ali ertaga kelishini aytdi.» Bu qanday gap? (koʻchirma yoki oʻzlashtirma)", "a": ["oʻzlashtirma", "ozlashtirma", "o'zlashtirma"], "e": "Oʻzlashtirma gap."}, {"k": "Gap turlari", "q": "«Havo sovuq, lekin biz chiqdik.» Bu qanday qoʻshma gap? (bogʻlangan, ergashgan, bogʻlovchisiz)", "a": ["bogʻlangan", "boglangan", "bog'langan"], "e": "Teng bogʻlovchi (lekin): bogʻlangan qoʻshma gap."}, {"k": "Gap turlari", "q": "«Agar kelsang, men ham boraman.» Bu qanday qoʻshma gap? (bogʻlangan, ergashgan, bogʻlovchisiz)", "a": ["ergashgan"], "e": "Ergash gapli qoʻshma gap."}, {"k": "Gap turlari", "q": "«Yoz keldi, kunlar isidi.» Bu qanday qoʻshma gap?", "a": ["bogʻlovchisiz", "boglovchisiz", "bog'lovchisiz"], "e": "Bogʻlovchisiz qoʻshma gap."}]''')
B_WR = "✍️ Yozma test"
WR_ALL = "🎲 Aralash (hamma turlar)"
WR_KINDS = []
for _q in WTESTS:
    if _q["k"] not in WR_KINDS:
        WR_KINDS.append(_q["k"])
WR_BTN = {f"📝 {k}": k for k in WR_KINDS}
WSTATE = {}      # {uid: yozma test holati}
WR_SKIP = "⏭ Oʻtkazib yuborish (savol)"
NAV_RESET = None


def wr_norm(s):
    s = str(s).lower().replace("ʻ", "'").replace("ʼ", "'").replace("’", "'").replace("‘", "'").replace("`", "'").replace("´", "'")
    s = " ".join(s.split()).strip().rstrip(".!?,;:")
    return s


def wr_ok(q, ans):
    v = wr_norm(ans)
    if not v:
        return False
    cands = [wr_norm(a) for a in q["a"]]
    if v in cands:
        return True
    if q["k"] not in ("Imlo", "Gapdagi xato", "Qoʻshimcha", "Soʻz yasalishi"):
        # atama/turkum javoblarida apostrof qoldirilsa ham qabul qilinadi (fel = feʼl)
        v2 = v.replace("'", "")
        return any(c.replace("'", "") == v2 for c in cands)
    return False


def wr_kb():
    rows = [[WR_ALL]] + [[t] for t in WR_BTN] + [[B_OTHER, B_MENU]]
    return rk(rows)


def wr_pool(kind):
    return [q for q in WTESTS if kind in (None, "all") or q["k"] == kind]


def start_wr(uid, chat_id, kind, n=None):
    pool = wr_pool(kind)
    random.shuffle(pool)
    n = min(n or 10, len(pool))
    STATE.pop(uid, None)
    WSTATE[uid] = {"list": pool[:n], "i": 0, "ok": 0, "log": [], "chat_id": chat_id,
                   "title": "Yozma test — " + (kind if kind not in (None, "all") else "aralash")}
    LAST[uid] = ("wr", kind)
    LAST_N[uid] = n
    send(chat_id, f"✍️ {WSTATE[uid]['title']}\n\n{n} ta savol. Javobni oʻzingiz yozasiz (apostrofni oddiy «'» bilan yozsangiz ham boʻladi). "
                  "Savolni oʻtkazish yoki testni toʻxtatish tugmalari pastda. Omad! 🍀",
         rk([[WR_SKIP], [B_STOP]]))
    wr_next(uid)


def wr_next(uid):
    st = WSTATE.get(uid)
    if not st:
        return
    if st["i"] >= len(st["list"]):
        wr_finish(uid)
        return
    q = st["list"][st["i"]]
    send(st["chat_id"], f"✍️ {st['i'] + 1}/{len(st['list'])} · {q['k']}\n\n{q['q']}\n\nJavobingizni yozing 👇",
         rk([[WR_SKIP], [B_STOP]]))


def wr_answer(uid, text):
    st = WSTATE.get(uid)
    if not st:
        return
    q = st["list"][st["i"]]
    skip = text == WR_SKIP
    ok = (not skip) and wr_ok(q, text)
    if ok:
        st["ok"] += 1
        send(st["chat_id"], "✅ Toʻgʻri! " + q["e"])
    else:
        st["log"].append(f"{q['q'].splitlines()[-1][:80]} → {q['a'][0]}")
        send(st["chat_id"], ("⏭ Oʻtkazildi. " if skip else "❌ Notoʻgʻri. ") + f"Toʻgʻri javob: {q['a'][0]}\n{q['e']}")
    st["i"] += 1
    wr_next(uid)


def wr_finish(uid):
    st = WSTATE.pop(uid, None)
    if not st:
        return
    n, ok = len(st["list"]), st["ok"]
    pc = round(ok / n * 100) if n else 0
    lvl = "A+" if pc >= 90 else "A" if pc >= 75 else "B+" if pc >= 60 else "B" if pc >= 45 else "B dan past"
    txt = f"✍️ {st['title']}\n\nNatija: {ok}/{n} ({pc}%)\nDaraja: {lvl}"
    if st["log"]:
        txt += "\n\n❌ Xato javoblar:\n" + "\n".join("• " + x for x in st["log"][:15])
    send_long(st["chat_id"], txt, result_kb())
    report_result(uid, st["title"], ok, n)


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


def esse_btn():
    """Pastki klaviaturadagi esse tugmasi: Telegram ichida sayt ochiladi (natija botga yuborilishi uchun)."""
    if "claude.ai" in ESSE_URL:
        return B_ESSE
    return {"text": B_ESSE, "web_app": {"url": ESSE_URL}}


def main_kb():
    kb = rk([[B_TESTS, B_DICT]] + ([[B_AI]] if groq_key() else []) + [[B_LEARN, B_ABOUT]])
    kb["keyboard"].insert(1, [esse_btn() if isinstance(esse_btn(), dict) else {"text": B_ESSE}])
    return kb


B_LEX = "🧠 Lugʻat testi"
LEX_CATS = [("📘 Atamalar testi", "atama"), ("🎭 Adabiy atamalar testi", "adabiy"),
            ("🌸 Badiiy soʻzlar testi", "badiiy"), ("🧵 Frazeologizm testi", "frazeo"),
            ("📜 Maqol testi", "maqol")]
LEX_BTN = dict(LEX_CATS)
LEX_NAME = {k: t for t, k in LEX_CATS}


def tests_kb():
    return rk([[B_TUR], [B_GEN], [B_LEX], [B_WR], [B_BACK]])


def lex_kb():
    return rk([[t] for t, _ in LEX_CATS] + [[B_OTHER, B_MENU]])


def lex_questions(key):
    """Lugʻat yozuvlaridan har safar yangi, tasodifiy savollar tuzadi (poll cheklovlari hisobga olingan)."""
    cat = next(c for c in CATEGORIES if c["key"] == key)
    E = cat["entries"]
    if key == "maqol":
        ask_a = "«{w}» maqolining maʼnosi qaysi?"
        ask_b = "Quyidagi maʼno qaysi maqolga tegishli?\n\n{m}"
    elif key == "frazeo":
        ask_a = "«{w}» frazeologizmi qanday maʼnoni bildiradi?"
        ask_b = "Quyidagi maʼno qaysi frazeologizmga tegishli?\n\n{m}"
    elif key == "atama":
        ask_a = "«{w}» atamasi nimani bildiradi?"
        ask_b = "Quyidagi taʼrif qaysi atamaga tegishli?\n\n{m}"
    else:
        ask_a = "«{w}» soʻzining maʼnosi qaysi?"
        ask_b = "Quyidagi izoh qaysi soʻzga tegishli?\n\n{m}"
    short = [e for e in E if len(e[1]) <= 98]
    out = []
    for i, (w, m, ex) in enumerate(E):
        others = [e for e in E if e[0] != w]
        if len(m) <= 98 and len(short) >= 4:
            wr = random.sample([e for e in short if e[0] != w], 3)
            o = [m] + [x[1] for x in wr]
            if len(set(o)) == 4:
                random.shuffle(o)
                out.append({"q": ask_a.format(w=w), "o": o, "a": o.index(m), "kind": 0})
        if len(w) <= 98 and len(m) <= 240:
            wr = random.sample([e for e in others if len(e[0]) <= 98], 3)
            o = [w] + [x[0] for x in wr]
            if len(set(o)) == 4:
                random.shuffle(o)
                out.append({"q": ask_b.format(m=m), "o": o, "a": o.index(w), "kind": 1})
    return out


def start_lex(uid, chat_id, key, n=None):
    start_quiz(uid, chat_id, LEX_NAME[key].replace(" testi", "") + " — lugʻat testi",
               lex_questions(key), ("lex", key), 0, n)


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


def size_kb():
    items = [f"{n} talik" for n in SIZES]
    rows = [items[i:i + 3] for i in range(0, len(items), 3)]
    rows.append([B_OTHER, B_MENU])
    return rk(rows)


def ask_size(uid, chat_id, last):
    PENDING[uid] = last
    extra = ("Javobni oʻzingiz yozasiz, vaqt cheklanmagan. " if last[0] == "wr" else "Har bir savolga 30 soniya. ")
    send(chat_id, "Nechta savolli test yechasiz? 👇\n\n10 talik — tezkor mashq, 50 talik — jiddiy tayyorgarlik, "
                  "100 talik — toʻliq imtihon. " + extra +
                  "(Agar bu boʻlimda savol kam boʻlsa, mavjud savollarning hammasi beriladi.)", size_kb())


def learn_kb():
    items = list(NEW_BTN) + list(SEC_BTN)
    rows = [[B_LT]] + [items[i:i + 2] for i in range(0, len(items), 2)] + [[B_MENU]]
    return rk(rows)


def lt_kb():
    items = list(LT_BTN)
    rows = [items[i:i + 2] for i in range(0, len(items), 2)]
    rows.append([B_LEARN, B_MENU])
    return rk(rows)


def show_lesson(chat_id, text, extra_row=None, back=None):
    rows = ([extra_row] if extra_row else []) + [[B_LEARN, B_MENU]]
    send(chat_id, text, rk(rows), "HTML")


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
def start_quiz(uid, chat_id, title, pool, last, pro_n=None, size=None):
    size = size or QUIZ_SIZE
    pros = [q for q in pool if q.get("pro")]
    random.shuffle(pros)
    base = QUIZ_SIZE // 2 if pro_n is None else pro_n
    pros = pros[:max(0, round(base * size / QUIZ_SIZE))]
    pool = [q for q in pool if not any(q is p for p in pros)]
    groups = {}
    for q in pool:
        groups.setdefault(q.get("kind", 0), []).append(q)
    for g in groups.values():
        random.shuffle(g)
    order = list(groups)
    random.shuffle(order)
    chosen = list(pros)
    while len(chosen) < size and any(groups.values()):
        for kd in order:
            if groups[kd] and len(chosen) < size:
                chosen.append(groups[kd].pop())
    random.shuffle(chosen)
    qs = [fresh(q) for q in chosen]
    STATE[uid] = {"title": title, "qs": qs, "i": 0, "score": 0,
                  "chat_id": chat_id, "poll_id": None}
    LAST[uid] = last
    LAST_N[uid] = size
    send(chat_id, f"{title}\n\n{len(qs)} ta savol. Har bir savolga {TIME_LIMIT} soniya beriladi ⏱ "
                  "(vaqt tugasa, savol oʻtkazib yuboriladi). Omad! 🍀", quiz_kb())
    send_next(uid)


# Darajalar bir pogʻona yuqorilashtirilgan: B — B+ va A savollaridan, B+ — A, A — A va A+, A+ — eng qiyin savollar
HARD_SRC = {"d1": ["d2", "d3"], "d2": ["d3"], "d3": ["d3", "d4"], "d4": ["d4", "d3"]}
HARD_PRO = {"d1": 4, "d2": 6, "d3": 8, "d4": 9}


def start_general(uid, chat_id, level, n=None):
    pool = []
    for src in HARD_SRC[level]:
        part = LEVELS[src]["questions"]
        pool += part if not (level == "d4" and src == "d3") else [q for q in part if q.get("pro")]
    start_quiz(uid, chat_id, LEVELS[level]["title"], pool, ("gen", level), HARD_PRO[level], n)


def start_turkum(uid, chat_id, tk, lv, n=None):
    title = f"{TUR_META['title'][tk]} — {LVL_TITLE[lv]}"
    pool = []
    for src in HARD_SRC[lv]:
        part = TUR_TESTS[tk][src]
        pool += part if not (lv == "d4" and src == "d3") else [q for q in part if q.get("pro")]
    start_quiz(uid, chat_id, title, pool, ("tur", tk, lv), HARD_PRO[lv], n)


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


# ------------------------------------------------------------------ Esse natijalari
ESSE_FILE = os.path.join(DATA_DIR, "esse_natijalar.jsonl")
A_ESSE = "✍️ Esse natijalari"


def read_esse():
    out = []
    try:
        with open(ESSE_FILE, encoding="utf-8") as f:
            for line in f:
                try:
                    out.append(json.loads(line))
                except Exception:
                    pass
    except FileNotFoundError:
        pass
    return out


def save_esse(rec):
    with open(ESSE_FILE, "a", encoding="utf-8") as f:
        f.write(json.dumps(rec, ensure_ascii=False) + "\n")


def handle_esse_data(msg):
    """Saytdan (Mini App) kelgan esse natijasi."""
    uid = msg.get("from", {}).get("id")
    chat_id = msg["chat"]["id"]
    try:
        d = json.loads(msg["web_app_data"]["data"])
        if d.get("k") != "esse":
            return
        rec = {
            "ts": int(d.get("ts") or time.time() * 1000), "uid": uid,
            "name": str(d.get("name") or "")[:60], "topic": str(d.get("topic") or "")[:90],
            "cat": str(d.get("cat") or "")[:40], "words": int(d.get("words") or 0),
            "score": int(d.get("score") or 0), "level": str(d.get("level") or "")[:12],
            "im": d.get("im"), "tu": d.get("tu"), "mz": d.get("mz"),
        }
    except Exception:
        send(chat_id, "Natijani oʻqib boʻlmadi. Qayta urinib koʻring.")
        return
    for old in read_esse():
        if old.get("uid") == uid and old.get("ts") == rec["ts"]:
            send(chat_id, "Bu natija allaqachon yuborilgan ✅", main_kb())
            return
    save_esse(rec)
    send(chat_id, f"✅ Natijangiz qabul qilindi: {rec['score']} ball ({rec['level']}).\nOmad!", main_kb())
    if not is_admin(uid):
        notify_admins(f"✍️ Yangi esse\n👤 {rec['name']} ({who(uid)})\n📝 {rec['topic']}\n"
                       f"⭐ {rec['score']} ball, {rec['level']} · {rec['words']} soʻz")


def admin_url(limit=1900):
    """Admin uchun sayt havolasi: natijalar siqilgan holda havolaga joylanadi."""
    import zlib, base64
    rows = read_esse()
    if "claude.ai" in ESSE_URL:
        return ESSE_URL
    scores = [r.get("score", 0) for r in rows]
    base = {"n": len(rows), "u": len({r.get("uid") for r in rows}),
            "v": round(sum(scores) / len(scores)) if scores else 0}
    take = rows[-80:][::-1]
    while True:
        base["r"] = [[r.get("ts"), r.get("name"), r.get("topic"), r.get("words"), r.get("score"),
                      r.get("level"), r.get("im"), r.get("tu"), r.get("mz")] for r in take]
        raw = json.dumps(base, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
        b = base64.urlsafe_b64encode(zlib.compress(raw, 9)).decode().rstrip("=")
        url = ESSE_URL + ("&" if "?" in ESSE_URL else "?") + "a=" + b
        if len(url) <= limit or not take:
            return url
        take = take[:-2] if len(take) > 2 else []


def esse_summary(chat_id):
    rows = read_esse()
    if not rows:
        send(chat_id, "Hozircha esse natijasi yoʻq.")
        return
    avg = round(sum(r.get("score", 0) for r in rows) / len(rows))
    lines = [f"{i}. {r['name']} — {r['score']} ({r['level']}), {r['words']} soʻz\n   {r['topic']}"
             for i, r in enumerate(rows[-15:][::-1], 1)]
    send(chat_id, f"✍️ Esse natijalari\nJami: {len(rows)} ta · oʻrtacha: {avg}\n\n" + "\n".join(lines))


def notify_admins(text):
    for a in all_admin_ids():
        try:
            send(a, text)
        except Exception:
            pass


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
    if not is_admin(uid):
        notify_admins(f"📊 Yangi natija\n👤 {who(uid)}\n📝 {title}\n✅ {score}/{total}")


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
    n = LAST_N.get(uid)
    if last and last[0] == "gen":
        start_general(uid, chat_id, last[1], n)
    elif last and last[0] == "tur":
        start_turkum(uid, chat_id, last[1], last[2], n)
    elif last and last[0] == "lex":
        start_lex(uid, chat_id, last[1], n)
    elif last and last[0] == "wr":
        start_wr(uid, chat_id, last[1], n)
    else:
        send(chat_id, "Qaysi testni yechamiz? 👇", tests_kb())


def finish_registration(uid, chat_id):
    REG.pop(uid, None)
    save_users()
    send(chat_id, "✅ Roʻyxatdan oʻtdingiz! Endi testlarni boshlashingiz mumkin.", main_kb())
    if ADMIN_ID:
        notify_admins(f"🆕 Yangi foydalanuvchi: {who(uid)}\nJami: {len(USERS)} ta")


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


A_ADM = "👮 Adminlar"
A_ADD = "➕ Admin qoʻshish"
A_DEL = "➖ Adminni chiqarish"
A_LIST = "📋 Adminlar roʻyxati"
A_CANCEL = "❌ Bekor qilish"
A_BACKADM = "⬅️ Admin menyusi"
ADMST = {}   # {uid: "add" | "del"}


def admin_kb(uid=None):
    kb = rk([[A_RES, A_STAT], [A_USERS, A_LAST], [A_EXP]])
    try:
        kb["keyboard"].append([{"text": A_ESSE, "web_app": {"url": admin_url()}}] if "claude.ai" not in ESSE_URL
                              else [{"text": "/esse"}])
    except Exception:
        pass
    if uid is not None and is_main(uid):
        kb["keyboard"].append([A_ADM])
    return kb


def adm_kb():
    return rk([[A_ADD, A_DEL], [A_LIST], [A_BACKADM]])


def admin_label(a):
    star = " ⭐ (bosh admin)" if a == ADMIN_ID else ""
    return f"{who(a)} — ID {a}{star}"


def admins_text():
    lines = [f"{i}. {admin_label(a)}" for i, a in enumerate(all_admin_ids(), 1)]
    return "👮 Adminlar roʻyxati:\n\n" + "\n".join(lines)


def parse_admin_target(msg, text):
    """ID raqam, @username yoki forward qilingan xabardan foydalanuvchi ID sini topadi."""
    fo = msg.get("forward_from") or ((msg.get("forward_origin") or {}).get("sender_user")) or {}
    if fo.get("id"):
        return int(fo["id"])
    t = text.strip()
    if t.lstrip("-").isdigit():
        return int(t)
    if t.startswith("@") or t.replace("_", "").isalnum():
        un = t.lstrip("@").lower()
        for u, d in USERS.items():
            if (d.get("username") or "").lower() == un:
                return int(u)
    return None


def admin_manage(chat_id, uid, text, msg):
    """Faqat bosh admin uchun: admin qoʻshish va chiqarish. True qaytarsa, xabar shu yerda ishlangan."""
    if text == A_BACKADM or text == A_CANCEL:
        ADMST.pop(uid, None)
        send(chat_id, "Admin menyusi 👇", admin_kb(uid))
        return True
    if text == A_ADM:
        ADMST.pop(uid, None)
        send(chat_id, admins_text() + "\n\nQuyidagi tugmalardan birini tanlang 👇", adm_kb())
        return True
    if text == A_LIST:
        send(chat_id, admins_text(), adm_kb())
        return True
    if text == A_ADD:
        ADMST[uid] = "add"
        send(chat_id, "Yangi adminning Telegram <b>ID raqamini</b> yuboring.\n\n"
                      "• U botga /id deb yozsa, ID raqamini koʻradi.\n"
                      "• Yoki uning <b>@username</b> ini yozing (u botdan roʻyxatdan oʻtgan boʻlsa).\n"
                      "• Yoki uning biror xabarini shu yerga <b>forward</b> qiling.",
             rk([[A_CANCEL]]), "HTML")
        return True
    if text == A_DEL:
        rest = [a for a in all_admin_ids() if a != ADMIN_ID]
        if not rest:
            send(chat_id, "Hozircha qoʻshimcha adminlar yoʻq. Faqat siz — bosh adminsiz.", adm_kb())
            return True
        ADMST[uid] = "del"
        rows = [[f"❌ {(USERS.get(str(a), {}).get('name') or 'Admin')[:30]} · {a}"] for a in rest]
        rows.append([A_CANCEL])
        send(chat_id, "Qaysi adminni chiqaramiz? 👇", rk(rows))
        return True
    st = ADMST.get(uid)
    if st == "add":
        if not text and not msg.get("forward_from") and not msg.get("forward_origin"):
            return True
        target = parse_admin_target(msg, text or "")
        if not target:
            send(chat_id, "Foydalanuvchini topa olmadim. ID raqam (masalan, 123456789), @username "
                          "yoki forward qilingan xabar yuboring.", rk([[A_CANCEL]]))
            return True
        ADMST.pop(uid, None)
        if target == ADMIN_ID:
            send(chat_id, "Bu siz — bosh adminsiz 🙂", adm_kb())
        elif target in ADMINS:
            send(chat_id, f"Bu foydalanuvchi allaqachon admin: {who(target)} (ID {target})", adm_kb())
        else:
            ADMINS.add(target)
            save_admins()
            STATE.pop(target, None)
            send(chat_id, f"✅ Admin qoʻshildi: {who(target)} (ID {target})\nJami adminlar: {len(all_admin_ids())} ta", adm_kb())
            try:
                send(target, "👑 Sizga admin huquqi berildi!\n\nEndi botda ishtirokchilar natijalari, "
                             "statistika va esse natijalarini koʻrasiz. Boshlash uchun /start yozing.", admin_kb(target))
            except Exception:
                pass
        return True
    if st == "del" and text.startswith("❌ "):
        tail = text.rsplit("·", 1)[-1].strip()
        if tail.isdigit() and int(tail) in ADMINS:
            t = int(tail)
            ADMINS.discard(t)
            save_admins()
            ADMST.pop(uid, None)
            send(chat_id, f"✅ Admin huquqi bekor qilindi: {who(t)} (ID {t})\nQolgan adminlar: {len(all_admin_ids())} ta", adm_kb())
            try:
                send(t, "Sizning admin huquqingiz bekor qilindi.", main_kb() if str(t) in USERS else {"remove_keyboard": True})
            except Exception:
                pass
        else:
            ADMST.pop(uid, None)
            send(chat_id, "Bunday admin topilmadi.", adm_kb())
        return True
    return False


def admin_entry(chat_id, text, uid=None, msg=None):
    """Admin rejimi: faqat natijalar, test va lugʻat yoʻq. Bosh admin adminlarni boshqaradi."""
    if uid is not None and is_main(uid) and admin_manage(chat_id, uid, text, msg or {}):
        return
    if text.startswith("/esse"):
        esse_summary(chat_id)
        return
    cmd = ADMIN_MAP.get(text) or (text.split()[0].split("@")[0] if text.startswith("/") else None)
    if cmd in ADMIN_MAP.values():
        admin_command(chat_id, cmd)
    else:
        send(chat_id, "👑 Admin rejimi — faqat natijalarni koʻrasiz.\n"
                      "Quyidagi tugmalardan birini tanlang 👇", admin_kb(uid))


def handle_message(msg):
    chat_id = msg["chat"]["id"]
    uid = msg.get("from", {}).get("id", chat_id)
    text = (msg.get("text") or "").strip()
    frm = msg.get("from", {})

    if msg.get("web_app_data"):
        handle_esse_data(msg)
        return
    if text.startswith("/id"):
        send(chat_id, f"Sizning Telegram ID raqamingiz: {uid}")
        return
    if is_admin(uid):
        admin_entry(chat_id, text, uid, msg)
        return
    if not is_admin(uid) and (str(uid) not in USERS or uid in REG):
        registration(msg, uid, chat_id, text, frm)
        return
    if not text:
        return

    # --- Yozma test: javoblar
    if WSTATE.get(uid):
        if text in (B_MENU, B_BACK, B_STOP, B_TESTS, B_OTHER, B_LEARN, B_DICT, B_ESSE, B_ABOUT) or text.startswith("/"):
            WSTATE.pop(uid, None)
        else:
            wr_answer(uid, text)
            return
    # --- AI esse tekshiruvi
    if text == B_AI:
        STATE.pop(uid, None)
        AIST[uid] = True
        send(chat_id, "🤖 AI esse tekshiruvi\n\nEsseingizni bitta xabar qilib yuboring (kamida 40 soʻz, 100+ tavsiya). "
                      "Birinchi qatorga mavzuni yozsangiz ham boʻladi.\n\n"
                      "AI imlo, tinish, tuzilish, mazmun va uslubni baholaydi, xatolarni koʻrsatadi va maslahat beradi. "
                      f"Kuniga {AI_PER_DAY} tagacha tekshirish mumkin. Chiqish: 🏠 Menyu.", rk([[B_MENU]]))
        return
    if AIST.get(uid) and not text.startswith("/") and len(text.split()) >= AI_MIN_WORDS:
        ai_check(uid, chat_id, text)
        return

    # --- Asosiy menyu
    if text.startswith("/start"):
        STATE.pop(uid, None)
        send(chat_id,
             "Assalomu alaykum! 👋\n\n"
             "Men ona tilini 0 dan oʻrganishda yordam beraman:\n"
             f"📝 Quiz-testlar ({total_questions()} ta savol): har bir soʻz turkumi uchun B, B+, A, A+ darajalarida\n"
             "📖 lugʻat — soʻz yozing, maʼnosini topaman\n"
             "✍️ Esse yozish — maxsus saytda 223 ta mavzu va tekshiruv\n\n"
             "Quyidagi tugmalardan birini tanlang 👇", main_kb())
    elif text.startswith("/menu") or text in (B_MENU, B_BACK):
        STATE.pop(uid, None)
        PICK.pop(uid, None)
        AIST.pop(uid, None)
        send(chat_id, "Asosiy menyu 👇", main_kb())
    elif text == B_STOP:
        STATE.pop(uid, None)
        WSTATE.pop(uid, None)
        send(chat_id, "Test toʻxtatildi.", main_kb())
    elif text == B_LEARN:
        STATE.pop(uid, None)
        send(chat_id, "📚 Oʻrganish\n\nOna tilining barcha boʻlimlari bir joyda:\n"
                      "🧩 12 ta soʻz turkumi: nima, soʻroqlari, maʼnoviy guruhlari, tuzilishi, qoʻllanishi + «Xatolar va mashq» sahifasi\n"
                      "🧱 Gap boʻlaklari, qoʻshma va ergash gap, koʻchirma gap, soʻz birikmasi, tahlil namunalari\n"
                      "✍️ Imlo, tinish belgilari, esse yozish bosqichlari, eng koʻp 20 xato, imtihonga tayyorgarlik\n"
                      "Har bir darsdan keyin shu mavzu boʻyicha test yechishingiz mumkin 👇",
             learn_kb())
    elif text == B_LT:
        send(chat_id, "Qaysi soʻz turkumini oʻrganamiz? 👇", lt_kb())
    elif text in LT_BTN:
        k = LT_BTN[text]
        LESSON[uid] = k
        tb = TUR_BTN_REV.get(k)
        row = ([tb] if tb else []) + [B_PRAC]
        send(chat_id, TUR[k], rk([row, [B_LT, B_LEARN], [B_MENU]]), "HTML")
    elif text == B_PRAC:
        k = LESSON.get(uid)
        if k in PRAC:
            tb = TUR_BTN_REV.get(k)
            send(chat_id, PRAC[k], rk([[tb] if tb else [B_LT], [B_LT, B_LEARN], [B_MENU]]), "HTML")
        else:
            send(chat_id, "Avval soʻz turkumini tanlang 👇", lt_kb())
    elif text in NEW_BTN:
        show_lesson(chat_id, NEW[NEW_BTN[text]])
    elif text in SEC_BTN:
        show_lesson(chat_id, SEC[SEC_BTN[text]])
    elif text == B_WR:
        STATE.pop(uid, None)
        send(chat_id, f"✍️ Yozma test\n\nBu yerda variant yoʻq: javobni oʻzingiz yozasiz. Jami {len(WTESTS)} ta savol: "
                      "imlo, qoʻshimchalar, soʻz yasalishi, soʻz turkumi, feʼl shakllari, olmosh turlari, boʻgʻin, antonim-sinonim, "
                      "atama-adabiyot, tinish belgilari va gap turlari. Turini tanlang 👇", wr_kb())
    elif text == WR_ALL:
        ask_size(uid, chat_id, ("wr", None))
    elif text in WR_BTN:
        ask_size(uid, chat_id, ("wr", WR_BTN[text]))
    elif text in (B_TESTS, B_OTHER):
        STATE.pop(uid, None)
        send(chat_id, "📝 Testlar\n\n🧩 Soʻz turkumlari testi — har bir turkum (ot, sifat, feʼl...) "
                      "uchun B, B+, A, A+ darajalarida 100 dan ortiq, yarmi professor darajasidagi savol; savollar sonini (10 dan 100 gacha) oʻzingiz tanlaysiz. Har bir savolga 30 soniya beriladi.\n"
                      "📊 Umumiy testlar — butun ona tili boʻyicha B, B+, A, A+ darajalari.", tests_kb())
    elif text == B_GEN:
        STATE.pop(uid, None)
        send(chat_id, levels_text(), levels_kb())
    elif text == B_LEX:
        STATE.pop(uid, None)
        n = sum(len(c["entries"]) for c in CATEGORIES if c["key"] in LEX_NAME)
        send(chat_id, f"🧠 Lugʻat testi\n\nLugʻatdagi {n} ta yozuvdan (atama, adabiy va badiiy soʻz, frazeologizm, maqol) "
                      "har safar yangi savollar tuziladi (10 dan 100 gacha tanlaysiz). Har bir savolga 30 soniya.", lex_kb())
    elif text in LEX_BTN:
        STATE.pop(uid, None)
        ask_size(uid, chat_id, ("lex", LEX_BTN[text]))
    elif text == B_TUR:
        STATE.pop(uid, None)
        send(chat_id, "Soʻz turkumini tanlang 👇", tur_kb())
    elif text in TUR_BTN:
        STATE.pop(uid, None)
        PICK[uid] = TUR_BTN[text]
        send(chat_id, f"{TUR_META['title'][PICK[uid]]}\n\nDarajani tanlang 👇 (B, B+, A, A+)\n"
                      "Savollar qiyinlashtirilgan: har bir darajada 100 dan ortiq savol, koʻpchiligi professor darajasida; savollar sonini 10 dan 100 gacha oʻzingiz tanlaysiz.", tur_levels_kb())
    elif text in LVL_BTN:
        STATE.pop(uid, None)
        if PICK.get(uid) in TUR_TESTS:
            ask_size(uid, chat_id, ("tur", PICK[uid], LVL_BTN[text]))
        else:
            send(chat_id, "Avval soʻz turkumini tanlang 👇", tur_kb())
    elif text in TITLE2KEY:
        STATE.pop(uid, None)
        ask_size(uid, chat_id, ("gen", TITLE2KEY[text]))
    elif text in SIZE_BTN and PENDING.get(uid):
        STATE.pop(uid, None)
        p = PENDING.pop(uid)
        n = SIZE_BTN[text]
        if p[0] == "wr":
            start_wr(uid, chat_id, p[1], n)
        elif p[0] == "gen":
            start_general(uid, chat_id, p[1], n)
        elif p[0] == "tur":
            start_turkum(uid, chat_id, p[1], p[2], n)
        else:
            start_lex(uid, chat_id, p[1], n)
    elif text == B_AGAIN:
        STATE.pop(uid, None)
        restart_last(uid, chat_id)
    elif text in CAT2OBJ:
        STATE.pop(uid, None)
        send_category(chat_id, CAT2OBJ[text])
    elif text == B_ESSE:
        STATE.pop(uid, None)
        send(chat_id,
             "✍️ Esse ustaxonasi\n\n"
             "223 ta mavzu (milliy sertifikat yoʻnalishlari), oʻz mavzu, kamida 100 soʻz, imlo, tinish va gap tuzilishi "
             "tekshiruvi, ball va daraja. Esse faqat saytda yoziladi 👇",
             {"inline_keyboard": [[({"text": "✍️ Esse ustaxonasini ochish", "web_app": {"url": ESSE_URL}}
                                    if "claude.ai" not in ESSE_URL else
                                    {"text": "✍️ Esse ustaxonasini ochish", "url": ESSE_URL})]]})
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
             f"📝 Testlar: jami {total_questions()} ta savol (12 soʻz turkumi × B, B+, A, A+ + umumiy testlar)\n"
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
