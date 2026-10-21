# Ona tili botining ma'lumotlari: testlar va lug'at
import random

LEVELS = {
    "alifbo": {
        "title": "🔤 1-daraja: Alifbo",
        "questions": [
            {"q": "Oʻzbek alifbosida nechta harf bor?",
             "o": ["26", "29", "32", "35"], "a": 1},
            {"q": "Oʻzbek tilida nechta unli harf bor?",
             "o": ["5", "6", "7", "8"], "a": 1},
            {"q": "Quyidagilardan qaysi biri unli harf?",
             "o": ["k", "m", "u", "s"], "a": 2},
            {"q": "Quyidagilardan qaysi biri undosh harf?",
             "o": ["a", "e", "o", "b"], "a": 3},
            {"q": "Qaysi harflar birikmasi alifboda alohida harf hisoblanadi?",
             "o": ["Sh", "Tr", "Kl", "Pr"], "a": 0},
        ],
    },
    "bogin": {
        "title": "✂️ 2-daraja: Boʻgʻin",
        "questions": [
            {"q": "«Olma» soʻzida nechta boʻgʻin bor?",
             "o": ["1", "2", "3", "4"], "a": 1},
            {"q": "«Kitob» soʻzida nechta boʻgʻin bor?",
             "o": ["1", "2", "3", "4"], "a": 1},
            {"q": "«Maktab» soʻzi qanday boʻgʻinlanadi?",
             "o": ["mak-tab", "ma-ktab", "m-ak-tab", "maktab"], "a": 0},
            {"q": "«Oʻqituvchi» soʻzida nechta boʻgʻin bor?",
             "o": ["2", "3", "4", "5"], "a": 2},
            {"q": "Boʻgʻin nechta unlidan iborat boʻladi?",
             "o": ["Hech qanday", "Bitta", "Ikkita", "Uchta"], "a": 1},
        ],
    },
    "turkum": {
        "title": "📚 3-daraja: Soʻz turkumlari",
        "questions": [
            {"q": "«Kitob» qaysi soʻz turkumiga kiradi?",
             "o": ["Ot", "Sifat", "Feʼl", "Son"], "a": 0},
            {"q": "«Chiroyli» qaysi soʻz turkumiga kiradi?",
             "o": ["Ot", "Sifat", "Feʼl", "Olmosh"], "a": 1},
            {"q": "«Yozmoq» qaysi soʻz turkumiga kiradi?",
             "o": ["Ot", "Sifat", "Feʼl", "Son"], "a": 2},
            {"q": "«Uch» qaysi soʻz turkumiga kiradi?",
             "o": ["Ot", "Son", "Feʼl", "Sifat"], "a": 1},
            {"q": "«Men» qaysi soʻz turkumiga kiradi?",
             "o": ["Son", "Sifat", "Olmosh", "Feʼl"], "a": 2},
            {"q": "Ot qanday soʻroqqa javob boʻladi?",
             "o": ["Kim? Nima?", "Qanday?", "Nima qildi?", "Necha?"], "a": 0},
        ],
    },
    "imlo": {
        "title": "✍️ 4-daraja: Imlo",
        "questions": [
            {"q": "Qaysi soʻz toʻgʻri yozilgan?",
             "o": ["Oquvchi", "Oʻquvchi", "Oʻkuvchi", "Okuvchi"], "a": 1},
            {"q": "Qaysi soʻz toʻgʻri yozilgan?",
             "o": ["Goya", "Gooya", "Gʻoya", "Gaya"], "a": 2},
            {"q": "Qaysi soʻz toʻgʻri yozilgan?",
             "o": ["Mano", "Maʼno", "Maano", "Manoo"], "a": 1},
            {"q": "Qaysi soʻz toʻgʻri yozilgan?",
             "o": ["Qishloq", "Qishlok", "Kishloq", "Qishloqq"], "a": 0},
            {"q": "«Kitob» soʻzining koʻplik shakli qaysi?",
             "o": ["Kitoblar", "Kitoblarlar", "Kitobtar", "Kitoblari"], "a": 0},
        ],
    },
}

