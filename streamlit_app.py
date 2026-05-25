import streamlit as st
import websocket
import json
import threading
from collections import deque

# =========================
# CONFIG
# =========================

st.set_page_config(
    page_title="WHO AI Real-Time WebSocket System",
    page_icon="🌍",
    layout="wide"
)

st.title("🌍 WHO AI Real-Time Intelligence System (WebSocket)")

st.caption("Live global outbreak monitoring dashboard")

# =========================
# LIVE DATA STORAGE (SAFE BUFFER)
# =========================

if "live_data" not in st.session_state:
    st.session_state.live_data = deque(maxlen=15)

container = st.empty()

# =========================
# WEBSOCKET CALLBACK
# =========================

def on_message(ws, message):

    data = json.loads(message)

    st.session_state.live_data.appendleft(data)

    with container.container():

        st.subheader("🔄 LIVE GLOBAL STREAM")

        for d in st.session_state.live_data:

            st.write(
                f"{d.get('country')} | "
                f"{d.get('cases')} | "
                f"{d.get('deaths')} | "
                f"{d.get('risk')} | "
                f"{d.get('time')}"
            )

# =========================
# WEBSOCKET RUNNER
# =========================

def run_ws():

    ws = websocket.WebSocketApp(
        "ws://localhost:8000/ws/live",
        on_message=on_message
    )

    ws.run_forever()

# =========================
# START BACKGROUND THREAD
# =========================

threading.Thread(target=run_ws, daemon=True).start()

# =========================
# STATUS PANEL
# =========================

st.success("🌍 WebSocket Connection Active")

st.info("Waiting for real-time WHO + GDELT outbreak stream...")
