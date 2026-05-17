import streamlit as st
import pandas as pd
import requests
import plotly.express as px

# ======================================
# PAGE CONFIG
# ======================================
st.set_page_config(
    page_title="WHO Global Intelligence",
    layout="wide"
)

# ======================================
# TITLE
# ======================================
st.title("🌍 WHO GLOBAL HEALTH INTELLIGENCE")
st.caption("Live global surveillance dashboard")

# ======================================
# LOAD LIVE GDELT DATA
# ======================================
@st.cache_data(ttl=300)
def load_data():

    url = "https://api.gdeltproject.org/api/v2/doc/doc"

    params = {
        "query": "health OR outbreak OR epidemic OR virus OR disease",
        "mode": "ArtList",
        "format": "json"
    }

    try:

        r = requests.get(
            url,
            params=params,
            timeout=15
        )

        # API failed
        if r.status_code != 200:
            return pd.DataFrame()

        data = r.json()

        articles = data.get("articles", [])

        rows = []

        for a in articles:

            rows.append({
                "country": a.get(
                    "sourceCountry",
                    "Unknown"
                ),

                "signal": 1,

                "title": a.get(
                    "title",
                    "No Title"
                )
            })

        return pd.DataFrame(rows)

    except:
        return pd.DataFrame()

# ======================================
# FETCH DATA
# ======================================
df = load_data()

# ======================================
# EMPTY PROTECTION
# ======================================
if df.empty:

    st.error(
        "❌ Live GDELT data unavailable right now"
    )

    st.info(
        "The dashboard is working, but the live API returned no data."
    )

    st.stop()

# ======================================
# AGGREGATION
# ======================================
world = (
    df.groupby("country")["signal"]
    .sum()
    .reset_index()
)

# ======================================
# RISK SCORE
# ======================================
world["risk"] = (
    world["signal"]
    /
    world["signal"].max()
) * 100

# ======================================
# METRICS
# ======================================
st.subheader("📊 Global Intelligence Overview")

c1, c2, c3 = st.columns(3)

c1.metric(
    "Countries",
    len(world)
)

c2.metric(
    "Signals",
    len(df)
)

c3.metric(
    "Average Risk",
    round(
        world["risk"].mean(),
        2
    )
)

# ======================================
# GLOBAL MAP
# ======================================
st.subheader("🗺️ Global Risk Map")

fig = px.choropleth(
    world,
    locations="country",
    locationmode="country names",
    color="risk",
    color_continuous_scale="Reds",
    title="Global Health Risk Distribution"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# ======================================
# TABLE
# ======================================
st.subheader("📋 Intelligence Feed")

st.dataframe(
    df,
    use_container_width=True
)

# ======================================
# TREND ENGINE
# ======================================
st.subheader("📈 Global Trend")

avg = world["risk"].mean()

if avg > 60:

    st.error(
        "🚨 Elevated global health activity"
    )

elif avg > 40:

    st.warning(
        "🟡 Moderate global activity"
    )

else:

    st.success(
        "🟢 Stable global conditions"
    )

# ======================================
# TOP RISK COUNTRIES
# ======================================
st.subheader("🚨 Highest Activity Countries")

top = (
    world.sort_values(
        "risk",
        ascending=False
    )
    .head(10)
)

st.dataframe(
    top,
    use_container_width=True
)

# ======================================
# ARCHITECTURE
# ======================================
st.subheader("🧠 System Architecture")

st.code("""
[ GDELT Live API ]
          ↓
[ Streamlit Intelligence Layer ]
          ↓
[ Aggregation Engine ]
          ↓
[ Global Risk Scoring ]
          ↓
[ Interactive WHO Dashboard ]
""")

# ======================================
# FOOTER
# ======================================
st.caption(
    "WHO-style live intelligence dashboard (stable cloud version)"
)
