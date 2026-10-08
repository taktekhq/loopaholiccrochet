#!/usr/bin/env python3
"""Generates the static Loopaholic shop site from catalog.json.

Run `python3 build.py` after any catalog.json or copy edit, then commit the
generated HTML/sitemap/robots files alongside it. Photos: `make_images.py`.
Design notes (not served): docs-design/PLAN.md.
"""
import hashlib
import html
import json
import os
import re
import sys
from urllib.parse import quote

ROOT = os.path.dirname(os.path.abspath(__file__))
DOMAIN = "loopaholiccrochet.com"
BASE_URL = f"https://{DOMAIN}"
GA = "G-EQ20EYFSY3"
INSTAGRAM = "https://instagram.com/loopaholic.crochet"      # profile ("follow us")
INSTAGRAM_DM = "https://ig.me/m/loopaholic.crochet"          # opens a direct message (ordering)
INSTAGRAM_HANDLE = "@loopaholic.crochet"
# No business WhatsApp number is confirmed yet (ask in workstream log).
# Set this once Rana/Nizar give one: the primary order button, its event
# (whatsapp_click) and the "WhatsApp or Instagram" copy all come back on rebuild.
WHATSAPP_NUMBER = None  # e.g. "+9613XXXXXX"
HAS_WHATSAPP = bool(WHATSAPP_NUMBER)
# Sizes and making times in catalog.json (and the FAQ's day ranges) were never
# confirmed by Rana. Flip to True once she confirms them: sizes and making
# times reappear on product pages and in JSON-LD, and the FAQ/shipping copy
# switches back to the ranges.
SHOW_UNCONFIRMED_DETAILS = False
YEAR = 2026

CATALOG = json.load(open(os.path.join(ROOT, "catalog.json"), encoding="utf-8"))
PRODUCTS = CATALOG["products"]
BY_ID = {p["id"]: p for p in PRODUCTS}

CATEGORY_LABEL = {
    "animal": {"en": "Plushies", "ar": "حيوانات محشوة"},
    "doll": {"en": "Dolls", "ar": "عرائس"},
    "flower": {"en": "Flowers", "ar": "زهور"},
    "fun": {"en": "Fun & Novelty", "ar": "طرائف"},
    "giftset": {"en": "Gift Sets", "ar": "مجموعات هدايا"},
    "seasonal": {"en": "Seasonal", "ar": "مواسم"},
    "accessory": {"en": "Accessories", "ar": "إكسسوارات"},
    "baby": {"en": "Baby", "ar": "أطفال"},
}
CATEGORY_ORDER = ["animal", "doll", "flower", "giftset", "seasonal", "accessory", "baby", "fun"]
# Shop sections. Categories with one piece each share a section so the grid has no
# single-tile rows; each piece keeps its own category everywhere else.
SHOP_GROUPS = [
    ("animal", ["animal"]), ("doll", ["doll"]), ("flower", ["flower"]),
    ("more", ["giftset", "seasonal", "accessory"]), ("baby", ["baby"]), ("fun", ["fun"]),
]
GROUP_LABEL = {"more": {"en": "Gifts & more", "ar": "هدايا وأكثر"}}
GROUP_OF = {c: g for g, cs in SHOP_GROUPS for c in cs}
# Kept out of home and "more pieces" picks: its photo has a sliver of a hand in it.
NOT_FEATURED = {"p207"}
CROPPED = {"p207"}
_SC = os.path.join(ROOT, "assets/img/p/stitch-centres.json")
STITCH_CENTRES = json.load(open(_SC)) if os.path.exists(_SC) else {}   # photo cropped to the head and front paws (make_images.py CROP)


def group_label(g, lang):
    return GROUP_LABEL[g][lang] if g in GROUP_LABEL else CATEGORY_LABEL[g][lang]

# Colour names as they appear in catalog.json → Arabic (the colours visible in each photo).
COLOR_AR = {
    "beige": "بيج", "black": "أسود", "black hair": "شعر أسود", "blue": "أزرق", "blue-grey": "أزرق رمادي",
    "brown": "بني", "brown hair": "شعر بني", "cream": "كريمي", "green": "أخضر", "grey": "رمادي",
    "lavender": "ليلكي فاتح", "lilac": "ليلكي", "navy": "كحلي", "olive": "زيتي", "orange": "برتقالي",
    "pink": "وردي", "pink tail": "ذيل وردي", "purple": "بنفسجي", "purple tail": "ذيل بنفسجي", "red": "أحمر",
    "tan": "بني فاتح", "teal": "تركوازي", "teal/blue": "تركوازي وأزرق", "white": "أبيض", "yellow": "أصفر",
}
# Words used in catalog size_approx → Arabic (only rendered when SHOW_UNCONFIRMED_DETAILS).
SIZE_AR = [
    ("comes with a display stand", "مع قاعدة عرض"), ("set of 2", "مجموعة من قطعتين"), ("long ears", "بأذنين طويلتين"),
    ("on stand", "على قاعدة"), ("in pot", "في أصيص"), ("sitting", "جالسًا"), ("standing", "واقفًا"),
    ("stem", "مع الساق"), ("across", "عرضًا"), ("each", "لكل قطعة"), ("ring", "للحلقة"), ("boxed", "في علبة"),
    ("coiled", "ملفوفًا"), ("long", "طولًا"), ("cm", "سم"), (",", "،"),
]

HOME_HERO_ID = "p005"        # panda: clean cut-out edges, stitches read clearly inside the loupe
FEATURED_IDS = ["p003", "p008", "p154", "p065", "p016", "p043", "p021", "p369"]
CUSTOM_EXAMPLES = [("custom-letter-d", "letter_d"), ("custom-daisy-keychain", "daisy")]

