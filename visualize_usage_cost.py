#!/usr/bin/env python3

# brew install python-matplotlib

import csv
from datetime import datetime
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

INPUT_FILE = "combined-with-cost-per-usage.csv"
OUTPUT_FILE = "usage-cost-history.png"

periods = []

with open(INPUT_FILE, "r", newline="", encoding="utf-8-sig") as infile:
    reader = csv.DictReader(infile)

    for row in reader:
        # Example period:
        # 2014-07-03 00:00 to 2014-07-28 00:00
        start_string, end_string = row["period"].split(" to ")

        start = datetime.strptime(start_string, "%Y-%m-%d %H:%M")
        end = datetime.strptime(end_string, "%Y-%m-%d %H:%M")

        usage = float(row["usage"])
        cost_per_usage = float(row["cost_per_usage"])

        periods.append({
            "start": start,
            "end": end,
            "usage": usage,
            "cost_per_usage": cost_per_usage,
        })

# Sort chronologically
periods.sort(key=lambda x: x["start"])

# Prepare plotting data
starts = [p["start"] for p in periods]
ends = [p["end"] for p in periods]
usage = [p["usage"] for p in periods]
cost_per_usage = [p["cost_per_usage"] for p in periods]

# Calculate the midpoint of each billing period for the line
midpoints = [
    p["start"] + (p["end"] - p["start"]) / 2
    for p in periods
]

# Matplotlib bar widths are measured in days for date axes
widths = [
    (p["end"] - p["start"]).total_seconds() / 86400
    for p in periods
]

fig, ax1 = plt.subplots(figsize=(16, 8))

# ------------------------------------------------------------
# Usage
# Each bar begins on the actual billing-period start date and
# spans the full billing period.
# ------------------------------------------------------------

bars = ax1.bar(
    starts,
    usage,
    width=widths,
    align="edge",
    alpha=0.6,
    label="Usage"
)

ax1.set_xlabel("Billing period")
ax1.set_ylabel("Usage")
ax1.grid(True, axis="y", alpha=0.3)

# ------------------------------------------------------------
# Cost per usage
# Plot each value at the midpoint of its billing period.
# ------------------------------------------------------------

ax2 = ax1.twinx()

line = ax2.plot(
    midpoints,
    cost_per_usage,
    marker="o",
    linewidth=2,
    label="Cost per usage"
)

ax2.set_ylabel("Cost per usage (cents)")

# ------------------------------------------------------------
# Date formatting
# ------------------------------------------------------------

ax1.xaxis.set_major_locator(mdates.AutoDateLocator())

ax1.xaxis.set_major_formatter(
    mdates.ConciseDateFormatter(
        ax1.xaxis.get_major_locator()
    )
)

# Force the chart to exactly cover the available billing periods
ax1.set_xlim(
    min(starts),
    max(ends)
)

# ------------------------------------------------------------
# Legend / title
# ------------------------------------------------------------

handles = [bars, line[0]]
labels = ["Usage", "Cost per usage"]

ax1.legend(
    handles,
    labels,
    loc="upper left"
)

ax1.set_title(
    "Usage and Cost per Usage Over Time"
)

fig.tight_layout()

# ------------------------------------------------------------
# Save and display
# ------------------------------------------------------------

plt.savefig(
    OUTPUT_FILE,
    dpi=150,
    bbox_inches="tight"
)

plt.show()

print(f"Chart saved to {OUTPUT_FILE}")