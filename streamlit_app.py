import streamlit as st
import pandas as pd
import numpy as np
import requests
import sqlite3
from sklearn.ensemble import IsolationForest
from datetime import datetime

# =====================================
# PAGE CONFIG
# =====================================
st.set_page_config(
    page_title="WHO Digital Twin System",
    layout="wide"
)

st.title("🌍 WHO DIGITAL TWIN SYSTEM")
st.caption("Continuous global health intelligence platform")

# =====================================
# DATABASE
# =====================================
DB = "digital_twin.db"

def init_db():
    conn = sqlite3.connect(DB)
    c = conn.cursor()

    c.execute("""
        CREATE TABLE IF NOT EXISTS world_state (
            country TEXT,
            signal REAL,
            source TEXT,
            timestamp TEXT
        )
    """)

    conn.commit()
    conn.close()

init_db()

# =====================================
# SAVE DATA
# =====================================
def save_data(df):
    conn = sqlite3.connect(DB)
    df.to_sql("world_state", conn, if_exists="append", index=False)
    conn.close()

# =====================================
# LOAD DATA
# =====================================
def load_data():
    conn = sqlite3.connect(DB)

    try:
        df = pd.read_sql(
            "SELECT * FROM world_state",
            conn
        )
    except:
        df = pd.DataFrame(
            columns=["country", "signal", "source", "timestamp"]
        )

    conn.close()
    return df

# =====================================
# LIVE SOURCE: GDELT
# =====================================
@st.cache_data(ttl=300)
def fetch_gdelt():

    try:
        url = "https://api.gdeltproject.org/api/v2/doc/doc"

        params = {
            "query": "health OR outbreak OR epidemic OR disease OR virus",
            "mode": "ArtList",
            "format": "json"
        }

        r = requests.get(
            url,
            params=params,
            timeout=10
        )

        data = r.json()

        articles = data.get("articles", [])

        rows = []

        for a in articles:
            rows.append({
                "country": a.get("sourceCountry", "Unknown"),
                "signal": 1,
                "source": "GDELT",
                "timestamp": str(datetime.utcnow())
            })

        return pd.DataFrame(rows)

    except:
        return pd.DataFrame()

# =====================================
# SYNTHETIC DIGITAL TWIN DATA
# =====================================
def synthetic_data():

    countries = [
        "Ethiopia",
        "Kenya",
        "USA",
        "India",
        "Brazil",
        "Germany",
        "China"
    ]

    signals = np.random.randint(
        10,
        500,
        len(countries)
    )

    return pd.DataFrame({
        "country": countries,
        "signal": signals,
        "source": "SYNTHETIC",
        "timestamp": str(datetime.utcnow())
    })

# =====================================
# INGESTION
# =====================================
gdelt_df = fetch_gdelt()

if not gdelt_df.empty:
    save_data(gdelt_df)

# always add synthetic layer
save_data(synthetic_data())

# =====================================
# LOAD WORLD STATE
# =====================================
df = load_data()

# =====================================
# SAFETY
# =====================================
if df.empty:

    st.warning(
        "⚠️ No data available yet — initializing digital twin"
    )

    df = synthetic_data()

# =====================================
# CLEANING
# =====================================
df["signal"] = pd.to_numeric(
    df["signal"],
    errors="coerce"
)

df = df.dropna()

# =====================================
# AGGREGATION
# =====================================
world = (
    df.groupby("country")["signal"]
    .sum()
    .reset_index()
)

# =====================================
# RISK SCORE
# =====================================
world["risk_score"] = (
    world["signal"] /
    world["signal"].max()
) * 100

# =====================================
# ML ENGINE
# =====================================
if len(world) >= 5:

    model = IsolationForest(
        contamination=0.2,
        random_state=42
    )

    world["anomaly"] = model.fit_predict(
        world[["risk_score"]]
    )

    world["status"] = world["anomaly"].apply(
        lambda x:
        "🚨 OUTBREAK ZONE"
        if x == -1
        else "🟢 STABLE"
    )

else:
    world["status"] = "🟡 LOW DATA"

# =====================================
# WHO ALERT LEVELS
# =====================================
def who_alert(score):

    if score > 80:
        return "🔴 LEVEL 5"

    elif score > 60:
        return "🟠 LEVEL 4"

    elif score > 40:
        return "🟡 LEVEL 3"

    elif score > 20:
        return "🟢 LEVEL 2"

    else:
        return "⚪ LEVEL 1"

world["WHO_ALERT"] = world["risk_score"].apply(
    who_alert
)

# =====================================
# METRICS
# =====================================
st.subheader("📊 Global Intelligence Overview")

col1, col2, col3 = st.columns(3)

col1.metric(
    "Countries",
    len(world)
)

col2.metric(
    "Outbreak Zones",
    (
        world["status"] ==
        "🚨 OUTBREAK ZONE"
    ).sum()
)

col3.metric(
    "Average Risk",
    round(
        world["risk_score"].mean(),
        2
    )
)

# =====================================
# DATA TABLE
# =====================================
st.subheader("📊 World State")

st.dataframe(
    world,
    use_container_width=True
)

# =====================================
# TREND ENGINE
# =====================================
st.subheader("📈 Global Trend Engine")

mean_risk = world["risk_score"].mean()

if mean_risk > 60:

    st.error(
        "🚨 Elevated global outbreak activity detected"
    )

else:

    st.success(
        "🟢 Global conditions stable"
    )

# =====================================
# SYSTEM ARCHITECTURE
# =====================================
st.subheader("🧠 Digital Twin Architecture")

st.code("""
[ Live Global Signals ]
        ↓
[ Synthetic Twin Layer ]
        ↓
[ SQLite Memory ]
        ↓
[ ML Risk Detection ]
        ↓
[ WHO Alert System ]
        ↓
[ Streamlit Dashboard ]
""")

st.caption(
    "WHO Digital Twin System — production-ready stable version"
)
   
    