# ---------------------------------------------------------------- i18n ----
T = {
    "en": {
        "lang": "en", "dir": "ltr", "alt_lang": "ar", "alt_label": "العربية", "og_locale": "en_US", "og_alt": "ar_AR",
        "site_name": "Loopaholic",
        "skip": "Skip to content", "menu": "Menu", "nav_label": "Main", "menu_label": "All pages",
        "home_label": "Loopaholic, home",
        "nav_home": "Home", "nav_shop": "Shop", "nav_custom": "Custom orders",
        "nav_shipping": "Shipping", "nav_about": "About", "nav_faq": "FAQ",
        "hero_h1": "Handmade crochet gifts, made to order in Lebanon",
        "hero_lead": "Plushies, dolls, flowers and baby pieces, crocheted by hand once you order. For birthdays, new arrivals, or anyone who likes a soft thing to hold.",
        "cta_shop": "Browse the pieces", "how_link": "How ordering works",
        "loupe_alt": "Close-up of the stitches, cropped from the same photo",
        "loupe_role": "magnifier",
        "loupe_hint": "Move over the photo: the ring shows the stitches up close.",
        "loupe_hint_touch": "Tap the photo to look closer.",
        "crop_note": " Photo cropped to the head and front paws.",
        "loupe_label": "Close-up of the stitches, from the same photo. Use the arrow keys to move it over the photo, Escape to put it back.",
        "featured_h": "Some of the pieces", "featured_more": "See every piece in the shop",
        "how_h": "How ordering works",
        "how_lead": "There’s no cart and no checkout. You order in a conversation with the person who makes it.",
        "how": [
            ("Pick a piece", "Browse the shop, or bring an idea for a custom order."),
            ("Message us", "On Instagram. We confirm the price, colors and making time with you there."),
            ("We make it by hand", "Once the price and colors are agreed, we crochet your piece and arrange delivery."),
        ],
        "made_h": "Made by hand in Lebanon",
        "made_b": "Every plushie, doll and flower is crocheted by hand, one stitch at a time, after you order it. Small differences in a stitch or a shade of yarn are part of what makes each one yours.",
        "made_link": "About the craft",
        "follow_h": "On Instagram",
        "follow_b": "Follow the latest pieces and works in progress on Instagram.",
        "follow_cta": "Follow @loopaholic.crochet",
        "shop_title": "Shop",
        "shop_lead": "Every piece is made by hand when you order it.",
        "chips_label": "Categories",
        "cant_find_h": "Can’t find it?", "cant_find_b": "Ask for a different color, a name, or a piece that doesn’t exist yet.",
        "cant_find_link": "Custom orders",
        "breadcrumb_label": "Breadcrumb", "breadcrumb_home": "Home", "breadcrumb_shop": "Shop",
        "size_label": "Size", "colors_label": "Colors in the photo", "lead_label": "Making time", "days": "days",
        "made_to_order": "Made to order",
        "price_note": "Made to order. Price confirmed in the chat.",
        "order_whatsapp": "Order on WhatsApp", "order_instagram": "Order on Instagram",
        "message_instagram": "Message on Instagram",
        "order_note_ig": "Opens a direct message to @loopaholic.crochet. We reply with the price, colors and making time.",
        "order_note_short": "Opens a direct message to @loopaholic.crochet.",
        "order_note_wa": "Opens WhatsApp with a message about this piece. We reply with the price, colors and making time.",
        "order_intl_title": "Ordering from outside Lebanon",
        "order_intl_body_live": "Pay online by card; shipping is calculated at checkout.",
        "buy_now": "Buy now",
        "delivery_h": "Delivery and returns",
        "delivery_b1": "Lebanon: pay by Whish or cash on delivery. Gulf and worldwide: we quote shipping in the chat once we know your city.",
        "delivery_b2": "Each piece is made for you, so we can’t take change-of-mind returns. If it arrives damaged or wrong, message us within 48 hours and we’ll make it right.",
        "delivery_link": "Shipping details",
        "related_title": "More pieces like this",
        "custom_title": "Custom orders",
        "custom_lead": "Want a color swap, a name, or a piece that doesn’t exist yet? We take commissions.",
        "custom_body_1": "Most of our plushies and dolls can be made in different colors or sizes on request. We also make fully custom pieces: a name in crochet letters, a character, or a gift built around an idea you bring us.",
        "custom_body_2": "Two examples: a crochet letter for a nursery, and a small flower keychain made as a party favor.",
        "letter_d": "Crochet letter D", "daisy": "Daisy keychain",
        "custom_how_title": "How it works",
        "custom_how": [
            ("Tell us the idea", "Message us on Instagram with what you have in mind. A photo or a description helps."),
            ("We agree the details", "We confirm the design, price and making time. Custom pieces usually take longer than the shop pieces."),
            ("We make it by hand", "You pay a deposit to start, we crochet it, and send photos before it ships."),
        ],
        "custom_cta": "Start a custom order",
        "shipping_title": "Shipping",
        "shipping_lead": "Every piece is made to order, then shipped from Lebanon.",
        "shipping_lebanon_h": "Lebanon",
        "shipping_lebanon_b": "Order on WhatsApp or Instagram. Pay by Whish transfer or cash on delivery. Delivery time depends on your area and how long the piece takes to make — we’ll confirm both when you order.",
        "shipping_gulf_h": "Gulf countries",
        "shipping_gulf_b": "We ship to the UAE, Saudi Arabia, Kuwait, Qatar, Bahrain and Oman. Shipping cost is quoted on WhatsApp or Instagram once we know your city and the pieces you want. We haven’t fixed flat rates yet.",
        "shipping_intl_h": "Everywhere else",
        "shipping_intl_b": "We ship internationally. Shipping cost is quoted on WhatsApp or Instagram once we know your city and the pieces you want.",
        "shipping_returns_h": "Returns",
        "shipping_note_h": "Good to know",
        "shipping_note_b_confirmed": "Every piece is made to order, so shipping starts after the made-to-order time on the product page, not the day you order. Customs fees outside Lebanon are the buyer’s responsibility.",
        "shipping_note_b_unconfirmed": "Every piece is made to order, so shipping starts once your piece is finished, not the day you order. We confirm the making time when you message us. Customs fees outside Lebanon are the buyer’s responsibility.",
        "about_title": "About the craft",
        "about_lead": "Every piece is crocheted by hand in Lebanon, one stitch at a time.",
        "about_body_1": "Loopaholic makes amigurumi — crocheted, stuffed figures — and crochet flowers entirely by hand, one stitch at a time. Nothing is machine-made or mass-produced: every plushie, doll and flower on this site is handmade in Lebanon and made to order.",
        "about_body_2": "Because each piece is made by hand after you order it, small variations, like a slightly different stitch or a shade of yarn, are part of what makes it one of a kind, not a flaw.",
        "about_body_3": "Follow the latest pieces and works in progress on Instagram:",
        "faq_title": "FAQ",
        "faq_lead": "The questions people ask before ordering.",
        "faq": [
            ("How long does an order take to make?", "@LEAD@"),
            ("Do you ship outside Lebanon?", "Yes, to the Gulf and internationally. Shipping cost is quoted by hand on WhatsApp or Instagram for now, based on your location and what you’re ordering."),
            ("How do I pay?", "In Lebanon: Whish transfer or cash on delivery. Outside Lebanon: message us and we’ll arrange payment in the chat."),
            ("How much does a piece cost?", "We don’t list prices on the site. Message us on WhatsApp or Instagram with the piece you want and we’ll confirm a price before you order."),
            ("Can I change the colors?", "Usually yes. Message us with the colors you’d like and we’ll confirm if it works for that piece."),
            ("What are the pieces made from?", "Message us on WhatsApp or Instagram and we’ll confirm the materials for the specific piece you’re asking about."),
            ("Can I return or exchange a piece?", "Because every piece is made to order just for you, we can’t accept returns for a change of mind. If a piece arrives damaged or wrong, message us within 48 hours and we’ll make it right."),
            ("Are the pieces suitable for babies and small children?", "Our baby pieces haven’t been through any testing, so we make no claim about which ages they suit. Message us before ordering for an infant, and always supervise young children with any small handmade item."),
        ],
        "faq_lead_time_confirmed": "Most plushies and dolls take 10–28 days to crochet, and flowers take 5–12 days. The exact range is on each product page. Custom orders usually take a bit longer. We’ll confirm a date when you order.",
        "faq_lead_time_unconfirmed": "We confirm the making time when you message us. Custom orders usually take a bit longer.",
        "footer_tagline": "Handmade crochet from Lebanon, made to order.",
        "footer_shop": "Shop", "footer_info": "Help", "footer_follow": "Follow",
        "meta_shipping_desc": "Order on Instagram. Pay by Whish or cash on delivery in Lebanon. We confirm the delivery time when you order.",
        "meta_home_desc": "Handmade amigurumi plushies, dolls, flowers and baby gifts, crocheted to order in Lebanon and shipped to the Gulf and worldwide.",
        "meta_shop_desc": "Browse handmade crochet plushies, dolls, flowers and gifts, made to order and shipped from Lebanon worldwide.",
        "nf_title": "Page not found",
        "nf_body": "This page slipped a stitch: it isn’t here. It may have moved when the shop was rebuilt.",
        "nf_contact": "Looking for a specific piece? Message us on Instagram.",
    },
    "ar": {
        "lang": "ar", "dir": "rtl", "alt_lang": "en", "alt_label": "English", "og_locale": "ar_AR", "og_alt": "en_US",
        "site_name": "لوباهوليك",
        "skip": "انتقلوا إلى المحتوى", "menu": "القائمة", "nav_label": "الرئيسية", "menu_label": "كل الصفحات",
        "home_label": "لوباهوليك، الصفحة الرئيسية",
        "nav_home": "الرئيسية", "nav_shop": "المتجر", "nav_custom": "طلب خاص",
        "nav_shipping": "الشحن", "nav_about": "عن الحرفة", "nav_faq": "الأسئلة الشائعة",
        "hero_h1": "هدايا كروشيه يدوية، تُصنع عند الطلب في لبنان",
        "hero_lead": "حيوانات محشوة وعرائس وزهور وقطع للأطفال، نحيكها باليد بعد طلبكم. لأعياد الميلاد، للمولود الجديد، أو لكل من يحب شيئًا ناعمًا يحضنه.",
        "cta_shop": "تصفّحوا القطع", "how_link": "كيف يتم الطلب",
        "loupe_alt": "صورة مقرّبة للغرز، مقتطعة من الصورة نفسها",
        "loupe_role": "عدسة مكبّرة",
        "loupe_hint": "مرّروا المؤشر فوق الصورة: الحلقة تُظهر الغرز عن قرب.",
        "loupe_hint_touch": "اضغطوا على الصورة للتكبير.",
        "crop_note": " الصورة مقتطعة لتُظهر الرأس والقدمين الأماميتين.",
        "loupe_label": "صورة مقرّبة للغرز من الصورة نفسها. استخدموا مفاتيح الأسهم لتحريكها فوق الصورة، وEscape لإعادتها.",
        "featured_h": "بعض القطع", "featured_more": "كل القطع في المتجر",
        "how_h": "كيف يتم الطلب",
        "how_lead": "لا سلة شراء ولا دفع إلكتروني. تطلبون بمحادثة مباشرة مع من تصنع القطعة.",
        "how": [
            ("اختاروا قطعة", "تصفّحوا المتجر، أو أخبرونا بفكرة لطلب خاص."),
            ("راسلونا", "على إنستغرام. نتفق معكم هناك على السعر والألوان ومدة التصنيع."),
            ("نصنعها باليد", "بعد الاتفاق على السعر والألوان، نحيك قطعتكم ونرتّب التوصيل."),
        ],
        "made_h": "مصنوعة يدويًا في لبنان",
        "made_b": "كل حيوان محشو وعروسة وزهرة نحيكها باليد، غرزة بعد غرزة، بعد أن تطلبوها. الاختلافات الصغيرة في غرزة أو درجة لون هي ما يجعل كل قطعة خاصة بكم.",
        "made_link": "عن الحرفة",
        "follow_h": "على إنستغرام",
        "follow_b": "تابعوا أحدث القطع والأعمال الجارية على إنستغرام.",
        "follow_cta": "تابعوا @loopaholic.crochet",
        "shop_title": "المتجر",
        "shop_lead": "كل قطعة نحيكها باليد عند طلبها.",
        "chips_label": "الفئات",
        "cant_find_h": "لم تجدوا ما تريدونه؟", "cant_find_b": "اطلبوا لونًا مختلفًا، أو اسمًا، أو قطعة غير موجودة بعد.",
        "cant_find_link": "الطلبات الخاصة",
        "breadcrumb_label": "مسار التصفح", "breadcrumb_home": "الرئيسية", "breadcrumb_shop": "المتجر",
        "size_label": "القياس", "colors_label": "الألوان في الصورة", "lead_label": "مدة التصنيع", "days": "يومًا",
        "made_to_order": "تُصنع عند الطلب",
        "price_note": "تُصنع عند الطلب، ونؤكد السعر في المحادثة.",
        "order_whatsapp": "اطلبوا على واتساب", "order_instagram": "اطلبوا على إنستغرام",
        "message_instagram": "راسلونا على إنستغرام",
        "order_note_ig": "يفتح رسالة مباشرة إلى @loopaholic.crochet. نرد عليكم بالسعر والألوان ومدة التصنيع.",
        "order_note_short": "يفتح رسالة مباشرة إلى @loopaholic.crochet.",
        "order_note_wa": "يفتح واتساب برسالة عن هذه القطعة. نرد عليكم بالسعر والألوان ومدة التصنيع.",
        "order_intl_title": "الطلب من خارج لبنان",
        "order_intl_body_live": "ادفعوا إلكترونيًا بالبطاقة، وتُحسب تكلفة الشحن عند الدفع.",
        "buy_now": "اشتروا الآن",
        "delivery_h": "التوصيل والاسترجاع",
        "delivery_b1": "داخل لبنان: الدفع عبر Whish أو عند التسليم. الخليج وباقي العالم: نحدد تكلفة الشحن في المحادثة بعد معرفة مدينتكم.",
        "delivery_b2": "كل قطعة تُصنع لكم خصيصًا، لذلك لا نقبل الاسترجاع لمجرد تغيير الرأي. إذا وصلت تالفة أو خاطئة، راسلونا خلال 48 ساعة وسنصلح الأمر.",
        "delivery_link": "تفاصيل الشحن",
        "related_title": "قطع مشابهة",
        "custom_title": "طلب خاص",
        "custom_lead": "تريدون تغيير لون، إضافة اسم، أو قطعة غير موجودة بعد؟ نستقبل الطلبات الخاصة.",
        "custom_body_1": "معظم الحيوانات المحشوة والعرائس يمكن صنعها بألوان أو قياسات مختلفة عند الطلب. كما نصنع قطعًا خاصة بالكامل: اسم بحروف كروشيه، شخصية، أو هدية مبنية على فكرتكم.",
        "custom_body_2": "مثالان: حرف كروشيه لغرفة طفل، وسلسلة مفاتيح على شكل زهرة صُنعت كتذكار لحفلة.",
        "letter_d": "حرف D بالكروشيه", "daisy": "سلسلة مفاتيح بزهرة أقحوان",
        "custom_how_title": "كيف تطلبون",
        "custom_how": [
            ("أخبرونا بالفكرة", "راسلونا على إنستغرام بما تريدونه. صورة أو وصف يساعدنا."),
            ("نتفق على التفاصيل", "نؤكد التصميم والسعر ومدة التصنيع. الطلبات الخاصة تستغرق غالبًا أطول من قطع المتجر."),
            ("نصنعها باليد", "تدفعون دفعة أولى للبدء، نحيك القطعة، ونرسل لكم صورًا قبل الشحن."),
        ],
        "custom_cta": "ابدأوا طلبًا خاصًا",
        "shipping_title": "الشحن",
        "shipping_lead": "كل قطعة تُصنع عند الطلب، ثم تُشحن من لبنان.",
        "shipping_lebanon_h": "لبنان",
        "shipping_lebanon_b": "الطلب عبر واتساب أو إنستغرام. الدفع عبر تحويل Whish أو الدفع عند التسليم. مدة التوصيل تعتمد على منطقتكم ومدة تصنيع القطعة — نؤكد الاثنين عند الطلب.",
        "shipping_gulf_h": "دول الخليج",
        "shipping_gulf_b": "نشحن إلى الإمارات والسعودية والكويت وقطر والبحرين وعُمان. تكلفة الشحن تُحدد عبر واتساب أو إنستغرام بعد معرفة مدينتكم والقطع المطلوبة، فلم نحدد أسعارًا ثابتة بعد.",
        "shipping_intl_h": "باقي دول العالم",
        "shipping_intl_b": "نشحن دوليًا. تكلفة الشحن تُحدد عبر واتساب أو إنستغرام بعد معرفة مدينتكم والقطع المطلوبة.",
        "shipping_returns_h": "الاسترجاع",
        "shipping_note_h": "جيد أن تعرفوا",
        "shipping_note_b_confirmed": "كل قطعة تُصنع عند الطلب، فتبدأ مدة الشحن بعد مدة التصنيع المذكورة في صفحة المنتج، لا من يوم الطلب. رسوم الجمارك خارج لبنان على مسؤولية المشتري.",
        "shipping_note_b_unconfirmed": "كل قطعة تُصنع عند الطلب، فيبدأ الشحن بعد انتهاء صنع قطعتكم، لا من يوم الطلب. نؤكد مدة التصنيع عندما تراسلونا. رسوم الجمارك خارج لبنان على مسؤولية المشتري.",
        "about_title": "عن الحرفة",
        "about_lead": "كل قطعة نحيكها باليد في لبنان، غرزة بعد غرزة.",
        "about_body_1": "تصنع لوباهوليك قطع الأميغورومي — شخصيات كروشيه محشوة — وزهور الكروشيه بالكامل باليد، غرزة بعد غرزة. لا شيء مصنوع بالآلة أو بكميات كبيرة: كل حيوان محشو وعروسة وزهرة في هذا المتجر مصنوع يدويًا في لبنان وعند الطلب.",
        "about_body_2": "لأن كل قطعة تُصنع يدويًا بعد الطلب، فالاختلافات الصغيرة، كغرزة مختلفة قليلًا أو درجة لون، هي ما يجعلها فريدة، لا عيبًا.",
        "about_body_3": "تابعوا أحدث القطع والأعمال الجارية على إنستغرام:",
        "faq_title": "الأسئلة الشائعة",
        "faq_lead": "الأسئلة التي تصلنا قبل الطلب.",
        "faq": [
            ("كم تستغرق مدة تصنيع الطلب؟", "@LEAD@"),
            ("هل تشحنون خارج لبنان؟", "نعم، إلى دول الخليج وحول العالم. تكلفة الشحن تُحدد يدويًا عبر واتساب أو إنستغرام حاليًا، حسب موقعكم وما تطلبونه."),
            ("كيف أدفع؟", "داخل لبنان: تحويل Whish أو الدفع عند التسليم. خارج لبنان: راسلونا ونرتّب الدفع في المحادثة."),
            ("كم تكلفة القطعة؟", "لا نضع الأسعار على الموقع. راسلونا على واتساب أو إنستغرام بالقطعة التي تريدونها وسنؤكد السعر قبل الطلب."),
            ("هل يمكنني تغيير الألوان؟", "غالبًا نعم. راسلونا بالألوان التي تريدونها وسنؤكد إن كانت تناسب تلك القطعة."),
            ("من ماذا تُصنع القطع؟", "راسلونا على واتساب أو إنستغرام وسنؤكد لكم المواد الخاصة بالقطعة التي تسألون عنها."),
            ("هل يمكنني استرجاع أو استبدال قطعة؟", "لأن كل قطعة تُصنع خصيصًا عند الطلب، لا يمكننا قبول الاسترجاع لمجرد تغيير الرأي. إذا وصلت القطعة تالفة أو خاطئة، راسلونا خلال 48 ساعة وسنصلح الأمر."),
            ("هل القطع مناسبة للرضّع والأطفال الصغار؟", "قطع الأطفال لم تخضع لأي اختبارات، لذلك لا نقدّم أي ادعاء بشأن الأعمار التي تناسبها. راسلونا قبل الطلب لطفل رضيع، وراقبوا الأطفال الصغار دائمًا عند استخدام أي قطعة يدوية صغيرة."),
        ],
        "faq_lead_time_confirmed": "معظم الحيوانات المحشوة والعرائس تستغرق 10–28 يومًا للكروشيه، والزهور 5–12 يومًا. المدة الدقيقة مذكورة في صفحة كل منتج. الطلبات الخاصة تستغرق غالبًا أطول. نؤكد تاريخًا عند الطلب.",
        "faq_lead_time_unconfirmed": "نؤكد مدة التصنيع عندما تراسلونا. الطلبات الخاصة تستغرق غالبًا أطول.",
        "footer_tagline": "كروشيه يدوي من لبنان، يُصنع عند الطلب.",
        "footer_shop": "المتجر", "footer_info": "مساعدة", "footer_follow": "تابعونا",
        "meta_shipping_desc": "الطلب عبر إنستغرام. الدفع عبر Whish أو عند التسليم داخل لبنان. نؤكد مدة التوصيل عند الطلب.",
        "meta_home_desc": "حيوانات محشوة وعرائس وزهور وهدايا أطفال مصنوعة يدويًا بالكروشيه عند الطلب في لبنان، تُشحن إلى الخليج وحول العالم.",
        "meta_shop_desc": "تصفحوا حيوانات وعرائس وزهور وهدايا كروشيه يدوية، تُصنع عند الطلب وتُشحن من لبنان حول العالم.",
        "nf_title": "الصفحة غير موجودة",
        "nf_body": "انحلّت غرزة: هذه الصفحة غير موجودة هنا. ربما تغيّر عنوانها عندما أعدنا بناء المتجر.",
        "nf_contact": "تبحثون عن قطعة معيّنة؟ راسلونا على إنستغرام.",
    },
}

