import streamlit as st
import pandas as pd
import numpy as np
import requests
from datetime import datetime

# Optional imports (fail-safe)
try:
    import plotly.express as px
except:
    px = None

try:
    from sklearn.ensemble import IsolationForest
    ml_available = True
except:
    ml_available = False

try:
    from supabase import create_client
    supabase_available = True
except:
    supabase_available = False

# =========================
# APP CONFIG
# =========================
st.set_page_config(page_title="WHO AI System v3", layout="wide")

st.title("🌍 WHO AI Intelligence System v3")
st.caption("Stable production version (Streamlit-safe)")

# =========================
# SUPABASE SAFE CONNECT
# =========================
SUPABASE_URL = "https://bboiakuwwvqdlpnzlhct.supabase.co"
SUPABASE_KEY = "sb_publishable_BqQ_HClqREj01bd164av9A_Sl8XG1-Y"

supabase = None

if supabase_available and "PUT_YOUR" not in SUPABASE_KEY:

    try:
        supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
        st.success("🟢 Supabase connected")
    except:
        st.warning("⚠️ Supabase not connected (running offline mode)")
else:
    st.warning("⚠️ Supabase disabled or missing key")

# =========================
# DATA LOADING (SAFE)
# =========================
def load_data():

    try:
        url = "https://disease.sh/v3/covid-19/countries"
        data = requests.get(url, timeout=10).json()

        df = pd.DataFrame(data)[[
            "country",
            "casesPerOneMillion",
            "deathsPerOneMillion"
        ]]

        df.columns = ["Country", "Cases", "Deaths"]
        df["Policy"] = np.random.randint(40, 90, len(df))

    except:
        df = pd.DataFrame({
            "Country": ["Ethiopia", "Kenya", "USA", "India", "Brazil"],
            "Cases": np.random.randint(1000, 5000, 5),
            "Deaths": np.random.randint(50, 300, 5),
            "Policy": np.random.randint(40, 90, 5)
        })

    return df

df = load_data()

# =========================
# AI LAYER (SAFE)
# =========================
def compute_risk(df):

    df["risk_score"] = (
        df["Cases"] * 0.4 +
        df["Deaths"] * 0.4 +
        (100 - df["Policy"]) * 0.2
    )

    return df


def detect_anomaly(df):

    if ml_available:

        model = IsolationForest(contamination=0.1, random_state=42)
        df["anomaly"] = model.fit_predict(df[["risk_score"]])

        df["anomaly"] = df["anomaly"].apply(
            lambda x: "ALERT" if x == -1 else "OK"
        )
    else:
        df["anomaly"] = "OK"

    return df


df = compute_risk(df)
df = detect_anomaly(df)

# =========================
# SUPABASE SAVE (SAFE)
# =========================
def save_to_supabase(df):

    if supabase is None:
        return

    for _, row in df.iterrows():
        try:
            supabase.table("outbreak_history").insert({
                "country": row["Country"],
                "risk_score": float(row["risk_score"]),
                "anomaly": row["anomaly"],
                "timestamp": str(datetime.utcnow())
            }).execute()
        except:
            pass

save_to_supabase(df)

# =========================
# FILTERS
# =========================
st.sidebar.header("Filters")

countries = st.sidebar.multiselect(
    "Countries",
    df["Country"].tolist(),
    default=df["Country"].tolist()
)

filtered = df[df["Country"].isin(countries)]

# =========================
# METRICS
# =========================
st.subheader("📊 Global Health Overview")

c1, c2, c3 = st.columns(3)

c1.metric("Countries", len(filtered))
c2.metric("Avg Risk", round(filtered["risk_score"].mean(), 2))
c3.metric("Alerts", int((filtered["anomaly"] == "ALERT").sum()))

# =========================
# ALERTS
# =========================
st.subheader("🚨 Alerts")

alerts = filtered[filtered["anomaly"] == "ALERT"]

if alerts.empty:
    st.success("No major outbreaks detected")
else:
    for _, row in alerts.iterrows():
        st.error(f"{row['Country']} - HIGH RISK")

# =========================
# CHARTS (SAFE)
# =========================
st.subheader("📈 Risk Chart")

if px:
    fig = px.bar(filtered, x="Country", y="risk_score")
    st.plotly_chart(fig, use_container_width=True)
else:
    st.bar_chart(filtered.set_index("Country")["risk_score"])

# =========================
# TABLE
# =========================
st.subheader("📋 Data")
st.dataframe(filtered)

# =========================
# FOOTER
# =========================
st.markdown("---")
st.write("WHO AI System v3 | Stable Mode | No Crash Architecture")
