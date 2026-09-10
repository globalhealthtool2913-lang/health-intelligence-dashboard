import streamlit as st
import pandas as pd

from data_sources import (
    health_data_status,
    get_who_health_data,
)

# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Nora Global Health Intelligence",
    page_icon="🌍",
    layout="wide",
)

# ============================================================
# HEADER
# ============================================================

st.title("🌍 Nora Global Health Intelligence")
st.caption(
    "Public-health intelligence dashboard powered by real WHO data"
)

# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.header("⚙️ Intelligence Controls")

indicator = st.sidebar.text_input(
    "WHO Indicator",
    value="WHOSIS_000001",
)

records = st.sidebar.slider(
    "Number of records",
    min_value=5,
    max_value=100,
    value=20,
)

# ============================================================
# WHO CONNECTION STATUS
# ============================================================

status = health_data_status()

if status.get("status") == "online":
    st.success("🟢 WHO data connection is online")
else:
    st.error("🔴 WHO data connection is unavailable")

# ============================================================
# LOAD WHO DATA
# ============================================================

st.header("📊 WHO Health Intelligence")

if st.button("🔄 Fetch Latest WHO Data", type="primary"):

    with st.spinner("Connecting to WHO and retrieving data..."):

        data = get_who_health_data(
            indicator=indicator,
            top=records,
        )

    if data:

        st.session_state["who_data"] = data

        st.success(
            f"✅ Retrieved {len(data)} WHO records"
        )

    else:

        st.warning(
            "No WHO records were returned. "
            "Check the indicator or WHO connection."
        )

# ============================================================
# DISPLAY DATA
# ============================================================

if "who_data" in st.session_state:

    data = st.session_state["who_data"]

    df = pd.DataFrame(data)

    st.subheader("🌍 WHO Data")

    display_columns = [
        column
        for column in [
            "country_code",
            "time",
            "value",
            "value_type",
            "indicator",
        ]
        if column in df.columns
    ]

    if display_columns:

        st.dataframe(
            df[display_columns],
            use_container_width=True,
        )

    else:

        st.dataframe(
            df,
            use_container_width=True,
        )

    # ========================================================
    # SUMMARY
    # ========================================================

    st.subheader("📈 Intelligence Summary")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "WHO Records",
            len(df),
        )

    with col2:

        if "country_code" in df.columns:
            countries = df["country_code"].nunique()
        else:
            countries = 0

        st.metric(
            "Countries",
            countries,
        )

    with col3:

        if "value" in df.columns:

            numeric_values = pd.to_numeric(
                df["value"],
                errors="coerce",
            )

            valid_values = numeric_values.dropna()

            if len(valid_values) > 0:
                average = valid_values.mean()
                st.metric(
                    "Average Value",
                    f"{average:,.2f}",
                )
            else:
                st.metric(
                    "Average Value",
                    "N/A",
                )

        else:

            st.metric(
                "Average Value",
                "N/A",
            )

else:

    st.info(
        "👆 Click **Fetch Latest WHO Data** to load real WHO records."
    )

# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "Nora Global Health Intelligence • "
    "Public-health data intelligence platform"
)
