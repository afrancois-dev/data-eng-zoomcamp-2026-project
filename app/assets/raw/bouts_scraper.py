"""@bruin

name: raw.bouts
connection: duckdb-dev
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
  - key: duckdb-dev
    inject_as: duckdb-dev

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

@bruin"""

import requests
from bs4 import BeautifulSoup
import time
import random
from bruin import query
import logging


def scrape_bouts_from_event(event_url):
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
        }


def materialize():
    try:
        raw_events = query("SELECT url FROM raw.events")
        if raw_events is None or "url" not in raw_events.columns:
            return

        urls = raw_events["url"].tolist()
        for i, url in enumerate(urls, 1):
            try:
                yield from scrape_bouts_from_event(url)
                if i % 500 == 0 or i == len(urls):
                    logging.info(f"Progress: {i / len(urls):.1%} ({i}/{len(urls)} events processed)")
                time.sleep(1 + random.uniform(0, 0.3))
            except Exception as e:
                logging.error(f"Error scraping event {url}: {e}")
    except Exception as e:
        logging.error(f"Error during bout scraping: {e}")
