"""@bruin

name: raw.events
connection: db
tags:
  - raw
  - events

materialization:
  type: table
  strategy: create+replace

secrets:
  - key: db
    inject_as: db

columns:
  - name: url
    type: VARCHAR
    primary_key: true
  - name: name
    type: VARCHAR
  - name: date
    type: DATE
  - name: location
    type: VARCHAR

@bruin"""

import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
import logging


def scrape_events():
    response = requests.get("http://ufcstats.com/statistics/events/completed?page=all", timeout=15)
    response.raise_for_status()

    rows = BeautifulSoup(response.text, "html.parser").select("tr.b-statistics__table-row")
    for i, row in enumerate(rows, 1):
        link = row.select_one("a.b-link.b-link_style_black")
        cells = row.select("td")

        if not link:
            logging.debug(f"Skipping row {i}: link not found")
        elif not cells or len(cells) < 2:
            logging.debug(f"Skipping row {i}: insufficient cells")
        else:
            try:
                date_span = cells[0].select_one("span.b-statistics__date")
                date_str = date_span.text.strip() if date_span else ""
                event_date = datetime.strptime(date_str, "%B %d, %Y").date()
            except (AttributeError, ValueError):
                event_date = None

            if i % 50 == 0 or i == len(rows):
                logging.info(f"Progress: {i / len(rows):.1%} ({i}/{len(rows)} events processed)")

            yield {
                "name": link.text.strip(),
                "url": link.get("href"),
                "date": event_date,
                "location": cells[1].text.strip(),
            }


def materialize() -> pd.DataFrame:
    try:
        return pd.DataFrame(scrape_events())
    except Exception as e:
        logging.error(f"Error during event scraping: {e}")
        return pd.DataFrame()
