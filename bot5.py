# ============================================================
# bot5.py  —  O'zbek tili lug'ati (so'z turkumlari bo'yicha)
# Telegram bot uchun mo'ljallangan
# ============================================================

lugat = {
    "ot": {
        "nomi": "Ot",
        "izoh": "Predmet, shaxs, joy, holat, tushuncha nomini bildiruvchi so'z turkumi.",
        "sozlar": {
            "kitob": "O'qish uchun mo'ljallangan yozma asar.",
            "odam": "Inson, shaxs.",
            "uy": "Yashash uchun mo'ljallangan bino.",
            "baxt": "Xursandchilik, omad, farovonlik holati.",
            "Toshkent": "O'zbekiston poytaxti.",
            "daraxt": "Yer ustida o'sadigan, tanasi va shoxlari bo'lgan o'simlik.",
            "suv": "Hayot uchun zarur bo'lgan suyuqlik.",
            "maktab": "Ta'lim beriladigan muassasa.",
            "do'st": "Yaqin, ishonchli kishi.",
            "vaqt": "Hodisalar ketma-ketligi o'lchovi.",
            "yurak": "Qon aylanishini ta'minlovchi organ yoki his-tuyg'u markazi.",
            "osmon": "Yer ustidagi ko'k maydon.",
            "gul": "O'simlikning gullash organlari yoki chiroyli o'simlik.",
            "bolalik": "Bolalik davri.",
            "vatan": "Tug'ilib o'sgan yurt."
        }
    },

    "sifat": {
        "nomi": "Sifat",
        "izoh": "Otning belgisini, sifatini, holatini bildiruvchi so'z turkumi.",
        "sozlar": {
            "chiroyli": "Ko'rkam, go'zal.",
            "katta": "Hajmi yoki miqdori yuqori.",
            "kichik": "Hajmi yoki miqdori past.",
            "qizil": "Qizil rangdagi.",
            "aqlli": "Aql-zakovatli, o'ychan.",
            "yaxshi": "Ijobiy sifatga ega.",
            "yomon": "Salbiy sifatga ega.",
            "tez": "Tez harakatlanuvchi yoki tez sodir bo'luvchi.",
            "sekin": "Sekin harakatlanuvchi.",
            "issiq": "Yuqori haroratli.",
            "sovuq": "Past haroratli.",
            "yang i": "Hali eski bo'lmagan, yangidan yaratilgan.",
            "eski": "Uzoq vaqt ishlatilgan yoki o'tgan zamonga oid.",
            "baland": "Yuqori joylashgan yoki tovushi kuchli.",
            "past": "Past joylashgan yoki tovushi past."
        }
    },

    "son": {
        "nomi": "Son",
        "izoh": "Miqdor yoki tartibni bildiruvchi so'z turkumi.",
        "sozlar": {
            "bir": "1 soni.",
            "ikki": "2 soni.",
            "uch": "3 soni.",
            "to'rt": "4 soni.",
            "besh": "5 soni.",
            "o'n": "10 soni.",
            "yuz": "100 soni.",
            "ming": "1000 soni.",
            "birinchi": "Tartibdagi 1-o'rin.",
            "ikkinchi": "Tartibdagi 2-o'rin.",
            "uchinchi": "Tartibdagi 3-o'rin.",
            "oxirgi": "Eng so'nggi.",
            "yarim": "Yarmi, 1/2.",
            "ko'p": "Ko'p miqdorda.",
            "kam": "Kam miqdorda."
        }
    },

    "olmosh": {
        "nomi": "Olmosh",
        "izoh": "Ot o'rnida ishlatiladigan so'z turkumi.",
        "sozlar": {
            "men": "1-shaxs birlik.",
            "sen": "2-shaxs birlik (yaqin).",
            "u": "3-shaxs birlik.",
            "biz": "1-shaxs ko'plik.",
            "siz": "2-shaxs ko'plik yoki hurmat.",
            "ular": "3-shaxs ko'plik.",
            "bu": "Yaqin narsani ko'rsatadi.",
            "shu": "Yaqinroq narsani ko'rsatadi.",
            "o'sha": "Uzoqroq narsani ko'rsatadi.",
            "kim": "Shaxsni so'rash.",
            "nima": "Narsani so'rash.",
            "qayer": "Joyni so'rash.",
            "qachon": "Vaqtni so'rash.",
            "qanday": "Holat yoki usulni so'rash.",
            "necha": "Miqdorni so'rash."
        }
    },

    "fel": {
        "nomi": "Fe'l",
        "izoh": "Harakat yoki holatni bildiruvchi so'z turkumi.",
        "sozlar": {
            "yozmoq": "Yozish harakati.",
            "o'qimoq": "O'qish harakati.",
            "kelmoq": "Kelish harakati.",
            "ketmoq": "Ketish harakati.",
            "bo'lmoq": "Bo'lish, mavjud bo'lish.",
            "qilmoq": "Bajarish, amalga oshirish.",
            "ko'rmoq": "Ko'rish harakati.",
            "eshitmoq": "Eshitish harakati.",
            "yemoq": "Yeyish harakati.",
            "ichmoq": "Ichish harakati.",
            "yugurmoq": "Tez yugurish.",
            "o'tirmoq": "O'tirish holati.",
            "turmoq": "Turish holati.",
            "uxlamoq": "Uxlab qolish.",
            "o'ylamoq": "Fikr yuritish."
        }
    },

    "ravish": {
        "nomi": "Ravish",
        "izoh": "Fe'l, sifat yoki boshqa ravishning belgisini bildiruvchi so'z turkumi.",
        "sozlar": {
            "tez": "Tez sur'atda.",
            "sekin": "Sekin sur'atda.",
            "yaxshi": "Yaxshi tarzda.",
            "yomon": "Yomon tarzda.",
            "kecha": "O'tgan kun.",
            "bugun": "Hozirgi kun.",
            "ertaga": "Keyingi kun.",
            "hozir": "Hozirgi vaqtda.",
            "keyin": "Keyinroq.",
            "oldin": "Oldinroq.",
            "juda": "Juda yuqori darajada.",
            "ancha": "Ancha miqdorda.",
            "biroz": "Biroz miqdorda.",
            "doim": "Har doim.",
            "hech qachon": "Hech qachon emas."
        }
    },

    "boglovchi": {
        "nomi": "Bog'lovchi",
        "izoh": "So'zlar, so'z birikmalari yoki gaplarni bog'lovchi yordamchi so'zlar.",
        "sozlar": {
            "va": "Biriktiruvchi bog'lovchi. Ikki yoki undan ortiq narsani qo'shadi.",
            "ham": "Biriktiruvchi. Qo'shimcha ma'no beradi.",
            "yoki": "Ajratuvchi bog'lovchi. Tanlovni bildiradi.",
            "yoxud": "Ajratuvchi. 'Yoki'ning sinonimi.",
            "lekin": "Zidlovchi bog'lovchi. Qarama-qarshilikni bildiradi.",
            "ammo": "Zidlovchi. 'Lekin'ning sinonimi.",
            "biroq": "Zidlovchi. Qarama-qarshilikni bildiradi.",
            "chunki": "Sabab bog'lovchisi. Sababni bildiradi.",
            "chunki": "Sabab. Nima uchunligini tushuntiradi.",
            "agar": "Shart bog'lovchisi. Shartni bildiradi.",
            "agar ... bo'lsa": "Shartli bog'lanish.",
            "garchi": "Zidlovchi-shart. Garchi ... bo'lsa ham.",
            "shuning uchun": "Natija bog'lovchisi.",
            "demak": "Xulosa bog'lovchisi.",
            "ya'ni": "Tushuntiruvchi bog'lovchi.",
            "masalan": "Misol keltirish uchun.",
            "hamda": "Biriktiruvchi. 'Va'ning sinonimi.",
            "yana": "Qo'shimcha ma'no.",
            "balki": "Taxmin yoki tanlov.",
            "zero": "Sabab. 'Chunki'ning sinonimi."
        }
    },

    "yuklama": {
        "nomi": "Yuklama",
        "izoh": "So'z yoki gapga qo'shimcha ma'no (so'roq, ta'kid, cheklash va h.k.) beruvchi yordamchi so'zlar.",
        "sozlar": {
            "-mi": "So'roq yuklamasi.",
            "-chi": "So'roq yoki undov yuklamasi.",
            "-ku": "Ta'kid yuklamasi.",
            "-da": "Ta'kid.",
            "faqat": "Cheklash yuklamasi.",
            "hatto": "Kuchaytirish.",
            "hatto ... ham": "Kuchaytirish.",
            "na ... na": "Inkor.",
            "go'yo": "O'xshatish.",
            "xuddi": "O'xshatish.",
            "aynan": "Aniqlik.",
            "albatta": "Tasdiq.",
            "haqiqatan": "Tasdiq.",
            "aslo": "Kuchli inkor.",
            "mutlaqo": "Kuchli inkor yoki tasdiq."
        }
    },

    "komakchi": {
        "nomi": "Ko'makchi",
        "izoh": "Ot yoki otlashgan so'z bilan birikib, undosh yoki boshqa munosabatlarni bildiruvchi yordamchi so'zlar.",
        "sozlar": {
            "bilan": "Birgalik, vosita.",
            "uchun": "Maqsad.",
            "haqida": "Mavzu.",
            "to'g'risida": "Mavzu.",
            "kabi": "O'xshatish.",
            "singari": "O'xshatish.",
            "bo'yicha": "Asosida.",
            "orqali": "Vosita.",
            "sababli": "Sabab.",
            "tufayli": "Sabab.",
            "qadar": "Chegara.",
            "gacha": "Chegara.",
            "oldin": "Vaqt.",
            "keyin": "Vaqt.",
            "davomida": "Vaqt oralig'i."
        }
    },

    "undov": {
        "nomi": "Undov",
        "izoh": "His-hayajon, chaqiriq, buyruq yoki boshqa hissiyotni bildiruvchi so'zlar.",
        "sozlar": {
            "Voy!": "Hayrat yoki qo'rquv.",
            "Oh!": "Afus yoki hayrat.",
            "Eh!": "Afus.",
            "Barakalla!": "Maqtov.",
            "Rahmat!": "Minnatdorchilik.",
            "Mayli!": "Rozilik.",
            "Hoy!": "Chaqiriq.",
            "Ush!": "Og'riq yoki charchoq.",
            "Uf!": "Charchoq yoki afus.",
            "Ha!": "Tasdiq yoki eslash.",
            "Yo'q!": "Inkor.",
            "Assalomu alaykum!": "Salomlashish.",
            "Xayr!": "Xayrlashish.",
            "Marhamat!": "Taklif.",
            "Iltimos!": "Iltimos qilish."
        }
    },

    "taqlid": {
        "nomi": "Taqlid so'zlar",
        "izoh": "Tovush, harakat yoki holatni taqlid qilib bildiruvchi so'zlar.",
        "sozlar": {
            "shuv-shuv": "Suv yoki shamol tovushi.",
            "taq-taq": "Qattiq narsa urilishi.",
            "gurs": "Og'ir narsa tushishi.",
            "piss": "Suv oqishi.",
            "vizz": "Tez harakat tovushi.",
            "dong": "Metall tovushi.",
            "qars": "Qarsak tovushi.",
            "shitir": "Qog'oz yoki barg tovushi.",
            "g'ijir": "Eshik yoki tish tovushi.",
            "barr": "Portlash yoki kuchli tovush.",
            "tip-tip": "Yomg'ir tomchilari.",
            "sharaq": "Suv to'kilishi.",
            "du-du": "Baraban tovushi.",
            "miyov": "Mushuk tovushi.",
            "vov": "It tovushi."
        }
    },

    "modal": {
        "nomi": "Modal so'zlar",
        "izoh": "Gapning mazmuniga so'zlovchining munosabatini bildiruvchi so'zlar.",
        "sozlar": {
            "albatta": "To'liq ishonch.",
            "ehtimol": "Taxmin.",
            "shart": "Zarurat.",
            "mumkin": "Imkoniyat.",
            "kerak": "Zarurat.",
            "lozim": "Zarurat.",
            "zarur": "Zarurat.",
            "balki": "Taxmin.",
            "shekilli": "Taxmin.",
            "go'yo": "O'xshatish, taxmin.",
            "afsuski": "Afus.",
            "baxtimga": "Ijobiy holat.",
            "tasodifan": "Kutilmagan holat.",
            "asosan": "Asosiy jihatdan.",
            "umuman": "Umumiy holda."
        }
    },

    "badiiy": {
        "nomi": "Badiiy so'zlar",
        "izoh": "Badiiy adabiyotda qo'llaniladigan, obrazli, ta'sirchan so'z va iboralar.",
        "sozlar": {
            "ko'ngil": "Yurak, his-tuyg'u.",
            "dil": "Yurak (badiiy).",
            "jon": "Hayot, ruh.",
            "orzu": "Istak, xohish.",
            "armon": "Ushalmagan orzu.",
            "hijron": "Ayriliq dardi.",
            "vasl": "Uchrashuv, birlashish.",
            "g'am": "Qayg'u.",
            "shodlik": "Xursandchilik.",
            "bahor": "Bahor fasli (yoshlik, yangilanish ma'nosida).",
            "qish": "Qish fasli (qiyinchilik ma'nosida).",
            "oy": "Oy (go'zallik timsoli).",
            "yulduz": "Yulduz (orzu, umid).",
            "gul": "Gul (go'zallik, sevgili).",
            "bulbul": "Bulbul (ashula, shoir)."
        }
    },

    "atama": {
        "nomi": "Atamalar",
        "izoh": "Fan, texnika, san'at va boshqa sohalarga oid maxsus so'zlar.",
        "sozlar": {
            "kompyuter": "Elektron hisoblash mashinasi.",
            "internet": "Global kompyuter tarmog'i.",
            "dastur": "Kompyuter uchun yozilgan buyruqlar to'plami.",
            "bot": "Avtomatlashtirilgan dastur (masalan, Telegram bot).",
            "algoritm": "Muammoni yechish ketma-ketligi.",
            "ma'lumot": "Axborot, data.",
            "fayl": "Ma'lumot saqlanadigan birlik.",
            "server": "Xizmat ko'rsatuvchi kompyuter.",
            "token": "Telegram bot uchun maxsus kalit.",
            "webhook": "Telegram botga xabar yuborish usuli.",
            "API": "Dasturlar o'rtasida bog'lanish interfeysi.",
            "kod": "Dastur matni.",
            "xato": "Xatolik, error.",
            "funksiya": "Dasturdagi alohida vazifa bajaruvchi qism.",
            "o'zgaruvchi": "Qiymat saqlovchi nom."
        }
    }
}


