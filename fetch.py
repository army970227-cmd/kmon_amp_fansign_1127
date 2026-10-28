import requests
import csv
import os
from datetime import datetime, timezone, timedelta

PRODUCT_HANDLE = "應募-261127-axmxp-2nd-mini-album-hello-axmxp-專輯發行紀念簽名會-in-taipei"
URL = f"https://www.kmonstar.com.tw/products/{PRODUCT_HANDLE}.json"
CSV_PATH = "kmonstar_sales.csv"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "application/json"
}

def main():
    tw = timezone(timedelta(hours=8))
    now = datetime.now(tw).strftime("%Y-%m-%d %H:%M:%S")
    
    try:
        r = requests.get(URL, headers=HEADERS, timeout=15)
        r.raise_for_status()
        data = r.json()
        
        total_sold = data.get("total_sold", 0)
        
        prev_sold = None
        if os.path.exists(CSV_PATH):
            with open(CSV_PATH, "r", encoding="utf-8-sig") as f:
                lines = f.readlines()
                if len(lines) > 1:
                    last_line = lines[-1].strip().split(",")
                    if len(last_line) >= 3:
                        prev_sold = int(last_line[2])
                        
        delta = 0
        if prev_sold is not None and total_sold > prev_sold:
            delta = total_sold - prev_sold

        print(f"Success: 累積銷量 {total_sold} | 增加: {delta}")

        new_file = not os.path.exists(CSV_PATH)
        with open(CSV_PATH, "a", newline="", encoding="utf-8-sig") as f:
            w = csv.DictWriter(f, fieldnames=["time", "member", "total_sold", "stock", "delta"])
            if new_file:
                w.writeheader()
            w.writerow({
                "time": now,
                "member": "AxMxP 簽名會",
                "total_sold": total_sold,
                "stock": 0,
                "delta": delta
            })

    except Exception as e:
        print(f"[ERROR]: {e}")

if __name__ == "__main__":
    main()