for _lang, _t in T.items():
    _lt = _t["faq_lead_time_confirmed" if SHOW_UNCONFIRMED_DETAILS else "faq_lead_time_unconfirmed"]
    _t["faq"] = [(q, _lt if a == "@LEAD@" else a) for q, a in _t["faq"]]
    _t["shipping_note_b"] = _t["shipping_note_b_confirmed" if SHOW_UNCONFIRMED_DETAILS else "shipping_note_b_unconfirmed"]

if not HAS_WHATSAPP:
    # Copy must not claim a WhatsApp ordering channel that doesn't exist yet
    # (R8, reviewer 2026-10-08). Reverts itself once WHATSAPP_NUMBER is set.
    _CHANNEL_RULES = [
        (r"WhatsApp or Instagram", "Instagram"),
        (r"Instagram or WhatsApp", "Instagram"),
        (r"واتساب أو إنستغرام", "إنستغرام"),
        (r"إنستغرام أو واتساب", "إنستغرام"),
    ]

    def _ig_only(s):
        for pat, rep in _CHANNEL_RULES:
            s = re.sub(pat, rep, s)
        return s
    for _lang in T:
        for _k, _v in list(T[_lang].items()):
            if isinstance(_v, str):
                T[_lang][_k] = _ig_only(_v)
            elif isinstance(_v, list):
                T[_lang][_k] = [tuple(_ig_only(x) for x in pair) for pair in _v]
