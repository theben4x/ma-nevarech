import streamlit as st
import openai
import pandas as pd
import io
import base64
import json
import re

# --- הגדרות דף ---
st.set_page_config(page_title="קמפיונר AI", page_icon="🪄", layout="centered")

# --- CSS מתקדם: פונט Heebo, מרכזיות ועיצוב SaaS ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Heebo:wght@300;400;700;900&display=swap');
    
    /* הגדרות גלובליות */
    .stApp {
        background-color: #0f172a;
        color: #f1f5f9;
        font-family: 'Heebo', sans-serif;
        direction: RTL;
    }
    
    /* מרכז את כל התוכן */
    .main .block-container {
        max-width: 800px;
        padding-top: 5rem;
    }

    /* כותרת על חלל */
    .hero-title {
        font-weight: 900;
        font-size: 4rem;
        background: linear-gradient(to bottom right, #fff 30%, #64748b);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 0.5rem;
        letter-spacing: -1px;
    }
    
    .hero-subtitle {
        text-align: center;
        color: #94a3b8;
        font-size: 1.2rem;
        margin-bottom: 3rem;
    }

    /* עיצוב שדות קלט - נקי וברור */
    .stTextInput>div>div>input {
        background-color: rgba(255,255,255,0.03) !important;
        border: 1px solid rgba(255,255,255,0.1) !important;
        border-radius: 16px !important;
        padding: 15px !important;
        color: white !important;
        font-size: 1.1rem !important;
    }
    
    /* כרטיסיית פוסט */
    .post-card {
        background: #1e293b;
        border: 1px solid #334155;
        border-radius: 20px;
        padding: 30px;
        margin-top: 25px;
        box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1);
    }

    /* כפתור */
    .stButton>button {
        background-color: #f8fafc !important;
        color: #0f172a !important;
        border-radius: 12px !important;
        font-weight: 700 !important;
        border: none !important;
        padding: 12px 24px !important;
        transition: all 0.2s;
    }
    .stButton>button:hover {
        transform: scale(1.02);
        background-color: #e2e8f0 !important;
    }

    /* פוטר */
    .footer {
        text-align: center;
        font-size: 0.8rem;
        color: #475569;
        margin-top: 5rem;
        padding-bottom: 2rem;
        letter-spacing: 1px;
    }

    /* סעיף CSV */
    .section-label {
        font-size: 0.95rem;
        color: #94a3b8;
        margin: 1.5rem 0 0.75rem 0;
        text-align: right;
    }
    /* העלאת קובץ – עיצוב תואם */
    [data-testid="stFileUploader"] {
        border-radius: 12px;
        padding: 8px 0;
    }
    [data-testid="stFileUploader"] section {
        background: rgba(255,255,255,0.03) !important;
        border: 1px solid rgba(255,255,255,0.1) !important;
        border-radius: 12px !important;
        transition: border-color 0.2s ease, box-shadow 0.2s ease !important;
    }
    [data-testid="stFileUploader"] section:hover {
        border-color: rgba(148, 163, 184, 0.25) !important;
    }
    /* טבלת תוצאות */
    .stDataFrame {
        border-radius: 12px !important;
        overflow: hidden;
        border: 1px solid rgba(51, 65, 85, 0.5) !important;
    }
    [data-testid="stDataFrame"] {
        direction: RTL;
    }

    /* תצוגת תמונה שהועלתה */
    .image-upload-card {
        background: rgba(30, 41, 59, 0.4);
        border: 1px solid rgba(51, 65, 85, 0.5);
        border-radius: 16px;
        padding: 1rem;
        margin: 1rem 0;
        box-shadow: 0 4px 24px rgba(0, 0, 0, 0.15);
        text-align: center;
    }
    .image-upload-card img { border-radius: 12px; max-width: 100%; }
    .image-upload-label { font-size: 0.9rem; color: #94a3b8; margin-bottom: 0.5rem; }

    /* Sidebar – Heebo, מראה מקצועי */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0f172a 0%, #0c1222 100%) !important;
        font-family: 'Heebo', sans-serif !important;
    }
    [data-testid="stSidebar"] > div:first-child {
        padding: 1.25rem 1rem !important;
    }
    [data-testid="stSidebar"] h3 {
        font-family: 'Heebo', sans-serif !important;
        font-weight: 600 !important;
        font-size: 0.95rem !important;
        color: #e2e8f0 !important;
        letter-spacing: 0.02em !important;
        margin-bottom: 0.5rem !important;
    }
    [data-testid="stSidebar"] .stMarkdown {
        font-family: 'Heebo', sans-serif !important;
        color: #cbd5e1 !important;
        font-size: 0.9rem !important;
        line-height: 1.5 !important;
    }
    [data-testid="stSidebar"] .stCaptionContainer {
        font-family: 'Heebo', sans-serif !important;
        color: #64748b !important;
        font-size: 0.8rem !important;
    }
    [data-testid="stSidebar"] hr {
        border-color: rgba(51, 65, 85, 0.6) !important;
        margin: 1rem 0 !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- לוגיקה ---
client = openai.OpenAI(api_key="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")

# --- Campaign history (persist in session) ---
if "campaign_history" not in st.session_state:
    st.session_state["campaign_history"] = []
if "vision_specs" not in st.session_state:
    st.session_state["vision_specs"] = None


def encode_image_to_base64(image_bytes: bytes) -> str:
    """Encode image bytes to Base64 string (standard AI practice for vision APIs)."""
    return base64.standard_b64encode(image_bytes).decode("utf-8")


def analyze_image_vision(client, image_base64: str, image_mime: str) -> dict:
    """Analyze image with Vision; return Brand, Colors, Product Category, Target Audience (strictly from image)."""
    url = f"data:{image_mime};base64,{image_base64}"
    prompt = """Analyze this image strictly from visual content only. Do not invent or assume.
Respond with a JSON object only (no markdown, no code fence), with exactly these keys:
- "Brand": brand name or label visible in the image; empty string if none.
- "Colors": main colors (e.g. "Blue, White, Gold"); empty string if unclear.
- "Product_Category": category of product/scene (e.g. "Fitness", "Food", "Fashion"); empty string if unclear.
- "Target_Audience": who the image seems to target (e.g. "Young professionals", "Families"); empty string if unclear."""
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{
            "role": "user",
            "content": [
                {"type": "text", "text": prompt},
                {"type": "image_url", "image_url": {"url": url}}
            ]
        }]
    )
    text = response.choices[0].message.content.strip()
    # Extract JSON (handle optional markdown wrapper or nested braces)
    start = text.find("{")
    if start == -1:
        return {"Brand": "", "Colors": "", "Product_Category": "", "Target_Audience": ""}
    depth, end = 0, start
    for i, c in enumerate(text[start:], start):
        if c == "{": depth += 1
        elif c == "}": depth -= 1
        if depth == 0: end = i; break
    try:
        return json.loads(text[start : end + 1])
    except json.JSONDecodeError:
        return {"Brand": "", "Colors": "", "Product_Category": "", "Target_Audience": ""}