def _q(text, right, *wrong):
    """Savol yaratadi; variantlar har ishga tushganda aralashtiriladi."""
    opts = [right, *wrong]
    random.shuffle(opts)
    return {"q": text, "o": opts, "a": opts.index(right)}


# ---- Mavjud darajalarga qo'shimcha savollar ----
LEVELS["alifbo"]["questions"] += [
    _q("Qaysi harf oʻzbek lotin alifbosida yoʻq?", "W", "Q", "X", "J"),
    _q("Oʻzbek alifbosining birinchi harfi qaysi?", "A", "B", "D", "E"),
    _q("«Ch» harflar birikmasi nechta tovushni bildiradi?", "1", "2", "3", "4"),
    _q("«Oʻzbekiston» soʻzida nechta unli harf bor?", "4", "3", "5", "6"),
    _q("«Kitob» soʻzida nechta undosh harf bor?", "3", "2", "4", "5"),
    _q("Quyidagilardan qaysi biri undosh harf?", "q", "a", "i", "u"),
    _q("Quyidagilardan qaysi biri unli harf?", "e", "d", "r", "t"),
    _q("«Gʻ» harfi qaysi guruhga kiradi?", "Undosh", "Unli", "Ikkalasi ham", "Hech qaysi"),
]

LEVELS["bogin"]["questions"] += [
    _q("«Dars» soʻzida nechta boʻgʻin bor?", "1", "2", "3", "4"),
    _q("«Daftar» soʻzi qanday boʻgʻinlanadi?", "daf-tar", "da-ftar", "d-af-tar", "dafta-r"),
    _q("«Qalam» soʻzida nechta boʻgʻin bor?", "2", "1", "3", "4"),
    _q("«Oʻzbekiston» soʻzida nechta boʻgʻin bor?", "4", "3", "5", "6"),
    _q("«Ona» soʻzi qanday boʻgʻinlanadi?", "o-na", "on-a", "ona", "o-n-a"),
    _q("«Bolalar» soʻzida nechta boʻgʻin bor?", "3", "2", "4", "5"),
    _q("«Maktabda» soʻzida nechta boʻgʻin bor?", "3", "2", "4", "1"),
    _q("Boʻgʻin soni nimaga qarab aniqlanadi?", "Unlilar soniga", "Undoshlar soniga",
       "Harflar soniga", "Soʻz uzunligiga"),
    _q("«Kelajak» soʻzi qanday boʻgʻinlanadi?", "ke-la-jak", "kel-a-jak", "ke-laj-ak", "kela-jak"),
    _q("«Ustoz» soʻzi qanday boʻgʻinlanadi?", "us-toz", "u-stoz", "ust-oz", "ustoz"),
]

LEVELS["turkum"]["questions"] += [
    _q("«Yaxshi» qaysi soʻz turkumiga kiradi?", "Sifat", "Ot", "Feʼl", "Son"),
    _q("«Oʻqiyman» qaysi soʻz turkumiga kiradi?", "Feʼl", "Ot", "Sifat", "Olmosh"),
    _q("«Besh» qaysi soʻz turkumiga kiradi?", "Son", "Ot", "Feʼl", "Sifat"),
    _q("«Sen» qaysi soʻz turkumiga kiradi?", "Olmosh", "Son", "Ot", "Sifat"),
    _q("«Daryo» qaysi soʻz turkumiga kiradi?", "Ot", "Sifat", "Feʼl", "Son"),
    _q("«Kim?» soʻrogʻiga qaysi soʻz javob boʻladi?", "Oʻqituvchi", "Katta", "Yozdi", "Uch"),
    _q("«Qanday?» soʻrogʻiga qaysi soʻz javob boʻladi?", "Baland", "Daraxt", "Oʻqidi", "Sakkiz"),
    _q("«Nima qildi?» soʻrogʻiga qaysi soʻz javob boʻladi?", "Yozdi", "Kitob", "Chiroyli", "Toʻrt"),
    _q("«Necha?» soʻrogʻiga qaysi soʻz javob boʻladi?", "Yetti", "Qalam", "Aytdi", "Yaxshi"),
    _q("Quyidagilardan qaysi biri ot?", "Gul", "Oʻqidi", "Qizil", "Ikki"),
]