else:
    for _lang in T:  # "Message us … On Instagram." becomes channel-neutral
        T[_lang]["how"][1] = (T[_lang]["how"][1][0], T[_lang]["how"][1][1].replace("On Instagram.", "On WhatsApp or Instagram.").replace("على إنستغرام.", "على واتساب أو إنستغرام."))

# ------------------------------------------------------- claims guard (R2b) ----
FORBIDDEN = [
    (r"\bsafe", "safe/safety"), (r"آمن", "آمن"), (r"(?i)\bcertif", "certified"), (r"(?i)non-?toxic", "non-toxic"),
    (r"(?i)\borganic\b", "organic"), (r"(?i)hypoallergenic", "hypoallergenic"), (r"(?i)\bwood", "wood/wooden"),
    (r"خشب", "خشب"), (r"\bCE\b", "CE"), (r"100\s?%", "100%"), (r"\$\s?\d", "$ price"),
    (r"(?i)\bUSD\s?\d|\d\s?USD\b", "USD price"),
]


def find_claims(text):
    return [label for pat, label in FORBIDDEN if re.search(pat, text, flags=re.I if label == "safe/safety" else 0)]


def check_claims():
    """Fail the build if catalog or site copy makes a material, safety or price claim."""
    problems = []

    def walk(obj, where):
        if isinstance(obj, dict):
            for k, v in obj.items():
                if k in ("currency", "image", "slug", "id", "stripe_payment_link"):
                    continue
                walk(v, f"{where}.{k}")
        elif isinstance(obj, (list, tuple)):
            for i, v in enumerate(obj):
                walk(v, f"{where}[{i}]")
        elif isinstance(obj, str):
            for label in find_claims(obj):
                problems.append(f"{where}: '{label}' in {obj[:90]!r}")
    walk(CATALOG, "catalog")
    walk(T, "copy")
    return problems


def check_rendered(relpath, content):
    """Same guard on the visible text of every rendered page (template strings included)."""
    text = re.sub(r"<script(?![^>]*ld\+json)[^>]*>.*?</script>|<style.*?</style>", " ", content, flags=re.S)
    text = re.sub(r"<[^>]+>", " ", text)
    text = html.unescape(text)
    return [f"{relpath}: '{label}'" for label in find_claims(text)]


RENDER_PROBLEMS = []

# ------------------------------------------------------------- assets ----


