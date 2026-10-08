#!/usr/bin/env python3
"""Generates the static Loopaholic shop site from catalog.json.

Run `python3 build.py` after any catalog.json edit, then commit the
generated HTML/sitemap/robots files alongside it.
"""
import json
import os
import shutil

ROOT = os.path.dirname(os.path.abspath(__file__))
DOMAIN = "loopaholiccrochet.com"
BASE_URL = f"https://{DOMAIN}"
GA = "G-EQ20EYFSY3"
INSTAGRAM = "https://instagram.com/loopaholic.crochet"
INSTAGRAM_HANDLE = "@loopaholic.crochet"
# No business WhatsApp number is confirmed yet (ask in workstream log).
# Set this once Rana/Nizar give one; WhatsApp buttons fall back to the
# Instagram DM link until then.
WHATSAPP_NUMBER = None  # e.g. "+9613XXXXXX"

CATALOG = json.load(open(os.path.join(ROOT, "catalog.json"), encoding="utf-8"))
PRODUCTS = CATALOG["products"]

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

def whatsapp_link(text):
    if not WHATSAPP_NUMBER:
        return INSTAGRAM
    num = WHATSAPP_NUMBER.replace("+", "").replace(" ", "")
    from urllib.parse import quote
    return f"https://wa.me/{num}?text={quote(text)}"

