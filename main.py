from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import json

app = FastAPI()

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

# 100 מאכלים נפוצים: (שם, אימוג'י, ברכה ראשונה)
FOOD_LIST = [
    ("תפוח", "🍎", "בורא פרי העץ"),
    ("מלפפון", "🥒", "בורא פרי האדמה"),
    ("לחם", "🍞", "המוציא לחם מן הארץ"),
    ("במבה", "🥜", "שהכל נהיה בדברו"),
    ("אורז", "🍚", "בורא מיני מזונות"),
    ("יין", "🍷", "בורא פרי הגפן"),
    ("ענבים", "🍇", "בורא פרי העץ"),
    ("שוקולד", "🍫", "שהכל נהיה בדברו"),
    ("פיצה", "🍕", "בורא מיני מזונות"),
    ("סטייק", "🥩", "שהכל נהיה בדברו"),
    ("פסטה", "🍝", "בורא מיני מזונות"),
    ("בננה", "🍌", "בורא פרי האדמה"),
    ("תפוז", "🍊", "בורא פרי העץ"),
    ("אגוז", "🥥", "בורא פרי העץ"),
    ("עגבנייה", "🍅", "בורא פרי האדמה"),
    ("עוגה", "🍰", "בורא מיני מזונות"),
    ("ביסלי", "🥨", "שהכל נהיה בדברו"),
    ("קרמבו", "🧁", "שהכל נהיה בדברו"),
    ("מילקה", "🍫", "שהכל נהיה בדברו"),
    ("אפרופו", "🍬", "שהכל נהיה בדברו"),
    ("טוגו", "🍫", "שהכל נהיה בדברו"),
    ("וופל", "🧇", "שהכל נהיה בדברו"),
    ("חלווה", "🍬", "שהכל נהיה בדברו"),
    ("עוגיות", "🍪", "בורא מיני מזונות"),
    ("פופקורן", "🍿", "בורא מיני מזונות"),
    ("בייגלה", "🥨", "בורא מיני מזונות"),
    ("תמר", "🌴", "בורא פרי העץ"),
    ("רימון", "🍎", "בורא פרי העץ"),
    ("אבטיח", "🍉", "בורא פרי האדמה"),
    ("מלון", "🍈", "בורא פרי האדמה"),
    ("תות", "🍓", "בורא פרי האדמה"),
    ("אננס", "🍍", "בורא פרי העץ"),
    ("מנגו", "🥭", "בורא פרי העץ"),
    ("שקדים", "🥜", "בורא פרי העץ"),
    ("חמאת בוטנים", "🥜", "שהכל נהיה בדברו"),
    ("גלידה", "🍦", "שהכל נהיה בדברו"),
    ("אגס", "🍐", "בורא פרי העץ"),
    ("דובדבן", "🍒", "בורא פרי העץ"),
    ("שזיף", "🍑", "בורא פרי העץ"),
    ("נקטרינה", "🍑", "בורא פרי העץ"),
    ("אבוקדו", "🥑", "בורא פרי העץ"),
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
    ("אוכמניות", "🫐", "בורא פרי האדמה"),
    ("פטל", "🫐", "בורא פרי האדמה"),
    ("גזר", "🥕", "בורא פרי האדמה"),
    ("ברוקולי", "🥦", "בורא פרי האדמה"),
    ("כרוב", "🥬", "בורא פרי האדמה"),
    ("חסה", "🥬", "בורא פרי האדמה"),
    ("בצל", "🧅", "בורא פרי האדמה"),
    ("תפוח אדמה", "🥔", "בורא פרי האדמה"),
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
    ("חלב", "🥛", "שהכל נהיה בדברו"),
    ("מים", "💧", "שהכל נהיה בדברו"),
    ("קפה", "☕", "שהכל נהיה בדברו"),
    ("תה", "🍵", "שהכל נהיה בדברו"),
    ("מיץ", "🧃", "שהכל נהיה בדברו"),
    ("ביצה", "🥚", "שהכל נהיה בדברו"),
    ("דג", "🐟", "שהכל נהיה בדברו"),
    ("סלמון", "🍣", "שהכל נהיה בדברו"),
    ("טונה", "🐟", "שהכל נהיה בדברו"),
    ("חזה עוף", "🍗", "שהכל נהיה בדברו"),
    ("המבורגר", "🍔", "שהכל נהיה בדברו"),
    ("נקניק", "🌭", "שהכל נהיה בדברו"),
    ("צ'יפס", "🍟", "שהכל נהיה בדברו"),
    ("פלאפל", "🧆", "שהכל נהיה בדברו"),
    ("חומוס", "🫓", "שהכל נהיה בדברו"),
    ("טחינה", "🫙", "שהכל נהיה בדברו"),
    ("סושי", "🍣", "שהכל נהיה בדברו"),
    ("גבינה", "🧀", "שהכל נהיה בדברו"),
    ("יוגורט", "🥛", "שהכל נהיה בדברו"),
    ("חמאה", "🧈", "שהכל נהיה בדברו"),
    ("דבש", "🍯", "שהכל נהיה בדברו"),
    ("ריבה", "🍓", "שהכל נהיה בדברו"),
    ("סוכריה", "🍬", "שהכל נהיה בדברו"),
    ("מרשמלו", "🍡", "שהכל נהיה בדברו"),
    ("מרק", "🍲", "שהכל נהיה בדברו"),
    ("סלט", "🥗", "שהכל נהיה בדברו"),
    ("שווארמה", "🥙", "שהכל נהיה בדברו"),
    ("כבב", "🍢", "שהכל נהיה בדברו"),
    ("חמין", "🍲", "שהכל נהיה בדברו"),
    ("גפילטע פיש", "🐟", "שהכל נהיה בדברו"),
    ("קולה", "🥤", "שהכל נהיה בדברו"),
    ("לימונדה", "🍋", "שהכל נהיה בדברו"),
    ("שייק", "🥤", "שהכל נהיה בדברו"),
    ("בירה", "🍺", "שהכל נהיה בדברו"),
    ("קרואסון", "🥐", "בורא מיני מזונות"),
    ("מאפין", "🧁", "בורא מיני מזונות"),
    ("דגנים", "🥣", "בורא מיני מזונות"),
    ("גרנולה", "🥣", "בורא מיני מזונות"),
    ("פיתה", "🫓", "המוציא לחם מן הארץ"),
    ("חלה", "🍞", "המוציא לחם מן הארץ"),
    ("בורקס", "🥐", "בורא מיני מזונות"),
    ("מלאווח", "🥐", "בורא מיני מזונות"),
    ("ג'חנון", "🥐", "בורא מיני מזונות"),
    ("קוסקוס", "🍚", "בורא מיני מזונות"),
    ("קינואה", "🍚", "בורא מיני מזונות"),
    ("פנקייק", "🥞", "בורא מיני מזונות"),
    ("עוגת גבינה", "🍰", "בורא מיני מזונות"),
    ("סופגנייה", "🍩", "בורא מיני מזונות"),
    ("בייגל", "🥯", "בורא מיני מזונות"),
    ("לחם שום", "🍞", "המוציא לחם מן הארץ"),
    ("טוסט", "🍞", "המוציא לחם מן הארץ"),
    ("לחמניה", "🍞", "המוציא לחם מן הארץ"),
    ("מיץ ענבים", "🍇", "בורא פרי הגפן"),
    ("מיץ תפוזים", "🧃", "שהכל נהיה בדברו"),
    ("מיץ תפוחים", "🧃", "שהכל נהיה בדברו"),
    ("קרקר", "🍘", "בורא מיני מזונות"),
    ("כוסברה", "🌿", "בורא פרי האדמה"),
    ("פטרוזיליה", "🌿", "בורא פרי האדמה"),
    ("נענע", "🌿", "בורא פרי האדמה"),
    ("פיסטוק", "🥜", "בורא פרי העץ"),
    ("ערמונים", "🌰", "בורא פרי העץ"),
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
        <link href="https://fonts.googleapis.com/css2?family=Heebo:wght@300;400;700;900&display=swap" rel="stylesheet">
        <style>
            :root {{
                --bg-gradient: linear-gradient(-45deg, #a1c4fd, #c2e9fb, #fbc2eb, #a1c4fd);
                --card-bg: rgba(255, 255, 255, 0.7);
                --text-color: #333;
                --nav-bg: rgba(255, 255, 255, 0.8);
                --accent: #007AFF;
            }}

            [data-theme="dark"] {{
                --bg-gradient: linear-gradient(-45deg, #0f2027, #203a43, #2c5364);
                --card-bg: rgba(0, 0, 0, 0.5);
                --text-color: #fff;
                --nav-bg: rgba(0, 0, 0, 0.6);
                --accent: #00D1FF;
            }}

            body {{
                margin: 0; padding: 0; font-family: 'Heebo', sans-serif;
                background: var(--bg-gradient); background-size: 400% 400%;
                animation: gradient 15s ease infinite; min-height: 100vh;
                display: flex; flex-direction: column; align-items: center;
                color: var(--text-color); transition: 0.5s; overflow-x: hidden;
            }}

            @keyframes gradient {{
                0% {{ background-position: 0% 50%; }}
                50% {{ background-position: 100% 50%; }}
                100% {{ background-position: 0% 50%; }}
            }}

            .navbar {{
                margin-top: 20px; background: var(--nav-bg); backdrop-filter: blur(15px);
                padding: 10px 30px; border-radius: 50px; display: flex; gap: 15px;
                align-items: center; box-shadow: 0 4px 15px rgba(0,0,0,0.1);
                border: 1px solid rgba(255,255,255,0.2); z-index: 1000;
            }}

            .logo {{
                font-weight: 900; color: var(--accent); margin-left: 10px; 
                cursor: pointer; font-size: 1.2rem; display: flex; align-items: center; gap: 5px;
            }}

            .nav-item {{
                cursor: pointer; padding: 8px 18px; border-radius: 20px;
                font-weight: 500; transition: 0.3s; color: var(--text-color); border: none; background: none; font-family: 'Heebo';
            }}

            .nav-item.active {{ background: var(--accent); color: white; }}

            .main-content {{ margin-top: 60px; text-align: center; width: 90%; max-width: 600px; display: block; }}
            #about-content {{ display: none; margin-top: 60px; text-align: center; width: 90%; max-width: 600px; }}

            .search-container {{ position: relative; width: 100%; margin-top: 20px; }}
            input {{
                width: 100%; padding: 18px 25px; font-size: 1.3rem; border-radius: 30px;
                border: 1px solid rgba(255,255,255,0.3); background: var(--card-bg);
                backdrop-filter: blur(10px); color: var(--text-color); outline: none; box-sizing: border-box;
            }}

            .suggestions {{
                position: absolute; top: 70px; width: 100%; background: var(--nav-bg);
                backdrop-filter: blur(20px); border-radius: 20px; max-height: 250px;
                overflow-y: auto; display: none; z-index: 100; box-shadow: 0 10px 25px rgba(0,0,0,0.1);
            }}

            .suggestion-item {{
                padding: 12px 20px; cursor: pointer; border-bottom: 1px solid rgba(0,0,0,0.05);
                display: flex; align-items: center; gap: 10px; font-size: 1.1rem;
            }}

            .suggestion-item:hover {{ background: var(--accent); color: white; }}

            #result-card {{
                margin-top: 30px; padding: 0; background: var(--card-bg);
                backdrop-filter: blur(20px); border-radius: 30px; display: none;
                animation: slideIn 0.4s ease-out; box-shadow: 0 15px 35px rgba(0,0,0,0.1);
                overflow: hidden; max-width: 520px; width: 100%;
            }}
            .bracha-card-header {{
                padding: 28px 28px 20px; text-align: center; border-bottom: 1px solid rgba(0,0,0,0.06);
            }}
            .bracha-card-body {{
                padding: 24px 28px 28px; text-align: right;
            }}
            .bracha-section {{
                background: rgba(0,0,0,0.03); border-radius: 16px; padding: 18px 20px;
                margin-bottom: 16px; border: 1px solid rgba(0,0,0,0.05);
            }}
            .bracha-section:last-child {{
                margin-bottom: 0;
            }}
            .bracha-section-title {{
                font-size: 0.85rem; font-weight: 700; color: var(--accent); margin-bottom: 8px;
                letter-spacing: 0.02em;
            }}
            .bracha-section-name {{
                font-size: 1.15rem; font-weight: 700; color: var(--text-color); margin-bottom: 6px;
            }}
            .bracha-section-text {{
                font-size: 1.35rem; line-height: 1.55; color: var(--text-color);
                font-weight: 400; letter-spacing: 0.01em;
            }}

            .about-card {{
                padding: 40px; background: var(--card-bg); backdrop-filter: blur(20px);
                border-radius: 30px; line-height: 1.6; text-align: right;
            }}

            @keyframes slideIn {{ from {{ transform: translateY(20px); opacity: 0; }} to {{ transform: translateY(0); opacity: 1; }} }}

            .theme-toggle {{
                cursor: pointer; background: none; border: 2px solid var(--accent);
                color: var(--accent); padding: 5px 12px; border-radius: 15px; font-size: 0.8rem;
            }}
        </style>
    </head>
    <body>
        <div class="navbar">
            <div class="logo" onclick="showPage('home')">🍎 BRACHOT</div>
            <button id="nav-home" class="nav-item active" onclick="showPage('home')">מה נברך?</button>
            <button id="nav-about" class="nav-item" onclick="showPage('about')">אודות</button>
            <button class="theme-toggle" onclick="toggleTheme()">DARK MODE</button>
        </div>

        <div id="home-content" class="main-content">
            <div style="opacity: 0.8; margin-bottom: 5px;">האתר הרשמי לברכות על מאכלים</div>
            <h1 style="font-size: 3rem; font-weight: 900; margin: 0 0 20px 0;">מה נברך היום?</h1>
            
            <div class="search-container">
                <input type="text" id="foodInput" placeholder="חפש מאכל..." oninput="handleSearch(this.value)">
                <div id="suggestions" class="suggestions"></div>
            </div>

            <div id="result-card">
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
                </div>
            </div>
        </div>

        <div id="about-content">
            <div class="about-card">
                <h2 style="color: var(--accent);">על האתר</h2>
                <p>ברוכים הבאים לאתר הברכות המודרני הראשון בישראל. האתר נועד לעזור לכל יהודי למצוא את הברכה הנכונה על המאכל שלו בצורה מהירה ונעימה.</p>
                <p>הפרויקט נבנה בטכנולוגיית <b>FastAPI</b> ומשתמש בעיצוב <b>Glassmorphism</b> מתקדם.</p>
                <hr style="opacity: 0.2;">
                <p style="font-size: 0.9rem;">נוצר באהבה על ידי צוות ה-AI של הפרויקט שלך.</p>
            </div>
        </div>

        <script>
            const foodData = {food_json};

            function showPage(page) {{
                if (page === 'home') {{
                    document.getElementById('home-content').style.display = 'block';
                    document.getElementById('about-content').style.display = 'none';
                    document.getElementById('nav-home').classList.add('active');
                    document.getElementById('nav-about').classList.remove('active');
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
                document.querySelector('.theme-toggle').innerText = next === 'light' ? 'DARK MODE' : 'LIGHT MODE';
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

            function select(food) {{
                const d = foodData[food];
                document.getElementById('foodInput').value = food;
                document.getElementById('suggestions').style.display = 'none';
                document.getElementById('res-emoji').innerText = d.emoji;
                document.getElementById('selected-label').innerText = 'על ' + food;
                document.getElementById('bracha-rishona-name').innerText = d.bracha_rishona;
                document.getElementById('rishona-full-text').innerText = d.rishona_text;
                document.getElementById('bracha-achrona-name').innerText = d.bracha_achrona;
                document.getElementById('achrona-full-text').innerText = d.achrona_text;
                document.getElementById('result-card').style.display = 'block';
            }}
        </script>
    </body>
    </html>
    """
    return html_content