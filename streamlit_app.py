import streamlit as st
import pandas as pd
import plotly.express as px
import requests
import feedparser
import random
import time
from datetime import datetime

# =========================================
# PAGE CONFIG
# =========================================

st.set_page_config(
    page_title="WHO AI Enterprise Intelligence System",
    page_icon="🌍",
    layout="wide"
)

# =========================================
# ENTERPRISE EVENT BUS
# =========================================

class EventBus:
    def __init__(self):
        self.events = []

    def publish(self, event):
        self.events.append(event)

    def consume(self):
        return self.events[-100:]

bus = EventBus()

# =========================================
# WHO RSS SERVICE
# =========================================

WHO_FEEDS = [
    "https://www.who.int/feeds/entity/csr/don/en/rss.xml"
]

def fetch_who_data():

    results = []

    try:

        for url in WHO_FEEDS:

            feed = feedparser.parse(url)

            for entry in feed.entries[:5]:

                results.append({
                    "source": "WHO",
                    "title": entry.title,
                    "summary": entry.summary,
                    "country": random.choice([
                        "Ethiopia",
                        "Kenya",
                        "India",
                        "Brazil",
                        "USA"
                    ]),
                    "cases":