# ---------------------------------------------------------------- i18n ----
T = {
    "en": {
        "lang": "en", "dir": "ltr", "alt_lang": "ar", "alt_label": "العربية", "alt_path": "/ar",
        "site_name": "Loopaholic",
        "tagline": "Handmade crochet, made to order",
        "nav_home": "Home", "nav_shop": "Shop", "nav_custom": "Custom Orders",
        "nav_shipping": "Shipping", "nav_about": "About", "nav_faq": "FAQ",
        "hero_lead": "Every piece is crocheted by hand, one stitch at a time — amigurumi plushies, dolls, flowers and baby gifts, made to order and shipped worldwide.",
        "cta_shop": "Shop the collection", "cta_instagram": "See more on Instagram",
        "shop_title": "Shop", "shop_lead": "Every piece below is made to order by hand. Message us on WhatsApp or Instagram for the price.",
        "price_cta": "Ask for the price on WhatsApp",
        "badge_handmade": "Handmade in Lebanon", "badge_handmade_d": "Every piece is crocheted by hand, start to finish.",
        "badge_order": "Made to order", "badge_order_d": "We start your piece once you order — no stock sitting on a shelf.",
        "badge_ship": "Ships worldwide", "badge_ship_d": "Lebanon, the Gulf, and internationally.",
        "view_product": "View",
        "breadcrumb_home": "Home", "breadcrumb_shop": "Shop",
        "size_label": "Size", "colors_label": "Colors", "lead_label": "Made-to-order time",
        "days": "days",
        "order_lebanon_title": "Order in Lebanon",
        "order_lebanon_body": "Message us on WhatsApp or Instagram to confirm color, size and price, then pay by Whish or cash on delivery.",
        "order_whatsapp": "Order on WhatsApp", "order_instagram": "Message on Instagram",
        "order_intl_title": "Order internationally",
        "order_intl_body_pending": "International checkout is almost ready — message us on Instagram for now and we’ll quote shipping and take your order by hand.",
        "order_intl_body_live": "Pay securely online — shipping is calculated at checkout.",
        "buy_now": "Buy now",
        "related_title": "You might also like",
        "custom_title": "Custom Orders",
        "custom_lead": "Want a color swap, a name, or a piece that doesn’t exist yet? We take commissions.",
        "custom_body_1": "Most of our plushies and dolls can be made in different colors or sizes on request. We also make fully custom pieces — a name in crochet letters, a character, or a gift built around an idea you bring us.",
        "custom_body_2": "Two examples below: crochet letters for a nursery, and a small flower keychain made as a party favor.",
        "custom_how_title": "How it works",
        "custom_how_1": "Message us on Instagram or WhatsApp with what you have in mind (a photo or description helps).",
        "custom_how_2": "We confirm the design, price and a made-to-order time — custom pieces usually take longer than the shop catalog.",
        "custom_how_3": "You pay a deposit to start, we crochet it by hand, and send photos before it ships.",
        "custom_cta": "Start a custom order",
        "shipping_title": "Shipping",
        "shipping_lebanon_h": "Lebanon",
        "shipping_lebanon_b": "Order on WhatsApp or Instagram. Pay by Whish transfer or cash on delivery. Delivery time depends on your area and how long the piece takes to make — we’ll confirm both when you order.",
        "shipping_gulf_h": "Gulf countries",
        "shipping_gulf_b": "We ship to the UAE, Saudi Arabia, Kuwait, Qatar, Bahrain and Oman. Shipping cost is quoted on WhatsApp or Instagram once we know your city and the pieces you want — we haven’t fixed flat rates yet.",
        "shipping_intl_h": "Everywhere else",
        "shipping_intl_b": "We ship internationally. Shipping cost is quoted on WhatsApp or Instagram until our checkout can calculate it automatically.",
        "shipping_note_h": "Good to know",
        "shipping_note_b": "Every piece is made to order, so shipping starts after the made-to-order time on the product page, not the day you order. Customs fees outside Lebanon are the buyer’s responsibility.",
        "about_title": "About the craft",
        "about_body_1": "Loopaholic makes amigurumi — crocheted, stuffed figures — and crochet flowers entirely by hand, one stitch at a time. Nothing is machine-made or mass-produced: every plushie, doll and flower on this site is handmade in Lebanon and made to order.",
        "about_body_2": "Because each piece is made by hand after you order it, small variations — a slightly different stitch, a shade of yarn — are part of what makes it one of a kind, not a flaw.",
        "about_body_3": "Follow the latest pieces and works in progress on Instagram.",
        "faq_title": "FAQ",
        "faq": [
            ("How long does an order take to make?", "Most plushies and dolls take 10–28 days to crochet, and flowers take 5–12 days — the exact range is on each product page. Custom orders usually take a bit longer. We’ll confirm a date when you order."),
            ("Do you ship outside Lebanon?", "Yes — to the Gulf and internationally. Shipping cost is quoted by hand on WhatsApp or Instagram for now, based on your location and what you’re ordering."),
            ("How do I pay?", "In Lebanon: Whish transfer or cash on delivery. Internationally: online card payment (coming soon) — for now, message us and we’ll arrange it."),
            ("How much does a piece cost?", "We don’t list prices on the site — message us on WhatsApp or Instagram with the piece you want and we’ll confirm a price before you order."),
            ("Can I change the colors?", "Usually yes. Message us with the colors you’d like and we’ll confirm if it works for that piece."),
            ("What are the pieces made from?", "Message us on WhatsApp or Instagram — we’ll confirm the materials for the specific piece you’re asking about."),
            ("Can I return or exchange a piece?", "Because every piece is made to order just for you, we can’t accept returns for a change of mind. If a piece arrives damaged or wrong, message us within 48 hours and we’ll make it right."),
            ("Is this safe for babies and small children?", "We haven’t completed safety testing for baby items, so we don’t make any safety or age claim. Message us if you have questions before ordering for an infant, and always supervise young children with any small handmade item."),
        ],
        "footer_tagline": "Handmade crochet from Lebanon, shipped worldwide.",
        "footer_shop": "Shop", "footer_info": "Info", "footer_follow": "Follow",
        "meta_home_desc": "Handmade amigurumi plushies, dolls, flowers and baby gifts, crocheted to order in Lebanon and shipped to the Gulf and worldwide.",
        "meta_shop_desc": "Browse handmade crochet plushies, dolls, flowers and gifts, made to order and shipped from Lebanon worldwide.",
    },
    "ar": {
        "lang": "ar", "dir": "rtl", "alt_lang": "en", "alt_label": "English", "alt_path": "",
        "site_name": "لوباهوليك",
        "tagline": "كروشيه يدوي، يُصنع عند الطلب",
        "nav_home": "الرئيسية", "nav_shop": "المتجر", "nav_custom": "طلب خاص",
        "nav_shipping": "الشحن", "nav_about": "عن الحرفة", "nav_faq": "الأسئلة الشائعة",
        "hero_lead": "كل قطعة مكروشية يدويًا، غرزة بعد غرزة — حيوانات محشوة وعرائس وزهور وهدايا أطفال، تُصنع عند الطلب وتُشحن حول العالم.",
        "cta_shop": "تصفّح المجموعة", "cta_instagram": "المزيد على إنستغرام",
        "shop_title": "المتجر", "shop_lead": "كل قطعة أدناه تُصنع يدويًا عند الطلب. راسلينا على واتساب أو إنستغرام لمعرفة السعر.",
        "price_cta": "اسألينا عن السعر على واتساب",
        "badge_handmade": "مصنوع يدويًا في لبنان", "badge_handmade_d": "كل قطعة مكروشية بالكامل باليد.",
        "badge_order": "تُصنع عند الطلب", "badge_order_d": "نبدأ قطعتك بعد الطلب — لا مخزون جاهز على الرف.",
        "badge_ship": "شحن عالمي", "badge_ship_d": "لبنان، دول الخليج، وحول العالم.",
        "view_product": "عرض",
        "breadcrumb_home": "الرئيسية", "breadcrumb_shop": "المتجر",
        "size_label": "القياس", "colors_label": "الألوان", "lead_label": "مدة التصنيع",
        "days": "أيام",
        "order_lebanon_title": "الطلب داخل لبنان",
        "order_lebanon_body": "راسلينا على واتساب أو إنستغرام لتأكيد اللون والقياس والسعر، ثم الدفع عبر Whish أو الدفع عند التسليم.",
        "order_whatsapp": "الطلب عبر واتساب", "order_instagram": "راسلينا على إنستغرام",
        "order_intl_title": "الطلب من خارج لبنان",
        "order_intl_body_pending": "الدفع الإلكتروني الدولي أصبح جاهزًا تقريبًا — راسلينا الآن على إنستغرام وسنحدد تكلفة الشحن ونأخذ طلبك يدويًا.",
        "order_intl_body_live": "الدفع الإلكتروني الآمن متاح — تُحسب تكلفة الشحن عند الدفع.",
        "buy_now": "اشترِ الآن",
        "related_title": "قد يعجبك أيضًا",
        "custom_title": "طلب خاص",
        "custom_lead": "تريدين تغيير لون، إضافة اسم، أو قطعة غير موجودة بعد؟ نستقبل الطلبات الخاصة.",
        "custom_body_1": "معظم القطع والعرائس يمكن تصنيعها بألوان أو قياسات مختلفة عند الطلب. كما نصنع قطعًا خاصة بالكامل — اسم بحروف كروشيه، شخصية، أو هدية مبنية على فكرتك.",
        "custom_body_2": "مثالان أدناه: حروف كروشيه لغرفة طفل، وسلسلة مفاتيح على شكل زهرة صُنعت كهدية حفلة.",
        "custom_how_title": "كيف تطلبين",
        "custom_how_1": "راسلينا على إنستغرام أو واتساب بما تريدينه (صورة أو وصف يساعد).",
        "custom_how_2": "نؤكد التصميم والسعر ومدة التصنيع — الطلبات الخاصة تستغرق غالبًا أطول من قطع المتجر.",
        "custom_how_3": "تدفعين دفعة أولى للبدء، نصنع القطعة يدويًا، ونرسل صورًا قبل الشحن.",
        "custom_cta": "ابدئي طلبًا خاصًا",
        "shipping_title": "الشحن",
        "shipping_lebanon_h": "لبنان",
        "shipping_lebanon_b": "الطلب عبر واتساب أو إنستغرام. الدفع عبر تحويل Whish أو الدفع عند التسليم. مدة التوصيل تعتمد على منطقتك ومدة تصنيع القطعة — نؤكد الاثنين عند الطلب.",
        "shipping_gulf_h": "دول الخليج",
        "shipping_gulf_b": "نشحن إلى الإمارات والسعودية والكويت وقطر والبحرين وعُمان. تكلفة الشحن تُحدد عبر واتساب أو إنستغرام بعد معرفة مدينتك والقطع المطلوبة — لم نحدد أسعارًا ثابتة بعد.",
        "shipping_intl_h": "باقي دول العالم",
        "shipping_intl_b": "نشحن دوليًا. تكلفة الشحن تُحدد عبر واتساب أو إنستغرام حتى يصبح الدفع الإلكتروني قادرًا على حسابها تلقائيًا.",
        "shipping_note_h": "جيد أن تعرفي",
        "shipping_note_b": "كل قطعة تُصنع عند الطلب، فتبدأ مدة الشحن بعد مدة التصنيع المذكورة في صفحة المنتج، لا من يوم الطلب. رسوم الجمارك خارج لبنان على مسؤولية المشتري.",
        "about_title": "عن الحرفة",
        "about_body_1": "تصنع لوباهوليك قطع الأميغورومي — شخصيات كروشيه محشوة — وزهور الكروشيه بالكامل باليد، غرزة بعد غرزة. لا شيء مصنوع بالآلة أو بكميات كبيرة: كل حيوان محشو وعروسة وزهرة في هذا المتجر مصنوع يدويًا في لبنان وعند الطلب.",
        "about_body_2": "لأن كل قطعة تُصنع يدويًا بعد الطلب، الاختلافات الصغيرة — غرزة مختلفة قليلًا، درجة لون — هي ما يجعلها فريدة، لا عيبًا.",
        "about_body_3": "تابعي أحدث القطع والأعمال الجارية على إنستغرام.",
        "faq_title": "الأسئلة الشائعة",
        "faq": [
            ("كم تستغرق مدة تصنيع الطلب؟", "معظم القطع المحشوة والعرائس تستغرق 10–28 يومًا للكروشيه، والزهور 5–12 يومًا — المدة الدقيقة مذكورة في صفحة كل منتج. الطلبات الخاصة تستغرق غالبًا أطول. نؤكد تاريخًا عند الطلب."),
            ("هل تشحنون خارج لبنان؟", "نعم — إلى دول الخليج وحول العالم. تكلفة الشحن تُحدد يدويًا عبر واتساب أو إنستغرام حاليًا، حسب موقعك وما تطلبينه."),
            ("كيف أدفع؟", "داخل لبنان: تحويل Whish أو الدفع عند التسليم. دوليًا: الدفع الإلكتروني بالبطاقة (قريبًا) — حاليًا راسلينا وسنرتب الدفع."),
            ("كم تكلفة القطعة؟", "لا نضع الأسعار على الموقع — راسلينا على واتساب أو إنستغرام بالقطعة التي تريدينها وسنؤكد السعر قبل الطلب."),
            ("هل يمكنني تغيير الألوان؟", "غالبًا نعم. راسلينا بالألوان التي تريدينها وسنؤكد إن كانت متاحة لتلك القطعة."),
            ("من ماذا تُصنع القطع؟", "راسلينا على واتساب أو إنستغرام — سنؤكد لك المواد الخاصة بالقطعة التي تسألين عنها."),
            ("هل يمكنني استرجاع أو استبدال قطعة؟", "لأن كل قطعة تُصنع خصيصًا عند الطلب، لا يمكننا قبول الاسترجاع لمجرد تغيير الرأي. إذا وصلت القطعة تالفة أو خاطئة، راسلينا خلال 48 ساعة وسنصلح الأمر."),
            ("هل هذا مناسب وآمن للأطفال الصغار؟", "لم نكمل بعد اختبارات السلامة لقطع الأطفال، ولذلك لا نقدّم أي تأكيد على السلامة أو الفئة العمرية. راسلينا إذا كان لديك سؤال قبل الطلب لطفل رضيع، وراقبي الأطفال الصغار دائمًا عند استخدام أي قطعة يدوية صغيرة."),
        ],
        "footer_tagline": "كروشيه يدوي من لبنان، يُشحن حول العالم.",
        "footer_shop": "المتجر", "footer_info": "معلومات", "footer_follow": "تابعونا",
        "meta_home_desc": "حيوانات محشوة وعرائس وزهور وهدايا أطفال مصنوعة يدويًا بالكروشيه عند الطلب في لبنان، تُشحن إلى الخليج وحول العالم.",
        "meta_shop_desc": "تصفحي حيوانات وعرائس وزهور وهدايا كروشيه يدوية، تُصنع عند الطلب وتُشحن من لبنان حول العالم.",
    },
}