def asset_hash(rel):
    with open(os.path.join(ROOT, rel), "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()[:10]


def v(rel):
    return f"/{rel}?v={asset_hash(rel)}"


CSS_SRC = "assets/css/style.css"   # edit this one
CSS = "assets/css/site.min.css"     # generated by build_css(), the one pages load


def build_css():
    src = open(os.path.join(ROOT, CSS_SRC), encoding="utf-8").read()
    css = re.sub(r"/\*.*?\*/", "", src, flags=re.S)
    css = re.sub(r"\s+", " ", css)
    css = re.sub(r"\s*([{};,>])\s*", r"\1", css)
    css = re.sub(r":\s+", ":", css.replace(";}", "}"))
    with open(os.path.join(ROOT, CSS), "w", encoding="utf-8") as f:
        f.write(css.strip() + "\n")
JS_SRC = "assets/js/site.js"     # edit this one
JS = "assets/js/site.min.js"     # generated by build_js(), the one pages load


def build_js():
    """Conservative minify: comments and indentation go, line breaks stay (no ASI risk)."""
    src = open(os.path.join(ROOT, JS_SRC), encoding="utf-8").read()
    js = re.sub(r"/\*.*?\*/", "", src, flags=re.S)
    out = []
    for line in js.splitlines():
        line = re.sub(r"\s+//\s.*$", "", line).strip()
        if line and not line.startswith("//"):
            out.append(line)
    with open(os.path.join(ROOT, JS), "w", encoding="utf-8") as f:
        f.write("\n".join(out) + "\n")
FONT_LATIN = "assets/fonts/nunito-latin.woff2"
FONT_AR = "assets/fonts/baloo-bhaijaan2-arabic.woff2"
FONT_AR_SWITCH = "assets/fonts/baloo-bhaijaan2-switch.woff2"   # pyftsubset --text="العربية"
LATIN_RANGE = "U+0000-00FF, U+0131, U+0152-0153, U+02BB-02BC, U+02C6, U+02DA, U+02DC, U+0304, U+0308, U+0329, U+2000-206F, U+20AC, U+2122, U+2191, U+2193, U+2212, U+2215, U+FEFF, U+FFFD"
ARABIC_RANGE = "U+0600-06FF, U+0750-077F, U+0870-0891, U+0897-08E1, U+08E3-08FF, U+200C-200E, U+2010-2011, U+204F, U+2E41, U+FB50-FDFF, U+FE70-FE74, U+FE76-FEFC"

ICONS = {
    "instagram": '<svg class="icon" viewBox="0 0 24 24" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="3" width="18" height="18" rx="5"/><circle cx="12" cy="12" r="4"/><circle cx="17.3" cy="6.7" r=".6" fill="currentColor"/></svg>',
    "whatsapp": '<svg class="icon" viewBox="0 0 24 24" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round"><path d="M3.5 20.5l1.3-4.2A8.5 8.5 0 1 1 8 19.4z"/><path d="M9 8.6c.2 2.9 2.9 5.9 6.3 6.4l1-1.3-1.9-1-1 .9c-1-.4-2.2-1.6-2.6-2.6l.9-1-1-1.9z"/></svg>',
    "menu": '<svg class="icon icon-open" viewBox="0 0 24 24" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="1.75" stroke-linecap="round"><path d="M4 7h16M4 12h16M4 17h16"/></svg>',
    "close": '<svg class="icon icon-close" viewBox="0 0 24 24" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="1.75" stroke-linecap="round"><path d="M6 6l12 12M18 6L6 18"/></svg>',
}

# ------------------------------------------------------------- helpers ----


def esc(s):
    return html.escape(s, quote=True)


def L(t, path):
    """Localised path: '/shop/' → '/ar/shop/' on Arabic pages."""
    return path if t["lang"] == "en" else "/ar" + path


def whatsapp_link(text):
    num = WHATSAPP_NUMBER.replace("+", "").replace(" ", "")
    return f"https://wa.me/{num}?text={quote(text)}"


def ga(event, params):
    return f'onclick="gtag(\'event\',\'{event}\',{params})"'


def order_cta(t, ctx_js, wa_text, label_key=None, block=True, cta_id=None, secondary=True, variant="btn-primary"):
    # block=True: the inline button, watched by the sticky bar (data-order-cta).
    """The one order action. Instagram DM until a WhatsApp number exists; then WhatsApp
    is primary and the Instagram DM becomes the outline secondary."""
    idattr = (f' id="{cta_id}"' if cta_id else "") + (" data-order-cta" if block else "")
    blk = " btn-block" if block else ""
    if HAS_WHATSAPP:
        label = t[label_key] if label_key else t["order_whatsapp"]
        out = (f'<a class="btn {variant}{blk}"{idattr} href="{esc(whatsapp_link(wa_text))}" {ga("whatsapp_click", ctx_js)}>'
               f'{ICONS["whatsapp"]}<span>{label}</span></a>')
        if secondary:
            out += (f'\n<a class="btn btn-secondary" href="{INSTAGRAM_DM}" {ga("instagram_click", ctx_js)}>'
                    f'{ICONS["instagram"]}<span>{t["message_instagram"]}</span></a>')
        return out
    label = t[label_key] if label_key else t["order_instagram"]
    return (f'<a class="btn {variant}{blk}"{idattr} href="{INSTAGRAM_DM}" {ga("instagram_click", ctx_js)}>'
            f'{ICONS["instagram"]}<span>{label}</span></a>')


def handle(t):
    return f'<bdi dir="ltr">{INSTAGRAM_HANDLE}</bdi>'


def with_handle(t, s):
    return esc(s).replace(INSTAGRAM_HANDLE, handle(t))


def img_base(pid):
    return f"/assets/img/p/{pid}"


def picture(pid, alt, sizes, *, eager=False, cls=""):
    b = img_base(pid)
    load = 'fetchpriority="high" decoding="async"' if eager else 'loading="lazy" decoding="async"'
    return (f'<picture{f" class={chr(34)}{cls}{chr(34)}" if cls else ""}>'
            f'<source type="image/avif" srcset="{b}/w400.avif 400w, {b}/w800.avif 800w, {b}/w1200.avif 1200w" sizes="{sizes}">'
            f'<source type="image/webp" srcset="{b}/w400.webp 400w, {b}/w800.webp 800w, {b}/w1200.webp 1200w" sizes="{sizes}">'
            f'<img src="{b}/w800.jpg" width="800" height="800" alt="{esc(alt)}" {load}></picture>')


def loupe(pid, t, interactive=False):
    b = img_base(pid)
    cx, cy = STITCH_CENTRES.get(pid, [0.5, 0.5])
    live = (f' data-full="{b}/w1200" data-cx="{cx}" data-cy="{cy}" data-role="{esc(t["loupe_role"])}" data-label="{esc(t["loupe_label"])}"'
            if interactive else "")
    return (f'<figure class="loupe"{live}><picture>'
            f'<source type="image/avif" srcset="{b}/stitch.avif"><source type="image/webp" srcset="{b}/stitch.webp">'
            f'<img src="{b}/stitch.jpg" width="400" height="400" alt="{esc(t["loupe_alt"])}" loading="lazy" decoding="async"></picture></figure>')


def colors_text(p, t):
    if t["lang"] == "ar":
        return "، ".join(COLOR_AR.get(c, c) for c in p["colors"])
    return ", ".join(p["colors"])


def size_text(p, t):
    s = p["size_approx"]
    if t["lang"] == "ar":
        for en, ar in SIZE_AR:
            s = s.replace(en, ar)
        s = s.replace("~", "حوالي ")
    return s


GRID_SIZES = "(min-width: 75em) 17rem, (min-width: 40em) 30vw, 46vw"


def piece(p, t, eager=False, meta=True, sizes=None):
    title = p["title"][t["lang"]]
    meta = f'<span class="piece-meta">{CATEGORY_LABEL[p["category"]][t["lang"]]}</span>' if meta else ""
    return (f'<li><a class="piece" href="{L(t, "/shop/" + p["slug"] + "/")}">'
            f'<div class="tile">{picture(p["id"], "", sizes or GRID_SIZES, eager=eager)}</div>'
            f'<span class="piece-name">{esc(title)}</span>{meta}</a></li>')


FEATURE_SIZES = "(min-width: 75em) 36rem, (min-width: 40em) 30vw, 46vw"


def grid(items, t, eager_first=0, meta=True):
    # A section that would leave one tile alone on the last row of the 4-up grid shows
    # its first piece at double size instead (17 → 2×2 + 16 fills five full rows).
    feature = len(items) > 4 and len(items) % 4 == 1
    cls = "grid grid-feature" if feature else "grid"
    return (f'<ul class="{cls}" role="list">' + "".join(
        piece(p, t, eager=i < eager_first, meta=meta, sizes=FEATURE_SIZES if feature and i == 0 else None)
        for i, p in enumerate(items)) + "</ul>")


def steps(items, compact=False, row=False, level="h3"):
    cls = "steps" + (" steps-compact" if compact else "") + (" steps-row" if row else "")
    lis = "".join(f"<li><{level}>{esc(h)}</{level}><p>{esc(b)}</p></li>" for h, b in items)
    return f'<ol class="{cls}" role="list">{lis}</ol>'

# --------------------------------------------------------------- shell ----


NAV = [("nav_home", "/", "home"), ("nav_shop", "/shop/", "shop"), ("nav_custom", "/custom-orders/", "custom"),
       ("nav_shipping", "/shipping/", "shipping"), ("nav_about", "/about/", "about"), ("nav_faq", "/faq/", "faq")]


def nav_links(t, active, key_only_shop=False):
    out = []
    for key, href, name in NAV:
        if key_only_shop and name == "home":
            continue
        cur = ' aria-current="page"' if name == active else ""
        cls = ' class="key"' if (key_only_shop and name == "shop") else ""
        out.append(f'<li{cls}><a href="{L(t, href)}"{cur}>{t[key]}</a></li>')
    return "".join(out)


def font_faces(arabic):
    # English pages only show the word «العربية»: a ~2 KB subset of the same face draws it.
    css = (f'@font-face{{font-family:"Baloo Switch";font-weight:400 800;font-display:swap;'
           f'src:url("{v(FONT_AR_SWITCH)}") format("woff2");unicode-range:{ARABIC_RANGE}}}')
    css += (f'@font-face{{font-family:"Nunito";font-style:normal;font-weight:200 1000;font-display:swap;'
           f'src:url("{v(FONT_LATIN)}") format("woff2");unicode-range:{LATIN_RANGE}}}')
    if arabic:
        css += (f'@font-face{{font-family:"Baloo Bhaijaan 2";font-style:normal;font-weight:400 800;font-display:swap;'
                f'src:url("{v(FONT_AR)}") format("woff2");unicode-range:{ARABIC_RANGE}}}')
    return f"<style>{css}</style>"


def ga_snippet():
    # gtag() is a stub that queues into dataLayer from the first byte; gtag.js loads on
    # the first interaction (so a DM click right after landing still gets sent) or when
    # the browser is idle after DOMContentLoaded (1 s cap), whichever comes first. GA4 sends
    # with sendBeacon, so a hit queued just before navigating to Instagram still goes out.
    return f"""<script>
window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments);}}
if(!(navigator.webdriver||/bot|crawl|spider|headless|lighthouse/i.test(navigator.userAgent)||(screen.width===800&&screen.height===600))){{
gtag('js',new Date());gtag('config','{GA}',{{anonymize_ip:true,transport_type:'beacon'}});
var gl=function(){{if(gl.d)return;gl.d=1;var s=document.createElement('script');s.async=true;s.src='https://www.googletagmanager.com/gtag/js?id={GA}';document.head.appendChild(s);}};
['pointerdown','touchstart','keydown','scroll'].forEach(function(e){{addEventListener(e,gl,{{once:true,passive:true}});}});
addEventListener('DOMContentLoaded',function(){{(window.requestIdleCallback||function(f){{setTimeout(f,1000)}})(gl,{{timeout:1000}});}});
}}
</script>"""


def page_shell(t, *, title, description, canonical_path, body, extra_head="", active="",
               path_en="/", path_ar="/ar/", og_image=None, sticky=""):
    og_image = og_image or f"{BASE_URL}/assets/img/{'og-ar.jpg' if t['lang'] == 'ar' else 'og.jpg'}"
    ar = t["lang"] == "ar"
    alt_path = path_en if ar else path_ar
    preload = FONT_AR if ar else FONT_LATIN
    return f"""<!doctype html>
<html lang="{t['lang']}" dir="{t['dir']}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)}</title>
<meta name="description" content="{esc(description)}">
<link rel="canonical" href="{BASE_URL}{canonical_path}">
<link rel="alternate" hreflang="en" href="{BASE_URL}{path_en}">
<link rel="alternate" hreflang="ar" href="{BASE_URL}{path_ar}">
<link rel="alternate" hreflang="x-default" href="{BASE_URL}{path_en}">
<meta name="theme-color" content="#FAF7FC">
<meta name="color-scheme" content="light">
<link rel="icon" href="/favicon.ico" sizes="32x32">
<link rel="icon" href="/assets/img/icon.svg?v={asset_hash('assets/img/icon.svg')}" type="image/svg+xml">
<link rel="apple-touch-icon" href="/assets/img/icon-180.png">
<link rel="manifest" href="/site.webmanifest">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Loopaholic">
<meta property="og:url" content="{BASE_URL}{canonical_path}">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(description)}">
<meta property="og:image" content="{og_image}">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:locale" content="{t['og_locale']}">
<meta property="og:locale:alternate" content="{t['og_alt']}">
<meta name="twitter:card" content="summary_large_image">
<link rel="preload" href="{v(preload)}" as="font" type="font/woff2" crossorigin>
{font_faces(ar)}
<link rel="stylesheet" href="{v(CSS)}">
{ga_snippet()}
{extra_head}
</head>
<body>
<a class="skip" href="#main">{t['skip']}</a>
<header class="site-header">
  <div class="wrap bar">
    <a class="logo" href="{L(t, '/')}" aria-label="{t['home_label']}"><img src="{v('assets/img/lockup.svg')}" width="636" height="106" alt=""></a>
    <nav class="nav" aria-label="{t['nav_label']}"><ul role="list">{nav_links(t, active, key_only_shop=True)}</ul></nav>
    <a class="lang" href="{alt_path}" hreflang="{t['alt_lang']}" lang="{t['alt_lang']}">{t['alt_label']}</a>
    <details class="menu">
      <summary aria-label="{t['menu']}" aria-expanded="false">{ICONS['menu']}{ICONS['close']}</summary>
      <nav class="menu-sheet" aria-label="{t['menu_label']}"><ul role="list">{nav_links(t, active)}</ul></nav>
    </details>
  </div>
</header>
<main id="main" tabindex="-1">
{body}
</main>
{footer(t, alt_path)}
{sticky}
<script src="{v(JS)}" defer></script>
</body>
</html>
"""


def footer(t, alt_path):
    return f"""<footer class="site-footer">
  <div class="wrap">
    <div class="foot-grid">
      <div class="foot-brand">
        <img src="{v('assets/img/lockup-white.svg')}" width="636" height="106" alt="Loopaholic">
        <p>{t['footer_tagline']}</p>
      </div>
      <nav aria-labelledby="f-shop"><h2 id="f-shop">{t['footer_shop']}</h2><ul role="list">
        <li><a href="{L(t, '/shop/')}">{t['nav_shop']}</a></li>
        <li><a href="{L(t, '/custom-orders/')}">{t['nav_custom']}</a></li></ul></nav>
      <nav aria-labelledby="f-help"><h2 id="f-help">{t['footer_info']}</h2><ul role="list">
        <li><a href="{L(t, '/shipping/')}">{t['nav_shipping']}</a></li>
        <li><a href="{L(t, '/faq/')}">{t['nav_faq']}</a></li>
        <li><a href="{L(t, '/about/')}">{t['nav_about']}</a></li></ul></nav>
      <nav aria-labelledby="f-follow"><h2 id="f-follow">{t['footer_follow']}</h2><ul role="list">
        <li><a href="{INSTAGRAM}">{handle(t)}</a></li></ul></nav>
    </div>
    <div class="foot-base"><span>© <span dir="ltr">{YEAR}</span> Loopaholic</span><a class="foot-lang" href="{alt_path}" hreflang="{t['alt_lang']}" lang="{t['alt_lang']}">{t['alt_label']}</a></div>
  </div>
</footer>"""

# -------------------------------------------------------------- JSON-LD ----


def ld(data):
    return f'<script type="application/ld+json">{json.dumps(data, ensure_ascii=False)}</script>'


def breadcrumb_ld(t, items):
    return ld({"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": i + 1, "name": name, "item": f"{BASE_URL}{path}"} for i, (name, path) in enumerate(items)]})


