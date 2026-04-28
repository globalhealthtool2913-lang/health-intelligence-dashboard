import streamlit as st

# -----------------------
# SAMPLE DATA
# -----------------------
data = [
    {"title": "Conflict impacts health services", "summary": "Emergency response needed"},
    {"title": "Disease outbreak monitoring", "summary": "No major escalation"},
    {"title": "Child health progress", "summary": "Gradual improvement"},
    {"title": "Health system strengthening", "summary": "Ongoing support"}
]

# -----------------------
# ANALYSIS FUNCTION
# -----------------------
def analyze(text):
    t = text.lower()
    score = 0
    cats = []

    if "conflict" in t:
        score += 30
        cats.append("Conflict")

    if "outbreak" in t:
        score += 30
        cats.append("Disease")

    if "child" in t:
        score += 15
        cats.append("Child Health")

    if not cats:
        cats.append("Routine")

    return score, cats

# -----------------------
# AI INSIGHT
# -----------------------
def ai_insight(high, moderate, low):
    if high > 0:
        return "⚠️ High-risk signals detected. Immediate action needed."
    elif moderate > low:
        return "⚠️ Moderate-risk situation. Monitoring recommended."
    else:
        return "✅ Stable situation. No major risks."

# -----------------------
# STREAMLIT APP
# -----------------------
st.title("Global Health Intelligence Dashboard")

results = []
high = moderate = low = 0

for item in data:
    score, cats = analyze(item["title"] + " " + item["summary"])

    if score >= 60:
        level = "HIGH"
        high += 1
    elif score >= 30:
        level = "MODERATE"
        moderate += 1
    else:
        level = "LOW"
        low += 1

    results.append([item["title"], score, level, ", ".join(cats)])

# TABLE
st.subheader("Results")
st.table(results)

# AI INSIGHT
st.subheader("AI Insight")
st.write(ai_insight(high, moderate, low))

# CHART
st.subheader("Risk Distribution")
st.bar_chart({
    "High": [high],
    "Moderate": [moderate],
    "Low": [low]
})
