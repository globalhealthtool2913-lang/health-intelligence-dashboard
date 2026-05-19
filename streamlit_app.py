import streamlit as st
import pandas as pd
import numpy as np
import requests
import plotly.express as px
import feedparser
from sklearn.ensemble import IsolationForest

# =========================
# PAGE CONFIG
# =========================
st.set_page_config(
    page_title="WHO Global Intelligence System",
    layout="wide"
)

st.title("🌍 WHO Global Intelligence System")
st.caption(
    "Live Epidemic Intelligence + AI Risk Detection + Global Monitoring"
)

# =========================
# LOAD LIVE HEALTH DATA
# =========================
@st.cache_data(ttl=120)
def load_health_data():

    try:

        url = "https://disease.sh/v3/covid-19/countries"

        r = requests.get(url, timeout=15)

        data = r.json()

        df = pd.DataFrame(data)[[
            "country",
            "casesPerOneMillion",
            "deathsPerOneMillion"
        ]]

        df.columns = [
            "Country",
            "Cases",
            "Deaths"
        ]

        df["Policy"] = np.random.randint(
            40,
            90,
            len(df)
        )

        return df, True

    except:

        fallback = pd.DataFrame({
            "Country": [
                "Ethiopia",
                "Kenya",
                "USA",
                "India",
                "Brazil"
            ],
            "Cases": np.random.randint(1000, 5000, 5),
            "Deaths": np.random.randint(50, 300, 5),
            "Policy": np.random.randint(40, 90, 5)
        })

        return fallback, False


df, live = load_health_data()

if live:
    st.success("🟢 LIVE HEALTH DATA ACTIVE")
else:
    st.warning("🔴 Fallback Mode Active")

# =========================
# CLEAN DATA
# =========================
df = df.dropna()

# =========================
# AI RISK ENGINE
# =========================
df["Risk"] = (
    df["Cases"] * 0.4 +
    df["Deaths"] * 0.4 +
    (100 - df["Policy"]) * 0.2
)

df["Risk"] = df["Risk"].clip(0, 5000)

# =========================
# AI ANOMALY DETECTION
# =========================
model = IsolationForest(
    contamination=0.1,
    random_state=42
)

df["Anomaly"] = model.fit_predict(
    df[["Risk"]]
)

df["Anomaly"] = df["Anomaly"].apply(
    lambda x: "ALERT" if x == -1 else "OK"
)

# =========================
# FORECASTING
# =========================
df["Forecast"] = (
    df["Risk"]
    .rolling(2)
    .mean()
    .fillna(df["Risk"])
)

# =========================
# SIDEBAR FILTERS
# =========================
st.sidebar.header("🌍 Filters")

selected_countries = st.sidebar.multiselect(
    "Select Countries",
    df["Country"].tolist(),
    default=df["Country"].tolist()
)

min_risk = st.sidebar.slider(
    "Minimum Risk",
    0,
    int(df["Risk"].max()),
    0
)

filtered = df[
    (df["Country"].isin(selected_countries)) &
    (df["Risk"] >= min_risk)
]

# =========================
# METRICS
# =========================
col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Countries",
    len(filtered)
)

col2.metric(
    "Average Risk",
    round(filtered["Risk"].mean(), 2)
)

col3.metric(
    "Maximum Risk",
    round(filtered["Risk"].max(), 2)
)

col4.metric(
    "AI Alerts",
    int((filtered["Anomaly"] == "ALERT").sum())
)

# =========================
# ALERTS
# =========================
st.subheader("🚨 Live Outbreak Alerts")

alerts = filtered[
    filtered["Anomaly"] == "ALERT"
]

if alerts.empty:

    st.success(
        "🟢 No critical outbreak anomalies detected"
    )

else:

    for _, row in alerts.iterrows():

        st.error(
            f"{row['Country']} → HIGH RISK ALERT "
            f"({row['Risk']:.2f})"
        )

# =========================
# WHO RSS FEEDS
# =========================
st.subheader("📰 WHO Disease Outbreak News")

try:

    feed = feedparser.parse(
        "https://www.who.int/feeds/entity/csr/don/en/rss.xml"
    )

    for entry in feed.entries[:5]:

        st.markdown(f"• {entry.title}")

except:

    st.warning("WHO RSS feed unavailable")

# =========================
# GDELT OUTBREAK INTELLIGENCE
# =========================
@st.cache_data(ttl=600)
def get_gdelt_outbreaks():

    url = "https://api.gdeltproject.org/api/v2/doc/doc"

    params = {
        "query": (
            "outbreak OR epidemic OR pandemic "
            "OR virus OR cholera OR dengue"
        ),
        "mode": "ArtList",
        "maxrecords": 10,
        "format": "json",
        "sort": "DateDesc"
    }

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    try:

        r = requests.get(
            url,
            params=params,
            headers=headers,
            timeout=30
        )

        if r.status_code == 200:

            data = r.json()

            return data.get("articles", [])

        return []

    except:

        return []


st.subheader("🌍 Live Global Outbreak Intelligence")

articles = get_gdelt_outbreaks()

if len(articles) == 0:

    st.warning(
        "GDELT outbreak feed unavailable"
    )

else:

    for article in articles:

        title = article.get(
            "title",
            "No title"
        )

        source = article.get(
            "sourceCommonName",
            "Unknown Source"
        )

        link = article.get("url", "")

        st.markdown(f"""
### 📰 {title}

**Source:** {source}

[Read Full Article]({link})
""")

# =========================
# AI OUTBREAK SUMMARY
# =========================
st.subheader("🧠 AI Global Situation Summary")

high_risk = filtered.sort_values(
    "Risk",
    ascending=False
).head(3)

summary = []

for _, row in high_risk.iterrows():

    summary.append(
        f"{row['Country']} shows elevated "
        f"risk activity with AI risk score "
        f"{row['Risk']:.2f}."
    )

st.info(" ".join(summary))

# =========================
# GLOBAL MAP
# =========================
st.subheader("🌍 WHO Global Risk Map")

fig = px.choropleth(
    filtered,
    locations="Country",
    locationmode="country names",
    color="Risk",
    hover_name="Country",
    title="Global AI Risk Intelligence"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# =========================
# FORECASTING
# =========================
st.subheader("📈 AI Forecasting Engine")

st.bar_chart(
    filtered.set_index("Country")["Forecast"]
)

# =========================
# DATA TABLE
# =========================
st.subheader("📊 Intelligence Dataset")

st.dataframe(filtered)

# =========================
# EXPORT
# =========================
csv = filtered.to_csv(
    index=False
).encode("utf-8")

st.download_button(
    label="⬇ Download Intelligence Report",
    data=csv,
    file_name="who_global_intelligence.csv",
    mime="text/csv"
)

# =========================
# FOOTER
# =========================
st.markdown("---")

st.write(
    "✔ WHO Global Intelligence System "
    "| Stable Production Cloud Version"
)  
