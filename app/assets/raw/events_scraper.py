"""@bruin

name: raw.events
connection: duckdb-dev

materialization:
  type: table
  strategy: create+replace

columns:
  - name: url
    type: string
    primary_key: true
  - name: name
    type: string
  - name: date
    type: date
  - name: location
    type: string

@bruin"""

import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime


def scrape_events():
    url = "http://ufcstats.com/statistics/events/completed?page=all"
    response = requests.get(url, timeout=15)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")
    # the events are in a table with class b-statistics__table-events
    rows = soup.select("tr.b-statistics__table-row")

    data = []
    for row in rows:
        # skip header rows or rows that don't have the expected link
        link = row.select_one("a.b-link.b-link_style_black")
        if not link:
            continue

        cells = row.select("td")
        if len(cells) < 2:
            continue
        try:
            date_span = cells[0].select_one("span.b-statistics__date")
            if date_span:
                event_date = datetime.strptime(date_span.text.strip(), "%B %d, %Y").date()
        except ValueError:
            event_date = None

        data.append(
            {
                "name": link.text.strip(),
                "url": link.get("href"),
                "date": event_date,
                "location": cells[1].text.strip(),
            }
        )
    return data


def materialize() -> pd.DataFrame:
    try:
        events = scrape_events()
        return pd.DataFrame(events)
    except Exception as e:
        print(f"Error during event scraping: {e}")
        return pd.DataFrame(columns=["name", "url", "date", "location"])