def generate_post(client, platform: str, product: str, tone: str, audience: str) -> str:
    """Generate one marketing post for a platform."""
    prompt = f"Write a {tone} {platform} post in Hebrew for {product}. Audience: {audience or 'general'}. Include emojis and RTL punctuation."
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content.strip()


def generate_post_from_image(client, image_base64: str, image_mime: str, tone: str, audience: str, platform: str, specs: dict | None = None) -> str:
    """Use OpenAI Vision to generate a marketing post from image; optional specs from prior analysis."""
    url = f"data:{image_mime};base64,{image_base64}"
    spec_ctx = ""
    if specs:
        spec_ctx = f" Use this analysis: Brand={specs.get('Brand','')}, Colors={specs.get('Colors','')}, Product category={specs.get('Product_Category','')}, Target audience={specs.get('Target_Audience','')}."
    prompt = f"""Look at this image.{spec_ctx} Write a {tone} {platform} marketing post in Hebrew based on the visual content. Audience: {audience or 'general'}. Include emojis and correct RTL punctuation. Write only the post text, no preamble."""
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{
            "role": "user",
            "content": [
                {"type": "text", "text": prompt},
                {"type": "image_url", "image_url": {"url": url}}
            ]
        }]
    )
    return response.choices[0].message.content.strip()