LEVELS["imlo"]["questions"] += [
    _q("Qaysi soʻz toʻgʻri yozilgan?", "Moʻjiza", "Mojiza", "Mojzia", "Moʻziza"),
    _q("Qaysi soʻz toʻgʻri yozilgan?", "Toʻgʻri", "Togri", "Toʻgri", "Tugʻri"),
    _q("Qaysi soʻz toʻgʻri yozilgan?", "Maktab", "Maqtab", "Maktap", "Makhtab"),
    _q("Qaysi soʻz toʻgʻri yozilgan?", "Gʻalaba", "Galaba", "Ghalaba", "Gʻalabba"),
    _q("Qaysi soʻz toʻgʻri yozilgan?", "Shahar", "Shaxar", "Shehar", "Shahhar"),
    _q("Qaysi soʻz toʻgʻri yozilgan?", "Hayot", "Xayot", "Hayyot", "Hayoot"),
    _q("Qaysi soʻz toʻgʻri yozilgan?", "Eʼlon", "Elon", "Eelon", "Eʼlonn"),
    _q("«Bola» soʻzining koʻplik shakli qaysi?", "Bolalar", "Bolalarlar", "Bolatar", "Bolaler"),
]

# ---- Yangi darajalar ----
LEVELS["tinish"] = {
    "title": "✏️ 5-daraja: Tinish belgilari",
    "questions": [
        _q("Darak gap oxiriga qaysi belgi qoʻyiladi?", "Nuqta", "Soʻroq belgisi", "Undov belgisi", "Ikki nuqta"),
        _q("Soʻroq gap oxiriga qaysi belgi qoʻyiladi?", "Soʻroq belgisi", "Nuqta", "Vergul", "Tire"),
        _q("Hayajonli, his-tuygʻuli gap oxiriga qaysi belgi qoʻyiladi?", "Undov belgisi", "Nuqta", "Vergul", "Qavs"),
        _q("Bir xil boʻlaklar (sanash) orasiga qaysi belgi qoʻyiladi?", "Vergul", "Nuqta", "Tire", "Undov belgisi"),
        _q("«?» belgisi qanday ataladi?", "Soʻroq belgisi", "Undov belgisi", "Nuqta", "Vergul"),
        _q("«!» belgisi qanday ataladi?", "Undov belgisi", "Soʻroq belgisi", "Ikki nuqta", "Tire"),
        _q("«,» belgisi qanday ataladi?", "Vergul", "Nuqta", "Ikki nuqta", "Tire"),
        _q("«:» belgisi qanday ataladi?", "Ikki nuqta", "Nuqta", "Vergul", "Undov belgisi"),
        _q("Gap qanday harf bilan boshlanadi?", "Bosh harf", "Kichik harf", "Raqam", "Tinish belgisi"),
    ],
}

LEVELS["sinonim"] = {
    "title": "🔀 6-daraja: Sinonim va antonim",
    "questions": [
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
        _q("«Toʻgʻri» soʻzining antonimi qaysi?", "Notoʻgʻri", "Rost", "Aniq", "Mukammal"),
    ],
}

