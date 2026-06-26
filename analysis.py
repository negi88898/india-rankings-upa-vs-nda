"""
India Global Rankings — UPA (Manmohan Singh) vs NDA (Narendra Modi)
Data Analyst / Data Scientist portfolio script
Reads from india_rankings.db (SQLite) and produces charts + summary stats.
Sources: UNDP, World Bank, Transparency International, IEP (GTI), RSF, IQAir,
Henley & Partners, RBI. See README.md for full source table & caveats.
"""
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import os

DB = "india_rankings.db"
OUT = "charts"
os.makedirs(OUT, exist_ok=True)

conn = sqlite3.connect(DB)
df = pd.read_sql("SELECT * FROM india_rankings", conn)
df["Era"] = df["Year"].apply(lambda y: "UPA (Manmohan Singh)" if y < 2014 else "NDA (Narendra Modi)")

plt.style.use("seaborn-v0_8-whitegrid")
COLORS = {"UPA (Manmohan Singh)": "#1f77b4", "NDA (Narendra Modi)": "#ff7f0e"}

def lineplot(col, title, ylabel, fname, invert=False):
    fig, ax = plt.subplots(figsize=(10, 5))
    for era, sub in df.groupby("Era"):
        ax.plot(sub["Year"], sub[col], marker="o", label=era, color=COLORS[era])
    ax.axvline(2014, color="gray", linestyle="--", linewidth=1)
    ax.set_title(title, fontsize=13, fontweight="bold")
    ax.set_xlabel("Year"); ax.set_ylabel(ylabel)
    if invert: ax.invert_yaxis()
    ax.legend()
    fig.tight_layout()
    fig.savefig(f"{OUT}/{fname}.png", dpi=150)
    plt.close(fig)

lineplot("HDI_Rank", "India HDI World Rank (lower = better) — UNDP", "Rank", "01_hdi_rank", invert=True)
lineplot("Poverty_Rate_Pct", "India Poverty Rate (%) — World Bank", "% Population", "02_poverty")
lineplot("Unemployment_Rate_Pct", "India Unemployment Rate (%) — ILO/World Bank", "%", "03_unemployment")
lineplot("CPI_Score", "Corruption Perceptions Index Score — Transparency Intl (higher=cleaner)", "Score", "04_corruption")
lineplot("Passport_Rank_Henley", "Indian Passport World Rank (lower = better) — Henley Index", "Rank", "05_passport", invert=True)
lineplot("INR_per_USD", "Rupee vs US Dollar (annual avg) — RBI", "INR per 1 USD", "06_inr_usd")
lineplot("AQI_Avg_PM2.5", "India Avg PM2.5 (µg/m³) — IQAir", "µg/m³", "07_pollution")
lineplot("GTI_Score", "Global Terrorism Index Score — IEP (lower=safer)", "Score", "08_terrorism", invert=True)

summary = df.groupby("Era").agg(
    Avg_HDI_Rank=("HDI_Rank", "mean"),
    Avg_Poverty_Pct=("Poverty_Rate_Pct", "mean"),
    Avg_Unemployment_Pct=("Unemployment_Rate_Pct", "mean"),
    Avg_CPI_Score=("CPI_Score", "mean"),
    Avg_Passport_Rank=("Passport_Rank_Henley", "mean"),
    Avg_INR_per_USD=("INR_per_USD", "mean"),
).round(2)
summary.to_csv("upa_vs_nda_summary.csv")
print(summary)
print("\nCharts saved to ./charts/")
conn.close()