def product_jsonld(p, t):
    path = L(t, f"/shop/{p['slug']}/")
    data = {
        "@context": "https://schema.org",
        "@type": "Product",
        "name": p["title"][t["lang"]],
        "description": p["description"][t["lang"]],
        "image": f"{BASE_URL}{img_base(p['id'])}/w1200.jpg",
        "url": f"{BASE_URL}{path}",
        "sku": p["id"],
        "brand": {"@type": "Brand", "name": "Loopaholic"},
        "category": CATEGORY_LABEL[p["category"]]["en"],
        "color": ", ".join(p["colors"]),
    }
    if SHOW_UNCONFIRMED_DETAILS:
        lo, hi = p["lead_time_days"]
        data["additionalProperty"] = [
            {"@type": "PropertyValue", "name": "Size", "value": p["size_approx"]},
            {"@type": "PropertyValue", "name": "Made-to-order time", "value": f"{lo}–{hi} days"},
        ]
    # An Offer is only emitted with a real checkout link. "Price on request" offers
    # without price/priceCurrency are invalid in Google's Rich Results test.
    if p.get("stripe_payment_link"):
        data["offers"] = {
            "@type": "Offer", "url": p["stripe_payment_link"],
            "availability": "https://schema.org/MadeToOrder" if p.get("made_to_order") else "https://schema.org/InStock",
            "itemCondition": "https://schema.org/NewCondition",
        }
    return ld(data)

# --------------------------------------------------------------- pages ----


def build_home(t, outdir):
    path_en, path_ar = "/", "/ar/"
    hero = BY_ID[HOME_HERO_ID]
    featured = [BY_ID[i] for i in FEATURED_IDS]
    body = f'''<section class="hero">
  <div class="wrap hero-grid">
    <div>
      <h1>{t['hero_h1']}</h1>
      <p class="lead">{t['hero_lead']}</p>
      <div class="actions">
        <a class="btn btn-primary" href="{L(t, '/shop/')}">{t['cta_shop']}</a>
        <a class="text-link" href="#how">{t['how_link']}</a>
      </div>
    </div>
    <div>
      <div class="gallery">
        <a class="tile" href="{L(t, '/shop/' + hero['slug'] + '/')}" aria-label="{esc(hero['title'][t['lang']])}">{picture(hero['id'], '', '(min-width: 52.5em) 34rem, 92vw', eager=True)}</a>
        {loupe(hero['id'], t)}
      </div>
    </div>
  </div>
</section>
<section class="section" aria-labelledby="featured-h">
  <div class="wrap">
    <div class="head"><h2 id="featured-h">{t['featured_h']}</h2></div>
    {grid(featured, t)}
    <p class="more"><a class="btn btn-secondary" href="{L(t, '/shop/')}">{t['featured_more']}</a></p>
  </div>
</section>
<section class="section band" id="how" aria-labelledby="how-h">
  <div class="wrap">
    <div class="head"><h2 id="how-h">{t['how_h']}</h2><p class="muted measure">{t['how_lead']}</p></div>
    {steps(t['how'], row=True)}
  </div>
</section>
<section class="section" aria-labelledby="made-h">
  <div class="wrap split">
    <div class="stack">
      <h2 id="made-h">{t['made_h']}</h2>
      <p>{t['made_b']}</p>
      <p><a class="text-link" href="{L(t, '/about/')}">{t['made_link']}</a></p>
    </div>
    <div class="stack">
      <h2>{t['follow_h']}</h2>
      <p class="muted">{t['follow_b']}</p>
      <p><a class="btn btn-secondary" href="{INSTAGRAM}">{ICONS['instagram']}<span>{with_handle(t, t['follow_cta'])}</span></a></p>
    </div>
  </div>
</section>'''
    org = {
        "@context": "https://schema.org", "@type": "Organization", "@id": f"{BASE_URL}/#org",
        "name": "Loopaholic", "url": BASE_URL, "logo": f"{BASE_URL}/assets/img/icon-512.png",
        "sameAs": [INSTAGRAM],
        "areaServed": [{"@type": "Country", "name": "Lebanon"}, {"@type": "Place", "name": "Gulf countries"}, {"@type": "Place", "name": "Worldwide"}],
    }
    html_ = page_shell(t, title=f"{t['site_name']} | Handmade Crochet, Made to Order" if t["lang"] == "en" else f"{t['site_name']} | كروشيه يدوي عند الطلب",
                       description=t["meta_home_desc"], canonical_path=path_en if t["lang"] == "en" else path_ar,
                       body=body, extra_head=ld(org), active="home", path_en=path_en, path_ar=path_ar)
    write(outdir, "index.html", html_)


