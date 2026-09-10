```python
"""
Nora Global Health Intelligence
Real public-health data ingestion layer.

WHO GHO OData API
https://ghoapi.azureedge.net/api
"""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

import requests


# ============================================================
# CONFIGURATION
# ============================================================

WHO_GHO_API = "https://ghoapi.azureedge.net/api"

DEFAULT_TIMEOUT = 30


# ============================================================
# TIME
# ============================================================

def utc_now() -> str:
    """Return the current UTC time in ISO-8601 format."""
    return datetime.now(timezone.utc).isoformat()


# ============================================================
# EVENT NORMALIZATION
# ============================================================

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
    Convert information from different public-health sources
    into one standard Nora event format.
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


# ============================================================
# WHO GHO API
# ============================================================

def fetch_who_indicator(
    indicator: str,
    top: int = 100,
    timeout: int = DEFAULT_TIMEOUT,
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
            headers={
                "Accept": "application/json",
                "User-Agent": "Nora-Global-Health-Intelligence/1.0",
            },
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


# ============================================================
# WHO HEALTH DATA
# ============================================================

def get_who_health_data(
    indicator: str,
    top: int = 100,
) -> list[dict[str, Any]]:
    """
    Retrieve WHO indicator data and attach Nora metadata.
    """

    rows = fetch_who_indicator(
        indicator,
        top=top,
    )

    results: list[dict[str, Any]] = []

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


# ============================================================
# WHO INDICATOR LIST
# ============================================================

def get_who_indicators(
    top: int = 100,
    timeout: int = DEFAULT_TIMEOUT,
) -> list[dict[str, Any]]:
    """
    Retrieve available indicators from the WHO GHO API.
    """

    url = f"{WHO_GHO_API}/Indicator"

    try:
        response = requests.get(
            url,
            params={"$top": top},
            timeout=timeout,
            headers={
                "Accept": "application/json",
                "User-Agent": "Nora-Global-Health-Intelligence/1.0",
            },
        )

        response.raise_for_status()

        data = response.json()

        return data.get("value", [])

    except requests.RequestException as exc:
        print(f"WHO indicator request failed: {exc}")
        return []

    except ValueError as exc:
        print(f"WHO indicator API returned invalid JSON: {exc}")
        return []


# ============================================================
# WHO COUNTRY LIST
# ============================================================

def get_who_countries(
    timeout: int = DEFAULT_TIMEOUT,
) -> list[dict[str, Any]]:
    """
    Retrieve country dimension values from WHO.
    """

    url = f"{WHO_GHO_API}/DIMENSION/COUNTRY/DimensionValues"

    try:
        response = requests.get(
            url,
            timeout=timeout,
            headers={
                "Accept": "application/json",
                "User-Agent": "Nora-Global-Health-Intelligence/1.0",
            },
        )

        response.raise_for_status()

        data = response.json()

        return data.get("value", [])

    except requests.RequestException as exc:
        print(f"WHO country request failed: {exc}")
        return []

    except ValueError as exc:
        print(f"WHO country API returned invalid JSON: {exc}")
        return []


# ============================================================
# SERVICE STATUS
# ============================================================

def health_data_status() -> dict[str, Any]:
    """
    Check whether the WHO GHO API is reachable.
    """

    url = f"{WHO_GHO_API}/Indicator"

    try:
        response = requests.get(
            url,
            params={"$top": 1},
            timeout=10,
            headers={
                "Accept": "application/json",
                "User-Agent": "Nora-Global-Health-Intelligence/1.0",
            },
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


# ============================================================
# SIMPLE TEST
# ============================================================

if __name__ == "__main__":
    print("🌍 Nora Global Health Intelligence")
    print("🔎 Checking WHO GHO API...")

    status = health_data_status()

    print("\nWHO STATUS:")
    print(status)

    if status["status"] == "online":
        print("\n✅ WHO API is reachable.")
        print("📊 Loading a sample indicator...")

        sample = get_who_health_data(
            "WHOSIS_000001",
            top=5,
        )

        print(f"Received {len(sample)} records.")

        for record in sample:
            print(record)
    else:
        print("\n❌ WHO API could not be reached.")
```