def nav_html(t, active):
    items = [
        ("nav_home", "/" if t["lang"] == "en" else "/ar/", "home"),
        ("nav_shop", "/shop/" if t["lang"] == "en" else "/ar/shop/", "shop"),
        ("nav_custom", "/custom-orders/" if t["lang"] == "en" else "/ar/custom-orders/", "custom"),
        ("nav_shipping", "/shipping/" if t["lang"] == "en" else "/ar/shipping/", "shipping"),
        ("nav_about", "/about/" if t["lang"] == "en" else "/ar/about/", "about"),
        ("nav_faq", "/faq/" if t["lang"] == "en" else "/ar/faq/", "faq"),
    ]
    out = []
    for key, href, name in items:
        out.append(f'<a href="{href}"{" aria-current=\"page\"" if name == active else ""}>{t[key]}</a>')
    return "\n".join(out)

def lang_switch_html(t, path_en, path_ar):
    target = path_en if t["lang"] == "ar" else path_ar
    return f'<a href="{target}" hreflang="{t["alt_lang"]}">{t["alt_label"]}</a>'

def page_shell(t, *, title, description, canonical_path, body, extra_head="", active="", path_en="/", path_ar="/ar/"):
    og_image = f"{BASE_URL}/assets/img/og.jpg"
    html_lang = t["lang"]
    alt_href_en = f"{BASE_URL}{path_en}"
    alt_href_ar = f"{BASE_URL}{path_ar}"
    return f"""<!doctype html>
<html lang="{html_lang}" dir="{t['dir']}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{description}">
<link rel="canonical" href="{BASE_URL}{canonical_path}">
<link rel="alternate" hreflang="en" href="{alt_href_en}">
<link rel="alternate" hreflang="ar" href="{alt_href_ar}">
<link rel="alternate" hreflang="x-default" href="{alt_href_en}">
<meta name="theme-color" content="#c1613f">
<link rel="icon" type="image/png" sizes="32x32" href="/assets/img/icon-32.png">
<link rel="apple-touch-icon" href="/assets/img/icon-180.png">
<meta property="og:type" content="website">
<meta property="og:url" content="{BASE_URL}{canonical_path}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{description}">
<meta property="og:image" content="{og_image}">
<meta name="twitter:card" content="summary_large_image">
<link rel="stylesheet" href="/assets/css/style.css">
<script async src="https://www.googletagmanager.com/gtag/js?id={GA}"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){{dataLayer.push(arguments);}}
  if (!(navigator.webdriver || /bot|crawl|spider|headless|lighthouse/i.test(navigator.userAgent) || (screen.width === 800 && screen.height === 600))) {{
    gtag('js', new Date());
    gtag('config', '{GA}', {{ anonymize_ip: true }});
  }}
</script>
{extra_head}
</head>
<body>
<header class="site">
  <div class="bar">
    <a class="brand" href="{'/' if t['lang']=='en' else '/ar/'}"><span class="dot"></span>{t['site_name']}</a>
    <nav class="main">{nav_html(t, active)}</nav>
    <div class="lang-switch">{lang_switch_html(t, path_en, path_ar)}</div>
  </div>
</header>
{body}
<footer class="site">
  <div class="wrap cols">
    <div>
      <div class="brand" style="margin-bottom:8px"><span class="dot"></span>{t['site_name']}</div>
      <p>{t['footer_tagline']}</p>
    </div>
    <nav>
      <strong>{t['footer_shop']}</strong>
      <a href="{'/shop/' if t['lang']=='en' else '/ar/shop/'}">{t['nav_shop']}</a>
      <a href="{'/custom-orders/' if t['lang']=='en' else '/ar/custom-orders/'}">{t['nav_custom']}</a>
    </nav>
    <nav>
      <strong>{t['footer_info']}</strong>
      <a href="{'/shipping/' if t['lang']=='en' else '/ar/shipping/'}">{t['nav_shipping']}</a>
      <a href="{'/about/' if t['lang']=='en' else '/ar/about/'}">{t['nav_about']}</a>
      <a href="{'/faq/' if t['lang']=='en' else '/ar/faq/'}">{t['nav_faq']}</a>
    </nav>
    <nav>
      <strong>{t['footer_follow']}</strong>
      <a href="{INSTAGRAM}">{INSTAGRAM_HANDLE}</a>
    </nav>
  </div>
</footer>
</body>
</html>
"""

