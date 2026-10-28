"""
Adult diabetes prevalence: Pakistan, China, India, Bangladesh (2011 vs 2024)

Data: International Diabetes Federation (Diabetes Atlas), via World Bank,
      processed by Our World in Data
      https://ourworldindata.org/grapher/diabetes-prevalence
Unit: % of population aged 20-79

diabetes_selected_rows.csv contains the 8 rows used here, copied from the
downloaded "Download full data" CSV (row numbers are listed in the file).
"""
import pandas as pd
import matplotlib.pyplot as plt

# 1. Load and check ---------------------------------------------------
df = pd.read_csv("diabetes_selected_rows.csv")
print(df.info())
print("Missing values:\n", df.isna().sum())
print("Rows per country (should all be 2):\n", df.groupby("country").size())

# 2. Change table: 2024 minus 2011 ---------------------------------------
wide = df.pivot(index="country", columns="year", values="prevalence")
wide.columns = ["y2011", "y2024"]
wide["change"] = (wide["y2024"] - wide["y2011"]).round(1)
wide = wide.sort_values("y2024", ascending=False).reset_index()
print(wide)
wide.to_csv("change_table.csv", index=False)

# 3. Chart 1: 2011 vs 2024 ---------------------------------------------
fig, ax = plt.subplots(figsize=(8, 5))
for _, r in wide.iterrows():
    ax.plot([2011, 2024], [r["y2011"], r["y2024"]], marker="o", linewidth=2, label=r["country"])
    ax.annotate(f'{r["y2024"]}', (2024, r["y2024"]), textcoords="offset points", xytext=(8, -3))
    # 2011 labels are placed at spread-out heights so the close values stay readable
    y_text = {"Bangladesh": 10.7, "India": 9.6, "China": 8.6, "Pakistan": 7.5}[r["country"]]
    ax.text(2010.6, y_text, f'{r["y2011"]}', ha="right", va="center")
ax.set_xticks([2011, 2024])
ax.set_xlim(2009.5, 2025.5)
ax.set_ylim(5, 33)
ax.set_ylabel("% of population aged 20-79")
ax.set_title("Adult diabetes prevalence: 2011 vs 2024\n(estimates for two time points only)")
ax.legend(title="Country")
fig.text(0.01, 0.01, "Source: IDF Diabetes Atlas via World Bank, processed by Our World in Data",
         fontsize=7, color="gray")
ax.spines[["top", "right"]].set_visible(False)
fig.tight_layout(rect=(0, 0.03, 1, 1))
fig.savefig("chart1_2011_vs_2024.png", dpi=150)

# 4. Chart 2: 2024 comparison --------------------------------------------
fig, ax = plt.subplots(figsize=(8, 4.5))
order = wide.sort_values("y2024")
bars = ax.barh(order["country"], order["y2024"], color="#1F3864")
for b, v in zip(bars, order["y2024"]):
    ax.text(v + 0.4, b.get_y() + b.get_height() / 2, f"{v}", va="center")
ax.set_xlabel("% of population aged 20-79")
ax.set_title("Adult diabetes prevalence in 2024")
fig.text(0.01, 0.01, "Source: IDF Diabetes Atlas via World Bank, processed by Our World in Data",
         fontsize=7, color="gray")
ax.spines[["top", "right"]].set_visible(False)
fig.tight_layout(rect=(0, 0.03, 1, 1))
fig.savefig("chart2_2024.png", dpi=150)
print("Done.")
