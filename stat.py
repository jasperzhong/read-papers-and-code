import datetime
import json
import sys

import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import pandas as pd
import requests
from requests.exceptions import HTTPError

closed_time = []
page = 1
while True:
    try:
        response = requests.get("https://api.github.com/repos/vycezhong/read-papers/issues",
                                params={"state": "closed",
                                        "per_page": "100", "page": page},
                                headers={"Accept": "application/vnd.github.v3+json"})
        response.raise_for_status()
    except HTTPError as http_error:
        print(f"HTTP error occurred: {http_error}")
        sys.exit(1)
    except Exception as err:
        print(f"Other error occurred: {err}")
        sys.exit(1)
    else:
        print("Success!")

    json_response = response.json()
    if not json_response:
        break
    closed_time.extend([item["closed_at"] for item in json_response])
    page += 1

print(len(closed_time))
df = pd.DataFrame(index=pd.to_datetime(closed_time))
stat = df.groupby(pd.Grouper(freq='M')).size()
ticklabels = [item.strftime("%Y-%m") for item in stat.index]
ax = stat.plot.bar(figsize=(15, 10))
ax.xaxis.set_major_formatter(ticker.FixedFormatter(ticklabels))
ax.figure.autofmt_xdate(rotation=30, ha='center')
ax.set_xlabel("Date")
ax.set_ylabel("# Papers")
ax.set_title("Statistics of Reading Papers")
plt.savefig("stat.png")
