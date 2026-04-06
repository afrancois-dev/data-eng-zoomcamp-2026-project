"""@bruin

name: raw.bouts
connection: db
tags:
  - raw
  - bouts

materialization:
  type: table
  strategy: create+replace

depends:
  - raw.fighters
  - raw.events

secrets:
  - key: db
    inject_as: db

columns:
  - name: event_url
    type: VARCHAR
  - name: bout_url
    type: VARCHAR
  - name: fighter_1
    type: VARCHAR
  - name: fighter_2
    type: VARCHAR
  - name: winner
    type: VARCHAR
  - name: weight_class
    type: VARCHAR
  - name: method
    type: VARCHAR
  - name: round
    type: VARCHAR
  - name: time
    type: VARCHAR
  - name: date
    type: DATE

@bruin"""

# NB: this DAG may take up to 25 min for the first load

import requests
from bs4 import BeautifulSoup
import time
import random
from bruin import query
import logging
import os
from datetime import datetime, timezone

# built-in variables
start_date_env = os.environ.get("BRUIN_START_DATE")
end_date_env = os.environ.get("BRUIN_END_DATE")
full_refresh = os.environ.get("BRUIN_FULL_REFRESH") == "1"


def scrape_bouts_from_events(events_df):
    for _, event in events_df.iterrows():
        event_url = event["url"]
        event_date = event["date"]

        try:
            response = requests.get(event_url, timeout=15)
            response.raise_for_status()
            rows = BeautifulSoup(response.text, "html.parser").select("tr.b-fight-details__table-row")

            for row in rows:
                cells = row.select("td")
                if len(cells) < 10:
                    continue

                fighters = [f.text.strip() for f in cells[1].select("a.b-link_style_black")]
                if len(fighters) < 2:
                    continue

                # winner detection -> gérer les draw
                win_tags = cells[0].select("i.b-flag__text")
                winner = None
                if win_tags:
                    if win_tags[0].text.strip().lower() == "win":
                        winner = fighters[0]
                    elif len(win_tags) > 1 and win_tags[1].text.strip().lower() == "win":
                        winner = fighters[1]

                yield {
                    "event_url": event_url,
                    "bout_url": row.get("data-link"),
                    "fighter_1": fighters[0],
                    "fighter_2": fighters[1],
                    "winner": winner,
                    "weight_class": cells[6].text.strip(),
                    "method": " ".join(cells[7].get_text().split()),
                    "round": cells[8].text.strip(),
                    "time": cells[9].text.strip(),
                    "date": event_date,
                }

            time.sleep(1 + random.uniform(0, 0.15))
        except Exception as e:
            logging.error(f"Error scraping event {event_url}: {e}")


def materialize():
    try:
        query_str = "SELECT url, date FROM raw.events"
        conditions = []

        if not full_refresh:
            # by default, bruin runs for D-1 if no dates are provided.
            start_date = start_date_env if not start_date_env else datetime.now(timezone.utc).strftime("%Y-%m-%d")
            conditions.append(f"date >= '{start_date}'")

            if end_date_env:
                conditions.append(f"date <= '{end_date_env}'")

            query_str += f" WHERE {' AND '.join(conditions)}"
            logging.info(f"Incremental run: filtering events from {start_date} to {end_date_env or 'now'}.")
        else:
            logging.info("Full refresh: scraping all historically available events.")

        raw_events = query(query_str)
        if raw_events is None or "url" not in raw_events.columns:
            logging.warning("No event URLs found to scrape.")
            return

        yield from scrape_bouts_from_events(raw_events)

    except Exception as e:
        logging.error(f"Error during bout scraping: {e}")