def campaign_history_to_csv() -> str:
    """Export all campaigns to a clean CSV string (UTF-8)."""
    rows = []
    for i, camp in enumerate(st.session_state.get("campaign_history", []), 1):
        src = camp.get("product", "Vision") if camp.get("type") == "text" else "Vision"
        tone = camp.get("tone", "")
        aud = camp.get("audience", "")
        for p in camp.get("posts", []):
            rows.append({
                "Campaign": i,
                "Source": src,
                "Tone": tone,
                "Audience": aud,
                "Platform": p.get("platform", ""),
                "Content": p.get("content", ""),
            })
    if not rows:
        return "Campaign,Source,Tone,Audience,Platform,Content\n"
    df = pd.DataFrame(rows)
    buf = io.StringIO()
    df.to_csv(buf, index=False, encoding="utf-8-sig")
    return buf.getvalue()


def campaign_history_to_pdf() -> bytes | None:
    """Export all campaigns to a simple PDF. Returns None if reportlab not available."""
    try:
        from reportlab.lib.pagesizes import A4
        from reportlab.pdfgen import canvas
        from reportlab.lib.units import cm
    except ImportError:
        return None
    buf = io.BytesIO()
    c = canvas.Canvas(buf, pagesize=A4)
    width, height = A4
    y = height - 2 * cm
    c.setFont("Helvetica-Bold", 14)
    c.drawString(2 * cm, y, "Campaign Results - Generated Posts")
    y -= 1.2 * cm
    c.setFont("Helvetica", 10)
    for i, camp in enumerate(st.session_state.get("campaign_history", []), 1):
        src = camp.get("product", "Vision") if camp.get("type") == "text" else "Vision"
        c.setFont("Helvetica-Bold", 10)
        c.drawString(2 * cm, y, f"Campaign {i}: {src[:50]}")
        y -= 0.6 * cm
        c.setFont("Helvetica", 9)
        for p in camp.get("posts", []):
            plat = p.get("platform", "")
            content = (p.get("content", "") or "")[:500]
            c.drawString(2.2 * cm, y, f"  [{plat}]")
            y -= 0.4 * cm
            for line in content.replace("\r", "\n").split("\n")[:8]:
                if len(line) > 90:
                    line = line[:87] + "..."
                c.drawString(2.2 * cm, y, line)
                y -= 0.4 * cm
            y -= 0.2 * cm
        y -= 0.4 * cm
        if y < 2 * cm:
            c.showPage()
            y = height - 2 * cm
    c.save()
    buf.seek(0)
    return buf.read()


# --- תוכן האתר ---
st.markdown('<h1 class="hero-title">קמפיונר AI</h1>', unsafe_allow_html=True)
st.markdown('<p class="hero-subtitle">צור תוכן שיווקי ברמה עולמית בתוך שניות</p>', unsafe_allow_html=True)

# --- Sidebar: empty until image is uploaded and analyzed ---
with st.sidebar:
    if st.session_state.get("vision_specs"):
        st.markdown("### Technical Specs")
        st.caption("Image analysis (Vision)")
        s = st.session_state["vision_specs"]
        st.markdown(f"**Brand**  \n{s.get('Brand') or '—'}")
        st.markdown(f"**Colors**  \n{s.get('Colors') or '—'}")
        st.markdown(f"**Product Category**  \n{s.get('Product_Category') or '—'}")
        st.markdown(f"**Target Audience**  \n{s.get('Target_Audience') or '—'}")

# About
st.markdown("""
    <div class="about-section">
        <h2>מה זה?</h2>
        <p>כלי שיווקי מבוסס בינה מלאכותית. הזן מוצר, בחר טון וקבל פוסטים מוכנים ל-Facebook, Instagram ו-LinkedIn — בעברית, עם פיסוק נכון ל-RTL.</p>
    </div>
    """, unsafe_allow_html=True)

