"""@bruin

name: raw.fighters
type: duckdb.sql

materialization:
  type: table
  strategy: create+replace

columns:
  - name: first_name
    type: string
  - name: last_name
    type: string
  - name: wins
    type: integer

@bruin"""

import requests
from bs4 import BeautifulSoup
import pandas as pd
import string


def scrape_fighters(char: str):
    url = f"http://ufcstats.com/statistics/fighters?char={char}&page=all"
    response = requests.get(url, timeout=10)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")
    rows = soup.select("tr.b-statistics__table-row")[1:]

    data = []
    for row in rows:
        cells = row.select("td")
        if len(cells) < 8:
            continue

        data.append(
            {
                "first_name": cells[0].text.strip(),
                "last_name": cells[1].text.strip(),
                "nick_name": cells[2].text.strip(),
                "height": cells[3].text.strip(),
                "weight": cells[4].text.strip(),
                "wins": int(cells[7].text.strip()) if cells[7].text.strip().isdigit() else 0,
            }
        )
    return data


def materialize() -> pd.DataFrame:
    all_fighters = []

    for char in string.ascii_lowercase[0]:
        try:
            fighters = scrape_fighters(char)
            all_fighters.extend(fighters)
        except Exception as e:
            print(f"Error scraping {char}: {e}")

    return pd.DataFrame(all_fighters)
