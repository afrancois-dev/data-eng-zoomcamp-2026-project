"""@bruin

name: raw.fighters
connection: duckdb-dev
tags:
  - raw
  - fighters

materialization:
  type: table
  strategy: create+replace

secrets:
  - key: duckdb-dev
    inject_as: duckdb-dev

columns:
  - name: url
    type: VARCHAR
    primary_key: true
  - name: first_name
    type: VARCHAR
  - name: last_name
    type: VARCHAR
  - name: nick_name
    type: VARCHAR
  - name: height
    type: VARCHAR
  - name: weight
    type: VARCHAR
  - name: wins
    type: BIGINT

@bruin"""

import requests
from bs4 import BeautifulSoup
import pandas as pd
import string
import logging


def scrape_fighters(char: str):
    response = requests.get(f"http://ufcstats.com/statistics/fighters?char={char}&page=all", timeout=10)
    response.raise_for_status()
    rows = BeautifulSoup(response.text, "html.parser").select("tr.b-statistics__table-row")[1:]

    for row in rows:
        cells = row.select("td")
        if len(cells) < 8:
            logging.debug(f"Skipping row with insufficient cells: {len(cells)}")
        else:
            yield {
                "url": (cells[0].select_one("a") or {}).get("href"),
                "first_name": cells[0].text.strip(),
                "last_name": cells[1].text.strip(),
                "nick_name": cells[2].text.strip(),
                "height": cells[3].text.strip(),
                "weight": cells[4].text.strip(),
                "wins": int(cells[7].text.strip()) if cells[7].text.strip().isdigit() else None,
            }


def materialize() -> pd.DataFrame:
    all_fighters, alphabet = [], string.ascii_lowercase
    for i, char in enumerate(alphabet, 1):
        try:
            all_fighters.extend(list(scrape_fighters(char)))
            logging.info(f"Progress: {i / len(alphabet):.1%} ({char})")
        except Exception as e:
            logging.error(f"Error scraping {char}: {e}")
    return pd.DataFrame(all_fighters)
