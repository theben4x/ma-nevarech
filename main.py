from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
import json

app = FastAPI()
# app.mount("/static", StaticFiles(directory="static"), name="static")

# טקסטים מלאים של ברכות (רישא וחתימה) עם ניקוד
RISHONA_TEXTS = {
    "בורא פרי העץ": "בָּרוּךְ אַתָּה ה' אֱלֹהֵינוּ מֶלֶךְ הָעוֹלָם בּוֹרֵא פְּרִי הָעֵץ",
    "בורא פרי האדמה": "בָּרוּךְ אַתָּה ה' אֱלֹהֵינוּ מֶלֶךְ הָעוֹלָם בּוֹרֵא פְּרִי הָאֲדָמָה",
    "בורא מיני מזונות": "בָּרוּךְ אַתָּה ה' אֱלֹהֵינוּ מֶלֶךְ הָעוֹלָם בּוֹרֵא מִינֵי מְזוֹנוֹת",
    "המוציא לחם מן הארץ": "בָּרוּךְ אַתָּה ה' אֱלֹהֵינוּ מֶלֶךְ הָעוֹלָם הַמּוֹצִיא לֶחֶם מִן הָאָרֶץ",
    "בורא פרי הגפן": "בָּרוּךְ אַתָּה ה' אֱלֹהֵינוּ מֶלֶךְ הָעוֹלָם בּוֹרֵא פְּרִי הַגָּפֶן",
    "שהכל נהיה בדברו": "בָּרוּךְ אַתָּה ה' אֱלֹהֵינוּ מֶלֶךְ הָעוֹלָם שֶׁהַכֹּל נִהְיָה בִּדְבָרוֹ",
}
ACHRONA_TEXTS = {
    "בורא נפשות": "בָּרוּךְ אַתָּה ה' אֱלֹהֵינוּ מֶלֶךְ הָעוֹלָם בּוֹרֵא נְפָשׁוֹת רַבּוֹת וְחֶסְרוֹנָן עַל כָּל מַה שֶׁבָּרָאתָ לְהַחֲיוֹת בָּהֶם נֶפֶשׁ כָּל חָי. בָּרוּךְ חַי הָעוֹלָמִים.",
    "על המחיה": "בָּרוּךְ אַתָּה ה' אֱלֹהֵינוּ מֶלֶךְ הָעוֹלָם עַל הַמִּחְיָה וְעַל הַכַּלְכָּלָה וְעַל תְּנוּבַת הַשָּׂדֶה. בָּרוּךְ אַתָּה ה' זָן אֶת הַכֹּל.",
    "על העץ ועל פרי העץ": "בָּרוּךְ אַתָּה ה' אֱלֹהֵינוּ מֶלֶךְ הָעוֹלָם עַל הָעֵץ וְעַל פְּרִי הָעֵץ. בָּרוּךְ אַתָּה ה' עַל הָעֵץ וְעַל פְּרִי הָעֵץ.",
    "על האדמה ועל פרי האדמה": "בָּרוּךְ אַתָּה ה' אֱלֹהֵינוּ מֶלֶךְ הָעוֹלָם עַל הָאֲדָמָה וְעַל פְּרִי הָאֲדָמָה. בָּרוּךְ אַתָּה ה' עַל הָאֲדָמָה וְעַל פְּרִי הָאֲדָמָה.",
    "על הגפן ועל פרי הגפן": "בָּרוּךְ אַתָּה ה' אֱלֹהֵינוּ מֶלֶךְ הָעוֹלָם עַל הַגֶּפֶן וְעַל פְּרִי הַגֶּפֶן. בָּרוּךְ אַתָּה ה' עַל הַגֶּפֶן וְעַל פְּרִי הַגֶּפֶן.",
    "ברכת המזון": "אַחֲרֵי אֲכִילַת לֶחֶם מְבָרְכִים בִּרְכַּת הַמָּזוֹן (שָׁלֹשׁ בְּרָכוֹת). בָּרוּךְ אַתָּה ה' אֱלֹהֵינוּ מֶלֶךְ הָעוֹלָם זָן אֶת הָעוֹלָם כֻּלּוֹ בְּטוּבוֹ.",
}
ACHRONA_BY_RISHONA = {
    "בורא פרי העץ": "על העץ ועל פרי העץ",
    "בורא פרי האדמה": "על האדמה ועל פרי האדמה",
    "בורא מיני מזונות": "על המחיה",
    "המוציא לחם מן הארץ": "ברכת המזון",
    "בורא פרי הגפן": "על הגפן ועל פרי הגפן",
    "שהכל נהיה בדברו": "בורא נפשות",
}

# 150 מאכלים כשרים נפוצים: (שם, אימוג'י, ברכה ראשונה)
FOOD_LIST = [
    # גרעינים/מאפייה — Grains/Bakery
    ("חלה", "🍞", "המוציא לחם מן הארץ"),
    ("פיתה", "🫓", "המוציא לחם מן הארץ"),
    ("בייגל", "🥯", "בורא מיני מזונות"),
    ("פיצה", "🍕", "בורא מיני מזונות"),
    ("עוגיות", "🍪", "בורא מיני מזונות"),
    ("קרקר", "🍘", "בורא מיני מזונות"),
    ("בורקס", "🥐", "בורא מיני מזונות"),
    ("לחם", "🍞", "המוציא לחם מן הארץ"),
    ("לחמניה", "🍞", "המוציא לחם מן הארץ"),
    ("טוסט", "🍞", "המוציא לחם מן הארץ"),
    ("לחם שום", "🍞", "המוציא לחם מן הארץ"),
    ("קרואסון", "🥐", "בורא מיני מזונות"),
    ("מאפין", "🧁", "בורא מיני מזונות"),
    ("פנקייק", "🥞", "בורא מיני מזונות"),
    ("סופגנייה", "🍩", "בורא מיני מזונות"),
    ("עוגה", "🍰", "בורא מיני מזונות"),
    ("עוגת גבינה", "🍰", "בורא מיני מזונות"),
    ("מלאווח", "🥐", "בורא מיני מזונות"),
    ("ג'חנון", "🥐", "בורא מיני מזונות"),
    ("בייגלה", "🥨", "בורא מיני מזונות"),
    ("פופקורן", "🍿", "בורא מיני מזונות"),
    ("וופל", "🧇", "בורא מיני מזונות"),
    ("אורז", "🍚", "בורא מיני מזונות"),
    ("פסטה", "🍝", "בורא מיני מזונות"),
    ("קוסקוס", "🍚", "בורא מיני מזונות"),
    ("קינואה", "🍚", "בורא מיני מזונות"),
    ("דגנים", "🥣", "בורא מיני מזונות"),
    ("גרנולה", "🥣", "בורא מיני מזונות"),
    # פירות — Fruits
    ("תפוח", "🍎", "בורא פרי העץ"),
    ("בננה", "🍌", "בורא פרי האדמה"),
    ("ענבים", "🍇", "בורא פרי העץ"),
    ("מנגו", "🥭", "בורא פרי העץ"),
    ("תמר", "🌴", "בורא פרי העץ"),
    ("תמרים", "🌴", "בורא פרי העץ"),
    ("אננס", "🍍", "בורא פרי העץ"),
    ("אבוקדו", "🥑", "בורא פרי העץ"),
    ("תפוז", "🍊", "בורא פרי העץ"),
    ("אגס", "🍐", "בורא פרי העץ"),
    ("דובדבן", "🍒", "בורא פרי העץ"),
    ("שזיף", "🍑", "בורא פרי העץ"),
    ("נקטרינה", "🍑", "בורא פרי העץ"),
    ("קיווי", "🥝", "בורא פרי העץ"),
    ("תאנה", "🍇", "בורא פרי העץ"),
    ("צימוקים", "🍇", "בורא פרי העץ"),
    ("זיתים", "🫒", "בורא פרי העץ"),
    ("משמש", "🍑", "בורא פרי העץ"),
    ("אפרסק", "🍑", "בורא פרי העץ"),
    ("פומלה", "🍊", "בורא פרי העץ"),
    ("קלמנטינה", "🍊", "בורא פרי העץ"),
    ("לימון", "🍋", "בורא פרי העץ"),
    ("אשכולית", "🍊", "בורא פרי העץ"),
    ("רימון", "🍎", "בורא פרי העץ"),
    ("אבטיח", "🍉", "בורא פרי האדמה"),
    ("מלון", "🍈", "בורא פרי האדמה"),
    ("תות", "🍓", "בורא פרי האדמה"),
    ("אוכמניות", "🫐", "בורא פרי האדמה"),
    ("פטל", "🫐", "בורא פרי האדמה"),
    ("שקדים", "🥜", "בורא פרי העץ"),
    ("אגוז", "🥥", "בורא פרי העץ"),
    ("פיסטוק", "🥜", "בורא פרי העץ"),
    ("ערמונים", "🌰", "בורא פרי העץ"),
    # ירקות — Vegetables
    ("מלפפון", "🥒", "בורא פרי האדמה"),
    ("עגבנייה", "🍅", "בורא פרי האדמה"),
    ("גזר", "🥕", "בורא פרי האדמה"),
    ("תפוח אדמה", "🥔", "בורא פרי האדמה"),
    ("סלט", "🥗", "שהכל נהיה בדברו"),
    ("חסה", "🥬", "בורא פרי האדמה"),
    ("ברוקולי", "🥦", "בורא פרי האדמה"),
    ("כרוב", "🥬", "בורא פרי האדמה"),
    ("בצל", "🧅", "בורא פרי האדמה"),
    ("בטטה", "🍠", "בורא פרי האדמה"),
    ("כרובית", "🥦", "בורא פרי האדמה"),
    ("אפונה", "🟢", "בורא פרי האדמה"),
    ("תירס", "🌽", "בורא פרי האדמה"),
    ("פלפל", "🫑", "בורא פרי האדמה"),
    ("חציל", "🍆", "בורא פרי האדמה"),
    ("דלעת", "🎃", "בורא פרי האדמה"),
    ("קישוא", "🥒", "בורא פרי האדמה"),
    ("סלרי", "🥬", "בורא פרי האדמה"),
    ("תרד", "🥬", "בורא פרי האדמה"),
    ("כוסברה", "🌿", "בורא פרי האדמה"),
    ("פטרוזיליה", "🌿", "בורא פרי האדמה"),
    ("נענע", "🌿", "בורא פרי האדמה"),
    # חלב/בשר/דגים — Dairy/Meat/Fish
    ("גבינה", "🧀", "שהכל נהיה בדברו"),
    ("יוגורט", "🥛", "שהכל נהיה בדברו"),
    ("חלב", "🥛", "שהכל נהיה בדברו"),
    ("חזה עוף", "🍗", "שהכל נהיה בדברו"),
    ("עוף", "🍗", "שהכל נהיה בדברו"),
    ("סטייק", "🥩", "שהכל נהיה בדברו"),
    ("דג", "🐟", "שהכל נהיה בדברו"),
    ("סלמון", "🍣", "שהכל נהיה בדברו"),
    ("טונה", "🐟", "שהכל נהיה בדברו"),
    ("ביצה", "🥚", "שהכל נהיה בדברו"),
    ("חמאה", "🧈", "שהכל נהיה בדברו"),
    ("גפילטע פיש", "🐟", "שהכל נהיה בדברו"),
    # חטיפים וממתקים — Snacks
    ("במבה", "🥜", "שהכל נהיה בדברו"),
    ("ביסלי", "🥨", "שהכל נהיה בדברו"),
    ("שוקולד", "🍫", "שהכל נהיה בדברו"),
    ("גלידה", "🍦", "שהכל נהיה בדברו"),
    ("פרטزل", "🥨", "בורא מיני מזונות"),
    ("קרמבו", "🧁", "שהכל נהיה בדברו"),
    ("מילקה", "🍫", "שהכל נהיה בדברו"),
    ("אפרופו", "🍬", "שהכל נהיה בדברו"),
    ("טוגו", "🍫", "שהכל נהיה בדברו"),
    ("חלווה", "🍬", "שהכל נהיה בדברו"),
    ("חמאת בוטנים", "🥜", "שהכל נהיה בדברו"),
    ("סוכריה", "🍬", "שהכל נהיה בדברו"),
    ("מרשמלו", "🍡", "שהכל נהיה בדברו"),
    ("דבש", "🍯", "שהכל נהיה בדברו"),
    ("ריבה", "🍓", "שהכל נהיה בדברו"),
    # משקאות ומאכלים נוספים
    ("מים", "💧", "שהכל נהיה בדברו"),
    ("קפה", "☕", "שהכל נהיה בדברו"),
    ("תה", "🍵", "שהכל נהיה בדברו"),
    ("מיץ", "🧃", "שהכל נהיה בדברו"),
    ("מיץ ענבים", "🍇", "בורא פרי הגפן"),
    ("מיץ תפוזים", "🧃", "שהכל נהיה בדברו"),
    ("מיץ תפוחים", "🧃", "שהכל נהיה בדברו"),
    ("יין", "🍷", "בורא פרי הגפן"),
    ("קולה", "🥤", "שהכל נהיה בדברו"),
    ("לימונדה", "🍋", "שהכל נהיה בדברו"),
    ("שייק", "🥤", "שהכל נהיה בדברו"),
    ("בירה", "🍺", "שהכל נהיה בדברו"),
    ("מרק", "🍲", "שהכל נהיה בדברו"),
    ("המבורגר", "🍔", "שהכל נהיה בדברו"),
    ("נקניק", "🌭", "שהכל נהיה בדברו"),
    ("צ'יפס", "🍟", "שהכל נהיה בדברו"),
    ("פלאפל", "🧆", "שהכל נהיה בדברו"),
    ("חומוס", "🫓", "שהכל נהיה בדברו"),
    ("טחינה", "🫙", "שהכל נהיה בדברו"),
    ("סושי", "🍣", "שהכל נהיה בדברו"),
    ("שווארמה", "🥙", "שהכל נהיה בדברו"),
    ("כבב", "🍢", "שהכל נהיה בדברו"),
    ("חמין", "🍲", "שהכל נהיה בדברו"),
    ("קציצות", "🍖", "שהכל נהיה בדברו"),
    ("כבד", "🍖", "שהכל נהיה בדברו"),
    ("קובה", "🍲", "שהכל נהיה בדברו"),
    ("קיגל", "🍲", "שהכל נהיה בדברו"),
    ("לאטקס", "🥞", "בורא פרי האדמה"),
    ("טחינה גולמית", "🫙", "שהכל נהיה בדברו"),
    ("סביח", "🥙", "שהכל נהיה בדברו"),
    ("ממולאים", "🫑", "בורא פרי האדמה"),
    ("אריסה", "🌶️", "שהכל נהיה בדברו"),
    ("חרוסת", "🍎", "שהכל נהיה בדברו"),
    ("מצה", "🍞", "המוציא לחם מן הארץ"),
    ("מצה שמורה", "🍞", "המוציא לחם מן הארץ"),
    ("לחם שחור", "🍞", "המוציא לחם מן הארץ"),
    ("לחם מחמצת", "🍞", "המוציא לחם מן הארץ"),
    ("בגט", "🥖", "המוציא לחם מן הארץ"),
    ("לחם פרוס", "🍞", "המוציא לחם מן הארץ"),
    ("עוגיות טחינה", "🍪", "בורא מיני מזונות"),
]