def build_shop(t, outdir):
    path_en, path_ar = "/shop/", "/ar/shop/"
    groups = [(g, [p for p in PRODUCTS if p["category"] in cs]) for g, cs in SHOP_GROUPS]
    groups = [(g, items) for g, items in groups if items]
    chips = "".join(f'<li><a class="chip" href="#cat-{g}">{group_label(g, t["lang"])}</a></li>' for g, _ in groups)
    sections = []
    for n, (g, items) in enumerate(groups):
        mixed = len({p["category"] for p in items}) > 1
        sections.append(f'<section class="cat" id="cat-{g}" aria-labelledby="h-{g}"><h2 id="h-{g}">{group_label(g, t["lang"])}</h2>{grid(items, t, eager_first=2 if n == 0 else 0, meta=mixed)}</section>')
    body = f'''<div class="wrap page-head">
  <h1>{t['shop_title']}</h1>
  <p class="lead">{t['shop_lead']}</p>
</div>
<nav class="chips-bar" aria-label="{t['chips_label']}"><div class="wrap"><ul class="chips" role="list">{chips}</ul></div></nav>
<div class="wrap section shop-body">
  {''.join(sections)}
  <div class="cant-find">
    <h2>{t['cant_find_h']}</h2>
    <p>{t['cant_find_b']} <a href="{L(t, '/custom-orders/')}">{t['cant_find_link']}</a></p>
  </div>
</div>'''
    crumbs = breadcrumb_ld(t, [(t["breadcrumb_home"], L(t, "/")), (t["breadcrumb_shop"], L(t, "/shop/"))])
    html_ = page_shell(t, title=f"Shop | {t['site_name']}" if t["lang"] == "en" else f"المتجر | {t['site_name']}",
                       description=t["meta_shop_desc"], canonical_path=path_en if t["lang"] == "en" else path_ar,
                       body=body, extra_head=crumbs, active="shop", path_en=path_en, path_ar=path_ar)
    write(outdir, "shop/index.html", html_)


def build_product(p, t, outdir):
    path_en, path_ar = f"/shop/{p['slug']}/", f"/ar/shop/{p['slug']}/"
    title = p["title"][t["lang"]]
    desc = p["description"][t["lang"]]
    cat = CATEGORY_LABEL[p["category"]][t["lang"]]
    ctx = f"{{product:'{p['slug']}'}}"
    wa_text = (f"Hi! I'd like to order: {p['title']['en']} ({BASE_URL}{path_en}). My area: "
               if t["lang"] == "en" else f"مرحبا! بدي اطلب: {p['title']['ar']} ({BASE_URL}{path_ar}). منطقتي: ")

    facts = [(t["colors_label"], colors_text(p, t))]
    if SHOW_UNCONFIRMED_DETAILS:
        lo, hi = p["lead_time_days"]
        facts = [(t["size_label"], size_text(p, t))] + facts + [(t["lead_label"], f"{lo}–{hi} {t['days']}")]
    facts_html = "".join(f"<div><dt>{k}</dt><dd>{esc(val)}</dd></div>" for k, val in facts)

    intl = ""
    if p.get("stripe_payment_link"):
        intl = (f'<div class="aside"><h2>{t["order_intl_title"]}</h2><p>{t["order_intl_body_live"]}</p>'
                f'<p><a class="btn btn-secondary" href="{esc(p["stripe_payment_link"])}" {ga("buy_click", ctx)}>{t["buy_now"]}</a></p></div>')

    pool = [x for x in PRODUCTS if x["id"] != p["id"] and x["id"] not in NOT_FEATURED]
    others = [x for x in pool if x["category"] == p["category"]][:4]
    if len(others) < 4:
        others += [x for x in pool if x not in others][: 4 - len(others)]
    note = t["order_note_wa"] if HAS_WHATSAPP else t["order_note_ig"]

    body = f'''<div class="wrap">
  <nav aria-label="{t['breadcrumb_label']}"><ol class="crumbs" role="list">
    <li><a href="{L(t, '/shop/')}">{t['breadcrumb_shop']}</a></li>
    <li><a href="{L(t, '/shop/')}#cat-{GROUP_OF[p['category']]}">{group_label(GROUP_OF[p['category']], t['lang'])}</a></li>
  </ol></nav>
  <div class="pdp">
    <div>
      <div class="gallery">
        <div class="tile">{picture(p['id'], desc + t['crop_note'] if p['id'] in CROPPED else desc, '(min-width: 52.5em) 55vw, 100vw', eager=True)}</div>
        {loupe(p['id'], t, interactive=True)}
      </div>
      <p class="loupe-hint" aria-hidden="true"><span class="hint-hover">{t['loupe_hint']}</span><span class="hint-touch">{t['loupe_hint_touch']}</span></p>
    </div>
    <div class="pdp-info">
      <h1>{esc(title)}</h1>
      <p>{esc(desc)}</p>
      <dl class="facts">{facts_html}</dl>
      <div class="order">
        <p class="price-note">{t['price_note']}</p>
        <div class="actions">{order_cta(t, ctx, wa_text, cta_id="order-cta")}</div>
        <p class="note">{with_handle(t, note)}</p>
      </div>
      <div class="aside" id="how">
        <h2>{t['how_h']}</h2>
        {steps(t['how'], compact=True, level="h3")}
      </div>
      <div class="aside">
        <h2>{t['delivery_h']}</h2>
        <p>{t['delivery_b1']}</p>
        <p>{t['delivery_b2']} <a href="{L(t, '/shipping/')}">{t['delivery_link']}</a></p>
      </div>
      {intl}
    </div>
  </div>
</div>
<section class="section related" aria-labelledby="rel-h">
  <div class="wrap">
    <h2 id="rel-h">{t['related_title']}</h2>
    {grid(others, t)}
  </div>
</section>'''
    sticky = (f'<div class="sticky-cta" aria-hidden="true"><span class="name">{esc(title)}</span>'
              f'{order_cta(t, ctx, wa_text, block=False, secondary=False).replace("<a ", "<a tabindex=" + chr(34) + "-1" + chr(34) + " ", 1)}</div>')
    head = product_jsonld(p, t) + "\n" + breadcrumb_ld(t, [(t["breadcrumb_home"], L(t, "/")), (t["breadcrumb_shop"], L(t, "/shop/")), (title, L(t, f"/shop/{p['slug']}/"))])
    html_ = page_shell(t, title=f"{title} | {t['site_name']}", description=desc,
                       canonical_path=path_en if t["lang"] == "en" else path_ar,
                       body=body, extra_head=head, active="shop", path_en=path_en, path_ar=path_ar,
                       og_image=f"{BASE_URL}{img_base(p['id'])}/og.jpg", sticky=sticky)
    write(outdir, f"shop/{p['slug']}/index.html", html_)


def build_custom(t, outdir):
    path_en, path_ar = "/custom-orders/", "/ar/custom-orders/"
    wa_text = "Hi! I'd like to ask about a custom order." if t["lang"] == "en" else "مرحبا، أريد الاستفسار عن طلب خاص."
    examples = "".join(
        f'<figure><div class="tile">{picture(pid, t[key], "(min-width: 40em) 17rem, 46vw")}</div><figcaption>{t[key]}</figcaption></figure>'
        for pid, key in CUSTOM_EXAMPLES)
    ctx = "{page:'custom-orders'}"
    note = with_handle(t, t['order_note_wa'] if HAS_WHATSAPP else t['order_note_short'])
    body = f'''<div class="wrap custom-layout">
  <div class="page-head c-head">
    <h1>{t['custom_title']}</h1>
    <p class="lead">{t['custom_lead']}</p>
    <div class="actions head-cta">{order_cta(t, ctx, wa_text, label_key="custom_cta")}</div>
    <p class="muted small">{note}</p>
  </div>
  <div class="prose c-body">
    <p>{t['custom_body_1']}</p>
    <p>{t['custom_body_2']}</p>
  </div>
  <div class="examples c-ex">{examples}</div>
  <div class="prose c-how">
    <h2>{t['custom_how_title']}</h2>
    {steps(t['custom_how'])}
    <div class="actions cta-block">{order_cta(t, ctx, wa_text, label_key="custom_cta", variant="btn-primary btn-quiet-wide")}</div>
  </div>
</div>'''
    sticky = (f'<div class="sticky-cta" aria-hidden="true"><span class="name">{t["custom_title"]}</span>'
              f'{order_cta(t, ctx, wa_text, label_key="custom_cta", block=False, secondary=False).replace("<a ", "<a tabindex=" + chr(34) + "-1" + chr(34) + " ", 1)}</div>')
    html_ = page_shell(t, title=f"{t['custom_title'] if t['lang'] == 'ar' else 'Custom Orders'} | {t['site_name']}", description=t['custom_lead'],
                       canonical_path=path_en if t["lang"] == "en" else path_ar,
                       body=body, active="custom", path_en=path_en, path_ar=path_ar, sticky=sticky)
    write(outdir, "custom-orders/index.html", html_)