def product_jsonld(p, t):
    offer = {
        "@type": "Offer",
        "url": f"{BASE_URL}/shop/{p['slug']}/",
        "availability": "https://schema.org/MadeToOrder" if p.get("made_to_order") else "https://schema.org/InStock",
        "itemCondition": "https://schema.org/NewCondition",
    }
    if p.get("stripe_payment_link"):
        offer["url"] = p["stripe_payment_link"]
    data = {
        "@context": "https://schema.org",
        "@type": "Product",
        "name": p["title"][t["lang"]],
        "description": p["description"][t["lang"]],
        "image": f"{BASE_URL}/{p['image']['main']}",
        "category": CATEGORY_LABEL[p["category"]]["en"],
        "offers": offer,
    }
    return f'<script type="application/ld+json">{json.dumps(data, ensure_ascii=False)}</script>'

def product_card(p, t):
    path = f"/shop/{p['slug']}/" if t["lang"] == "en" else f"/ar/shop/{p['slug']}/"
    title = p["title"][t["lang"]]
    return f'''<a class="card" href="{path}">
  <img src="/{p['image']['thumb']}" alt="{title}" loading="lazy" width="400" height="400">
  <div class="body">
    <h3>{title}</h3>
    <div class="price">{t['price_cta']}</div>
  </div>
</a>'''

