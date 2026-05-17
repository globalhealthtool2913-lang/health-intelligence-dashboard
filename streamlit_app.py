import streamlit as st
import pandas as pd
import numpy as np
import requests
import sqlite3
import pydeck as pdk

from datetime import datetime
from sklearn.ensemble import IsolationForest
from sklearn.linear_model import LinearRegression

# ==================================================
# PAGE CONFIG
# ==================================================
st.set_page_config(
    page_title="WHO Digital Twin",
    layout="wide"
)

st.title("🌍 WHO DIGITAL TWIN SYSTEM")
st.caption(
    "Continuous global surveillance + forecasting platform"
)

# ==================================================
# DATABASE
# ==================================================
DB = "who_digital_twin.db"

def init_db():

    conn = sqlite3.connect(DB)
    c = conn.cursor()

    c.execute("""
        CREATE TABLE IF NOT EXISTS signals (
            country TEXT,
            signal REAL,
            source TEXT,
            timestamp TEXT
        )
    """)

    conn.commit()
    conn.close()

init_db()

# ==================================================
# SAVE DATA
# ==================================================
def save_data(df):

    conn = sqlite3.connect(DB)

    df.to_sql(
        "signals",
        conn,
        if_exists="append",
        index=False
    )

    conn.close()

# ==================================================
# LOAD DATA
# ==================================================
def load_data():

    conn = sqlite3.connect(DB)

    try:

        df = pd.read_sql(
            "SELECT * FROM signals",
            conn
        )

    except:

        df = pd.DataFrame(
            columns=[
                "country",
                "signal",
                "source",
                "timestamp"
            ]
        )

    conn.close()

    return df

# ==================================================
# LIVE SOURCE (GDELT)
# ==================================================
@st.cache_data(ttl=300)
def fetch_gdelt():

    try:

        url = (
            "https://api.gdeltproject.org/"
            "api/v2/doc/doc"
        )

        params = {
            "query":
            "health OR outbreak OR epidemic "
            "OR virus OR disease",

            "mode": "ArtList",
            "format": "json"
        }

        r = requests.get(
            url,
            params=params,
            timeout=10
        )

        if r.status_code != 200:
            return pd.DataFrame()

        data = r.json()

        articles = data.get(
            "articles",
            []
        )

        rows = []

        for a in articles:

            rows.append({
                "country":
                a.get(
                    "sourceCountry",
                    "Unknown"
                ),

                "signal": 1,

                "source":
                "GDELT",

                "timestamp":
                str(datetime.utcnow())
            })

        return pd.DataFrame(rows)

    except:
        return pd.DataFrame()

# ==================================================
# SYNTHETIC DIGITAL TWIN
# ==================================================
def synthetic_world():

    countries = [
        "Ethiopia",
        "Kenya",
        "USA",
        "India",
        "Brazil",
        "Germany",
        "China",
        "South Africa"
    ]

    return pd.DataFrame({

        "country":
        countries,

        "signal":
        np.random.randint(
            20,
            500,
            len(countries)
        ),

        "source":
        "SYNTHETIC",

        "timestamp":
        str(datetime.utcnow())
    })

# ==================================================
# INGESTION
# ==================================================
gdelt_df = fetch_gdelt()

if not gdelt_df.empty:
    save_data(gdelt_df)

save_data(
    synthetic_world()
)

# ==================================================
# LOAD WORLD STATE
# ==================================================
df = load_data()

if df.empty:

    st.warning(
        "⚠️ Initializing WHO Digital Twin..."
    )

    df = synthetic_world()

# ==================================================
# CLEANING
# ==================================================
df["signal"] = pd.to_numeric(
    df["signal"],
    errors="coerce"
)

df = df.dropna()

# ==================================================
# AGGREGATION
# ==================================================
world = (
    df.groupby("country")["signal"]
    .sum()
    .reset_index()
)

# ==================================================
# COORDINATES
# ==================================================
coords = {

    "Ethiopia":
    [9.145, 40.4897],

    "Kenya":
    [-1.286389, 36.817223],

    "USA":
    [37.0902, -95.7129],

    "India":
    [20.5937, 78.9629],

    "Brazil":
    [-14.235, -51.9253],

    "Germany":
    [51.1657, 10.4515],

    "China":
    [35.8617, 104.1954],

    "South Africa":
    [-30.5595, 22.9375]
}

world["lat"] = world["country"].apply(
    lambda x: coords.get(x, [0, 0])[0]
)

world["lon"] = world["country"].apply(
    lambda x: coords.get(x, [0, 0])[1]
)