LEVELS["gap"] = {
    "title": "🧩 7-daraja: Gap boʻlaklari",
    "questions": [
        _q("Ish-harakatni bildirib, gapni tugallovchi boʻlak qaysi?", "Kesim", "Ega", "Aniqlovchi", "Hol"),
        _q("Kim? nima? soʻrogʻiga javob boʻlib, harakat egasini bildiruvchi boʻlak qaysi?", "Ega", "Kesim", "Toʻldiruvchi", "Hol"),
        _q("«Ali kitob oʻqidi.» gapida ega qaysi?", "Ali", "kitob", "oʻqidi", "Gapda ega yoʻq"),
        _q("«Ali kitob oʻqidi.» gapida kesim qaysi?", "oʻqidi", "Ali", "kitob", "Gapda kesim yoʻq"),
        _q("«Bahor keldi.» gapida ega qaysi?", "Bahor", "keldi", "Ikkalasi ham", "Hech qaysi"),
        _q("Gapning eng muhim ikki boʻlagi qaysilar?", "Ega va kesim", "Aniqlovchi va hol",
           "Toʻldiruvchi va hol", "Ega va aniqlovchi"),
        _q("«Bolalar maktabga bordi.» gapida nechta soʻz bor?", "3", "2", "4", "5"),
        _q("«Men kitob oʻqiyman.» gapida kesim qaysi?", "oʻqiyman", "Men", "kitob", "Hammasi"),
        _q("«Quyosh chiqdi.» gapida kesim qaysi?", "chiqdi", "Quyosh", "Ikkalasi ham", "Hech qaysi"),
    ],
}

LEVELS["kelishik"] = {
    "title": "🔗 8-daraja: Kelishiklar",
    "questions": [
        _q("Oʻzbek tilida nechta kelishik bor?", "6", "4", "5", "7"),
        _q("«Kitobni» soʻzi qaysi kelishikda?", "Tushum", "Bosh", "Qaratqich", "Chiqish"),
        _q("«Maktabga» soʻzi qaysi kelishikda?", "Joʻnalish", "Oʻrin-payt", "Tushum", "Bosh"),
        _q("«Uyda» soʻzi qaysi kelishikda?", "Oʻrin-payt", "Joʻnalish", "Chiqish", "Qaratqich"),
        _q("«Shahardan» soʻzi qaysi kelishikda?", "Chiqish", "Oʻrin-payt", "Tushum", "Bosh"),
        _q("«Onamning» soʻzi qaysi kelishikda?", "Qaratqich", "Tushum", "Joʻnalish", "Bosh"),
        _q("Bosh kelishik qaysi soʻroqlarga javob beradi?", "Kim? Nima?", "Kimni? Nimani?",
           "Kimga? Nimaga?", "Kimning? Nimaning?"),
        _q("Joʻnalish kelishigining qoʻshimchasi qaysi?", "-ga", "-ni", "-da", "-dan"),
        _q("Chiqish kelishigining qoʻshimchasi qaysi?", "-dan", "-ga", "-ni", "-ning"),
        _q("Oʻrin-payt kelishigining qoʻshimchasi qaysi?", "-da", "-dan", "-ga", "-ning"),
        _q("Tushum kelishigining qoʻshimchasi qaysi?", "-ni", "-ning", "-da", "-ga"),
        _q("Qaratqich kelishigining qoʻshimchasi qaysi?", "-ning", "-ni", "-dan", "-ga"),
    ],
}

