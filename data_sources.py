"""
Nora Global Health Intelligence
Real public-health data ingestion layer.

This module provides a consistent structure for health events so the
risk engine, database, API, and dashboard can use the same data format.
"""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

import requests


WHO_GHO_API = "https://ghoapi.azureedge.net/api"


def utc_now() -> str:
    """Return the current UTC time in ISO-8601 format."""
    return datetime.now(timezone.utc).isoformat()


def normalize_event(
    *,
    source: str,
    title: str,
    country: str | None = None,
    country_code: str | None = None,
    event_type: str = "health_event",
    description: str | None = None,
    cases: int | None = None,
    deaths: int | None = None,
    latitude: float | None = None,
    longitude: float | None = None,
    url: str | None = None,
    published_at: str | None = None,
) -> dict[str, Any]:
    """
    Convert information from different sources into one standard event format.
    """

    return {
        "source": source,
        "title": title,
        "country": country,
        "country_code": country_code,
        "event_type": event_type,
        "description": description,
        "cases": cases,
        "deaths": deaths,
        "latitude": latitude,
        "longitude": longitude,
        "url": url,
        "published_at": published_at or utc_now(),
        "ingested_at": utc_now(),
    }


def fetch_who_indicator(
    indicator: str,
    top: int = 100,
    timeout: int = 30,
) -> list[dict[str, Any]]:
    """
    Fetch indicator data from the WHO GHO OData API.

    Example:
        fetch_who_indicator("WHOSIS_000001")
    """

    url = f"{WHO_GHO_API}/{indicator}"

    try:
        response = requests.get(
            url,
            params={"$top": top},
            timeout=timeout,
        )

        response.raise_for_status()

        data = response.json()

        return data.get("value", [])

    except requests.RequestException as exc:
        print(f"WHO API request failed: {exc}")
        return []

    except ValueError as exc:
        print(f"WHO API returned invalid JSON: {exc}")
        return []


def get_who_health_data(
    indicator: str,
    top: int = 100,
) -> list[dict[str, Any]]:
    """
    Retrieve WHO data and attach ingestion metadata.
    """

    rows = fetch_who_indicator(indicator, top=top)

    results = []

    for row in rows:
        results.append(
            {
                "source": "WHO",
                "indicator": indicator,
                "country_code": row.get("SpatialDim"),
                "time": row.get("TimeDim"),
                "value": row.get("NumericValue"),
                "value_type": row.get("Value"),
                "raw": row,
                "ingested_at": utc_now(),
            }
        )

    return results


def health_data_status() -> dict[str, Any]:
    """
    Check whether the WHO data service is reachable.
    """

    try:
        response = requests.get(
            WHO_GHO_API,
            timeout=10,
        )

        return {
            "source": "WHO GHO API",
            "status": "online" if response.ok else "error",
            "http_status": response.status_code,
            "checked_at": utc_now(),
        }

    except requests.RequestException as exc:
        return {
            "source": "WHO GHO API",
            "status": "offline",
            "error": str(exc),
            "checked_at": utc_now(),
        }


if __name__ == "__main__":
    print("🌍 Nora Global Health Intelligence")
    print("🔎 Checking WHO data service...")

    status = health_data_status()

    print(status)