# בניית מאגר עם כל השדות
FOOD_DATA = {}
for name, emoji, rishona in FOOD_LIST:
    achrona = ACHRONA_BY_RISHONA[rishona]
    FOOD_DATA[name] = {
        "emoji": emoji,
        "bracha_rishona": rishona,
        "rishona_text": RISHONA_TEXTS[rishona],
        "bracha_achrona": achrona,
        "achrona_text": ACHRONA_TEXTS[achrona],
    }

@app.get("/", response_class=HTMLResponse)
async def get_index():
    food_json = json.dumps(FOOD_DATA, ensure_ascii=False)
    
    html_content = f"""
    <!DOCTYPE html>
    <html dir="rtl" lang="he" data-theme="light">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>ברכות - האתר הרשמי</title>
        <link rel="icon" href="/favicon.png" type="image/png">
        <link href="https://fonts.googleapis.com/css2?family=Heebo:wght@300;400;700;900&display=swap" rel="stylesheet">
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css" crossorigin="anonymous">
        <style>
            :root {{
                --accent: #007AFF;
                --accent-tint: rgba(0, 122, 255, 0.09);
                --bg-gradient: linear-gradient(-45deg, #e8f0fe, #f0f5fc, #e8f0fe);
                --card-bg: rgba(255, 255, 255, 0.82);
                --nav-bg: rgba(255, 255, 255, 0.85);
                --text-color: #1a1a1a;
                --text-muted: rgba(0, 0, 0, 0.55);
            }}

            [data-theme="light"] .modal-body {{
                color: var(--text-color);
            }}
            [data-theme="light"] .modal-body p {{
                color: var(--text-color);
            }}
            [data-theme="light"] .result-card-back-btn {{
                color: var(--text-color);
            }}
            [data-theme="light"] .result-breadcrumbs {{
                color: var(--text-color);
            }}
            [data-theme="light"] .result-breadcrumb-link {{
                color: var(--text-color);
            }}
            [data-theme="light"] .result-breadcrumb-sep {{
                color: var(--text-color);
                opacity: 0.75;
            }}

            [data-theme="dark"] {{
                --accent: #5eb8ff;
                --accent-tint: rgba(94, 184, 255, 0.12);
                --bg-gradient: linear-gradient(-45deg, #0f1820, #151f28, #0f1820);
                --card-bg: rgba(255, 255, 255, 0.06);
                --nav-bg: rgba(0, 0, 0, 0.5);
                --text-color: #f5f5f5;
                --text-muted: rgba(255, 255, 255, 0.65);
            }}
            [data-theme="dark"] .modal-body {{
                color: var(--text-color);
            }}
            [data-theme="dark"] .modal-body p {{
                color: var(--text-color);
            }}
            [data-theme="dark"] #tefilat-body {{
                color: var(--text-color);
            }}
            [data-theme="dark"] #random-tehillim-text {{
                color: var(--text-color);
            }}
            [data-theme="dark"] #tehillim-chapter-text {{
                color: var(--text-color);
            }}
            [data-theme="dark"] .tehillim-grid-num {{
                color: #1a1a1a;
            }}

            html {{
                scroll-behavior: smooth;
                overflow-x: hidden;
                max-width: 100%;
            }}
            body {{
                margin: 0; padding: 0; font-family: 'Heebo', sans-serif;
                background: var(--bg-gradient); background-size: 400% 400%;
                animation: gradient 15s ease infinite; min-height: 100vh;
                display: flex; flex-direction: column; align-items: center;
                color: var(--text-color); transition: 0.5s; overflow-x: hidden;
                position: relative;
                max-width: 100vw;
                box-sizing: border-box;
            }}

            .bg-circles {{
                position: fixed;
                inset: 0;
                z-index: 0;
                pointer-events: none;
                overflow: hidden;
            }}
            .bg-circle {{
                position: absolute;
                border-radius: 50%;
            }}
            .bg-circle--top-right {{
                width: 420px;
                height: 420px;
                top: 80px;
                right: 15%;
                background: rgba(210, 230, 255, 0.55);
                border: 2px solid rgba(180, 210, 255, 0.4);
                box-shadow: inset 0 0 60px rgba(180, 210, 255, 0.3);
            }}
            .bg-circle--bottom-left {{
                width: 260px;
                height: 260px;
                bottom: 120px;
                left: 10%;
                background: rgba(210, 230, 255, 0.55);
                border: 2px solid rgba(180, 210, 255, 0.4);
                box-shadow: inset 0 0 40px rgba(180, 210, 255, 0.25);
            }}
            .bg-circle--top-left {{
                width: 180px;
                height: 180px;
                top: 60px;
                left: 8%;
                background: rgba(210, 230, 255, 0.55);
                border: 2px solid rgba(180, 210, 255, 0.4);
                box-shadow: inset 0 0 40px rgba(180, 210, 255, 0.25);
            }}
            .blob {{
                position: fixed;
                border-radius: 50%;
                filter: blur(80px);
                z-index: -1;
                pointer-events: none;
            }}
            .blob:first-child {{
                width: 320px;
                height: 320px;
                background: rgba(147, 197, 253, 0.4);
                top: -100px;
                left: -100px;
            }}
            .blob:last-child {{
                width: 300px;
                height: 300px;
                background: rgba(216, 180, 254, 0.35);
                bottom: -80px;
                right: -80px;
            }}
            .floating-orbs {{
                position: fixed; inset: 0; z-index: -1; overflow: hidden;
                pointer-events: none;
            }}
            .ambient-bg {{
                position: fixed;
                inset: 0;
                pointer-events: none;
                z-index: 0;
                overflow: hidden;
            }}
            .ambient-bg::before,
            .ambient-bg::after {{
                content: "";
                position: absolute;
                border-radius: 50%;
                filter: blur(90px);
                opacity: 0.08;
            }}
            .ambient-bg::before {{
                width: 420px;
                height: 420px;
                background: radial-gradient(circle, #3b82f6, transparent 70%);
                top: -120px;
                right: -120px;
            }}
            .ambient-bg::after {{
                width: 360px;
                height: 360px;
                background: radial-gradient(circle, #a78bfa, transparent 70%);
                bottom: -120px;
                left: -120px;
            }}
            .orb {{
                position: absolute; border-radius: 50%; filter: blur(90px);
                will-change: transform; pointer-events: none;
                background: radial-gradient(circle at 40% 40%, var(--accent-tint), transparent 70%);
            }}
            .orb-1 {{
                width: min(50vmin, 280px); height: min(50vmin, 280px);
                right: -8%; top: 15%; opacity: 0.5;
                animation: floatOrb1 28s ease-in-out infinite;
            }}
            .orb-2 {{
                width: min(45vmin, 260px); height: min(45vmin, 260px);
                right: -6%; bottom: 20%; opacity: 0.4;
                animation: floatOrb2 32s ease-in-out infinite;
            }}
            .orb-3 {{
                width: min(50vmin, 280px); height: min(50vmin, 280px);
                left: -8%; top: 35%; opacity: 0.45;
                animation: floatOrb3 26s ease-in-out infinite;
            }}
            .orb-4 {{
                width: min(44vmin, 240px); height: min(44vmin, 240px);
                left: -6%; bottom: 15%; opacity: 0.4;
                animation: floatOrb4 30s ease-in-out infinite;
            }}
            .orb-edge {{
                position: absolute; border-radius: 50%; pointer-events: none;
                filter: blur(75px); will-change: transform;
                background: radial-gradient(circle at 35% 35%, var(--accent-tint), transparent 65%);
            }}
            .orb-edge-1 {{
                width: min(42vmin, 220px); height: min(42vmin, 220px);
                left: -12%; top: 20%; opacity: 0.35;
                animation: floatEdgeV 22s ease-in-out infinite;
            }}
            .orb-edge-2 {{
                width: min(38vmin, 200px); height: min(38vmin, 200px);
                left: -10%; bottom: 25%; opacity: 0.3;
                animation: floatEdgeV 26s ease-in-out infinite 1s;
            }}
            .orb-edge-3 {{
                width: min(44vmin, 240px); height: min(44vmin, 240px);
                right: -12%; top: 30%; opacity: 0.35;
                animation: floatEdgeV 24s ease-in-out infinite 0.5s;
            }}
            .orb-edge-4 {{
                width: min(40vmin, 200px); height: min(40vmin, 200px);
                right: -10%; bottom: 20%; opacity: 0.3;
                animation: floatEdgeV 20s ease-in-out infinite 2s;
            }}
            [data-theme="dark"] .orb {{
                opacity: 0.35;
            }}
            [data-theme="dark"] .orb-edge {{
                opacity: 0.25;
            }}
            .ambient-circle {{
                position: absolute;
                border-radius: 50%;
                pointer-events: none;
                filter: blur(100px);
                will-change: transform;
                background: radial-gradient(circle at 50% 50%, var(--accent-tint), transparent 70%);
                opacity: 0.2;
            }}
            .ambient-circle-1 {{
                width: min(70vmin, 380px);
                height: min(70vmin, 380px);
                right: -18%;
                top: -8%;
                animation: ambientFloat 32s ease-in-out infinite;
            }}
            .ambient-circle-2 {{
                width: min(65vmin, 340px);
                height: min(65vmin, 340px);
                left: -18%;
                bottom: -8%;
                animation: ambientFloat 36s ease-in-out infinite 4s;
            }}
            .ambient-circle-3 {{
                width: min(45vmin, 240px);
                height: min(45vmin, 240px);
                right: -12%;
                bottom: 25%;
                opacity: 0.12;
                animation: ambientFloat 28s ease-in-out infinite 2s;
            }}
            [data-theme="dark"] .ambient-circle {{
                opacity: 0.14;
            }}
            [data-theme="dark"] .ambient-circle-3 {{
                opacity: 0.08;
            }}
            @keyframes ambientFloat {{
                0%, 100% {{ transform: translate(0, 0) scale(1); }}
                50% {{ transform: translate(1.5vw, -1.5vh) scale(1.03); }}
            }}
            @media (max-width: 480px) {{
                .orb {{ opacity: 0.25; filter: blur(60px); }}
                .orb-edge {{ opacity: 0.2; filter: blur(50px); }}
                .orb-edge-1, .orb-edge-3 {{ width: 32vmin; height: 32vmin; }}
                .orb-edge-2, .orb-edge-4 {{ width: 28vmin; height: 28vmin; }}
                .ambient-circle {{ filter: blur(70px); opacity: 0.12; }}
                .ambient-circle-1, .ambient-circle-2 {{ width: 45vmin; height: 45vmin; }}
                .ambient-circle-3 {{ width: 32vmin; height: 32vmin; opacity: 0.08; }}
            }}
            @keyframes floatEdgeV {{
                0%, 100% {{ transform: translateY(0); }}
                50% {{ transform: translateY(-2.5vh); }}
            }}
            @keyframes floatOrb1 {{
                0%, 100% {{ transform: translate(0, 0) scale(1); }}
                33% {{ transform: translate(-2vw, 3vh) scale(1.02); }}
                66% {{ transform: translate(2vw, -2vh) scale(0.98); }}
            }}
            @keyframes floatOrb2 {{
                0%, 100% {{ transform: translate(0, 0) scale(1); }}
                50% {{ transform: translate(3vw, -3vh) scale(1.03); }}
            }}
            @keyframes floatOrb3 {{
                0%, 100% {{ transform: translate(0, 0) scale(1); }}
                25% {{ transform: translate(2vw, 2vh) scale(0.97); }}
                75% {{ transform: translate(-2vw, -2vh) scale(1.02); }}
            }}
            @keyframes floatOrb4 {{
                0%, 100% {{ transform: translate(0, 0) scale(1); }}
                50% {{ transform: translate(-1.5vw, 2.5vh) scale(1.01); }}
            }}

            @keyframes gradient {{
                0% {{ background-position: 0% 50%; }}
                50% {{ background-position: 100% 50%; }}
                100% {{ background-position: 0% 50%; }}
            }}

            .navbar {{
                position: relative;
                position: sticky;
                top: 0;
                margin-top: 24px;
                background: transparent;
                backdrop-filter: none;
                border: none;
                box-shadow: none;
                padding: 10px 40px;
                display: flex;
                justify-content: space-between;
                align-items: center;
                width: 90%;
                max-width: 960px;
                z-index: 1000;
                transition: background 0.3s ease, backdrop-filter 0.3s ease, border 0.3s ease, box-shadow 0.3s ease;
                box-sizing: border-box;
            }}
            .navbar.scrolled {{
                background: rgba(255, 255, 255, 0.6);
                backdrop-filter: blur(24px) saturate(180%);
                -webkit-backdrop-filter: blur(24px) saturate(180%);
                border: 1px solid rgba(255,255,255,0.5);
                box-shadow: 0 8px 32px rgba(0,0,0,0.08);
                border-radius: 50px;
                margin-top: 12px;
            }}
            [data-theme="dark"] .navbar.scrolled {{
                background: rgba(15, 24, 32, 0.65);
                border-color: rgba(255,255,255,0.1);
            }}

            .navbar-divider {{
                width: 90%;
                max-width: 960px;
                border: none;
                border-top: 1px dashed rgba(0, 0, 0, 0.15);
                margin: 8px auto 0;
            }}
            [data-theme="dark"] .navbar-divider {{
                border-top-color: rgba(255, 255, 255, 0.1);
            }}

            .logo {{
                font-weight: 900; color: var(--accent); margin-left: 10px; 
                cursor: pointer; font-size: 1.2rem; display: flex; align-items: center; gap: 12px;
            }}
            .logo img {{
                height: 60px; width: auto; display: block; object-fit: contain;
            }}

            .nav-item {{
                cursor: pointer;
                padding: 8px 18px;
                border-radius: 20px;
                font-weight: 400;
                font-size: 1.2rem;
                transition: 0.2s;
                color: var(--text-color);
                border: none;
                background: none;
                font-family: 'Heebo';
            }}
            .nav-item:hover {{
                background: rgba(0, 0, 0, 0.06);
            }}
            .nav-item.active {{
                background: none;
                color: var(--text-color);
            }}
            [data-theme="dark"] .nav-item:hover {{
                background: rgba(255, 255, 255, 0.08);
            }}

            .flex-container {{
                position: relative;
                z-index: 2;
                display: flex;
                flex-direction: column;
                align-items: center;
                width: 100%;
                max-width: 100%;
                flex: 1;
                box-sizing: border-box;
                overflow-x: hidden;
            }}

            .main-content {{
                margin-top: 48px; padding: 0 24px 60px; text-align: center; width: 90%; max-width: 720px;
                display: flex; flex-direction: column; align-items: center;
                overflow: visible; gap: 0;
                box-sizing: border-box;
            }}
            #about-content {{ display: none; margin-top: 60px; text-align: center; width: 90%; max-width: 720px; }}

            .hero-tagline {{ font-size: 1.05rem; margin-bottom: 8px; }}
            .hero-title {{
                font-size: 3.5rem; font-weight: 900; margin: 0 0 12px 0;
            }}
            .hero-subtitle {{
                color: var(--text-muted); font-size: 1.15rem; margin: 0 0 28px 0; text-align: center;
                line-height: 1.55; max-width: 100%;
            }}
            [data-theme="dark"] .hero-subtitle {{ color: var(--text-muted); }}

            .search-container {{ position: relative; width: 100%; max-width: 100%; margin-top: 0; overflow: visible; z-index: 10; box-sizing: border-box; }}
            .search-bar-pill {{
                display: flex; align-items: stretch; width: 100%; max-width: 100%; border-radius: 50px;
                background: var(--card-bg); overflow: hidden; border: 1px solid rgba(0,0,0,0.06);
                box-shadow: 0 4px 18px rgba(0,0,0,0.08); box-sizing: border-box;
            }}
            .search-bar-pill input {{
                flex: 1; min-width: 0; padding: 24px 31px; font-size: 1.5rem;
                border: none; background: transparent; color: var(--text-color); outline: none;
                font-family: 'Heebo', sans-serif;
            }}
            .search-bar-pill input::placeholder {{ color: #9ca3af; }}
            .search-bar-btn {{
                flex: none; display: inline-flex; align-items: center; justify-content: center;
                gap: 12px; padding: 22px 34px; background: var(--accent); color: #fff;
                border: none; font-weight: 600; font-size: 1.38rem; cursor: pointer;
                font-family: 'Heebo', sans-serif; transition: background 0.2s;
            }}
            .search-bar-btn:hover {{ filter: brightness(1.05); }}
            [data-theme="dark"] .search-bar-pill {{ border-color: rgba(255,255,255,0.08); }}
            [data-theme="dark"] .search-bar-pill input {{ color: var(--text-color); }}
            [data-theme="dark"] .search-bar-btn {{ background: var(--accent); color: #fff; }}

            .suggestions {{
                position: absolute;
                top: 78px; width: 100%; background: var(--nav-bg);
                backdrop-filter: blur(20px); border-radius: 24px; max-height: 280px;
                overflow-y: auto; display: none;
                z-index: 9999;
                box-shadow: 0 12px 32px rgba(0,0,0,0.18), 0 4px 12px rgba(0,0,0,0.08);
            }}

            .suggestion-item {{
                padding: 14px 22px; cursor: pointer; border-bottom: 1px solid rgba(0,0,0,0.05);
                display: flex; align-items: center; gap: 12px; font-size: 1.2rem;
            }}

            .suggestion-item:hover {{ background: var(--accent); color: #fff; }}

            .daily-cards-wrap {{
                clear: both;
                display: flex;
                flex-direction: row;
                align-items: stretch;
                gap: 20px;
                width: 100%;
                justify-content: center;
                max-width: 960px;
                margin: 32px auto 0;
                box-sizing: border-box;
                position: relative !important;
                flex-wrap: wrap;
                padding: 0 16px;
            }}
            @media (max-width: 900px) {{
                .daily-cards-wrap {{ flex-direction: column; align-items: center; padding: 0 16px; }}
            }}
            .daily-card {{
                background: var(--card-bg);
                backdrop-filter: blur(10px); -webkit-backdrop-filter: blur(10px);
                border: 1px solid rgba(0, 122, 255, 0.08);
                border-radius: 34px; box-shadow: 0 8px 24px rgba(0, 0, 0, 0.08);
                padding: 41px; box-sizing: border-box;
                display: flex;
                flex-direction: column;
                align-items: center;
                flex: 1 1 280px;
                min-width: 220px;
                max-width: 320px;
                overflow: hidden;
                position: relative !important;
            }}
            .daily-card .daily-card-title,
            .daily-card .daily-card-quote,
            .daily-card .daily-card-source,
            .daily-card .daily-card-refresh {{
                position: relative;
            }}
            .inspiration-card::before {{
                content: '';
                position: absolute;
                top: -20px;
                right: -20px;
                width: 100px;
                height: 100px;
                border-radius: 50%;
                background: radial-gradient(circle, var(--accent-tint) 0%, transparent 70%);
            }}
            .halacha-card::before {{
                content: '';
                position: absolute;
                top: -20px;
                right: -20px;
                width: 100px;
                height: 100px;
                border-radius: 50%;
                background: radial-gradient(circle, var(--accent-tint) 0%, transparent 70%);
            }}
            .tehillim-card {{
                background: var(--card-bg);
                border-color: rgba(0, 122, 255, 0.12);
            }}
            .tehillim-card .daily-card-source {{
                flex: 1;
            }}
            .tehillim-card::before {{
                content: '';
                position: absolute;
                top: -20px;
                right: -20px;
                width: 100px;
                height: 100px;
                border-radius: 50%;
                background: radial-gradient(circle, var(--accent-tint) 0%, transparent 70%);
            }}
            [data-theme="dark"] .tehillim-card {{
                border-color: rgba(94, 184, 255, 0.15);
            }}
            .daily-card-title {{
                margin: 0 0 16px 0; font-size: 1.82rem; font-weight: 700;
                color: var(--text-color); flex-shrink: 0;
            }}
            .daily-card-quote {{
                margin: 0 0 10px 0; font-size: 1.58rem; line-height: 1.65;
                color: var(--text-color);
                flex: 1;
            }}
            .daily-card-source {{
                margin: 0 0 16px 0; font-size: 1.3rem;
                color: var(--text-muted);
            }}
            .inspiration-card .daily-card-source,
            .halacha-card .daily-card-source {{
                flex-shrink: 0;
            }}
            .daily-card-refresh {{
                flex-shrink: 0;
                display: inline-flex; align-items: center; justify-content: center; gap: 10px;
                padding: 17px 29px; border-radius: 18px; border: 1px solid var(--accent);
                background: var(--accent-tint); color: var(--accent);
                font-weight: 600; font-size: 1.38rem; cursor: pointer;
                font-family: 'Heebo', sans-serif; transition: background 0.2s, color 0.2s;
            }}
            .daily-card-refresh:hover {{
                background: var(--accent); color: #fff;
            }}
            [data-theme="dark"] .daily-card {{
                background: var(--card-bg);
                border-color: rgba(255, 255, 255, 0.12);
            }}
            [data-theme="dark"] .daily-card-title {{
                color: var(--text-color);
            }}
            [data-theme="dark"] .daily-card-quote {{
                color: var(--text-color);
            }}
            [data-theme="dark"] .daily-card-source {{
                color: var(--text-muted);
            }}

            .section-goal {{
                direction: rtl;
                text-align: right;
                width: 100%; max-width: 720px; margin: 100px auto 36px;
                padding: 48px 32px; box-sizing: border-box;
                background: var(--card-bg);
                backdrop-filter: blur(14px); -webkit-backdrop-filter: blur(14px);
                border: 1px solid rgba(0, 122, 255, 0.08);
                border-radius: 28px; box-shadow: 0 8px 28px rgba(0, 0, 0, 0.06);
            }}
            [data-theme="dark"] .section-goal {{
                border-color: rgba(94, 184, 255, 0.08);
            }}
            .section-goal-title {{
                margin: 0 0 32px 0; font-size: 2.2rem; font-weight: 800;
                color: var(--accent); text-align: center; letter-spacing: 0.02em;
            }}
            .section-goal-list {{
                list-style: none; margin: 0; padding: 0;
                text-align: right; direction: rtl;
            }}
            .section-goal-list li {{
                display: flex; flex-direction: row; align-items: center;
                justify-content: flex-start; gap: 14px;
                padding: 16px 0; font-size: 1.2rem; line-height: 1.4;
                color: var(--text-color); border-bottom: 1px solid rgba(0,0,0,0.06);
                direction: rtl;
            }}
            .section-goal-list li:last-child {{ border-bottom: none; }}
            .section-goal-list li i {{
                font-size: 1.4rem; color: var(--accent); flex-shrink: 0;
            }}
            .section-goal-list li span {{
                flex: 1; min-width: 0; text-align: right;
            }}
            [data-theme="dark"] .section-goal-list li {{ color: var(--text-color); border-bottom-color: rgba(255,255,255,0.1); }}

            .process-steps {{
                direction: rtl;
                width: 100%;
                max-width: 960px;
                margin: 40px auto 120px;
                padding: 72px 40px;
                box-sizing: border-box;
                position: relative;
            }}
            .process-steps::before {{
                content: '';
                position: absolute;
                top: 50%;
                left: 50%;
                transform: translate(-50%, -50%);
                width: 140%;
                height: 160%;
                background: radial-gradient(ellipse at center, var(--accent-tint) 0%, transparent 60%);
                pointer-events: none;
                z-index: -1;
            }}
            .process-steps-inner {{
                position: relative;
            }}
            .process-steps-connector {{
                position: absolute;
                top: 56px;
                left: 0;
                right: 0;
                height: 64px;
                pointer-events: none;
                z-index: 0;
            }}
            .process-steps-connector svg {{
                width: 100%;
                height: 100%;
                display: block;
            }}
            .process-steps-connector path {{
                fill: none;
                stroke: var(--accent);
                opacity: 0.35;
                stroke-width: 1.5;
                stroke-dasharray: 10 8;
                stroke-dashoffset: 100;
                stroke-linecap: round;
                transition: stroke-dashoffset 1s cubic-bezier(0.4, 0, 0.2, 1);
            }}
            .process-steps.journey-drawn .process-steps-connector path {{
                stroke-dashoffset: 0;
            }}
            [data-theme="dark"] .process-steps-connector path {{
                opacity: 0.45;
            }}
            .process-steps-list {{
                display: grid;
                grid-template-columns: repeat(3, 1fr);
                gap: 36px;
                position: relative;
                z-index: 1;
                direction: rtl;
            }}
            .process-step {{
                min-width: 0;
                text-align: right;
                padding: 36px 28px 40px;
                box-sizing: border-box;
                position: relative;
            }}
            .process-step-num {{
                width: 104px;
                height: 104px;
                border-radius: 50%;
                background: linear-gradient(145deg, rgba(255,255,255,0.95) 0%, var(--accent-tint) 50%, transparent 100%);
                border: 1px solid rgba(0, 122, 255, 0.18);
                box-shadow: 0 4px 24px rgba(0, 122, 255, 0.12),
                            inset 0 1px 0 rgba(255,255,255,0.8);
                display: flex;
                align-items: center;
                justify-content: center;
                font-size: 1.8rem;
                font-weight: 800;
                color: var(--accent);
                margin: 0 0 28px 0;
                margin-inline-end: 0;
                flex-shrink: 0;
                letter-spacing: 0.02em;
            }}
            [data-theme="dark"] .process-step-num {{
                background: linear-gradient(145deg, rgba(255,255,255,0.08) 0%, var(--accent-tint) 50%, transparent 100%);
                border-color: rgba(94, 184, 255, 0.25);
                box-shadow: 0 4px 24px rgba(0, 0, 0, 0.2),
                            inset 0 1px 0 rgba(255,255,255,0.06);
            }}
            .process-step-title {{
                font-size: 1.6rem;
                font-weight: 700;
                color: var(--text-color);
                margin: 0 0 12px 0;
                line-height: 1.35;
            }}
            .process-step-desc {{
                font-size: 1.06rem;
                line-height: 1.65;
                color: var(--text-muted);
                margin: 0;
            }}
            @media (max-width: 768px) {{
                .process-steps-connector {{ display: none; }}
                .process-steps-list {{ grid-template-columns: 1fr; gap: 56px; }}
                .process-steps {{ margin: 40px auto 64px; padding: 52px 24px; }}
            }}

            .modal-overlay {{
                position: fixed; inset: 0; background: rgba(0, 0, 0, 0.5);
                backdrop-filter: blur(4px); z-index: 2000;
                display: none; align-items: center; justify-content: center;
                padding: 20px; box-sizing: border-box;
                opacity: 0; transition: opacity 0.3s ease;
            }}
            .modal-overlay.show {{
                display: flex; opacity: 1;
            }}
            .modal-content {{
                background: var(--card-bg); backdrop-filter: blur(20px);
                border-radius: 24px; max-width: 560px; width: 100%;
                max-height: 80vh; overflow: hidden;
                display: flex; flex-direction: column;
                box-shadow: 0 24px 48px rgba(0, 0, 0, 0.2);
                border: 1px solid rgba(255, 255, 255, 0.3);
                transform: scale(0.95); opacity: 0;
                transition: transform 0.3s ease, opacity 0.3s ease;
            }}
            .modal-overlay.show .modal-content {{
                transform: scale(1); opacity: 1;
            }}
            .modal-header {{
                flex-shrink: 0;
                padding: 20px 24px; border-bottom: 1px solid rgba(0,0,0,0.08);
                display: flex; align-items: center; justify-content: space-between;
                background: var(--card-bg);
            }}
            .modal-header h3 {{
                margin: 0; font-size: 1.25rem; color: var(--accent);
            }}
            .modal-close {{
                background: none; border: none; cursor: pointer;
                font-size: 1.5rem; color: var(--text-color); opacity: 0.7;
                padding: 0; line-height: 1;
            }}
            .modal-close:hover {{ opacity: 1; }}
            .modal-body {{
                flex: 1; min-height: 0;
                padding: 24px; overflow-y: auto; overflow-x: hidden;
                text-align: right; line-height: 1.7; color: var(--text-color);
                -webkit-overflow-scrolling: touch;
            }}
            .modal-body::-webkit-scrollbar {{
                width: 8px;
            }}
            .modal-body::-webkit-scrollbar-track {{
                background: rgba(0,0,0,0.06); border-radius: 4px;
            }}
            .modal-body::-webkit-scrollbar-thumb {{
                background: var(--accent); border-radius: 4px;
            }}
            .tehillim-shuffle-wrap {{
                margin-bottom: 16px; text-align: center;
            }}
            .tehillim-shuffle-btn {{
                padding: 12px 24px; border-radius: 14px; border: 1px solid var(--accent);
                background: rgba(0,122,255,0.1); color: var(--accent);
                font-weight: 700; font-family: 'Heebo'; cursor: pointer;
                transition: background 0.2s, color 0.2s;
            }}
            .tehillim-shuffle-btn:hover {{
                background: var(--accent); color: #fff;
            }}
            #tehillim-grid-container {{
                display: grid; grid-template-columns: repeat(10, 1fr);
                gap: 6px; max-height: 50vh; overflow-y: auto;
                direction: rtl;
            }}
            #tehillim-chapter-view {{
                direction: rtl; text-align: right;
            }}
            .tehillim-grid-num {{
                aspect-ratio: 1; min-width: 0; min-height: 0;
                display: flex; align-items: center; justify-content: center;
                padding: 4px; border-radius: 8px;
                background: rgba(255,255,255,0.4); border: 1px solid rgba(255,255,255,0.4);
                font-size: 0.8rem; font-weight: 700; cursor: pointer;
                transition: transform 0.2s, background 0.2s;
            }}
            .tehillim-grid-num:hover {{
                background: var(--accent); color: #fff;
            }}

            #result-card {{
                display: none; margin: 36px auto 0; padding: 0;
                background: var(--card-bg);
                backdrop-filter: blur(20px); border-radius: 32px;
                animation: slideIn 0.4s ease-out; box-shadow: 0 18px 40px rgba(0,0,0,0.1);
                overflow: hidden;
                width: 100%; max-width: 100%;
                position: relative !important;
                box-sizing: border-box;
            }}
            .result-card-back {{
                display: flex; flex-direction: row; align-items: center; justify-content: center;
                gap: 10px; padding: 12px 20px;
                background: rgba(0, 0, 0, 0.04);
                border-bottom: 1px solid rgba(0, 0, 0, 0.06);
            }}
            [data-theme="dark"] .result-card-back {{
                background: rgba(255, 255, 255, 0.06);
                border-bottom-color: rgba(255, 255, 255, 0.08);
            }}
            .result-card-back-btn {{
                display: inline-flex; align-items: center; justify-content: center;
                width: 32px; height: 32px; padding: 0;
                background: rgba(0, 0, 0, 0.06);
                border: none; border-radius: 10px;
                color: var(--text-color); opacity: 0.85;
                cursor: pointer; transition: opacity 0.2s, background 0.2s;
            }}
            .result-card-back-btn:hover {{
                opacity: 1; background: rgba(0, 0, 0, 0.1);
            }}
            .result-breadcrumbs {{
                font-size: 0.85rem; color: var(--text-color);
                opacity: 0.85;
            }}
            .result-breadcrumb-link {{
                color: var(--text-color); opacity: 0.9;
                cursor: pointer; text-decoration: none;
                transition: opacity 0.2s;
            }}
            .result-breadcrumb-link:hover {{
                opacity: 1; text-decoration: underline;
            }}
            .result-breadcrumb-sep {{
                margin: 0 6px; opacity: 0.6;
            }}

            .bracha-card-header {{
                padding: 32px 32px 24px; text-align: center; border-bottom: 1px solid rgba(0,0,0,0.06);
            }}
            .bracha-card-body {{
                padding: 28px 32px 32px; text-align: right;
            }}
            .bracha-section {{
                background: rgba(0,0,0,0.03); border-radius: 18px; padding: 22px 24px;
                margin-bottom: 18px; border: 1px solid rgba(0,0,0,0.05);
            }}
            .bracha-section:last-child {{
                margin-bottom: 0;
            }}
            .bracha-section-title {{
                font-size: 0.95rem; font-weight: 700; color: var(--accent); margin-bottom: 10px;
                letter-spacing: 0.02em;
            }}
            .bracha-section-name {{
                font-size: 1.28rem; font-weight: 700; color: var(--text-color); margin-bottom: 8px;
            }}
            .bracha-section-text {{
                font-size: 1.45rem; line-height: 1.6; color: var(--text-color);
                font-weight: 400; letter-spacing: 0.01em;
            }}
            .whatsapp-share-wrap {{
                padding: 0 28px 24px; text-align: center;
            }}
            .whatsapp-share-btn {{
                display: inline-flex; align-items: center; justify-content: center; gap: 12px;
                background: var(--accent-tint); color: var(--accent);
                border: 1px solid rgba(0, 122, 255, 0.3); border-radius: 16px;
                padding: 16px 28px; font-size: 1.05rem; font-weight: 700; font-family: 'Heebo', sans-serif;
                cursor: pointer; backdrop-filter: blur(12px); -webkit-backdrop-filter: blur(12px);
                box-shadow: 0 4px 16px rgba(0, 122, 255, 0.12), inset 0 1px 0 rgba(255,255,255,0.4);
                transition: transform 0.2s, box-shadow 0.2s, background 0.2s;
                min-height: 48px; min-width: 160px;
            }}
            .whatsapp-share-btn:hover {{
                background: var(--accent); color: #fff;
                border-color: var(--accent);
                box-shadow: 0 6px 20px rgba(0, 122, 255, 0.25);
            }}
            .whatsapp-share-btn:active {{
                transform: translateY(0);
            }}
            .whatsapp-share-btn i {{
                font-size: 1.4rem;
            }}
            [data-theme="dark"] .whatsapp-share-btn {{
                border-color: rgba(94, 184, 255, 0.35);
                box-shadow: 0 4px 16px rgba(0,0,0,0.2), inset 0 1px 0 rgba(255,255,255,0.06);
            }}
            [data-theme="dark"] .whatsapp-share-btn:hover {{
                box-shadow: 0 6px 20px rgba(94, 184, 255, 0.2);
            }}
            @media (max-width: 480px) {{
                .whatsapp-share-wrap {{
                    padding: 0 20px 20px;
                }}
                .whatsapp-share-btn {{
                    width: 100%; max-width: 280px; padding: 18px 24px;
                    min-height: 52px; font-size: 1.1rem;
                }}
                .whatsapp-share-btn i {{
                    font-size: 1.5rem;
                }}
            }}

            /* === Mobile: special layout and typography === */
            @media (max-width: 768px) {{
                .logo {{
                    display: none;
                }}
                .hero-tagline {{
                    font-size: 0.95rem;
                    margin-bottom: 6px;
                }}
                .hero-title {{
                    font-size: 2rem;
                    line-height: 1.25;
                    margin: 0 0 10px 0;
                }}
                .hero-subtitle {{
                    font-size: 1.05rem;
                    margin: 0 0 24px 0;
                    line-height: 1.5;
                }}
                .search-bar-pill {{
                    flex-direction: column;
                    border-radius: 24px;
                    overflow: hidden;
                    gap: 0;
                    box-shadow: 0 6px 24px rgba(0,0,0,0.1);
                }}
                .search-bar-pill input {{
                    width: 100%;
                    padding: 18px 20px;
                    font-size: 1.1rem;
                    min-width: 0;
                    min-height: 48px;
                }}
                .search-bar-btn {{
                    width: 100%;
                    padding: 18px 24px;
                    font-size: 1.15rem;
                    min-height: 52px;
                }}
                .main-content {{
                    padding: 0 20px 40px;
                    width: 100%;
                    margin-top: 32px;
                }}
                #about-content {{
                    padding: 0 20px 40px;
                    width: 100%;
                    box-sizing: border-box;
                    margin-top: 32px;
                }}
                .daily-cards-wrap {{
                    padding: 0 20px;
                    margin: 28px auto 0;
                    gap: 16px;
                }}
                .daily-card {{
                    max-width: 100%;
                    width: 100%;
                    padding: 24px 20px;
                    border-radius: 24px;
                }}
                .daily-card-title {{
                    font-size: 1.5rem;
                    margin-bottom: 12px;
                }}
                .daily-card-quote {{
                    font-size: 1.35rem;
                    line-height: 1.55;
                }}
                .daily-card-refresh {{
                    padding: 14px 24px;
                    font-size: 1.2rem;
                    min-height: 48px;
                }}
                .navbar {{
                    width: 94%;
                    padding: 10px 16px;
                    margin-top: 16px;
                }}
                .navbar .logo img {{
                    height: 48px !important;
                    max-height: 48px;
                }}
                .nav-item {{
                    padding: 10px 16px;
                    font-size: 1.05rem;
                    min-height: 44px;
                }}
                .navbar-divider {{
                    width: 94%;
                    margin: 6px auto 0;
                }}
                .suggestions {{
                    left: 0;
                    right: 0;
                    width: 100%;
                    box-sizing: border-box;
                    border-radius: 20px;
                    top: 100%;
                    margin-top: 8px;
                }}
                .suggestion-item {{
                    padding: 16px 20px;
                    font-size: 1.1rem;
                    min-height: 48px;
                }}
                .section-top {{
                    padding: 0 4px;
                }}
                .process-steps {{
                    padding: 32px 20px 48px;
                }}
                .process-steps-list {{
                    gap: 40px;
                }}
                #result-card {{
                    margin: 20px 16px 0;
                    width: calc(100% - 32px);
                    max-width: none;
                    border-radius: 24px;
                }}
                .result-card-back {{
                    padding: 14px 16px;
                    min-height: 48px;
                }}
                .result-card-back-btn {{
                    width: 40px;
                    height: 40px;
                    min-width: 40px;
                    min-height: 40px;
                }}
                .bracha-card-header {{
                    padding: 24px 20px 20px;
                }}
                .bracha-card-body {{
                    padding: 20px 20px 24px;
                }}
                .bracha-section {{
                    padding: 18px 20px;
                    border-radius: 16px;
                }}
                .bracha-section-title {{
                    font-size: 0.9rem;
                }}
                .bracha-section-name {{
                    font-size: 1.15rem;
                }}
                .bracha-section-text {{
                    font-size: 1.25rem;
                    line-height: 1.55;
                }}
                .flex-container {{
                    padding: 0 16px;
                }}
                #tehillim-grid-container {{
                    padding: 0 4px;
                    max-width: 100%;
                    gap: 8px;
                }}
                .tehillim-grid-num {{
                    min-width: 36px;
                    min-height: 36px;
                    font-size: 0.85rem;
                }}
                #analytics-content {{
                    padding: 0 20px 40px !important;
                    width: 100% !important;
                    max-width: 100% !important;
                    box-sizing: border-box;
                    margin-top: 24px !important;
                }}
                #analytics-cards {{
                    grid-template-columns: 1fr;
                    gap: 14px;
                }}
                #analytics-cards > div {{
                    padding: 20px 16px !important;
                }}
                .modal-content {{
                    margin: 16px;
                    max-height: calc(100vh - 32px);
                    border-radius: 20px;
                }}
                .modal-overlay {{
                    padding: 16px;
                }}
                footer {{
                    padding: 20px 24px !important;
                }}
                footer span {{
                    font-size: 0.85rem !important;
                }}
                #accessibility-btn {{
                    width: 48px;
                    height: 48px;
                    bottom: 16px;
                    left: 16px;
                }}
                #accessibility-panel {{
                    bottom: 72px;
                    left: 16px;
                    width: calc(100vw - 32px);
                    max-width: 280px;
                }}
            }}

            @media (max-width: 480px) {{
                .hero-title {{
                    font-size: 1.75rem;
                }}
                .hero-subtitle {{
                    font-size: 0.95rem;
                    margin: 0 0 20px 0;
                }}
                .navbar .logo img {{
                    height: 42px !important;
                }}
                .nav-item {{
                    padding: 8px 14px;
                    font-size: 1rem;
                }}
                .main-content {{
                    padding: 0 16px 36px;
                }}
                #about-content {{
                    padding: 0 16px 36px;
                }}
                .daily-cards-wrap {{
                    padding: 0 16px;
                    margin: 24px auto 0;
                }}
                .daily-card {{
                    padding: 20px 16px;
                }}
                .daily-card-title {{
                    font-size: 1.35rem;
                }}
                .daily-card-quote {{
                    font-size: 1.2rem;
                }}
                #tehillim-grid-container {{
                    grid-template-columns: repeat(5, 1fr);
                    gap: 8px;
                }}
                .tehillim-grid-num {{
                    min-width: 40px;
                    min-height: 40px;
                }}
                .about-card {{
                    padding: 24px 20px !important;
                    border-radius: 24px;
                }}
            }}

            .about-card {{
                padding: 40px; background: var(--card-bg); backdrop-filter: blur(20px);
                border-radius: 30px; line-height: 1.6; text-align: right;
            }}

            @keyframes slideIn {{ from {{ transform: translateY(20px); opacity: 0; }} to {{ transform: translateY(0); opacity: 1; }} }}

            .theme-toggle {{
                cursor: pointer;
                background: none;
                border: none;
                font-size: 1.8rem;
                padding: 4px 8px;
                border-radius: 50%;
                transition: transform 0.3s;
            }}
            .theme-toggle:hover {{
                transform: rotate(20deg);
            }}

            .scroll-reveal {{
                opacity: var(--scroll-opacity, 0);
                transform: translateY(calc(var(--scroll-y, 0) * 1px)) scale(var(--scroll-scale, 0.98));
                transition: none;
            }}

            .high-contrast {{
                filter: contrast(1.5);
            }}
            .underline-links a, .underline-links button {{
                text-decoration: underline !important;
            }}
            #accessibility-btn:hover {{
                transform: scale(1.1);
            }}

            footer span:hover {{
                color: var(--accent) !important;
            }}
            [data-theme="dark"] footer {{
                border-top-color: rgba(255,255,255,0.08);
            }}

        </style>
    </head>
    <body>
        <div class="bg-circles" aria-hidden="true">
            <div class="bg-circle bg-circle--top-right"></div>
            <div class="bg-circle bg-circle--top-left"></div>
            <div class="bg-circle bg-circle--bottom-left"></div>
        </div>
        <div class="blob" aria-hidden="true"></div>
        <div class="blob" aria-hidden="true"></div>
        <div class="floating-orbs" aria-hidden="true">
            <div class="orb orb-1"></div>
            <div class="orb orb-2"></div>
            <div class="orb orb-3"></div>
            <div class="orb orb-4"></div>
            <div class="orb-edge orb-edge-1" aria-hidden="true"></div>
            <div class="orb-edge orb-edge-2" aria-hidden="true"></div>
            <div class="orb-edge orb-edge-3" aria-hidden="true"></div>
            <div class="orb-edge orb-edge-4" aria-hidden="true"></div>
            <div class="ambient-circle ambient-circle-1" aria-hidden="true"></div>
            <div class="ambient-circle ambient-circle-2" aria-hidden="true"></div>
            <div class="ambient-circle ambient-circle-3" aria-hidden="true"></div>
        </div>
        <div class="ambient-bg" aria-hidden="true"></div>
        <div class="navbar">
            <div style="display:flex; gap:8px; align-items:center; flex:1;">
                <button id="nav-home" class="nav-item active" onclick="showPage('home')">מה נברך?</button>
                <button id="nav-about" class="nav-item" onclick="showPage('about')">אודות</button>
            </div>
            <div class="logo" onclick="showPage('home')" style="position:absolute; left:50%; transform:translateX(-50%);">
                <img src="/mylogo.png" style="height:100px; width:auto; vertical-align:middle;">
            </div>
            <div style="display:flex; flex:1; justify-content:flex-end;">
                <button class="theme-toggle" onclick="toggleTheme()" id="theme-btn">☀️</button>
            </div>
        </div>
        <hr class="navbar-divider">

        <div class="flex-container">
        <div id="home-content" class="main-content">
            <div class="section-top" id="section-top">
            <div style="opacity: 0.8; margin-bottom: 5px;" class="hero-tagline">האתר הרשמי לברכות על מאכלים</div>
            <h1 class="hero-title">מה נברך היום?</h1>
            <p class="hero-subtitle">כל המידע ההלכתי במקום אחד. פשוט הקלידו את שם המאכל וקבלו תשובה מיידית.</p>
            
            <div class="search-container">
                <div class="search-bar-pill">
                    <input type="text" id="foodInput" placeholder="חפש מאכל..." oninput="handleSearch(this.value)" aria-label="חיפוש מאכל">
                    <button type="button" class="search-bar-btn" onclick="document.getElementById('foodInput').focus()" aria-label="חיפוש">
                        <i class="fa-solid fa-magnifying-glass" aria-hidden="true"></i>
                        <span>חפש</span>
                    </button>
                </div>
                <div id="suggestions" class="suggestions"></div>
            </div>

            <div id="result-card" class="scroll-reveal">
                <div class="result-card-back">
                    <button type="button" class="result-card-back-btn" onclick="goBack()" aria-label="חזרה">
                        <i class="fa-solid fa-chevron-right" aria-hidden="true"></i>
                    </button>
                    <div class="result-breadcrumbs">
                        <a class="result-breadcrumb-link" onclick="goBack(); return false;" href="#">דף הבית</a>
                        <span class="result-breadcrumb-sep">&gt;</span>
                        <a class="result-breadcrumb-link" id="breadcrumb-category" onclick="goBack(); return false;" href="#">מאכלים</a>
                        <span class="result-breadcrumb-sep">&gt;</span>
                        <span id="breadcrumb-food"></span>
                    </div>
                </div>
                <div class="bracha-card-header">
                    <div id="res-emoji" style="font-size: 4rem; margin-bottom: 10px;"></div>
                    <div id="selected-label" style="opacity: 0.8; font-size: 1.2rem;"></div>
                </div>
                <div class="bracha-card-body">
                    <div class="bracha-section">
                        <div class="bracha-section-title">ברכה ראשונה</div>
                        <div class="bracha-section-name" id="bracha-rishona-name"></div>
                        <div class="bracha-section-text" id="rishona-full-text"></div>
                    </div>
                    <div class="bracha-section">
                        <div class="bracha-section-title">ברכה אחרונה</div>
                        <div class="bracha-section-name" id="bracha-achrona-name"></div>
                        <div class="bracha-section-text" id="achrona-full-text"></div>
                    </div>
                    <div class="whatsapp-share-wrap">
                        <button type="button" class="whatsapp-share-btn" onclick="shareOnWhatsApp()" aria-label="שתף בוואטסאפ">
                            <i class="fa-brands fa-whatsapp" aria-hidden="true"></i>
                            <span>שתף בוואטסאפ</span>
                        </button>
                    </div>
                </div>
            </div>

            <div class="daily-cards-wrap">
                <div class="daily-card inspiration-card scroll-reveal">
                    <h3 class="daily-card-title">חיזוק יומי ✨</h3>
                    <p class="daily-card-quote" id="daily-quote-text"></p>
                    <p class="daily-card-source" id="daily-quote-source"></p>
                    <button type="button" class="daily-card-refresh" onclick="fetchDailyQuote()" aria-label="רענן ציטוט">
                        <i class="fa-solid fa-arrows-rotate" aria-hidden="true"></i>
                        <span>רענן</span>
                    </button>
                </div>
                <div class="daily-card tehillim-card scroll-reveal">
                    <h3 class="daily-card-title">תהילים 📖</h3>
                    <p class="daily-card-source">בחר פרק וקרא תהילים</p>
                    <button type="button" class="daily-card-refresh" onclick="openModal('tehillim-list-modal')" aria-label="בחר פרק תהלים">
                        <i class="fa-solid fa-book-open" aria-hidden="true"></i>
                        <span>בחר פרק</span>
                    </button>
                </div>
                <div class="daily-card halacha-card scroll-reveal">
                    <h3 class="daily-card-title">הלכה יומית 📜</h3>
                    <p class="daily-card-quote" id="daily-halacha-text"></p>
                    <p class="daily-card-source" id="daily-halacha-source"></p>
                    <button type="button" class="daily-card-refresh" onclick="fetchDailyHalacha()" aria-label="רענן הלכה">
                        <i class="fa-solid fa-arrows-rotate" aria-hidden="true"></i>
                        <span>רענן</span>
                    </button>
                </div>
            </div>
            </div>

            <section id="section-goal" class="section-goal scroll-reveal">
                <h2 class="section-goal-title">מטרת האתר</h2>
                <ul class="section-goal-list">
                    <li><i class="fa-solid fa-hand-holding-heart" aria-hidden="true"></i><span>הנגשת ברכות המזון</span></li>
                    <li><i class="fa-solid fa-star-of-david" aria-hidden="true"></i><span>חיבור יומיומי ליהדות</span></li>
                    <li><i class="fa-solid fa-handshake" aria-hidden="true"></i><span>כלי עזר ידידותי לכל יהודי</span></li>
                    <li><i class="fa-solid fa-book-open" aria-hidden="true"></i><span>מקום אחד לכל המידע ההלכתי</span></li>
                </ul>
            </section>

            <section class="process-steps scroll-reveal" id="process-steps-section" aria-label="שלבי השימוש">
                <div class="process-steps-inner">
                    <div class="process-steps-connector" aria-hidden="true">
                        <svg viewBox="0 0 300 60" preserveAspectRatio="none">
                            <path pathLength="100" d="M 212 30 Q 175 8 188 30" />
                            <path pathLength="100" d="M 112 30 Q 75 8 88 30" />
                        </svg>
                    </div>
                    <div class="process-steps-list">
                        <div class="process-step">
                            <div class="process-step-num" aria-hidden="true">01</div>
                            <h3 class="process-step-title">הזן מאכל</h3>
                            <p class="process-step-desc">הקלד את שם המאכל בשדה החיפוש או בחר מהרשימה.</p>
                        </div>
                        <div class="process-step">
                            <div class="process-step-num" aria-hidden="true">02</div>
                            <h3 class="process-step-title">המערכת מנתחת</h3>
                            <p class="process-step-desc">אנו מזינים לך את הברכה הרלוונטית לפי ההלכה.</p>
                        </div>
                        <div class="process-step">
                            <div class="process-step-num" aria-hidden="true">03</div>
                            <h3 class="process-step-title">קבל את הברכה</h3>
                            <p class="process-step-desc">קרא את נוסח הברכה במלואו ושתף אם תרצה.</p>
                        </div>
                    </div>
                </div>
            </section>
        </div>

        <div id="about-content">
            <div class="about-card">
                <h2 style="color: var(--accent);">על האתר</h2>
                <p>ברוכים הבאים לאתר הברכות המודרני הראשון בישראל. האתר נועד לעזור לכל יהודי למצוא את הברכה הנכונה על המאכל שלו בצורה מהירה ונעימה.</p>
                <p>הפרויקט נבנה בטכנולוגיית <b>FastAPI</b> ומשתמש בעיצוב <b>Glassmorphism</b> מתקדם.</p>
                <hr style="opacity: 0.2;">
            </div>
        </div>
        </div>

        <div id="tefilat-modal" class="modal-overlay" onclick="if(event.target===this) closeModal('tefilat-modal')">
            <div class="modal-content">
                <div class="modal-header">
                    <h3>תפילת הדרך</h3>
                    <button type="button" class="modal-close" onclick="closeModal('tefilat-modal')" aria-label="סגור">&times;</button>
                </div>
                <div class="modal-body" id="tefilat-body"></div>
            </div>
        </div>

        <div id="random-tehillim-modal" class="modal-overlay" onclick="if(event.target===this) closeModal('random-tehillim-modal')">
            <div class="modal-content">
                <div class="modal-header">
                    <h3 id="random-tehillim-title">תהלים — פרק אקראי</h3>
                    <button type="button" class="modal-close" onclick="closeModal('random-tehillim-modal')" aria-label="סגור">&times;</button>
                </div>
                <div class="modal-body">
                    <div class="tehillim-shuffle-wrap">
                        <button type="button" class="tehillim-shuffle-btn" onclick="showRandomTehillim()">🔀 שלב פרק אחר</button>
                    </div>
                    <div id="random-tehillim-text"></div>
                </div>
            </div>
        </div>

        <div id="tehillim-list-modal" class="modal-overlay" onclick="if(event.target===this) closeModal('tehillim-list-modal')">
            <div class="modal-content">
                <div class="modal-header">
                    <h3 id="tehillim-list-title">רשימת תהלים (1–150)</h3>
                    <button type="button" class="modal-close" onclick="closeModal('tehillim-list-modal')" aria-label="סגור">&times;</button>
                </div>
                <div class="modal-body">
                    <div id="tehillim-grid-container"></div>
                    <div id="tehillim-chapter-view" style="display:none; margin-top:20px; padding-top:20px; border-top:1px solid rgba(0,0,0,0.1);">
                        <h4 id="tehillim-chapter-heading"></h4>
                        <div id="tehillim-chapter-text"></div>
                    </div>
                </div>
            </div>
        </div>

        <script>
            const foodData = {food_json};
            let currentFood = null;

            const TEFILAT_HADERECH = `יְהִי רָצוֹן מִלְּפָנֶיךָ ה' אֱלֹהֵינוּ וֵאלֹהֵי אֲבוֹתֵינוּ, שֶׁתּוֹלִיכֵנוּ לְשָׁלוֹם וְתַצְעִידֵנוּ לְשָׁלוֹם, וְתַגִּיעֵנוּ לִמְחוֹז חֶפְצֵנוּ לְחַיִּים וּלְשִׂמְחָה וּלְשָׁלוֹם. וְתַצִּילֵנוּ מִכַּף כָּל אוֹיֵב וְאוֹרֵב בַּדֶּרֶךְ, וּמִכָּל מִינֵי פֻּרְעָנִיּוֹת הַמִּתְרַעֲשׁוֹת לָבוֹא לָעוֹלָם. וְתִשְׁלַח בְּרָכָה בְּמַעֲשֵׂה יָדֵינוּ. וְתִתְּנֵנוּ לְחֵן וּלְחֶסֶד וּלְרַחֲמִים בְּעֵינֶיךָ וּבְעֵינֵי כָל רוֹאֵינוּ. בָּרוּךְ אַתָּה ה', שׁוֹמֵעַ תְּפִלָּה.`;

            function stripHtml(html) {{
                var div = document.createElement('div');
                div.innerHTML = html || '';
                return (div.textContent || div.innerText || '').trim();
            }}

            var inspirationQuotes = [
                {{ text: 'מצווה גדולה להיות בשמחה תמיד', source: 'רבי נחמן מברסלב' }},
                {{ text: 'דע שהכל לפי המחשבה', source: 'רבי נחמן מברסלב' }},
                {{ text: 'היום בו נולדת הוא היום בו אלוהים החליט שהעולם אינו יכול להתקיים בלעדיך', source: 'רבי נחמן מברסלב' }},
                {{ text: 'כל העולם כולו גשר צר מאוד, והעיקר לא לפחד כלל.', source: 'רבי נחמן מברסלב' }},
                {{ text: 'מצווה גוררת מצווה, ועבירה גוררת עבירה.', source: 'פרקי אבות ד, ב' }},
                {{ text: 'איזהו חכם? הלומד מכל אדם.', source: 'פרקי אבות ד, א' }},
                {{ text: 'במקום שאין אנשים, השתדל להיות איש.', source: 'פרקי אבות ב, ה' }},
                {{ text: 'לא עליך המלאכה לגמור, ולא אתה בן חורין להיבטל ממנה.', source: 'פרקי אבות ב, טז' }},
                {{ text: 'הוי מקבל את כל האדם בסבר פנים יפות.', source: 'פרקי אבות א, טו' }},
                {{ text: 'אם אין אני לי מי לי, וכשאני לעצמי מה אני.', source: 'פרקי אבות א, יד' }},
                {{ text: 'תשובה ומעשים טובים כתריס בפני הפורענות.', source: 'פרקי אבות ד, יא' }},
                {{ text: 'העולם נברא בחסד, ועל החסד הוא עומד.', source: 'רבי נחמן מברסלב' }},
            ];

            var dailyHalachot = [
                {{ text: 'ברכת המזון היא מצווה מהתורה.', source: 'קיצור שולחן ערוך' }},
                {{ text: 'על פרי עץ מברכים בורא פרי העץ.', source: 'קיצור שולחן ערוך' }},
                {{ text: 'אין משיחין בשעת הסעודה.', source: 'קיצור שולחן ערוך' }},
                {{ text: 'טעה ולא בירך ברכה ראשונה – מברך לפני שיטעם, ואם טעם כבר – יש לברך ברכה אחרונה אם אכל כזית.', source: 'שולחן ערוך אורח חיים' }},
                {{ text: 'על קפה ותה מברכים שהכל לפני, ובורא נפשות אחרי.', source: 'קיצור שולחן ערוך' }},
                {{ text: 'אין אוכלים ולא שותים (מלבד מים) לפני תפילת שחרית.', source: 'שולחן ערוך אורח חיים' }},
                {{ text: 'המברך על הכוס מוציא את השותים עימו אם כיוונו לצאת.', source: 'קיצור שולחן ערוך' }},
                {{ text: 'על הלחם מברכים המוציא לחם מן הארץ, ואחרי אכילה – ברכת המזון.', source: 'שולחן ערוך אורח חיים' }},
                {{ text: 'ספק ברכות להקל – כשיש ספק איזו ברכה לברך, פוסקים להקל.', source: 'קיצור שולחן ערוך' }},
                {{ text: 'טעימת מאכל מחייבת ברכה לפני הטעימה.', source: 'שולחן ערוך אורח חיים' }},
                {{ text: 'כיסוי הסכין בזמן ברכת המוציא – מנהג יפה אצל חלק מהעדות.', source: 'קיצור שולחן ערוך' }},
            ];

            function setDailyQuote(text, source) {{
                var el = document.getElementById('daily-quote-text');
                var srcEl = document.getElementById('daily-quote-source');
                if (el) el.textContent = text || '';
                if (srcEl) srcEl.textContent = source ? ('מקור: ' + source) : '';
            }}

            function pickRandomQuoteFromLibrary() {{
                var i = Math.floor(Math.random() * inspirationQuotes.length);
                var o = inspirationQuotes[i];
                setDailyQuote(o.text, o.source);
            }}

            function fetchDailyQuote() {{
                pickRandomQuoteFromLibrary();
                try {{
                    fetch('https://www.sefaria.org/api/texts/random?titles=Pirkei_Avot')
                        .then(function(r) {{ return r.json(); }})
                        .then(function(data) {{
                            try {{
                                var he = data.he;
                                var text = '';
                                if (Array.isArray(he)) {{
                                    text = he.map(function(s) {{ return stripHtml(s); }}).join(' ');
                                }} else if (he && typeof he === 'string') {{
                                    text = stripHtml(he);
                                }}
                                var ref = (data.ref || data.reference || '').replace(/_/g, ' ');
                                if (text) setDailyQuote(text, ref || 'פרקי אבות');
                            }} catch (e) {{}}
                        }})
                        .catch(function() {{}});
                }} catch (e) {{}}
            }}

            function setDailyHalacha(text, source) {{
                var el = document.getElementById('daily-halacha-text');
                var srcEl = document.getElementById('daily-halacha-source');
                if (el) el.textContent = text || '';
                if (srcEl) srcEl.textContent = source ? ('מקור: ' + source) : '';
            }}

            function pickRandomHalachaFromLibrary() {{
                var i = Math.floor(Math.random() * dailyHalachot.length);
                var o = dailyHalachot[i];
                setDailyHalacha(o.text, o.source);
            }}

            function fetchDailyHalacha() {{
                pickRandomHalachaFromLibrary();
                try {{
                    var titles = 'Kitzur_Shulchan_Aruch|Shulchan_Arukh,_Orach_Chayim';
                    fetch('https://www.sefaria.org/api/texts/random?titles=' + encodeURIComponent(titles))
                        .then(function(r) {{ return r.json(); }})
                        .then(function(data) {{
                            try {{
                                var he = data.he;
                                var text = '';
                                if (Array.isArray(he)) {{
                                    text = he.map(function(s) {{ return stripHtml(s); }}).join(' ');
                                }} else if (he && typeof he === 'string') {{
                                    text = stripHtml(he);
                                }}
                                var ref = (data.ref || data.reference || '').replace(/_/g, ' ');
                                if (text) setDailyHalacha(text, ref || 'שולחן ערוך');
                            }} catch (e) {{}}
                        }})
                        .catch(function() {{}});
                }} catch (e) {{}}
            }}

            var tehillimCache = {{}};
            function fetchTehillimFromSefaria(chapterNum, onSuccess, onError) {{
                if (tehillimCache[chapterNum]) {{
                    onSuccess(tehillimCache[chapterNum]);
                    return;
                }}
                var url = 'https://www.sefaria.org/api/texts/Psalms.' + chapterNum + '?context=0';
                fetch(url).then(function(r) {{
                    if (!r.ok) throw new Error('Network error');
                    return r.json();
                }}).then(function(data) {{
                    var he = data.he;
                    if (he && Array.isArray(he)) {{
                        var text = he.map(function(verse) {{ return stripHtml(verse); }}).join(' ');
                        tehillimCache[chapterNum] = text;
                        onSuccess(text);
                    }} else {{
                        onError('לא נמצא טקסט לפרק זה.');
                    }}
                }}).catch(function(err) {{
                    onError('שגיאה בטעינה. נסה שוב.');
                }});
            }}
            function setTehillimContent(elId, text, isLoading) {{
                var el = document.getElementById(elId);
                if (!el) return;
                if (isLoading) {{
                    el.innerHTML = '<p style="text-align:center; opacity:0.8;">טוען...</p>';
                }} else {{
                    var safe = (text || '').replace(/</g, '&lt;').replace(/>/g, '&gt;');
                    el.innerHTML = '<p style="white-space:pre-wrap; margin:0;">' + safe + '</p>';
                }}
            }}

            function openModal(id) {{
                document.getElementById(id).classList.add('show');
                document.body.style.overflow = 'hidden';
                if (id === 'tefilat-modal') {{
                    document.getElementById('tefilat-body').innerHTML = '<p style="white-space:pre-wrap; margin:0;">' + TEFILAT_HADERECH + '</p>';
                }} else if (id === 'random-tehillim-modal') {{
                    showRandomTehillim();
                }} else if (id === 'tehillim-list-modal') {{
                    var c = document.getElementById('tehillim-grid-container');
                    c.innerHTML = '';
                    for (var i = 1; i <= 150; i++) {{
                        var b = document.createElement('button');
                        b.className = 'tehillim-grid-num';
                        b.textContent = i;
                        b.onclick = (function(num) {{ return function() {{ showTehillimChapterInList(num); }}; }})(i);
                        c.appendChild(b);
                    }}
                    document.getElementById('tehillim-chapter-view').style.display = 'none';
                }}
            }}
            function closeModal(id) {{
                document.getElementById(id).classList.remove('show');
                document.body.style.overflow = '';
            }}
            function showRandomTehillim() {{
                var num = Math.floor(Math.random() * 150) + 1;
                document.getElementById('random-tehillim-title').textContent = 'תהלים פרק ' + num;
                setTehillimContent('random-tehillim-text', null, true);
                fetchTehillimFromSefaria(num, function(text) {{
                    setTehillimContent('random-tehillim-text', text, false);
                }}, function(errMsg) {{
                    setTehillimContent('random-tehillim-text', errMsg, false);
                }});
            }}
            function showTehillimChapterInList(num) {{
                document.getElementById('tehillim-chapter-heading').textContent = 'תהלים פרק ' + num;
                document.getElementById('tehillim-chapter-view').style.display = 'block';
                document.getElementById('tehillim-chapter-text').innerHTML = '<p style="text-align:center; opacity:0.8;">טוען...</p>';
                fetchTehillimFromSefaria(num, function(text) {{
                    var safe = (text || '').replace(/</g, '&lt;').replace(/>/g, '&gt;');
                    document.getElementById('tehillim-chapter-text').innerHTML = '<p style="white-space:pre-wrap; margin:0;">' + safe + '</p>';
                }}, function(errMsg) {{
                    document.getElementById('tehillim-chapter-text').innerHTML = '<p style="margin:0;">' + errMsg + '</p>';
                }});
            }}

            function shareOnWhatsApp() {{
                if (!currentFood || !foodData[currentFood]) return;
                const d = foodData[currentFood];
                const lines = [
                    d.emoji + ' ברכות על ' + currentFood,
                    '',
                    'ברכה ראשונה: ' + d.bracha_rishona,
                    d.rishona_text,
                    '',
                    'ברכה אחרונה: ' + d.bracha_achrona,
                    d.achrona_text,
                ];
                const text = lines.join('\\n');
                const url = 'https://wa.me/?text=' + encodeURIComponent(text);
                window.open(url, '_blank', 'noopener,noreferrer');
            }}

            function resetHomeState() {{
                currentFood = null;
                var input = document.getElementById('foodInput');
                if (input) input.value = '';
                var card = document.getElementById('result-card');
                if (card) card.style.display = 'none';
                var suggestions = document.getElementById('suggestions');
                if (suggestions) {{ suggestions.innerHTML = ''; suggestions.style.display = 'none'; }}
                var ids = ['res-emoji', 'selected-label', 'bracha-rishona-name', 'rishona-full-text', 'bracha-achrona-name', 'achrona-full-text', 'breadcrumb-category', 'breadcrumb-food'];
                ids.forEach(function(id) {{
                    var el = document.getElementById(id);
                    if (el) el.textContent = '';
                }});
            }}

            function showPage(page) {{
                if (page === 'home') {{
                    document.getElementById('home-content').style.display = 'block';
                    document.getElementById('about-content').style.display = 'none';
                    document.getElementById('nav-home').classList.add('active');
                    document.getElementById('nav-about').classList.remove('active');
                    resetHomeState();
                    requestAnimationFrame(function() {{
                        window.dispatchEvent(new Event('scroll'));
                    }});
                }} else {{
                    document.getElementById('home-content').style.display = 'none';
                    document.getElementById('about-content').style.display = 'block';
                    document.getElementById('nav-home').classList.remove('active');
                    document.getElementById('nav-about').classList.add('active');
                }}
            }}

            function toggleTheme() {{
                const html = document.documentElement;
                const current = html.getAttribute('data-theme');
                const next = current === 'light' ? 'dark' : 'light';
                html.setAttribute('data-theme', next);
                document.getElementById('theme-btn').innerText = next === 'dark' ? '🌙' : '☀️';
            }}

            function handleSearch(val) {{
                const box = document.getElementById('suggestions');
                box.innerHTML = '';
                if (!val) {{ box.style.display = 'none'; return; }}

                const matches = Object.keys(foodData).filter(f => f.includes(val));
                if (matches.length > 0) {{
                    box.style.display = 'block';
                    matches.forEach(m => {{
                        const d = document.createElement('div');
                        d.className = 'suggestion-item';
                        d.innerHTML = `<span>${{foodData[m].emoji}}</span> <span>${{m}}</span>`;
                        d.onclick = () => select(m);
                        box.appendChild(d);
                    }});
                }} else {{ box.style.display = 'none'; }}
            }}

            function goBack() {{
                resetHomeState();
            }}

            function select(food) {{
                currentFood = food;
                const d = foodData[food];
                document.getElementById('foodInput').value = food;
                document.getElementById('suggestions').style.display = 'none';
                document.getElementById('res-emoji').innerText = d.emoji;
                document.getElementById('selected-label').innerText = 'על ' + food;
                document.getElementById('bracha-rishona-name').innerText = d.bracha_rishona;
                document.getElementById('rishona-full-text').innerText = d.rishona_text;
                document.getElementById('bracha-achrona-name').innerText = d.bracha_achrona;
                document.getElementById('achrona-full-text').innerText = d.achrona_text;
                document.getElementById('breadcrumb-category').textContent = d.bracha_rishona;
                document.getElementById('breadcrumb-food').textContent = food;
                document.getElementById('result-card').style.display = 'block';
                window.dispatchEvent(new Event('scroll'));
            }}

            fetchDailyQuote();
            fetchDailyHalacha();

            (function() {{
                var elements = document.querySelectorAll('.scroll-reveal');
                var ticking = false;
                function updateScrollEffects() {{
                    var vh = window.innerHeight;
                    var vCenter = vh / 2;
                    elements.forEach(function(el) {{
                        var r = el.getBoundingClientRect();
                        var visibleTop = Math.max(0, r.top);
                        var visibleBottom = Math.min(vh, r.bottom);
                        var visibleHeight = Math.max(0, visibleBottom - visibleTop);
                        var ratio = r.height > 0 ? visibleHeight / r.height : 0;
                        ratio = Math.max(0, Math.min(1, ratio));
                        var elCenter = r.top + r.height / 2;
                        var parallaxY = (vCenter - elCenter) * 0.08;
                        parallaxY = Math.max(-12, Math.min(12, parallaxY));
                        var scale = 0.98 + 0.02 * 2 * Math.min(ratio, 1 - ratio);
                        if (ratio <= 0) scale = 0.98;
                        el.style.setProperty('--scroll-opacity', String(ratio));
                        el.style.setProperty('--scroll-y', String(parallaxY));
                        el.style.setProperty('--scroll-scale', String(scale));
                    }});
                    ticking = false;
                }}
                function onScroll() {{
                    if (!ticking) {{
                        ticking = true;
                        requestAnimationFrame(updateScrollEffects);
                    }}
                }}
                window.addEventListener('scroll', onScroll, {{ passive: true }});
                window.addEventListener('resize', onScroll);
                updateScrollEffects();
            }})();

            (function() {{
                var section = document.getElementById('process-steps-section');
                if (!section) return;
                var observer = new IntersectionObserver(function(entries) {{
                    entries.forEach(function(entry) {{
                        if (entry.isIntersecting) {{
                            entry.target.classList.add('journey-drawn');
                            observer.unobserve(entry.target);
                        }}
                    }});
                }}, {{ threshold: 0.25, rootMargin: '0px' }});
                observer.observe(section);
            }})();

            window.addEventListener('scroll', function() {{
                var navbar = document.querySelector('.navbar');
                if (window.scrollY > 40) {{
                    navbar.classList.add('scrolled');
                }} else {{
                    navbar.classList.remove('scrolled');
                }}
            }});

            var fontSizeLevel = 0;

            function toggleAccessibility() {{
                var panel = document.getElementById('accessibility-panel');
                panel.style.display = panel.style.display === 'none' ? 'block' : 'none';
            }}

            function changeFontSize(dir) {{
                fontSizeLevel += dir;
                fontSizeLevel = Math.max(-2, Math.min(4, fontSizeLevel));
                document.documentElement.style.fontSize = (100 + fontSizeLevel * 10) + '%';
            }}

            function toggleHighContrast() {{
                document.body.classList.toggle('high-contrast');
            }}

            function toggleUnderlineLinks() {{
                document.body.classList.toggle('underline-links');
            }}

            function resetAccessibility() {{
                fontSizeLevel = 0;
                document.documentElement.style.fontSize = '100%';
                document.body.classList.remove('high-contrast');
                document.body.classList.remove('underline-links');
            }}
        </script>

        <div id="accessibility-panel" style="display:none; position:fixed; bottom:90px; left:20px; z-index:9999; background:var(--card-bg); backdrop-filter:blur(20px); border:1px solid rgba(255,255,255,0.5); border-radius:24px; padding:24px; box-shadow:0 8px 32px rgba(0,0,0,0.15); width:220px; direction:rtl;">
            <h3 style="margin:0 0 16px 0; font-size:1.1rem; font-weight:700; color:var(--accent);">נגישות ♿</h3>
            <div style="display:flex; flex-direction:column; gap:10px;">
                <button onclick="changeFontSize(1)" style="padding:10px; border-radius:12px; border:1px solid rgba(0,122,255,0.2); background:var(--accent-tint); color:var(--text-color); font-family:Heebo; font-size:1rem; cursor:pointer;">הגדל טקסט A+</button>
                <button onclick="changeFontSize(-1)" style="padding:10px; border-radius:12px; border:1px solid rgba(0,122,255,0.2); background:var(--accent-tint); color:var(--text-color); font-family:Heebo; font-size:1rem; cursor:pointer;">הקטן טקסט A-</button>
                <button onclick="toggleHighContrast()" style="padding:10px; border-radius:12px; border:1px solid rgba(0,122,255,0.2); background:var(--accent-tint); color:var(--text-color); font-family:Heebo; font-size:1rem; cursor:pointer;">ניגודיות גבוהה</button>
                <button onclick="toggleUnderlineLinks()" style="padding:10px; border-radius:12px; border:1px solid rgba(0,122,255,0.2); background:var(--accent-tint); color:var(--text-color); font-family:Heebo; font-size:1rem; cursor:pointer;">הדגש קישורים</button>
                <button onclick="resetAccessibility()" style="padding:10px; border-radius:12px; border:1px solid rgba(255,0,0,0.2); background:rgba(255,0,0,0.06); color:#ef4444; font-family:Heebo; font-size:1rem; cursor:pointer;">איפוס</button>
            </div>
        </div>

        <button onclick="toggleAccessibility()" id="accessibility-btn" aria-label="נגישות" style="position:fixed; bottom:20px; left:20px; z-index:9999; width:52px; height:52px; border-radius:50%; background:var(--accent); color:#fff; border:none; cursor:pointer; box-shadow:0 4px 16px rgba(0,122,255,0.35); transition:transform 0.2s; display:flex; align-items:center; justify-content:center;">
            <svg xmlns="http://www.w3.org/2000/svg" width="26" height="26" viewBox="0 0 24 24" fill="white">
                <circle cx="12" cy="3.5" r="2"/>
                <path d="M12 7c-2.8 0-5 2.2-5 5s2.2 5 5 5 5-2.2 5-5-2.2-5-5-5zm0 8c-1.7 0-3-1.3-3-3s1.3-3 3-3 3 1.3 3 3-1.3 3-3 3z"/>
                <path d="M12 7v5l3 3"/>
            </svg>
        </button>

        <footer style="width:100%; padding:24px 40px; box-sizing:border-box; border-top:1px dashed rgba(0,0,0,0.1); text-align:center; direction:rtl;">
            <span style="color:var(--text-muted); font-size:0.9rem;">© כל הזכויות שמורות 2026</span>
        </footer>
    </body>
    </html>
    """
    return html_content