def how_aside(t):
    return (f'<aside class="side" aria-labelledby="side-h"><h2 id="side-h">{t["how_h"]}</h2>'
            f'{steps(t["how"], compact=True)}'
            f'<p><a class="btn btn-primary" href="{L(t, "/shop/")}">{t["cta_shop"]}</a></p></aside>')


def prose_page(t, outdir, *, rel, title_text, head_title, lead, inner, description, active, extra_head="", aside=""):
    path_en, path_ar = f"/{rel}/", f"/ar/{rel}/"
    body = f'''<div class="wrap page-head">
  <h1>{head_title}</h1>
  {f'<p class="lead">{lead}</p>' if lead else ''}
</div>
<div class="wrap section flush prose-layout">
  <div class="prose">
{inner}
  </div>
  {aside}
</div>'''
    html_ = page_shell(t, title=title_text, description=description,
                       canonical_path=path_en if t["lang"] == "en" else path_ar,
                       body=body, extra_head=extra_head, active=active, path_en=path_en, path_ar=path_ar)
    write(outdir, f"{rel}/index.html", html_)


def build_shipping(t, outdir):
    inner = "\n".join(f"<h2>{t[h]}</h2>\n<p>{t[b]}</p>" for h, b in [
        ("shipping_lebanon_h", "shipping_lebanon_b"), ("shipping_gulf_h", "shipping_gulf_b"),
        ("shipping_intl_h", "shipping_intl_b"), ("shipping_returns_h", "delivery_b2"), ("shipping_note_h", "shipping_note_b")])
    prose_page(t, outdir, rel="shipping", title_text=f"{t['shipping_title']} | {t['site_name']}", head_title=t["shipping_title"],
               lead=t["shipping_lead"], inner=inner, description=t["meta_shipping_desc"], active="shipping", aside=how_aside(t))


def build_about(t, outdir):
    trio = "".join(f'<li class="tile">{picture(pid, "", "(min-width: 40em) 13rem, 30vw")}</li>' for pid in ("p066", "p150", "p013"))
    inner = (f'<ul class="trio" role="list">{trio}</ul>\n'
             f"<p>{t['about_body_1']}</p>\n<p>{t['about_body_2']}</p>\n"
             f"<p>{t['about_body_3']} <a href=\"{INSTAGRAM}\">{handle(t)}</a></p>")
    prose_page(t, outdir, rel="about", title_text=f"{t['about_title']} | {t['site_name']}", head_title=t["about_title"],
               lead=t["about_lead"], inner=inner, description=t["about_body_1"][:150], active="about", aside=how_aside(t))


def build_faq(t, outdir):
    inner = "\n".join(f'<div class="qa"><h2>{esc(q)}</h2><p>{esc(a)}</p></div>' for q, a in t["faq"])
    faq_ld = ld({"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in t["faq"]]})
    prose_page(t, outdir, rel="faq", title_text=f"{t['faq_title']} | {t['site_name']}", head_title=t["faq_title"],
               lead=t["faq_lead"], inner=inner, description=t["faq"][0][1][:150], active="faq", extra_head=faq_ld, aside=how_aside(t))


def build_404(outdir):
    """Bilingual 404 (GitHub Pages serves /404.html with status 404). English shell,
    Arabic block marked lang="ar" dir="rtl"; noindex."""
    en, ar = T["en"], T["ar"]

    def block(t, tag):
        links = "".join(f'<li><a class="text-link" href="{L(t, href)}">{t[key]}</a></li>' for key, href in
                        [("nav_shop", "/shop/"), ("nav_home", "/"), ("nav_faq", "/faq/")])
        return (f'<div lang="{t["lang"]}" dir="{t["dir"]}" class="stack"><{tag}>{t["nf_title"]}</{tag}><p class="muted">{t["nf_body"]}</p>'
                f'<ul role="list">{links}</ul><p>{esc(t["nf_contact"])} <a href="{INSTAGRAM_DM}">{handle(t)}</a></p></div>')
    body = f'''<div class="wrap lost"><div class="lost-ring" aria-hidden="true"></div><div class="lost-grid">{block(en, "h1")}{block(ar, "h2")}</div></div>'''
    html_ = page_shell(en, title="Page not found | Loopaholic", description="This page isn’t here.", canonical_path="/404.html",
                       body=body, extra_head='<meta name="robots" content="noindex">')
    # no canonical/hreflang on the 404 page
    html_ = re.sub(r'<link rel="(canonical|alternate)"[^>]*>\n', "", html_)
    html_ = html_.replace(font_faces(False), font_faces(True))
    write(outdir, "404.html", html_)


LATIN_IN_AR = ("Whish", "Loopaholic", "Instagram", INSTAGRAM_HANDLE)


def isolate_latin(html_):
    """On Arabic pages, wrap Latin names in running text in <bdi dir="ltr"> (text nodes of
    <body> only: never inside attributes, scripts, or an existing bdi)."""
    head, sep, body = html_.partition("<body>")
    parts = re.split(r"(<script.*?</script>|<bdi[^>]*>.*?</bdi>|<[^>]+>)", body, flags=re.S)
    for i in range(0, len(parts), 2):
        for word in LATIN_IN_AR:
            parts[i] = re.sub(r"(?<![\w@.])" + re.escape(word) + r"(?![\w.])", f'<bdi dir="ltr">{word}</bdi>', parts[i])
    return head + sep + "".join(parts)


def write(outdir, relpath, content):
    full = os.path.join(outdir, relpath)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    if relpath.endswith(".html") and '<html lang="ar"' in content:
        content = isolate_latin(content)
    if relpath.endswith(".html"):
        RENDER_PROBLEMS.extend(check_rendered(os.path.relpath(full, ROOT), content))
    with open(full, "w", encoding="utf-8") as f:
        f.write(content)


def build_sitemap(outdir):
    urls = ["/", "/shop/", "/custom-orders/", "/shipping/", "/about/", "/faq/"]
    urls += [f"/shop/{p['slug']}/" for p in PRODUCTS]
    urls += ["/ar/", "/ar/shop/", "/ar/custom-orders/", "/ar/shipping/", "/ar/about/", "/ar/faq/"]
    urls += [f"/ar/shop/{p['slug']}/" for p in PRODUCTS]
    lastmod = CATALOG.get("updated", "2026-10-08")
    entries = "\n".join(f"  <url><loc>{BASE_URL}{u}</loc><lastmod>{lastmod}</lastmod></url>" for u in urls)
    xml = f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{entries}\n</urlset>\n'
    write(outdir, "sitemap.xml", xml)


INDEXNOW_KEY = "ea77b6da080977a1becb866c3314f534"  # same key used on every other Taktek domain


def build_robots(outdir):
    write(outdir, "robots.txt", f"User-agent: *\nAllow: /\n\nSitemap: {BASE_URL}/sitemap.xml\n")
    write(outdir, f"{INDEXNOW_KEY}.txt", INDEXNOW_KEY + "\n")


def build_cname(outdir):
    write(outdir, "CNAME", DOMAIN + "\n")


def build_manifest(outdir):
    write(outdir, "site.webmanifest", json.dumps({
        "name": "Loopaholic", "short_name": "Loopaholic", "start_url": "/", "display": "browser",
        "background_color": "#FAF7FC", "theme_color": "#FAF7FC",
        "icons": [{"src": "/assets/img/icon-192.png", "sizes": "192x192", "type": "image/png"},
                  {"src": "/assets/img/icon-512.png", "sizes": "512x512", "type": "image/png", "purpose": "any"},
                  {"src": "/assets/img/icon-maskable-512.png", "sizes": "512x512", "type": "image/png", "purpose": "maskable"}],
    }, indent=2) + "\n")


def main():
    problems = check_claims()
    if problems:
        sys.exit("Build stopped: forbidden claim(s) in catalog/copy (owner rule R2b):\n  " + "\n  ".join(problems))
    outdir = ROOT
    build_css()
    build_js()
    for lang in ("en", "ar"):
        t = T[lang]
        sub = outdir if lang == "en" else os.path.join(outdir, "ar")
        build_home(t, sub)
        build_shop(t, sub)
        for p in PRODUCTS:
            build_product(p, t, sub)
        build_custom(t, sub)
        build_shipping(t, sub)
        build_about(t, sub)
        build_faq(t, sub)
    build_404(outdir)
    build_sitemap(outdir)
    build_robots(outdir)
    build_cname(outdir)
    build_manifest(outdir)
    if RENDER_PROBLEMS:
        sys.exit("Build stopped: forbidden claim(s) in rendered pages (owner rule R2b):\n  " + "\n  ".join(RENDER_PROBLEMS))
    print(f"Built {len(PRODUCTS)} products × 2 languages (+404). SHOW_UNCONFIRMED_DETAILS={SHOW_UNCONFIRMED_DETAILS}, HAS_WHATSAPP={HAS_WHATSAPP}")


if __name__ == "__main__":
    main()