# חיפוש / טופס – מיכל מרכזי
st.markdown("""
    <div class="search-container">
        <div class="form-card-header"><span>צור תוכן</span></div>
    """, unsafe_allow_html=True)

product = st.text_input("", placeholder="מה המוצר שלך? (לדוגמה: מנוי לחדר כושר יוקרתי)", label_visibility="collapsed")

col1, col2 = st.columns(2)
with col1:
    audience = st.text_input("", placeholder="קהל יעד (אופציונלי)", label_visibility="collapsed")
with col2:
    tone = st.selectbox("", ["שיווקי", "חברי", "מקצועי", "מצחיק"], label_visibility="collapsed")

generate_btn = st.button("Generate Content →")

# --- Advanced Vision Module: העלאת תמונה (PNG/JPG) ---
st.markdown('<p class="section-label">מודול Vision מתקדם — העלה תמונה (PNG / JPG)</p>', unsafe_allow_html=True)
img_file = st.file_uploader("", type=["png", "jpg", "jpeg"], label_visibility="collapsed", key="img_upload")

if img_file is not None:
    st.markdown('<p class="image-upload-label">תמונה שהועלתה</p>', unsafe_allow_html=True)
    st.image(img_file, use_container_width=True)
    generate_img_btn = st.button("Analyze image & generate posts →", key="gen_img")
    if generate_img_btn:
        img_bytes = img_file.getvalue()
        img_type = img_file.type or "image/jpeg"
        img_mime = img_type if img_type.startswith("image/") else f"image/{img_type}"
        b64 = encode_image_to_base64(img_bytes)
        with st.spinner("מנתח תמונה..."):
            try:
                specs = analyze_image_vision(client, b64, img_mime)
                st.session_state["vision_specs"] = specs
            except Exception as e:
                st.error(f"שגיאה בניתוח: {e}")
                specs = {}
        if specs:
            with st.spinner("יוצר פוסטים..."):
                platforms = {"Facebook": "🔵", "Instagram": "📸", "LinkedIn": "💼"}
                posts_list = []
                for platform, icon in platforms.items():
                    try:
                        content = generate_post_from_image(client, b64, img_mime, tone, audience or "", platform, specs)
                        posts_list.append({"platform": platform, "icon": icon, "content": content})
                        st.markdown(f"""
                        <div class="post-card">
                            <small style="color: #64748b;">{icon} {platform}</small>
                            <p style="margin-top:10px; line-height:1.6;">{content}</p>
                        </div>
                        """, unsafe_allow_html=True)
                    except Exception as e:
                        st.error(f"Error: {e}")
                st.session_state["campaign_history"].append({
                    "type": "vision",
                    "specs": specs,
                    "posts": posts_list,
                })
                st.balloons()
                st.success("הפוסטים נוצרו בהצלחה")

if generate_btn:
    if product:
        with st.spinner("Writing..."):
            platforms = {"Facebook": "🔵", "Instagram": "📸", "LinkedIn": "💼"}
            posts_list = []
            for platform, icon in platforms.items():
                try:
                    content = generate_post(client, platform, product, tone, audience or "")
                    posts_list.append({"platform": platform, "icon": icon, "content": content})
                    st.markdown(f"""
                    <div class="post-card">
                        <small style="color: #64748b;">{icon} {platform}</small>
                        <p style="margin-top:10px; line-height:1.6;">{content}</p>
                    </div>
                    """, unsafe_allow_html=True)
                except Exception as e:
                    st.error(f"Error: {e}")
            if posts_list:
                st.session_state["campaign_history"].append({
                    "type": "text",
                    "product": product,
                    "tone": tone,
                    "audience": audience or "",
                    "posts": posts_list,
                })
                st.balloons()
                st.success("הפוסטים נוצרו בהצלחה")
    else:
        st.toast("נא להזין שם מוצר")