# --------------------------------------------------------------- pages ----
def build_home(t, outdir):
    path_en, path_ar = "/", "/ar/"
    featured = PRODUCTS[:8]
    showcase = "\n".join(
        f'<a href="{"/shop/"+p["slug"]+"/" if t["lang"]=="en" else "/ar/shop/"+p["slug"]+"/"}"><img src="/{p["image"]["thumb"]}" alt="{p["title"][t["lang"]]}" loading="lazy" width="300" height="300"></a>'
        for p in featured
    )
    shop_path = "/shop/" if t["lang"] == "en" else "/ar/shop/"
    body = f'''<main>
<section class="hero">
  <div class="wrap">
    <h1>{t['site_name']}</h1>
    <p class="lead">{t['hero_lead']}</p>
    <div class="cta-row">
      <a class="btn btn-primary" href="{shop_path}">{t['cta_shop']}</a>
      <a class="btn btn-ig" href="{INSTAGRAM}">{t['cta_instagram']}</a>
    </div>
  </div>
</section>
<div class="wrap">
  <div class="showcase">{showcase}</div>
</div>
<section class="alt">
  <div class="wrap badge-row">
    <div><span class="ic">\U0001f9f6</span><strong>{t['badge_handmade']}</strong><br>{t['badge_handmade_d']}</div>
    <div><span class="ic">\U0001f9f5</span><strong>{t['badge_order']}</strong><br>{t['badge_order_d']}</div>
    <div><span class="ic">\U0001f4e6</span><strong>{t['badge_ship']}</strong><br>{t['badge_ship_d']}</div>
  </div>
</section>
</main>'''
    org_jsonld = json.dumps({
        "@context": "https://schema.org",
        "@type": "Organization",
        "@id": f"{BASE_URL}/#org",
        "name": "Loopaholic",
        "url": BASE_URL,
        "logo": f"{BASE_URL}/assets/img/icon-512.png",
        "sameAs": [INSTAGRAM],
        "areaServed": [{"@type": "Country", "name": "Lebanon"}, {"@type": "Place", "name": "Gulf countries"}, {"@type": "Place", "name": "Worldwide"}],
    }, ensure_ascii=False)
    extra_head = f'<script type="application/ld+json">{org_jsonld}</script>'
    html = page_shell(t, title=f"{t['site_name']} | Handmade Crochet, Made to Order" if t["lang"]=="en" else f"{t['site_name']} | كروشيه يدوي عند الطلب",
                       description=t["meta_home_desc"], canonical_path=path_en if t["lang"]=="en" else path_ar,
                       body=body, extra_head=extra_head, active="home", path_en=path_en, path_ar=path_ar)
    write(outdir, "index.html", html)

