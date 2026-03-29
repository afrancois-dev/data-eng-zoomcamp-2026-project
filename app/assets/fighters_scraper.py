"""@bruin

name: mma.fighters_scraper
connection: duckdb-default

materialization:
  type: table
  strategy: create+replace
image: python:3.13-slim

columns:
  - name: FirstName
    type: string
  - name: LastName
    type: string
  - name: Wins
    type: integer

@bruin"""

import requests
from bs4 import BeautifulSoup
import pandas as pd
import string


def scrape_fighters(char):
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
                "FirstName": cells[0].text.strip(),
                "LastName": cells[1].text.strip(),
                "Nickname": cells[2].text.strip(),
                "Height": cells[3].text.strip(),
                "Weight": cells[4].text.strip(),
                "Wins": int(cells[7].text.strip()) if cells[7].text.strip().isdigit() else 0,
            }
        )
    return data


def materialize():
    all_fighters = []

    for char in string.ascii_lowercase:
        try:
            fighters = scrape_fighters(char)
            all_fighters.extend(fighters)
        except Exception as e:
            print(f"Error scraping {char}: {e}")

    return pd.DataFrame(all_fighters)
