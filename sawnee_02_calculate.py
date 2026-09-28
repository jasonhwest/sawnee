#!/usr/bin/env python3

import csv

INPUT_FILE = "combined.csv"
OUTPUT_FILE = "combined-with-cost-per-usage.csv"

with open(INPUT_FILE, "r", newline="", encoding="utf-8-sig") as infile, \
     open(OUTPUT_FILE, "w", newline="", encoding="utf-8") as outfile:

    reader = csv.DictReader(infile)

    # Write manually so period remains quoted
    outfile.write('"period","usage","cost","cost_per_usage"\n')

    rows_written = 0

    for row in reader:
        period = row["period"]
        usage = float(row["usage"])
        cost = float(row["cost"])

        # cents per therm
        cost_per_usage = (cost / usage) * 100

        outfile.write(
            f'"{period}",{usage},{cost},{cost_per_usage:.2f}\n'
        )

        rows_written += 1

print(f"Done. Wrote {rows_written} records to {OUTPUT_FILE}")