def build_shop(t, outdir):
    path_en, path_ar = "/shop/", "/ar/shop/"
    chips = "\n".join(
        f'<a href="#cat-{c}">{CATEGORY_LABEL[c][t["lang"]]}</a>' for c in CATEGORY_ORDER if any(p["category"] == c for p in PRODUCTS)
    )
    sections = []
    for c in CATEGORY_ORDER:
        items = [p for p in PRODUCTS if p["category"] == c]
        if not items:
            continue
        cards = "\n".join(product_card(p, t) for p in items)
        sections.append(f'<section id="cat-{c}"><div class="wrap"><div class="section-head"><h2>{CATEGORY_LABEL[c][t["lang"]]}</h2></div><div class="grid">{cards}</div></div></section>')
    body = f'''<main>
<section>
  <div class="wrap">
    <div class="section-head">
      <h1>{t['shop_title']}</h1>
      <p>{t['shop_lead']}</p>
    </div>
    <div class="chips">{chips}</div>
  </div>
</section>
{''.join(sections)}
</main>'''
    html = page_shell(t, title=f"Shop | {t['site_name']}" if t["lang"]=="en" else f"المتجر | {t['site_name']}",
                       description=t["meta_shop_desc"], canonical_path=path_en if t["lang"]=="en" else path_ar,
                       body=body, active="shop", path_en=path_en, path_ar=path_ar)
    write(outdir, "shop/index.html", html)