# ============================================================
# Yordamchi funksiyalar (botda ishlatish uchun)
# ============================================================

def turkumlar_royxati():
    """Barcha so'z turkumlarini qaytaradi"""
    return list(lugat.keys())


def turkum_haqida(turkum_nomi: str):
    """Berilgan turkum haqida ma'lumot qaytaradi"""
    turkum_nomi = turkum_nomi.lower().strip()
    if turkum_nomi in lugat:
        return lugat[turkum_nomi]
    return None


def soz_izohi(soz: str):
    """So'zni barcha turkumlardan qidiradi va izohini qaytaradi"""
    soz = soz.lower().strip()
    natijalar = []
    for turkum, data in lugat.items():
        if soz in data["sozlar"]:
            natijalar.append({
                "turkum": data["nomi"],
                "izoh": data["sozlar"][soz]
            })
    return natijalar


def turkum_sozlari(turkum_nomi: str):
    """Berilgan turkumdagi barcha so'zlarni qaytaradi"""
    data = turkum_haqida(turkum_nomi)
    if data:
        return data["sozlar"]
    return {}


# ============================================================
# Test (faylni to'g'ridan-to'g'ri ishga tushirsangiz)
# ============================================================
if __name__ == "__main__":
    print("O'zbek tili lug'ati yuklandi!")
    print(f"Jami turkumlar: {len(lugat)}")
    print("Turkumlari:", ", ".join(turkumlar_royxati()))
    print("\nMisol: 'kitob' so'zi →", soz_izohi("kitob"))
