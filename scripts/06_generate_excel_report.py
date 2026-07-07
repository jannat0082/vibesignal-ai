"""
CreatorIQ - Excel Report Generator
Module 4
"""
#  — starting with data loading and basic workbook structure


import pandas as pd
import numpy as np
import os
from openpyxl import Workbook
from openpyxl.styles import (
    PatternFill, Font, Alignment, Border, Side
)
from openpyxl.utils import get_column_letter
from openpyxl.chart import BarChart, Reference
from datetime import datetime

# paths — using abspath so this works from any directory
BASE_DIR   = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR   = os.path.join(BASE_DIR, "data")
OUTPUT_DIR = os.path.join(BASE_DIR, "notebooks")

# load all the data we need
creators          = pd.read_csv(os.path.join(DATA_DIR, "creators.csv"))
campaigns         = pd.read_csv(os.path.join(DATA_DIR, "campaigns.csv"))
campaign_creators = pd.read_csv(os.path.join(DATA_DIR, "campaign_creators.csv"))
posts             = pd.read_csv(os.path.join(DATA_DIR, "posts.csv"))
conversions       = pd.read_csv(os.path.join(DATA_DIR, "conversions.csv"))

print("Data loaded successfully.")

# ___Colours (hex without #)for the report
# note: openpyxl doesn't use # before hex codes, took me a bit to figure that out
GREEN_DARK  = "0F6E56"
GREEN_LIGHT = "E1F5EE"
BLUE_DARK   = "185FA5"
BLUE_LIGHT  = "E6F1FB"
RED_DARK    = "993C1D"
RED_LIGHT   = "FAECE7"
AMBER_LIGHT = "FAEEDA"
AMBER_DARK  = "854F0B"
GREY_HEADER = "2C2C2C"
WHITE       = "FFFFFF"
LIGHT_GREY  = "F5F5F5"

# helper functions to avoid repeating style code everywhere
# makes the sheet-building code much cleaner
def make_fill(hex_color):
    return PatternFill("solid", fgColor=hex_color)

def make_font(bold=False, color=WHITE, size=11):
    return Font(bold=bold, color=color, size=size)

def make_border():
    # light grey border — not too heavy, not invisible
    thin = Side(style="thin", color="DDDDDD")
    return Border(left=thin, right=thin, top=thin, bottom=thin)

def make_center():
    return Alignment(horizontal="center", vertical="center", wrap_text=True)

def make_left():
    return Alignment(horizontal="left", vertical="center", wrap_text=True)

def style_header_row(ws, row, col_start, col_end,
                     bg=GREY_HEADER, fg=WHITE, height=30):
    ws.row_dimensions[row].height = height
    for col in range(col_start, col_end + 1):
        cell = ws.cell(row=row, column=col)
        cell.fill      = make_fill(bg)
        cell.font      = make_font(bold=True, color=fg, size=11)
        cell.alignment = make_center()
        cell.border    = make_border()

def style_data_row(ws, row, col_start, col_end,
                   bg=WHITE, fg="2C2C2C", height=22):
    ws.row_dimensions[row].height = height
    for col in range(col_start, col_end + 1):
        cell = ws.cell(row=row, column=col)
        cell.fill      = make_fill(bg)
        cell.font      = Font(color=fg, size=10)
        cell.alignment = make_left()
        cell.border    = make_border()

def set_col_widths(ws, widths):
    for col, width in enumerate(widths, start=1):
        ws.column_dimensions[get_column_letter(col)].width = width

# --- compute all the metrics we need before building the sheets ---

# merge creator info into campaign_creators so we have tier/platform
cc = campaign_creators.merge(
    creators[["creator_id", "name", "tier", "platform", "niche"]],
    on="creator_id", how="left"
)
cc["roi_pct"] = (
    (cc["revenue_attributed"] - cc["creator_fee"])
    / cc["creator_fee"].replace(0, np.nan)
) * 100