def build_product(p, t, outdir):
    path_en, path_ar = f"/shop/{p['slug']}/", f"/ar/shop/{p['slug']}/"
    shop_path = "/shop/" if t["lang"] == "en" else "/ar/shop/"
    title = p["title"][t["lang"]]
    desc = p["description"][t["lang"]]
    colors = ", ".join(p["colors"])
    lead_lo, lead_hi = p["lead_time_days"]

    wa_text = f"Hi! I'd like to order: {p['title']['en']}" if t["lang"] == "en" else f"مرحبا، أريد طلب: {p['title']['ar']}"
    wa_href = whatsapp_link(wa_text)
    intl_block = (
        f'<div class="stripe-slot active"><a class="btn btn-primary" href="{p["stripe_payment_link"]}">{t["buy_now"]}</a></div>'
        if p.get("stripe_payment_link") else
        f'<p>{t["order_intl_body_pending"]}</p><a class="btn btn-outline" href="{INSTAGRAM}">{t["order_instagram"]}</a>'
    )

    others = [x for x in PRODUCTS if x["category"] == p["category"] and x["id"] != p["id"]][:4]
    related_html = ""
    if others:
        cards = "\n".join(product_card(x, t) for x in others)
        related_html = f'<section class="alt"><div class="wrap"><div class="section-head"><h2>{t["related_title"]}</h2></div><div class="grid">{cards}</div></div></section>'

    body = f'''<main>
<section>
  <div class="wrap">
    <p class="breadcrumb"><a href="{'/' if t['lang']=='en' else '/ar/'}">{t['breadcrumb_home']}</a> / <a href="{shop_path}">{t['breadcrumb_shop']}</a> / {title}</p>
    <div class="product-layout">
      <img src="/{p['image']['main']}" alt="{title}" width="800" height="800">
      <div>
        <h1>{title}</h1>
        <div class="price-block"><a href="{wa_href}" onclick="gtag('event','whatsapp_click',{{product:'{p['slug']}'}})">{t['price_cta']}</a></div>
        <div class="meta-row">
          <span class="pill">{t['size_label']}: {p['size_approx']}</span>
          <span class="pill">{t['colors_label']}: {colors}</span>
          <span class="pill">{t['lead_label']}: {lead_lo}–{lead_hi} {t['days']}</span>
        </div>
        <p>{desc}</p>

        <h2 style="font-size:1.1rem;margin-top:1.4em">{t['order_lebanon_title']}</h2>
        <p>{t['order_lebanon_body']}</p>
        <div class="order-actions">
          <a class="btn btn-primary" href="{wa_href}" onclick="gtag('event','whatsapp_click',{{product:'{p['slug']}'}})">{t['order_whatsapp']}</a>
          <a class="btn btn-outline" href="{INSTAGRAM}" onclick="gtag('event','instagram_click',{{product:'{p['slug']}'}})">{t['order_instagram']}</a>
        </div>

        <h2 style="font-size:1.1rem;margin-top:1.4em">{t['order_intl_title']}</h2>
        {intl_block.replace('class="btn btn-primary"', f'class="btn btn-primary" onclick="gtag(\'event\',\'buy_click\',{{product:\'{p["slug"]}\'}})"')}
      </div>
    </div>
  </div>
</section>
{related_html}
</main>'''
    extra_head = product_jsonld(p, t)
    html = page_shell(t, title=f"{title} | {t['site_name']}", description=desc,
                       canonical_path=path_en if t["lang"]=="en" else path_ar,
                       body=body, extra_head=extra_head, active="shop", path_en=path_en, path_ar=path_ar)
    write(outdir, f"shop/{p['slug']}/index.html", html)