# (soʻz, turkumi, maʼnosi, misol)
WORDS = [
    ("ona", "ot", "Farzandni dunyoga keltirgan ayol.", "Onam menga ertak aytib berdi."),
    ("kitob", "ot", "Bosilgan, varaqlardan iborat oʻqiladigan asar.", "Men yangi kitob oʻqiyapman."),
    ("maktab", "ot", "Bolalar taʼlim oladigan joy.", "Ertalab maktabga boraman."),
    ("oʻqituvchi", "ot", "Oʻquvchilarga bilim beradigan kishi.", "Oʻqituvchimiz juda mehribon."),
    ("oʻquvchi", "ot", "Maktabda taʼlim oladigan bola.", "Oʻquvchilar sinfga kirishdi."),
    ("alifbo", "ot", "Tilning yozuvida qoʻllanadigan harflar tizimi.", "Oʻzbek alifbosi 29 harfdan iborat."),
    ("harf", "ot", "Yozuvda tovushni ifodalovchi belgi.", "A — alifboning birinchi harfi."),
    ("tovush", "ot", "Nutqda aytiladigan eng kichik birlik.", "Unli va undosh tovushlar bor."),
    ("unli", "ot", "Havo toʻsiqsiz chiqib aytiladigan tovush.", "A, e, i, o, u, oʻ — unlilar."),
    ("undosh", "ot", "Havo toʻsiqqa uchrab aytiladigan tovush.", "B, d, k, m — undoshlar."),
    ("boʻgʻin", "ot", "Soʻzning bir ovoz bilan aytiladigan boʻlagi.", "Ona soʻzi ikki boʻgʻinli: o-na."),
    ("soʻz", "ot", "Biror narsa yoki tushunchani bildiruvchi til birligi.", "Bu soʻzning maʼnosi nima?"),
    ("gap", "ot", "Tugal fikr bildiruvchi soʻz yoki soʻzlar birikmasi.", "Gap nuqta bilan tugaydi."),
    ("ot", "ot", "Kim? nima? soʻroqlariga javob boʻladigan soʻz turkumi.", "Kitob, maktab, ona — otlar."),
    ("sifat", "ot", "Narsaning belgisini bildiradigan soʻz turkumi.", "Chiroyli, katta — sifatlar."),
    ("son", "ot", "Narsaning miqdori yoki tartibini bildiradigan soʻz turkumi.", "Uch, besh, oʻninchi — sonlar."),
    ("olmosh", "ot", "Ot, sifat yoki son oʻrnida qoʻllanadigan soʻz.", "Men, sen, u — olmoshlar."),
    ("feʼl", "ot", "Ish-harakat yoki holatni bildiradigan soʻz turkumi.", "Yozmoq, oʻqimoq — feʼllar."),
    ("sinonim", "ot", "Maʼnosi bir-biriga yaqin soʻzlar.", "Chiroyli va goʻzal — sinonimlar."),
    ("antonim", "ot", "Maʼnosi bir-biriga qarama-qarshi soʻzlar.", "Katta va kichik — antonimlar."),
    ("imlo", "ot", "Soʻzlarni toʻgʻri yozish qoidalari.", "Imlo qoidalarini bilish kerak."),
    ("soʻroq", "ot", "Savol bildirish uchun ishlatiladigan soʻz yoki gap.", "Kim? nima? — soʻroqlar."),
    ("nuqta", "ot", "Darak gap oxirida qoʻyiladigan tinish belgisi.", "Gap oxiriga nuqta qoʻyamiz."),
    ("vergul", "ot", "Gap boʻlaklarini ajratish uchun qoʻyiladigan tinish belgisi.", "Olma, nok, uzum sotib oldim."),
    ("goʻzal", "sifat", "Koʻrinishi yoqimli, chiroyli.", "Bu juda goʻzal joy."),
    ("katta", "sifat", "Hajmi yoki yoshi jihatidan yirik.", "Katta uyda yashaymiz."),
    ("kichik", "sifat", "Hajmi yoki yoshi jihatidan mayda.", "Kichik ukam bor."),
    ("yozmoq", "feʼl", "Qalam yoki klaviatura bilan harf va soʻzlarni tushirmoq.", "Men xat yozaman."),
    ("oʻqimoq", "feʼl", "Yozilganni anglab aytmoq yoki ichida mutolaa qilmoq; oʻrganmoq.", "U kitob oʻqiyapti."),
    ("gapirmoq", "feʼl", "Soʻzlamoq, nutq aytmoq.", "U ravon gapiradi."),
]