# roll up to creator level — one row per creator across all campaigns
creator_summary = cc.groupby(
    ["creator_id", "name", "tier", "platform", "niche"]
).agg(
    total_fee     = ("creator_fee",        "sum"),
    total_revenue = ("revenue_attributed", "sum"),
    num_campaigns = ("campaign_id",        "nunique"),
    avg_roi       = ("roi_pct",            "mean"),
).reset_index()

creator_summary["roi_pct"] = (
    (creator_summary["total_revenue"] - creator_summary["total_fee"])
    / creator_summary["total_fee"].replace(0, np.nan)
) * 100
creator_summary = creator_summary.sort_values(
    "roi_pct", ascending=False
).reset_index(drop=True)

# campaign level summary
camp = campaigns.merge(
    cc.groupby("campaign_id").agg(
        total_fee     = ("creator_fee",        "sum"),
        total_revenue = ("revenue_attributed", "sum"),
        num_creators  = ("creator_id",         "nunique"),
    ).reset_index(),
    on="campaign_id", how="left"
)
camp["roi_pct"] = (
    (camp["total_revenue"] - camp["total_fee"])
    / camp["total_fee"].replace(0, np.nan)
) * 100
camp = camp.sort_values("roi_pct", ascending=False).reset_index(drop=True)

# top level KPIs for the executive summary sheet
total_revenue   = conversions["order_value"].sum()
total_orders    = len(conversions)
avg_order       = conversions["order_value"].mean()
top_platform    = posts.groupby("platform")["likes"].mean().idxmax()
top_format      = posts.groupby("content_format")["likes"].mean().idxmax()
top_creator_row = creator_summary.iloc[0]

print("Metrics computed.")

# --- start building the workbook ---
wb = Workbook()

# sheet 1: executive summary
# this is the overview page — KPIs and tier breakdown
ws1 = wb.active
ws1.title = "Executive Summary"
ws1.sheet_view.showGridLines = False

ws1.merge_cells("A1:F1")
ws1["A1"] = "CreatorIQ — Executive Summary Report"
ws1["A1"].fill      = make_fill(BLUE_DARK)
ws1["A1"].font      = Font(bold=True, color=WHITE, size=16)
ws1["A1"].alignment = make_center()
ws1.row_dimensions[1].height = 45

ws1.merge_cells("A2:F2")
ws1["A2"] = f"Generated: {datetime.now().strftime('%d %B %Y, %I:%M %p')}"
ws1["A2"].font      = Font(color="888888", size=10, italic=True)
ws1["A2"].alignment = make_center()
ws1.row_dimensions[2].height = 20

ws1.append([])

ws1.merge_cells("A4:F4")
ws1["A4"] = "KEY PERFORMANCE INDICATORS"
ws1["A4"].fill      = make_fill(GREY_HEADER)
ws1["A4"].font      = Font(bold=True, color=WHITE, size=11)
ws1["A4"].alignment = make_center()
ws1.row_dimensions[4].height = 28

kpi_headers = ["Metric", "Value", "", "Metric", "Value", ""]
for col, val in enumerate(kpi_headers, start=1):
    cell = ws1.cell(row=5, column=col, value=val)
    cell.fill      = make_fill(BLUE_LIGHT)
    cell.font      = Font(bold=True, color=BLUE_DARK, size=10)
    cell.alignment = make_center()
    cell.border    = make_border()
ws1.row_dimensions[5].height = 22

kpi_data = [
    ("Total Revenue",       f"${total_revenue:,.2f}",
     "", "Total Conversions",  f"{total_orders:,}",     ""),
    ("Average Order Value", f"${avg_order:.2f}",
     "", "Best Platform",      top_platform.title(),     ""),
    ("Best Content Format", top_format.title(),
     "", "Top Creator",        top_creator_row["name"],  ""),
    ("Top Creator ROI",     f"{top_creator_row['roi_pct']:.1f}%",
     "", "Total Creators",     "200",                    ""),
    ("Total Campaigns",     "70",
     "", "Total Posts",        "783",                    ""),
]