# --- העלאת CSV ויצירה מרובה ---
st.markdown('<p class="section-label">או העלה קובץ CSV</p>', unsafe_allow_html=True)
csv_file = st.file_uploader("", type=["csv"], label_visibility="collapsed", key="csv_upload")

if csv_file is not None:
    try:
        df_in = pd.read_csv(csv_file)
        df_in.columns = df_in.columns.str.strip()
        if "Product" not in df_in.columns:
            st.error("נא להעלות קובץ CSV עם עמודה בשם 'Product'.")
        else:
            products = df_in["Product"].dropna().astype(str).str.strip()
            products = products[products != ""].tolist()
            if not products:
                st.warning("לא נמצאו ערכים בעמודה 'Product'.")
            else:
                st.caption(f"נמצאו {len(products)} מוצרים. הטון וקהל היעד מהטופס למעלה יחולו על כולם.")
                generate_csv_btn = st.button("Generate posts for all products →", key="gen_csv")
                if generate_csv_btn:
                    platforms = ["Facebook", "Instagram", "LinkedIn"]
                    rows = []
                    progress = st.progress(0, text="יוצר פוסטים...")
                    for i, prod in enumerate(products):
                        row = {"Product": prod, "Tone": tone, "Audience": audience or ""}
                        for platform in platforms:
                            try:
                                row[platform] = generate_post(client, platform, prod, tone, audience or "")
                            except Exception as e:
                                row[platform] = f"[Error: {e}]"
                        rows.append(row)
                        progress.progress((i + 1) / len(products), text=f"מוצר {i+1}/{len(products)}")
                    progress.empty()
                    results_df = pd.DataFrame(rows)
                    st.session_state["csv_results"] = results_df
                    st.success(f"נוצרו פוסטים ל-{len(products)} מוצרים.")
    except Exception as e:
        st.error(f"שגיאה בקריאת הקובץ: {e}")

if "csv_results" in st.session_state:
    st.markdown("---")
    st.markdown("**תוצאות**")
    st.dataframe(st.session_state["csv_results"], use_container_width=True, height=min(400, 80 + 35 * len(st.session_state["csv_results"])))
    buf = io.StringIO()
    st.session_state["csv_results"].to_csv(buf, index=False, encoding="utf-8-sig")
    st.download_button("Download as CSV ↓", data=buf.getvalue().encode("utf-8-sig"), file_name="campaign_posts.csv", mime="text/csv", key="dl_csv")

# --- Download Results & Campaign history ---
if st.session_state["campaign_history"]:
    st.markdown("---")
    st.markdown("**Download Results**")
    csv_data = campaign_history_to_csv()
    col_dl1, col_dl2, _ = st.columns([1, 1, 2])
    with col_dl1:
        st.download_button(
            "Download as CSV",
            data=csv_data.encode("utf-8-sig"),
            file_name="campaign_results.csv",
            mime="text/csv",
            key="dl_results_csv",
        )
    with col_dl2:
        pdf_bytes = campaign_history_to_pdf()
        if pdf_bytes is not None:
            st.download_button(
                "Download as PDF",
                data=pdf_bytes,
                file_name="campaign_results.pdf",
                mime="application/pdf",
                key="dl_results_pdf",
            )
        else:
            st.caption("PDF: install reportlab")
    st.markdown("**היסטוריית קמפיינים (הסשן)**")
    for i, camp in enumerate(reversed(st.session_state["campaign_history"]), 1):
        label = f"Campaign #{len(st.session_state['campaign_history']) - i + 1}"
        if camp["type"] == "text":
            label += f" — {camp.get('product', '')}"
        else:
            label += " — Vision"
        with st.expander(label):
            for p in camp.get("posts", []):
                st.markdown(f"**{p.get('icon', '')} {p.get('platform', '')}**")
                st.markdown(p.get("content", ""))
                st.markdown("")

# Footer – תחתית הדף
st.markdown("""
    <div class="landing-footer">
        <p class="footer-line">AI Campaign OS | Professional Marketing Automation 2026</p>
    </div>
    """, unsafe_allow_html=True)