def build_custom(t, outdir):
    path_en, path_ar = "/custom-orders/", "/ar/custom-orders/"
    wa_href = whatsapp_link("Hi! I'd like to ask about a custom order." if t["lang"] == "en" else "مرحبا، أريد الاستفسار عن طلب خاص.")
    body = f'''<main>
<section>
  <div class="wrap prose">
    <div class="section-head"><h1>{t['custom_title']}</h1><p>{t['custom_lead']}</p></div>
    <p>{t['custom_body_1']}</p>
    <p>{t['custom_body_2']}</p>
    <div class="showcase" style="grid-template-columns:repeat(2,1fr);max-width:500px;margin:0 auto 20px">
      <img src="/assets/img/custom/letter-d.jpg" alt="Crochet letter D" loading="lazy">
      <img src="/assets/img/custom/daisy-keychain.jpg" alt="Crochet daisy keychain" loading="lazy">
    </div>
    <h2>{t['custom_how_title']}</h2>
    <ol>
      <li>{t['custom_how_1']}</li>
      <li>{t['custom_how_2']}</li>
      <li>{t['custom_how_3']}</li>
    </ol>
    <div class="cta-row" style="justify-content:flex-start">
      <a class="btn btn-primary" href="{wa_href}" onclick="gtag('event','whatsapp_click',{{page:'custom-orders'}})">{t['custom_cta']}</a>
      <a class="btn btn-outline" href="{INSTAGRAM}" onclick="gtag('event','instagram_click',{{page:'custom-orders'}})">{t['order_instagram']}</a>
    </div>
  </div>
</section>
</main>'''
    html = page_shell(t, title=f"{t['custom_title']} | {t['site_name']}", description=t['custom_lead'],
                       canonical_path=path_en if t["lang"]=="en" else path_ar,
                       body=body, active="custom", path_en=path_en, path_ar=path_ar)
    write(outdir, "custom-orders/index.html", html)

def build_shipping(t, outdir):
    path_en, path_ar = "/shipping/", "/ar/shipping/"
    body = f'''<main>
<section>
  <div class="wrap prose">
    <div class="section-head"><h1>{t['shipping_title']}</h1></div>
    <h2>{t['shipping_lebanon_h']}</h2>
    <p>{t['shipping_lebanon_b']}</p>
    <h2>{t['shipping_gulf_h']}</h2>
    <p>{t['shipping_gulf_b']}</p>
    <h2>{t['shipping_intl_h']}</h2>
    <p>{t['shipping_intl_b']}</p>
    <h2>{t['shipping_note_h']}</h2>
    <p>{t['shipping_note_b']}</p>
  </div>
</section>
</main>'''
    html = page_shell(t, title=f"{t['shipping_title']} | {t['site_name']}", description=t['shipping_lebanon_b'],
                       canonical_path=path_en if t["lang"]=="en" else path_ar,
                       body=body, active="shipping", path_en=path_en, path_ar=path_ar)
    write(outdir, "shipping/index.html", html)

def build_about(t, outdir):
    path_en, path_ar = "/about/", "/ar/about/"
    body = f'''<main>
<section>
  <div class="wrap prose">
    <div class="section-head"><h1>{t['about_title']}</h1></div>
    <p>{t['about_body_1']}</p>
    <p>{t['about_body_2']}</p>
    <p>{t['about_body_3']} <a href="{INSTAGRAM}">{INSTAGRAM_HANDLE}</a></p>
  </div>
</section>
</main>'''
    html = page_shell(t, title=f"{t['about_title']} | {t['site_name']}", description=t['about_body_1'][:150],
                       canonical_path=path_en if t["lang"]=="en" else path_ar,
                       body=body, active="about", path_en=path_en, path_ar=path_ar)
    write(outdir, "about/index.html", html)

def build_faq(t, outdir):
    path_en, path_ar = "/faq/", "/ar/faq/"
    items = "\n".join(f'<div class="faq-item"><h3>{q}</h3><p>{a}</p></div>' for q, a in t["faq"])
    body = f'''<main>
<section>
  <div class="wrap prose">
    <div class="section-head"><h1>{t['faq_title']}</h1></div>
    {items}
  </div>
</section>
</main>'''
    faq_jsonld = json.dumps({
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}}
            for q, a in t["faq"]
        ],
    }, ensure_ascii=False)
    extra_head = f'<script type="application/ld+json">{faq_jsonld}</script>'
    html = page_shell(t, title=f"{t['faq_title']} | {t['site_name']}", description=t["faq"][0][1][:150],
                       canonical_path=path_en if t["lang"]=="en" else path_ar,
                       body=body, extra_head=extra_head, active="faq", path_en=path_en, path_ar=path_ar)
    write(outdir, "faq/index.html", html)

def write(outdir, relpath, content):
    full = os.path.join(outdir, relpath)
    os.makedirs(os.path.dirname(full), exist_ok=True)
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

def main():
    outdir = ROOT
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
    build_sitemap(outdir)
    build_robots(outdir)
    build_cname(outdir)
    print(f"Built {len(PRODUCTS)} products × 2 languages.")

if __name__ == "__main__":
    main()