for r, row_data in enumerate(kpi_data, start=6):
    ws1.row_dimensions[r].height = 24
    for c, val in enumerate(row_data, start=1):
        cell = ws1.cell(row=r, column=c, value=val)
        cell.border    = make_border()
        cell.alignment = make_left()
        if c in (1, 4):
            cell.fill = make_fill(LIGHT_GREY)
            cell.font = Font(bold=True, color=GREY_HEADER, size=10)
        elif c in (2, 5):
            cell.fill = make_fill(GREEN_LIGHT)
            cell.font = Font(bold=True, color=GREEN_DARK, size=11)
        else:
            cell.fill = make_fill(WHITE)

ws1.append([])

# tier breakdown — useful for seeing which tier performs best overall
ws1.merge_cells("A12:F12")
ws1["A12"] = "PERFORMANCE BY CREATOR TIER"
ws1["A12"].fill      = make_fill(GREY_HEADER)
ws1["A12"].font      = Font(bold=True, color=WHITE, size=11)
ws1["A12"].alignment = make_center()
ws1.row_dimensions[12].height = 28

tier_headers = ["Tier", "Creators", "Avg Fee ($)",
                "Avg Revenue ($)", "Avg ROI (%)", "Campaigns"]
for col, val in enumerate(tier_headers, start=1):
    cell = ws1.cell(row=13, column=col, value=val)
    cell.fill      = make_fill(BLUE_LIGHT)
    cell.font      = Font(bold=True, color=BLUE_DARK, size=10)
    cell.alignment = make_center()
    cell.border    = make_border()
ws1.row_dimensions[13].height = 22

tier_stats = cc.groupby("tier").agg(
    creators  = ("creator_id",        "nunique"),
    avg_fee   = ("creator_fee",        "mean"),
    avg_rev   = ("revenue_attributed", "mean"),
    avg_roi   = ("roi_pct",            "mean"),
    campaigns = ("campaign_id",        "nunique"),
).reindex(["nano", "micro", "macro", "mega"]).reset_index()

# each tier gets its own background color
tier_colors = {
    "nano":  GREEN_LIGHT,
    "micro": BLUE_LIGHT,
    "macro": AMBER_LIGHT,
    "mega":  RED_LIGHT,
}

for r, (_, row) in enumerate(tier_stats.iterrows(), start=14):
    ws1.row_dimensions[r].height = 22
    row_vals = [
        row["tier"].title(),
        int(row["creators"]),
        round(row["avg_fee"], 2),
        round(row["avg_rev"], 2),
        round(row["avg_roi"], 1),
        int(row["campaigns"]),
    ]
    bg = tier_colors.get(row["tier"], WHITE)
    for c, val in enumerate(row_vals, start=1):
        cell = ws1.cell(row=r, column=c, value=val)
        cell.fill      = make_fill(bg)
        cell.font      = Font(color=GREY_HEADER, size=10)
        cell.alignment = make_center()
        cell.border    = make_border()

set_col_widths(ws1, [22, 14, 14, 16, 14, 12])

# sheet 2: creator performance
# ranked by ROI — color coded so it's easy to spot who to scale vs drop
ws2 = wb.create_sheet("Creator Performance")
ws2.sheet_view.showGridLines = False

ws2.merge_cells("A1:H1")
ws2["A1"] = "Creator Performance — Ranked by ROI"
ws2["A1"].fill      = make_fill(GREEN_DARK)
ws2["A1"].font      = Font(bold=True, color=WHITE, size=14)
ws2["A1"].alignment = make_center()
ws2.row_dimensions[1].height = 40

headers2 = [
    "Rank", "Creator Name", "Tier", "Platform",
    "Niche", "Total Fee ($)", "Total Revenue ($)", "ROI (%)"
]
for col, val in enumerate(headers2, start=1):
    cell = ws2.cell(row=2, column=col, value=val)
    cell.fill      = make_fill(GREY_HEADER)
    cell.font      = Font(bold=True, color=WHITE, size=10)
    cell.alignment = make_center()
    cell.border    = make_border()
ws2.row_dimensions[2].height = 25

