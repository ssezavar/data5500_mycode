# --------------------------------------------------------------------- #
# hw5_covid.py
# Sara Sezavar Dokhtfaroughi
# Web JSON API (COVID Tracking Project) - State/Territory analysis
# --------------------------------------------------------------------- #

import json
import time
import calendar
from datetime import datetime
import cloudscraper

# -----------------------------
# 1) Initial settings and keys
# -----------------------------

# URL parts
url1 = "https://api.covidtracking.com/v1/states/"
url2 = "/daily.json"

# important JSON keys
key_date = "date"               # YYYYMMDD (int)
key_inc = "positiveIncrease"    # daily confirmed cases increase

# state/Territory codes (55 s/t)
state_codes = [
    "al","ar","as","az","ca","co","ct","dc","de","fl","ga","gu","hi","ia","id",
    "il","in","ks","ky","la","ma","md","me","mi","mn","mo","mp","ms","mt","nc",
    "nd","ne","nh","nj","nm","nv","ny","oh","ok","or","pa","pr","ri","sc","sd",
    "tn","tx","ut","va","vi","vt","wa","wi","wv","wy"
]

# Cloudflare-aware HTTP client
scraper = cloudscraper.create_scraper()

# ---------------------------
# (2) Helper functions
# ---------------------------

def yyyymmdd_to_date(yyyymmdd_int):
    """Convert integer YYYYMMDD to a datetime.date object."""
    s = str(yyyymmdd_int)
    return datetime.strptime(s, "%Y%m%d").date()

def safe_inc(val):
    """
    Normalize positiveIncrease:
    - None -> 0
    - Negative values -> 0
    """
    if val is None:
        return 0
    try:
        v = int(val)
    except:
        return 0
    return v if v > 0 else 0

# ----------------------------
# 3) Processing a single state
# ----------------------------

def process_state(code):
    # Build URL
    url = url1 + code + url2

    # fetch the JSON data:
    resp = scraper.get(url)
    data = resp.json()  # list of daily records (dict)

    # Save raw JSON to <state>.json
    with open(f"{code}.json", "w", encoding="utf-8") as f:
        json.dump(data, f)

    # in case of no data, print empty stats
    if not data:
        print_block(code.upper(), None, None, None, None, None)
        return


    # normalize the rows: convert date and extract positiveIncrease
    rows = []
    for r in data:
        dte = yyyymmdd_to_date(r.get(key_date))
        inc = safe_inc(r.get(key_inc))
        rows.append({"date": dte, "inc": inc})

    # sorting by date (newest first)
    rows.sort(key=lambda x: x["date"], reverse=True)

    # (1) average daily increase
    incs = [x["inc"] for x in rows]
    avg_inc = (sum(incs) / len(incs)) if incs else 0

    # 2) date with highest new cases
    day_max = max(rows, key=lambda x: x["inc"]) if rows else None
    max_date = day_max["date"] if day_max else None
    max_val = day_max["inc"] if day_max else 0

    # 3) Most recent date with zero new cases
    last_zero = None
    for x in rows:
        if x["inc"] == 0:
            last_zero = x["date"]
            break

    # (4) monthly totals (find max and min month)
    monthly = {}  # (year, month) -> total cases
    for x in rows:
        key = (x["date"].year, x["date"].month)
        monthly[key] = monthly.get(key, 0) + x["inc"]

    if not monthly:
        print_block(code.upper(), avg_inc, (max_date, max_val), last_zero, None, None)
        return

    month_max = max(monthly.items(), key=lambda kv: kv[1])
    month_min = min(monthly.items(), key=lambda kv: kv[1])

    def fmt_month(ym, total):
        y, m = ym
        return f"{calendar.month_name[m]} {y}", total

    mmx_label, mmx_val = fmt_month(month_max[0], month_max[1])
    mmn_label, mmn_val = fmt_month(month_min[0], month_min[1])

    # print statistics for this state
    print_block(code.upper(), avg_inc, (max_date, max_val), last_zero,
                (mmx_label, mmx_val), (mmn_label, mmn_val))

def print_block(state_name, avg_inc, day_max_tuple, last_zero_date,
                month_max_tuple, month_min_tuple):
    """Prints the statistics block for one state."""
    print("\nCovid confirmed cases statistics")
    print("State name:", state_name)

    # average
    if avg_inc is None:
        print("Average number of new daily confirmed cases for the entire state dataset:", "None")
    else:
        print("Average number of new daily confirmed cases for the entire state dataset:", round(avg_inc, 2))

    # highest daily
    if day_max_tuple and day_max_tuple[0]:
        d, v = day_max_tuple
        print("Date with the highest new number of covid cases:", f"{d.isoformat()}  ({v})")
    else:
        print("Date with the highest new number of covid cases:", "None")

    # MOst recent zero day
    if last_zero_date:
        print("Most recent date with no new covid cases:", last_zero_date.isoformat())
    else:
        print("Most recent date with no new covid cases:", "None")

    # Highest month
    if month_max_tuple:
        label, total = month_max_tuple
        print("Month and Year, with the highest new number of covid cases:", f"{label}  ({total})")
    else:
        print("Month and Year, with the highest new number of covid cases:", "None")

    # Lowest month
    if month_min_tuple:
        label, total = month_min_tuple
        print("Month and Year, with the lowest new number of covid cases:", f"{label}  ({total})")
    else:
        print("Month and Year, with the lowest new number of covid cases:", "None")

# ------------------------
# (4) MAin execution:
# --------------------------

if __name__ == "__main__":
    for code in state_codes:
        try:
            process_state(code)
            time.sleep(0.3)  # avoid hammering the API
        except Exception as e:
            print("\nCovid confirmed cases statistics")
            print("State name:", code.upper())
            print("ERROR while processing state:", e)
