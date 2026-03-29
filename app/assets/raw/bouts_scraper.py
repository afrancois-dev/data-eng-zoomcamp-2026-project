"""@bruin

name: raw.bouts
connection: duckdb-dev

materialization:
  type: table
  strategy: create+replace

depends:
  - raw.fighters
  - raw.events

columns:
  - name: event_url
    type: string
  - name: bout_url
    type: string
  - name: fighter_1
    type: string
  - name: fighter_2
    type: string
  - name: winner
    type: string
  - name: weight_class
    type: string
  - name: method
    type: string
  - name: round
    type: string
  - name: time
    type: string

@bruin"""

import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import random
from bruin import query


def scrape_bouts_from_event(event_url):
    response = requests.get(event_url, timeout=15)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")

    rows = soup.select("tr.b-fight-details__table-row")
    bouts = []

    for row in rows:
        cells = row.select("td")
        if len(cells) < 10:
            continue

        fighters = [f.text.strip() for f in cells[1].select("a.b-link_style_black")]
        if len(fighters) < 2:
            continue

        weight_class = cells[6].text.strip()
        method = " ".join(cells[7].get_text().split())
        round_num = cells[8].text.strip()
        time_val = cells[9].text.strip()
        bout_url = row.get("data-link")

        # winner detection -> gérer les draw
        win_tags = cells[0].select("i.b-flag__text")
        winner = None
        if win_tags:
            first_tag = win_tags[0].text.strip().lower()
            if first_tag == "win":
                winner = fighters[0]
            elif len(win_tags) > 1 and win_tags[1].text.strip().lower() == "win":
                winner = fighters[1]

        bouts.append(
            {
                "event_url": event_url,
                "bout_url": bout_url,
                "fighter_1": fighters[0],
                "fighter_2": fighters[1],
                "winner": winner,
                "weight_class": weight_class,
                "method": method,
                "round": round_num,
                "time": time_val,
            }
        )

    return bouts


def materialize() -> pd.DataFrame:
    all_bouts = []
    try:
        raw_events = query("SELECT url FROM raw.events")
        if raw_events is None or "url" not in raw_events.columns:
            return pd.DataFrame()

        event_urls = raw_events["url"].tolist()
        for url in event_urls:
            try:
                bouts = scrape_bouts_from_event(url)
                all_bouts.extend(bouts)
                # wait 1 sec + random between 0 and 300ms to do not disturb the service
                time.sleep(1 + random.uniform(0, 0.3))
            except Exception as e:
                print(f"Error scraping event {url}: {e}")

        return pd.DataFrame(all_bouts)
    except Exception as e:
        print(f"Error during bout scraping: {e}")
        return pd.DataFrame()
