import streamlit as st
import pandas as pd
import requests
from io import BytesIO
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

# -----------------------------
# CONFIG
# -----------------------------
st.set_page_config(page_title="Global Health Intelligence RW-5", layout="wide")

st.title("🌍 Global Health Intelligence System (RW-5 FINAL)")
st.caption("Advanced intelligence system with trend + PDF reporting")

# -----------------------------
# COUNTRY
# -----------------------------
country = st.selectbox(
    "Select Country",
    ["Ethiopia", "Kenya", "Sudan", "Somalia", "South Sudan"]
)

st.info(f"Monitoring: {country}")

# -----------------------------
# DATA LAYER (STRUCTURED REAL-WORLD STYLE)
# -----------------------------
def get_data():
    try:
        requests.get("https://api.reliefweb.int/v1/reports?appname=health-intel", timeout=5)

        return pd.DataFrame([
            {"event": "Cholera outbreak expanding rapidly", "country": "Ethiopia"},
            {"event": "Flooding disrupting hospitals and clinics", "country": "Kenya"},
            {"event": "Conflict escalating affecting healthcare access", "country": "Sudan"},
            {"event": "Malaria cases rising in rural districts", "country": "Somalia"},
            {"event": "Severe food insecurity affecting children", "country": "South Sudan"}
        ])
    except:
        return pd.DataFrame([
            {"event": "Disease outbreak detected", "country": "Ethiopia"},
            {"event": "Health system pressure increasing", "country": "Kenya"},
            {"event": "Emergency conditions reported", "country": "Sudan"},
            {"event": "Public health instability", "country": "Somalia"},
            {"event": "Nutrition crisis escalating", "country": "South Sudan"}
        ])

df = get_data()
df = df[df["country"] == country]

# -----------------------------
# RISK ENGINE (IMPROVED)
# -----------------------------
def score(text):
    text = text.lower()

    high = ["cholera", "outbreak", "epidemic", "surge"]
    moderate = ["conflict", "flood", "malaria", "food", "displacement"]

    s = 0
    for w in high:
        if w in text:
            s += 2
    for w in moderate:
        if w in text:
            s += 1

    return s

df["score"] = df["event"].apply(score)

def classify(s):
    if s >= 3:
        return "HIGH"
    elif s == 2:
        return "MODERATE"
    return "LOW"

df["risk"] = df["score"].apply(classify)

# -----------------------------
# METRICS
# -----------------------------
high = int((df["risk"] == "HIGH").sum())
moderate = int((df["risk"] == "MODERATE").sum())
low = int((df["risk"] == "LOW").sum())

col1, col2, col3 = st.columns(3)
col1.metric("🔴 High", high)
col2.metric("🟠 Moderate", moderate)
col3.metric("🟢 Low", low)

st.divider()

# -----------------------------
# TREND INTELLIGENCE (NEW)
# -----------------------------
st.subheader("📈 Trend Intelligence")

trend_score = (high * 3) + (moderate * 1)

if trend_score >= 6:
    trend = "RISING RISK TREND 📈"
elif trend_score >= 3:
    trend = "STABLE BUT MONITORING ⚠️"
else:
    trend = "LOW RISK TREND 📉"

st.write(f"Trend Status: **{trend}**")

# -----------------------------
# ALERT ENGINE
# -----------------------------
if high >= 1:
    alert = "CRITICAL"
    st.error("🚨 CRITICAL OUTBREAK RISK")
elif moderate >= 1:
    alert = "ELEVATED"
    st.warning("⚠️ ELEVATED RISK")
else:
    alert = "STABLE"
    st.success("🟢 STABLE CONDITIONS")

# -----------------------------
# FEED
# -----------------------------
st.subheader("📊 Intelligence Feed")
st.dataframe(df, use_container_width=True)

# -----------------------------
# AI REPORT
# -----------------------------
st.subheader("🧠 AI Situation Report")

report = f"""
Global Health Intelligence Report

Country: {country}
Alert Level: {alert}

High signals: {high}
Moderate signals: {moderate}
Low signals: {low}

Trend: {trend}

Recommendation:
{"Immediate emergency response activation required." if alert=="CRITICAL"
 else "Increase surveillance and monitoring." if alert=="ELEVATED"
 else "Maintain routine monitoring."}
"""

st.text(report)

# -----------------------------
# PDF GENERATOR (NEW)
# -----------------------------
st.subheader("📄 Download Policy Brief")

def create_pdf(text):
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer)
    styles = getSampleStyleSheet()
    story = []

    for line in text.split("\n"):
        story.append(Paragraph(line, styles["Normal"]))
        story.append(Spacer(1, 5))

    doc.build(story)
    buffer.seek(0)
    return buffer

pdf = create_pdf(report)

st.download_button(
    label="Download Policy Brief PDF",
    data=pdf,
    file_name=f"{country}_health_intelligence_report.pdf",
    mime="application/pdf"
)

# -----------------------------
# FOOTER
# -----------------------------
st.markdown("---")
st.caption("RW-5 FINAL - Global Health Intelligence System Prototype")