# ==================================================
# RISK ENGINE
# ==================================================
world["risk_score"] = (
    world["signal"]
    /
    world["signal"].max()
) * 100

# ==================================================
# ML ENGINE
# ==================================================
if len(world) >= 5:

    model = IsolationForest(
        contamination=0.2,
        random_state=42
    )

    world["anomaly"] = (
        model.fit_predict(
            world[["risk_score"]]
        )
    )

    world["status"] = (
        world["anomaly"]
        .apply(
            lambda x:
            "🚨 OUTBREAK"
            if x == -1
            else "🟢 STABLE"
        )
    )

else:
    world["status"] = "🟡 LOW DATA"

# ==================================================
# WHO ALERT LEVELS
# ==================================================
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

world["WHO_ALERT"] = (
    world["risk_score"]
    .apply(who_alert)
)

# ==================================================
# METRICS
# ==================================================
st.subheader(
    "📊 Global Intelligence Overview"
)

col1, col2, col3 = st.columns(3)

col1.metric(
    "Countries",
    len(world)
)

col2.metric(
    "Outbreak Zones",
    (
        world["status"]
        ==
        "🚨 OUTBREAK"
    ).sum()
)

col3.metric(
    "Average Risk",
    round(
        world["risk_score"]
        .mean(),
        2
    )
)

# ==================================================
# TABLE
# ==================================================
st.subheader(
    "📊 World State"
)

st.dataframe(
    world,
    use_container_width=True
)

# ==================================================
# GLOBAL MAP
# ==================================================
st.subheader(
    "🗺️ Global Risk Map"
)

layer = pdk.Layer(
    "ScatterplotLayer",
    data=world,
    get_position='[lon, lat]',
    get_radius='risk_score * 50000',
    get_fill_color='[255, 0, 0, 140]',
    pickable=True
)

view_state = pdk.ViewState(
    latitude=20,
    longitude=0,
    zoom=1
)

deck = pdk.Deck(
    layers=[layer],
    initial_view_state=view_state,
    tooltip={
        "text":
        "{country}\n"
        "Risk Score: {risk_score}"
    }
)

st.pydeck_chart(deck)

# ==================================================
# TREND ENGINE
# ==================================================
st.subheader(
    "📈 Global Trend Engine"
)

mean_risk = (
    world["risk_score"]
    .mean()
)

if mean_risk > 60:

    st.error(
        "🚨 Elevated global outbreak "
        "activity detected"
    )

else:

    st.success(
        "🟢 Global conditions stable"
    )

# ==================================================
# FORECAST ENGINE
# ==================================================
st.subheader(
    "🔮 Outbreak Forecast Engine"
)

forecast_df = (
    world.copy()
    .reset_index()
)

forecast_df["time"] = (
    forecast_df.index
)

X = forecast_df[["time"]]

y = forecast_df["risk_score"]

forecast_model = (
    LinearRegression()
)

forecast_model.fit(X, y)

future_time = np.array([
    [len(forecast_df) + 1]
])

future_prediction = (
    forecast_model.predict(
        future_time
    )[0]
)

st.metric(
    "Predicted Global Risk",
    round(
        future_prediction,
        2
    )
)

if future_prediction > 70:

    st.error(
        "🚨 Forecast suggests "
        "escalating outbreak activity"
    )

elif future_prediction > 40:

    st.warning(
        "🟡 Moderate outbreak "
        "activity predicted"
    )

else:

    st.success(
        "🟢 Stable future "
        "conditions predicted"
    )

# ==================================================
# HIGHEST RISK
# ==================================================
top_country = (
    world.sort_values(
        "risk_score",
        ascending=False
    )
    .iloc[0]
)

st.subheader(
    "🚨 Highest Risk Zone"
)

st.write(
    f"Country: "
    f"{top_country['country']}"
)

st.write(
    f"Risk Score: "
    f"{round(top_country['risk_score'],2)}"
)

st.write(
    f"WHO Alert: "
    f"{top_country['WHO_ALERT']}"
)

# ==================================================
# ARCHITECTURE
# ==================================================
st.subheader(
    "🧠 Digital Twin Architecture"
)

st.code("""
[ Live Signals ]
        ↓
[ Synthetic Twin Layer ]
        ↓
[ SQLite Memory ]
        ↓
[ Risk Aggregation ]
        ↓
[ ML Anomaly Detection ]
        ↓
[ WHO Alert System ]
        ↓
[ Geographic Risk Map ]
        ↓
[ Forecast Engine ]
        ↓
[ Streamlit Dashboard ]
""")

st.caption(
    "WHO Digital Twin System — "
    "continuous surveillance + forecasting"
)
    
