#!/usr/bin/env python3

import csv
import glob
import os

INPUT_GLOB = "*.csv"
OUTPUT_FILE = "combined.csv"

HEADER_PREFIX = "Energy consumption time period"

rows_written = 0

with open(OUTPUT_FILE, "w", newline="", encoding="utf-8") as outfile:
    # Write header explicitly to control quoting
    outfile.write('"period","usage","cost"\n')

    for filename in sorted(glob.glob(INPUT_GLOB)):
        # Don't accidentally process our output from a previous run
        if os.path.basename(filename) == OUTPUT_FILE:
            continue

        print(f"Processing: {filename}")

        with open(filename, "r", newline="", encoding="utf-8-sig") as infile:
            reader = csv.reader(infile)

            expect_data_row = False

            for row in reader:
                if not row:
                    continue

                row = [field.strip() for field in row]

                if expect_data_row:
                    if len(row) >= 3:
                        period = row[0]

                        # Convert "1,995.000" -> 1995
                        usage = int(float(row[1].replace(",", "")))

                        # Convert cost to a number as well
                        cost = float(row[2])

                        # Period quoted; numeric fields unquoted
                        outfile.write(
                            f'"{period}",{usage},{cost}\n'
                        )

                        rows_written += 1

                    expect_data_row = False
                    continue

                if row[0].startswith(HEADER_PREFIX):
                    expect_data_row = True

print(f"\nDone. Wrote {rows_written} records to {OUTPUT_FILE}")
