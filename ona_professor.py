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

PRO_DATA = {'ot': {'d3': [('«Kitoblarimizdan» soʻzida qoʻshimchalar qaysi tartibda joylashgan?', 'koʻplik + egalik + kelishik', 'egalik + koʻplik + kelishik', 'kelishik + egalik + koʻplik', 'kelishik + koʻplik + egalik'), ('Otlarning kelishik qoʻshimchalari bilan oʻzgarishi nima deyiladi?', 'Turlanish', 'Tuslanish', 'Darajalanish', 'Boʻgʻinlanish'), ('Quyidagi qatorlardan qaysi birida faqat atoqli otlar berilgan?', 'Navoiy, Samarqand, Amudaryo', 'shoir, shahar, daryo', 'Navoiy, shahar, Amudaryo', 'kitob, Samarqand, daryo'), ('Quyidagi qatorlardan qaysi birida mavhum otlar berilgan?', 'mehr, adolat, baxt', 'kitob, stol, qalam', 'Toshkent, Navoiy, Sirdaryo', 'bola, ona, oʻquvchi'), ('«Gulzor» soʻzi qanday yoʻl bilan yasalgan?', 'Qoʻshimcha qoʻshish (affiksatsiya) yoʻli bilan', 'Soʻzlarni qoʻshish (kompozitsiya) yoʻli bilan', 'Soʻzni takrorlash yoʻli bilan', 'Soʻzni qisqartirish yoʻli bilan'), ('«Ota-ona» soʻzi tuzilishiga koʻra qanday ot?', 'Juft ot', 'Takroriy ot', 'Qoʻshma ot', 'Qisqartma ot'), ('«Maktabning hovlisi» birikmasida «maktabning» qanday vazifada keladi?', 'Qaratqich aniqlovchi', 'Sifatlovchi aniqlovchi', 'Vositali toʻldiruvchi', 'Payt holi'), ('Qaratqich kelishigidagi ot odatda qaysi shakldagi ot bilan birikadi?', 'Egalik qoʻshimchasini olgan ot bilan', 'Feʼl bilan', 'Ravish bilan', 'Undov soʻz bilan'), ('«Bolani maktabga olib bordim.» gapida «bolani» qaysi gap boʻlagi?', 'Vositasiz toʻldiruvchi', 'Vositali toʻldiruvchi', 'Ega', 'Payt holi'), ('«Qalam» soʻzi qaysi tildan oʻzlashgan?', 'Arab tilidan', 'Fors tilidan', 'Rus tilidan', 'Yunon tilidan'), ('«Stol» soʻzi qaysi tildan oʻzlashgan?', 'Rus tilidan', 'Arab tilidan', 'Fors tilidan', 'Mongol tilidan'), ('Ot III shaxs egalik qoʻshimchasini qabul qilganda qaysi qoida amal qiladi?', 'Undoshdan keyin -i, unlidan keyin -si', 'Undoshdan keyin -si, unlidan keyin -i', 'Har doim -i', 'Har doim -si')], 'd4': [('«Tilak» soʻziga -im qoʻshilganda «tilagim» boʻladi. Bu qanday tovush hodisasi?', 'k tovushining g ga almashishi (jaranglilashuv)', 'Unli tovush tushishi', 'Unli tovush ortishi', 'Boʻgʻin tushishi'), ('«Singil» soʻzidan «singlim» hosil boʻlishida qanday hodisa yuz beradi?', 'Unli tovush (i) tushishi', 'Undosh tovush ortishi', 'Unli tovush ortishi', 'Undoshning almashishi'), ('«Toshkent — Oʻzbekistonning poytaxti.» gapida kesim qanday ifodalangan?', 'Ot bilan', 'Feʼl bilan', 'Sifat bilan', 'Son bilan'), ('«Yosh» soʻzi «yosh bola» va «yoshi katta» birikmalarida qanday xususiyat koʻrsatadi?', 'Sifat va ot sifatida qoʻllanadi (turkumdan turkumga oʻtish)', 'Faqat sifat sifatida qoʻllanadi', 'Faqat ot sifatida qoʻllanadi', 'Ravish sifatida qoʻllanadi'), ('Otlar maʼnosiga koʻra qaysi juft guruhlarga boʻlinadi?', 'Atoqli va turdosh; moddiy va mavhum', 'Oʻtimli va oʻtimsiz; sodda va qoʻshma', 'Asliy va nisbiy; oddiy va qiyosiy', 'Sanoq va tartib; dona va kasr'), ('«Qirollik» soʻzida -lik qoʻshimchasi qanday maʼno qoʻshgan?', 'Mavhum tushuncha (holat) nomini yasagan', 'Kichraytirish maʼnosini bergan', 'Koʻplik maʼnosini bergan', 'Oʻrin-joy nomini yasagan'), ('«Maktab» soʻzining «bino» va «taʼlim tizimi» maʼnolarida qoʻllanishi qanday hodisa?', 'Koʻp maʼnolilik (polisemiya)', 'Omonimiya', 'Sinonimiya', 'Paronimiya'), ('«Qoʻl» soʻzining «aʼzo» va «yordam» (qoʻl uzatmoq) maʼnolarida qoʻllanishi qaysi hodisaga misol?', 'Koʻchma maʼno', 'Omonimiya', 'Antonimiya', 'Paronimiya'), ('Qaysi gapda ot ega vazifasida kelgan?', 'Yomgʻir yogʻdi.', 'U yomgʻirda ketdi.', 'Yomgʻirni kutdik.', 'Yomgʻirdan keyin chiqdik.'), ('Qaysi gapda ot hol vazifasida kelgan?', 'Biz maktabda oʻqiymiz.', 'Maktab katta.', 'Maktabni koʻrdim.', 'Maktab bogʻi chiroyli.'), ('«Uyga keldim» gapida «uyga» soʻzi qaysi kelishikda va qanday vazifada?', 'Joʻnalish kelishigida, oʻrin holi', 'Tushum kelishigida, toʻldiruvchi', 'Chiqish kelishigida, oʻrin holi', 'Qaratqich kelishigida, aniqlovchi'), ('«Olma» soʻzining «meva» va «daraxt» maʼnolarida qoʻllanishi qanday hodisa?', 'Koʻp maʼnolilik', 'Omonimiya', 'Antonimiya', 'Paronimiya'), ('«Yoz» (fasl) va «yoz» (yozmoq) soʻzlari oʻzaro qanday munosabatda?', 'Omonim', 'Sinonim', 'Antonim', 'Paronim')]}, 'sifat': {'d3': [('«Shirin» sifati belgining qaysi turini bildiradi?', 'Taʼm-maza belgisini', 'Rang-tus belgisini', 'Shakl belgisini', 'Hajm-oʻlchov belgisini'), ('«Yumaloq» sifati belgining qaysi turini bildiradi?', 'Shakl belgisini', 'Taʼm belgisini', 'Rang belgisini', 'Harorat belgisini'), ('«Baland» sifati belgining qaysi turini bildiradi?', 'Hajm-oʻlchov belgisini', 'Rang belgisini', 'Taʼm belgisini', 'Xarakter belgisini'), ('«Ilmiy» soʻzi sifatning qaysi turiga kiradi?', 'Nisbiy sifat', 'Asliy sifat', 'Qiyosiy sifat', 'Orttirma sifat'), ('«Yoʻgʻon» soʻzi sifatning qaysi turiga kiradi?', 'Asliy sifat', 'Nisbiy sifat', 'Qiyosiy sifat', 'Kamaytirma sifat'), ('«Xushmuomala» soʻzi tuzilishiga koʻra qanday sifat?', 'Qoʻshma sifat', 'Sodda sifat', 'Juft sifat', 'Takroriy sifat'), ('«Oq-sariq» soʻzi tuzilishiga koʻra qanday sifat?', 'Juft sifat', 'Qoʻshma sifat', 'Takroriy sifat', 'Sodda sifat'), ('«Katta-katta» soʻzi tuzilishiga koʻra qanday sifat?', 'Takroriy sifat', 'Juft sifat', 'Qoʻshma sifat', 'Sodda sifat'), ('«Bu gul juda chiroyli.» gapida «chiroyli» qaysi gap boʻlagi?', 'Kesim', 'Aniqlovchi', 'Ega', 'Hol'), ('«Chiroyli bogʻ koʻrindi.» gapida «chiroyli» qaysi gap boʻlagi?', 'Sifatlovchi aniqlovchi', 'Kesim', 'Ega', 'Oʻrin holi'), ('«Yaxshilar koʻp boʻlsin.» gapida «yaxshilar» soʻzida qanday hodisa yuz bergan?', 'Sifatning otlashishi', 'Otning sifatlanishi', 'Sifatning ravishlanishi', 'Feʼlning otlashishi'), ('«Qizgʻish» soʻzidagi -ish qoʻshimchasi qanday maʼno beradi?', 'Belgining kamligini (kamaytirma)', 'Belgining kuchliligini', 'Joy nomini', 'Kasb-hunar nomini')], 'd4': [('«Yengil» soʻzining «vazni kam» va «oson» maʼnolarida qoʻllanishi qanday hodisa?', 'Koʻp maʼnolilik (polisemiya)', 'Omonimiya', 'Sinonimiya', 'Paronimiya'), ('«Achchiq soʻz» birikmasida «achchiq» qanday maʼnoda?', 'Koʻchma maʼnoda', 'Toʻgʻri (asosiy) maʼnoda', 'Antonim maʼnoda', 'Termin maʼnoda'), ('«Tez poyezd keldi.» gapida «tez» qaysi soʻz turkumiga kiradi?', 'Sifat', 'Ravish', 'Ot', 'Olmosh'), ('«U tez yurdi.» gapida «tez» qaysi soʻz turkumiga kiradi?', 'Ravish', 'Sifat', 'Ot', 'Son'), ('«Yaxshi yozdi.» gapida «yaxshi» qaysi soʻz turkumiga kiradi?', 'Ravish', 'Sifat', 'Ot', 'Olmosh'), ('Soʻzning shaklini oʻzgartirmasdan boshqa turkumga oʻtishi nima deyiladi?', 'Konversiya', 'Affiksatsiya', 'Kompozitsiya', 'Abbreviatsiya'), ('«Kattagina» soʻzidagi -gina qoʻshimchasi qanday maʼno beradi?', 'Kichraytirish-erkalash', 'Kuchaytirish', 'Qiyoslash', 'Inkor'), ('«Qip-qizil» soʻzidagi «qip-» qismi qanday vazifa bajaradi?', 'Belgini kuchaytiradi', 'Belgini kamaytiradi', 'Ot yasaydi', 'Koʻplik bildiradi'), ('«Chiroylilik» soʻzi qanday yoʻl bilan va qaysi turkumdan yasalgan?', 'Sifatdan ot (affiksatsiya)', 'Otdan sifat (affiksatsiya)', 'Feʼldan ot (konversiya)', 'Sifatdan feʼl (affiksatsiya)'), ('«Oltin soch» birikmasida «oltin» soʻzi qanday vazifada qoʻllangan?', 'Koʻchma maʼnoli sifatlash (epitet)', 'Nisbiy sifat sifatida, toʻgʻri maʼnoda', 'Qiyosiy daraja shaklida', 'Ravish sifatida'), ('Sifatning orttirma darajasi qaysi usulda hosil qilinadi?', '«eng», «juda» kabi soʻzlar yoki takror orqali', '-roq qoʻshimchasi orqali', '-lik qoʻshimchasi orqali', '-la qoʻshimchasi orqali'), ('«Yaxshi» va «yomon» soʻzlari oʻzaro qanday munosabatda?', 'Antonim', 'Sinonim', 'Omonim', 'Paronim'), ('«Goʻzal» va «chiroyli» soʻzlari oʻzaro qanday munosabatda?', 'Sinonim', 'Antonim', 'Omonim', 'Paronim')]}, 'son': {'d3': [('Quyidagi qatorlardan qaysi birida sonlarning maʼno turlari toʻgʻri sanalgan?', 'sanoq, tartib, dona, kasr, jamlovchi, taxminiy', 'sanoq, tartib, atoqli, turdosh', 'asliy, nisbiy, oddiy, qiyosiy', 'sodda, qoʻshma, juft, takroriy'), ('«Yigirma» soniga tartib son qoʻshimchasi qoʻshilsa, qaysi shakl toʻgʻri?', 'yigirmanchi', 'yigirmainchi', 'yigirmachi', 'yigirmaninchi'), ('«Besh» soniga tartib son qoʻshimchasi qoʻshilsa, qaysi shakl toʻgʻri?', 'beshinchi', 'beshnchi', 'beshchi', 'beshanchi'), ('Son ot bilan birikkanda ot qanday shaklda keladi?', 'Birlikda: «uch kitob»', 'Koʻplikda: «uch kitoblar»', 'Qaratqich kelishigida', 'Faqat egalik shaklida'), ('«Beshta» soʻzidagi -ta qoʻshimchasi qanday son yasaydi?', 'Dona son', 'Tartib son', 'Jamlovchi son', 'Kasr son'), ('«Oʻnlab» soʻzidagi -lab qoʻshimchasi qanday maʼno beradi?', 'Taxminiy, noaniq koʻp miqdor', 'Tartib', 'Jamlovchi maʼno', 'Kasr maʼno'), ('«Besh kishi keldi.» gapida «besh» qaysi gap boʻlagi?', 'Aniqlovchi', 'Ega', 'Kesim', 'Hol'), ('Quyidagi qatorlardan qaysi birida faqat kasr sonlar bor?', 'yarim, chorak, uchdan bir', 'ikkita, beshinchi, oʻnlab', 'uch, besh, yetti', 'birinchi, ikkinchi, uchinchi'), ('«Bir kishi keldi.» gapida «bir» soni qanday maʼnoda qoʻllangan?', 'Noaniqlik maʼnosida', 'Sanoq maʼnosida (1 ta)', 'Tartib maʼnosida', 'Kasr maʼnosida'), ('«Beshni uchga qoʻshdim.» gapida «beshni» soʻzida qanday hodisa yuz bergan?', 'Sonning otlashishi', 'Otning sonlashishi', 'Sifatning otlashishi', 'Feʼlning otlashishi')], 'd4': [('«Ikki» va «ikkita» soʻzlari oʻrtasidagi farq qaysi?', 'Ikki — sanoq son, ikkita — dona son', 'Ikki — dona son, ikkita — sanoq son', 'Ikkisi ham tartib son', 'Farq yoʻq, bir xil son turi'), ('«Yuz» soʻzining «100» va «betning old qismi» maʼnolarida qoʻllanishi qanday hodisa?', 'Omonimiya', 'Koʻp maʼnolilik', 'Sinonimiya', 'Antonimiya'), ('Qaysi qatorda tartib sonlar toʻgʻri yozilgan?', 'oltinchi, yettinchi, sakkizinchi', 'oltiinchi, yettinchi, sakkizinchi', 'oltinchi, yettiinchi, sakkizinchi', 'oltinchi, yettinchi, sakkiznchi'), ('«Beshta olma yedi.» gapida «beshta» qaysi gap boʻlagi?', 'Aniqlovchi', 'Toʻldiruvchi', 'Hol', 'Kesim'), ('Sonlar boshqa turkumlardan qaysi belgisi bilan ajraladi?', 'Miqdor yoki tartibni bildirishi va necha? nechanchi? soʻroqlariga javob berishi', 'Harakat bildirishi', 'Narsa belgisini rang bilan bildirishi', 'Shaxs oʻrnida ishlatilishi'), ('Tartib sonlar sifatga qaysi jihatdan oʻxshaydi?', 'Otni aniqlashi va aniqlovchi vazifasida kelishi', 'Daraja shakllariga ega boʻlishi', 'Qiyoslanishi', 'Harakat bildirishi'), ('«Oʻninchi dars» birikmasida bosh soʻz qaysi?', 'dars', 'oʻninchi', 'Ikkalasi teng', 'Bosh soʻz yoʻq')]}, 'olmosh': {'d3': [('Olmoshlar qaysi soʻz turkumlari oʻrnida ishlatiladi?', 'Ot, sifat, son (va ravish) oʻrnida', 'Faqat feʼl oʻrnida', 'Faqat undov soʻz oʻrnida', 'Faqat bogʻlovchi oʻrnida'), ('«U» olmoshiga -ga qoʻshilganda «unga» boʻladi. Qaysi hodisa yuz beradi?', 'n tovushining ortishi', 'Unli tovush tushishi', 'Undoshning almashishi', 'Boʻgʻin tushishi'), ('«Bu kitob qiziq.» gapida «bu» qaysi gap boʻlagi?', 'Aniqlovchi', 'Ega', 'Kesim', 'Hol'), ('«Hamma keldi.» gapida «hamma» qaysi gap boʻlagi?', 'Ega', 'Kesim', 'Aniqlovchi', 'Hol'), ('«Hech kim kelmadi.» gapida inkor maʼnosi qanday ifodalangan?', 'Boʻlishsizlik olmoshi va boʻlishsiz shakldagi kesim bilan', 'Faqat olmosh bilan', 'Faqat yuklama bilan', 'Faqat ravish bilan'), ('«Mening kitobim» birikmasida «mening» qanday vazifada?', 'Qaratqich aniqlovchi', 'Sifatlovchi aniqlovchi', 'Ega', 'Toʻldiruvchi'), ('«Siz» va «sen» olmoshlari oʻrtasidagi asosiy uslubiy farq qaysi?', '«Siz» hurmat, «sen» yaqinlik bildiradi', '«Siz» koʻplik, «sen» birlik, farqi faqat sonda', 'Farq yoʻq', '«Sen» rasmiy, «siz» norasmiy'), ('Qaysi qatorda faqat soʻroq olmoshlari bor?', 'kim, nima, qaysi, qancha', 'men, sen, u, biz', 'bu, shu, oʻsha', 'hamma, barcha, har'), ('Qaysi qatorda faqat belgilash olmoshlari bor?', 'hamma, barcha, har, butun', 'kim, nima, qaysi', 'bu, shu, oʻsha', 'kimdir, nimadir, biror'), ('Qaysi qatorda faqat gumon olmoshlari bor?', 'kimdir, nimadir, biror', 'men, sen, u', 'hech kim, hech narsa', 'oʻzim, oʻzing, oʻzi')], 'd4': [('Oʻzlik olmoshi «oʻz» qaysi qoʻshimchalarni qabul qiladi?', 'Egalik qoʻshimchalarini', 'Faqat tuslovchi qoʻshimchalarni', 'Faqat -lar ni', 'Hech qanday qoʻshimchani'), ('Olmosh bilan ot orasidagi asosiy farq qaysi?', 'Olmosh narsani nomlamaydi, balki unga ishora qiladi yoki uni almashtiradi', 'Olmosh narsani aniq nomlaydi', 'Olmosh harakatni bildiradi', 'Olmosh faqat sonni bildiradi'), ('Ilmiy maqolada muallif «Biz bu masalani tahlil qildik» deganda «biz» qanday maʼnoda?', 'Muallifning oʻzi (kamtarlik maʼnosida)', 'Koʻp odam', 'Oʻquvchilar', 'Hurmat bilan murojaat'), ('«Shunday kitob qiziq.» gapida «shunday» qaysi gap boʻlagi?', 'Aniqlovchi', 'Ega', 'Kesim', 'Hol'), ('«U kelganda uyda edim.» gapida «u» olmoshi qaysi shaxsni bildiradi?', 'III shaxs birlik', 'I shaxs birlik', 'II shaxs birlik', 'III shaxs koʻplik'), ('«Men» olmoshining tushum kelishigi shakli qaysi?', 'meni', 'mening', 'menga', 'mendan'), ('«Ular» olmoshining joʻnalish kelishigi shakli qaysi?', 'ularga', 'ularni', 'ularning', 'ulardan'), ('«Kimning?» soʻrogʻiga javob boʻlgan olmosh shakli qaysi?', 'mening, sening, uning', 'meni, seni, uni', 'menga, senga, unga', 'mendan, sendan, undan'), ('Gumon olmoshlari qaysi qoʻshimcha yordamida yasaladi?', '-dir (kimdir, nimadir) va bir (birov, bironta)', '-lik', '-chi', '-siz'), ('«Har kim oʻz ishini qiladi» gapida «har kim» qanday olmosh?', 'Belgilash olmoshi', 'Soʻroq olmoshi', 'Gumon olmoshi', 'Kishilik olmoshi')]}, 'feil': {'d3': [('«Yordam bermoq» birikmasi tuzilishiga koʻra qanday feʼl?', 'Qoʻshma feʼl', 'Sodda feʼl', 'Juft feʼl', 'Takroriy feʼl'), ('«Oʻqimoq» feʼli qanday feʼl?', 'Oʻtimli feʼl', 'Oʻtimsiz feʼl', 'Yordamchi feʼl', 'Nisbat feʼli'), ('«Yugurmoq» feʼli qanday feʼl?', 'Oʻtimsiz feʼl', 'Oʻtimli feʼl', 'Yordamchi feʼl', 'Qoʻshma feʼl'), ('Oʻtimli feʼl qanday gap boʻlagini talab qiladi?', 'Vositasiz toʻldiruvchini (tushum kelishigida)', 'Payt holini', 'Qaratqich aniqlovchini', 'Undalmani'), ('Feʼlning shaxs-son qoʻshimchalari bilan oʻzgarishi nima deyiladi?', 'Tuslanish', 'Turlanish', 'Darajalanish', 'Qoʻshilish'), ('Feʼlning boʻlishsiz shakli qaysi qoʻshimcha bilan yasaladi?', '-ma', '-mi', '-siz', '-ga'), ('«Yozmoqchi» soʻzidagi -moqchi qoʻshimchasi qanday maʼno bildiradi?', 'Niyat, maqsad', 'Boʻlishsizlik', 'Tugallanganlik', 'Orttirma'), ('Qaysi qatorda ravishdosh qoʻshimchalari berilgan?', '-ib, -gach, -guncha', '-gan, -ar, -yotgan', '-moq, -ish, -v', '-ma, -mi, -siz'), ('Qaysi qatorda sifatdosh qoʻshimchalari berilgan?', '-gan, -ar, -yotgan', '-ib, -gach, -guncha', '-moq, -ish, -v', '-di, -yapti, -adi'), ('Qaysi qatorda harakat nomi qoʻshimchalari berilgan?', '-moq, -ish, -v', '-ib, -gach, -guncha', '-gan, -ar, -yotgan', '-man, -san, -miz'), ('«Oʻqimoq» feʼlining «savod chiqarmoq» va «taʼlim olmoq» maʼnolari qanday hodisaga misol?', 'Koʻp maʼnolilik', 'Omonimiya', 'Sinonimiya', 'Antonimiya'), ('«Kelsa» shakli feʼlning qaysi mayliga kiradi?', 'Shart mayli', 'Buyruq mayli', 'Aniqlik mayli', 'Istak mayli'), ('«Boramiz» soʻzidagi -miz qoʻshimchasi qaysi shaxs-sonni bildiradi?', 'I shaxs koʻplik', 'II shaxs koʻplik', 'I shaxs birlik', 'III shaxs koʻplik')], 'd4': [('«Oʻqib chiqdi» birikmasida «chiqdi» yordamchi feʼli qanday maʼno qoʻshadi?', 'Harakatning tugallanganlik maʼnosini', 'Boʻlishsizlik maʼnosini', 'Orttirma maʼnosini', 'Majhullik maʼnosini'), ('Feʼlning qaysi shakli gapda sifat vazifasini bajaradi?', 'Sifatdosh', 'Ravishdosh', 'Harakat nomi', 'Buyruq mayli'), ('Feʼlning qaysi shakli gapda ravish vazifasini bajaradi?', 'Ravishdosh', 'Sifatdosh', 'Harakat nomi', 'Shart mayli'), ('Feʼlning qaysi shakli gapda ot vazifasini bajara oladi?', 'Harakat nomi', 'Ravishdosh', 'Sifatdosh', 'Buyruq mayli'), ('«Oʻqiyotgan bola» birikmasida «oʻqiyotgan» qaysi shaklda?', 'Hozirgi zamon sifatdoshi', 'Oʻtgan zamon ravishdoshi', 'Harakat nomi', 'Shart mayli'), ('«Yozdirdi» va «yozildi» shakllari qaysi nisbatlarga mansub?', 'Orttirma va majhul nisbat', 'Majhul va orttirma nisbat', 'Oʻzlik va birgalik nisbat', 'Birgalik va oʻzlik nisbat'), ('«Keldi» soʻzida III shaxs birlik qoʻshimchasi qanday ifodalangan?', 'Nol (koʻrinmaydigan) qoʻshimcha bilan', '-i bilan', '-di bilan shaxs ham ifodalangan', '-man bilan'), ('«Kitob oʻqigan odam» birikmasida «oʻqigan» qanday sintaktik vazifada?', 'Aniqlovchi', 'Kesim', 'Ega', 'Payt holi'), ('«Kulib gapirdi» gapida «kulib» qaysi shakl va qaysi vazifada?', 'Ravishdosh, tarz holi', 'Sifatdosh, aniqlovchi', 'Harakat nomi, ega', 'Aniqlik mayli, kesim'), ('«Yozish foydali.» gapida «yozish» qanday vazifada?', 'Ega (harakat nomi)', 'Kesim', 'Aniqlovchi', 'Hol'), ('«Bor!» shakli feʼlning qaysi mayliga kiradi?', 'Buyruq mayli', 'Shart mayli', 'Aniqlik mayli', 'Istak mayli'), ('«Borgim keldi» shakli qaysi mayl?', 'Istak mayli', 'Buyruq mayli', 'Shart mayli', 'Aniqlik mayli'), ('«Bormoq» va «borish» shakllari qanday umumiy xususiyatga ega?', 'Ikkalasi ham harakat nomi', 'Ikkalasi ham sifatdosh', 'Ikkalasi ham ravishdosh', 'Ikkalasi ham buyruq mayli')]}, 'ravish': {'d3': [('Ravish qaysi turkumlarni aniqlab keladi?', 'Feʼl, sifat va boshqa ravishni', 'Faqat otni', 'Faqat sonni', 'Faqat olmoshni'), ('«Juda chiroyli» birikmasida «juda» qaysi soʻz turkumi?', 'Ravish', 'Sifat', 'Olmosh', 'Yuklama'), ('Ravishlar maʼnosiga koʻra qaysi guruhlarga boʻlinadi?', 'Payt, oʻrin, tarz, miqdor-daraja, maqsad, sabab', 'Asliy, nisbiy, qiyosiy', 'Sanoq, tartib, dona', 'Oʻtimli, oʻtimsiz'), ('«Tez-tez» soʻzi tuzilishiga koʻra qanday ravish?', 'Takroriy ravish', 'Juft ravish', 'Qoʻshma ravish', 'Sodda ravish'), ('Qaysi qoʻshimcha ravish yasaydi?', '-lab (kunlab)', '-chi', '-lik', '-li'), ('«Oʻzbekcha gapirdi» soʻzida «oʻzbekcha» qaysi soʻz turkumi va vazifada?', 'Ravish, tarz holi', 'Sifat, aniqlovchi', 'Ot, ega', 'Olmosh, toʻldiruvchi'), ('«Bugun dars bor.» gapida «bugun» qaysi gap boʻlagi?', 'Payt holi', 'Ega', 'Kesim', 'Aniqlovchi'), ('«Pastda daryo oqdi.» gapida «pastda» qaysi gap boʻlagi?', 'Oʻrin holi', 'Payt holi', 'Tarz holi', 'Ega'), ('«Ancha uzoq yoʻl yurdik.» gapida «ancha» qaysi soʻz turkumi?', 'Ravish (miqdor-daraja)', 'Sifat', 'Son', 'Olmosh')], 'd4': [('«Yaxshi» soʻzining «yaxshi odam» va «yaxshi yozdi» birikmalarida qoʻllanishi qanday hodisa?', 'Konversiya (turkumdan turkumga oʻtish)', 'Omonimiya', 'Antonimiya', 'Paronimiya'), ('Konversiya nima?', 'Soʻzning shaklini oʻzgartirmay boshqa turkumga oʻtishi', 'Soʻzning qisqarishi', 'Soʻzga yasovchi qoʻshimcha qoʻshilishi', 'Soʻz maʼnosining koʻchishi'), ('Qaysi gapda «kech» ravish vazifasida kelgan?', 'U bugun kech qaytdi.', 'Kech tushdi.', 'Kechni tinch oʻtkazdik.', 'Kechning sovugʻi yoqdi.'), ('«Kam-kam gapirdi» gapida «kam-kam» soʻzi tuzilishiga koʻra qanday?', 'Takroriy ravish', 'Qoʻshma ravish', 'Juft ravish', 'Sodda ravish'), ('«Juda yaxshi, juda tez» birikmalarida «juda» ravishining vazifasi qanday?', 'Sifat va ravishning belgisini kuchaytiradi', 'Otni aniqlaydi', 'Feʼlni boʻlishsiz qiladi', 'Gap boʻlagini bogʻlaydi'), ('«Hozirgina ketdi» soʻzidagi -gina qoʻshimchasi qanday maʼno beradi?', 'Taʼkid (shu zahotiyoq maʼnosini kuchaytiradi)', 'Kichraytirish (hajm)', 'Koʻplik', 'Inkor'), ('Ravish gapda koʻpincha qaysi gap boʻlagi vazifasida keladi?', 'Hol', 'Ega', 'Kesim', 'Undalma'), ('«Oʻzbekcha», «ruscha» soʻzlaridagi -cha qoʻshimchasi qanday maʼno beradi?', 'Tarz (til yoki uslub boʻyicha)', 'Oʻrin', 'Payt', 'Miqdor')]}, 'komakchi': {'d3': [('«Uchun» koʻmakchisi qanday maʼnoni bildiradi?', 'Maqsad yoki sabab', 'Oʻxshatish', 'Yoʻnalish', 'Chegara'), ('«Kabi» koʻmakchisi qanday maʼnoni bildiradi?', 'Oʻxshatish', 'Maqsad', 'Chegara', 'Yoʻnalish'), ('«Qadar» koʻmakchisi qanday maʼnoni bildiradi?', 'Chegara (vaqt, oʻrin, miqdor)', 'Oʻxshatish', 'Vosita', 'Sabab'), ('Koʻmakchi gap boʻlagi boʻla oladimi?', 'Yoʻq, u mustaqil gap boʻlagi boʻlmaydi', 'Ha, har doim ega boʻladi', 'Ha, har doim kesim boʻladi', 'Ha, hol boʻladi'), ('«Doʻstim bilan keldim» gapida «doʻstim bilan» qaysi gap boʻlagi?', 'Toʻldiruvchi', 'Ega', 'Kesim', 'Payt holi'), ('«Mendan boshqa hamma keldi» gapida «boshqa» koʻmakchisi qaysi kelishikdagi soʻz bilan keldi?', 'Chiqish kelishigi', 'Tushum kelishigi', 'Joʻnalish kelishigi', 'Qaratqich kelishigi'), ('«Kechadan beri yomgʻir yogʻyapti» gapida «beri» koʻmakchisi qaysi kelishikdagi soʻz bilan keldi?', 'Chiqish kelishigi', 'Joʻnalish kelishigi', 'Tushum kelishigi', 'Oʻrin-payt kelishigi'), ('«Ali bilan Vali keldi.» gapida «bilan» qaysi soʻz turkumi?', 'Bogʻlovchi', 'Koʻmakchi', 'Yuklama', 'Ravish'), ('«Qalam bilan yozdim.» gapida «bilan» qaysi soʻz turkumi?', 'Koʻmakchi', 'Bogʻlovchi', 'Yuklama', 'Undov')], 'd4': [('Koʻmakchilar boshqa yordamchi soʻzlardan qaysi belgisi bilan farqlanadi?', 'Soʻzlarning grammatik bogʻlanishini kelishik bilan birgalikda ifodalashi', 'Gapni gapga bogʻlashi', 'Soʻroq maʼnosini berishi', 'Hissiyotni bildirishi'), ('«Yomgʻirga qaramay chiqdik» gapida «qaramay» qanday maʼno bildiradi?', 'Qarshilik', 'Sabab', 'Maqsad', 'Oʻxshatish'), ('«Reja asosida ish olib borildi» gapidagi «asosida» soʻzi qanday vazifada?', 'Asos bildiruvchi koʻmakchi vazifasida', 'Ega', 'Kesim', 'Undalma'), ('Koʻmakchili birikma gapda koʻpincha qanday vazifada keladi?', 'Toʻldiruvchi yoki hol', 'Faqat ega', 'Faqat kesim', 'Faqat undalma'), ('«Sari» va «tomon» koʻmakchilari qanday maʼno bildiradi?', 'Yoʻnalish', 'Chegara', 'Sabab', 'Oʻxshatish'), ('«Boʻyicha» koʻmakchisi qanday maʼno bildiradi?', 'Soha yoki asos', 'Qarshilik', 'Oʻxshatish', 'Chegara')]}, 'boglovchi': {'d3': [('Bogʻlovchilar qanday guruhlarga boʻlinadi?', 'Teng bogʻlovchilar va ergashtiruvchi bogʻlovchilar', 'Asliy va nisbiy bogʻlovchilar', 'Oʻtimli va oʻtimsiz bogʻlovchilar', 'Sodda va qoʻshma bogʻlovchilar'), ('«Va» bogʻlovchisi qaysi turga kiradi?', 'Biriktiruvchi (teng) bogʻlovchi', 'Ayiruvchi bogʻlovchi', 'Zid bogʻlovchi', 'Shart bogʻlovchisi'), ('«Lekin» bogʻlovchisi qaysi turga kiradi?', 'Zid (teng) bogʻlovchi', 'Biriktiruvchi bogʻlovchi', 'Shart bogʻlovchisi', 'Sabab bogʻlovchisi'), ('«Agar» bogʻlovchisi qaysi turga kiradi?', 'Shart (ergashtiruvchi) bogʻlovchi', 'Zid bogʻlovchi', 'Ayiruvchi bogʻlovchi', 'Biriktiruvchi bogʻlovchi'), ('«Chunki» bogʻlovchisi qaysi turga kiradi?', 'Sabab (ergashtiruvchi) bogʻlovchi', 'Zid bogʻlovchi', 'Shart bogʻlovchisi', 'Maqsad bogʻlovchisi'), ('«Yoki» bogʻlovchisi qaysi turga kiradi?', 'Ayiruvchi bogʻlovchi', 'Biriktiruvchi bogʻlovchi', 'Zid bogʻlovchi', 'Sabab bogʻlovchisi'), ('Uyushiq boʻlaklar orasidagi «va» dan oldin odatda vergul qoʻyiladimi?', 'Yoʻq, qoʻyilmaydi', 'Ha, har doim qoʻyiladi', 'Faqat savol gapda', 'Faqat undov gapda'), ('«Urindi, ammo eplay olmadi.» gapida «ammo» dan oldin qaysi belgi qoʻyilgan?', 'Vergul', 'Nuqta', 'Ikki nuqta', 'Tire')], 'd4': [('«Ham... ham» takrorlanuvchi bogʻlovchisi qaysi turga kiradi?', 'Biriktiruvchi bogʻlovchi', 'Ayiruvchi bogʻlovchi', 'Zid bogʻlovchi', 'Shart bogʻlovchisi'), ('«Goh... goh» takrorlanuvchi bogʻlovchisi qaysi turga kiradi?', 'Ayiruvchi bogʻlovchi', 'Biriktiruvchi bogʻlovchi', 'Zid bogʻlovchi', 'Natija bogʻlovchisi'), ('Bogʻlovchi gapda qanday vazifa bajaradi?', 'Soʻz yoki gap boʻlaklarini, gaplarni bogʻlaydi, oʻzi gap boʻlagi boʻlmaydi', 'Gap boʻlagi boʻladi', 'His-hayajon bildiradi', 'Soʻroq maʼnosini beradi'), ('«Garchi... boʻlsa-da» konstruksiyasi qaysi ergash gapni hosil qiladi?', 'Toʻsiqsiz (qarshilik) ergash gap', 'Shart ergash gap', 'Sabab ergash gap', 'Payt ergash gap'), ('«Yomgʻir yogʻdi, shuning uchun uyda qoldik.» gapida «shuning uchun» qanday vazifada?', 'Natija bildiruvchi bogʻlovchi vazifasida', 'Sabab bildiruvchi koʻmakchi vazifasida', 'Hol vazifasida', 'Ega vazifasida'), ('«Yaʼni» soʻzi qanday bogʻlovchi?', 'Izohlovchi bogʻlovchi', 'Zid bogʻlovchi', 'Shart bogʻlovchisi', 'Maqsad bogʻlovchisi'), ('«Toki» bogʻlovchisi qaysi ergash gapni bogʻlaydi?', 'Maqsad ergash gapni', 'Sabab ergash gapni', 'Shart ergash gapni', 'Payt ergash gapni')]}, 'yuklama': {'d3': [('Yuklama gapda gap boʻlagi boʻladimi?', 'Yoʻq, qoʻshimcha maʼno beradi', 'Ha, ega boʻladi', 'Ha, kesim boʻladi', 'Ha, hol boʻladi'), ('«Siz keldingizmi?» gapidagi -mi yuklamasi qanday maʼno beradi?', 'Soʻroq maʼnosi', 'Cheklash maʼnosi', 'Inkor maʼnosi', 'Kichraytirish maʼnosi'), ('«Kichkinagina bola» birikmasidagi -gina yuklamasi qanday maʼno beradi?', 'Kichraytirish-erkalash', 'Soʻroq', 'Taʼkid', 'Inkor'), ('«Menda faqat bitta qalam bor.» gapida «faqat» yuklamasi qanday maʼno beradi?', 'Cheklash', 'Kuchaytirish', 'Soʻroq', 'Qiyoslash'), ('«Hatto bolalar ham tushundi.» gapida «hatto» yuklamasi qanday maʼno beradi?', 'Kuchaytirish', 'Cheklash', 'Inkor', 'Soʻroq'), ('«Xuddi bahordek issiq.» gapida «xuddi» yuklamasi qanday maʼno beradi?', 'Qiyoslash', 'Cheklash', 'Soʻroq', 'Inkor')], 'd4': [('«Kelding-ku!» gapidagi -ku yuklamasi qanday maʼno beradi?', 'Taʼkid, ajablanish', 'Cheklash', 'Soʻroq', 'Kichraytirish'), ('«-mi» yuklamasi gapda qayerga qoʻshiladi?', 'Soʻroq qaratilgan soʻzga, odatda kesimga', 'Faqat gap boshiga', 'Faqat gap oxiriga', 'Faqat egaga'), ('«Nahotki u kelmasa?» gapidagi «nahotki» qanday maʼno beradi?', 'Soʻroq-taʼkid (ajablanish)', 'Cheklash', 'Qiyoslash', 'Kichraytirish'), ('«Ham» soʻzi qaysi turkumlarda uchrashi mumkin?', 'Yuklama va bogʻlovchi', 'Faqat ot', 'Faqat feʼl', 'Faqat son'), ('Yuklamalar qaysi vazifani bajaradi?', 'Soʻz yoki gapga qoʻshimcha maʼno qoʻshadi', 'Soʻzlarni kelishik bilan bogʻlaydi', 'Gaplarni teng bogʻlaydi', 'Tovushga taqlid qiladi'), ('«Bugunoq boraman» soʻzidagi -oq yuklamasi qanday maʼno beradi?', 'Kuchaytirish, aniqlik', 'Cheklash', 'Soʻroq', 'Kichraytirish')]}, 'undov': {'d3': [('Undov soʻzlar gap boʻlagi boʻladimi?', 'Yoʻq, gap boʻlagi boʻlmaydi', 'Ha, ega boʻladi', 'Ha, kesim boʻladi', 'Ha, aniqlovchi boʻladi'), ('«Oh, naqadar goʻzal!» gapida «oh» qanday undov soʻz?', 'His-hayajon undovi', 'Buyruq-xitob undovi', 'Nutq odobi undovi', 'Taqlid undovi'), ('«Hoy, toʻxta!» gapida «hoy» qanday undov soʻz?', 'Buyruq-xitob undovi', 'His-hayajon undovi', 'Nutq odobi undovi', 'Taqlid undovi'), ('«Rahmat» soʻzi qanday undov soʻz?', 'Nutq odobi undovi', 'His-hayajon undovi', 'Buyruq-xitob undovi', 'Taqlid undovi'), ('Undov soʻzdan keyin odatda qaysi tinish belgisi qoʻyiladi?', 'Undov belgisi yoki vergul', 'Nuqta', 'Ikki nuqta', 'Tire'), ('«Voy, qoʻlim ogʻridi!» gapida «voy» qanday maʼno bildiradi?', 'Ogʻriq, qoʻrquv', 'Maqtov', 'Rozilik', 'Chaqiriq')], 'd4': [('«Ali, bu yoqqa kel!» gapida «Ali» qaysi vazifada?', 'Undalma', 'Undov soʻz', 'Ega', 'Kirish soʻz'), ('Undov soʻz bilan undalma farqi qaysi?', 'Undov soʻz his-hayajon bildiradi, undalma murojaat qilinayotgan shaxsni bildiradi', 'Ular bir xil', 'Undalma his-hayajon bildiradi, undov soʻz shaxsni bildiradi', 'Ikkalasi ham gap boʻlagi'), ('«Barakalla, yigit!» gapida «barakalla» qanday maʼno bildiradi?', 'Maqtov, tahsin', 'Afsus', 'Qoʻrquv', 'Ogʻriq'), ('«Attang, kechikib qoldim!» gapida «attang» qanday maʼno bildiradi?', 'Afsus, pushaymon', 'Quvonch', 'Maqtov', 'Chaqiriq'), ('Undov soʻzlar gapda qanday sintaktik xususiyatga ega?', 'Gapning boshqa boʻlaklari bilan grammatik bogʻlanmaydi', 'Kesimga tobe boʻladi', 'Egaga tobe boʻladi', 'Aniqlovchi boʻladi')]}, 'modal': {'d3': [('Modal soʻzlar gapda qanday vazifa bajaradi?', 'Kirish soʻz vazifasini bajaradi', 'Ega vazifasini bajaradi', 'Kesim vazifasini bajaradi', 'Aniqlovchi vazifasini bajaradi'), ('«Albatta» modal soʻzi qanday maʼno bildiradi?', 'Ishonch, aniqlik', 'Gumon, taxmin', 'Afsus', 'Tartib'), ('«Ehtimol» modal soʻzi qanday maʼno bildiradi?', 'Gumon, taxmin', 'Ishonch', 'Afsus', 'Tartib'), ('«Afsuski» modal soʻzi qanday maʼno bildiradi?', 'Afsus, noxushlik', 'Ishonch', 'Gumon', 'Tartib'), ('«Birinchidan» modal soʻzi qanday maʼno bildiradi?', 'Fikrlar tartibi, ketma-ketligi', 'Ishonch', 'Afsus', 'Gumon'), ('Kirish soʻzlar gapdan qaysi tinish belgisi bilan ajratiladi?', 'Vergul bilan', 'Nuqta bilan', 'Ikki nuqta bilan', 'Qavs bilan')], 'd4': [('«Masalan» soʻzi qanday maʼno bildiradi?', 'Misol keltirish', 'Ishonch', 'Afsus', 'Taxmin'), ('«Xullas» modal soʻzi qanday maʼno bildiradi?', 'Xulosa', 'Gumon', 'Afsus', 'Misol'), ('Modal soʻz bilan ravish farqi qaysi?', 'Modal soʻz gap mazmuniga munosabat bildiradi, ravish harakat belgisini bildiradi', 'Ular bir xil', 'Ravish munosabat bildiradi, modal soʻz harakat belgisini', 'Ikkalasi ham otni aniqlaydi'), ('«Haqiqatan, u haq ekan.» gapida «haqiqatan» qanday vazifada?', 'Kirish soʻz', 'Ega', 'Kesim', 'Hol'), ('«Balki» soʻzining qaysi turkumlarga mansubligi mumkin?', 'Modal soʻz va bogʻlovchi', 'Faqat ot', 'Faqat feʼl', 'Faqat son'), ('«Mumkin», «kerak», «zarur» soʻzlari qaysi maʼnoni bildiradi?', 'Imkoniyat yoki zarurlik (modallik)', 'Tasdiq', 'Qoʻrquv', 'Tartib')]}, 'taqlid': {'d3': [('Taqlid soʻzlar maʼnosiga koʻra qaysi ikki guruhga boʻlinadi?', 'Tovushga va holat (obraz)ga taqlid', 'Asliy va nisbiy', 'Oʻtimli va oʻtimsiz', 'Sanoq va tartib'), ('«Taq-taq» qaysi taqlid soʻz guruhiga kiradi?', 'Tovushga taqlid', 'Holat (obraz)ga taqlid', 'Rangga taqlid', 'Maʼnoga taqlid'), ('«Yaltir-yultur» qaysi taqlid soʻz guruhiga kiradi?', 'Holat (obraz)ga taqlid', 'Tovushga taqlid', 'Hidga taqlid', 'Mazaga taqlid'), ('«Shitir-shitir» qaysi taqlid soʻz guruhiga kiradi?', 'Tovushga taqlid', 'Holat (obraz)ga taqlid', 'Harakat nomi', 'Sifat'), ('Taqlid soʻzlar gapda koʻpincha qanday vazifa bajaradi?', 'Hol (tarz holi) yoki kesim boʻlib keladi', 'Faqat ega', 'Faqat aniqlovchi', 'Faqat undalma')], 'd4': [('Taqlid soʻzdan feʼl yasovchi qoʻshimcha qaysi?', '-la (shitirlamoq)', '-chi', '-lik', '-siz'), ('«Gʻijirlamoq» feʼli qanday yoʻl bilan yasalgan?', 'Taqlid soʻzdan -la qoʻshimchasi bilan', 'Sifatdan -la bilan', 'Otdan -chi bilan', 'Sondan -ta bilan'), ('Badiiy matnda taqlid soʻzlar nima uchun qoʻllanadi?', 'Tasvirni jonli va taʼsirchan qilish uchun', 'Qoidalarni belgilash uchun', 'Hisob-kitob uchun', 'Rasmiy hujjat yozish uchun'), ('«Miyov-miyov» taqlid soʻzi nimaga taqlid?', 'Mushukning ovoziga', 'Itning ovoziga', 'Qargʻaning ovoziga', 'Suv oqishiga'), ('«Vov-vov» taqlid soʻzi nimaga taqlid?', 'Itning ovoziga', 'Mushukning ovoziga', 'Qargʻaning ovoziga', 'Eshik gʻijirlashiga')]}}
PRO_GEN = {'d3': [('«Ogʻiz — ogʻzi», «oʻgʻil — oʻgʻli» juftliklarida qanday fonetik hodisa roʻy bergan?', 'Unli tovush tushishi', 'Unli tovush ortishi', 'Undosh tovush almashishi', 'Boʻgʻin qoʻshilishi'), ('«Qishloq — qishlogʻim», «ketmoq — ketgan» juftliklaridan birinchisida qanday fonetik hodisa kuzatiladi?', 'Undosh almashishi (q — gʻ)', 'Unli tushishi', 'Undosh ortishi', 'Boʻgʻin tushishi'), ('«Oʻqituvchilarimizga» soʻzi nechta boʻgʻindan iborat?', '8', '6', '7', '9'), ('Lablangan unlilar qatorini toping.', 'u, o, oʻ', 'i, e, a', 'i, u, e', 'a, i, oʻ'), ('Faqat jarangsiz undoshlardan iborat qatorni toping.', 'p, t, q, sh', 'b, t, q, sh', 'p, d, q, sh', 'p, t, g, sh'), ('Sonor undoshlar qatorini toping.', 'm, n, l, r', 'p, t, k, q', 'b, d, g, z', 's, sh, f, x'), ('Shakl yasovchi qoʻshimchani toping.', '-ning', '-chi', '-lik', '-kor'), ('«Kitoblarimizdan» soʻzida qoʻshimchalar qanday tartibda kelgan?', 'Koʻplik — egalik — kelishik', 'Egalik — koʻplik — kelishik', 'Kelishik — koʻplik — egalik', 'Koʻplik — kelishik — egalik'), ('Quyidagilardan qaysi biri tub soʻz?', 'Qalam', 'Yozuvchi', 'Gulzor', 'Oqqush'), ('«OʻzMU», «BMT» kabi soʻzlar qaysi usulda hosil boʻlgan?', 'Abbreviatsiya (qisqartma)', 'Qoʻshish', 'Juftlash', 'Takrorlash'), ('«Qop-qora», «yam-yashil» shakllari sifatning qaysi darajasiga kiradi?', 'Orttirma daraja', 'Qiyosiy daraja', 'Ozaytirma daraja', 'Oddiy daraja'), ('Quyidagilardan qaysi biri ravishdosh qoʻshimchasi?', '-ib', '-gan', '-ayotgan', '-di'), ('Quyidagi shakllardan qaysi biri kelasi zamon sifatdoshi qoʻshimchasi?', '-ajak', '-gan', '-ayotgan', '-moqda'), ('«Yozdirdi» feʼli qaysi nisbatda?', 'Orttirma nisbat', 'Oʻzlik nisbat', 'Majhul nisbat', 'Birgalik nisbat'), ('«Yuvindi» feʼli qaysi nisbatda?', 'Oʻzlik nisbat', 'Orttirma nisbat', 'Majhul nisbat', 'Birgalik nisbat'), ('«Tanishdi» feʼli qaysi nisbatga kiradi?', 'Birgalik nisbat', 'Oʻzlik nisbat', 'Orttirma nisbat', 'Majhul nisbat'), ('«Xat yozildi» gapida «yozildi» feʼli qaysi nisbatda?', 'Majhul nisbat', 'Orttirma nisbat', 'Oʻzlik nisbat', 'Birgalik nisbat'), ('Umumlashtiruvchi soʻz uyushiq boʻlaklardan oldin kelsa, undan keyin qaysi tinish belgisi qoʻyiladi?', 'Ikki nuqta', 'Nuqtali vergul', 'Tire', 'Vergul'), ('«Men kitobni oʻqidim.» gapida «kitobni» qaysi gap boʻlagi?', 'Vositasiz toʻldiruvchi', 'Vositali toʻldiruvchi', 'Aniqlovchi', 'Hol'), ('«Alining kitobi» birikmasida «Alining» soʻzi qaysi gap boʻlagi vazifasida?', 'Qaratqich aniqlovchi', 'Sifatlovchi aniqlovchi', 'Izohlovchi', 'Hol'), ('«Shoir Navoiy» birikmasida «shoir» soʻzi qaysi boʻlak vazifasida kelgan?', 'Izohlovchi', 'Sifatlovchi', 'Qaratqich aniqlovchi', 'Toʻldiruvchi'), ('«Bu uy goʻzal.» gapida kesim qanday turga kiradi?', 'Otli kesim', 'Feʼlli kesim', 'Sodda ega', 'Aniqlovchi'), ('«Yurish — sogʻliq garovi.» gapida ega qaysi shakldagi soʻz bilan ifodalangan?', 'Harakat nomi', 'Sifatdosh', 'Ravishdosh', 'Buyruq mayli'), ('Koʻchirma gap muallif gapidan oldin kelganda, qoʻshtirnoqdan keyin qanday tinish belgilari qoʻyiladi?', 'Vergul va tire', 'Ikki nuqta', 'Faqat nuqta', 'Nuqtali vergul'), ('«Men shuni bilamanki, u kelmaydi.» gapida ergash gap qaysi turga kiradi?', 'Toʻldiruvchi ergash gap', 'Ega ergash gap', 'Aniqlovchi ergash gap', 'Kesim ergash gap')], 'd4': [('«Oltin kuz» birikmasida «oltin» soʻzining koʻchma maʼnosi qaysi hodisaga asoslangan?', 'Metafora (oʻxshashlik)', 'Metonimiya (bogʻliqlik)', 'Evfemizm', 'Litota'), ('«Butun auditoriya qarsak chaldi» gapida «auditoriya» soʻzi qanday koʻchgan?', 'Metonimiya (joy — odamlar)', 'Metafora', 'Gradatsiya', 'Inversiya'), ('«Dunyodan oʻtdi» ifodasi qanday uslubiy hodisa?', 'Evfemizm', 'Disfemizm', 'Arxaizm', 'Neologizm'), ('Quyidagi juftliklardan qaysi biri omonim?', 'oʻt (alanga) — oʻt (oʻtmoq)', 'bosh (aʼzo) — bosh (rahbar)', 'koʻz (aʼzo) — koʻz (ignaning koʻzi)', 'oyoq (aʼzo) — oyoq (stol oyogʻi)'), ('«Tarif» va «taʼrif» soʻzlari qaysi lugʻaviy munosabatda?', 'Paronim', 'Omonim', 'Sinonim', 'Antonim'), ('Isteʼmoldan chiqqan, chunki ifodalagan narsasi yoʻqolgan soʻzlar qanday ataladi?', 'Historizm', 'Arxaizm', 'Neologizm', 'Dialektizm'), ('Narsa saqlanib qolgan, lekin uni bildiruvchi soʻz eskirgan boʻlsa, bunday soʻz nima deyiladi?', 'Arxaizm', 'Historizm', 'Neologizm', 'Jargon'), ('Yangi paydo boʻlgan narsa-hodisani ifodalovchi soʻz qanday ataladi?', 'Neologizm', 'Arxaizm', 'Historizm', 'Dialektizm'), ('Faqat muayyan hududda ishlatiladigan soʻz qanday ataladi?', 'Dialektizm', 'Jargon', 'Termin', 'Professionalizm'), ('Qaysi soʻz fors-tojik tilidan oʻzlashgan?', 'Dehqon', 'Kitob', 'Samolyot', 'Pichoq'), ('«Qoʻli egri» frazeologizmining maʼnosi qaysi?', 'Oʻgʻrilik qiladigan', 'Ishyoqmas', 'Gap tashuvchi', 'Baxil'), ('«Bahor dalalarni uygʻotdi» jumlasidagi badiiy vosita nima?', 'Jonlantirish (shaxslantirish)', 'Muboʻlagʻa', 'Kinoya', 'Oʻxshatish'), ('«Chumoli fil boʻlib koʻrindi» ifodasi qaysi badiiy vositaga misol?', 'Muboʻlagʻa', 'Litota', 'Jonlantirish', 'Antiteza'), ('«Barakalla, ishyoqmas!» deganda hajviy maʼno qaysi vosita orqali ifodalangan?', 'Kinoya', 'Oʻxshatish', 'Sifatlash', 'Inversiya'), ('«Keldi bahor.» gapida qaysi uslubiy hodisa kuzatiladi?', 'Inversiya', 'Gradatsiya', 'Antiteza', 'Anafora'), ('Ilmiy uslubning asosiy belgisi qaysi?', 'Terminlarga boyligi va aniqligi', 'Sheʼriy obrazlilik', 'Soʻzlashuv unsurlarining koʻpligi', 'Hissiy boʻyoqdorlikning kuchliligi'), ('Ijtimoiy-siyosiy mavzularni ommaga yetkazuvchi, taʼsirchan uslub qaysi?', 'Publitsistik uslub', 'Ilmiy uslub', 'Rasmiy uslub', 'Soʻzlashuv uslubi'), ('Ish qogʻozlari, buyruq va arizalar qaysi uslubga xos?', 'Rasmiy uslub', 'Badiiy uslub', 'Publitsistik uslub', 'Ilmiy-ommabop uslub'), ('Gap ichida sinonim soʻzlarning oʻrinsiz takrorlanishi qanday nuqson sanaladi?', 'Tavtologiya', 'Inversiya', 'Gradatsiya', 'Antiteza'), ('«Yurak» soʻzining «jasur odam» maʼnosida qoʻllanishi qanday maʼno turiga kiradi?', 'Koʻchma maʼno', 'Bevosita maʼno', 'Terminologik maʼno', 'Lugʻaviy omonimlik'), ('Soʻzning bevosita predmetga bogʻlanib, birinchi navbatda eslanadigan maʼnosi nima deyiladi?', 'Asosiy (toʻgʻri) maʼno', 'Koʻchma maʼno', 'Frazeologik maʼno', 'Qoʻshimcha maʼno'), ('Soʻz maʼnosining kengayishi, torayishi va koʻchishi qaysi tilshunoslik boʻlimida oʻrganiladi?', 'Semasiologiya (soʻz maʼnosi haqidagi taʼlimot)', 'Fonetika', 'Grafika', 'Orfografiya'), ('Soʻzlarning tarkibiy qismlarini oʻrganuvchi boʻlim qaysi?', 'Morfemika', 'Sintaksis', 'Leksikografiya', 'Orfoepiya'), ('Toʻgʻri talaffuz qoidalarini oʻrganuvchi boʻlim qaysi?', 'Orfoepiya', 'Orfografiya', 'Grafika', 'Leksikologiya'), ('Soʻzlarning yozilish qoidalarini oʻrganuvchi boʻlim qaysi?', 'Orfografiya', 'Orfoepiya', 'Fonetika', 'Morfologiya'), ('Lugʻat tuzish nazariyasi va amaliyoti qaysi boʻlimda oʻrganiladi?', 'Leksikografiya', 'Etimologiya', 'Frazeologiya', 'Dialektologiya'), ('Soʻzlarning kelib chiqishini oʻrganuvchi boʻlim qaysi?', 'Etimologiya', 'Leksikografiya', 'Semasiologiya', 'Morfemika'), ('Gap boʻlaklari oʻrtasidagi grammatik munosabat va soʻzlarning bogʻlanish usullarini oʻrganuvchi boʻlim qaysi?', 'Sintaksis', 'Morfologiya', 'Fonetika', 'Leksikologiya')]}
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
    def collect(rng, gens, size=POOL_SIZE):
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
        result[k]["d1"] = collect(rg, [
            f_extra(rg, k, "d1"),
            f_which_is(rg, k, 1), f_word_to_label(rg, k), f_meaning_far(rg, k),
            f_not_is(rg, k, False, 80)])
        rg = r("d2")
        result[k]["d2"] = collect(rg, [
            f_extra(rg, k, "d2"),
            f_context(rg, k), f_meaning_same(rg, k), f_def_label(rg, k), f_count(rg, k, False),
            f_which_is(rg, k, 2, True), f_not_is(rg, k, False, 80), f_row(rg, k, False, 80)])
        rg = r("d3")
        result[k]["d3"] = collect(rg, [
            deepen(f_extra(rg, k, "d3")), deepen(f_context_near(rg, k), 40),
            f_meaning_of(rg, k), f_type(rg, k), f_type_ctx(rg, k), deepen(f_form(rg, k)),
            f_count(rg, k, True), f_row(rg, k, False, 160), f_not_is(rg, k, True, 100),
            deepen(f_son_form(rg, k)), deepen(f_olmosh_form(rg, k)), deepen(f_derive(rg, k)),
            f_pair(rg, k, False)])
        rg = r("d4")
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

