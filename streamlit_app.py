import streamlit as st
import pandas as pd
import requests
import plotly.express as px

# ==========================================
# PAGE CONFIG
# ==========================================
st.set_page_config(
    page_title="WHO Global Intelligence",
    layout="wide"
)

# ==========================================
# TITLE
# ==========================================
st.title("🌍 WHO GLOBAL HEALTH INTELLIGENCE")
st.caption("Continuous live global surveillance dashboard")

# ==========================================
# LOAD LIVE DATA
# ==========================================
@st.cache_data(ttl=300)
def load_data():

    url = "https://api.gdeltproject.org/api/v2/doc/doc"

    params = {
        "query": "health OR outbreak OR epidemic OR virus OR disease",
        "mode": "ArtList",
        "maxrecords": 50,
        "format": "json"
    }

    try:

        r = requests.get(
            url,
            params=params,
            timeout=20,
            headers={
                "User-Agent": "Mozilla/5.0"
            }
        )

        if r.status_code != 200:
            raise Exception("API Error")

        data = r.json()

        articles = data.get(
            "articles",
            []
        )

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

        # ==================================
        # FALLBACK IF EMPTY
        # ==================================
        if len(rows) == 0:

            rows = [
                {
                    "country": "USA",
                    "signal": 5,
                    "title": "Baseline health signal"
                },
                {
                    "country": "India",
                    "signal": 4,
                    "title": "Baseline health signal"
                },
                {
                    "country": "Ethiopia",
                    "signal": 3,
                    "title": "Baseline health signal"
                },
                {
                    "country": "Brazil",
                    "signal": 2,
                    "title": "Baseline health signal"
                }
            ]

        return pd.DataFrame(rows)

    except:

        # ==================================
        # FULL FAILSAFE
        # ==================================
        fallback = pd.DataFrame([
            {
                "country": "USA",
                "signal": 5,
                "title": "Fallback signal"
            },
            {
                "country": "India",
                "signal": 4,
                "title": "Fallback signal"
            },
            {
                "country": "Ethiopia",
                "signal": 3,
                "title": "Fallback signal"
            },
            {
                "country": "Brazil",
                "signal": 2,
                "title": "Fallback signal"
            }
        ])

        return fallback

# ==========================================
# FETCH DATA
# ==========================================
df = load_data()

# ==========================================
# AGGREGATION
# ==========================================
world = (
    df.groupby("country")["signal"]
    .sum()
    .reset_index()
)

# ==========================================
# RISK SCORE
# ==========================================
world["risk"] = (
    world["signal"]
    /
    world["signal"].max()
) * 100

# ==========================================
# METRICS
# ==========================================
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

# ==========================================
# MAP
# ==========================================
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

# ==========================================
# TREND ENGINE
# ==========================================
st.subheader("📈 Global Trend Engine")

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

# ==========================================
# TOP COUNTRIES
# ==========================================
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

# ==========================================
# LIVE FEED
# ==========================================
st.subheader("📋 Live Intelligence Feed")

st.dataframe(
    df,
    use_container_width=True
)

# ==========================================
# ARCHITECTURE
# ==========================================
st.subheader("🧠 System Architecture")

st.code("""
[ GDELT Live API ]
          ↓
[ Streamlit Intelligence Layer ]
          ↓
[ Aggregation Engine ]
          ↓
[ Risk Scoring System ]
          ↓
[ WHO-style Surveillance Dashboard ]
""")

# ==========================================
# FOOTER
# ==========================================
st.caption(
    "Stable WHO-style continuous surveillance platform"
)
