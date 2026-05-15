import streamlit as st
import pandas as pd

# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(
    page_title="Global Health Intelligence Dashboard v8",
    layout="wide"
)

st.title("🌍 Global Health Intelligence Dashboard v8")
st.markdown("AI-powered surveillance, intelligence & early warning system")

# -----------------------------
# COUNTRY SELECTION
# -----------------------------
country = st.selectbox(
    "Select Country",
    ["Ethiopia", "Kenya", "Sudan", "Somalia", "South Sudan"]
)

# -----------------------------
# DATA
# -----------------------------
data = [
    {"event": "Conflict disruption", "type": "conflict"},
    {"event": "Disease outbreak signals", "type": "outbreak"},
    {"event": "Child health trends", "type": "child"},
    {"event": "Health system capacity", "type": "system"},
    {"event": "Vaccination changes", "type": "system"}
]

df = pd.DataFrame(data)

# -----------------------------
# COUNTRY MODEL
# -----------------------------
weights = {
    "Ethiopia": {"conflict": 1.0, "outbreak": 1.0, "child": 0.9, "system": 0.9},
    "Kenya": {"conflict": 0.8, "outbreak": 0.9, "child": 0.85, "system": 0.9},
    "Sudan": {"conflict": 1.3, "outbreak": 1.2, "child": 1.1, "system": 1.0},
    "Somalia": {"conflict": 1.4, "outbreak": 1.3, "child": 1.2, "system": 1.1},
    "South Sudan": {"conflict": 1.5, "outbreak": 1.4, "child": 1.3, "system": 1.2}
}

w = weights[country]

base = {
    "conflict": 45,
    "outbreak": 45,
    "child": 25,
    "system": 15
}

df["score"] = df["type"].apply(lambda x: base[x] * w[x])

def classify(x):
    if x >= 70:
        return "HIGH"
    elif x >= 40:
        return "MODERATE"
    return "LOW"

df["risk"] = df["score"].apply(classify)

# -----------------------------
# METRICS
# -----------------------------
high = int((df["risk"] == "HIGH").sum())
moderate = int((df["risk"] == "MODERATE").sum())
low = int((df["risk"] == "LOW").sum())

# -----------------------------
# ALERT BANNER
# -----------------------------
if high >= 2:
    st.error("🚨 RED ALERT: Critical instability detected")
elif moderate >= 3:
    st.warning("⚠️ YELLOW ALERT: Elevated risk environment")
else:
    st.success("🟢 GREEN STATUS: Stable surveillance conditions")

# -----------------------------
# METRICS DISPLAY
# -----------------------------
col1, col2, col3 = st.columns(3)
col1.metric("High Risk", high)
col2.metric("Moderate Risk", moderate)
col3.metric("Low Risk", low)

# -----------------------------
# TABLE
# -----------------------------
st.subheader("📊 Intelligence Feed")
st.dataframe(df)

# -----------------------------
# SIMPLE AFRICA MAP (V8 ADDITION)
# -----------------------------
st.subheader("🗺️ Regional View (Simplified)")

map_data = pd.DataFrame({
    "country": ["Ethiopia", "Kenya", "Sudan", "Somalia", "South Sudan"],
    "risk": [high, moderate, low, moderate, high]
})

st.bar_chart(map_data.set_index("country"))

# -----------------------------
# AI CHATBOT (SIMPLE V8 VERSION)
# -----------------------------
st.subheader("🤖 AI Assistant")

if "chat" not in st.session_state:
    st.session_state.chat = []

user_input = st.text_input("Ask about health risks or situation:")

if user_input:
    if "conflict" in user_input.lower():
        reply = "Conflict-related risks are influencing health service disruption patterns."
    elif "outbreak" in user_input.lower():
        reply = "Outbreak signals require increased surveillance and reporting."
    elif "country" in user_input.lower():
        reply = f"{country} currently shows {'elevated' if high > 0 else 'moderate'} risk levels."
    else:
        reply = "I am monitoring multiple health indicators. Please ask about conflict, outbreak, or country risk."

    st.session_state.chat.append((user_input, reply))

for q, a in st.session_state.chat:
    st.markdown(f"**You:** {q}")
    st.markdown(f"**AI:** {a}")

# -----------------------------
# AI SUMMARY REPORT
# -----------------------------
st.subheader("🧠 AI Situation Report")

st.write(f"""
**Country:** {country}

- High risk signals: {high}
- Moderate risk signals: {moderate}
- Low risk signals: {low}

**Interpretation:**
System indicates {'high instability' if high >= 2 else 'moderate risk activity' if moderate >= 3 else 'stable conditions'} in {country}.

**Recommendation:**
{'Immediate response required.' if high >= 2 else 'Increase monitoring frequency.' if moderate >= 3 else 'Maintain routine surveillance.'}
""")

# -----------------------------
# FOOTER
# -----------------------------
st.markdown("---")
st.markdown("v8 - AI-assisted Global Health Intelligence System")