TOKEN = (os.getenv("BOT_TOKEN") or "8679356904:AAHoxrc1J8BQzWSna-6LobAS_yd82G_ckRo").strip()
if ":" not in TOKEN:
    sys.exit("BOT_TOKEN noto'g'ri yoki yo'q. U shunday ko'rinadi: 123456789:AAH...\n"
             "Yozing: export BOT_TOKEN=\"butun_token\"")

URL = f"https://api.telegram.org/bot{TOKEN}/"

# --- Admin va roʻyxatdan oʻtish ---
try:
    ADMIN_ID = int((os.getenv("ADMIN_ID") or "7617175325").strip() or 0)
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
    pros = [q for q in pool if q.get("pro")]
    random.shuffle(pros)
    pros = pros[:QUIZ_SIZE // 2]
    pool = [q for q in pool if not any(q is p for p in pros)]
    groups = {}
    for q in pool:
        groups.setdefault(q.get("kind", 0), []).append(q)
    for g in groups.values():
        random.shuffle(g)
    order = list(groups)
    random.shuffle(order)
    chosen = list(pros)
    while len(chosen) < QUIZ_SIZE and any(groups.values()):
        for kd in order:
            if groups[kd] and len(chosen) < QUIZ_SIZE:
                chosen.append(groups[kd].pop())
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
                      "uchun B, B+, A, A+ darajalarida 150 tagacha, yarmi professor darajasidagi savol; har safar 10 tasi tasodifiy beriladi. Har bir savolga 30 soniya beriladi.\n"
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
                      "Har bir darajada 150 tagacha, yarmi professor darajasidagi savol bor, 10 tasi tasodifiy beriladi.", tur_levels_kb())
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
             f"📝 Testlar: jami {total_questions()} ta savol (12 soʻz turkumi × B, B+, A, A+ × 150 + umumiy)\n"
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