# color code by ROI threshold
# green = scale, blue = solid, amber = watch, red = stop
for r, (_, row) in enumerate(creator_summary.iterrows(), start=3):
    roi = row["roi_pct"]

    if roi >= 150:
        bg = GREEN_LIGHT
        fg = GREEN_DARK
    elif roi >= 50:
        bg = BLUE_LIGHT
        fg = BLUE_DARK
    elif roi >= 0:
        bg = AMBER_LIGHT
        fg = AMBER_DARK
    else:
        bg = RED_LIGHT
        fg = RED_DARK

    if (r - 3) % 2 == 1 and bg == WHITE:
        bg = LIGHT_GREY

    row_vals = [
        r - 2,
        row["name"],
        row["tier"].title(),
        row["platform"].title(),
        row["niche"].title(),
        round(row["total_fee"], 2),
        round(row["total_revenue"], 2),
        round(roi, 1),
    ]
    ws2.row_dimensions[r].height = 20
    for c, val in enumerate(row_vals, start=1):
        cell = ws2.cell(row=r, column=c, value=val)
        cell.fill      = make_fill(bg)
        cell.font      = Font(color=fg, size=10)
        cell.alignment = make_center()
        cell.border    = make_border()

set_col_widths(ws2, [7, 22, 10, 12, 12, 14, 16, 10])

# sheet 3: campaign summary
# same color coding logic as creator sheet
ws3 = wb.create_sheet("Campaign Summary")
ws3.sheet_view.showGridLines = False

ws3.merge_cells("A1:H1")
ws3["A1"] = "Campaign Summary — Ranked by ROI"
ws3["A1"].fill      = make_fill(AMBER_DARK)
ws3["A1"].font      = Font(bold=True, color=WHITE, size=14)
ws3["A1"].alignment = make_center()
ws3.row_dimensions[1].height = 40

headers3 = [
    "Rank", "Campaign Name", "Objective", "Status",
    "Budget ($)", "Revenue ($)", "Creators", "ROI (%)"
]
for col, val in enumerate(headers3, start=1):
    cell = ws3.cell(row=2, column=col, value=val)
    cell.fill      = make_fill(GREY_HEADER)
    cell.font      = Font(bold=True, color=WHITE, size=10)
    cell.alignment = make_center()
    cell.border    = make_border()
ws3.row_dimensions[2].height = 25

for r, (_, row) in enumerate(camp.iterrows(), start=3):
    roi = row["roi_pct"] if not pd.isna(row["roi_pct"]) else 0

    if roi >= 150:
        bg = GREEN_LIGHT
    elif roi >= 50:
        bg = BLUE_LIGHT
    elif roi >= 0:
        bg = AMBER_LIGHT
    else:
        bg = RED_LIGHT

    row_vals = [
        r - 2,
        row["campaign_name"],
        row["objective"].title() if not pd.isna(row["objective"]) else "N/A",
        row["status"].title() if not pd.isna(row["status"]) else "N/A",
        round(row["total_budget"], 2),
        round(row["total_revenue"], 2) if not pd.isna(row["total_revenue"]) else 0,
        int(row["num_creators"]) if not pd.isna(row["num_creators"]) else 0,
        round(roi, 1),
    ]
    ws3.row_dimensions[r].height = 20
    for c, val in enumerate(row_vals, start=1):
        cell = ws3.cell(row=r, column=c, value=val)
        cell.fill      = make_fill(bg)
        cell.font      = Font(color=GREY_HEADER, size=10)
        cell.alignment = make_center()
        cell.border    = make_border()

set_col_widths(ws3, [7, 30, 14, 12, 14, 14, 10, 10])

# save the file with today's date in the name
# so old reports don't get overwritten
filename = f"CreatorIQ_Report_{datetime.now().strftime('%Y%m%d')}.xlsx"
out_path = os.path.join(OUTPUT_DIR, filename)
wb.save(out_path)

print()
print("=" * 50)
print("report saved:", filename)
print("location:", out_path)
print()
print("sheets:")
print("  1. Executive Summary")
print("  2. Creator Performance")
print("  3. Campaign Summary")
print()
print("color coding:")
print("  green  — ROI above 150%  (scale)")
print("  blue   — ROI 50-150%     (solid)")
print("  amber  — ROI 0-50%       (watch)")
print("  red    — ROI negative    (stop)")


